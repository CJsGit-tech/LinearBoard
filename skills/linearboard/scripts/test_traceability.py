#!/usr/bin/env python3
"""Offline transport-level tests; never connect to a service."""
import copy
import json
import unittest
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs
from traceability import Traceability, PRD_SCHEMA, STORY_SCHEMA


def fenced(value):
    return '\n```json\n' + json.dumps(value) + '\n```\n'


class Fake:
    def __init__(self):
        self.data = {k: {} for k in ('projects', 'issues', 'documents', 'milestones', 'relations')}
        self.calls = []
        self.keys = {}
        self.fail_relation = False
        self.lose_relation_response = False
        self.on_get = None
        self.add('projects', 'p')
        self.add('milestones', 'm', project_id='p')
        self.add('milestones', 'other', project_id='p')
        self.stories = [{'id': 'US-01', 'milestone_id': 'm', 'anchor': 'us-01'},
                        {'id': 'US-02', 'milestone_id': 'm', 'anchor': 'us-02'}]
        self.source()
        self.add('issues', 'prd', category='ProductRequirement', project_id='p', milestone_id='other',
                 status='In Progress', label_ids=['keep'], body='[US1](/documents/doc#us-01)' + fenced(
                     {'schema': PRD_SCHEMA, 'document_id': 'doc', 'story_ids': ['US-01']}))

    def add(self, kind, rid, **fields):
        self.data[kind][rid] = {'id': rid, 'version': 1, 'url': '/' + kind + '/' + rid, **fields}

    def source(self):
        self.add('documents', 'doc', project_id='p', body=''.join('<a id="' + s['anchor'] + '"></a>\n' for s in self.stories) + fenced({'schema': STORY_SCHEMA, 'stories': self.stories}))

    def __call__(self, name, args):
        self.calls.append((name, copy.deepcopy(args)))
        kind = args.get('kind')
        if name == 'linearboard_get':
            if self.on_get:
                self.on_get(kind, args['id'])
            if args['id'] not in self.data[kind]:
                raise ValueError('Not found')
            return copy.deepcopy(self.data[kind][args['id']])
        if name == 'linearboard_list':
            rows = [x for x in self.data[kind].values() if all(x.get(k) == v for k, v in args['filters'].items())]
            # Always paginate at one row, forcing the client to follow cursors.
            cursor = args['cursor']
            return {'items': copy.deepcopy(rows[cursor:cursor + 1]), 'next_cursor': cursor + 1 if cursor + 1 < len(rows) else None}
        payload = copy.deepcopy(args['data'])
        cache_key = args['idempotency_key']
        if cache_key in self.keys:
            old_args, result = self.keys[cache_key]
            if args != old_args:
                raise ValueError('Idempotency conflict')
            return copy.deepcopy(result)
        if name == 'linearboard_update':
            old = self.data[kind][args['id']]
            if payload.pop('expected_version') != old['version']:
                raise ValueError('Version conflict')
            old.update(payload)
            old['version'] += 1
            result = old
        elif name == 'linearboard_create' and kind == 'relations':
            if self.fail_relation:
                self.fail_relation = False
                raise ValueError('Simulated failure')
            rid = 'rel-' + str(len(self.data['relations']))
            self.add('relations', rid, project_id='p', **payload)
            result = self.data['relations'][rid]
        else:
            raise AssertionError('Unexpected mutation')
        self.keys[cache_key] = (copy.deepcopy(args), copy.deepcopy(result))
        if name == 'linearboard_create' and self.lose_relation_response:
            self.lose_relation_response = False
            raise ValueError('Simulated lost response after commit')
        return copy.deepcopy(result)

    def mutations(self):
        return [c for c in self.calls if c[0] in ('linearboard_create', 'linearboard_update')]

    def legacy(self):
        self.stories[0]['legacy_issue_id'] = 'legacy'
        self.source()
        self.add('issues', 'legacy', project_id='p', category='UserStory', milestone_id='m', body='untouched', status='Done')


class TraceTests(unittest.TestCase):
    def setUp(self):
        self.fake = Fake()
        self.audit = Traceability(self.fake)

    def result(self, apply=False):
        return self.audit.run('p', ['prd'], apply)['issues'][0]

    def test_visible_sources_verify_tags_and_anchor_identity(self):
        issue = self.fake.data['issues']['prd']
        issue.update(team_id='team', milestone_id='m', label_ids=['stage', 'story'],
                     body='**Source stories:** [US-01](/#/documents/doc#us-01)')
        self.fake.data['documents']['doc']['url'] = '/#/documents/doc'
        self.fake.data['milestones']['m']['name'] = 'M1 — Booking'
        self.fake.data['labels'] = {}
        self.fake.add('labels', 'stage', name='M1', team_id='team')
        self.fake.add('labels', 'story', name='US1', team_id='team')
        self.assertEqual(self.result()['warnings'], [])
        issue['label_ids'].remove('stage')
        self.assertIn('Missing or ambiguous tracking tag M1', self.result()['warnings'])
        issue['body'] = issue['body'].replace('#us-01', '#us-02')
        self.assertEqual(self.result()['status'], 'blocked')

    def test_inline_code_anchor_cannot_authorize_repair(self):
        doc = self.fake.data['documents']['doc']
        doc['body'] = doc['body'].replace('<a id="us-01"></a>', '`<a id="us-01"></a>`')
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertFalse(self.fake.mutations())

    def test_tilde_fenced_anchor_cannot_authorize_repair(self):
        doc = self.fake.data['documents']['doc']
        doc['body'] = doc['body'].replace('<a id="us-01"></a>', '~~~html\n<a id="us-01"></a>\n~~~')
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertFalse(self.fake.mutations())

    def test_inline_code_link_is_not_readable_source_link(self):
        prd = self.fake.data['issues']['prd']
        prd['body'] = prd['body'].replace('[US1](/documents/doc#us-01)', '``[US1](/documents/doc#us-01)``')
        self.assertTrue(self.result()['warnings'])

    def test_tilde_fenced_link_is_not_readable_source_link(self):
        prd = self.fake.data['issues']['prd']
        prd['body'] = prd['body'].replace('[US1](/documents/doc#us-01)', '~~~~markdown\n[US1](/documents/doc#us-01)\n~~~~\n')
        self.assertTrue(self.result()['warnings'])

    def test_wrong_document_link_is_warning(self):
        self.fake.data['issues']['prd']['body'] = self.fake.data['issues']['prd']['body'].replace('/documents/doc#', '/documents/wrong#')
        self.assertTrue(self.result()['warnings'])

    def test_anchor_inside_code_does_not_validate_readable_story(self):
        doc = self.fake.data['documents']['doc']
        doc['body'] = doc['body'].replace('<a id="us-01"></a>', '```html\n<a id="us-01"></a>\n```')
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertFalse(self.fake.mutations())

    def test_duplicate_readable_anchor_blocks(self):
        self.fake.data['documents']['doc']['body'] += '<a id="us-01"></a>\n'
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertFalse(self.fake.mutations())

    def test_existing_conflicting_relation_is_preserved(self):
        self.fake.legacy()
        self.fake.add('relations', 'blocker', project_id='p', source_id='legacy', target_id='prd', relation='blocks')
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertFalse(self.fake.mutations())
        self.assertEqual(self.fake.data['relations']['blocker']['relation'], 'blocks')

    def test_report_retains_applied_actions(self):
        result = self.result(True)
        self.assertEqual(result['applied_actions'], [{'kind': 'milestone', 'value': 'm'}])
        self.assertEqual(result['actions'], [])

    def test_audit_read_only(self):
        self.assertEqual(self.result()['status'], 'needs-repair')
        self.assertEqual(self.fake.mutations(), [])

    def test_repair_preserves_body_status_labels_and_sources(self):
        before = copy.deepcopy(self.fake.data)
        self.assertEqual(self.result(True)['status'], 'repaired')
        prd = self.fake.data['issues']['prd']
        for field in ('body', 'status', 'label_ids', 'category'):
            self.assertEqual(prd[field], before['issues']['prd'][field])
        self.assertEqual(self.fake.data['documents'], before['documents'])
        self.assertEqual(prd['milestone_id'], 'm')
        self.assertEqual(self.result(True)['status'], 'consistent')
        self.assertEqual(len(self.fake.mutations()), 1)

    def test_explicit_apply_selection_required(self):
        with self.assertRaises(ValueError):
            self.audit.run('p', apply=True)
        self.assertEqual(self.fake.mutations(), [])

    def test_pagination_selects_all_prds(self):
        self.fake.add('issues', 'second', **{k: v for k, v in self.fake.data['issues']['prd'].items() if k not in ('id', 'version')})
        result = self.audit.run('p')
        self.assertEqual({r['issue_id'] for r in result['issues']}, {'prd', 'second'})
        cursors = [args['cursor'] for name, args in self.fake.calls if name == 'linearboard_list' and args['kind'] == 'issues']
        self.assertEqual(cursors, [0, 1])

    def test_duplicate_story_and_anchor_fail_closed(self):
        self.fake.stories.append(copy.deepcopy(self.fake.stories[0]))
        self.fake.source()
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertEqual(self.fake.mutations(), [])

    def test_malformed_source_json_fail_closed(self):
        self.fake.data['documents']['doc']['body'] = '```json\n{"schema":"' + STORY_SCHEMA + '",oops}\n```\n'
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertEqual(self.fake.mutations(), [])

    def test_multiple_provenance_blocks_fail_closed(self):
        prd = self.fake.data['issues']['prd']
        prd['body'] += prd['body']
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertEqual(self.fake.mutations(), [])

    def test_unknown_story_not_inferred_from_title(self):
        self.fake.data['issues']['prd']['body'] = fenced({'schema': PRD_SCHEMA, 'document_id': 'doc', 'story_ids': ['US-99']})
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertEqual(self.fake.mutations(), [])

    def test_cross_project_source_fail_closed(self):
        self.fake.data['documents']['doc']['project_id'] = 'q'
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertEqual(self.fake.mutations(), [])

    def test_cross_project_selection_fail_closed(self):
        self.fake.data['issues']['prd']['project_id'] = 'q'
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertEqual(self.fake.mutations(), [])

    def test_cross_milestone_split_required(self):
        self.fake.stories[1]['milestone_id'] = 'other'
        self.fake.source()
        self.fake.data['issues']['prd']['body'] = fenced({'schema': PRD_SCHEMA, 'document_id': 'doc', 'story_ids': ['US-01', 'US-02']})
        self.assertIn('Cross-milestone', self.result(True)['error'])
        self.assertEqual(self.fake.mutations(), [])

    def test_partial_failure_retry_only_missing_relation(self):
        self.fake.legacy()
        self.fake.fail_relation = True
        failed = self.result(True)
        self.assertEqual(failed['status'], 'blocked')
        self.assertEqual(failed['applied_actions'], [{'kind': 'milestone', 'value': 'm'}])
        self.assertEqual(self.fake.data['issues']['prd']['milestone_id'], 'm')
        self.assertEqual(self.result(True)['status'], 'repaired')
        self.assertEqual(len([c for c in self.fake.mutations() if c[0] == 'linearboard_update']), 1)
        self.assertEqual(len(self.fake.data['relations']), 1)
        self.assertEqual(self.fake.data['issues']['legacy']['status'], 'Done')

    def test_lost_response_retry_reads_existing_relation(self):
        self.fake.legacy()
        self.fake.lose_relation_response = True
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertEqual(len(self.fake.data['relations']), 1)
        self.assertEqual(self.result(True)['status'], 'consistent')
        self.assertEqual(len([c for c in self.fake.mutations() if c[0] == 'linearboard_create']), 1)

    def test_concurrent_issue_edit_blocks_stale_plan(self):
        plan = self.audit.plan('p', 'prd')
        self.fake.data['issues']['prd']['status'] = 'In Review'
        self.fake.data['issues']['prd']['version'] += 1
        with self.assertRaisesRegex(ValueError, 'Plan changed'):
            self.audit.apply('p', plan)
        self.assertEqual(self.fake.mutations(), [])

    def test_non_numeric_story_and_milestone_ids_supported(self):
        self.fake.stories[0]['id'] = 'PM-US-alpha'
        self.fake.stories[0]['anchor'] = 'story-alpha'
        self.fake.source()
        self.fake.data['issues']['prd']['body'] = '[source](/documents/doc#story-alpha)' + fenced({'schema': PRD_SCHEMA, 'document_id': 'doc', 'story_ids': ['PM-US-alpha']})
        self.assertEqual(self.result(True)['story_ids'], ['PM-US-alpha'])

    def test_reciprocal_relation_reused_with_pagination(self):
        self.fake.legacy()
        self.fake.add('relations', 'irrelevant', project_id='p', source_id='a', target_id='b', relation='related')
        self.fake.add('relations', 'existing', project_id='p', source_id='legacy', target_id='prd', relation='related')
        self.result(True)
        self.assertFalse(any(c[0] == 'linearboard_create' for c in self.fake.mutations()))

    def test_legacy_mismatch_fail_closed(self):
        self.fake.legacy()
        self.fake.data['issues']['legacy']['milestone_id'] = 'other'
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertEqual(self.fake.mutations(), [])

    def test_concurrent_source_change_blocks_apply(self):
        plan = self.audit.plan('p', 'prd')
        self.fake.data['documents']['doc']['version'] += 1
        with self.assertRaisesRegex(ValueError, 'Plan changed'):
            self.audit.apply('p', plan)
        self.assertEqual(self.fake.mutations(), [])

    def test_source_change_at_write_boundary_blocks_apply(self):
        plan = self.audit.plan('p', 'prd')
        count = [0]
        def race(kind, rid):
            if kind == 'documents':
                count[0] += 1
                if count[0] == 2:
                    self.fake.data[kind][rid]['version'] += 1
        self.fake.on_get = race
        with self.assertRaisesRegex(ValueError, 'Concurrent change'):
            self.audit.apply('p', plan)
        self.assertEqual(self.fake.mutations(), [])

    def test_missing_anchor_reports_blocker(self):
        self.fake.data['documents']['doc']['body'] = self.fake.data['documents']['doc']['body'].replace('<a id="us-01"></a>', '')
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertEqual(self.fake.mutations(), [])

    def test_readable_link_warning_does_not_rewrite_content(self):
        self.fake.data['issues']['prd']['body'] = fenced({'schema': PRD_SCHEMA, 'document_id': 'doc', 'story_ids': ['US-01']})
        result = self.result(True)
        self.assertEqual(len(result['warnings']), 1)
        self.assertNotIn('body', self.fake.mutations()[0][1]['data'])

    def test_collision_story_ids_in_other_doc_do_not_mix(self):
        self.fake.add('documents', 'unrelated', project_id='p', body=self.fake.data['documents']['doc']['body'])
        self.assertEqual(self.result()['document_id'], 'doc')

    def test_deleted_source_fail_closed(self):
        self.fake.data['documents']['doc']['deleted_at'] = 'now'
        self.assertEqual(self.result(True)['status'], 'blocked')
        self.assertEqual(self.fake.mutations(), [])


class CliTests(unittest.TestCase):
    def cli(self, *args):
        return subprocess.run([sys.executable, str(Path(__file__).with_name('traceability.py')), *args], capture_output=True, text=True, timeout=15)

    def test_invalid_origin_and_unbounded_apply_rejected_without_network(self):
        for args in (['--url', 'https://example.com', '--project-id', 'p'],
                     ['--project-id', 'p', '--apply'],
                     ['--url', 'http://127.0.0.1/api', '--project-id', 'p']):
            result = self.cli(*args)
            self.assertEqual(result.returncode, 2)
            self.assertIn('error:', result.stderr)

    def test_cli_http_audit_then_repair_then_idempotent_audit(self):
        fake, requests = Fake(), []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                parsed = urlsplit(self.path)
                requests.append(('GET', parsed.path, None, dict(self.headers)))
                if parsed.path == '/api/capabilities':
                    value = {'application': 'LinearBoard'}
                else:
                    parts = parsed.path.strip('/').split('/')
                    kind = parts[1]
                    if len(parts) == 3:
                        value = fake('linearboard_get', {'kind': kind, 'id': parts[2]})
                    else:
                        query = parse_qs(parsed.query)
                        value = fake('linearboard_list', {'kind': kind, 'filters': json.loads(query['filters'][0]), 'cursor': int(query['cursor'][0]), 'limit': int(query['limit'][0])})
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(value).encode())

            def do_PATCH(self):
                parts = self.path.strip('/').split('/')
                data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                requests.append(('PATCH', self.path, data, dict(self.headers)))
                value = fake('linearboard_update', {'kind': parts[1], 'id': parts[2], 'data': data, 'idempotency_key': self.headers['Idempotency-Key']})
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(value).encode())

        with ThreadingHTTPServer(('127.0.0.1', 0), Handler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            args = ['--url', 'http://127.0.0.1:' + str(server.server_port), '--project-id', 'p', '--issue-id', 'prd']
            try:
                audit = self.cli(*args)
                self.assertEqual(audit.returncode, 1, audit.stderr)
                self.assertEqual(json.loads(audit.stdout)['issues'][0]['status'], 'needs-repair')
                self.assertTrue(all(r[0] == 'GET' for r in requests))
                repaired = self.cli(*args, '--apply')
                self.assertEqual(repaired.returncode, 0, repaired.stderr)
                self.assertEqual(json.loads(repaired.stdout)['issues'][0]['status'], 'repaired')
                writes = [r for r in requests if r[0] != 'GET']
                self.assertEqual(len(writes), 1)
                self.assertEqual(writes[0][2], {'milestone_id': 'm', 'expected_version': 1})
                self.assertTrue(writes[0][3]['Idempotency-Key'].startswith('trace-v1-'))
                again = self.cli(*args, '--apply')
                self.assertEqual(again.returncode, 0, again.stderr)
                self.assertEqual(json.loads(again.stdout)['issues'][0]['status'], 'consistent')
                self.assertEqual(len([r for r in requests if r[0] != 'GET']), 1)
            finally:
                server.shutdown()
                thread.join()


if __name__ == '__main__':
    unittest.main()
