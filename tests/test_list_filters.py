"""Exact-array and scalar-membership filtering use disposable application records."""
import tempfile
import unittest
from pathlib import Path

from linearboard.store import Invalid, Store


class ListFilterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / 'filters.sqlite3')
        self.team = self.store.snapshot()['teams'][0]
        self.project = self.store.mutate('projects', {'name':'Filter QA','team_id':self.team['id']})
        self.issues = [self.store.mutate('issues', {'project_id':self.project['id'],'title':'Task '+str(n)}) for n in range(3)]

    def tearDown(self):
        self.temp.cleanup()

    def batch(self, name, ids):
        return self.store.mutate('batches', {'project_id':self.project['id'],'name':name,'issue_ids':ids})

    def test_dispatch_filter_accepts_exact_array_and_scalar_member(self):
        issue = self.issues[0]
        dispatch = self.store.mutate('dispatches', {'project_id':self.project['id'],'issue_ids':[issue['id']]})
        for value in [[issue['id']], issue['id']]:
            with self.subTest(value=value):
                result = self.store.list('dispatches', {'issue_ids':value})
                self.assertEqual([r['id'] for r in result['items']], [dispatch['id']])
        self.assertEqual(self.store.list('dispatches', {'issue_ids':[]})['total'], 0)

    def test_array_equality_is_ordered_and_does_not_mean_subset(self):
        first, second = [issue['id'] for issue in self.issues[:2]]
        forward = self.batch('Forward', [first, second])
        reverse = self.batch('Reverse', [second, first])
        single = self.batch('Single', [first])
        self.assertEqual([r['id'] for r in self.store.list('batches', {'issue_ids':[first,second]})['items']], [forward['id']])
        self.assertEqual([r['id'] for r in self.store.list('batches', {'issue_ids':[second,first]})['items']], [reverse['id']])
        self.assertEqual([r['id'] for r in self.store.list('batches', {'issue_ids':[first]})['items']], [single['id']])
        self.assertEqual(self.store.list('batches', {'issue_ids':first})['total'], 3)

    def test_label_scalar_membership_and_scalar_fields_remain_unchanged(self):
        one = self.store.mutate('labels', {'team_id':self.team['id'],'name':'US1'})
        two = self.store.mutate('labels', {'team_id':self.team['id'],'name':'US2'})
        issue = self.store.mutate('issues', {'project_id':self.project['id'],'title':'Labeled task','label_ids':[one['id'],two['id']]})
        self.assertEqual([r['id'] for r in self.store.list('issues', {'label_ids':one['id'],'project_id':self.project['id']})['items']], [issue['id']])
        self.assertEqual([r['id'] for r in self.store.list('issues', {'label_ids':issue['label_ids']})['items']], [issue['id']])
        self.assertEqual(self.store.list('issues', {'label_ids':[one['id']]})['total'], 0)
        self.assertEqual(self.store.list('issues', {'title':'Labeled task'})['total'], 1)
        self.assertEqual(self.store.list('issues', {'title':['Labeled task']})['total'], 0)

    def test_filters_apply_before_pagination(self):
        issue_id = self.issues[0]['id']
        for n in range(5):
            self.batch('Batch '+str(n), [issue_id])
        self.batch('Not a member', [self.issues[1]['id']])
        first = self.store.list('batches', {'issue_ids':[issue_id]}, limit=2)
        second = self.store.list('batches', {'issue_ids':[issue_id]}, cursor=first['next_cursor'], limit=2)
        last = self.store.list('batches', {'issue_ids':[issue_id]}, cursor=second['next_cursor'], limit=2)
        self.assertEqual(first['total'], 5)
        self.assertEqual(len(first['items']) + len(second['items']) + len(last['items']), 5)
        self.assertIsNone(last['next_cursor'])

    def test_invalid_filter_container_is_normal_validation_error(self):
        before = self.store.snapshot()
        for filters in [[], '', 'not-an-object', 4, True]:
            with self.subTest(filters=filters), self.assertRaises(Invalid):
                self.store.list('issues', filters)
        self.assertEqual(self.store.list('issues', None)['total'], 3)
        self.assertEqual(self.store.snapshot(), before)
        self.assertEqual(self.store.list('issues', {'label_ids':{'bad':'shape'}})['total'], 0)


if __name__ == '__main__':
    unittest.main()
