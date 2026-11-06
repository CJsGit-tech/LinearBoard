import { t } from "./i18n.js";
import React, { useLayoutEffect, useRef, useState } from "react";
import {
  S,
  list,
  get,
  project,
  teamStatuses,
  defaultStatus,
  labelName,
  api,
  persist,
  refresh,
  render,
  notify,
  dismissDialog,
  closeDialog,
  openIssue,
  openDocument,
  reopen,
  canGoBack,
  moveToTrash,
} from "./model.js";
import { cats, defaultStatuses, statusLabel, stamp, relationLabels, approvalOptions, dispatchOptions } from "./labels.js";
import {
  Button,
  Icon,
  Markdown,
  Picker,
  Select,
  Field,
  Input,
  Area,
  MilestoneField,
  LabelsSelect,
  IssueChip,
  AttachmentSections,
  AutoTitle,
  BodyEditor,
  revealAnchor,
} from "./ui.jsx";
function FormShell({ title, children, onSubmit, submit = t("儲存") }) {
  const [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  return (
    <form
      id="record-form"
      onSubmit={async (e) => {
        e.preventDefault();
        if (busy) return;
        const fd = new FormData(e.currentTarget);
        setBusy(true);
        setError("");
        try {
          await onSubmit(fd);
        } catch (error) {
          setError(error.message);
        } finally {
          setBusy(false);
        }
      }}
    >
      <header className="dialog-head">
        <h2 id="modal-title">{title}</h2>
        <Button
          action="close"
          icon="x"
          aria-label={t("關閉")}
          className="icon-button"
        />
      </header>
      <div className="form-content">{children}</div>
      <footer className="dialog-foot">
        <span id="form-error" role="alert">
          {error}
        </span>
        <Button action="close">{t("取消")}</Button>
        <button className="primary" type="submit" disabled={busy}>
          {submit}
        </button>
      </footer>
    </form>
  );
}
function RecordForm({ kind, record: r }) {
  const teams = S.db.teams.filter((t) => !t.archived);
  const [labelTeam, setLabelTeam] = useState(r.team_id || project()?.team_id || teams[0]?.id || ""),
    [labelParent, setLabelParent] = useState(r.parent_id || "");
  const labelGroups = S.db.labels.filter((l) => !l.archived && l.is_group && l.team_id === labelTeam);
  const available = list("issues").filter((i) =>
    ["FrontEnd", "BackEnd"].includes(i.category),
  );
  const names = {
    projects: t("專案"),
    teams: t("團隊"),
    milestones: t("里程碑"),
    labels: t("標籤"),
    views: " View",
    batches: t("交付批次"),
    dispatches: t("派工紀錄"),
    evidence: t("驗證證據"),
    comments: t("留言"),
  };
  return (
    <FormShell
      title={(r.id ? t("編輯") : t("新增")) + names[kind]}
      onSubmit={async (fd) => {
        const owner = S.modal;
        const data = Object.fromEntries(fd);
        if (["views", "batches", "dispatches"].includes(kind))
          for (const key of ["statuses", "issue_ids", "label_ids"])
            if (
              fd.has(key) ||
              (kind === "views" && ["statuses", "label_ids"].includes(key)) ||
              (kind !== "views" && key === "issue_ids")
            )
              data[key] = fd.getAll(key);
        if (kind === "teams")
          data.statuses = String(fd.get("statuses") || "")
            .split(/\r?\n/)
            .map((s) => s.trim())
            .filter(Boolean);
        if (kind === "labels") {
          data.is_group = fd.has("is_group");
          data.single_select = fd.has("single_select");
        }
        if (!["teams", "projects", "labels", "comments"].includes(kind))
          data.project_id = S.project;
        if (kind === "evidence") data.issue_id = r.issue_id;
        const saved = await persist(kind, r, data);
        if (S.modal !== owner) return;
        if (kind === "evidence" && r.issue_id) {
          await reopen("issues", r.issue_id, { owner });
          notify(t("已儲存"));
          return;
        }
        if (kind === "comments" && ["issues", "documents"].includes(r.target_kind)) {
          await reopen(r.target_kind, r.target_id, { owner });
          notify(t("已儲存"));
          return;
        }
        dismissDialog();
        if (kind === "projects") S.project = saved.id;
        await refresh();
        render();
        notify(t("已儲存"));
      }}
    >
      {kind === "teams" && (
        <>
          <Field label={t("團隊名稱")}>
            <Input name="name" value={r.name} required />
          </Field>
          <Field label={t("團隊代碼")}>
            <Input
              name="key"
              value={r.key}
              required
              pattern="[A-Z][A-Z0-9]{1,9}"
              placeholder={t("例如 DEV")}
            />
          </Field>
          <Field label={t("工作流狀態（每行一個）")}>
            <Area
              name="statuses"
              value={(r.id
                ? teamStatuses(r.id)
                : S.db.statuses || defaultStatuses
              ).join("\n")}
              rows={7}
            />
          </Field>
          <p className="muted small">{t("仍被任務或 View 使用的狀態不可移除。")}</p>
        </>
      )}
      {kind === "projects" && (
        <>
          <Field label={t("專案名稱")}>
            <Input name="name" value={r.name} required autoFocus />
          </Field>
          <Field label={t("團隊")}>
            <Select
              name="team_id"
              items={teams}
              value={r.team_id || teams[0]?.id}
              disabled={Boolean(r.id)}
            />
          </Field>
          <Field label={t("專案說明")}>
            <Area name="body" value={r.body} />
          </Field>
        </>
      )}
      {kind === "milestones" && (
        <>
          <Field label={t("名稱")}>
            <Input name="name" value={r.name} required />
          </Field>
          <Field label={t("預期成果")}>
            <Area name="description" value={r.description} rows={3} />
          </Field>
          <Field label={t("目標日期（選填）")}>
            <Input name="target_date" value={r.target_date} type="date" />
          </Field>
        </>
      )}
      {kind === "labels" && (
        <>
          <Field label={t("名稱")}>
            <Input name="name" value={r.name} required />
          </Field>
          <Field label={t("團隊")}>
            <Picker name="team_id" items={teams} value={labelTeam} onValueChange={(teamId) => {
              setLabelTeam(teamId);
              if (!S.db.labels.some((l) => l.id === labelParent && !l.archived && l.is_group && l.team_id === teamId))
                setLabelParent("");
            }} />
          </Field>
          <Field label={t("上層群組")}>
            <Picker name="parent_id" value={labelParent} onValueChange={setLabelParent}
              items={labelGroups} blank={t("無群組")} />
          </Field>
          <label className="check-field">
            <input
              type="checkbox"
              name="is_group"
              defaultChecked={r.is_group || false}
            />{t("建立為群組")}</label>
          <label className="check-field">
            <input
              type="checkbox"
              name="single_select"
              defaultChecked={r.single_select || false}
            />{t("群組內單選")}</label>
        </>
      )}
      {kind === "views" && (
        <>
          <Field label={t("View 名稱")}>
            <Input name="name" value={r.name} required />
          </Field>
          <Field label={t("類別")}>
            <Select
              name="category"
              items={S.db.categories}
              value={r.category}
              blank={t("所有類別")}
            />
          </Field>
          <MilestoneField record={r} />
          <Field label={t("狀態（未選取時包含全部）")}>
            <div className="checkbox-grid">
              {teamStatuses().map((s) => (
                <label key={s}>
                  <input
                    name="statuses"
                    type="checkbox"
                    value={s}
                    defaultChecked={r.statuses?.includes(s) || false}
                  />
                  {statusLabel(s)}
                </label>
              ))}
            </div>
          </Field>
          <Field label={t("必含標籤")}>
            <LabelsSelect selected={r.label_ids || []} />
          </Field>
          <Field label={t("分組")}>
            <Select
              name="group_by"
              items={[
                { id: "status", name: t("狀態") },
                { id: "category", name: t("類別") },
                { id: "milestone_id", name: t("里程碑") },
                { id: "priority", name: t("優先級") },
              ]}
              value={r.group_by || "status"}
            />
          </Field>
          <Field label={t("顯示位置")}>
            <Select
              name="placement"
              items={[
                { id: "tabs", name: t("任務分頁列") },
                { id: "shared", name: t("側邊共享 Views") },
              ]}
              value={r.placement || "tabs"}
            />
          </Field>
        </>
      )}
      {["batches", "dispatches"].includes(kind) && (
        <>
          {kind === "batches" ? (
            <Field label={t("批次名稱")}>
              <Input name="name" value={r.name} required />
            </Field>
          ) : (
            <Field label="Worker／Run ID">
              <Input name="worker" value={r.worker} required />
            </Field>
          )}
          <MilestoneField record={r} />
          <Field
            label={kind === "batches" ? t("FE／BE 任務") : t("負責任務（選一張）")}
          >
            <div className="issue-checklist">
              {available.map((i) => (
                <label key={i.id}>
                  <input
                    type={kind === "batches" ? "checkbox" : "radio"}
                    name="issue_ids"
                    value={i.id}
                    defaultChecked={r.issue_ids?.includes(i.id) || false}
                  />
                  <code>{i.identifier}</code>
                  <span>{i.title}</span>
                </label>
              ))}
              {!available.length && (
                <p className="muted">{t("請先建立 FE／BE 任務。")}</p>
              )}
            </div>
          </Field>
          {kind === "batches" ? (
            <>
              <Field label={t("分組原因")}>
                <Area name="rationale" value={r.rationale} rows={3} />
              </Field>
              <Field label={t("交付成果與驗證方式")}>
                <Area name="checkpoint" value={r.checkpoint} rows={4} />
              </Field>
              <Field label={t("前置批次／阻礙")}>
                <Area name="dependencies" value={r.dependencies} rows={2} />
              </Field>
            </>
          ) : (
            <>
              <Field label={t("執行目標")}>
                <Input
                  name="target"
                  value={r.target}
                  required
                  placeholder={t("Repository、App 入口或測試 URL")}
                />
              </Field>
              <Field label={t("範圍與來源")}>
                <Area name="scope" value={r.scope} rows={3} />
              </Field>
              <Field label={t("已審閱計畫")}>
                <Area name="plan" value={r.plan} rows={4} />
              </Field>
              <Field label={t("狀態")}>
                <Select
                  name="state"
                  items={dispatchOptions}
                  value={r.state || "review"}
                />
              </Field>
              <Field label={t("Worker 回報")}>
                <Area name="report" value={r.report} rows={4} />
              </Field>
              <Field label={t("TPM 獨立檢查")}>
                <Area name="verification" value={r.verification} rows={3} />
              </Field>
            </>
          )}
        </>
      )}
      {kind === "comments" && (
        <Field label={t("留言內容")}>
          <Area name="body" value={r.body} rows={8} />
        </Field>
      )}
      {kind === "evidence" && (
        <>
          <Field label={t("驗收條件")}>
            <Input name="criterion" value={r.criterion} required />
          </Field>
          <Field label={t("結果")}>
            <Select
              name="result"
              items={["Pass", "Fail", "Not tested", "Environment-blocked"]}
              value={r.result || "Not tested"}
            />
          </Field>
          <Field label={t("環境／Viewport／路徑")}>
            <Input name="environment" value={r.environment} required />
          </Field>
          <Field label={t("操作、觀察與限制")}>
            <Area name="body" value={r.body} rows={5} />
          </Field>
        </>
      )}
    </FormShell>
  );
}
function NewIssue({ record: r }) {
  const [category, setCategory] = useState(r.category || "FrontEnd"),
    [status, setStatus] = useState(defaultStatus(r.category, r.status)),
    [explicitStatus, setExplicitStatus] = useState(Boolean(r.status && teamStatuses().includes(r.status)));
  return (
    <FormShell
      title={t("新增任務")}
      submit={t("建立任務")}
      onSubmit={async (fd) => {
        const saved = await api("issues", {
          ...(r.priority ? { priority: r.priority } : {}),
          ...Object.fromEntries(fd),
          label_ids: fd.getAll("label_ids"),
          project_id: S.project,
        });
        dismissDialog();
        await refresh();
        render();
        await openIssue(saved.id);
        notify(t("已建立任務"));
      }}
    >
      <Field label={t("任務標題")}>
        <Input name="title" required autoFocus />
      </Field>
      <div className="field-grid">
        <Field label={t("類別")}>
          <Picker
            name="category"
            value={category}
            onValueChange={(value) => {
              setCategory(value);
              setStatus(defaultStatus(value, explicitStatus ? status : undefined));
            }}
            items={S.db.categories}
          />
        </Field>
        <Field label={t("狀態")}>
          <Picker
            name="status"
            value={status}
            onValueChange={(value) => { setStatus(value); setExplicitStatus(true); }}
            items={teamStatuses()}
          />
        </Field>
        <MilestoneField record={r} />
      </div>
      <Field label={t("標籤")}>
        <LabelsSelect selected={r.label_ids} />
      </Field>
      <BodyEditor value={r.body || ""} />
    </FormShell>
  );
}
function CommentForm({ kind, id }) {
  const [body, setBody] = useState(S.modal?.draft?.comment || ""),
    [busy, setBusy] = useState(false);
  return (
    <form
      id={kind === "issues" ? "comment-form" : "doc-comment-form"}
      onSubmit={async (e) => {
        e.preventDefault();
        if (busy) return;
        setBusy(true);
        const owner = S.modal;
        try {
          await api("comments", {
            target_kind: kind,
            target_id: id,
            body,
            author: "user",
          });
          await reopen(kind, id, { owner, commentSent: true });
        } catch (error) {
          notify(error.message, true);
          setBusy(false);
        }
      }}
    >
      <textarea
        name="body"
        rows={3}
        required
        aria-label={kind === "issues" ? t("任務留言") : t("文件留言")}
        placeholder={t("新增留言…")}
        value={body}
        onChange={(e) => setBody(e.target.value)}
      />
      <button className="button" type="submit" disabled={busy}>
        <Icon name="send" />{t("送出留言")}</button>
    </form>
  );
}
function Comment({ record: c, document = false }) {
  return (
    <article className="comment">
      {!document && (
        <span className="avatar small-avatar">
          {c.author === "user" ? "CJ" : "AG"}
        </span>
      )}
      <div>
        <span className="small muted">
          {!document ? (c.author || "user") + " · " : ""}
          {stamp(c.created_at)}
        </span>
        <Button
          action="edit-record"
          kind="comments"
          id={c.id}
          className="quiet comment-edit"
        >{t("編輯")}</Button>
        <Button action="trash-confirm" kind="comments" id={c.id} icon="trash" className="icon-button" aria-label={t("刪除留言")} />
        <Markdown body={c.body} />
      </div>
    </article>
  );
}
function ObjectBack() {
  return <Button action="back-object" icon="arrow-left" className="quiet object-back"
    disabled={!canGoBack()} title={t("返回（Alt+←）")} aria-label={t("返回")}>{t("返回")}</Button>;
}
const trashNames = { get projects() { return t("專案"); }, get issues() { return t("任務"); }, get documents() { return t("文件"); }, get milestones() { return t("里程碑"); }, views: 'View', get labels() { return t("標籤"); }, get teams() { return t("團隊"); }, get comments() { return t("留言"); }, get attachments() { return t("附件"); }, get evidence() { return t("驗證證據"); }, get batches() { return t("交付批次"); }, get dispatches() { return t("派工紀錄"); }, get relations() { return t("關聯"); } };
function TrashConfirm({ modal }) {
  const [busy, setBusy] = useState(false), [error, setError] = useState('');
  const groups = {};
  for (const entry of modal.impact.deleted) groups[entry.kind] = (groups[entry.kind] || 0) + 1;
  const multiple = Array.isArray(modal.id);
  const root = modal.impact.deleted.find(entry => entry.record.id === (multiple ? modal.id[0] : modal.id))?.record;
  const relation = modal.kind === 'relations' && root && `${get('issues', root.source_id)?.identifier || root.source_id} ${relationLabels[root.relation] || root.relation} ${get('issues', root.target_id)?.identifier || root.target_id}`;
  return <div className="trash-confirm">
    <header className="dialog-head"><h2 id="modal-title">{t("移至垃圾桶")}</h2><Button action="close" icon="x" aria-label={t("關閉")} className="icon-button" /></header>
    <div className="form-content">
      <p>{multiple ? t("將選取的 {0} 個任務移至垃圾桶？", modal.id.length) : t("將「{0}」移至垃圾桶？", root?.title || root?.name || root?.criterion || root?.worker || root?.body?.slice(0, 80) || relation || modal.id)}</p>
      <p className="muted small">{t("包含 ")}{Object.entries(groups).map(([kind, count]) => `${trashNames[kind] || kind} ${count}`).join(t('、'))}。</p>
      {modal.impact.affected.length > 0 && <p className="muted small">{t("另有 {0} 筆紀錄的關聯會調整。", modal.impact.affected.length)}</p>}
      <span id="form-error" role="alert">{error}</span>
    </div>
    <footer className="dialog-foot"><Button action="close">{t("取消")}</Button><button type="button" className="primary" disabled={busy} onClick={async () => {
      if (busy) return; setBusy(true); setError('');
      try { await moveToTrash(modal.kind, modal.id, modal.impact.fingerprint); }
      catch (e) { setError(e.message); setBusy(false); }
    }}>{t("移至垃圾桶")}</button></footer>
  </div>;
}
function TrashPurgeConfirm({ modal }) {
  const [busy, setBusy] = useState(false), [error, setError] = useState('');
  return <div className="trash-confirm">
    <header className="dialog-head"><h2 id="modal-title">{t("永久刪除")}</h2><Button action="close" icon="x" aria-label={t("關閉")} className="icon-button" /></header>
    <div className="form-content">
      <p>{t("永久刪除 {0} 筆垃圾桶紀錄？", modal.count)}</p>
      <p className="muted small">{t("此操作無法還原；先前的資料庫備份仍可能包含這些資料。")}</p>
      <span id="form-error" role="alert">{error}</span>
    </div>
    <footer className="dialog-foot"><Button action="close">{t("取消")}</Button><button type="button" className="primary" disabled={busy} onClick={async () => {
      if (busy) return; setBusy(true); setError('');
      try { await api('trash/purge', { batch_ids: modal.batchIds }); dismissDialog(); S.trashRevision = (S.trashRevision || 0) + 1; render(); notify(t("已永久刪除")); }
      catch (e) { setError(e.message); setBusy(false); }
    }}>{t("永久刪除")}</button></footer>
  </div>;
}
function IssueDetail({ record: r, history }) {
  const [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  const relations = list("relations").filter(
      (rel) => rel.source_id === r.id || rel.target_id === r.id,
    ),
    attachments = list("attachments").filter((a) => a.target_id === r.id),
    evidence = list("evidence").filter((e) => e.issue_id === r.id),
    comments = list("comments").filter(
      (c) => c.target_kind === "issues" && c.target_id === r.id,
    );
  return (
    <>
      <header className="dialog-head">
        <div className="inline">
          <ObjectBack />
          <span className="identifier">{r.identifier}</span>
          <span className="badge">{cats[r.category]}</span>
        </div>
        <div className="actions">
          <button type="submit" form="issue-form" className="primary" disabled={busy}>{t("儲存變更")}</button>
          <Button action="trash-confirm" kind="issues" id={r.id} icon="trash" className="quiet">{t("刪除")}</Button>
          <Button
            action="copy-link"
            icon="link-2"
            aria-label={t("複製任務連結")}
            className="icon-button"
          />
          <Button
            action="close"
            icon="x"
            aria-label={t("關閉任務")}
            className="icon-button"
          />
        </div>
      </header>
      <div className="issue-detail">
        <form
          id="issue-form"
          onSubmit={async (e) => {
            e.preventDefault();
            if (busy) return;
            setBusy(true);
            setError("");
            const owner = S.modal;
            const fd = new FormData(e.currentTarget),
              categoryIds = S.db.labels
                .filter((l) => get("labels", l.parent_id)?.name === "Category")
                .map((l) => l.id);
            const ids = [
              ...fd.getAll("label_ids"),
              ...r.label_ids.filter((id) => categoryIds.includes(id)),
            ];
            try {
              await persist("issues", r, {
                ...Object.fromEntries(fd),
                label_ids: ids,
              });
              await reopen("issues", r.id, { saved: true, owner });
              notify(t("已儲存變更"));
            } catch (error) {
              setError(error.message);
              setBusy(false);
            }
          }}
        >
          <div className="issue-edit-content">
            <AutoTitle value={r.title} label={t("任務標題")} />
            <BodyEditor value={r.body} initialPreview={S.modal?.draft?.preview ?? true} />
            <span id="form-error" role="alert">{error}</span>
          </div>
          <aside className="issue-properties" aria-label={t("任務屬性")}>
            <div className="property-grid">
              <Field label={t("狀態")}>
                <Select
                  name="status"
                  items={teamStatuses(r.team_id)}
                  value={r.status}
                />
              </Field>
              <Field label={t("類別")}>
                <Select
                  name="category"
                  items={S.db.categories}
                  value={r.category}
                />
              </Field>
              <MilestoneField record={r} />
            </div>
            <details className="supplemental-properties">
              <summary>{t("其他屬性")}</summary>
              <Field label={t("優先級")}>
                <Select
                  name="priority"
                  items={["No priority", "Urgent", "High", "Medium", "Low"]}
                  value={r.priority}
                />
              </Field>
              <Field label={t("負責人")}>
                <Input name="assignee" value={r.assignee} />
              </Field>
              <Field label={t("上層任務")}>
                <Select
                  name="parent_id"
                  items={list("issues")
                    .filter((i) => i.id !== r.id)
                    .map((i) => ({
                      id: i.id,
                      name: i.identifier + " " + i.title,
                    }))}
                  value={r.parent_id}
                  blank={t("無")}
                />
              </Field>
            </details>
            <details className="label-details">
              <summary>{t("標籤")}{" "}
                <span className="muted">
                  {r.label_ids.filter((id) => get("labels", get("labels", id)?.parent_id)?.name !== "Category").map(labelName).join(" · ")}
                </span>
              </summary>
              <LabelsSelect selected={r.label_ids} />
            </details>
            <section className="detail-section">
              <div className="section-title">
                <h3>{t("關聯與依賴")}</h3>
                <Button
                  action="new-relation"
                  id={r.id}
                  icon="plus"
                  className="quiet"
                >{t("新增關聯")}</Button>
              </div>
              {relations.map((rel) => {
                const out = rel.source_id === r.id;
                return (
                  <div className="relation-row" key={rel.id}>
                    <span className="muted small">
                      {rel.relation === "blocks"
                        ? out
                          ? t("阻擋")
                          : t("受阻於")
                        : relationLabels[rel.relation] || rel.relation}
                    </span>
                    <IssueChip
                      id={out ? rel.target_id : rel.source_id}
                      showTitle
                    />
                    <Button
                      action="trash-confirm"
                      kind="relations"
                      id={rel.id}
                      icon="x"
                      aria-label={t("移除關聯")}
                      className="icon-button"
                    />
                  </div>
                );
              })}
            </section>
          </aside>
        </form>

        <AttachmentSections records={attachments} kind="issues" id={r.id} />
        <section className="detail-section">
          <div className="section-title">
            <h3>{t("驗證證據")}</h3>
            <Button
              action="new-evidence"
              id={r.id}
              icon="plus"
              className="quiet"
            >{t("記錄驗證")}</Button>
          </div>
          {evidence.map((e) => (
            <article className="evidence" key={e.id}>
              <Button action="trash-confirm" kind="evidence" id={e.id} icon="trash" className="icon-button" aria-label={t("刪除驗證證據")} />
              <span className={"badge result-" + e.result.replaceAll(" ", "-")}>
                {e.result}
              </span>
              <strong>{e.criterion}</strong>
              <p>{e.environment}</p>
              <Markdown body={e.body} />
            </article>
          ))}
        </section>
        <section className="detail-section">
          <h3>{t("活動")}</h3>
          {comments.map((c) => (
            <Comment key={c.id} record={c} />
          ))}
          <CommentForm kind="issues" id={r.id} />
        </section>
        <details className="revisions">
          <summary>
            <Icon name="history" />{t("修訂歷史 ")}<span className="count">{history.length}</span>
          </summary>
          {history.map((h) => (
            <details key={h.after_data.version}>
              <summary>
                {stamp(h.at)} · {h.actor} · v{h.after_data.version}
              </summary>
              <pre>{JSON.stringify(h.after_data, null, 2)}</pre>
            </details>
          ))}
        </details>
      </div>
    </>
  );
}
function DocumentDetail({ record: r, history }) {
  const [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  return (
    <>
      <header className="dialog-head">
        <span className="inline">
          <ObjectBack />
          <Icon name="file-text" />{t("專案文件")}</span>
        <div className="actions">
          <button type="submit" form="document-form" className="primary" disabled={busy}>{t("儲存文件")}</button>
          {r.id && (
            <>
              <Button action="trash-confirm" kind="documents" id={r.id} icon="trash" className="quiet">{t("刪除")}</Button>
              <Button
                action="copy-link"
                icon="link-2"
                aria-label={t("複製文件連結")}
                className="icon-button"
              />
            </>
          )}
          <Button
            action="close"
            icon="x"
            aria-label={t("關閉文件")}
            className="icon-button"
          />
        </div>
      </header>
      <div className="document-detail">
        <form
          id="document-form"
          onSubmit={async (e) => {
            e.preventDefault();
            if (busy) return;
            setBusy(true);
            setError("");
            const owner = S.modal;
            const data = Object.fromEntries(new FormData(e.currentTarget));
            try {
              const saved = await persist("documents", r, {
                ...data,
                project_id: S.project,
              });
              await reopen("documents", saved.id, { saved: true, owner });
              notify(t("文件已儲存"));
            } catch (error) {
              setError(error.message);
              setBusy(false);
            }
          }}
        >
          <AutoTitle value={r.title} label={t("文件標題")} placeholder={t("文件標題")} />
          <div className="field-grid">
            <Field label={t("文件類型")}>
              <Select
                name="doc_type"
                items={[
                  "Vision",
                  "Milestones",
                  "QA",
                  "Design overview",
                  "Screen specification",
                  "Bugs",
                  "FRD",
                  "Technical Baseline",
                  "Notes",
                ]}
                value={r.doc_type}
              />
            </Field>
            <MilestoneField record={r} />
          </div>
          <BodyEditor value={r.body} document initialPreview={S.modal?.draft?.preview ?? true} />
          <div className="form-save">
            <span id="form-error" role="alert">
              {error}
            </span>
          </div>
        </form>
        {r.id && (
          <>
            <AttachmentSections records={list("attachments").filter(a => a.target_id === r.id)} kind="documents" id={r.id} />
            <section className="detail-section">
              <h3>{t("文件留言")}</h3>
              {list("comments")
                .filter(
                  (c) => c.target_kind === "documents" && c.target_id === r.id,
                )
                .map((c) => (
                  <Comment key={c.id} record={c} document />
                ))}
              <CommentForm kind="documents" id={r.id} />
            </section>
            <details className="revisions">
              <summary>{t("修訂歷史 · ")}{history.length}</summary>
              {history.map((h) => (
                <details key={h.after_data.version}>
                  <summary>
                    v{h.after_data.version} · {stamp(h.at)}
                  </summary>
                  <Markdown body={h.after_data.body} />
                </details>
              ))}
            </details>
          </>
        )}
      </div>
    </>
  );
}
function UploadForm({ kind, id }) {
  return (
    <FormShell
      title={t("新增附件")}
      submit={t("加入附件")}
      onSubmit={async (fd) => {
        const owner = S.modal;
        const data = {
            ...Object.fromEntries(fd),
            target_kind: kind,
            target_id: id,
          },
          file = fd.get("file");
        delete data.file;
        if (file?.size) {
          if (file.size > 15 * 1024 * 1024) throw Error(t("附件不可超過 15 MB。"));
          data.name = data.name || file.name;
          data.mime = file.type;
          data.content_base64 = await new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result.split(",")[1]);
            reader.onerror = reject;
            reader.readAsDataURL(file);
          });
        } else if (!data.external_url) throw Error(t("請選擇檔案或填寫連結。"));
        await api("attachments", data);
        await reopen(kind, id, { owner });
        notify(t("附件已儲存"));
      }}
    >
      <Field label={t("選擇檔案（上限 15 MB）")}>
        <input type="file" name="file" />
      </Field>
      <Field label={t("或使用外部連結")}>
        <Input name="external_url" type="url" placeholder="https://…" />
      </Field>
      <Field label={t("名稱")}>
        <Input name="name" placeholder={t("未填寫時使用檔名")} />
      </Field>
      <div className="field-grid">
        <Field label={t("畫面識別")}>
          <Input name="screen" />
        </Field>
        <Field label={t("版本")}>
          <Input name="visual_version" placeholder="v1" />
        </Field>
      </div>
      <Field label={t("用途")}>
        <Select name="approval" items={approvalOptions.filter((o) => ["draft", "evidence"].includes(o.id))} value="draft" />
      </Field>
    </FormShell>
  );
}
function RelationForm({ id }) {
  return (
    <FormShell
      title={t("新增關聯")}
      onSubmit={async (fd) => {
        const owner = S.modal;
        const data = Object.fromEntries(fd);
        if (data.relation === "blocked_by") {
          data.relation = "blocks";
          data.source_id = data.target_id;
          data.target_id = id;
        } else data.source_id = id;
        await api("relations", data);
        await reopen("issues", id, { owner });
      }}
    >
      <Field label={t("關聯類型")}>
        <Select
          name="relation"
          items={[
            { id: "related", name: t("相關任務") },
            { id: "blocks", name: t("此任務阻擋對方") },
            { id: "blocked_by", name: t("此任務被對方阻擋") },
            { id: "supersedes", name: t("取代") },
            { id: "duplicate", name: t("重複任務") },
          ]}
          value="related"
        />
      </Field>
      <Field label={t("目標任務")}>
        <Select
          name="target_id"
          items={list("issues")
            .filter((i) => i.id !== id)
            .map((i) => ({ id: i.id, name: i.identifier + " " + i.title }))}
        />
      </Field>
    </FormShell>
  );
}
export function Dialog() {
  const ref = useRef(),
    modal = S.modal;
  useLayoutEffect(() => {
    const el = ref.current;
    if (modal) {
      if (!el.open) el.showModal();
      if (modal.draft) {
        el.querySelectorAll("details").forEach((detail, i) => { detail.open = Boolean(modal.draft.expanded[i]); });
        el.scrollTop = modal.draft.scroll;
        const body = el.querySelector('[name="body"]');
        if (body) body.scrollTop = modal.draft.bodyScroll || 0;
      } else el.scrollTop = 0;
      if (modal.fragment && !revealAnchor(el, modal.fragment)) notify(t("找不到此文件段落。"), true);
    } else if (el.open) el.close();
  }, [modal?.key]);
  let content = null;
  if (modal) {
    if (modal.type === "record")
      content = <RecordForm kind={modal.kind} record={modal.record} />;
    else if (modal.type === "new-issue")
      content = <NewIssue record={modal.record} />;
    else if (modal.type === "issue")
      content = <IssueDetail record={{ ...modal.record, ...modal.draft?.fields }} history={modal.history} />;
    else if (modal.type === "document")
      content = (
        <DocumentDetail record={{ ...modal.record, ...modal.draft?.fields }} history={modal.history} />
      );
    else if (modal.type === "upload")
      content = <UploadForm kind={modal.kind} id={modal.id} />;
    else if (modal.type === "relation")
      content = <RelationForm id={modal.id} />;
    else if (modal.type === "trash-confirm")
      content = <TrashConfirm modal={modal} />;
    else if (modal.type === "trash-purge-confirm")
      content = <TrashPurgeConfirm modal={modal} />;
  }
  return (
    <dialog
      ref={ref}
      id="dialog"
      className={
        modal?.type === "issue"
          ? "detail-dialog"
          : modal?.type === "document"
            ? "document-dialog"
            : "form-dialog"
      }
      aria-label={
        modal?.type === "issue"
          ? t("任務詳情")
          : modal?.type === "document"
            ? t("專案文件")
            : undefined
      }
      aria-labelledby={
        modal && !["issue", "document"].includes(modal.type)
          ? "modal-title"
          : undefined
      }
      onCancel={(e) => {
        e.preventDefault();
        closeDialog();
      }}
    >
      <React.Fragment key={modal?.key}>{content}</React.Fragment>
    </dialog>
  );
}
