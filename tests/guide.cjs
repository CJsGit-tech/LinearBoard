// Guide interaction, strict CSP and both offline export paths; disposable app only.
const {chromium}=require('playwright');
const {spawn}=require('node:child_process');
const fs=require('node:fs/promises'),os=require('node:os'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const assert=require('node:assert/strict');
const expectedCommands=15;
(async()=>{
 const temp=await fs.mkdtemp(path.join(os.tmpdir(),'linearboard-guide-'));
 const base='http://127.0.0.1:'+(process.env.LINEARBOARD_GUIDE_PORT||'8795');
 let service,browser;
 try {
  service=spawn('python3',['server.py','--port',new URL(base).port,'--db',path.join(temp,'qa.sqlite3')],{cwd:path.resolve(__dirname,'..')});
  await new Promise((resolve,reject)=>{service.stdout.once('data',resolve);service.once('error',reject);service.once('exit',code=>reject(Error('Guide server exit '+code)));});
  browser=await chromium.launch({channel:'chrome',headless:true});
  const context=await browser.newContext({locale:'zh-TW',acceptDownloads:true,permissions:['clipboard-read','clipboard-write']});
  const page=await context.newPage(),errors=[];
  const watch=page=>{page.on('pageerror',error=>errors.push(error.message));page.on('console',msg=>{if(msg.type()==='error'&&/Content Security Policy|Refused to execute/i.test(msg.text()))errors.push(msg.text());});};watch(page);
  await page.goto(base+'/guide');await page.locator('#catalog tr').last().waitFor({state:'attached'});
  const commands=await page.locator('#command-data').textContent().then(JSON.parse);
  assert.equal(commands.length,expectedCommands);assert.equal(await page.locator('#action option').count(),expectedCommands);
  assert.equal(await page.locator('#catalog tr').count(),expectedCommands);assert.equal(await page.locator('article.command').count(),expectedCommands);
  assert.equal(await page.locator('#result-count').innerText(),`${expectedCommands} / ${expectedCommands} 個指令`);
  assert.equal(await page.locator('#action option[value="frd"],#action option[value="create-userstories"],#action option[value="prd-demystify"]').count(),0);
  await page.locator('#project').fill('Guide QA');await page.locator('#milestone').fill('M2');
  for(const command of commands){
   await page.locator('#action').selectOption(command.name);
   const prompt=await page.locator('#built').innerText();assert.ok(prompt.startsWith('$linearboard '+command.name),prompt);
   const anchor=await page.locator('#catalog a').filter({hasText:command.name}).first().getAttribute('href');assert.equal(await page.locator(anchor).count(),1);
  }
  await page.locator('#action').selectOption('help');assert.equal(await page.locator('#built').innerText(),'$linearboard help');
  await page.locator('#action').selectOption('init');await page.locator('#repo').fill('/tmp/guide-project');
  assert.equal(await page.locator('#built').innerText(),'$linearboard init Guide QA /tmp/guide-project');
  await page.locator('#action').selectOption('create-technical-baseline');
  assert.equal(await page.locator('#built').innerText(),'$linearboard create-technical-baseline Guide QA');
  await page.locator('#action').selectOption('dispatch');assert.ok((await page.locator('#built').innerText()).includes('〈issue IDs〉'));
  await page.locator('#dispatchscope').selectOption('batch');await page.locator('#batch').fill('0');assert.ok((await page.locator('#built').innerText()).includes('〈批次編號〉'));
  await page.locator('#batch').fill('2');assert.equal(await page.locator('#built').innerText(),'$linearboard dispatch Guide QA M2 Batch 2');
  await page.locator('#search').fill('no-such-command');await page.locator('#search-empty').waitFor({state:'visible'});
  await page.locator('#clear-search').click();assert.equal(await page.locator('#catalog tr:visible').count(),expectedCommands);
  await page.locator('[data-stage="設計"]').click();assert.equal(await page.locator('#catalog tr:visible').count(),2);await page.locator('#clear-search').click();
  await page.locator('[data-command="help"]').first().click();assert.equal(await page.locator('#built').innerText(),'$linearboard help');
  await page.locator('[data-copy="#built"]').click();assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),'$linearboard help');
  await page.locator('[data-progress="start"]').check();await page.reload();await page.locator('#catalog tr').last().waitFor({state:'attached'});assert.equal(await page.locator('[data-progress="start"]').isChecked(),true);
  await page.locator('#action').selectOption('dispatch');await page.locator('#project').fill('Offline QA');await page.locator('#dispatchscope').selectOption('batch');await page.locator('#batch').fill('3');
  const offlinePreview=await page.locator('#built').innerText();
  await page.locator('[data-stage="設計"]').click();
  const downloadPromise=page.waitForEvent('download');await page.locator('a[download]').click();const download=await downloadPromise;
  const file=path.join(temp,download.suggestedFilename());await download.saveAs(file);
  const offline=await context.newPage();watch(offline);await offline.goto(pathToFileURL(file).href);await offline.locator('#catalog tr').last().waitFor({state:'attached'});
  assert.equal(await offline.locator('#catalog tr').count(),expectedCommands);assert.equal(await offline.locator('article.command').count(),expectedCommands);
  assert.equal(await offline.locator('#catalog tr:visible').count(),2);await offline.locator('#clear-search').click();
  assert.equal(await offline.locator('#built').innerText(),offlinePreview);assert.equal(await offline.locator('[data-progress="start"]').isChecked(),true);
  await offline.locator('#action').selectOption('help');assert.equal(await offline.locator('#built').innerText(),'$linearboard help');
  await offline.locator('#search').fill('create-designs');
  assert.equal(await offline.locator('#catalog a[href="#cmd-create-designs"]:visible').count(),1);
  assert.equal(await offline.locator('#catalog a[href="#cmd-debug"]:visible').count(),0);
  await offline.locator('#clear-search').click();
  // Exporting an already-exported guide must not duplicate generated options or cards.
  const secondDownloadPromise=offline.waitForEvent('download');await offline.locator('a[download]').click();const second=await secondDownloadPromise;const secondFile=path.join(temp,'second.html');await second.saveAs(secondFile);
  const reopened=await context.newPage();watch(reopened);await reopened.goto(pathToFileURL(secondFile).href);await reopened.locator('#catalog tr').last().waitFor({state:'attached'});assert.equal(await reopened.locator('article.command').count(),expectedCommands);
  const serverDownload=await context.request.get(base+'/guide/download');assert.equal(serverDownload.status(),200);const serverFile=path.join(temp,'server.html');await fs.writeFile(serverFile,await serverDownload.body());
  const serverOffline=await context.newPage();watch(serverOffline);await serverOffline.goto(pathToFileURL(serverFile).href);await serverOffline.locator('#catalog tr').last().waitFor({state:'attached'});await serverOffline.locator('#action').selectOption('help');assert.equal(await serverOffline.locator('#built').innerText(),'$linearboard help');
  await page.locator('#reset').click();assert.equal(await page.locator('[data-progress="start"]').isChecked(),false);
  await page.setViewportSize({width:390,height:844});await page.locator('#menu-toggle').click();assert.equal(await page.locator('#menu-toggle').getAttribute('aria-expanded'),'true');await page.locator('#guide-nav a[href="#builder"]').click();assert.equal(await page.locator('#menu-toggle').getAttribute('aria-expanded'),'false');
  for(const locale of ['en','zh-Hant']){
   const handsOn=await context.newPage();watch(handsOn);
   await handsOn.setViewportSize({width:390,height:844});
   const file=path.resolve(__dirname,'../docs/linearboard-guides',`hands-on.${locale}.html`);
   await handsOn.goto(pathToFileURL(file).href);
   assert.deepEqual(await handsOn.locator('#action option').evaluateAll(options=>options.map(o=>o.value)),commands.map(c=>c.name));
   await handsOn.locator('#search').fill('no-such-command');
   assert.equal(await handsOn.locator('[data-command-row]:visible').count(),0);
   await handsOn.locator('#search').fill('create-technical-baseline');
   await handsOn.locator('[data-command-row]:visible button').click();
   await handsOn.locator('#project').fill('Guide QA');
   assert.equal(await handsOn.locator('#built').innerText(),'$linearboard create-technical-baseline Guide QA');
   await handsOn.locator('#guide-menu-toggle').click();
   await handsOn.locator('#guide-nav a[href="#practice"]').click();
   assert.equal(await handsOn.locator('#guide-menu-toggle').getAttribute('aria-expanded'),'false');
   const mark=handsOn.locator('[data-progress="create-technical-baseline"]');
   await mark.check();await handsOn.reload();assert.equal(await mark.isChecked(),true);
   assert.ok(await handsOn.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   await handsOn.evaluate(()=>Object.defineProperty(navigator,'clipboard',{value:undefined}));
   await handsOn.locator('#builder .copy').click();
   assert.equal(await handsOn.evaluate(()=>getSelection().toString()),await handsOn.locator('#built').textContent());
   await handsOn.locator('#guide-menu-toggle').click();
   await handsOn.locator('#guide-nav a[href="#examples"]').click();
   const dispatchExample=handsOn.locator('#examples .codebox').filter({hasText:'$linearboard dispatch'});
   await dispatchExample.locator('.copy').click();
   assert.equal(await handsOn.evaluate(()=>getSelection().toString()),await dispatchExample.locator('code').textContent());
   assert.ok((await dispatchExample.locator('code').textContent()).includes('"M1 — Save a place" Batch 1'));
   await handsOn.close();
  }
  assert.deepEqual(errors,[]);
  console.log(`PASS: ${expectedCommands} commands, composers, search, clipboard and fallback, progress, mobile navigation, bilingual standalone guides, offline exports, and strict CSP`);
 } finally {if(browser)await browser.close();if(service&&service.exitCode===null&&!service.killed){const stopped=new Promise(r=>service.once('exit',r));service.kill();await stopped;}await fs.rm(temp,{recursive:true,force:true});}
})().catch(error=>{console.error(error);process.exitCode=1;});
