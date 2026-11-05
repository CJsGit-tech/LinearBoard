#!/usr/bin/env python3
"""Call the running LinearBoard application without credentials or a local data mirror."""
import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from urllib.parse import urlsplit
from adapter import TOOLS, request_tool
from ensure_running import ensure


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tool', choices=[tool['name'] for tool in TOOLS])
    parser.add_argument('--url', default=os.environ.get('LINEARBOARD_URL', 'http://127.0.0.1:8765'))
    parser.add_argument('--args-file', type=Path, help='JSON input file; otherwise read JSON from stdin')
    parser.add_argument('--all', action='store_true', help='Collect every page of linearboard_list')
    parser.add_argument('--no-autostart', action='store_true', help='Use an explicitly managed service without Docker startup')
    parser.add_argument('--project-dir', type=Path, help='Existing LinearBoard Compose project directory')
    args = parser.parse_args()
    url = urlsplit(args.url)
    if url.scheme != 'http' or url.hostname not in ('127.0.0.1', 'localhost', '::1') or url.username or url.password or url.path not in ('', '/') or url.query or url.fragment:
        parser.error('Use an explicit loopback HTTP service origin')
    raw = args.args_file.read_text() if args.args_file else (sys.stdin.read() if not sys.stdin.isatty() else '')
    payload = json.loads(raw) if raw.strip() else {}
    if not isinstance(payload, dict):
        parser.error('Input must be a JSON object')
    base = args.url.rstrip('/')
    if not args.no_autostart:
        ensure(base, args.project_dir)
    if args.all:
        if args.tool != 'linearboard_list':
            parser.error('--all applies only to linearboard_list')
        items, seen = [], set()
        payload.setdefault('cursor', 0)
        while True:
            result = request_tool(base, args.tool, payload)
            items.extend(result['items'])
            cursor = result['next_cursor']
            if cursor is None:
                result = {'items': items, 'total': len(items), 'next_cursor': None}
                break
            if cursor in seen:
                raise RuntimeError('Repeated pagination cursor; stop instead of returning incomplete results')
            seen.add(cursor)
            payload['cursor'] = cursor
    else:
        result = request_tool(base, args.tool, payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
