import React, { useEffect, useState } from "react";
import Issues from "./issues.jsx";
import {
  S,
  caps,
  list,
  get,
  project,
  teamStatuses,
  milestoneName,
  api, refresh, render, notify, show,
} from "./model.js";
import { statusLabel, stamp, dispatchOptions, relationLabels } from "./labels.js";
import {
  Button,
  Icon,
  StatusIcon,
  Options,
  Markdown,
  Empty,
  IssueChip,
} from "./ui.jsx";
export function Welcome() {
  return (
    <section className="welcome">
      <div className="welcome-symbol">
        <Icon name="layers" />
      </div>
      <h1>尚無專案</h1>
      <Button action="new-project" icon="plus" className="primary">
        建立專案
      </Button>
    </section>
  );
}
function Heading({ title, children }) {
  return (
    <div className="page-heading">
      <div>
        <h1>{title}</h1>
      </div>
      {children}
    </div>
  );
}
export function DocumentRows({ documents }) {
  return documents.length ? (
    documents.map((d) => (
      <Button
        key={d.id}
        action="open-document"
        id={d.id}
        className="document-row"
      >
        <span className="doc-icon">
          <Icon name="file-text" />
        </span>
        <div>
          <strong>{d.title}</strong>
          <span>
            {d.doc_type || "Document"}
            {d.milestone_id ? " · " + milestoneName(d.milestone_id) : ""}
          </span>
        </div>
        <time>{stamp(d.updated_at)}</time>
        <Icon name="chevron-right" />
      </Button>
    ))
  ) : (
    <Empty title="尚無文件" />
  );
}
export function Milestones() {
  const milestones = list("milestones");
  return milestones.length ? (
    milestones.map((m) => {
      const issues = list("issues").filter((i) => i.milestone_id === m.id),
        done = issues.filter((i) => i.status === "Done").length,
        prefix = m.name.match(/^(M\d+)\s*[—·-]\s*/);
      return (
        <article className="milestone-row" key={m.id} aria-label={m.name}>
          <div className="milestone-symbol">
            {prefix ? prefix[1] : <Icon name="flag" />}
          </div>
          <div className="milestone-content">
            <h3 aria-label={m.name}>{prefix ? m.name.slice(prefix[0].length) : m.name}</h3>
            {m.target_date && <time className="small muted">{m.target_date}</time>}
            {m.description && (
              <details className="milestone-description">
                <summary>預期成果</summary>
                <p>{m.description}</p>
              </details>
            )}
          </div>
          <div className="milestone-acceptance">
            <strong>{done} / {issues.length}</strong>
            <span>已驗收</span>
            <progress value={done} max={issues.length || 1} aria-label={m.name + "完成進度"} />
          </div>
          <div className="actions record-actions"><Button
            action="edit-record"
            kind="milestones"
            id={m.id}
            icon="settings-2"
          >
            編輯
          </Button>
          <Button action="trash-confirm" kind="milestones" id={m.id} icon="trash" className="icon-button" aria-label={'刪除 ' + m.name} /></div>
        </article>
      );
    })
  ) : (
    <Empty title="尚無里程碑" />
  );
}
function Overview() {
  const p = project();
  return (
    <section className="page project-overview">
      <div className="project-symbol">
        <Icon name="boxes" />
      </div>
      <Heading title={p.name}>
        <div className="actions"><Button action="edit-project" icon="settings-2" className="quiet">
          編輯專案
        </Button><Button action="trash-confirm" kind="projects" id={p.id} icon="trash" className="quiet">刪除專案</Button></div>
      </Heading>
      <div className="project-resources">
        <h2>專案文件</h2>
        <div className="resource-links">
          {list("documents").map((d) => (
            <Button
              key={d.id}
              action="open-document"
              id={d.id}
              icon="file-text"
              className="resource-link"
            >
              {d.title}
            </Button>
          ))}
          <Button
            action="new-document"
            icon="plus"
            className="icon-button"
            aria-label="新增文件"
          />
        </div>
      </div>
      {p.body && (
        <details className="project-summary">
          <summary>專案說明</summary>
          <Markdown body={p.body} />
        </details>
      )}
      <div className="section-title">
        <h2>里程碑</h2>
        <Button action="new-milestone" icon="plus">
          新增
        </Button>
      </div>
      <Milestones />
    </section>
  );
}
function Delivery() {
  const batches = list("batches"),
    dispatches = list("dispatches");
  return (
    <section className="page">
      <Heading title="交付">
        <div className="actions">
          <Button action="new-batch" icon="boxes">
            建立批次
          </Button>
          <Button action="new-dispatch" icon="plus" className="primary">
            記錄派工
          </Button>
        </div>
      </Heading>
      <div className="section-title">
        <h2>交付批次</h2>
      </div>
      {batches.map((b) => (
        <article key={b.id} className="delivery-row">
          <div>
            <h3>{b.name}</h3>
            {b.checkpoint && <p>{b.checkpoint}</p>}
            <div className="issue-chips">
              {b.issue_ids.map((id) => (
                <IssueChip key={id} id={id} />
              ))}
            </div>
          </div>
          <div className="actions record-actions"><Button
            action="edit-record"
            kind="batches"
            id={b.id}
            icon="settings-2"
          >
            編輯
          </Button>
          <Button action="trash-confirm" kind="batches" id={b.id} icon="trash" className="icon-button" aria-label={'刪除 ' + b.name} /></div>
        </article>
      ))}
      {!batches.length && (
        <Empty title="尚無批次" />
      )}
      <div className="section-title">
        <h2>派工紀錄</h2>
        <span className="muted small">
          {
            S.db.dispatches.filter((d) => !d.archived && ["review", "executing"].includes(d.state))
              .length
          }{" "}
          / 3 工作區進行中
        </span>
      </div>
      {dispatches.map((d) => (
        <article key={d.id} className="delivery-row">
          <div>
            <div className="inline">
              <span className="badge">{dispatchOptions.find((o) => o.id === d.state)?.name || d.state}</span>
              <h3>{d.worker || "未指定執行者"}</h3>
            </div>
            <div className="issue-chips">
              {d.issue_ids.map((id) => (
                <IssueChip key={id} id={id} />
              ))}
            </div>
            {d.target && <p>{d.target}</p>}
          </div>
          <div className="actions record-actions"><Button
            action="edit-record"
            kind="dispatches"
            id={d.id}
            icon="arrow-up-right"
          >
            開啟紀錄
          </Button>
          <Button action="trash-confirm" kind="dispatches" id={d.id} icon="trash" className="icon-button" aria-label={'刪除派工 ' + (d.worker || d.id)} /></div>
        </article>
      ))}
      {!dispatches.length && (
        <Empty title="尚無派工紀錄" />
      )}
    </section>
  );
}
function Settings() {
  const p = project();
  const [section, setSection] = useState('teams');
  const sections = [
    { id: 'teams', title: '團隊', icon: 'boxes' },
    { id: 'labels', title: '標籤與群組', icon: 'list-filter' },
    { id: 'trash', title: '垃圾桶', icon: 'trash' },
    { id: 'integration', title: '整合與說明', icon: 'terminal' },
  ];
  const roots = S.db.labels.filter(
      (l) => !l.archived && (!p || l.team_id === p.team_id) && !l.parent_id,
    );
  return (
    <section className="page settings-page">
      <Heading title="工作區設定">
        <a className="button quiet settings-backup" href="/api/backup">
          <Icon name="download" />
          下載資料庫備份
        </a>
      </Heading>
      <div className="settings-layout">
        <nav className="settings-navigation" aria-label="設定分類">
          {sections.map(item => <button key={item.id} type="button" className={'settings-nav-item' + (section === item.id ? ' active' : '')}
            aria-current={section === item.id ? 'page' : undefined} onClick={() => setSection(item.id)}>
            <Icon name={item.icon} /><span>{item.title}</span>
          </button>)}
        </nav>
        <div className="settings-panel">
      {section === 'teams' && <section aria-label="團隊">
      <div className="section-title settings-section-title">
        <h2>團隊</h2>
        <Button action="new-team" icon="plus" className="quiet settings-action">
          建立團隊
        </Button>
      </div>
      {S.db.teams
        .filter((t) => !t.archived)
        .map((t) => (
          <div key={t.id} className="setting-row team-setting">
            <div>
              <strong>{t.name}</strong>
              <code>{t.key}</code>
              <p className="muted small">
                {teamStatuses(t.id).map(statusLabel).join(" · ")}
              </p>
            </div>
            <div className="actions record-actions"><Button
              action="edit-record"
              kind="teams"
              id={t.id}
              icon="settings-2" className="quiet"
            >
              編輯
            </Button>
            <Button action="trash-confirm" kind="teams" id={t.id} icon="trash" className="icon-button" aria-label={'刪除團隊 ' + t.name} /></div>
          </div>
        ))}
      </section>}
      {section === 'labels' && <section aria-label="標籤與群組">
      <div className="section-title settings-section-title">
        <h2>標籤與群組</h2>
        <Button action="new-label" icon="plus" className="quiet settings-action">
          新增標籤
        </Button>
      </div>
      {roots.filter((l) => l.is_group).map((l) => (
        <div key={l.id} className="setting-row settings-label-group">
          <div className="settings-label-heading">
            <strong>{l.name}</strong>
            {l.single_select && <small className="muted">單選</small>}
            {l.name !== 'Category' && <Button action="trash-confirm" kind="labels" id={l.id} icon="trash" className="icon-button" aria-label={'刪除標籤群組 ' + l.name} />}
          </div>
          <div className="label-cloud">
            {S.db.labels
              .filter((c) => !c.archived && c.parent_id === l.id)
              .map((c) => (
                <span className="badge" key={c.id}>
                  {c.name}
                  {l.name !== 'Category' && <Button action="trash-confirm" kind="labels" id={c.id} icon="trash" className="icon-button" aria-label={'刪除標籤 ' + c.name} />}
                </span>
              ))}
          </div>
        </div>
      ))}
      {roots.some((l) => !l.is_group) && (
        <div className="settings-ungrouped">
        <h3>標籤</h3>
        <div className="label-cloud standalone-labels" aria-label="標籤">
          {roots.filter((l) => !l.is_group).map((l) => (
            <span className="badge" key={l.id}>{l.name}<Button action="trash-confirm" kind="labels" id={l.id} icon="trash" className="icon-button" aria-label={'刪除標籤 ' + l.name} /></span>
          ))}
        </div>
        </div>
      )}
      {!roots.length && (
        <Empty title="尚無標籤" detail="建立專案後會自動準備 Category。" />
      )}
      </section>}
      {section === 'trash' && <TrashPanel />}
      {section === 'integration' && <section aria-label="整合與說明">
      <div className="section-title settings-section-title"><h2>整合與說明</h2></div>
      <div className="settings-links">
        <Button action="nav" page="integration" icon="terminal" className="quiet">整合與指令</Button>
        <a className="button quiet" href="/guide" target="_blank" rel="noopener"><Icon name="arrow-up-right" />操作指南</a>
      </div>
      </section>}
        </div>
      </div>
    </section>
  );
}
function TrashPanel() {
  const [items, setItems] = useState([]), [error, setError] = useState(''), [busy, setBusy] = useState('');
  useEffect(() => {
    let active = true;
    api('trash').then(data => { if (active) { setItems(data); setError(''); } }, e => { if (active) setError(e.message); });
    return () => { active = false; };
  }, [S.trashRevision]);
  const names = { projects: '專案', issues: '任務', documents: '文件', milestones: '里程碑', views: 'View', labels: '標籤', teams: '團隊', comments: '留言', attachments: '附件', evidence: '驗證證據', batches: '交付批次', dispatches: '派工紀錄', relations: '關聯' };
  return <section aria-label="垃圾桶">
    <div className="section-title settings-section-title"><h2>垃圾桶</h2>{items.length > 0 && <button type="button" className="quiet settings-action" disabled={Boolean(busy)} onClick={() => show({ type: 'trash-purge-confirm', batchIds: items.map(item => item.batch_id), count: items.reduce((sum, item) => sum + item.count, 0) })}>清空垃圾桶</button>}</div>
    {error && <p role="alert">{error}</p>}
    {!items.length && !error && <p className="muted small">垃圾桶是空的</p>}
    {items.map(item => {
      const relation = item.kind === 'relations' && `${get('issues', item.record.source_id)?.identifier || item.record.source_id} ${relationLabels[item.record.relation] || item.record.relation} ${get('issues', item.record.target_id)?.identifier || item.record.target_id}`;
      const title = item.root_ids?.length > 1 ? `${item.root_ids.length} 個任務` : item.record.title || item.record.name || item.record.criterion || item.record.worker || item.record.body?.slice(0, 80) || relation || item.record.id;
      return <div className="setting-row" key={item.batch_id}>
        <div><span className="badge">{names[item.kind] || item.kind}</span> <strong>{title}</strong><span className="muted small"> · {item.count} 筆 · {stamp(item.deleted_at)}</span></div>
        <div className="actions"><button type="button" disabled={Boolean(busy)} onClick={async () => {
          setBusy(item.batch_id); setError('');
          try { const result = await api('trash/restore', { batch_id: item.batch_id }); await refresh(); S.trashRevision = (S.trashRevision || 0) + 1; render(); notify(result.unrestored_links.length ? `已還原；${result.unrestored_links.length} 筆關聯需檢查` : '已還原'); }
          catch (e) { setError(e.message); } finally { setBusy(''); }
        }}>還原</button><button type="button" disabled={Boolean(busy)} onClick={() => show({ type: 'trash-purge-confirm', batchIds: [item.batch_id], count: item.count })}>永久刪除</button></div>
      </div>;
    })}
  </section>;
}
function Integration() {
  return (
    <section className="page integration">
      <Heading title="整合與指令">
      </Heading>
      <p>使用 linear-tpm 時，需明確指定 LinearBoard 為紀錄目的地。</p>
      <div className="integration-grid">
        <div>
          <h2>啟動 MCP adapter</h2>
          <pre>
            {"python3 mcp_server.py --url http://127.0.0.1:" + location.port}
          </pre>
          <p className="small muted">在 MCP 客戶端設定為 stdio server。</p>
        </div>
        <div>
          <h2>工具介面</h2>
          <code>
            linearboard_capabilities
            <br />
            linearboard_list / get
            <br />
            linearboard_create / update
          </code>
          <p className="small muted">
            更新需帶 expected_version，寫入可帶 idempotency key。
          </p>
        </div>
      </div>
      <div className="section-title">
        <h2>指令契約</h2>
        <a href="/api/capabilities" target="_blank" rel="noopener">
          查看 JSON <Icon name="arrow-up-right" />
        </a>
      </div>
      <p className="small muted">
        以下列出資料能力與驗證方式，不代表外部派工、圖片生成或完整 skill
        流程已驗證。
      </p>
      {(caps?.commands || []).map((c) => (
        <details className="contract" key={c.command}>
          <summary>
            <code>{c.command}</code>
            <span>
              {c.resources.length ? c.resources.join(" · ") : "唯讀／對話"}
            </span>
            <Icon name="chevron-down" />
          </summary>
          <div>
            <h3>輸入</h3>
            <p>{c.inputs}</p>
            <h3>輸出</h3>
            <p>{c.outputs}</p>
            <h3>驗證方式</h3>
            <p>{c.verification}</p>
          </div>
        </details>
      ))}
    </section>
  );
}
export function Page() {
  if (!project() && !["settings", "integration"].includes(S.page))
    return <Welcome />;
  if (S.page === "issues") return <Issues />;
  if (S.page === "overview") return <Overview />;
  if (S.page === "documents")
    return (
      <section className="page">
        <Heading title="文件">
          <Button action="new-document" icon="plus" className="primary">
            新增文件
          </Button>
        </Heading>
        <div className="document-list">
          <DocumentRows documents={list("documents")} />
        </div>
      </section>
    );
  if (S.page === "milestones")
    return (
      <section className="page">
        <Heading title="里程碑">
          <Button action="new-milestone" icon="plus" className="primary">
            新增里程碑
          </Button>
        </Heading>
        <Milestones />
      </section>
    );
  if (S.page === "delivery") return <Delivery />;
  if (S.page === "settings") return <Settings />;
  return <Integration />;
}
