function initializeLinearBoardGuide() {
  'use strict';

  const commands = JSON.parse(document.getElementById('command-data').textContent);
  const $ = id => document.getElementById(id);
  const escapeHTML = value => String(value).replace(/[&<>"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[char]));
  const toast = message => {
    $('toast').textContent = message;
    clearTimeout(window.linearboardToast);
    window.linearboardToast = setTimeout(() => $('toast').textContent = '', 1800);
  };

  const phaseSection = phase => {
    if (phase === '起步') return 'start';
    if (phase === '規劃') return 'planning';
    if (phase === '需求') return 'requirements';
    if (phase === '設計') return 'design';
    if (phase === '維護') return 'maintenance';
    return 'delivery';
  };

  const action = $('action');
  const selectedAction = action.value || 'create-issues-FE';
  action.replaceChildren();
  $('catalog').replaceChildren();
  document.querySelectorAll('[id^="commands-"]').forEach(container => container.replaceChildren());
  commands.forEach(command => {
    const option = document.createElement('option');
    option.value = command.name;
    option.textContent = `${command.name} · ${command.title}`;
    if (command.name === selectedAction) option.selected = true;
    action.append(option);

    const row = document.createElement('tr');
    row.dataset.phase = command.phase;
    row.dataset.search = Object.values(command).join(' ').toLowerCase();
    row.innerHTML = `<td><a href="#cmd-${escapeHTML(command.name)}"><code>${escapeHTML(command.name)}</code></a></td><td>${escapeHTML(command.title)}</td><td>${escapeHTML(command.effect)}</td><td>${escapeHTML(command.view)}</td><td><button type="button" class="use-command" data-command="${escapeHTML(command.name)}">組合 ↗</button></td>`;
    $('catalog').append(row);

    const card = document.createElement('article');
    card.className = 'command';
    card.id = `cmd-${command.name}`;
    card.innerHTML = `
      <div class="command-top"><div><span class="eyebrow">${escapeHTML(command.phase)}</span><h3>${escapeHTML(command.name)}</h3><p class="subtitle">${escapeHTML(command.title)}</p></div><span class="badge">${escapeHTML(command.effect)}</span></div>
      <p>${escapeHTML(command.when)}</p>
      <div class="codebox"><div class="code-toolbar"><span>CODEX PROMPT</span><button class="copy" type="button" data-copy="#example-${escapeHTML(command.name)}">複製</button></div><pre><code id="example-${escapeHTML(command.name)}">${escapeHTML(command.example)}</code></pre></div>
      <dl><div><dt>先準備</dt><dd>${escapeHTML(command.input)}</dd></div><div><dt>會得到</dt><dd>${escapeHTML(command.output)}</dd></div><div><dt>怎麼確認</dt><dd>${escapeHTML(command.check)}</dd></div></dl>
      <p class="boundary"><strong>邊界：</strong>${escapeHTML(command.limit)}</p>
      <button type="button" class="compose-command" data-command="${escapeHTML(command.name)}">用這個指令組合範圍 ↗</button>`;
    const target = command.name === 'organize-task-batch' ? $('commands-delivery') : command.name === 'dispatch' ? $('commands-execution') : $(`commands-${phaseSection(command.phase)}`);
    target.append(card);
  });

  function build() {
    const command = commands.find(item => item.name === action.value);
    const project = $('project').value.trim() || '〈Project〉';
    const milestone = $('milestone').value.trim() || '〈Milestone〉';
    const scope = $('dispatchscope').value;
    const ids = $('issueids').value.trim();
    const batch = $('batch').value.trim();
    const validBatch = /^[1-9]\d*$/.test(batch);
    $('dispatch-scope-field').hidden = command.name !== 'dispatch';
    $('batch-field').hidden = command.name !== 'dispatch' || scope !== 'batch';
    $('issue-field').hidden = !(command.name === 'organize-task-batch' || (command.name === 'dispatch' && scope === 'issues'));
    $('issue-label').textContent = command.name === 'organize-task-batch' ? 'Issue IDs（選填）' : 'Issue IDs（必填）';
    $('debug-field').hidden = command.name !== 'debug';

    let args = command.name === 'help' ? '' : ` ${project}`;
    if (!['help', 'planning', 'create-vision-document', 'create-milestones'].includes(command.name)) args += ` ${milestone}`;
    if (command.name === 'organize-task-batch' && ids) args += ` ${ids}`;
    if (command.name === 'dispatch' && scope === 'batch') args += ` Batch ${validBatch ? batch : '〈批次編號〉'}`;
    if (command.name === 'dispatch' && scope === 'issues') args += ` ${ids || '〈issue IDs〉'}`;
    if (command.name === 'debug') args += ` ${$('debugsource').value.trim() || '〈Bugs 文件或 issue IDs〉'}`;
    let prompt = `$linearboard ${command.name}${args}`;
    const extra = $('additional').value.trim();
    if (extra) prompt += `\n${extra}`;
    $('built').textContent = prompt;
    $('builder-help').textContent = `${command.effect} · ${command.when} ${command.limit}`;
  }

  ['action','project','milestone','dispatchscope','batch','issueids','debugsource','additional'].forEach(id => $(id).addEventListener('input', build));
  build();

  document.addEventListener('click', async event => {
    const copy = event.target.closest('[data-copy]');
    if (copy) {
      const text = document.querySelector(copy.dataset.copy)?.textContent || '';
      try { await navigator.clipboard.writeText(text); toast('已複製指令。'); }
      catch { toast('瀏覽器未允許剪貼簿，請手動選取。'); }
    }
    const commandButton = event.target.closest('[data-command]');
    if (commandButton) {
      action.value = commandButton.dataset.command;
      build();
      location.hash = 'builder';
      action.focus({preventScroll: true});
    }
  });

  let activeStage = document.querySelector('[data-stage][aria-pressed="true"]')?.dataset.stage || '';
  function filterCommands() {
    const query = $('search').value.trim().toLowerCase();
    let count = 0;
    [...$('catalog').rows].forEach(row => {
      const phase = row.dataset.phase;
      const stageMatch = !activeStage || (activeStage === '交付' ? ['交付'].includes(phase) : phase === activeStage);
      const visible = stageMatch && row.dataset.search.includes(query);
      row.hidden = !visible;
      if (visible) count += 1;
    });
    $('result-count').textContent = `${count} / ${commands.length} 個指令`;
    $('search-empty').hidden = count !== 0;
  }
  $('search').addEventListener('input', filterCommands);
  $('clear-search').addEventListener('click', () => {
    $('search').value = '';
    activeStage = '';
    document.querySelectorAll('[data-stage]').forEach(item => item.setAttribute('aria-pressed', String(item.dataset.stage === '')));
    filterCommands();
    $('search').focus();
  });
  filterCommands();
  document.querySelectorAll('[data-stage]').forEach(button => button.addEventListener('click', () => {
    activeStage = button.dataset.stage;
    document.querySelectorAll('[data-stage]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    filterCommands();
  }));

  const menu = $('menu-toggle');
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    $('guide-nav').classList.toggle('is-open', open);
  });
  document.querySelectorAll('#guide-nav a').forEach(link => link.addEventListener('click', () => {
    $('guide-nav').classList.remove('is-open');
    menu.setAttribute('aria-expanded', 'false');
  }));

  const marks = [...document.querySelectorAll('[data-progress]')];
  const savedControl = document.querySelector('[data-guide-offline]');
  const progressKey = 'linearboard-guide-reading-v1';
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(progressKey) || '{}'); } catch {}
  function updateProgress() {
    const completed = marks.filter(mark => mark.checked).length;
    $('progress').value = completed;
    $('progress-label').textContent = `閱讀進度 ${completed} / ${marks.length}`;
    const state = {};
    marks.forEach(mark => state[mark.dataset.progress] = mark.checked);
    try { localStorage.setItem(progressKey, JSON.stringify(state)); } catch {}
  }
  marks.forEach(mark => {
    if (!savedControl) mark.checked = Boolean(saved[mark.dataset.progress]);
    mark.addEventListener('change', updateProgress);
  });
  $('reset').addEventListener('click', () => { marks.forEach(mark => mark.checked = false); updateProgress(); toast('已重設閱讀進度；未修改 LinearBoard。'); });
  updateProgress();

  const navLinks = [...document.querySelectorAll('#guide-nav a')];
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navLinks.forEach(link => link.classList.toggle('active', link.hash === `#${entry.target.id}`));
    }), {rootMargin: '-8% 0px -70% 0px'});
    document.querySelectorAll('main > section').forEach(section => observer.observe(section));
  }

// Export only this trusted runtime and the inert command data. The online page
// keeps script-src self; each standalone download authorizes its exact script hash.
const download=document.querySelector('a[download]');
download.addEventListener('click',async event=>{
 event.preventDefault();
 try{
  const runtime=('('+initializeLinearBoardGuide.toString()+')();').replace(/<\/script/gi,'<\\/script');
  const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(runtime));
  const hash=btoa(String.fromCharCode(...new Uint8Array(digest)));
  const copy=document.documentElement.cloneNode(true);
  copy.setAttribute('data-guide-offline', 'true');
  const originals=[...document.querySelectorAll('input,select,textarea')];
  copy.querySelectorAll('input,select,textarea').forEach((control,index)=>{
   const original=originals[index];
   if(control.tagName==='SELECT') [...control.options].forEach((option,n)=>option.toggleAttribute('selected',original.options[n].selected));
   else if(control.tagName==='TEXTAREA')control.textContent=original.value;
   else if(control.type==='checkbox'||control.type==='radio')control.toggleAttribute('checked',original.checked);
   else control.setAttribute('value',original.value);
  });
  copy.querySelectorAll('meta[http-equiv="Content-Security-Policy"]').forEach(meta=>meta.remove());
  const policy=document.createElement('meta');policy.httpEquiv='Content-Security-Policy';
  policy.content="default-src 'none'; script-src 'sha256-"+hash+"'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; base-uri 'none'; form-action 'none'";
  copy.querySelector('head').prepend(policy);
  copy.querySelectorAll('script').forEach(script=>{
   if(script.hasAttribute('data-guide-runtime')){script.removeAttribute('src');script.removeAttribute('defer');script.textContent=runtime;}
   else if(script.id==='command-data')script.textContent=JSON.stringify(commands).replaceAll('<','\\u003c').replaceAll('>','\\u003e').replaceAll('&','\\u0026');
   else script.remove();
  });
  copy.querySelector('a.download').setAttribute('href','#download');
  const blob=new Blob(['<!doctype html>\n',copy.outerHTML],{type:'text/html;charset=utf-8'});
  const url=URL.createObjectURL(blob),link=document.createElement('a');
  link.href=url;link.download='linearboard-command-tutorial.html';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  toast('已下載完整離線版 HTML；頁面中的指令不會自動執行。');
 }catch(error){
  if(location.protocol==='http:'||location.protocol==='https:')location.assign(download.href);
  else toast('此瀏覽器無法匯出離線 HTML，請使用支援 Web Crypto 的瀏覽器。');
 }
});

}
initializeLinearBoardGuide();
