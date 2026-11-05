"""Dependency analysis for the trash confirmation and transactional mutations."""


def deletion_impact(records, kind, record_id):
    """Return records to trash and surviving records that reference them.

    `records` contains all resource kinds, including archived records. Already
    trashed records are deliberately excluded so a later restore cannot claim
    ownership of a previous, independent deletion.
    """
    active = {
        name: [row for row in rows if isinstance(row, dict) and row.get('id') and not row.get('deleted_at')]
        for name, rows in records.items() if isinstance(rows, list)
    }
    by_id = {row['id']: (name, row) for name, rows in active.items() for row in rows}
    ids = record_id if isinstance(record_id, list) else [record_id]
    if (not ids or any(not isinstance(item, str) or not item for item in ids)
            or len(set(ids)) != len(ids) or (len(ids) > 1 and kind != 'issues')):
        raise ValueError('請選擇不重複的任務。')
    if any(item not in by_id or by_id[item][0] != kind for item in ids):
        raise ValueError('找不到可刪除的紀錄。')
    root = by_id[ids[0]][1]
    record_id = ids[0]
    if kind == 'issues' and len({by_id[item][1].get('project_id') for item in ids}) != 1:
        raise ValueError('一次只能刪除同一專案的任務。')
    if kind == 'labels':
        parent = by_id.get(root.get('parent_id'), (None, {}))[1]
        if root.get('name') == 'Category' or parent.get('name') == 'Category':
            raise ValueError('Category 群組與類別標籤不可刪除。')

    included = set(ids)
    if kind == 'projects':
        included.update(row['id'] for name, rows in active.items() for row in rows
                        if name != 'projects' and row.get('project_id') == record_id)
    if kind == 'teams':
        if any(row.get('team_id') == record_id for row in active.get('projects', [])):
            raise ValueError('此團隊仍有專案，請先處理所屬專案。')
        included.update(row['id'] for row in active.get('labels', [])
                        if row.get('team_id') == record_id)
    if kind == 'issues':
        # Traverse arbitrary depth and do not recurse through a malformed cycle.
        while True:
            children = {row['id'] for row in active.get('issues', [])
                        if row.get('parent_id') in included}
            new = children - included
            if not new:
                break
            included.update(new)
    if kind == 'labels' and root.get('is_group'):
        included.update(row['id'] for row in active.get('labels', [])
                        if row.get('parent_id') == record_id)

    # Comments, attachments and evidence belong to their parent record.
    for name in ('comments', 'attachments', 'evidence'):
        for row in active.get(name, []):
            if row.get('target_id') in included or row.get('issue_id') in included:
                included.add(row['id'])

    # A relation or dispatch cannot stand independently without its issue.
    for row in active.get('relations', []):
        if row.get('source_id') in included or row.get('target_id') in included:
            included.add(row['id'])
    for row in active.get('dispatches', []):
        if any(issue_id in included for issue_id in row.get('issue_ids', [])):
            included.add(row['id'])

    def references(row):
        fields = ('project_id', 'team_id', 'milestone_id', 'parent_id',
                  'target_id', 'source_id', 'issue_id')
        if any(row.get(field) in included for field in fields):
            return True
        return any(any(item in included for item in row.get(field, []))
                   for field in ('issue_ids', 'label_ids'))

    deleted = [{'kind': name, 'record': row} for name, rows in active.items()
               for row in rows if row['id'] in included]
    affected = [{'kind': name, 'record': row} for name, rows in active.items()
                for row in rows if row['id'] not in included and references(row)]
    return {'deleted': deleted, 'affected': affected, 'requested_ids': ids}
