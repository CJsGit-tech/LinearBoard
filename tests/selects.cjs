// Disposable picker checks: real pointer/keyboard input, forms and popup geometry.
const { chromium } = require('playwright');
const { spawn } = require('node:child_process');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const assert = require('node:assert/strict');
const { openSelect, selectValue, selectProject } = require('./controls.cjs');

(async () => {
  const temp = await fs.mkdtemp(path.join(os.tmpdir(), 'linearboard-selects-'));
  const base = 'http://127.0.0.1:' + (process.env.LINEARBOARD_QA_PORT || '8780');
  let service, browser;
  const passed = [], errors = [];
  const http = async (kind, data) => {
    const response = await fetch(base + '/api/' + kind, {
      method: data === undefined ? 'GET' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: data === undefined ? undefined : JSON.stringify(data),
    });
    const result = await response.json();
    assert.ok(response.ok, JSON.stringify(result));
    return result;
  };
  try {
    service = spawn('python3', ['server.py', '--port', base.split(':').pop(), '--db', path.join(temp, 'qa.sqlite3')], { cwd: path.resolve(__dirname, '..') });
    await new Promise((resolve, reject) => { service.stdout.once('data', resolve); service.once('error', reject); service.once('exit', code => reject(Error('QA server exit ' + code))); });
    const team = (await http('state')).teams[0];
    const project = await http('projects', { team_id: team.id, name: 'Dropdown QA' });
    const longProject = await http('projects', { team_id: team.id, name: '長名稱專案—'.repeat(16) });
    const milestone = await http('milestones', { project_id: project.id, name: 'M1 — 下拉選單驗證' });
    const rowLabels = await Promise.all(['M1', 'US1', '自訂標籤', 'Coder', '待確認', '長標籤'.repeat(30)].map(name => http('labels', {team_id:team.id, name})));
    const document = await http('documents', { project_id: project.id, title: 'Dropdown document', doc_type: 'Notes' });
    const originalBody = '## 原始內容\n\n**保留粗體**及*斜體*。[來源文件](#/documents/' + document.id + ')\n\n- [ ] 核對附件\n  - [x] 子項目\n\n| 欄位 | 內容 |\n| --- | --- |\n| 契約 | 保留 |\n\n```js\nconst total = 1;\n```\n';
    const issue = await http('issues', { project_id: project.id, title: 'Dropdown task', category: 'FrontEnd', status: 'Todo', milestone_id: milestone.id, label_ids:rowLabels.map(label=>label.id), body: originalBody });
    for (let n = 0; n < 18; n++) await http('issues', { project_id: project.id, title: '長名稱任務 '.repeat(12) + n, category: 'BackEnd', status: 'Backlog' });
    const attachment = await http('attachments', { target_kind: 'issues', target_id: issue.id, name: '參考連結', external_url: 'https://example.invalid/reference', approval: 'draft' });
    browser = await chromium.launch({ channel: 'chrome', headless: true });
    const page = await browser.newPage({locale:"zh-TW", viewport: { width: 1440, height: 960 } });
    page.on('pageerror', error => errors.push(error.message));
    page.setDefaultTimeout(10000);
    await page.goto(base);
    const projectList = page.getByRole('navigation', {name:'專案清單'});
    assert.deepEqual(await projectList.locator('[data-project-id]').evaluateAll(items => items.map(item=>item.dataset.projectId)), [project.id, longProject.id]);
    assert.equal(await page.getByRole('combobox', {name:'目前專案',exact:true}).count(), 0);
    await selectProject(page, longProject.id);
    await selectProject(page, project.id);
    await page.setViewportSize({width:390,height:844});
    await page.getByRole('button',{name:'開啟導覽',exact:true}).click();
    await selectProject(page,longProject.id);
    assert.equal(await page.getByRole('button',{name:'開啟導覽',exact:true}).getAttribute('aria-expanded'),'false');
    await page.getByRole('button',{name:'開啟導覽',exact:true}).click();
    await selectProject(page,project.id);
    await page.setViewportSize({width:1440,height:960});
    const labeledRow = page.locator('.issue-row[data-id="'+issue.id+'"]');
    await labeledRow.locator('.milestone-tag').waitFor({state:'visible'});
    assert.equal((await labeledRow.locator('.milestone-tag').innerText()).trim(), 'M1');
    assert.deepEqual(await labeledRow.locator('.custom-label').allTextContents(), ['US1', '自訂標籤', 'Coder']);
    assert.equal(await labeledRow.locator('.milestone-tag').getAttribute('title'), milestone.name);
    const entry = labeledRow.locator('..');
    const expandLabels = entry.getByRole('button', {name:'展開 '+issue.identifier+' 標籤', exact:true});
    assert.equal(await expandLabels.innerText(), '+2');
    await expandLabels.click();
    const allLabels = entry.getByRole('group', {name:issue.identifier+' 所有標籤', exact:true});
    assert.deepEqual(await allLabels.locator('.badge').allTextContents(), rowLabels.slice(1).map(label=>label.name));
    assert.equal(await page.locator('dialog[open]').count(), 0);
    await page.setViewportSize({width:390,height:844});
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth));
    await entry.getByRole('button', {name:'收合 '+issue.identifier+' 標籤',exact:true}).click();
    assert.equal(await allLabels.count(), 0);
    await page.setViewportSize({width:1440,height:960});
    await page.getByRole('button', { name: '篩選任務', exact: true }).click();
    await selectValue(page.locator('#filter-status'), 'In Progress');
    assert.equal(await page.locator('.issue-row').count(), 0);
    await selectValue(page.locator('#filter-status'), '');
    assert.equal(await page.locator('.issue-row').count(), 19);
    passed.push('Project list switching and empty filter recovery; property filters retain dark pickers');

    await page.goto(base + '/#/issues/' + issue.id);
    await page.getByRole('textbox', { name: '任務標題' }).fill('未儲存的草稿');
    await page.getByRole('button', { name: '返回', exact: true }).click();
    await page.locator('.issue-row[data-id="' + issue.id + '"]').click();
    assert.equal(await page.getByRole('textbox', { name: '任務標題' }).inputValue(), '未儲存的草稿');
    assert.equal((await http('issues/' + issue.id)).title, 'Dropdown task');
    await page.reload();
    passed.push('Back returns to the workspace and preserves unsaved edits when reopening');
    const status = page.getByRole('combobox', { name: '狀態', exact: true });
    await status.waitFor();
    const { popup: statusPopup } = await openSelect(status);
    await page.keyboard.press('Home');
    await page.waitForFunction(() => document.activeElement?.dataset.value === 'Backlog');
    await page.keyboard.press('ArrowDown');
    await page.waitForFunction(() => document.activeElement?.dataset.value === 'Todo');
    await page.keyboard.press('ArrowDown');
    await page.waitForFunction(() => document.activeElement?.dataset.value === 'In Progress');
    const highlighted = await statusPopup.locator('[data-highlighted]').evaluate(el => ({
      text: el.textContent, color: getComputedStyle(el).color, bg: getComputedStyle(el).backgroundColor,
    }));
    assert.equal(highlighted.text, 'In Progress');
    assert.equal(highlighted.color, 'rgb(233, 226, 212)');
    assert.equal(highlighted.bg, 'rgb(53, 49, 43)');
    await page.keyboard.press('Enter');
    await selectValue(page.getByRole('combobox', { name: '里程碑', exact: true }), '');
    const submitted = await page.locator('#issue-form').evaluate(form => Object.fromEntries(new FormData(form)));
    assert.equal(submitted.status, 'In Progress');
    assert.equal(submitted.milestone_id, '');
    await page.locator('button[form="issue-form"]').click();
    await page.waitForFunction(() => document.querySelector('#toast')?.textContent.includes('已儲存變更'));
    assert.equal((await http('issues/' + issue.id)).status, 'In Progress');
    assert.equal((await http('issues/' + issue.id)).milestone_id, '');
    assert.equal((await http('issues/' + issue.id)).body, originalBody);
    await openSelect(page.getByRole('combobox', { name: '狀態', exact: true }));
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('dialog[open]').count(), 1);
    passed.push('Keyboard highlight stays readable; native-dialog popup, blank milestone and FormData persist original values');

    const approval = page.locator('[data-approval]');
    const reject = route => route.fulfill({ status: 503, contentType: 'application/json', body: JSON.stringify({ error: 'QA 儲存失敗' }) });
    await page.route(base + '/api/attachments/' + attachment.id, reject);
    await selectValue(approval, 'evidence');
    await page.getByRole('status').filter({ hasText: 'QA 儲存失敗' }).waitFor();
    assert.equal(await approval.getAttribute('data-value'), 'draft');
    await page.unroute(base + '/api/attachments/' + attachment.id, reject);
    await selectValue(approval, 'evidence');
    await page.waitForFunction(() => document.querySelector('[data-approval]')?.dataset.value === 'evidence');
    assert.equal((await http('attachments/' + attachment.id)).approval, 'evidence');
    passed.push('Attachment picker preserves the saved value on failure and allows retry');

    const rich = page.getByRole('textbox', { name: '任務內容', exact: true });
    assert.equal(await rich.getAttribute('contenteditable'), 'true');
    assert.equal(await rich.locator('table').count(), 1);
    assert.equal(await rich.locator('pre code').innerText(), 'const total = 1;');
    assert.equal(await rich.locator('input[type="checkbox"]').count(), 2);
    await rich.press('ControlOrMeta+End');
    await rich.press('Enter');
    await page.getByRole('button', { name: '粗體', exact: true }).click();
    await page.keyboard.type('新增粗體');
    await page.getByRole('button', { name: '粗體', exact: true }).click();
    await rich.locator('input[type="checkbox"]').first().check();
    assert.equal((await http('issues/' + issue.id)).body, originalBody, 'Rich text waits for explicit save');
    await page.getByRole('button', { name: '連結', exact: true }).click();
    await page.getByRole('textbox', { name: '連結網址', exact: true }).fill('javascript:alert(1)');
    await page.getByRole('button', { name: '套用', exact: true }).click();
    await page.getByRole('alert').filter({ hasText: '請輸入有效的網址或紀錄連結。' }).waitFor();
    await page.locator('.rich-link-editor').getByRole('button', { name: '取消', exact: true }).click();
    const draftBody = await page.locator('#issue-form [name="body"]').inputValue();
    assert.ok(draftBody.includes('**新增粗體**'), draftBody);
    assert.ok(draftBody.includes('[x] 核對附件'), draftBody);
    assert.ok(draftBody.includes('| 契約'), draftBody);
    await rich.getByRole('link', { name: '來源文件', exact: true }).click();
    await page.locator('#document-form').waitFor();
    await page.getByRole('button', { name: '返回', exact: true }).click();
    await rich.waitFor();
    assert.equal(await page.locator('#issue-form [name="body"]').inputValue(), draftBody);
    await page.locator('button[form="issue-form"]').click();
    await page.waitForFunction(() => document.querySelector('#toast')?.textContent.includes('已儲存變更'));
    assert.equal((await http('issues/' + issue.id)).body, draftBody);
    await rich.press('ControlOrMeta+End');
    await page.keyboard.type('可復原文字');
    await page.getByRole('button', { name: '復原', exact: true }).click();
    assert.ok(!(await rich.innerText()).includes('可復原文字'));
    await page.getByRole('button', { name: '重做', exact: true }).click();
    assert.ok((await rich.innerText()).includes('可復原文字'));
    await page.getByRole('button', { name: '復原', exact: true }).click();
    await page.reload();
    await rich.waitFor();
    assert.ok((await rich.innerText()).includes('新增粗體'));
    assert.equal(await rich.locator('input[type="checkbox"]').first().isChecked(), true);
    assert.equal(await rich.locator('table').count(), 1);
    assert.equal((await http('history/' + issue.id)).length, 3);
    passed.push('Rich text preserves untouched Markdown, formats text and tasks, rejects unsafe links, keeps navigation drafts, supports undo/redo and persists after reload');

    await page.locator('.supplemental-properties summary').click();
    for (const width of [1440, 900, 390]) {
      await page.setViewportSize({ width, height: 844 });
      const parent = page.getByRole('combobox', { name: '上層任務', exact: true });
      const { popup } = await openSelect(parent);
      const box = await popup.boundingBox();
      assert.ok(box.x >= 0 && box.x + box.width <= width, JSON.stringify(box));
      assert.ok(box.y >= 0 && box.y + box.height <= 844, JSON.stringify(box));
      assert.ok(await popup.evaluate(el => el.scrollWidth <= el.clientWidth));
      await page.keyboard.press('End');
      assert.ok(await popup.locator('[data-highlighted]').isVisible());
      await page.screenshot({ path: '/tmp/linearboard-dark-options-' + width + '.png', fullPage: false });
      await page.keyboard.press('Escape');
      assert.ok(await page.locator('dialog').evaluate(el => el.scrollWidth <= el.clientWidth));
    }
    passed.push('Long option names and scrolling remain within 1440/900/390px popups without horizontal overflow');

    await page.setViewportSize({ width: 1440, height: 960 });
    await page.goto(base + '/#/documents/' + document.id);
    await page.getByRole('combobox', { name: '文件類型', exact: true }).waitFor();
    await selectValue(page.getByRole('combobox', { name: '文件類型', exact: true }), 'QA');
    await page.locator('button[form="document-form"]').click();
    await page.waitForFunction(() => document.querySelector('#toast')?.textContent.includes('文件已儲存'));
    assert.equal((await http('documents/' + document.id)).doc_type, 'QA');
    const htmlBody = '<!-- canonical comment -->\n<details><summary>決策</summary>保留原文</details>';
    const htmlDoc = await http('documents', { project_id: project.id, title: 'HTML source', doc_type: 'Notes', body: htmlBody });
    await page.goto(base + '/#/documents/' + htmlDoc.id);
    await page.getByRole('textbox', { name: '文件 Markdown', exact: true }).waitFor();
    assert.equal(await page.locator('#document-form [name="body"]').inputValue(), htmlBody);
    await page.locator('#document-form [name="title"]').fill('HTML source retained');
    await page.locator('button[form="document-form"]').click();
    await page.waitForFunction(() => document.querySelector('#toast')?.textContent.includes('文件已儲存'));
    assert.equal((await http('documents/' + htmlDoc.id)).body, htmlBody);
    passed.push('Source-only HTML and comments remain byte-for-byte intact when other fields are saved');
    await page.getByRole('button', { name: '關閉文件', exact: true }).click();
    await page.locator('dialog').waitFor({ state: 'hidden' });
    await page.getByRole('button', { name: '文件', exact: true }).click();
    await page.locator('[data-action="new-document"]').first().click();
    await page.getByRole('textbox', { name: '文件標題' }).fill('尚未建立的文件草稿');
    await page.getByRole('button', { name: '返回', exact: true }).click();
    await page.locator('[data-action="new-document"]').first().click();
    assert.equal(await page.getByRole('textbox', { name: '文件標題' }).inputValue(), '尚未建立的文件草稿');
    passed.push('Back preserves a new document draft before its first save');
    assert.deepEqual(errors, []);
    passed.push('Document type picker saves without changing technical values; no browser errors');
    console.log(JSON.stringify({ passed, consoleErrors: errors }, null, 2));
  } catch (error) {
    console.error('SELECT QA FAILED', error, '\nCompleted checkpoints', passed);
    process.exitCode = 1;
  } finally {
    if (browser) await browser.close();
    if (service && service.exitCode === null) { service.kill('SIGTERM'); await new Promise(resolve => service.once('exit', resolve)); }
    await fs.rm(temp, { recursive: true, force: true });
  }
})();
