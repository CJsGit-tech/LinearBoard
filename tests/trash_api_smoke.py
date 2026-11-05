"""HTTP smoke test against an isolated, temporary local database."""
import json
import tempfile
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from linearboard.store import Store
from linearboard.client import Client
from server import Handler


def run():
    with tempfile.TemporaryDirectory() as directory:
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        server.store, server.verbose = Store(Path(directory) / 'qa.sqlite'), False
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f'http://127.0.0.1:{server.server_port}/api/'

        def call(path, body=None, user=False):
            headers = {'Content-Type': 'application/json'}
            if user:
                headers['X-LinearBoard-Actor'] = 'user'
            request = Request(base + path, data=json.dumps(body).encode() if body is not None else None,
                              headers=headers, method='POST' if body is not None else 'GET')
            try:
                with urlopen(request) as response:
                    return response.status, json.load(response)
            except HTTPError as error:
                return error.code, json.loads(error.read())

        try:
            team = call('state')[1]['teams'][0]
            project = call('projects', {'team_id': team['id'], 'name': 'QA'})[1]
            issue = call('issues', {'project_id': project['id'], 'title': 'Parent', 'category': 'FrontEnd'})[1]
            child = call('issues', {'project_id': project['id'], 'title': 'Child', 'category': 'FrontEnd', 'parent_id': issue['id']})[1]
            preview = call(f"trash/impact?kind=issues&id={issue['id']}")[1]
            assert {row['record']['id'] for row in preview['deleted']} == {issue['id'], child['id']}
            status, moved = call('trash/move', {'kind': 'issues', 'id': issue['id'], 'fingerprint': preview['fingerprint']}, True)
            assert status == 200 and moved['deleted'] == 2
            assert call('issues/' + child['id'])[0] == 400
            assert call('trash')[1][0]['count'] == 2
            assert call('trash/purge', {'batch_ids': [moved['batch_id']]})[0] == 400
            assert call('trash/restore', {'batch_id': moved['batch_id']}, True)[1]['restored'] == 2
            assert call('issues/' + child['id'])[1]['parent_id'] == issue['id']
            preview = call(f"trash/impact?kind=issues&id={issue['id']}")[1]
            moved = call('trash/move', {'kind': 'issues', 'id': issue['id'], 'fingerprint': preview['fingerprint']}, True)[1]
            assert call('trash/purge', {'batch_ids': [moved['batch_id']]}, True)[1]['purged'] == 2
            assert call('trash')[1] == []
            with Client(base.removesuffix('/api/')) as client:
                record = client.create('issues', {'project_id':project['id'], 'title':'MCP QA', 'category':'FrontEnd'}, 'mcp-create')
                args = {'kind':'issues', 'ids':[record['id']]}
                impact = client.call('linearboard_trash_impact', args)
                args.update(fingerprint=impact['fingerprint'], idempotency_key='mcp-trash')
                moved = client.call('linearboard_trash_move', args)
                assert client.call('linearboard_trash_move', args) == moved
                assert len(client.call('linearboard_trash_list')) == 1
                restore = {'batch_id':moved['batch_id'], 'idempotency_key':'mcp-restore'}
                result = client.call('linearboard_trash_restore', restore)
                assert client.call('linearboard_trash_restore', restore) == result
                assert client.get('issues', record['id'])['title'] == 'MCP QA'
            print('PASS: HTTP impact, atomic move, listing, user-only purge, restore, permanent removal, MCP and safe retries')
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == '__main__':
    run()
