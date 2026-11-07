#!/usr/bin/env python3
"""Audit document-story → PRD → native milestone links; repair only explicit PRD metadata."""
import argparse
import hashlib
import json
import os
import re
import sys
from urllib.parse import urljoin, urlsplit
from adapter import request_tool

STORY_SCHEMA = 'linearboard-story-index-v1'
PRD_SCHEMA = 'linearboard-prd-sources-v1'


def block(body, schema):
    found = []
    for raw in re.findall(r'^```json\s*\n(.*?)^```\s*$', body, re.M | re.S):
        try:
            value = json.loads(raw)
        except ValueError:
            if schema in raw:
                raise ValueError('Malformed ' + schema)
            continue
        if isinstance(value, dict) and value.get('schema') == schema:
            found.append(value)
    if len(found) != 1:
        raise ValueError('Expected exactly one ' + schema + ' block')
    return found[0]



def readable_markdown(body):
    """Exclude code when checking rendered anchors/links; reject ambiguous open spans."""
    lines, fence = [], None
    for line in body.splitlines(keepends=True):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line.rstrip('\r\n'))
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
            continue
        if marker:
            fence = (marker[1][0], len(marker[1]))
            continue
        lines.append(line)
    text, parts, pos = ''.join(lines), [], 0
    while True:
        opening = re.search(r'`+', text[pos:])
        if not opening:
            parts.append(text[pos:])
            break
        start, end = pos + opening.start(), pos + opening.end()
        parts.append(text[pos:start])
        ticks = text[start:end]
        closing = re.search(r'(?<!`)' + re.escape(ticks) + r'(?!`)', text[end:])
        if not closing:
            break
        pos = end + closing.end()
    return ''.join(parts)


def prd_sources(body, base_url):
    """Read the declared source line, or a historical fenced record."""
    lines = re.findall(r'^\*\*Source stories:\*\*[^\n]*$', readable_markdown(body), re.M)
    if not lines:
        return block(body, PRD_SCHEMA)
    if len(lines) != 1 or PRD_SCHEMA in body:
        raise ValueError('Ambiguous PRD source declarations')
    links = re.findall(r'\[([\w-]+)\]\(([^\s)]+)\)', lines[0])
    residue = re.sub(r'\[([\w-]+)\]\(([^\s)]+)\)', '', lines[0].split('**', 2)[2])
    if not links or residue.strip(' ,·\t'):
        raise ValueError('Expected only source story links on the declared line')
    documents = set()
    anchors = {}
    for sid, target in links:
        absolute = urljoin(base_url, target)
        route = re.fullmatch(re.escape(base_url.rstrip('/')) + r'/#/documents/([\w-]+)#([\w-]+)', absolute)
        if not route or sid in anchors:
            raise ValueError('Invalid or duplicate source story link')
        documents.add(route[1])
        anchors[sid] = route[2]
    if len(documents) != 1:
        raise ValueError('Sources must share one milestone document')
    return {'document_id': documents.pop(), 'story_ids': list(anchors), 'anchors': anchors}


def grouped_stories(body):
    """Read story ownership from the human-readable numbered milestone sections."""
    readable = readable_markdown(body)
    sections = re.split(r'(?m)(?=^## )', readable)
    entries = []
    for section in sections:
        if not re.match(r'^## M[1-9]\d* — ', section):
            if re.search(r'^#### ', section, re.M):
                raise ValueError('Story outside a numbered milestone')
            continue
        links = re.findall(r'^\[Native milestone\]\([^\n)]*#/milestones/([\w-]+)\)', section, re.M)
        if len(links) != 1:
            raise ValueError('Expected one native milestone link in numbered section')
        parts = re.split(r'(?m)(?=^<a id=)', section)
        for part in parts[1:]:
            match = re.match(r'^<a id="([\w-]+)"></a>\s*\n#### ([\w-]+) — ', part)
            if not match:
                raise ValueError('Expected anchored story heading in numbered section')
            entry = dict(id=match[2], anchor=match[1], milestone_id=links[0])
            legacy = re.search(r'^- \*\*Legacy source:\*\* .*?#/issues/([\w-]+)\)', part, re.M)
            if legacy:
                entry['legacy_issue_id'] = legacy[1]
            entries.append(entry)
        if len(parts)-1 != len(re.findall(r'^#### ', section, re.M)):
            raise ValueError('Missing story anchor')
    return entries


def nonempty(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Missing or invalid ' + name)
    return value


def key(operation, data):
    raw = json.dumps([operation, data], sort_keys=True, separators=(',', ':'))
    return 'trace-v1-' + hashlib.sha256(raw.encode()).hexdigest()


class Traceability:
    def __init__(self, call, base_url="http://127.0.0.1:8765"):
        self.call = call
        self.base_url = base_url

    def get(self, kind, rid):
        value = self.call('linearboard_get', {'kind': kind, 'id': rid})
        if value.get('id') != rid or not isinstance(value.get('version'), int):
            raise ValueError('Invalid identity/version for ' + rid)
        if value.get('deleted_at'):
            raise ValueError('Deleted record ' + rid)
        return value

    def listing(self, kind, filters):
        cursor, seen, items = 0, set(), []
        while True:
            result = self.call('linearboard_list', {'kind': kind, 'filters': filters, 'cursor': cursor, 'limit': 100})
            items.extend(result['items'])
            cursor = result.get('next_cursor')
            if cursor is None:
                return items
            if cursor in seen:
                raise ValueError('Repeated pagination cursor')
            seen.add(cursor)

    def plan(self, project_id, issue_id):
        issue = self.get('issues', issue_id)
        if issue.get('project_id') != project_id or issue.get('category') != 'ProductRequirement':
            raise ValueError('Selection is not a PRD in the selected project')
        source = prd_sources(issue.get('body', ''), self.base_url)
        doc_id = nonempty(source.get('document_id'), 'document_id')
        ids = source.get('story_ids')
        if not isinstance(ids, list) or not ids or any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != len(ids):
            raise ValueError('story_ids must be a nonempty distinct string array')
        doc = self.get('documents', doc_id)
        if doc.get('project_id') != project_id:
            raise ValueError('Source document belongs to another project')
        body = doc.get('body', '')
        # Historical documents may still carry the earlier source format.
        entries = block(body, STORY_SCHEMA).get('stories') if STORY_SCHEMA in body else grouped_stories(body)
        if not isinstance(entries, list) or not entries:
            raise ValueError('Story index must be a nonempty array')
        indexed, anchors = {}, set()
        readable_body = readable_markdown(doc.get('body', ''))
        for story in entries:
            if not isinstance(story, dict):
                raise ValueError('Malformed story index entry')
            sid = nonempty(story.get('id'), 'story id')
            mid = nonempty(story.get('milestone_id'), 'milestone_id')
            anchor = nonempty(story.get('anchor'), 'anchor')
            if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', anchor):
                raise ValueError('Unsafe anchor ' + anchor)
            if sid in indexed or anchor in anchors:
                raise ValueError('Duplicate story id or anchor')
            matches = re.findall(r'<a\s+id=[\"\']' + re.escape(anchor) + r'[\"\']\s*>\s*</a>', readable_body)
            if len(matches) != 1:
                raise ValueError('Missing or duplicate explicit source anchor ' + anchor)
            indexed[sid] = story
            anchors.add(anchor)
        if any(sid not in indexed for sid in ids):
            raise ValueError('Unknown source story id')
        selected = [indexed[sid] for sid in ids]
        if 'anchors' in source and any(source['anchors'][s['id']] != s['anchor'] for s in selected):
            raise ValueError('Source link does not match its story anchor')
        mids = {s['milestone_id'] for s in selected}
        if len(mids) != 1:
            raise ValueError('Cross-milestone PRD: split or explicitly revise source grouping')
        mid = next(iter(mids))
        milestone = self.get('milestones', mid)
        if milestone.get('project_id') != project_id:
            raise ValueError('Source milestone belongs to another project')
        tracked = [('issues', issue), ('documents', doc), ('milestones', milestone)]
        legacy = []
        for story in selected:
            if 'legacy_issue_id' in story:
                lid = nonempty(story['legacy_issue_id'], 'legacy_issue_id')
                old = self.get('issues', lid)
                if old.get('project_id') != project_id or old.get('category') != 'UserStory' or old.get('milestone_id') != mid:
                    raise ValueError('Legacy source is not a UserStory in the same project/milestone')
                tracked.append(('issues', old))
                legacy.append(lid)
        if len(set(legacy)) != len(legacy):
            raise ValueError('Ambiguous legacy issue mapping')
        relations = self.listing('relations', {'project_id': project_id})
        related = {r['target_id'] if r['source_id'] == issue_id else r['source_id']
                   for r in relations if r.get('relation') == 'related' and issue_id in (r.get('source_id'), r.get('target_id'))}
        missing = sorted(set(legacy) - related)
        for lid in missing:
            if any({r.get('source_id'), r.get('target_id')} == {issue_id, lid} for r in relations):
                raise ValueError('Existing non-related source relation requires manual reconciliation')
        actions = []
        if issue.get('milestone_id') != mid:
            actions.append({'kind': 'milestone', 'value': mid})
        actions.extend({'kind': 'related', 'value': lid} for lid in missing)
        # Link text remains human-owned; automation reports missing links without rewriting body.
        warnings = []
        if 'anchors' in source:
            stage = re.match(r'^(M[1-9]\d*)\b', milestone.get('name', ''))
            if not stage:
                raise ValueError('Missing stable M-number in milestone name')
            team_labels = self.listing('labels', {'team_id': issue['team_id']})
            expected_tags = [stage[1]]
            for sid in ids:
                numeric = re.fullmatch(r'US-(\d+)', sid)
                if numeric:
                    expected_tags.append('US' + str(int(numeric[1])))
                else:
                    warnings.append('Verify custom story tag mapping for ' + sid)
            for tag in expected_tags:
                matches = [x for x in team_labels if x['name'] == tag and not x.get('archived') and not x.get('is_group')]
                if len(matches) != 1 or matches[0]['id'] not in issue.get('label_ids', []):
                    warnings.append('Missing or ambiguous tracking tag ' + tag)
        readable_issue = readable_markdown(issue.get('body', ''))
        links = re.findall(r'\[[^\]]+\]\(([^\s)]+)\)', readable_issue)
        doc_url = doc.get('url')
        for story in selected:
            expected = urljoin(self.base_url, doc_url + '#' + story['anchor']) if doc_url else None
            if not expected or not any(urljoin(self.base_url, link) == expected for link in links):
                warnings.append('Missing verified readable source link for ' + story['id'])
        return {'issue_id': issue_id, 'document_id': doc_id, 'story_ids': ids, 'milestone_id': mid,
                'actions': actions, 'warnings': warnings, '_tracked': tracked}

    def unchanged(self, tracked):
        for kind, record in tracked:
            latest = self.get(kind, record['id'])
            if latest != record:
                raise ValueError('Concurrent change to ' + record['id'] + '; rerun audit')

    def apply(self, project_id, plan):
        self._last_applied = []
        issue_id = plan['issue_id']
        # Recompute at the boundary: never execute an old in-memory action list.
        fresh = self.plan(project_id, issue_id)
        if fresh != plan:
            raise ValueError('Plan changed before repair; rerun audit')
        for action in plan['actions']:
            self.unchanged(plan['_tracked'])
            if action['kind'] == 'milestone':
                issue = plan['_tracked'][0][1]
                data = {'milestone_id': action['value'], 'expected_version': issue['version']}
                self.call('linearboard_update', {'kind': 'issues', 'id': issue_id, 'data': data,
                                                'idempotency_key': key('milestone', [issue_id, data])})
                updated = self.get('issues', issue_id)
                expected = {**issue, 'milestone_id': action['value']}
                # Server-managed timestamps and version change; all product fields must survive.
                for field, value in expected.items():
                    if field not in ('version', 'updated_at') and updated.get(field) != value:
                        raise ValueError('Unexpected changed field ' + field)
                plan['_tracked'][0] = ('issues', updated)
            else:
                # Recheck reciprocal relations immediately before creation and on subsequent runs.
                current = self.listing('relations', {'project_id': project_id})
                pair = {issue_id, action['value']}
                if any(r.get('relation') != 'related' and {r.get('source_id'), r.get('target_id')} == pair for r in current):
                    raise ValueError('Concurrent conflicting source relation; rerun audit')
                if not any(r.get('relation') == 'related' and {r.get('source_id'), r.get('target_id')} == pair for r in current):
                    data = {'source_id': issue_id, 'target_id': action['value'], 'relation': 'related'}
                    self.call('linearboard_create', {'kind': 'relations', 'data': data,
                                                    'idempotency_key': key('related', data)})
                current = self.listing('relations', {'project_id': project_id})
                if not any(r.get('relation') == 'related' and {r.get('source_id'), r.get('target_id')} == pair for r in current):
                    raise ValueError('Relation readback failed')
            self._last_applied.append(dict(action))
        self.unchanged(plan['_tracked'])
        result = self.plan(project_id, issue_id)
        if result['actions']:
            raise ValueError('Repair readback remains inconsistent')
        return result

    def run(self, project_id, issue_ids=None, apply=False):
        self.get('projects', project_id)
        if apply and not issue_ids:
            raise ValueError('--apply requires explicit PRD issue IDs')
        ids = issue_ids or [r['id'] for r in self.listing('issues', {'project_id': project_id, 'category': 'ProductRequirement'})]
        if len(set(ids)) != len(ids):
            raise ValueError('Duplicate selected issue IDs')
        reports = []
        for rid in ids:
            self._last_applied = []
            try:
                plan = self.plan(project_id, rid)
                applied_actions = [dict(a) for a in plan['actions']] if apply else []
                changed = bool(plan['actions'])
                if apply and changed:
                    plan = self.apply(project_id, plan)
                reports.append({k: v for k, v in plan.items() if not k.startswith('_')} |
                               {'status': 'repaired' if apply and changed else 'needs-repair' if changed else 'consistent',
                                'applied_actions': applied_actions})
            except (ValueError, KeyError, OSError) as error:
                reports.append({'issue_id': rid, 'status': 'blocked', 'error': str(error),
                                'applied_actions': list(self._last_applied)})
        return {'project_id': project_id, 'mode': 'apply' if apply else 'audit', 'issues': reports}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default=os.environ.get('LINEARBOARD_URL', 'http://127.0.0.1:8765'))
    parser.add_argument('--project-id', required=True)
    parser.add_argument('--issue-id', action='append', help='Exact native PRD ID; repeat to select more')
    parser.add_argument('--apply', action='store_true', help='Explicitly repair selected PRD metadata only')
    args = parser.parse_args()
    url = urlsplit(args.url)
    if url.scheme != 'http' or url.hostname not in ('127.0.0.1', 'localhost', '::1') or url.username or url.password or url.path not in ('', '/') or url.query or url.fragment:
        parser.error('Use an explicit loopback HTTP service origin')
    if args.apply and not args.issue_id:
        parser.error('--apply requires one or more --issue-id selections')
    call = lambda name, payload: request_tool(args.url.rstrip('/'), name, payload)
    capabilities = call('linearboard_capabilities', {})
    if capabilities.get('application') != 'LinearBoard':
        raise ValueError('Destination is not LinearBoard')
    result = Traceability(call, args.url.rstrip('/')).run(args.project_id, args.issue_id, args.apply)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(any(i['status'] in ('blocked', 'needs-repair') or i.get('warnings') for i in result['issues']))


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
