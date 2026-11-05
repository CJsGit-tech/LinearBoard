"""Lossless, transactional SQLite import; refuses a nonempty, different target."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from linearboard.postgres import PostgresStore

TABLES = {
    'records':['id','kind','data'],
    'history':['seq','record_id','at','actor','action','before_data','after_data'],
    'requests':['key','fingerprint','result'],
    'blobs':['id','content'],
    'counters':['team_id','value'],
    'trash_batches':['id','root_id','root_kind','deleted_at','detached','root_ids'],
}


def digest(rows):
    encoded = [[bytes(v).hex() if isinstance(v, (bytes, memoryview)) else v for v in row] for row in rows]
    return hashlib.sha256(json.dumps(sorted(encoded, key=lambda row: str(row[0])), ensure_ascii=False).encode()).hexdigest()


def migrate(source, target):
    # Source is a read-only, consistent SQLite snapshot. Never edit the original.
    source = Path(source).resolve()
    wal = Path(str(source) + '-wal')
    if wal.exists() and wal.stat().st_size:
        raise RuntimeError('Use a completed SQLite backup; source has pending WAL data')
    with sqlite3.connect(f'file:{source}?mode=ro&immutable=1', uri=True) as db:
        db.execute('BEGIN')
        if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise RuntimeError('SQLite integrity check failed')
        rows = {table:list(db.execute('SELECT '+','.join(columns)+' FROM '+table+(' ORDER BY rowid' if table=='records' else '')))
                for table, columns in TABLES.items()}
    with target.connect() as db:
        existing = {table:[tuple(row.values()) for row in db.execute('SELECT '+','.join(columns)+' FROM '+table)]
                    for table, columns in TABLES.items()}
        if any(existing.values()):
            if all(digest(existing[t]) == digest(rows[t]) for t in TABLES):
                print('Already migrated: all tables match; no changes made')
                return
            raise RuntimeError('Target contains different data; refusing to overwrite it')
        for table, columns in TABLES.items():
            if rows[table]:
                db.executemany('INSERT INTO '+table+'('+','.join(columns)+') VALUES('+','.join('?' for _ in columns)+')', rows[table])
            actual = [tuple(row.values()) for row in db.execute('SELECT '+','.join(columns)+' FROM '+table)]
            if digest(actual) != digest(rows[table]):
                raise RuntimeError('Verification failed: '+table)
        db.execute("SELECT setval(pg_get_serial_sequence('history','seq'), COALESCE((SELECT MAX(seq) FROM history),1), EXISTS(SELECT 1 FROM history))")
        print(json.dumps({table:{'rows':len(rows[table]), 'sha256':digest(rows[table])} for table in TABLES}, indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', help='Read-only SQLite backup path')
    args=parser.parse_args()
    migrate(args.source, PostgresStore(os.environ['DATABASE_URL'], seed=False))
