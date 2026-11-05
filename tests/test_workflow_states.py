"""Team workflow contracts, verified against disposable SQLite databases only."""
import json
import tempfile
import unittest
from pathlib import Path

from linearboard.contracts import capabilities
from linearboard.store import Invalid, STATUSES, Store

EXPECTED_DEFAULTS = ['Backlog', 'Todo', 'In Progress', 'In Review', 'Done', 'Canceled', 'Duplicate']


class TeamWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'workflow.sqlite3'
        self.store = Store(self.path)
        self.team = self.store.snapshot()['teams'][0]
        self.project = self.create('projects', name='Disposable workflow', team_id=self.team['id'])

    def tearDown(self):
        self.temp.cleanup()

    def create(self, kind, **fields):
        return self.store.mutate(kind, fields)

    def update(self, kind, record, **fields):
        return self.store.mutate(kind, {'expected_version': record['version'], **fields}, record['id'])

    def issue(self, **fields):
        return self.create('issues', title='Workflow check', project_id=self.project['id'], **fields)

    def custom_team(self):
        team = self.create('teams', name='Custom workflow', key='QA', statuses=['Queued', 'Working', 'Reviewed', 'Done'])
        project = self.create('projects', name='Custom project', team_id=team['id'])
        return team, project

    def make_legacy_team(self):
        # Simulate a database produced by the previous application version.
        # No production database or migration side effect is involved.
        with self.store.connect() as db:
            team = json.loads(db.execute('SELECT data FROM records WHERE id=?', (self.team['id'],)).fetchone()[0])
            team.pop('statuses')
            db.execute('UPDATE records SET data=? WHERE id=?', (json.dumps(team), self.team['id']))

    def test_default_workflow_matches_observed_linear_and_duplicate_round_trips(self):
        self.assertEqual(STATUSES, EXPECTED_DEFAULTS)
        self.assertEqual(self.team['statuses'], EXPECTED_DEFAULTS)
        issue = self.issue(status='Duplicate')
        self.assertEqual(self.store.get('issues', issue['id'])['status'], 'Duplicate')
        snapshot = self.store.snapshot()
        self.assertEqual(snapshot['statuses'], EXPECTED_DEFAULTS)
        self.assertEqual(snapshot['statuses_by_team'][self.team['id']], EXPECTED_DEFAULTS)
        for status in ['Ready for Test', 'Blocked']:
            with self.subTest(status=status), self.assertRaises(Invalid):
                self.issue(status=status)

    def test_custom_team_isolated_and_default_issue_uses_available_status(self):
        team, project = self.custom_team()
        issue = self.create('issues', title='Custom task', project_id=project['id'])
        design = self.create('issues', title='Custom design', project_id=project['id'], category='Design')
        self.assertEqual(issue['status'], 'Queued')
        self.assertEqual(design['status'], 'Queued')
        self.assertEqual(self.issue()['status'], 'Backlog')
        self.assertEqual(self.issue(category='Design')['status'], 'Todo')
        self.assertEqual(self.store.snapshot()['statuses_by_team'][team['id']], team['statuses'])
        with self.assertRaises(Invalid):
            self.create('issues', title='Wrong workflow', project_id=project['id'], status='Backlog')
        with self.assertRaises(Invalid):
            self.issue(status='Working')

    def test_unknown_status_update_is_atomic_and_does_not_add_history(self):
        issue = self.issue()
        before = self.store.snapshot()
        history = self.store.history(issue['id'])
        with self.assertRaises(Invalid):
            self.update('issues', issue, status='Unknown', body='Must not be persisted')
        self.assertEqual(self.store.snapshot(), before)
        self.assertEqual(self.store.history(issue['id']), history)

    def test_view_filters_use_owning_project_team_workflow(self):
        team, project = self.custom_team()
        issue = self.create('issues', title='Visible custom task', project_id=project['id'], status='Working')
        view = self.create('views', name='Custom active', project_id=project['id'], statuses=['Working'])
        self.assertEqual([i['id'] for i in self.store.view_members(view['id'])], [issue['id']])
        with self.assertRaises(Invalid):
            self.create('views', name='Wrong team filter', project_id=self.project['id'], statuses=['Working'])
        with self.assertRaises(Invalid):
            self.update('views', view, statuses=['In Progress'])
        for statuses in ['Working', None, {'Working': True}]:
            with self.subTest(statuses=statuses), self.assertRaises(Invalid):
                self.update('views', view, statuses=statuses)
        empty = self.update('views', view, statuses=[])
        self.assertEqual(self.store.view_members(empty['id'])[0]['id'], issue['id'])

    def test_workflow_cannot_remove_status_used_by_issue(self):
        issue = self.issue(status='Duplicate')
        before = self.store.get('teams', self.team['id'])
        history = self.store.history(self.team['id'])
        with self.assertRaises(Invalid):
            self.update('teams', before, statuses=[s for s in EXPECTED_DEFAULTS if s != 'Duplicate'])
        self.assertEqual(self.store.get('teams', self.team['id']), before)
        self.assertEqual(self.store.history(self.team['id']), history)

    def test_workflow_cannot_remove_status_used_only_by_view(self):
        view = self.create('views', name='Review filter', project_id=self.project['id'], statuses=['In Review'])
        with self.assertRaises(Invalid):
            self.update('teams', self.team, statuses=[s for s in EXPECTED_DEFAULTS if s != 'In Review'])
        # An unused state may be removed and the new contract survives reopening.
        updated = self.update('teams', self.team, statuses=[s for s in EXPECTED_DEFAULTS if s != 'Duplicate'])
        self.store = Store(self.path)
        self.assertEqual(self.store.get('teams', self.team['id'])['statuses'], updated['statuses'])

    def test_invalid_workflow_shapes_are_rejected(self):
        for statuses in [[], None, 'Backlog', ['Backlog', 'Backlog'], [''], [' Backlog'], ['Backlog '], [7], [{}]]:
            with self.subTest(statuses=statuses), self.assertRaises(Invalid):
                self.update('teams', self.team, statuses=statuses)
        self.assertEqual(self.store.get('teams', self.team['id'])['statuses'], EXPECTED_DEFAULTS)

    def test_legacy_team_fallback_does_not_rewrite_record_or_history(self):
        self.make_legacy_team()
        before = self.store.get('teams', self.team['id'])
        history = self.store.history(self.team['id'])
        self.store = Store(self.path)
        self.assertNotIn('statuses', self.store.get('teams', self.team['id']))
        self.assertEqual(self.store.snapshot()['statuses_by_team'][self.team['id']], EXPECTED_DEFAULTS)
        self.assertEqual(self.store.get('teams', self.team['id']), before)
        self.assertEqual(self.store.history(self.team['id']), history)
        self.assertEqual(self.issue()['status'], 'Backlog')

    def test_legacy_referenced_state_is_preserved_without_adding_unused_defaults(self):
        self.make_legacy_team()
        issue = self.issue()
        with self.store.connect() as db:
            issue['status'] = 'Blocked'
            db.execute('UPDATE records SET data=? WHERE id=?', (json.dumps(issue), issue['id']))
        self.store = Store(self.path)
        effective = self.store.snapshot()['statuses_by_team'][self.team['id']]
        self.assertEqual(effective, EXPECTED_DEFAULTS + ['Blocked'])
        self.assertNotIn('Ready for Test', effective)
        updated = self.update('issues', issue, body='Legacy metadata remains editable')
        self.assertEqual(updated['status'], 'Blocked')
        with self.assertRaises(Invalid):
            self.update('teams', self.store.get('teams', self.team['id']), statuses=EXPECTED_DEFAULTS)

    def test_legacy_view_reference_is_preserved_on_restart(self):
        view = self.create('views', name='Legacy filter', project_id=self.project['id'], statuses=[])
        self.make_legacy_team()
        with self.store.connect() as db:
            view['statuses'] = ['Ready for Test']
            db.execute('UPDATE records SET data=? WHERE id=?', (json.dumps(view), view['id']))
        self.store = Store(self.path)
        self.assertEqual(self.store.snapshot()['statuses_by_team'][self.team['id']], EXPECTED_DEFAULTS + ['Ready for Test'])
        with self.assertRaises(Invalid):
            self.update('teams', self.store.get('teams', self.team['id']), statuses=EXPECTED_DEFAULTS)

    def test_custom_done_still_requires_user_and_metadata_keeps_done(self):
        team, project = self.custom_team()
        issue = self.create('issues', title='Acceptance gate', project_id=project['id'])
        with self.assertRaises(Invalid):
            self.update('issues', issue, status='Done')
        done = self.store.mutate('issues', {'expected_version':issue['version'], 'status':'Done'}, issue['id'], actor='user')
        updated = self.update('issues', done, body='Metadata synchronization')
        self.assertEqual(updated['status'], 'Done')

    def test_capabilities_describe_team_state_contract(self):
        contract = capabilities()
        self.assertIn('statuses_by_team', contract['snapshot_fields'])
        self.assertIn('statuses', contract['resources']['teams']['fields'])
        self.assertIn('team', contract['resources']['issues']['fields']['status'])
        self.assertNotIn('Ready for Test', contract['resources']['issues']['fields']['status'])


if __name__ == '__main__':
    unittest.main()
