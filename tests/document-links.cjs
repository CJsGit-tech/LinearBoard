// Document story links (#/documents/<id>#us-NN) against a disposable SQLite workspace.
const {chromium}=require('playwright');
const {spawn}=require('node:child_process');
const fs=require('node:fs/promises'),os=require('node:os'),path=require('node:path');
const assert=require('node:assert/strict');
(async()=>{
 const temp=await fs.mkdtemp(path.join(os.tmpdir(),'linearboard-links-'));
 const port=process.env.LINEARBOARD_LINKS_PORT||'8795', base='http://127.0.0.1:'+port;
 const shots=process.env.LINEARBOARD_LINKS_SHOTS;
 let service,browser; const errors=[],passed=[];
 const http=async(kind,data,method='POST')=>{const r=await fetch(base+'/api/'+kind,{method:data===undefined?'GET':method,headers:{'Content-Type':'application/json'},body:data===undefined?undefined:JSON.stringify(data)});const out=await r.json();if(!r.ok)throw Error(JSON.stringify(out));return out;};
 try{
  service=spawn('python3',['server.py','--port',port,'--db',path.join(temp,'qa.sqlite3')],{cwd:path.resolve(__dirname,'..')});
  await new Promise((resolve,reject)=>{service.stdout.once('data',resolve);service.once('error',reject);service.once('exit',code=>reject(Error('QA server exited '+code)));});
  const team=(await http('state')).teams[0]||await http('teams',{name:'QA'});
  const project=await http('projects',{name:'Links QA',team_id:team.id});
  // Long enough that every later story sits well below the editor's first screen, with one wrapped paragraph.
  const stories=Array.from({length:12},(_,i)=>{const n=String(i+1).padStart(2,'0');return `<a id="us-${n}"></a>\n### US-${n} — Story ${n}\n\n${(i===1?'A long wrapped paragraph. '.repeat(120)+'\n\n':'')}${Array.from({length:6},(_,j)=>`- Criterion ${n}.${j}`).join('\n')}\n`;}).join('\n');
  const doc=await http('documents',{project_id:project.id,title:'M1 Stories',doc_type:'Milestones',body:'## Overview\n\n**Milestone outcomes** and [project context]('+project.url+').\n\n| Outcome | Prerequisite |\n| --- | --- |\n| Booking | None |\n\n- [ ] Final review\n\n```html\n<a id="example-in-code"></a>\n```\n\n'+stories+'\n```json\n'+JSON.stringify({schema:'linearboard-story-index-v1',stories:Array.from({length:12},(_,i)=>({id:'US-'+String(i+1).padStart(2,'0'),milestone_id:'fixture-milestone',anchor:'us-'+String(i+1).padStart(2,'0')}))})+'\n```'});
  const plain=await http('documents',{project_id:project.id,title:'No anchors',doc_type:'Notes',body:'## Plain\n\nNo story anchors here.'});
  assert.equal(doc.url,'/#/documents/'+doc.id);
  const issue=await http('issues',{project_id:project.id,title:'PRD-1',category:'ProductRequirement',body:`[US-08](${doc.url}#us-08)`});
  browser=await chromium.launch({channel:'chrome',headless:true});
  const context=await browser.newContext({locale:'en-US',viewport:{width:1440,height:900}});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));page.setDefaultTimeout(10000);
  const body=page.locator('#document-form [name="body"]');
  // The rendered story heading must be below the sticky toolbar and in view.
  const assertOnStory=async(owner,anchor)=>{
   await owner.locator('.rich-text-content [data-story-anchor][id="'+anchor+'"]').waitFor({state:'attached'});
   const r=await owner.evaluate(a=>{
    const marker=[...document.querySelectorAll('.rich-text-content [data-story-anchor]')].find(x=>x.id===a);
    const target=marker.nextElementSibling||marker,d=document.getElementById('dialog');
    const box=target.getBoundingClientRect(),head=d.querySelector('.dialog-head').getBoundingClientRect();
    return {top:box.top,bottom:box.bottom,headBottom:head.bottom,viewport:innerHeight,scrollTop:d.scrollTop};
   },anchor);
   assert.ok(r.scrollTop>0,JSON.stringify(r));
   assert.ok(r.top>=r.headBottom-1&&r.bottom<r.viewport,JSON.stringify(r));
  };
  // Direct load of a fragment link.
  await page.goto(base+'/#/documents/'+doc.id+'#us-04');await page.locator('.rich-text-content').waitFor();
  assert.equal(await page.locator('#document-form [name="title"]').inputValue(),'M1 Stories');
  await assertOnStory(page,'us-04');
  assert.equal(new URL(page.url()).hash,'#/documents/'+doc.id+'#us-04');
  assert.equal(await page.locator('#toast.error').count(),0);
  if(shots)await page.screenshot({path:path.join(shots,'fragment-us-04.png')});
  passed.push('direct fragment URL opens the document on its story and keeps the URL');
  assert.equal(await page.locator('.rich-text-content [data-story-anchor]').count(),12);
  assert.equal(await page.locator('.rich-text-content table').count(),1);
  assert.equal(await page.locator('.rich-text-content strong').innerText(),'Milestone outcomes');
  assert.equal(await page.locator('.rich-text-content a[href="'+project.url+'"]').count(),1);
  assert.equal(await body.isVisible(),false);
  passed.push('milestone documents default to rich text with tables, headings, bold, links and 12 anchors; code examples remain code');
  // Anchor after the wrapped paragraph, and a further story in the same open document.
  await page.evaluate(id=>{location.hash='#/documents/'+id+'#us-11';},doc.id);
  await page.waitForFunction(()=>document.querySelector('#dialog')?.scrollTop>0&&location.hash.endsWith('#us-11'));await page.waitForTimeout(250);
  await assertOnStory(page,'us-11');passed.push('changing the fragment moves within the open document');
  // Unsaved edits survive following a story link in the same document.
  await page.locator('.rich-text-content').press('ControlOrMeta+End');await page.keyboard.press('Enter');await page.keyboard.insertText('Unsaved note');const edited=await body.inputValue();
  await page.evaluate(id=>{location.hash='#/documents/'+id+'#us-03';},doc.id);await page.waitForFunction(()=>location.hash.endsWith('#us-03'));await page.waitForTimeout(400);
  assert.equal(await body.inputValue(),edited);await assertOnStory(page,'us-03');passed.push('story link keeps unsaved edits in the open document');
  // Saving rich edits and toggling source mode must retain every anchor, URL and the structural JSON index.
  await page.getByRole('button',{name:'Save document',exact:true}).click();
  await page.waitForFunction(()=>/saved/i.test(document.querySelector('#toast')?.textContent||''));
  const saved=await http('documents/'+doc.id);
  for(let i=1;i<=12;i++)assert.ok(saved.body.includes('<a id="us-'+String(i).padStart(2,'0')+'"></a>'));
  assert.ok(saved.body.includes('Unsaved note'));assert.ok(saved.body.includes(project.url));
  const originalIndex=JSON.parse(doc.body.match(/```json\n([\s\S]*?)\n```/)[1]);
  assert.deepEqual(JSON.parse(saved.body.match(/```json\n([\s\S]*?)\n```/)[1]),originalIndex);
  assert.ok(saved.body.includes('<a id="example-in-code"></a>'));
  await page.goto(base+'/#/documents/'+doc.id+'#us-03');await page.reload();await page.locator('.rich-text-content').waitFor();
  assert.equal(await page.locator('.rich-text-content [data-story-anchor]').count(),12);
  assert.equal(await page.locator('.rich-text-content table').count(),1);await assertOnStory(page,'us-03');
  await page.locator('#document-form [data-action="preview"]').click();await body.waitFor();
  assert.ok((await body.inputValue()).includes('<a id="us-08"></a>'));
  await page.locator('#document-form [data-action="preview"]').click();await page.locator('.rich-text-content').waitFor();
  assert.equal(await page.locator('.rich-text-content [data-story-anchor]').count(),12);
  passed.push('rich editing, save/reload and Markdown toggling preserve story anchors, links, tables, code examples and the JSON story index');
  // A plain URL still opens at the top, with its rich-text body.
  const fresh=await context.newPage();fresh.on('pageerror',e=>errors.push(e.message));
  await fresh.goto(base+'/#/documents/'+doc.id);await fresh.locator('.rich-text-content').waitFor();
  assert.equal(await fresh.locator('#document-form [name="body"]').evaluate(f=>f.scrollTop),0);
  assert.equal(new URL(fresh.url()).hash,'#/documents/'+doc.id);
  await fresh.goto(base+'/#/documents/'+plain.id);await fresh.reload();await fresh.locator('#body-preview').waitFor();
  assert.ok((await fresh.locator('#body-preview').innerText()).includes('No story anchors'));
  assert.equal(await fresh.locator('#toast.error').count(),0);passed.push('plain document URLs are unchanged');
  // A missing anchor still opens the right document and says what was not found.
  await fresh.goto(base+'/#/documents/'+doc.id+'#us-99');await fresh.reload();await fresh.locator('.rich-text-content').waitFor();
  assert.equal(await fresh.locator('#document-form [name="title"]').inputValue(),'M1 Stories');
  await fresh.locator('#toast.error').filter({hasText:'section was not found'}).waitFor();passed.push('unknown fragment opens the document and reports it');
  // Regex characters in a fragment are text.
  await fresh.goto(base+'/#/documents/'+doc.id+'#(.*');await fresh.reload();await fresh.locator('.rich-text-content').waitFor();await fresh.locator('#toast.error').waitFor();passed.push('fragment is not interpreted as a pattern');
  // The link as a PRD writes it, clicked from an issue body; Back returns to the issue.
  const linked=await context.newPage();linked.on('pageerror',e=>errors.push(e.message));
  await linked.goto(base+'/#/issues/'+issue.id);await linked.locator('#body-preview a',{hasText:'US-08'}).click();
  await linked.locator('.rich-text-content').waitFor();await linked.waitForTimeout(250);
  await assertOnStory(linked,'us-08');assert.equal(new URL(linked.url()).hash,'#/documents/'+doc.id+'#us-08');
  if(shots)await linked.screenshot({path:path.join(shots,'issue-link-us-08.png')});
  await linked.keyboard.press('Alt+ArrowLeft');await linked.locator('#issue-form').waitFor();assert.equal(new URL(linked.url()).hash,'#/issues/'+issue.id);passed.push('PRD link opens the story; back returns to the PRD');
  // Other routes tolerate a fragment and keep working.
  const routes=await context.newPage();routes.on('pageerror',e=>errors.push(e.message));
  await routes.goto(base+'/#/issues/'+issue.id+'#us-01');await routes.locator('#issue-form').waitFor();
  await routes.goto(base+'/#/documents');await routes.reload();await routes.locator('[data-action="open-document"][data-id="'+doc.id+'"]').first().waitFor();assert.equal(await routes.locator('#document-form').count(),0);
  await routes.locator('[data-action="open-document"][data-id="'+doc.id+'"]').first().click();await routes.locator('#document-form').waitFor();assert.equal(new URL(routes.url()).hash,'#/documents/'+doc.id);
  await routes.locator('dialog [data-action="close"]').click();assert.equal(new URL(routes.url()).hash,'#/documents');passed.push('issue, list and in-app document routes are unchanged');
  // Narrow screens land on the story too.
  const narrow=await browser.newContext({locale:'en-US',viewport:{width:390,height:844}});const mobile=await narrow.newPage();mobile.on('pageerror',e=>errors.push(e.message));
  await mobile.goto(base+'/#/documents/'+doc.id+'#us-06');await mobile.locator('.rich-text-content').waitFor();await mobile.waitForTimeout(250);await assertOnStory(mobile,'us-06');
  if(shots)await mobile.screenshot({path:path.join(shots,'fragment-mobile-us-06.png')});
  await narrow.close();passed.push('fragment link works at 390px');
  assert.deepEqual(errors,[]);console.log(JSON.stringify({passed,errors}));
 }catch(e){console.error('QA FAILED',e);console.error('Completed checkpoints',passed);process.exitCode=1;}
 finally{await browser?.close();service?.removeAllListeners('exit');service?.kill('SIGTERM');await fs.rm(temp,{recursive:true,force:true});}
})();
