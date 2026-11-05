"""Impact previews must not hide dependents or claim earlier deletions."""
import unittest
from linearboard.trash import deletion_impact


class TrashImpactTests(unittest.TestCase):
    def setUp(self):
        self.data = {
            'projects': [{'id': 'p', 'team_id': 't'}],
            'issues': [
                {'id': 'parent', 'project_id': 'p'},
                {'id': 'child', 'project_id': 'p', 'parent_id': 'parent'},
                {'id': 'grandchild', 'project_id': 'p', 'parent_id': 'child'},
                {'id': 'old', 'project_id': 'p', 'parent_id': 'parent', 'deleted_at': 'yesterday'},
                {'id': 'other', 'project_id': 'p', 'label_ids': ['tag']},
            ],
            'comments': [{'id': 'comment', 'project_id': 'p', 'target_id': 'child'}],
            'attachments': [{'id': 'attachment', 'project_id': 'p', 'target_id': 'grandchild'}],
            'relations': [{'id': 'relation', 'project_id': 'p', 'source_id': 'parent', 'target_id': 'other'}],
            'dispatches': [{'id': 'dispatch', 'project_id': 'p', 'issue_ids': ['child']}],
            'labels': [{'id': 'group', 'name': 'Category', 'is_group': True},
                       {'id': 'cat', 'name': 'FrontEnd', 'parent_id': 'group'},
                       {'id': 'tag', 'name': 'M1'}],
            'statuses': ['Backlog', 'Todo'],
        }

    def ids(self, impact, field):
        return {entry['record']['id'] for entry in impact[field]}

    def test_subtree_and_owned_content_are_separate_from_surviving_references(self):
        impact = deletion_impact(self.data, 'issues', 'parent')
        self.assertEqual(self.ids(impact, 'deleted'), {'parent', 'child', 'grandchild', 'comment', 'attachment', 'relation', 'dispatch'})
        self.assertEqual(self.ids(impact, 'affected'), set())
        self.assertNotIn('old', self.ids(impact, 'deleted'))

    def test_project_includes_archived_children_and_project_content(self):
        self.data['issues'][0]['archived'] = True
        impact = deletion_impact(self.data, 'projects', 'p')
        self.assertEqual(self.ids(impact, 'deleted'), {'p', 'parent', 'child', 'grandchild', 'other', 'comment', 'attachment', 'relation', 'dispatch'})
        self.assertFalse(self.ids(impact, 'affected'))
        self.assertEqual(self.ids(deletion_impact(self.data, 'projects', ['p']), 'deleted'), self.ids(impact, 'deleted'))

    def test_label_usage_and_protected_category(self):
        impact = deletion_impact(self.data, 'labels', 'tag')
        self.assertEqual(self.ids(impact, 'affected'), {'other'})
        for record_id in ('group', 'cat'):
            with self.assertRaises(ValueError):
                deletion_impact(self.data, 'labels', record_id)

    def test_missing_or_wrong_kind_is_rejected(self):
        with self.assertRaises(ValueError):
            deletion_impact(self.data, 'documents', 'parent')
        with self.assertRaises(ValueError):
            deletion_impact(self.data, 'issues', 'old')


if __name__ == '__main__':
    unittest.main()
