"""Guide assets and standalone download contracts without sockets or application data."""
import base64
import hashlib
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import server


class GuideHTML(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.scripts = []
        self.meta = []
        self.assets = []
        self.ids = set()
        self.download = None
        self.action_values = []
        self.catalog_links = []
        self.command_buttons = []
        self.nav_links = []
        self._select = None
        self._catalog = False
        self._nav = False
        self._script = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'select':
            self._select = attrs.get('id')
        if tag == 'option' and self._select == 'action':
            self.action_values.append(attrs['value'])
        if tag == 'table':
            self._catalog = attrs.get('id') == 'catalog'
        if tag == 'nav':
            self._nav = True
        if tag == 'button' and attrs.get('data-command'):
            self.command_buttons.append(attrs['data-command'])
        if tag == 'a':
            if self._catalog:
                self.catalog_links.append(attrs.get('href'))
            if self._nav:
                self.nav_links.append(attrs.get('href'))
        if tag == 'script':
            self._script = {'attrs':attrs, 'text':''}
            self.scripts.append(self._script)
            if attrs.get('src'):
                self.assets.append(attrs['src'])
        if tag == 'link' and attrs.get('href'):
            self.assets.append(attrs['href'])
        if tag == 'img' and attrs.get('src'):
            self.assets.append(attrs['src'])
        if tag == 'meta':
            self.meta.append(attrs)
        if tag == 'a' and 'download' in attrs:
            self.download = attrs

    def handle_endtag(self, tag):
        if tag == 'script':
            self._script = None
        if tag == 'select':
            self._select = None
        if tag == 'table':
            self._catalog = False
        if tag == 'nav':
            self._nav = False

    def handle_data(self, data):
        if self._script is not None:
            self._script['text'] += data

    def command_data(self):
        return json.loads(next(s['text'] for s in self.scripts if s['attrs'].get('id') == 'command-data'))


class GuideRouteTests(unittest.TestCase):
    def request(self, path, host='127.0.0.1:8765'):
        handler = server.Handler.__new__(server.Handler)
        handler.path = path
        handler.headers = {'Host':host}
        handler.server = SimpleNamespace(store=None, server_port=8765, verbose=False)
        handler.wfile = io.BytesIO()
        headers, statuses = {}, []
        handler.send_response = statuses.append
        handler.send_header = headers.__setitem__
        handler.end_headers = lambda:None
        handler.route('GET')
        return statuses[0], headers, handler.wfile.getvalue()

    def test_served_guide_loads_only_same_origin_external_runtime_under_existing_csp(self):
        status, headers, raw = self.request('/guide')
        self.assertEqual(status, 200)
        policy = headers['Content-Security-Policy']
        script_policy = next(part.strip() for part in policy.split(';') if part.strip().startswith('script-src '))
        self.assertEqual(script_policy, "script-src 'self'")
        page = GuideHTML(raw.decode())
        executable = [s for s in page.scripts if s['attrs'].get('type') != 'application/json']
        self.assertEqual(len(executable), 1)
        self.assertEqual(executable[0]['attrs']['src'], 'guide.js')
        self.assertEqual(executable[0]['text'], '')
        self.assertIn('$linearboard help', raw.decode())
        self.assertEqual(page.download['href'], 'guide/download')
        self.assertIn('built', page.ids)

    def test_fixed_runtime_route_returns_complete_script(self):
        status, headers, raw = self.request('/guide.js')
        self.assertEqual(status, 200)
        self.assertIn('javascript', headers['Content-Type'])
        self.assertEqual(raw, (server.ROOT / 'guide.js').read_bytes())
        for behavior in ['function build()', 'function filterCommands()', 'navigator.clipboard.writeText', "$('menu-toggle')", "$('reset')", "localStorage.setItem", 'URL.createObjectURL']:
            with self.subTest(behavior=behavior):
                self.assertIn(behavior, raw.decode())

    def test_no_print_action_is_exposed(self):
        page = GuideHTML((server.ROOT / 'linearboard-guide.html').read_text())
        self.assertNotIn('print', page.ids)
        self.assertNotIn('window.print', (server.ROOT / 'guide.js').read_text())
        self.assertNotIn('print', GuideHTML(server.offline_guide()).ids)

    def test_current_skill_commands_have_complete_teaching_data(self):
        html = (server.ROOT / 'linearboard-guide.html').read_text()
        page = GuideHTML(html)
        skill = (server.ROOT / 'skills/linearboard/SKILL.md').read_text()
        router = skill.split('## Commands\n')[1].split('Technology lookup')[0]
        expected = {match.split()[0] for match in re.findall(r'^- `([^`]+)`', router, re.M)}
        # FE and BE share a router bullet but remain separate commands.
        self.assertIn('`create-issues-BE`', router)
        expected.add('create-issues-BE')
        data = page.command_data()
        names = [command['name'] for command in data]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), expected)
        for command in data:
            with self.subTest(command=command['name']):
                for field in ['title', 'phase', 'effect', 'view', 'when', 'input', 'output', 'check', 'example', 'limit']:
                    self.assertTrue(command[field].strip(), field)
                self.assertTrue(command['example'].startswith('$linearboard ' + command['name']))
        self.assertIn(f'{len(expected)} 個主要指令', html)
        self.assertIn(f'{len(expected)} / {len(expected)} 個指令', html)
        # Story creation is now part of the milestone document, not a new issue stage.
        milestones = next(command for command in data if command['name'] == 'create-milestones')
        self.assertIn('User Stories', milestones['output'])
        self.assertIn('不建立 UserStory issues 或 View', milestones['limit'])
        self.assertNotIn('create-userstories', names)
        self.assertNotIn('frd', names)

    def test_debug_contract_requires_bugs_document_before_fix_and_document_results(self):
        html = (server.ROOT / 'linearboard-guide.html').read_text()
        debug = next(command for command in GuideHTML(html).command_data() if command['name'] == 'debug')
        self.assertLess(debug['output'].index('Bugs Project Document'), debug['output'].index('FIX'))
        for requirement in ['Datetime', 'User Report', 'bullet', '原生結果留言', 'issue-only']:
            self.assertIn(requirement, ' '.join(debug.values()))
        self.assertIn('不以 issue 留言替代文件結果', debug['check'])
        self.assertIn('先保存原始回報', html)
        self.assertIn('每張 FIX 指回正確 report batch／bullet', debug['check'])
        self.assertIn('在 Bugs 文件回寫結果', html)
        self.assertNotIn('若來源只有 issue，則回覆來源 issue', html)

    def test_download_is_complete_html_with_exact_hash_and_no_external_asset_dependency(self):
        status, headers, raw = self.request('/guide/download')
        self.assertEqual(status, 200)
        self.assertEqual(headers['Content-Type'], 'text/html; charset=utf-8')
        self.assertIn('attachment;', headers['Content-Disposition'])
        self.assertIn('linearboard-command-tutorial.html', headers['Content-Disposition'])
        self.assertTrue(raw.lower().startswith(b'<!doctype html>'))
        self.assertIn('<style>', raw.decode())
        page = GuideHTML(raw.decode())
        self.assertEqual(page.assets, [])
        runtime = next(s for s in page.scripts if 'data-guide-runtime' in s['attrs'])
        digest = base64.b64encode(hashlib.sha256(runtime['text'].encode()).digest()).decode()
        policy = next(m['content'] for m in page.meta if m.get('http-equiv') == 'Content-Security-Policy')
        self.assertIn("script-src 'sha256-"+digest+"'", policy)
        self.assertIn("connect-src 'none'", policy)
        script_policy = next(part.strip() for part in policy.split(';') if part.strip().startswith('script-src '))
        self.assertNotIn('unsafe-inline', script_policy)
        self.assertNotIn('data:', script_policy)
        self.assertNotIn("'self'", script_policy)
        self.assertEqual(page.download['href'], '#download')
        self.assertEqual(page.command_data(), GuideHTML((server.ROOT / 'linearboard-guide.html').read_text()).command_data())
        for control in ['action','project','milestone','dispatchscope','batch','issueids','debugsource','additional','search','clear-search','menu-toggle','reset']:
            with self.subTest(control=control):
                self.assertIn(control, page.ids)

    def test_packaging_escapes_closing_script_sequences_in_command_json(self):
        html = (server.ROOT / 'linearboard-guide.html').read_text()
        page = GuideHTML(html)
        data = page.command_data()
        data[0]['example'] = '</script><script>alert("untrusted-data")</script>&'
        opening = '<script id="command-data" type="application/json">'
        before, after = html.split(server.GUIDE_RUNTIME_TAG, 1)
        start = before.index(opening) + len(opening)
        end = before.rfind('</script>')
        source = before[:start] + json.dumps(data, ensure_ascii=False) + before[end:] + server.GUIDE_RUNTIME_TAG + after
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'linearboard-guide.html').write_text(source)
            (root / 'guide.js').write_text((server.ROOT / 'guide.js').read_text())
            with patch.object(server, 'ROOT', root):
                output = server.offline_guide()
        bundled = GuideHTML(output)
        self.assertEqual(len(bundled.scripts), 2)
        self.assertEqual(bundled.command_data()[0]['example'], data[0]['example'])
        inert = next(s['text'] for s in bundled.scripts if s['attrs'].get('id') == 'command-data')
        self.assertNotIn('</script', inert.lower())
        self.assertIn('\\u003c/script', inert)

    def test_runtime_closing_script_text_cannot_break_out_of_hashed_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'linearboard-guide.html').write_text((server.ROOT / 'linearboard-guide.html').read_text())
            runtime = 'const example = "</ScRiPt>";\n'
            (root / 'guide.js').write_text(runtime)
            with patch.object(server, 'ROOT', root):
                output = server.offline_guide()
        page = GuideHTML(output)
        self.assertEqual(len(page.scripts), 2)
        script = next(s['text'] for s in page.scripts if 'data-guide-runtime' in s['attrs'])
        self.assertIn('<\\/ScRiPt>', script)
        digest = base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
        policy = next(m['content'] for m in page.meta if m.get('http-equiv') == 'Content-Security-Policy')
        self.assertIn(digest, policy)

    def test_no_arbitrary_static_file_or_path_alias_exposure(self):
        for path in ['/index.html','/server.py','/data/linearboard.sqlite3','/guide/../../server.py','/guide.js/../server.py','/guide/download/extra','/%2e%2e/server.py']:
            with self.subTest(path=path):
                status, _, _ = self.request(path)
                self.assertEqual(status, 404)
        status, _, _ = self.request('/guide', host='untrusted.example:8765')
        self.assertEqual(status, 400)

    @unittest.skipUnless(shutil.which('node'), 'Node is required to check the browser runtime syntax')
    def test_online_and_offline_browser_runtime_parse(self):
        source = (server.ROOT / 'guide.js').read_text()
        downloaded = GuideHTML(server.offline_guide())
        bundle = next(s['text'] for s in downloaded.scripts if 'data-guide-runtime' in s['attrs'])
        for script in [source,bundle]:
            checked = subprocess.run(['node','--check','--input-type=commonjs'], input=script, text=True, capture_output=True)
            self.assertEqual(checked.returncode, 0, checked.stderr)


if __name__ == '__main__':
    unittest.main()
