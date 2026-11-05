import json
import tempfile
import unittest
from pathlib import Path

from linearboard.store import Invalid, Store


class ArchiveMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'test.sqlite'
        self.store = Store(self.path)
        self.team = self.store.snapshot()['teams'][0]
        self.project = self.store.mutate('projects', {'name': 'Project', 'team_id': self.team['id']})

    def legacy_archive(self, *records):
        with self.store.connect() as db:
            for record in records:
                db.execute('UPDATE records SET data=? WHERE id=?',
                           (json.dumps({**record, 'archived': True}), record['id']))

    def test_records_are_separate_recoverable_trash_entries_with_history(self):
        a = self.store.mutate('issues', {'project_id': self.project['id'], 'title': 'A'})
        b = self.store.mutate('issues', {'project_id': self.project['id'], 'title': 'B'})
        relation = self.store.mutate('relations', {'source_id': a['id'], 'target_id': b['id'], 'relation': 'related'})
        label = self.store.mutate('labels', {'team_id': self.team['id'], 'name': 'Old label'})
        self.legacy_archive(label, relation)
        self.store = Store(self.path)
        trash = self.store.trash_list()
        self.assertEqual({x['record']['id'] for x in trash}, {label['id'], relation['id']})
        self.assertTrue(all(x['count'] == 1 and not x['record']['archived'] for x in trash))
        self.assertEqual(len(Store(self.path).trash_list()), 2)
        for entry in trash:
            self.store.trash_restore(entry['batch_id'])
            restored = self.store.get(entry['kind'], entry['record']['id'])
            self.assertFalse(restored['archived'])
            self.assertEqual(restored['id'], entry['record']['id'])
            self.assertEqual([h['action'] for h in self.store.history(restored['id'])][:2], ['restore', 'trash'])
        with self.assertRaises(Invalid):
            self.store.mutate('issues', {'expected_version': a['version'], 'archived': True}, a['id'])

    def test_migration_does_not_hide_active_dependents(self):
        self.store.mutate('issues', {'project_id': self.project['id'], 'title': 'Active issue'})
        self.legacy_archive(self.project)
        with self.assertRaises(Invalid):
            Store(self.path)
        self.assertFalse(self.store.trash_list())


if __name__ == '__main__':
    unittest.main()
