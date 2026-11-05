"""Trash transactions use a disposable database and preserve unrelated data."""
import tempfile
import unittest
from pathlib import Path
from linearboard.store import Store, Invalid, Conflict


class TrashStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / 'trash.sqlite')
        self.team = self.store.snapshot()['teams'][0]
        self.project = self.store.mutate('projects', {'team_id': self.team['id'], 'name': 'QA'})
        self.milestone = self.store.mutate('milestones', {'project_id': self.project['id'], 'name': 'M1'})
        self.parent = self.issue('Parent')
        self.child = self.issue('Child', parent_id=self.parent['id'])
        self.grandchild = self.issue('Grandchild', parent_id=self.child['id'])
        self.other = self.issue('Other')
        self.relation = self.store.mutate('relations', {'source_id': self.parent['id'], 'target_id': self.other['id'], 'relation': 'blocks'})
        self.comment = self.store.mutate('comments', {'target_kind': 'issues', 'target_id': self.child['id'], 'body': 'Original'})

    def tearDown(self):
        self.temp.cleanup()

    def issue(self, title, **fields):
        return self.store.mutate('issues', {'project_id': self.project['id'], 'milestone_id': self.milestone['id'],
                                            'title': title, 'category': 'FrontEnd', **fields})

    def move(self, kind, record):
        impact = self.store.trash_impact(kind, record['id'])
        return self.store.trash_move(kind, record['id'], impact['fingerprint'])

    def test_subtree_restores_relations(self):
        result = self.move('issues', self.parent)
        self.assertEqual(result['deleted'], 5)
        self.assertEqual([r['id'] for r in self.store.snapshot(True)['issues']], [self.other['id']])
        with self.assertRaises(Invalid):
            self.store.get('issues', self.child['id'])
        self.assertEqual(self.store.trash_list()[0]['count'], 5)
        self.assertEqual(self.store.trash_restore(result['batch_id'])['restored'], 5)
        self.assertEqual(self.store.get('issues', self.child['id'])['parent_id'], self.parent['id'])
        self.assertFalse(self.store.get('issues', self.grandchild['id'])['archived'])
        self.assertEqual(self.store.get('relations', self.relation['id'])['target_id'], self.other['id'])
        self.assertEqual(self.store.get('comments', self.comment['id'])['body'], 'Original')
        self.assertFalse(self.store.trash_list())

    def test_milestone_detachment_is_reversible_without_overwriting_new_choice(self):
        result = self.move('milestones', self.milestone)
        current = self.store.get('issues', self.parent['id'])
        self.assertEqual(current['milestone_id'], '')
        replacement = self.store.mutate('milestones', {'project_id': self.project['id'], 'name': 'M2'})
        self.store.mutate('issues', {'expected_version': current['version'], 'milestone_id': replacement['id']}, current['id'])
        restored = self.store.trash_restore(result['batch_id'])
        self.assertIn(current['id'], restored['unrestored_links'])
        self.assertEqual(self.store.get('issues', current['id'])['milestone_id'], replacement['id'])
        self.assertEqual(self.store.get('issues', self.child['id'])['milestone_id'], self.milestone['id'])

    def test_stale_preview_rejects_whole_transaction(self):
        impact = self.store.trash_impact('issues', self.parent['id'])
        self.store.mutate('issues', {'expected_version': 1, 'title': 'changed'}, self.child['id'])
        with self.assertRaises(Conflict):
            self.store.trash_move('issues', self.parent['id'], impact['fingerprint'])
        self.assertFalse(self.store.trash_list())
        self.assertEqual(len(self.store.snapshot()['issues']), 4)

    def test_shared_batch_keeps_other_issues_and_recovers_deleted_references(self):
        batch = self.store.mutate('batches', {'project_id': self.project['id'], 'name': 'Batch',
                                             'issue_ids': [self.parent['id'], self.other['id']]})
        deleted = self.move('issues', self.parent)
        self.assertEqual(self.store.get('batches', batch['id'])['issue_ids'], [self.other['id']])
        self.store.trash_restore(deleted['batch_id'])
        self.assertEqual(self.store.get('batches', batch['id'])['issue_ids'], [self.parent['id'], self.other['id']])

    def test_empty_batch_stays_editable_when_its_last_issue_is_trashed(self):
        batch = self.store.mutate('batches', {'project_id': self.project['id'], 'name': 'Batch',
                                             'issue_ids': [self.parent['id']]})
        deleted = self.move('issues', self.parent)
        current = self.store.get('batches', batch['id'])
        self.assertEqual(current['issue_ids'], [])
        self.store.mutate('batches', {'expected_version': current['version'], 'name': 'Updated'}, batch['id'])
        self.store.trash_restore(deleted['batch_id'])
        self.assertEqual(self.store.get('batches', batch['id'])['issue_ids'], [self.parent['id']])

    def test_multi_selection_is_atomic_and_deduplicates_descendants(self):
        selected = [self.child['id'], self.parent['id'], self.other['id']]
        impact = self.store.trash_impact('issues', selected)
        result = self.store.trash_move('issues', selected, impact['fingerprint'])
        self.assertEqual(result['deleted'], 6)  # Four issues, relation and comment.
        self.assertEqual(self.store.trash_list()[0]['root_ids'], selected)
        self.assertEqual(self.store.snapshot()['issues'], [])
        self.assertEqual(self.store.trash_restore(result['batch_id'])['restored'], 6)
        self.assertEqual(len(self.store.snapshot()['issues']), 4)

    def test_multi_selection_rejects_duplicates_other_projects_and_stale_preview(self):
        selected = [self.parent['id'], self.other['id']]
        impact = self.store.trash_impact('issues', selected)
        self.store.mutate('issues', {'expected_version': 1, 'title': 'Changed'}, self.other['id'])
        with self.assertRaises(Conflict):
            self.store.trash_move('issues', selected, impact['fingerprint'])
        with self.assertRaises(Invalid):
            self.store.trash_impact('issues', [self.parent['id'], self.parent['id']])
        project = self.store.mutate('projects', {'team_id': self.team['id'], 'name': 'Other project'})
        other = self.store.mutate('issues', {'project_id': project['id'], 'title': 'Other'})
        with self.assertRaises(Invalid):
            self.store.trash_impact('issues', [self.parent['id'], other['id']])
        self.assertFalse(self.store.trash_list())

    def test_trash_move_and_restore_retry_exact_request(self):
        selected = [self.parent['id'], self.child['id']]
        fingerprint = self.store.trash_impact('issues', selected)['fingerprint']
        first = self.store.trash_move('issues', selected, fingerprint, actor='automation', key='move-key')
        self.assertEqual(self.store.trash_move('issues', selected, fingerprint, actor='automation', key='move-key'), first)
        self.assertEqual(len(self.store.trash_list()), 1)
        with self.assertRaises(Conflict):
            self.store.trash_move('issues', [self.other['id']], fingerprint, actor='automation', key='move-key')
        restored = self.store.trash_restore(first['batch_id'], actor='automation', key='restore-key')
        self.assertEqual(self.store.trash_restore(first['batch_id'], actor='automation', key='restore-key'), restored)
        with self.assertRaises(Conflict):
            self.store.trash_move('issues', selected, fingerprint, actor='automation', key='move-key')

    def test_restoring_child_requires_trashed_project_first(self):
        child_batch = self.move('issues', self.parent)
        project_batch = self.move('projects', self.project)
        with self.assertRaises(Invalid):
            self.store.trash_restore(child_batch['batch_id'])
        self.store.trash_restore(project_batch['batch_id'])
        self.store.trash_restore(child_batch['batch_id'])
        self.assertEqual(self.store.get('issues', self.child['id'])['parent_id'], self.parent['id'])

    def test_regular_patch_cannot_forge_trash_metadata(self):
        with self.assertRaises(Invalid):
            self.store.mutate('issues', {'expected_version': 1, 'deleted_at': 'fake'}, self.parent['id'])

    def test_create_replay_does_not_return_a_trashed_record(self):
        payload = {'project_id': self.project['id'], 'title': 'Retry', 'category': 'FrontEnd'}
        record = self.store.mutate('issues', payload, key='retry-key')
        batch = self.move('issues', record)
        with self.assertRaises(Conflict):
            self.store.mutate('issues', payload, key='retry-key')
        self.store.trash_restore(batch['batch_id'])
        self.assertEqual(self.store.mutate('issues', payload, key='retry-key')['id'], record['id'])

    def test_purge_removes_record_history_and_preserves_idempotency_guard(self):
        payload = {'project_id': self.project['id'], 'title': 'Disposable', 'category': 'FrontEnd'}
        record = self.store.mutate('issues', payload, key='purged-key')
        batch = self.move('issues', record)
        self.assertEqual(self.store.trash_purge([batch['batch_id']])['purged'], 1)
        self.assertEqual(self.store.history(record['id']), [])
        with self.assertRaises(Invalid):
            self.store.get('issues', record['id'])
        with self.assertRaises(Conflict):
            self.store.mutate('issues', payload, key='purged-key')

    def test_purge_parent_blocked_by_separately_trashed_children(self):
        child_batch = self.move('issues', self.parent)
        project_batch = self.move('projects', self.project)
        with self.assertRaises(Conflict):
            self.store.trash_purge([project_batch['batch_id']])
        result = self.store.trash_purge([child_batch['batch_id'], project_batch['batch_id']])
        self.assertGreater(result['purged'], 0)
        self.assertEqual(self.store.trash_list(), [])


if __name__ == '__main__':
    unittest.main()
