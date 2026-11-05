function initializeLinearTPMGuide(){'use strict';const $=id=>document.getElementById(id),data=JSON.parse($('command-data').textContent);let toastTimer;function toast(s){$('toast').textContent=s;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').textContent='',3000)}
document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',async()=>{const el=b.closest('.codebox').querySelector('code');try{if(!navigator.clipboard)throw new Error('clipboard unavailable');await navigator.clipboard.writeText(el.textContent);const prev=b.textContent;b.textContent='已複製';toast('已複製文字。貼到 Codex 並送出才會執行。');setTimeout(()=>b.textContent=prev,1800)}catch(e){const range=document.createRange();range.selectNodeContents(el);const s=window.getSelection();s.removeAllRanges();s.addRange(range);toast('指令已選取，請按 ⌘C／Ctrl+C 複製。')}}));
// Export only this trusted runtime and the inert command data. The online page
// keeps script-src self; each standalone download authorizes its exact script hash.
const download=document.querySelector('a.download');
download.addEventListener('click',async event=>{
 event.preventDefault();
 try{
  const runtime=('('+initializeLinearTPMGuide.toString()+')();').replace(/<\/script/gi,'<\\/script');
  const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(runtime));
  const hash=btoa(String.fromCharCode(...new Uint8Array(digest)));
  const copy=document.documentElement.cloneNode(true);
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
   else if(script.id==='command-data')script.textContent=JSON.stringify(data).replaceAll('<','\\u003c').replaceAll('>','\\u003e').replaceAll('&','\\u0026');
   else script.remove();
  });
  copy.querySelector('a.download').setAttribute('href','#download');
  const blob=new Blob(['<!doctype html>\n',copy.outerHTML],{type:'text/html;charset=utf-8'});
  const url=URL.createObjectURL(blob),link=document.createElement('a');
  link.href=url;link.download='linear-tpm-command-tutorial.html';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  toast('已下載完整離線版 HTML；頁面中的指令不會自動執行。');
 }catch(error){
  if(location.protocol==='http:'||location.protocol==='https:')location.assign(download.href);
  else toast('此瀏覽器無法匯出離線 HTML，請使用支援 Web Crypto 的瀏覽器。');
 }
});
const inputs=['action','project','milestone','dispatchscope','batch','issueids','debugsource','additional'];
function build(){
 const name=$('action').value,p=$('project').value.trim()||'〈Project〉',m=$('milestone').value.trim()||'〈Milestone〉',c=data.find(x=>x.name===name);
 const mode=$('dispatchscope').value,ids=$('issueids').value.trim(),batch=$('batch').value.trim();
 const validBatch=/^[1-9]\d*$/.test(batch);
 $('dispatch-scope-field').hidden=name!=='dispatch';
 $('batch-field').hidden=name!=='dispatch'||mode!=='batch';
 $('issue-field').hidden=!(name==='organize-task-batch'||name==='dispatch'&&mode==='issues');
 $('issue-label').textContent=name==='dispatch'?'Issue IDs（必填；不會自動擴成里程碑）':'Issue IDs（分批選填；留空＝里程碑 FE／BE）';
 $('debug-field').hidden=name!=='debug';
 let arg=name==='help'?'':p+' '+m;
 if(name==='organize-task-batch'&&ids)arg+=' '+ids;
 if(name==='dispatch'&&mode==='batch')arg+=' Batch '+(validBatch?batch:'〈批次編號〉');
 if(name==='dispatch'&&mode==='issues')arg+=' '+(ids||'〈issue IDs〉');
 if(name==='debug')arg+=' '+($('debugsource').value.trim()||'〈Linear 回報文件 URL 或來源 issue IDs〉');
 let text='$linear-tpm '+name+(arg?' '+arg:'');
 if(name==='create-issues-FE')text+='\n'+c.extended.replaceAll('PocketMap',p).replaceAll('M1',m);
 else if(name==='create-issues-BE'){
  text+='\n根據既有 US、PRDs 與已確認的資料／服務範圍建立或重用 BE issues。由 agent 先查核現有服務、相依套件與官方 SDK／API 文件，選用符合平台與資料邊界的技術。保留原生 '+m+'、'+m+'＋所有來源 US labels、Category BackEnd 及 Coder；共用契約指定負責票，選型依據、限制、待驗證項目與相依寫入 tickets，建立或重用團隊 Issues 上方的 '+p+'-BE View，不 dispatch。';
  if(p==='PocketMap'&&m==='M1')text+='\nPocketMap M1 的 BE 為 App 內資料／服務，不新增伺服器或帳號。';
 }else if(name==='frd')text+='\n'+c.extended;
 else if(name==='create-visuals')text+='\n先確認視覺方向，再使用 imagegen 產生指定畫面與狀態供我審閱。';
 else if(name==='dispatch'){
  text+='\n'+(mode==='batch'?'只執行既有分批提案中指定 Batch 的確切 IDs；定義缺失或衝突先釐清，不重新分組或擴成整個里程碑。':mode==='issues'?'只執行以上指定 IDs；空白時先補齊，不自動改派整個里程碑。':c.extended.replaceAll('M1',m));
  if(mode!=='milestone')text+='\n先核對原生 milestone、相依與現有派工，列出本次 IDs、排除原因及主 App 執行目標。最多三位 active worker，責任不重疊；計畫、技術決策與獨立驗證由 TPM 寫回各票。';
  text+='\n從主 App 正常入口驗證整合與資料結果，說明應 Build／Run 的主 scheme 或服務目標。診斷畫面不代替整合驗證；可交審工作 In Review，Done 留給使用者。';
 }else if(name==='organize-task-batch'||name==='sync'||name==='debug')text+='\n'+c.extended;
 const extra=$('additional').value.trim();if(extra)text+='\n'+extra;
 $('built').textContent=text;
 const dispatchHelp=mode==='batch'?(validBatch?'需有既有 Batch 定義；不會自行選取整個里程碑。':'請填正整數 Batch 編號並確認既有定義。'):mode==='issues'?(ids?'只處理指定 IDs。':'請填實際 issue IDs，不會自動擴張範圍。'):'會完整盤點里程碑 FE／BE，先列出可派工、排除與未就緒項目。';
 $('builder-help').textContent=c.effect+' · '+c.when+' '+(name==='help'?'':name==='organize-task-batch'?'只提供分批建議，不修改 Linear 或派工。':name==='dispatch'?dispatchHelp:name==='debug'?($('debugsource').value.trim()?'預設包含指定回報的建票、修復、獨立驗證與來源回覆；只建票請明確註明。':'先填入實際問題來源再送出；不會自動把整個里程碑當成修復範圍。'):name==='planning'?'規劃預設只討論，保存需明確要求。':'送出後會依指令範圍建立或更新產出。');
}
inputs.forEach(id=>$(id).addEventListener('input',build));build();
let activeStage=document.querySelector('[data-stage][aria-pressed="true"]')?.dataset.stage||'';function filterCommands(){const q=$('search').value.trim().toLowerCase();let n=0;document.querySelectorAll('#catalog tbody tr').forEach(r=>{const hay=r.dataset.search.toLowerCase(),name=r.querySelector('code').textContent,cmd=data.find(c=>c.name===name);const stageOK=!activeStage||(activeStage==='交付'?['開發拆票','交付規劃','交付'].includes(cmd.phase):cmd.phase===activeStage);const ok=hay.includes(q)&&stageOK;r.hidden=!ok;if(ok)n++});$('result-count').textContent=n+' / '+data.length+' 個指令';$('search-empty').hidden=n!==0} filterCommands(); $('search').addEventListener('input',filterCommands);document.querySelectorAll('[data-stage]').forEach(b=>b.addEventListener('click',()=>{activeStage=b.dataset.stage;document.querySelectorAll('[data-stage]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));filterCommands()}));$('clear-search').addEventListener('click',()=>{$('search').value='';activeStage='';document.querySelectorAll('[data-stage]').forEach(x=>x.setAttribute('aria-pressed',String(x.dataset.stage==='')));filterCommands();$('search').focus()});
function composeCommand(name){$('action').value=name;build();location.hash='builder';$('action').focus({preventScroll:true})}document.querySelectorAll('[data-command]').forEach(b=>b.addEventListener('click',()=>composeCommand(b.dataset.command)));
$('menu-toggle').addEventListener('click',()=>{const open=$('menu-toggle').getAttribute('aria-expanded')!=='true';$('menu-toggle').setAttribute('aria-expanded',String(open));$('guide-nav').classList.toggle('is-open',open)});document.querySelectorAll('#guide-nav a').forEach(a=>a.addEventListener('click',()=>{$('guide-nav').classList.remove('is-open');$('menu-toggle').setAttribute('aria-expanded','false')}));
const marks=[...document.querySelectorAll('[data-progress]')],key='linear-tpm-guide-reading-v1';let stored={};try{stored=JSON.parse(localStorage.getItem(key)||'{}')}catch(e){}function progress(){const n=marks.filter(c=>c.checked).length;$('progress').value=n;$('progress-label').textContent='閱讀進度 '+n+' / '+marks.length;const saved={};marks.forEach(c=>saved[c.dataset.progress]=c.checked);try{localStorage.setItem(key,JSON.stringify(saved))}catch(e){}}marks.forEach(c=>{c.checked=!!stored[c.dataset.progress];c.addEventListener('change',progress)});$('reset').addEventListener('click',()=>{marks.forEach(c=>c.checked=false);progress();toast('已重設閱讀進度；未修改 Linear。')});progress();
const links=[...document.querySelectorAll('nav a')];if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting)links.forEach(a=>(a.classList.toggle('active',a.hash==='#'+e.target.id),a.hash==='#'+e.target.id?a.setAttribute('aria-current','location'):a.removeAttribute('aria-current')))},{rootMargin:'-5% 0px -65% 0px',threshold:0});document.querySelectorAll('main>section').forEach(s=>observer.observe(s))}
}
initializeLinearTPMGuide();
