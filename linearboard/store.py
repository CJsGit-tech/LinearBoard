"""Transactional application data store. No Linear account or network dependency."""
import base64
import hashlib
import json
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from .trash import deletion_impact

CATEGORIES = ['UserStory', 'ProductRequirement', 'Design', 'FrontEnd', 'BackEnd']
STATUSES = ['Backlog', 'Todo', 'In Progress', 'In Review', 'Done', 'Canceled', 'Duplicate']
KINDS = {'teams', 'projects', 'milestones', 'labels', 'issues', 'documents', 'views', 'comments', 'relations', 'attachments', 'batches', 'dispatches', 'evidence'}

class Invalid(ValueError):
    pass

class Conflict(Invalid):
    pass

def now():
    return datetime.now(timezone.utc).isoformat()

class ClosingConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()

class Store:
    backend = "sqlite"
    record_order = "rowid"

    def _begin(self, db):
        db.execute("BEGIN IMMEDIATE")

    def backup(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "linearboard.sqlite3"
            with self.connect() as source, sqlite3.connect(path) as target:
                source.backup(target)
            return "linearboard.sqlite3", path.read_bytes()

    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS records(id TEXT PRIMARY KEY, kind TEXT NOT NULL, data TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS records_kind ON records(kind);
            CREATE TABLE IF NOT EXISTS history(seq INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT, at TEXT, actor TEXT, action TEXT, before_data TEXT, after_data TEXT);
            CREATE TABLE IF NOT EXISTS requests(key TEXT PRIMARY KEY, fingerprint TEXT, result TEXT);
            CREATE TABLE IF NOT EXISTS blobs(id TEXT PRIMARY KEY, content BLOB NOT NULL);
            CREATE TABLE IF NOT EXISTS counters(team_id TEXT PRIMARY KEY, value INTEGER);
            CREATE TABLE IF NOT EXISTS trash_batches(id TEXT PRIMARY KEY, root_id TEXT NOT NULL, root_kind TEXT NOT NULL, deleted_at TEXT NOT NULL, detached TEXT NOT NULL);
            ''')
            if 'root_ids' not in {row['name'] for row in db.execute('PRAGMA table_info(trash_batches)')}:
                db.execute("ALTER TABLE trash_batches ADD COLUMN root_ids TEXT")
            self._migrate_archived_records(db)
            if not db.execute("SELECT 1 FROM records WHERE kind='teams'").fetchone():
                self._create(db, 'teams', {'name': 'Personal workspace', 'key': 'LB'}, 'system')

    def _migrate_archived_records(self, db):
        """Keep formerly archived records separately recoverable in the trash."""
        self._begin(db)
        entries = [(row['kind'], json.loads(row['data'])) for row in db.execute('SELECT kind,data FROM records')]
        archived_ids = {record['id'] for _, record in entries if record.get('archived') and not record.get('deleted_at')}
        scalar_fields = ('project_id', 'team_id', 'milestone_id', 'parent_id', 'target_id', 'source_id', 'issue_id')
        for _, record in entries:
            if record.get('archived') or record.get('deleted_at'):
                continue
            if (any(record.get(field) in archived_ids for field in scalar_fields)
                    or any(any(value in archived_ids for value in (record.get(field) or []))
                           for field in ('issue_ids', 'label_ids'))):
                raise Invalid('無法轉移封存紀錄：仍有其他紀錄使用它，請先處理相關資料。')
        for kind, old in entries:
            if not old.get('archived'):
                continue
            timestamp = now()
            updated = {**old, 'archived': False, 'version': old['version'] + 1, 'updated_at': timestamp}
            if not old.get('deleted_at'):
                batch_id = uuid.uuid4().hex
                updated.update(deleted_at=timestamp, trash_batch_id=batch_id)
                db.execute('INSERT INTO trash_batches(id,root_id,root_kind,deleted_at,detached,root_ids) VALUES(?,?,?,?,?,?)',
                           (batch_id, old['id'], kind, timestamp, '[]', json.dumps([old['id']])))
            db.execute('UPDATE records SET data=? WHERE id=?', (json.dumps(updated, ensure_ascii=False), old['id']))
            self._audit(db, updated, 'system', 'trash' if not old.get('deleted_at') else 'update', old)

    def connect(self):
        db = sqlite3.connect(self.path, timeout=15, factory=ClosingConnection)
        db.row_factory = sqlite3.Row
        return db

    def _all(self, db, kind, archived=False):
        return [r for row in db.execute('SELECT data FROM records WHERE kind=? ORDER BY ' + self.record_order, (kind,))
                if (r := json.loads(row[0])) and not r.get('deleted_at') and (archived or not r.get('archived'))]

    def _get(self, db, rid, kind=None, include_deleted=False):
        row = db.execute('SELECT kind,data FROM records WHERE id=?', (rid,)).fetchone()
        if not row and kind == 'issues':
            row = next((r for r in db.execute("SELECT kind,data FROM records WHERE kind='issues'") if json.loads(r['data']).get('identifier') == rid), None)
        if not row or (kind and row['kind'] != kind):
            raise Invalid(f'找不到紀錄：{rid}')
        record = json.loads(row['data'])
        if record.get('deleted_at') and not include_deleted:
            raise Invalid(f'紀錄已移至垃圾桶：{rid}')
        return record

    def _ref(self, db, rid, kind, optional=False):
        if not rid and optional:
            return None
        r = self._get(db, rid, kind)
        if r.get('archived'):
            raise Invalid('關聯目標已封存，請先還原。')
        return r

    def _replay(self, db, stored):
        result = json.loads(stored)
        if isinstance(result, dict) and result.get('_purged') is True:
            raise Conflict('原操作包含已永久刪除的紀錄。')
        candidates = result.get('items', []) if isinstance(result, dict) and 'items' in result else [result]
        for record in candidates:
            if isinstance(record, dict) and all(field in record for field in ('id', 'version', 'url')):
                try:
                    self._get(db, record['id'])
                except Invalid as error:
                    raise Conflict('原操作的紀錄已刪除或移至垃圾桶。') from error
        return result

    def _project_match(self, db, r, target, kind):
        related = self._ref(db, target, kind)
        if related.get('project_id') != r.get('project_id'):
            raise Invalid('關聯必須屬於同一專案。')
        return related

    def _referenced_statuses(self, db, team_id):
        # Archived references count too: restoring a record must not invalidate its workflow.
        projects = {p['id'] for p in self._all(db, 'projects', True) if p['team_id'] == team_id}
        used = []
        for issue in self._all(db, 'issues', True):
            if issue.get('project_id') in projects and issue.get('status') not in used:
                used.append(issue['status'])
        for view in self._all(db, 'views', True):
            if view.get('project_id') in projects:
                for status in view.get('statuses') or []:
                    if status not in used:
                        used.append(status)
        return used

    def _workflow(self, db, team_id):
        team = self._get(db, team_id, 'teams')
        if 'statuses' in team:
            return list(team['statuses'])
        # Legacy teams had no configuration. Preserve actual references without
        # reintroducing the previous unused Ready for Test / Blocked defaults.
        return list(dict.fromkeys(STATUSES + self._referenced_statuses(db, team_id)))

    def _validate(self, db, kind, r, actor, old=None):
        if kind not in KINDS:
            raise Invalid('不支援的紀錄類型。')
        if kind in {'teams', 'projects', 'labels', 'views', 'milestones', 'batches'} and not str(r.get('name', '')).strip():
            raise Invalid('名稱不可空白。')
        if kind in {'issues', 'documents'} and not str(r.get('title', '')).strip():
            raise Invalid('標題不可空白。')
        if kind in {'projects', 'labels'}:
            self._ref(db, r.get('team_id'), 'teams')
        if kind == 'teams':
            if 'statuses' in r:
                statuses = r['statuses']
                if (not isinstance(statuses, list) or not statuses
                        or any(not isinstance(s, str) or not s.strip() or s != s.strip() for s in statuses)
                        or len(statuses) != len(set(statuses))):
                    raise Invalid('團隊狀態需為不重複、非空白的字串陣列。')
                missing = [s for s in self._referenced_statuses(db, r['id']) if s not in statuses]
                if missing:
                    raise Invalid('狀態仍被任務或 View 使用，不可移除：' + '、'.join(missing))
            if not re.fullmatch(r'[A-Z][A-Z0-9]{1,9}', r.get('key', '')):
                raise Invalid('團隊代碼需為 2–10 個大寫英數字。')
            for t in self._all(db, 'teams', True):
                if t['id'] != r['id'] and t['key'] == r['key']:
                    raise Invalid('團隊代碼已存在。')
        if kind in {'milestones', 'issues', 'documents', 'views', 'batches', 'dispatches', 'evidence'}:
            project = self._ref(db, r.get('project_id'), 'projects')
            r['team_id'] = project['team_id']
            if r.get('milestone_id'):
                self._project_match(db, r, r['milestone_id'], 'milestones')
        if kind == 'labels':
            if r.get('parent_id'):
                parent = self._ref(db, r['parent_id'], 'labels')
                if parent.get('parent_id') or not parent.get('is_group') or parent['team_id'] != r['team_id'] or r.get('is_group'):
                    raise Invalid('標籤群組或團隊無效。')
            if old and any(old.get(k) != r.get(k) for k in ['team_id', 'parent_id', 'is_group', 'single_select']):
                raise Invalid('標籤結構建立後不可變更，請建立新群組。')
            for label in self._all(db, 'labels', True):
                if label['id'] != r['id'] and all(label.get(k) == r.get(k) for k in ['team_id', 'parent_id', 'name']):
                    raise Invalid('相同群組中已有此標籤。')
            if r.get('name') == 'Category' and (not r.get('is_group') or not r.get('single_select')):
                raise Invalid('Category 必須是單選群組。')
        if kind == 'issues':
            if r.get('status') not in self._workflow(db, r['team_id']) or r.get('category') not in CATEGORIES:
                raise Invalid('狀態或 Category 無效。')
            if r.get('status') == 'Done' and (not old or old.get('status') != 'Done') and actor != 'user':
                raise Invalid('Done 只能由使用者驗收後設定。')
            seen = set()
            categories = []
            for lid in r.get('label_ids', []):
                label = self._ref(db, lid, 'labels')
                if label.get('is_group') or label['team_id'] != r['team_id']:
                    raise Invalid('請選擇同團隊的子標籤，不可套用群組本身。')
                parent = self._ref(db, label['parent_id'], 'labels') if label.get('parent_id') else None
                if parent and parent.get('single_select'):
                    if parent['id'] in seen:
                        raise Invalid(f"{parent['name']} 是單選群組。")
                    seen.add(parent['id'])
                if parent and parent['name'] == 'Category':
                    categories.append(label['name'])
            if categories != [r['category']]:
                raise Invalid('每張 issue 必須且只能有一個對應的 Category 子標籤。')
            if r.get('parent_id'):
                parent = self._project_match(db, r, r['parent_id'], 'issues')
                visited = {r['id']}
                while parent:
                    if parent['id'] in visited:
                        raise Invalid('父子 issue 不可形成循環。')
                    visited.add(parent['id'])
                    parent = self._get(db, parent['parent_id'], 'issues') if parent.get('parent_id') else None
            if r.get('priority') not in ['No priority', 'Urgent', 'High', 'Medium', 'Low']:
                raise Invalid('優先級無效。')
        if kind == 'views':
            if r.get('category') and r['category'] not in CATEGORIES:
                raise Invalid('View Category 無效。')
            statuses = r.get('statuses', [])
            if not isinstance(statuses, list) or any(s not in self._workflow(db, r['team_id']) for s in statuses):
                raise Invalid('View 狀態無效。')
            if r.get('placement') not in ['tabs', 'shared'] or r.get('group_by') not in ['status', 'category', 'milestone_id', 'priority']:
                raise Invalid('View 位置或分組無效。')
        if kind in {'comments', 'attachments'}:
            target = self._ref(db, r.get('target_id'), r.get('target_kind'))
            if r.get('target_kind') not in ['issues', 'documents', 'projects']:
                raise Invalid('不支援此附件或留言位置。')
            r['project_id'] = target['id'] if r['target_kind'] == 'projects' else target['project_id']
            if kind == 'comments' and not r.get('body', '').strip():
                raise Invalid('留言不可空白。')
            if kind == 'attachments':
                if not r.get('name'):
                    raise Invalid('附件需要檔名。')
                r['approval'] = r.get('approval', 'draft')
                if r['approval'] not in ['draft', 'approved', 'superseded', 'evidence']:
                    raise Invalid('附件審閱標記無效。')
                if r['approval'] == 'approved' and (not old or old.get('approval') != 'approved') and actor != 'user':
                    raise Invalid('只有使用者可以核准視覺參考。')
                if r.get('external_url') and not r['external_url'].startswith(('https://', 'http://')):
                    raise Invalid('附件連結需使用 HTTP 或 HTTPS。')
        if kind == 'relations':
            source = self._ref(db, r.get('source_id'), 'issues')
            target = self._ref(db, r.get('target_id'), 'issues')
            r['project_id'] = source['project_id']
            if source['id'] == target['id'] or source['project_id'] != target['project_id']:
                raise Invalid('關聯需為同專案的不同 issues。')
            if r.get('relation') not in ['related', 'blocks', 'supersedes', 'duplicate']:
                raise Invalid('關聯類型無效。')
            for rel in self._all(db, 'relations'):
                same = rel['source_id'] == r['source_id'] and rel['target_id'] == r['target_id']
                inverse = r['relation'] == 'related' and rel['source_id'] == r['target_id'] and rel['target_id'] == r['source_id']
                if rel['id'] != r['id'] and rel['relation'] == r['relation'] and (same or inverse):
                    raise Invalid('關聯已存在。')
            if r['relation'] == 'blocks':
                graph = {}
                for rel in self._all(db, 'relations'):
                    if rel['id'] != r['id'] and rel['relation'] == 'blocks':
                        graph.setdefault(rel['source_id'], []).append(rel['target_id'])
                pending, visited = [r['target_id']], set()
                while pending:
                    item = pending.pop()
                    if item == r['source_id']:
                        raise Invalid('阻擋關係不可形成循環。')
                    if item not in visited:
                        visited.add(item)
                        pending.extend(graph.get(item, []))
        if kind in {'batches', 'dispatches'}:
            ids = r.get('issue_ids', [])
            if (not ids and not (old and kind == 'batches')) or len(ids) != len(set(ids)):
                raise Invalid('請選擇 issues，且不可重複。')
            for iid in ids:
                issue = self._project_match(db, r, iid, 'issues')
                if issue['category'] not in ['FrontEnd', 'BackEnd']:
                    raise Invalid('交付批次只包含 FE／BE issues。')
                if r.get('milestone_id') and issue.get('milestone_id') != r['milestone_id']:
                    raise Invalid('Issue 不屬於所選里程碑。')
                if kind == 'dispatches' and (not old or r.get('state') in ['review', 'executing']):
                    if issue['status'] in ['Canceled', 'In Review', 'Done']:
                        raise Invalid(f"{issue['identifier']} 目前不可派工。")
                    for d in self._all(db, 'dispatches'):
                        if d['id'] != r['id'] and iid in d['issue_ids'] and d.get('state') in ['review', 'executing']:
                            raise Conflict('此 issue 已有進行中的派工。')
            if kind == 'dispatches':
                if len(ids) != 1:
                    raise Invalid('每筆派工負責一張 issue；批次可包含多筆派工。')
                if r.get('state') not in ['review', 'executing', 'completed', 'blocked', 'failed']:
                    raise Invalid('派工狀態無效。')
                if r.get('state') == 'executing' and not r.get('plan', '').strip():
                    raise Invalid('執行前需記錄已審閱的計畫。')
                if r.get('state') == 'completed' and not r.get('report', '').strip():
                    raise Invalid('完成回報不可空白。')
                active = [d for d in self._all(db, 'dispatches') if d['id'] != r['id'] and d.get('state') in ['review', 'executing']]
                if r.get('state') in ['review', 'executing'] and len(active) >= 3:
                    raise Invalid('最多三筆進行中的派工。')
        if kind == 'evidence':
            self._project_match(db, r, r.get('issue_id'), 'issues')
            if r.get('result') not in ['Pass', 'Fail', 'Not tested', 'Environment-blocked']:
                raise Invalid('驗證結果無效。')
            if not r.get('criterion', '').strip() or not r.get('environment', '').strip():
                raise Invalid('驗證需填寫條件與環境。')

    def _audit(self, db, record, actor, action, old=None):
        db.execute('INSERT INTO history(record_id,at,actor,action,before_data,after_data) VALUES(?,?,?,?,?,?)',
                   (record['id'], now(), actor, action, json.dumps(old, ensure_ascii=False) if old else None, json.dumps(record, ensure_ascii=False)))

    def _save(self, db, kind, r, actor, old=None):
        self._validate(db, kind, r, actor, old)
        db.execute('INSERT INTO records(id,kind,data) VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET kind=excluded.kind,data=excluded.data', (r['id'], kind, json.dumps(r, ensure_ascii=False)))
        self._audit(db, r, actor, 'update' if old else 'create', old)
        return r

    def _category_labels(self, db, team_id):
        labels = self._all(db, 'labels')
        group = next((l for l in labels if l['team_id'] == team_id and l['name'] == 'Category' and l.get('is_group')), None)
        if not group:
            group = self._create(db, 'labels', {'name': 'Category', 'team_id': team_id, 'is_group': True, 'single_select': True}, 'system')
        result = {}
        for category in CATEGORIES:
            label = next((l for l in labels if l.get('parent_id') == group['id'] and l['name'] == category), None)
            result[category] = label or self._create(db, 'labels', {'name': category, 'team_id': team_id, 'parent_id': group['id']}, 'system')
        return result

    def _create(self, db, kind, data, actor):
        r = {**data, 'id': uuid.uuid4().hex, 'version': 1, 'created_at': now(), 'updated_at': now(), 'archived': False}
        r['url'] = f"/#/{kind}/{r['id']}"
        if kind == 'teams':
            r.setdefault('key', 'LB')
            r.setdefault('statuses', list(STATUSES))
        if kind == 'issues':
            project = self._ref(db, r.get('project_id'), 'projects')
            team = self._ref(db, project['team_id'], 'teams')
            db.execute('INSERT INTO counters VALUES(?,1) ON CONFLICT(team_id) DO UPDATE SET value=counters.value+1', (team['id'],))
            r['identifier'] = f"{team['key']}-{db.execute('SELECT value FROM counters WHERE team_id=?', (team['id'],)).fetchone()[0]}"
            r.setdefault('category', 'FrontEnd')
            workflow = self._workflow(db, team['id'])
            preferred = 'Todo' if r['category'] == 'Design' else 'Backlog'
            r.setdefault('status', preferred if preferred in workflow else workflow[0])
            r.setdefault('priority', 'No priority')
            r.setdefault('body', '')
            r['label_ids'] = list(dict.fromkeys(r.get('label_ids', [])))
            category = self._category_labels(db, project['team_id']).get(r['category'])
            if not category:
                raise Invalid('Category 無效。')
            if category['id'] not in r['label_ids']:
                r['label_ids'].append(category['id'])
        if kind == 'views':
            r.setdefault('group_by', 'status')
            r.setdefault('placement', 'tabs')
        if kind == 'dispatches':
            r.setdefault('state', 'review')
        if kind == 'labels':
            r.setdefault('parent_id', None)
        saved = self._save(db, kind, r, actor)
        if kind == 'projects':
            self._category_labels(db, saved['team_id'])
        return saved

    def snapshot(self, archived=False):
        with self.connect() as db:
            result = {kind: self._all(db, kind, archived) for kind in KINDS}
            result['attachments'] = [{k: v for k, v in r.items() if k != 'content_base64'} for r in result['attachments']]
            result['categories'], result['statuses'] = CATEGORIES, list(STATUSES)
            result['statuses_by_team'] = {team['id']: self._workflow(db, team['id']) for team in result['teams']}
            return result

    def list(self, kind, filters=None, cursor=0, limit=100, archived=False):
        if kind not in KINDS:
            raise Invalid('不支援的紀錄類型。')
        if filters is not None and not isinstance(filters, dict):
            raise Invalid('篩選條件需為 JSON object。')
        with self.connect() as db:
            rows = self._all(db, kind, archived)
        for key, value in (filters or {}).items():
            if value is not None and value != '':
                # Array payloads select an exact ordered value; scalar payloads
                # retain membership filtering for labels and issue selections.
                rows = [r for r in rows if (value in r.get(key, [])
                        if isinstance(r.get(key), list) and not isinstance(value, list)
                        else r.get(key) == value)]
        cursor, limit = max(0, int(cursor)), min(200, max(1, int(limit)))
        return {'items': rows[cursor:cursor + limit], 'next_cursor': cursor + limit if len(rows) > cursor + limit else None, 'total': len(rows)}

    def get(self, kind, rid):
        with self.connect() as db:
            return self._get(db, rid, kind)

    def mutate(self, kind, data, rid=None, actor='automation', key=None):
        if kind not in KINDS:
            raise Invalid('不支援的紀錄類型。')
        payload = json.dumps([kind, rid, data, actor], sort_keys=True)
        fingerprint = hashlib.sha256(payload.encode()).hexdigest()
        with self.connect() as db:
            self._begin(db)
            if key:
                previous = db.execute('SELECT * FROM requests WHERE key=?', (key,)).fetchone()
                if previous:
                    if previous['fingerprint'] != fingerprint:
                        raise Conflict('此 idempotency key 已用於不同內容。')
                    return self._replay(db, previous['result'])
            data = dict(data)
            if 'deleted_at' in data or 'trash_batch_id' in data:
                raise Invalid('請使用垃圾桶操作修改刪除狀態。')
            if data.get('archived'):
                raise Invalid('不支援封存；請使用垃圾桶。')
            old = self._get(db, rid, kind) if rid else None
            if old:
                expected = data.pop('expected_version', None)
                if expected is None or expected != old['version']:
                    raise Conflict('此紀錄已變更，請重新讀取後再儲存。')
                for field in ['id', 'identifier', 'created_at', 'team_id', 'project_id', 'url']:
                    if field in data and data[field] != old.get(field):
                        raise Invalid(f'{field} 不可變更。')
                r = {**old, **data, 'version': old['version'] + 1, 'updated_at': now()}
                if kind == 'issues' and r['category'] != old['category']:
                    category_labels = self._category_labels(db, r['team_id'])
                    catids = {v['id'] for v in category_labels.values()}
                    r['label_ids'] = [x for x in r.get('label_ids', []) if x not in catids] + [category_labels[r['category']]['id']]
                r = self._save(db, kind, r, actor, old)
            else:
                data.pop('expected_version', None)
                content = data.pop('content_base64', None) if kind == 'attachments' else None
                if content is not None:
                    try:
                        blob = base64.b64decode(content, validate=True)
                    except (ValueError, TypeError):
                        raise Invalid('附件編碼無效。')
                    if len(blob) > 15 * 1024 * 1024:
                        raise Invalid('附件不可超過 15 MB。')
                    data['size'] = len(blob)
                    data['sha256'] = hashlib.sha256(blob).hexdigest()
                elif kind == 'attachments' and not data.get('external_url'):
                    raise Invalid('請上傳檔案或提供連結。')
                r = self._create(db, kind, data, actor)
                if content is not None:
                    db.execute('INSERT INTO blobs VALUES(?,?)', (r['id'], blob))
            if key:
                db.execute('INSERT INTO requests VALUES(?,?,?)', (key, fingerprint, json.dumps(r)))
            return r

    def update_issue_statuses(self, data, actor='automation', key=None):
        """Validate the entire selection before committing any status changes."""
        ids = data.get('issue_ids')
        versions = data.get('expected_versions')
        status = data.get('status')
        if set(data) != {'issue_ids', 'expected_versions', 'status'}:
            raise Invalid('批次操作只接受任務、版本與狀態。')
        if (not isinstance(ids, list) or not ids
                or any(not isinstance(i, str) or not i for i in ids)
                or len(ids) != len(set(ids))):
            raise Invalid('請選取任務，且不可重複。')
        if (not isinstance(versions, dict) or set(versions) != set(ids)
                or any(type(v) is not int for v in versions.values())):
            raise Invalid('每個任務都需要對應的版本。')
        if not isinstance(status, str):
            raise Invalid('請選擇有效的工作狀態。')
        payload = json.dumps(['issue-statuses', data, actor], sort_keys=True)
        fingerprint = hashlib.sha256(payload.encode()).hexdigest()
        with self.connect() as db:
            self._begin(db)
            if key:
                previous = db.execute('SELECT * FROM requests WHERE key=?', (key,)).fetchone()
                if previous:
                    if previous['fingerprint'] != fingerprint:
                        raise Conflict('此 idempotency key 已用於不同內容。')
                    return self._replay(db, previous['result'])
            records = [self._ref(db, iid, 'issues') for iid in ids]
            if len({r['project_id'] for r in records}) != 1:
                raise Invalid('一次只能更新同一專案的任務。')
            pending = []
            for old in records:
                if old['version'] != versions[old['id']]:
                    raise Conflict(f"{old['identifier']} 已變更；本次未更新任何任務，請重新讀取後再試。")
                updated = {**old, 'status': status}
                self._validate(db, 'issues', updated, actor, old)
                pending.append((old, updated))
            items, count = [], 0
            for old, updated in pending:
                if old['status'] == status:
                    items.append(old)
                    continue
                updated.update(version=old['version'] + 1, updated_at=now())
                items.append(self._save(db, 'issues', updated, actor, old))
                count += 1
            result = {'items': items, 'updated': count}
            if key:
                db.execute('INSERT INTO requests VALUES(?,?,?)', (key, fingerprint, json.dumps(result)))
            return result

    def history(self, rid):
        with self.connect() as db:
            return [{**dict(r), 'before_data': json.loads(r['before_data']) if r['before_data'] else None, 'after_data': json.loads(r['after_data'])}
                    for r in db.execute('SELECT * FROM history WHERE record_id=? ORDER BY seq DESC', (rid,))]

    def trash_impact(self, kind, rid):
        """Inspect a deletion without changing records, including archived dependents."""
        if kind not in KINDS:
            raise Invalid('不支援的紀錄類型。')
        with self.connect() as db:
            records = {name: self._all(db, name, True) for name in KINDS}
            try:
                result = deletion_impact(records, kind, rid)
                result['fingerprint'] = self._impact_fingerprint(result)
                return result
            except ValueError as error:
                raise Invalid(str(error)) from error

    @staticmethod
    def _impact_fingerprint(impact):
        items = sorted((side, item['kind'], item['record']['id'], item['record']['version'])
                       for side in ('deleted', 'affected') for item in impact[side])
        return hashlib.sha256(json.dumps([items, sorted(impact['requested_ids'])]).encode()).hexdigest()

    def trash_move(self, kind, rid, fingerprint, actor='user', key=None):
        """Atomically move a confirmed impact set to the trash."""
        if kind not in KINDS or not fingerprint:
            raise Invalid('請先確認刪除影響。')
        with self.connect() as db:
            self._begin(db)
            request_hash = hashlib.sha256(json.dumps(['trash-move', kind, rid, fingerprint, actor], sort_keys=True).encode()).hexdigest()
            if key:
                previous = db.execute('SELECT * FROM requests WHERE key=?', (key,)).fetchone()
                if previous:
                    if previous['fingerprint'] != request_hash:
                        raise Conflict('此 idempotency key 已用於不同內容。')
                    result = json.loads(previous['result'])
                    if not db.execute('SELECT 1 FROM trash_batches WHERE id=?', (result.get('batch_id'),)).fetchone():
                        raise Conflict('該次刪除已還原或清除。')
                    return result
            records = {name: self._all(db, name, True) for name in KINDS}
            try:
                impact = deletion_impact(records, kind, rid)
            except ValueError as error:
                raise Invalid(str(error)) from error
            if self._impact_fingerprint(impact) != fingerprint:
                raise Conflict('相關紀錄已變更，請重新確認刪除影響。')
            deleted = {entry['record']['id'] for entry in impact['deleted']}
            detached = []
            # Remove selected references from surviving records; preserve both
            # sides so a later restore never overwrites a subsequent user edit.
            for entry in impact['affected']:
                old, resource = entry['record'], entry['kind']
                changes = {}
                if old.get('milestone_id') in deleted:
                    changes['milestone_id'] = ''
                for field in ('label_ids', 'issue_ids'):
                    if any(item in deleted for item in old.get(field, [])):
                        changes[field] = [item for item in old[field] if item not in deleted]
                if not changes:
                    raise Invalid('有無法安全解除的關聯，請先處理。')
                updated = {**old, **changes, 'version': old['version'] + 1, 'updated_at': now()}
                self._save(db, resource, updated, actor, old)
                detached.append({'kind': resource, 'id': old['id'],
                                 'before': {field: old[field] for field in changes}, 'after': changes})
            batch_id, timestamp = uuid.uuid4().hex, now()
            for entry in impact['deleted']:
                old = entry['record']
                updated = {**old, 'deleted_at': timestamp, 'trash_batch_id': batch_id,
                           'version': old['version'] + 1, 'updated_at': timestamp}
                db.execute('UPDATE records SET data=? WHERE id=?', (json.dumps(updated, ensure_ascii=False), old['id']))
                self._audit(db, updated, actor, 'trash', old)
            roots = impact['requested_ids']
            db.execute('INSERT INTO trash_batches(id,root_id,root_kind,deleted_at,detached,root_ids) VALUES(?,?,?,?,?,?)',
                       (batch_id, roots[0], kind, timestamp, json.dumps(detached, ensure_ascii=False), json.dumps(roots)))
            result = {'batch_id': batch_id, 'deleted': len(deleted), 'detached': len(detached)}
            if key:
                db.execute('INSERT INTO requests VALUES(?,?,?)', (key, request_hash, json.dumps(result)))
            return result

    def trash_list(self):
        with self.connect() as db:
            rows = db.execute('SELECT * FROM trash_batches ORDER BY deleted_at DESC').fetchall()
            return [{'batch_id': row['id'], 'kind': row['root_kind'], 'deleted_at': row['deleted_at'],
                     'root_ids': json.loads(row['root_ids']) if row['root_ids'] else [row['root_id']],
                     'record': self._get(db, row['root_id'], row['root_kind'], include_deleted=True),
                     'count': sum(1 for item in db.execute('SELECT data FROM records')
                                  if json.loads(item['data']).get('trash_batch_id') == row['id'])}
                    for row in rows]

    def trash_restore(self, batch_id, actor='user', key=None):
        """Restore one complete batch and safely reconnect unchanged fields."""
        with self.connect() as db:
            self._begin(db)
            request_hash = hashlib.sha256(json.dumps(['trash-restore', batch_id, actor]).encode()).hexdigest()
            if key:
                previous = db.execute('SELECT * FROM requests WHERE key=?', (key,)).fetchone()
                if previous:
                    if previous['fingerprint'] != request_hash:
                        raise Conflict('此 idempotency key 已用於不同內容。')
                    result = json.loads(previous['result'])
                    if result.get('_purged') is True:
                        raise Conflict('原操作包含已永久刪除的紀錄。')
                    return result
            batch = db.execute('SELECT * FROM trash_batches WHERE id=?', (batch_id,)).fetchone()
            if not batch:
                raise Invalid('找不到垃圾桶紀錄。')
            entries = [(row['kind'], json.loads(row['data'])) for row in db.execute('SELECT kind,data FROM records')]
            restoring = [(kind, row) for kind, row in entries if row.get('trash_batch_id') == batch_id]
            ids = {row['id'] for _, row in restoring}
            if not ids or batch['root_id'] not in ids:
                raise Conflict('垃圾桶資料不完整，無法還原。')
            for kind, row in restoring:
                for field, target_kind in (('project_id', 'projects'), ('team_id', 'teams'), ('parent_id', kind)):
                    target = row.get(field)
                    if target and target not in ids:
                        try:
                            self._get(db, target, target_kind)
                        except Invalid as error:
                            raise Invalid('請先還原所屬團隊、專案或上層紀錄。') from error
            for kind, old in restoring:
                updated = {k: v for k, v in old.items() if k not in ('deleted_at', 'trash_batch_id')}
                updated.update(version=old['version'] + 1, updated_at=now())
                db.execute('UPDATE records SET data=? WHERE id=?', (json.dumps(updated, ensure_ascii=False), old['id']))
                self._audit(db, updated, actor, 'restore', old)
            # The whole batch is visible before checking cross-record references.
            for kind, old in restoring:
                restored = self._get(db, old['id'], kind)
                self._validate(db, kind, dict(restored), actor, restored)
            warnings = []
            for change in json.loads(batch['detached']):
                try:
                    old = self._get(db, change['id'], change['kind'])
                    if any(old.get(field) != value for field, value in change['after'].items()):
                        warnings.append(change['id'])
                        continue
                    updated = {**old, **change['before'], 'version': old['version'] + 1, 'updated_at': now()}
                    self._save(db, change['kind'], updated, actor, old)
                except Invalid:
                    warnings.append(change['id'])
            db.execute('DELETE FROM trash_batches WHERE id=?', (batch_id,))
            result = {'restored': len(restoring), 'unrestored_links': warnings}
            if key:
                db.execute('INSERT INTO requests VALUES(?,?,?)', (key, request_hash, json.dumps(result)))
            return result

    def trash_purge(self, batch_ids):
        """Permanently remove exactly the confirmed batches as one transaction."""
        if (not isinstance(batch_ids, list) or not batch_ids
                or any(not isinstance(item, str) or not item for item in batch_ids)
                or len(set(batch_ids)) != len(batch_ids)):
            raise Invalid('請選擇要永久刪除的垃圾桶紀錄。')
        with self.connect() as db:
            self._begin(db)
            batches = {row['id'] for row in db.execute('SELECT id FROM trash_batches')}
            if not set(batch_ids) <= batches:
                raise Conflict('垃圾桶內容已變更，請重新確認。')
            records = [(row['kind'], json.loads(row['data'])) for row in db.execute('SELECT kind,data FROM records')]
            purged = {record['id'] for _, record in records if record.get('trash_batch_id') in batch_ids}
            if not purged:
                raise Conflict('垃圾桶內容已變更，請重新確認。')
            for _, record in records:
                if record['id'] in purged:
                    continue
                fields = ('project_id', 'team_id', 'milestone_id', 'parent_id', 'target_id', 'source_id', 'issue_id')
                if (any(record.get(field) in purged for field in fields)
                        or any(any(value in purged for value in record.get(field, [])) for field in ('issue_ids', 'label_ids'))):
                    raise Conflict('其他紀錄仍參照這些項目，請先還原或刪除相關紀錄。')
            for record_id in purged:
                db.execute('DELETE FROM blobs WHERE id=?', (record_id,))
                db.execute('DELETE FROM history WHERE record_id=?', (record_id,))
                db.execute('DELETE FROM records WHERE id=?', (record_id,))
            for row in db.execute('SELECT key,result FROM requests').fetchall():
                if any(record_id in row['result'] for record_id in purged):
                    db.execute('UPDATE requests SET result=? WHERE key=?', ('{"_purged":true}', row['key']))
            db.executemany('DELETE FROM trash_batches WHERE id=?', [(batch_id,) for batch_id in batch_ids])
            return {'purged': len(purged)}

    def blob(self, rid):
        with self.connect() as db:
            metadata = self._get(db, rid, 'attachments')
            row = db.execute('SELECT content FROM blobs WHERE id=?', (rid,)).fetchone()
            if not row:
                raise Invalid('這是外部連結，沒有本機檔案。')
            return metadata, row[0]

    def view_members(self, rid):
        view = self.get('views', rid)
        rows = self.list('issues', {'project_id': view['project_id']}, limit=200)['items']
        # Use the full collection rather than truncating a View at an API page boundary.
        with self.connect() as db:
            rows = self._all(db, 'issues')
        return [r for r in rows if r['project_id'] == view['project_id']
                and (not view.get('category') or r['category'] == view['category'])
                and (not view.get('milestone_id') or r.get('milestone_id') == view['milestone_id'])
                and (not view.get('statuses') or r['status'] in view['statuses'])
                and all(lid in r.get('label_ids', []) for lid in view.get('label_ids', []))]
