"""HTTP localization leaves canonical records, actors, and retry behavior unchanged."""
import ast
import io
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from linearboard.i18n import ENGLISH, preferred_language, translate_error
from linearboard.store import Store
from server import Handler


class LocalizationTests(unittest.TestCase):
    def test_accept_language_quality_and_default(self):
        for header, expected in [('', 'zh-TW'), ('en-US,en;q=0.9', 'en'), ('zh-TW,en;q=0.8', 'zh-TW'),
                                 ('en;q=0.2,zh;q=0.9', 'zh-TW'), ('en;q=0,zh;q=1', 'zh-TW'),
                                 ('fr,en;q=0.5', 'en'), ('en;q=oops,zh', 'zh-TW')]:
            self.assertEqual(preferred_language(header), expected)

    def test_error_parameters_preserve_user_content(self):
        self.assertEqual(translate_error('名稱不可空白。', 'en'), 'Name cannot be empty.')
        self.assertEqual(translate_error('中文群組 是單選群組。', 'en'), '中文群組 is a single-select group.')
        self.assertEqual(translate_error('找不到紀錄：abc', 'en'), 'Record not found: abc')
        self.assertEqual(translate_error('未知的自訂訊息', 'en'), '未知的自訂訊息')
        self.assertEqual(translate_error('名稱不可空白。', 'zh-TW'), '名稱不可空白。')

    def test_every_application_error_has_an_english_catalog_entry(self):
        for filename in ['server.py', 'linearboard/store.py', 'linearboard/trash.py']:
            tree = ast.parse(Path(filename).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) and node.exc.args:
                    arg = node.exc.args[0]
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        message = arg.value
                    elif isinstance(arg, ast.JoinedStr):
                        message = ''.join(x.value if isinstance(x, ast.Constant) else '{0}' for x in arg.values)
                    elif isinstance(arg, ast.BinOp) and isinstance(arg.left, ast.Constant):
                        message = arg.left.value + '{0}'
                    else:
                        continue
                    if any('\u4e00' <= c <= '\u9fff' for c in message):
                        with self.subTest(filename=filename, line=node.lineno):
                            self.assertIn(message, ENGLISH)

    def request(self, store, path, language, payload=None):
        handler = object.__new__(Handler)
        handler.server = SimpleNamespace(store=store, server_port=8769, verbose=False)
        handler.path = path
        raw = json.dumps(payload).encode() if payload is not None else b''
        handler.headers = {'Host':'localhost:8769', 'Accept-Language':language,
                           'Content-Type':'application/json', 'Content-Length':str(len(raw))}
        handler.rfile = io.BytesIO(raw)
        handler.wfile = io.BytesIO()
        headers = {}
        result = {}
        handler.send_response = lambda status: result.update(status=status)
        handler.send_header = lambda name, value: headers.update({name:value})
        handler.end_headers = lambda: None
        handler.route('POST' if payload is not None else 'GET')
        return result['status'], headers, json.loads(handler.wfile.getvalue())

    def test_http_errors_localized_but_record_bodies_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            store = Store(Path(directory) / 'i18n.sqlite3')
            team = store.snapshot()['teams'][0]
            payload = {'name':'', 'team_id':team['id']}
            status, headers, body = self.request(store, '/api/projects', 'en', payload)
            self.assertEqual(status, 400)
            self.assertEqual(body['error'], 'Name cannot be empty.')
            self.assertEqual(headers['Content-Language'], 'en')
            self.assertEqual(headers['Vary'], 'Accept-Language')
            self.assertEqual(self.request(store, '/api/projects', 'zh-TW', payload)[2]['error'], '名稱不可空白。')
            project = store.mutate('projects', {'name':'中文專案', 'body':'Do not translate 我的內容', 'team_id':team['id']})
            for lang in ['en', 'zh-TW']:
                self.assertEqual(self.request(store, '/api/projects/' + project['id'], lang)[2]['body'], project['body'])
            # Locale must not grant the user-only Done transition to automation.
            issue = store.mutate('issues', {'title':'English issue', 'project_id':project['id']})
            status, _, body = self.request(store, '/api/issues/bulk-status', 'en', {
                'issue_ids':[issue['id']], 'expected_versions':{issue['id']:issue['version']}, 'status':'Done'})
            self.assertEqual(status, 400)
            self.assertIn('Only a user', body['error'])
