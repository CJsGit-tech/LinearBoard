"""Standalone skill integration check; uses only a disposable database. Optional argv: skill folder."""
import base64,json,subprocess,tempfile,threading,sys,re
from pathlib import Path
from http.server import ThreadingHTTPServer
from server import Handler
from linearboard.store import Store
skill=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'skills/linearboard'
source=(skill/'SKILL.md').read_text()
section=source.split('## Commands\n')[1].split('Technology lookup')[0]
commands={match.split()[0] for match in re.findall(r'^- `([^`]+)`',section,re.M)}
assert '`create-issues-BE`' in section, 'Backend delivery command missing'
commands.add('create-issues-BE')
help_commands=[match.split()[0] for match in re.findall(r'^- `([^`]+)`',(skill/'references/help.md').read_text(),re.M)]
assert len(help_commands)==len(commands) and set(help_commands)==commands, 'Offline help and skill router disagree'
design_skill=skill.parent/'design-pro'
assert (design_skill/'SKILL.md').is_file(), 'Missing bundled design-pro sibling'
external_skill_links={'../../file-change-summary/SKILL.md'}
for file in [*skill.rglob('*.md'), *design_skill.rglob('*.md')]:
 for target in re.findall(r'\]\(([^)]+)\)',file.read_text()):
  if ':' in target or target.startswith(('#','{{')) or '<' in target or ' ' in target or target in external_skill_links: continue
  path=target.split('#')[0]
  if not path: continue
  resolved=(file.parent/path).resolve()
  if '.system/imagegen/' in str(resolved): continue
  assert resolved.exists(),(file,target)
with tempfile.TemporaryDirectory() as temp:
 server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
 server.store,server.verbose=Store(Path(temp)/'qa.sqlite'),False
 threading.Thread(target=server.serve_forever,daemon=True).start()
 url=f'http://127.0.0.1:{server.server_port}'
 def call(tool,args={},fail=False,all=False):
  result=subprocess.run([sys.executable,str(skill/'scripts/operate.py'),tool,'--url',url,'--no-autostart']+(['--all'] if all else []),input=json.dumps(args),text=True,capture_output=True,timeout=25)
  if fail:
   assert result.returncode!=0,result.stdout
   return
  assert result.returncode==0,result.stderr
  return json.loads(result.stdout)
 def create(kind,**data):
  return call('linearboard_create',{'kind':kind,'data':data,'idempotency_key':'qa-'+kind+'-'+str(data)})
 try:
  caps=call('linearboard_capabilities')
  assert [command['command'] for command in caps['commands']]==help_commands, 'Capability catalog and offline help disagree'
  team=call('linearboard_list',{'kind':'teams'},all=True)['items'][0]
  project=create('projects',name='Skill QA',team_id=team['id'])
  milestone=create('milestones',name='M1',project_id=project['id'])
  docs={t:create('documents',title=t,doc_type=t,project_id=project['id'],body='## Confirmed scope\n\n- [ ] Verify') for t in ['Vision','Milestones','QA','Design overview','Screen specification','FRD','Bugs']}
  labels=[create('labels',name=n,team_id=team['id']) for n in ['M1','US1','Coder']]
  issues={c:create('issues',title=c,project_id=project['id'],milestone_id=milestone['id'],category=c,label_ids=[r['id'] for r in labels],body='## User story\n\nScope\n\n## Acceptance\n\n- [ ] Works') for c in caps['resources']['issues']['fields']['category'].split(' | ')}
  for category,issue in issues.items():
   view=create('views',name=category,project_id=project['id'],category=category,placement='tabs',group_by='status')
   members=call('linearboard_get',{'kind':'views','id':view['id'],'members':True})
   assert issue['id'] in str(members)
  relation=create('relations',source_id=issues['ProductRequirement']['id'],target_id=issues['UserStory']['id'],relation='related')
  create('comments',target_kind='documents',target_id=docs['Bugs']['id'],body='Verified result with FIX reference')
  attachment=create('attachments',target_kind='issues',target_id=issues['Design']['id'],name='reference.txt',mime='text/plain',content_base64=base64.b64encode(b'proof').decode(),approval='draft')
  create('batches',project_id=project['id'],name='Checkpoint',issue_ids=[issues['FrontEnd']['id'],issues['BackEnd']['id']])
  dispatch=create('dispatches',project_id=project['id'],issue_ids=[issues['FrontEnd']['id']],plan='Reviewed plan',state='review')
  create('evidence',project_id=project['id'],issue_id=issues['FrontEnd']['id'],criterion='CLI writes readable records',environment='Disposable local service',result='Pass')
  issue=issues['FrontEnd']; payload={'kind':'issues','id':issue['id'],'data':{'expected_version':issue['version'],'body':'Verified revision'},'idempotency_key':'same-update'}
  a=call('linearboard_update',payload); assert call('linearboard_update',payload)==a
  call('linearboard_update',{**payload,'idempotency_key':'stale'},fail=True)
  call('linearboard_update',{'kind':'issues','id':issue['id'],'data':{'expected_version':a['version'],'status':'Done'},'idempotency_key':'done'},fail=True)
  call('linearboard_update',{'kind':'attachments','id':attachment['id'],'data':{'expected_version':1,'approval':'approved'},'idempotency_key':'approve'},fail=True)
  assert len(call('linearboard_get',{'kind':'issues','id':issue['id'],'history':True}))==2
  print('PASS: standalone LinearBoard command router, local reference links, CLI capability/pagination, every resource kind, View membership, history, retries, stale-write rejection, user-only Done/approval')
 finally: server.shutdown();server.server_close()
