"""Exercise the real Client methods through a fake MCP transport backed by temp Store.

The transport uses normal JSON tool results and errors; no network or production data.
"""
from copy import deepcopy
import json
import tempfile
import unittest
from pathlib import Path

from linearboard.client import Client
from linearboard.store import Invalid, Store


class FakeMCP:
    def __init__(self, store):
        self.store = store
        self.calls = []
        self.get_transform = None
        self.lose_next_update_response = False

    def rpc(self, method, params):
        if method != 'tools/call':
            raise AssertionError('Unexpected MCP method')
        name, args = params['name'], params['arguments']
        self.calls.append((name, deepcopy(args)))
        try:
            if name == 'linearboard_get':
                output = self.store.get(args['kind'], args['id'])
                if self.get_transform:
                    output = self.get_transform(output)
            elif name == 'linearboard_list':
                output = self.store.list(args['kind'], args.get('filters'), args.get('cursor',0), args.get('limit',100))
            elif name == 'linearboard_create':
                output = self.store.mutate(args['kind'], args['data'], key=args['idempotency_key'])
            elif name == 'linearboard_update':
                output = self.store.mutate(args['kind'], args['data'], args['id'], key=args['idempotency_key'])
                if self.lose_next_update_response:
                    self.lose_next_update_response = False
                    raise OSError('Simulated response loss after commit')
            else:
                raise AssertionError('Unexpected tool: '+name)
        except Invalid as error:
            return {'isError':True,'content':[{'type':'text','text':str(error)}]}
        return {'content':[{'type':'text','text':json.dumps(output)}]}


def client_for(transport):
    client = Client.__new__(Client)
    client._update_requests = {}
    client.rpc = transport.rpc
    return client


class ClientRetryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / 'client.sqlite3')
        team = self.store.snapshot()['teams'][0]
        self.project = self.store.mutate('projects', {'name':'Client QA','team_id':team['id']})
        self.transport = FakeMCP(self.store)
        self.client = client_for(self.transport)
        self.data = {'title':'Replay document','project_id':self.project['id'],'body':'Original'}

    def tearDown(self):
        self.temp.cleanup()

    def test_create_replay_after_update_returns_same_identity_latest_revision(self):
        created = self.client.create('documents', self.data, 'create-document')
        updated = self.client.update('documents', created['id'], {'body':'Revised'}, 'update-document')
        replay = self.client.create('documents', self.data, 'create-document')
        self.assertEqual(replay, updated)
        self.assertEqual(replay['id'], created['id'])
        self.assertEqual(self.store.list('documents')['total'], 1)
        self.assertEqual(len(self.store.history(created['id'])), 2)
        # A create payload already includes everything needed for cross-instance replay.
        self.assertEqual(client_for(self.transport).create('documents', self.data, 'create-document'), updated)

    def test_same_instance_update_reuses_original_payload_and_writes_once(self):
        created = self.client.create('documents', self.data, 'create-document')
        patch = {'body':'Revised'}
        first = self.client.update('documents', created['id'], patch, 'update-document')
        second = self.client.update('documents', created['id'], patch, 'update-document')
        self.assertEqual(first, second)
        requests = [args for name,args in self.transport.calls if name == 'linearboard_update']
        self.assertEqual(requests[0], requests[1])
        self.assertEqual(requests[0]['data']['expected_version'], 1)
        self.assertEqual(len(self.store.history(created['id'])), 2)

    def test_update_replay_after_later_revision_keeps_original_operation_result(self):
        created = self.client.create('documents', self.data, 'create-document')
        first = self.client.update('documents', created['id'], {'body':'First change'}, 'first-update')
        latest = self.client.update('documents', created['id'], {'body':'Later change'}, 'later-update')
        replay = self.client.update('documents', created['id'], {'body':'First change'}, 'first-update')
        self.assertEqual(replay, first)
        self.assertEqual(self.client.get('documents', created['id']), latest)
        self.assertEqual(len(self.store.history(created['id'])), 3)

    def test_different_payload_with_same_key_still_reaches_server_conflict(self):
        created = self.client.create('documents', self.data, 'create-document')
        updated = self.client.update('documents', created['id'], {'body':'First change'}, 'shared-key')
        with self.assertRaisesRegex(RuntimeError, '不同內容'):
            self.client.update('documents', created['id'], {'body':'Different'}, 'shared-key')
        self.assertEqual(self.client.get('documents', created['id']), updated)
        self.assertEqual(len(self.store.history(created['id'])), 2)
        # The failed different-payload attempt must not replace the original envelope.
        self.assertEqual(self.client.update('documents', created['id'], {'body':'First change'}, 'shared-key'), updated)
        with self.assertRaisesRegex(RuntimeError, '不同內容'):
            self.client.create('documents', {**self.data,'body':'Different'}, 'create-document')

    def test_cached_payload_is_not_mutated_by_callers(self):
        created = self.client.create('documents', self.data, 'create-document')
        patch = {'body':'First change','metadata':{'tags':['one']}}
        saved_patch = deepcopy(patch)
        first = self.client.update('documents', created['id'], patch, 'update-document')
        patch['metadata']['tags'].append('two')
        with self.assertRaisesRegex(RuntimeError, '不同內容'):
            self.client.update('documents', created['id'], patch, 'update-document')
        replay = self.client.update('documents', created['id'], saved_patch, 'update-document')
        self.assertEqual(replay, first)
        self.assertEqual(replay['metadata']['tags'], ['one'])

    def test_response_loss_after_commit_can_retry_without_new_revision(self):
        created = self.client.create('documents', self.data, 'create-document')
        self.transport.lose_next_update_response = True
        with self.assertRaisesRegex(OSError, 'response loss'):
            self.client.update('documents', created['id'], {'body':'Committed'}, 'uncertain-update')
        replay = self.client.update('documents', created['id'], {'body':'Committed'}, 'uncertain-update')
        self.assertEqual(replay['body'], 'Committed')
        requests = [args for name,args in self.transport.calls if name == 'linearboard_update']
        self.assertEqual(requests[0], requests[1])
        self.assertEqual(len(self.store.history(created['id'])), 2)

    def test_new_instance_requires_original_expected_version_for_exact_replay(self):
        created = self.client.create('documents', self.data, 'create-document')
        first = self.client.update('documents', created['id'], {'body':'Committed'}, 'update-document')
        restarted = client_for(self.transport)
        with self.assertRaisesRegex(RuntimeError, '不同內容'):
            restarted.update('documents', created['id'], {'body':'Committed'}, 'update-document')
        replay = restarted.update('documents', created['id'], {'expected_version':created['version'],'body':'Committed'}, 'update-document')
        self.assertEqual(replay, first)
        self.assertEqual(len(self.store.history(created['id'])), 2)

    def test_different_key_does_not_silently_skip_server_on_matching_fields(self):
        created = self.client.create('documents', self.data, 'create-document')
        # Equal current content does not establish whether a key previously accepted it.
        result = self.client.update('documents', created['id'], {'body':'Original'}, 'new-operation')
        self.assertEqual(result['version'], 2)
        self.assertEqual(len(self.store.history(created['id'])), 2)

    def test_readback_rejects_wrong_identity_same_version_drift_and_version_rollback(self):
        transforms = [
            lambda r:{**r,'id':'different-record'},
            lambda r:{**r,'project_id':'different-project'},
            lambda r:{**r,'body':'Corrupted same revision'},
            lambda r:{**r,'version':0},
        ]
        for index, transform in enumerate(transforms):
            with self.subTest(index=index):
                self.transport.get_transform = transform
                with self.assertRaisesRegex(RuntimeError, 'readback'):
                    self.client.create('documents', {**self.data,'title':'Case '+str(index)}, 'case-'+str(index))
        self.transport.get_transform = None

    def test_automation_does_not_gain_user_actor_for_done(self):
        issue = self.client.create('issues', {'title':'Acceptance','project_id':self.project['id']}, 'create-issue')
        with self.assertRaisesRegex(RuntimeError, '使用者驗收'):
            self.client.update('issues', issue['id'], {'status':'Done'}, 'cannot-accept')
        self.assertEqual(self.client.get('issues', issue['id'])['status'], 'Backlog')
        self.assertEqual(self.store.history(issue['id'])[0]['actor'], 'automation')


if __name__ == '__main__':
    unittest.main()
