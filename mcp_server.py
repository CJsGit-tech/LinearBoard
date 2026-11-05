#!/usr/bin/env python3
"""Dependency-free MCP stdio adapter for the running local HTTP application.

This is an explicit LinearBoard tool surface, not a replacement of installed Linear tools.
"""
import argparse
import json
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from linearboard.store import KINDS

TOOLS = [
    {'name':'linearboard_trash_list', 'description':'List recoverable trash batches. Permanent deletion is user-only in the application.', 'inputSchema':{'type':'object','properties':{}}},
    {'name':'linearboard_trash_impact', 'description':'Preview exact affected records and receive a fingerprint before moving records to trash.', 'inputSchema':{'type':'object','properties':{'kind':{'type':'string'},'ids':{'type':'array','items':{'type':'string'}}},'required':['kind','ids']}},
    {'name':'linearboard_trash_move', 'description':'Move the confirmed selection atomically to trash, including descendant issues; use the current impact fingerprint.', 'inputSchema':{'type':'object','properties':{'kind':{'type':'string'},'ids':{'type':'array','items':{'type':'string'}},'fingerprint':{'type':'string'},'idempotency_key':{'type':'string'}},'required':['kind','ids','fingerprint','idempotency_key']}},
    {'name':'linearboard_trash_restore', 'description':'Restore one trash batch and return any links that could not be restored.', 'inputSchema':{'type':'object','properties':{'batch_id':{'type':'string'},'idempotency_key':{'type':'string'}},'required':['batch_id','idempotency_key']}},
    {'name':'linearboard_update_issue_statuses', 'description':'Atomically change selected issues in one project to a workflow status. All expected versions are required. No partial updates. Done requires user action.', 'inputSchema':{'type':'object','properties':{'issue_ids':{'type':'array','items':{'type':'string'}},'expected_versions':{'type':'object'},'status':{'type':'string'},'idempotency_key':{'type':'string'}},'required':['issue_ids','expected_versions','status','idempotency_key']}},
    {'name':'linearboard_capabilities', 'description':'Read command contracts, resources, aliases and external execution boundaries.', 'inputSchema':{'type':'object','properties':{}}},
    {'name':'linearboard_list', 'description':'List typed records with exact field filters and pagination.', 'inputSchema':{'type':'object','properties':{'kind':{'type':'string'},'filters':{'type':'object'},'cursor':{'type':'integer'},'limit':{'type':'integer'}},'required':['kind']}},
    {'name':'linearboard_get', 'description':'Read one record, its revisions, or a saved View membership. Use actual IDs.', 'inputSchema':{'type':'object','properties':{'kind':{'type':'string'},'id':{'type':'string'},'history':{'type':'boolean'},'members':{'type':'boolean'}},'required':['kind','id']}},
    {'name':'linearboard_create', 'description':'Create a record with a stable idempotency key. Actor is automation. Done and visual approval require user action. No agent execution is triggered.', 'inputSchema':{'type':'object','properties':{'kind':{'type':'string'},'data':{'type':'object'},'idempotency_key':{'type':'string'}},'required':['kind','data','idempotency_key']}},
    {'name':'linearboard_update', 'description':'Update only supplied fields. data.expected_version is required. Preserve current identity, unrelated fields and history.', 'inputSchema':{'type':'object','properties':{'kind':{'type':'string'},'id':{'type':'string'},'data':{'type':'object'},'idempotency_key':{'type':'string'}},'required':['kind','id','data','idempotency_key']}},
]

def request_tool(base, name, args):
    spec = next((tool for tool in TOOLS if tool['name'] == name), None)
    if not spec or not isinstance(args, dict):
        raise ValueError('Unknown tool or invalid arguments')
    for required in spec['inputSchema'].get('required', []):
        if required not in args or args[required] is None:
            raise ValueError('Missing argument: ' + required)
    if 'kind' in args and args['kind'] not in KINDS:
        raise ValueError('Unknown resource kind')
    if name in ['linearboard_create', 'linearboard_update', 'linearboard_update_issue_statuses', 'linearboard_trash_move', 'linearboard_trash_restore'] and not args.get('idempotency_key'):
        raise ValueError('A nonempty idempotency_key is required')
    if name == 'linearboard_trash_list':
        path, data = '/api/trash', None
    elif name == 'linearboard_trash_impact':
        path, data = '/api/trash/impact', json.dumps({'kind':args['kind'], 'ids':args['ids']}).encode()
    elif name == 'linearboard_trash_move':
        path, data = '/api/trash/move', json.dumps({k:args[k] for k in ['kind','ids','fingerprint']}).encode()
    elif name == 'linearboard_trash_restore':
        path, data = '/api/trash/restore', json.dumps({'batch_id':args['batch_id']}).encode()
    elif name == 'linearboard_update_issue_statuses':
        path = '/api/issues/bulk-status'
        data = json.dumps({k:args[k] for k in ['issue_ids','expected_versions','status']}).encode()
    elif name == 'linearboard_capabilities':
        path, data = '/api/capabilities', None
    elif name == 'linearboard_list':
        query = {k:json.dumps(v) if k == 'filters' else str(v).lower() if isinstance(v,bool) else v for k,v in args.items() if k != 'kind'}
        path, data = '/api/' + args['kind'] + '?' + urlencode(query), None
    elif name == 'linearboard_get':
        path = '/api/history/' + args['id'] if args.get('history') else '/api/' + args['kind'] + '/' + args['id']
        if args.get('members'):
            path += '/members'
        data = None
    elif name in ['linearboard_create', 'linearboard_update']:
        path = '/api/' + args['kind'] + ('/' + args['id'] if name.endswith('update') else '')
        data = json.dumps(args['data']).encode()
    else:
        raise ValueError('Unknown tool')
    if not path.startswith('/api/') or '..' in path:
        raise ValueError('Invalid resource path')
    req = Request(base + path, data=data, method='PATCH' if name.endswith('update') else 'POST' if data is not None else 'GET', headers={'Content-Type':'application/json','Idempotency-Key':args.get('idempotency_key','')})
    try:
        with urlopen(req, timeout=20) as response:
            return json.load(response)
    except HTTPError as e:
        raise ValueError(e.read().decode())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:8765')
    opts = parser.parse_args()
    if not opts.url.startswith(('http://127.0.0.1:', 'http://localhost:')):
        parser.error('Only a local LinearBoard endpoint is supported.')
    for line in sys.stdin:
        req = {}
        try:
            req = json.loads(line)
            if 'id' not in req:
                continue
            method, args = req.get('method'), req.get('params', {})
            if method == 'initialize':
                result = {'protocolVersion':'2024-11-05','capabilities':{'tools':{}},'serverInfo':{'name':'linearboard','version':'0.1.0'}}
            elif method == 'tools/list':
                result = {'tools': TOOLS}
            elif method == 'tools/call':
                try:
                    output = request_tool(opts.url.rstrip('/'), args['name'], args.get('arguments', {}))
                    result = {'content':[{'type':'text','text':json.dumps(output,ensure_ascii=False)}]}
                except (ValueError, URLError, KeyError) as e:
                    result = {'isError':True,'content':[{'type':'text','text':str(e)}]}
            elif method == 'ping':
                result = {}
            else:
                print(json.dumps({'jsonrpc':'2.0','id':req['id'],'error':{'code':-32601,'message':'Method not found'}}), flush=True)
                continue
            print(json.dumps({'jsonrpc':'2.0','id':req['id'],'result':result}, ensure_ascii=False), flush=True)
        except Exception as e:
            print(json.dumps({'jsonrpc':'2.0','id':req.get('id'),'error':{'code':-32602,'message':str(e)}}), flush=True)
