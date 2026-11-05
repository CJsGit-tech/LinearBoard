"""Atomic multi-ticket workflow changes, with no production data."""
import tempfile
import unittest
from pathlib import Path
from linearboard.store import Store, Invalid, Conflict


class BulkStatusTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.tmp.name) / 'bulk.sqlite3')
        team = self.store.snapshot()['teams'][0]
        self.project = self.store.mutate('projects', {'name':'QA', 'team_id':team['id']})
        self.issues = [self.store.mutate('issues', {'project_id':self.project['id'], 'title':f'QA {n}', 'category':'FrontEnd'}) for n in range(3)]

    def tearDown(self):
        self.tmp.cleanup()

    def payload(self, status='In Progress', issues=None):
        rows = self.issues if issues is None else issues
        return {'issue_ids':[r['id'] for r in rows], 'expected_versions':{r['id']:r['version'] for r in rows}, 'status':status}

    def test_status_group_move_preserves_identity_fields_and_history(self):
        result = self.store.update_issue_statuses(self.payload(), actor='user')
        self.assertEqual(result['updated'], 3)
        for before, after in zip(self.issues, result['items']):
            for field in ['id','identifier','project_id','team_id','label_ids','title','body','url']:
                self.assertEqual(after.get(field), before.get(field))
            self.assertEqual(after['status'], 'In Progress')
            self.assertEqual(after['version'], before['version'] + 1)
            self.assertEqual(self.store.history(after['id'])[0]['before_data']['status'], 'Backlog')
        self.assertEqual(Store(self.store.path).get('issues', self.issues[0]['id'])['status'], 'In Progress')

    def test_stale_last_record_rolls_back_every_record(self):
        last = self.issues[-1]
        self.store.mutate('issues', {'expected_version':last['version'], 'body':'external update'}, last['id'])
        with self.assertRaises(Conflict):
            self.store.update_issue_statuses(self.payload(), actor='user')
        for issue in self.issues:
            current = self.store.get('issues', issue['id'])
            self.assertEqual(current['status'], 'Backlog')
            self.assertEqual(current['version'], 2 if issue['id']==last['id'] else 1)

    def test_invalid_state_and_automation_done_leave_all_unchanged(self):
        for status, actor in [('Unknown','user'), ('Done','automation')]:
            with self.assertRaises(Invalid):
                self.store.update_issue_statuses(self.payload(status), actor=actor)
        self.assertTrue(all(self.store.get('issues', i['id'])['version']==1 for i in self.issues))
        self.assertEqual(self.store.update_issue_statuses(self.payload('Done'), actor='user')['updated'],3)

    def test_replay_and_same_status_do_not_duplicate_history(self):
        payload = self.payload()
        first = self.store.update_issue_statuses(payload, actor='user', key='bulk-1')
        self.assertEqual(self.store.update_issue_statuses(payload, actor='user', key='bulk-1'), first)
        rows = first['items']
        self.assertEqual(self.store.update_issue_statuses(self.payload(issues=rows), actor='user')['updated'],0)
        self.assertTrue(all(len(self.store.history(r['id']))==2 for r in rows))
        with self.assertRaises(Conflict):
            self.store.update_issue_statuses(self.payload('Todo', rows), actor='user', key='bulk-1')

    def test_incomplete_versions_duplicates_and_extra_fields_are_rejected(self):
        payload = self.payload()
        for invalid in [{**payload,'expected_versions':{}}, {**payload,'issue_ids':payload['issue_ids']*2}, {**payload,'title':'no'}, {**payload,'expected_versions':{**payload['expected_versions'],'other':1}}]:
            with self.assertRaises(Invalid):
                self.store.update_issue_statuses(invalid, actor='user')
        self.assertTrue(all(self.store.get('issues', i['id'])['version']==1 for i in self.issues))

    def test_trashed_issue_and_mixed_projects_are_rejected(self):
        last = self.issues[-1]
        impact = self.store.trash_impact('issues', last['id'])
        self.store.trash_move('issues', last['id'], impact['fingerprint'])
        with self.assertRaises(Invalid):
            self.store.update_issue_statuses(self.payload(), actor='user')
        other = self.store.mutate('projects', {'name':'other', 'team_id':self.project['team_id']})
        issue = self.store.mutate('issues', {'project_id':other['id'],'title':'other','category':'FrontEnd'})
        with self.assertRaises(Invalid):
            self.store.update_issue_statuses(self.payload(issues=[self.issues[0],issue]), actor='user')
        self.assertEqual(self.store.get('issues', self.issues[0]['id'])['version'],1)
