"""Small MCP stdio client for local automation and reproducible integration checks."""
import json
from copy import deepcopy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

class Client:
    def __init__(self, url='http://127.0.0.1:8765'):
        self.process = subprocess.Popen([sys.executable, str(ROOT / 'mcp_server.py'), '--url', url], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
        self.sequence = 0
        self._update_requests = {}
        self.url = url.rstrip('/')
        self.rpc('initialize', {'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'linearboard-workflow-client','version':'0.1.0'}})
        self.process.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n')
        self.process.stdin.flush()

    def rpc(self, method, params=None):
        self.sequence += 1
        self.process.stdin.write(json.dumps({'jsonrpc':'2.0','id':self.sequence,'method':method,'params':params or {}}, ensure_ascii=False)+'\n')
        self.process.stdin.flush()
        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError('MCP server exited without a response')
        response = json.loads(line)
        if 'error' in response:
            raise RuntimeError(response['error']['message'])
        return response['result']

    def call(self, name, arguments=None):
        result = self.rpc('tools/call', {'name':name,'arguments':arguments or {}})
        text = result['content'][0]['text']
        if result.get('isError'):
            raise RuntimeError(text)
        return json.loads(text)

    def list(self, kind, **filters):
        rows, cursor = [], 0
        while True:
            page = self.call('linearboard_list', {'kind':kind,'filters':filters,'cursor':cursor,'limit':200})
            rows.extend(page['items'])
            if page['next_cursor'] is None:
                return rows
            cursor = page['next_cursor']

    def get(self, kind, rid):
        return self.call('linearboard_get', {'kind':kind,'id':rid})

    def _readback(self, kind, record):
        if not isinstance(record, dict) or not record.get('id'):
            raise RuntimeError('Write response has no record identity')
        current = self.get(kind, record['id'])
        stable_fields = ['id', 'identifier', 'created_at', 'team_id', 'project_id', 'url']
        if not isinstance(current, dict) or any(current.get(field) != record[field]
                for field in stable_fields if field in record):
            raise RuntimeError('Write readback identity mismatch')
        original_version, current_version = record.get('version'), current.get('version')
        if (type(original_version) is not int or type(current_version) is not int
                or current_version < original_version
                or (current_version == original_version and current != record)):
            raise RuntimeError('Write readback version or content mismatch')
        return current

    def create(self, kind, data, key):
        """Return the current record, allowing an original response replay after revisions."""
        record = self.call('linearboard_create', {'kind':kind,'data':data,'idempotency_key':key})
        return self._readback(kind, record)

    def update(self, kind, rid, patch, key):
        """Replay the exact request for repeated operations in this Client instance.

        A new instance/process has no request cache. To retry across that boundary,
        keep the original payload, including expected_version, and supply it in
        patch. Without it the server may correctly return 409; current field
        equality alone cannot establish whether this key accepted that payload.
        The returned value is the server's original operation response, even if
        readback confirms that later legitimate revisions now exist.
        """
        operation = (key, json.dumps([kind, rid, patch], sort_keys=True, ensure_ascii=False))
        if operation not in self._update_requests:
            data = deepcopy(patch)
            if 'expected_version' not in data:
                data['expected_version'] = self.get(kind, rid)['version']
            self._update_requests[operation] = {
                'kind':kind, 'id':rid, 'data':data, 'idempotency_key':key}
        # Cache before sending: an interrupted response may still have committed.
        # Distinct payloads retain distinct envelopes and still reach the server's
        # same-key/different-payload check instead of being silently treated as a no-op.
        result = self.call('linearboard_update', deepcopy(self._update_requests[operation]))
        self._readback(kind, result)
        return result

    def ensure(self, kind, match, data, key):
        found = self.list(kind, **match)
        if len(found) > 1:
            raise RuntimeError('Ambiguous existing records; do not silently duplicate or overwrite')
        return found[0] if found else self.create(kind, {**match, **data}, key)

    def close(self):
        if self.process.poll() is None:
            self.process.stdin.close()
            self.process.wait(timeout=10)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
