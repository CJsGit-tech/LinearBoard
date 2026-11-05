#!/usr/bin/env python3
"""Local-only HTTP application. Run: python3 server.py --port 8765."""
import argparse
import base64
import hashlib
import json
import mimetypes
import os
import re
import sqlite3
import tempfile
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
from linearboard.store import Store, Invalid, Conflict, KINDS
from linearboard.contracts import capabilities
from linearboard.i18n import preferred_language, translate_error

ROOT = Path(__file__).resolve().parent
GUIDE_RUNTIME_TAG = '<script src="guide.js" data-guide-runtime defer></script>'


def offline_guide():
    """Bundle the trusted guide runtime with an exact hash, without remote assets."""
    html = (ROOT / 'linearboard-guide.html').read_text()
    before, after = html.split(GUIDE_RUNTIME_TAG, 1)
    opening = '<script id="command-data" type="application/json">'
    start = before.index(opening) + len(opening)
    end = before.rfind('</script>')
    data = json.loads(before[start:end])
    safe_json = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    before = before[:start] + safe_json + before[end:]
    runtime = (ROOT / 'guide.js').read_text()
    runtime = re.sub(r'</script', lambda match: '<\\/' + match.group()[2:], runtime, flags=re.IGNORECASE)
    digest = base64.b64encode(hashlib.sha256(runtime.encode()).digest()).decode()
    policy = ("default-src 'none'; script-src 'sha256-" + digest
              + "'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; base-uri 'none'; form-action 'none'")
    meta = '<meta http-equiv="Content-Security-Policy" content="' + policy + '">'
    html = before + '<script data-guide-runtime>' + runtime + '</script>' + after
    html = html.replace('<head>', '<head>' + meta, 1)
    return html.replace('href="guide/download"', 'href="#download"', 1)

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        if self.server.verbose:
            super().log_message(fmt, *args)

    def send(self, status, content, mime='application/json', headers=None):
        language = preferred_language(self.headers.get('Accept-Language', ''))
        if mime == 'application/json':
            if status >= 400 and isinstance(content, dict) and isinstance(content.get('error'), str):
                content = {**content, 'error': translate_error(content['error'], language)}
            content = json.dumps(content, ensure_ascii=False).encode()
        elif isinstance(content, str):
            content = content.encode()
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(content)))
        if mime == 'application/json':
            self.send_header('Content-Language', language)
            self.send_header('Vary', 'Accept-Language')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'same-origin')
        self.send_header('Cache-Control', 'no-store' if mime == 'application/json' else 'no-cache')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(content)

    def checked(self):
        host = self.headers.get('Host', '')
        if host not in [f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}']:
            raise Invalid('只接受本機連線。')
        origin = self.headers.get('Origin')
        if origin and origin not in [f'http://127.0.0.1:{self.server.server_port}', f'http://localhost:{self.server.server_port}']:
            raise Invalid('不接受跨來源操作。')

    def route(self, method):
        try:
            self.checked()
            parsed = urlparse(self.path)
            path = [unquote(x) for x in parsed.path.strip('/').split('/') if x]
            query = {k:v[0] for k,v in parse_qs(parsed.query).items()}
            store = self.server.store
            if method == 'GET':
                if parsed.path == '/guide/download':
                    return self.send(200, offline_guide(), 'text/html; charset=utf-8', {
                        'Content-Disposition':'attachment; filename="linearboard-command-tutorial.html"'})
                if path == ['api', 'state']:
                    return self.send(200, store.snapshot(query.get('archived') == 'true'))
                if path == ['api', 'trash']:
                    return self.send(200, store.trash_list())
                if path == ['api', 'trash', 'impact']:
                    return self.send(200, store.trash_impact(query.get('kind'), query.get('id')))
                if path == ['api', 'capabilities']:
                    return self.send(200, capabilities())
                if path == ['api', 'backup']:
                    name, content = store.backup()
                    return self.send(200, content, 'application/octet-stream', {'Content-Disposition':f'attachment; filename="{name}"'})
                if path == ['api', 'health']:
                    with store.connect() as db:
                        db.execute('SELECT 1').fetchone()
                    return self.send(200, {'status':'ok', 'database':store.backend})
                if len(path) == 3 and path[:2] == ['api', 'history']:
                    return self.send(200, store.history(path[2]))
                if len(path) == 4 and path[:2] == ['api', 'views'] and path[3] == 'members':
                    return self.send(200, store.view_members(path[2]))
                if len(path) == 3 and path[:2] == ['api', 'files']:
                    metadata, blob = store.blob(path[2])
                    # Only inert raster images render inline. HTML/SVG and all other types download.
                    mime = 'image/png' if blob.startswith(b'\x89PNG\r\n\x1a\n') else 'image/jpeg' if blob.startswith(b'\xff\xd8\xff') else 'application/octet-stream'
                    headers = {} if mime.startswith('image/') else {'Content-Disposition': 'attachment; filename="attachment"'}
                    return self.send(200, blob, mime, headers)
                if len(path) >= 2 and path[0] == 'api' and path[1] in KINDS:
                    if len(path) == 3:
                        return self.send(200, store.get(path[1], path[2]))
                    return self.send(200, store.list(path[1], json.loads(query.get('filters', '{}')), query.get('cursor', 0), query.get('limit', 100), query.get('archived') == 'true'))
                if parsed.path == '/visuals':
                    return self.send(302, '', 'text/plain', {'Location':'/visuals/'})
                if parsed.path.startswith('/visuals/'):
                    allowed = {'index.html','review.js','review.css','screen-01-v1-draft.png','screen-02-v1-draft.png','screen-03-v1-draft.png'}
                    name = parsed.path.removeprefix('/visuals/') or 'index.html'
                    if name in allowed:
                        artifact = ROOT / 'output/visual-review/v1' / name
                        if artifact.is_file():
                            return self.send(200, artifact.read_bytes(), mimetypes.guess_type(artifact)[0] or 'application/octet-stream')
                    return self.send(404, {'error':'找不到視覺參考。'})
                files = {'/': ROOT / 'web/index.html', '/app.js': ROOT / 'web/dist/app.js', '/style.css': ROOT / 'web/style.css', '/guide': ROOT / 'linearboard-guide.html', '/guide/en': ROOT / 'web/guide.en.html', '/guide.js': ROOT / 'guide.js'}
                file = files.get(parsed.path)
                if file and file.is_file():
                    return self.send(200, file.read_bytes(), mimetypes.guess_type(file)[0] or 'application/octet-stream')
                return self.send(404, {'error':'找不到頁面。'})
            if method == 'POST' and len(path) == 3 and path[:2] == ['api', 'trash'] and path[2] in ['impact', 'move', 'restore', 'purge']:
                if not self.headers.get('Content-Type', '').startswith('application/json'):
                    raise Invalid('請使用 application/json。')
                size = int(self.headers.get('Content-Length', 0))
                if size <= 0 or size > 1024 * 1024:
                    raise Invalid('請求大小無效。')
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise Invalid('請傳入 JSON object。')
                actor = 'user' if self.headers.get('X-LinearBoard-Actor') == 'user' else 'automation'
                key = self.headers.get('Idempotency-Key')
                if path[2] == 'impact' and set(data) == {'kind', 'ids'}:
                    return self.send(200, store.trash_impact(data['kind'], data['ids']))
                if path[2] == 'move' and set(data) == {'kind', 'id', 'fingerprint'}:
                    return self.send(200, store.trash_move(data['kind'], data['id'], data['fingerprint'], actor, key))
                if path[2] == 'move' and set(data) == {'kind', 'ids', 'fingerprint'}:
                    return self.send(200, store.trash_move(data['kind'], data['ids'], data['fingerprint'], actor, key))
                if path[2] == 'restore' and set(data) == {'batch_id'}:
                    return self.send(200, store.trash_restore(data['batch_id'], actor, key))
                if path[2] == 'purge' and set(data) == {'batch_ids'}:
                    if actor != 'user':
                        raise Invalid('永久刪除必須由使用者操作。')
                    return self.send(200, store.trash_purge(data['batch_ids']))
                raise Invalid('垃圾桶操作資料無效。')
            if len(path) in [2, 3] and path[0] == 'api' and path[1] in KINDS:
                if not self.headers.get('Content-Type', '').startswith('application/json'):
                    raise Invalid('請使用 application/json。')
                size = int(self.headers.get('Content-Length', 0))
                if size <= 0 or size > 22 * 1024 * 1024:
                    raise Invalid('請求大小無效（上限 22 MB）。')
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise Invalid('請傳入 JSON object。')
                rid = path[2] if len(path) == 3 else None
                actor = 'user' if self.headers.get('X-LinearBoard-Actor') == 'user' else 'automation'
                if method == 'POST' and path == ['api', 'issues', 'bulk-status']:
                    return self.send(200, store.update_issue_statuses(data, actor, self.headers.get('Idempotency-Key')))
                if (method == 'POST' and rid) or (method == 'PATCH' and not rid):
                    raise Invalid('操作路徑無效。')
                result = store.mutate(path[1], data, rid, actor, self.headers.get('Idempotency-Key'))
                return self.send(200 if rid else 201, result)
            self.send(404, {'error':'找不到操作。'})
        except Conflict as e:
            self.send(409, {'error': str(e)})
        except (Invalid, ValueError, KeyError, TypeError) as e:
            self.send(400, {'error': str(e)})
        except Exception:
            traceback.print_exc()
            self.send(500, {'error': '儲存失敗，請重試。原有資料已保留。'})

    def do_GET(self):
        self.route('GET')
    def do_POST(self):
        self.route('POST')
    def do_PATCH(self):
        self.route('PATCH')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--db', default=str(ROOT / 'data/linearboard.sqlite3'))
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        from linearboard.postgres import PostgresStore
        store = PostgresStore(database_url)
    else:
        store = Store(args.db)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    server.store, server.verbose = store, args.verbose
    print(f'LinearBoard → http://127.0.0.1:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
