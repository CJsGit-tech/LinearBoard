"""Postgres transaction and SQLite migration checks in disposable schemas only."""
import base64
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import tempfile
import subprocess
import uuid
import psycopg
from psycopg.conninfo import make_conninfo, conninfo_to_dict
from linearboard.postgres import PostgresStore
from linearboard.store import Store, Conflict
from scripts.migrate_postgres import migrate, TABLES, digest

url = os.environ['DATABASE_URL']
secret = Path(os.environ['DATABASE_PASSWORD_FILE']).read_text().strip()
schema = 'qa_' + uuid.uuid4().hex
with psycopg.connect(url, password=secret, autocommit=True) as db:
    db.execute('CREATE SCHEMA '+schema)
try:
    target=PostgresStore(make_conninfo(url, options='-csearch_path='+schema), seed=False)
    with tempfile.TemporaryDirectory() as temp:
        source=Store(Path(temp)/'source.sqlite')
        team=source.snapshot()['teams'][0]
        project=source.mutate('projects',{'team_id':team['id'],'name':'Migration QA'})
        milestone=source.mutate('milestones',{'project_id':project['id'],'name':'M1'})
        issue=source.mutate('issues',{'project_id':project['id'],'title':'Preserve source','milestone_id':milestone['id']},key='original-create')
        other=source.mutate('issues',{'project_id':project['id'],'title':'Second','parent_id':issue['id']})
        source.mutate('relations',{'source_id':issue['id'],'target_id':other['id'],'relation':'blocks'})
        file=source.mutate('attachments',{'target_kind':'issues','target_id':issue['id'],'name':'proof.txt','content_base64':base64.b64encode(b'file bytes').decode()})
        preview=source.trash_impact('issues',other['id'])
        source.trash_move('issues',other['id'],preview['fingerprint'])
        migrate(source.path,target)
        migrate(source.path,target) # exact replay performs no writes
        assert source.snapshot(True)==target.snapshot(True)
        assert target.blob(file['id'])[1]==b'file bytes'
        assert target.history(issue['id'])==source.history(issue['id'])
        assert target.trash_list()==source.trash_list()
        target.trash_restore(target.trash_list()[0]['batch_id'])
        assert target.get('issues',other['id'])['parent_id']==issue['id']
        created=target.mutate('issues',{'project_id':project['id'],'title':'PostgreSQL native creation'})
        assert created['identifier'] not in [issue['identifier'],other['identifier']]
        view=target.mutate('views',{'project_id':project['id'],'name':'FE','category':'FrontEnd'})
        assert len(target.view_members(view['id']))==3
        def update(n):
            try:
                target.mutate('issues',{'expected_version':issue['version'],'title':'Concurrent '+str(n)},issue['id'])
                return 'success'
            except Conflict: return 'conflict'
        with ThreadPoolExecutor(2) as pool:
            assert sorted(pool.map(update,[1,2]))==['conflict','success']
        current=target.get('issues',issue['id'])
        payload={'issue_ids':[issue['id'],other['id']],'expected_versions':{issue['id']:current['version'],other['id']:1},'status':'Todo'}
        try: target.update_issue_statuses(payload)
        except Conflict: pass
        else: raise AssertionError('Stale batch accepted')
        assert target.get('issues',issue['id'])['status']=='Backlog'
        assert PostgresStore(target.url).snapshot()==target.snapshot()
        name,data=target.backup()
        assert name.endswith('.pgdump') and data.startswith(b'PGDMP')
        restore_name='qa_restore_'+uuid.uuid4().hex
        with psycopg.connect(url,password=secret,autocommit=True) as admin:
            admin.execute('CREATE DATABASE '+restore_name)
        parameters=conninfo_to_dict(url)
        parameters['dbname']=restore_name
        restore_url=make_conninfo(**parameters)
        try:
            restored=subprocess.run(['pg_restore','--dbname',restore_url,'--no-owner','--exit-on-error'],input=data,env={**os.environ,'PGPASSWORD':secret},capture_output=True)
            assert restored.returncode==0,restored.stderr.decode()
            recovered=PostgresStore(make_conninfo(restore_url,options='-csearch_path='+schema))
            assert recovered.snapshot()==target.snapshot()
            assert recovered.blob(file['id'])[1]==b'file bytes'
        finally:
            with psycopg.connect(url,password=secret,autocommit=True) as admin:
                admin.execute('DROP DATABASE '+restore_name)
        print('PASS: six-table migration checksums, safe repeat, stable IDs, blobs/history/trash, views, concurrent conflicts, batch rollback, reconnect persistence and pg_dump')
finally:
    with psycopg.connect(url,password=secret,autocommit=True) as db:
        db.execute('DROP SCHEMA '+schema+' CASCADE')
