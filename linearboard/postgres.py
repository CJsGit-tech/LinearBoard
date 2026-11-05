"""PostgreSQL persistence using the same application validation and transactions."""
import os
import subprocess
from pathlib import Path
import psycopg
from psycopg.conninfo import conninfo_to_dict, make_conninfo
from .store import Store

# The repository uses sqlite.Row's named and positional access in its shared store.
class Row(dict):
    def __getitem__(self, key):
        return tuple(self.values())[key] if isinstance(key, int) else super().__getitem__(key)


def row_factory(cursor):
    names = [column.name for column in (cursor.description or [])]
    return lambda values: Row(zip(names, values))


class Connection:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        self.connection.__enter__()
        # Preserve SQLite's serialized mutation semantics, including read/validate/write.
        # Acquiring before any read prevents stale validation across concurrent requests.
        self.connection.execute('SELECT pg_advisory_xact_lock(784236510)')
        return self

    def __exit__(self, *args):
        return self.connection.__exit__(*args)

    def execute(self, sql, parameters=()):
        return self.connection.execute(sql.replace('?', '%s'), parameters)

    def executemany(self, sql, parameters):
        with self.connection.cursor() as cursor:
            cursor.executemany(sql.replace('?', '%s'), parameters)


SCHEMA = '''
CREATE TABLE IF NOT EXISTS records(id TEXT PRIMARY KEY, kind TEXT NOT NULL, data TEXT NOT NULL, position BIGSERIAL UNIQUE);
CREATE INDEX IF NOT EXISTS records_kind ON records(kind);
CREATE TABLE IF NOT EXISTS history(seq BIGSERIAL PRIMARY KEY, record_id TEXT, at TEXT, actor TEXT, action TEXT, before_data TEXT, after_data TEXT);
CREATE TABLE IF NOT EXISTS requests(key TEXT PRIMARY KEY, fingerprint TEXT, result TEXT);
CREATE TABLE IF NOT EXISTS blobs(id TEXT PRIMARY KEY, content BYTEA NOT NULL);
CREATE TABLE IF NOT EXISTS counters(team_id TEXT PRIMARY KEY, value BIGINT);
CREATE TABLE IF NOT EXISTS trash_batches(id TEXT PRIMARY KEY, root_id TEXT NOT NULL, root_kind TEXT NOT NULL, deleted_at TEXT NOT NULL, detached TEXT NOT NULL, root_ids TEXT);
'''


class PostgresStore(Store):
    backend = 'postgresql'
    record_order = 'position'

    def __init__(self, url, seed=True):
        self.url = url
        secret = os.environ.get('DATABASE_PASSWORD_FILE')
        self.password = Path(secret).read_text().strip() if secret else None
        with self.connect() as db:
            for statement in SCHEMA.split(';'):
                if statement.strip():
                    db.execute(statement)
            if seed:
                self._migrate_archived_records(db)
                if not db.execute("SELECT 1 FROM records WHERE kind='teams'").fetchone():
                    self._create(db, 'teams', {'name':'Personal workspace', 'key':'LB'}, 'system')

    def connect(self):
        options = {'password': self.password} if self.password else {}
        return Connection(psycopg.connect(self.url, row_factory=row_factory, connect_timeout=10, **options))

    def _begin(self, db):
        # Connection context already owns a transaction and the application lock.
        pass

    def backup(self):
        parameters = conninfo_to_dict(self.url)
        password = self.password or parameters.pop('password', None)
        parameters.pop('password', None)
        env = dict(os.environ)
        if password:
            env['PGPASSWORD'] = password
        result = subprocess.run(['pg_dump', '--dbname', make_conninfo(**parameters), '--format=custom', '--no-owner', '--no-acl'],
                                env=env, capture_output=True, timeout=120)
        if result.returncode:
            raise RuntimeError('PostgreSQL backup failed')
        return 'linearboard.pgdump', result.stdout
