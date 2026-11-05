import { defaultStatuses } from "./labels.js";
// The existing API and navigation state stay separate from React presentation.
let revision = 0;
const listeners = new Set();
export const subscribe = (listener) => {
  listeners.add(listener);
  return () => listeners.delete(listener);
};
export const snapshot = () => revision;
export function render() {
  revision++;
  for (const listener of listeners) listener();
}
let modalSerial = 0;
const objectHistory = [];
// A return to the workspace must not silently discard unsaved object edits.
const returnedDrafts = new Map();
let nestedParent = null;
const isObject = (modal) => ["issue", "document"].includes(modal?.type);
const objectRoute = (modal) => `#/${modal.type === "issue" ? "issues" : "documents"}/${modal.record.id}`;
function captureObject() {
  const modal = S.modal;
  if (!isObject(modal)) return modal;
  const form = document.querySelector(modal.type === "issue" ? "#issue-form" : "#document-form");
  if (!form) return modal;
  const fields = Object.fromEntries(new FormData(form));
  if (modal.type === "issue") fields.label_ids = [
    ...new FormData(form).getAll("label_ids"),
    ...modal.record.label_ids.filter((id) => get("labels", get("labels", id)?.parent_id)?.name === "Category"),
  ];
  return {
    ...modal,
    draft: {
      fields,
      preview: Boolean(form.querySelector('[name="body"]')?.hidden),
      comment: document.querySelector('#comment-form textarea, #doc-comment-form textarea')?.value || "",
      scroll: document.getElementById("dialog")?.scrollTop || 0,
      expanded: Array.from(document.querySelectorAll('#dialog details'), (el) => el.open),
    },
  };
}
export function show(modal) {
  if (isObject(S.modal) && !isObject(modal)) nestedParent = captureObject();
  if (isObject(modal) && nestedParent) {
    if (modal.type !== nestedParent.type || modal.record.id !== nestedParent.record.id)
      objectHistory.push(nestedParent);
    nestedParent = null;
  }
  if (isObject(modal) && isObject(S.modal) &&
      (modal.type !== S.modal.type || modal.record.id !== S.modal.record.id)) {
    objectHistory.push(captureObject());
    nestedParent = null;
  }
  S.modal = { ...modal, key: ++modalSerial };
  render();
}
export const canGoBack = () => isObject(S.modal);
function restoreObject(modal) {
  detailRequest++;
  S.project = modal.record.project_id || S.project;
  S.selected = modal.type === "issue" ? modal.record.id : null;
  if (modal.record.id) writeRoute(objectRoute(modal));
  S.modal = { ...modal, key: ++modalSerial };
  render();
}
export function backObject() {
  if (!canGoBack()) return;
  const current = captureObject();
  const key = current.record.id || `new:${S.project}`;
  returnedDrafts.set(`${current.type}:${key}`, current);
  if (objectHistory.length) restoreObject(objectHistory.pop());
  else closeDialog();
}
export const S = {
  db: null,
  project: localStorage.getItem("lb.project"),
  page: "issues",
  view: "all",
  layout: localStorage.getItem("lb.layout") || "list",
  q: "",
  category: "",
  status: "",
  milestone: "",
  selected: null,
  inspector: localStorage.getItem("lb.inspector") !== "false",
};
export let caps;
const inFlightWrites = new Map();

const workspaceFields = [
  "project",
  "page",
  "view",
  "layout",
  "q",
  "category",
  "status",
  "milestone",
  "filtersOpen",
];
let workspaceContext = null;
let detailRequest = 0;
let retryNavigation = null;
let requestedProject = null;
const isRecordRoute = () =>
  Boolean(location.hash.replace(/^#\//, "").split("/")[1]);
function workspaceRoute(context) {
  return context.page === "issues" && context.view !== "all"
    ? `#/views/${context.view}`
    : `#/${context.page}`;
}
function captureWorkspace() {
  const context = Object.fromEntries(
    workspaceFields.map((key) => [key, S[key]]),
  );
  return { ...context, route: workspaceRoute(context) };
}
function writeRoute(hash, context = workspaceContext) {
  history.replaceState(
    { ...history.state, linearboardWorkspace: context },
    "",
    hash,
  );
}
function rememberWorkspace() {
  workspaceContext = captureWorkspace();
  writeRoute(workspaceContext.route);
}
function fallbackWorkspace(page, projectId = S.project) {
  return {
    project: projectId,
    page,
    view: "all",
    layout: S.layout,
    q: "",
    category: "",
    status: "",
    milestone: "",
    route: `#/${page}`,
  };
}
function restoreWorkspace(context) {
  for (const key of workspaceFields)
    if (Object.hasOwn(context, key)) S[key] = context[key];
  if (!S.db.projects.some((p) => p.id === S.project && !p.archived))
    S.project = S.db.projects.find((p) => !p.archived)?.id;
  const view = get("views", S.view);
  if (
    S.view !== "all" &&
    (!view || view.archived || view.project_id !== S.project)
  )
    S.view = "all";
  S.filtersOpen = Boolean(
    context.filtersOpen || S.q || S.category || S.status || S.milestone,
  );
  S.selected = null;
}
function dismissDialog() {
  detailRequest += 1;
  S.modal = null;
  render();
  S.selected = null;
  objectHistory.length = 0;
  nestedParent = null;
}
function closeDialog() {
  if (nestedParent) {
    const parent = nestedParent;
    nestedParent = null;
    restoreObject(parent);
    return;
  }
  const recordRoute = isRecordRoute();
  dismissDialog();
  if (recordRoute) {
    restoreWorkspace(
      workspaceContext ||
        history.state?.linearboardWorkspace ||
        fallbackWorkspace(S.page),
    );
    rememberWorkspace();
    render();
  }
}
function enterDetail(type, id, projectId) {
  if (!isRecordRoute()) rememberWorkspace();
  workspaceContext ||=
    history.state?.linearboardWorkspace || fallbackWorkspace(type, projectId);
  const hash = `#/${type}/${id}`;
  writeRoute(hash);
  return { request: ++detailRequest, hash };
}

export function notify(message, error = false) {
  S.toast = { message, error };
  render();
  clearTimeout(notify.timer);
  notify.timer = setTimeout(() => {
    S.toast = null;
    render();
  }, 4000);
}
async function api(path, body, method = "POST") {
  const fingerprint =
    body === undefined ? null : JSON.stringify([path, method, body]);
  if (fingerprint && inFlightWrites.has(fingerprint))
    return inFlightWrites.get(fingerprint);
  const operation = (async () => {
    const response = await fetch("/api/" + path, {
      method: body === undefined ? "GET" : method,
      headers: {
        "Content-Type": "application/json",
        "X-LinearBoard-Actor": "user",
        "Idempotency-Key": crypto.randomUUID(),
      },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "操作失敗");
    return result;
  })();
  if (fingerprint) inFlightWrites.set(fingerprint, operation);
  try {
    return await operation;
  } finally {
    if (fingerprint) inFlightWrites.delete(fingerprint);
  }
}
function applySnapshot(snapshot) {
  S.db = snapshot;
  if (!S.db.projects.some((p) => p.id === S.project && !p.archived))
    S.project = S.db.projects.find((p) => !p.archived)?.id;
  localStorage.setItem("lb.project", S.project || "");
}
async function refresh(isCurrent = () => true) {
  const snapshot = await api("state?archived=true");
  if (!isCurrent()) return false;
  applySnapshot(snapshot);
  return true;
}
const navigationIntent = () => ({
  request: ++detailRequest,
  hash: location.hash,
});
const isCurrentNavigation = (pending) =>
  pending.request === detailRequest && pending.hash === location.hash;
async function refreshNavigation(pending) {
  const applied = await refresh(() => isCurrentNavigation(pending));
  if (applied && retryNavigation) {
    retryNavigation = null;
    S.toast = null;
  }
  return applied;
}
function navigationFailure(error, retry) {
  retryNavigation = retry;
  notify("無法取得最新資料；目前畫面尚未更新。" + error.message, true);
  clearTimeout(notify.timer);
  S.toast.retry = true;
  render();
}
async function withLatestSnapshot(work) {
  const pending = navigationIntent();
  try {
    if (!(await refreshNavigation(pending))) return;
    return await work();
  } catch (error) {
    if (isCurrentNavigation(pending))
      navigationFailure(error, () => withLatestSnapshot(work));
  }
}
function applyProjectSelection() {
  if (requestedProject === null) return;
  const id = requestedProject,
    target = get("projects", id);
  if (id && (!target || target.archived)) throw new Error("找不到此專案。");
  S.project = id;
  S.view = "all";
  S.q = S.category = S.status = S.milestone = "";
  localStorage.setItem("lb.project", S.project || "");
  requestedProject = null;
}
function navigateWorkspace(update) {
  return withLatestSnapshot(() => {
    applyProjectSelection();
    update();
    dismissDialog();
    rememberWorkspace();
    render();
  });
}
const list = (kind, all = false) =>
  S.db[kind].filter(
    (r) =>
      (all || !r.archived) && (!r.project_id || r.project_id === S.project),
  );
const get = (kind, id) => S.db[kind].find((r) => r.id === id);
const project = () => get("projects", S.project);
function teamStatuses(teamId = project()?.team_id) {
  const statuses =
    S.db.statuses_by_team?.[teamId] ||
    get("teams", teamId)?.statuses ||
    S.db.statuses ||
    defaultStatuses;
  return statuses.length ? statuses : defaultStatuses;
}
function defaultStatus(category, requested) {
  const statuses = teamStatuses();
  const preferred = category === "Design" ? "Todo" : "Backlog";
  return statuses.includes(requested)
    ? requested
    : statuses.includes(preferred)
      ? preferred
      : statuses[0];
}
const labelName = (id) => get("labels", id)?.name || id;
const milestoneName = (id) => get("milestones", id)?.name || "無里程碑";
export function filteredIssues() {
  let rows = list("issues");
  const v = get("views", S.view);
  if (v)
    rows = rows.filter(
      (r) =>
        (!v.category || r.category === v.category) &&
        (!v.milestone_id || r.milestone_id === v.milestone_id) &&
        (!v.statuses?.length || v.statuses.includes(r.status)) &&
        (v.label_ids || []).every((l) => r.label_ids.includes(l)),
    );
  return rows.filter(
    (r) =>
      (!S.category || r.category === S.category) &&
      (!S.status || r.status === S.status) &&
      (!S.milestone || r.milestone_id === S.milestone) &&
      (!S.q ||
        `${r.identifier} ${r.title} ${r.body}`
          .toLowerCase()
          .includes(S.q.toLowerCase())),
  );
}

export function editRecord(kind, record = {}, defaults = {}) {
  if (!S.project && !["teams", "projects"].includes(kind))
    return notify("請先建立專案。", true);
  show({ type: "record", kind, record: { ...defaults, ...record } });
}
export function newIssue(defaults = {}) {
  if (!S.project) return notify("請先建立專案。", true);
  const view = get("views", S.view);
  show({ type: "new-issue", record: {
    category: S.category || view?.category || "FrontEnd",
    milestone_id: S.milestone || view?.milestone_id || "",
    label_ids: view?.label_ids || [],
    ...defaults,
  } });
}
export async function openIssue(id, { fresh = true } = {}) {
  if (isObject(S.modal)) S.modal = captureObject();
  const pending = enterDetail("issues", id, get("issues", id)?.project_id);
  try {
    if (fresh && !(await refreshNavigation(pending))) return;
    const record = get("issues", id);
    if (!record) throw Error("找不到此任務。");
    S.project = record.project_id;
    const history = await api("history/" + id);
    if (!isCurrentNavigation(pending)) return;
    S.selected = id;
    const draft = returnedDrafts.get(`issue:${record.id}`);
    show(draft ? { ...draft, history } : { type: "issue", record, history });
  } catch (error) {
    if (isCurrentNavigation(pending))
      navigationFailure(error, () => openIssue(id));
  }
}
export async function openDocument(id, { fresh = true } = {}) {
  if (isObject(S.modal)) S.modal = captureObject();
  const pending = id
    ? enterDetail("documents", id, get("documents", id)?.project_id)
    : navigationIntent();
  try {
    if (fresh && !(await refreshNavigation(pending))) return;
    const record = id
      ? get("documents", id)
      : { doc_type: "Vision", title: "", body: "" };
    if (!record) throw Error("找不到此文件。");
    if (id) S.project = record.project_id;
    if (!S.project) return notify("請先建立專案。", true);
    const history = id ? await api("history/" + id) : [];
    if (!isCurrentNavigation(pending)) return;
    S.selected = null;
    const draft = returnedDrafts.get(`document:${id || `new:${S.project}`}`);
    show(draft ? { ...draft, history } : { type: "document", record, history });
  } catch (error) {
    if (isCurrentNavigation(pending))
      navigationFailure(error, () => openDocument(id));
  }
}
export async function persist(kind, record, data) {
  return api(
    kind + (record.id ? "/" + record.id : ""),
    record.id ? { ...data, expected_version: record.version } : data,
    record.id ? "PATCH" : "POST",
  );
}
export async function moveToTrash(kind, id, fingerprint) {
  await api('trash/move', Array.isArray(id) ? { kind, ids: id, fingerprint } : { kind, id, fingerprint });
  const parent = nestedParent;
  if (parent?.record.id && parent.record.id !== id) {
    const parentKind = parent.type === 'issue' ? 'issues' : 'documents';
    await reopen(parentKind, parent.record.id, { owner: S.modal });
    notify('已移至垃圾桶');
    return;
  }
  const wasDetail = isRecordRoute();
  returnedDrafts.delete(`${kind === 'issues' ? 'issue' : 'document'}:${id}`);
  dismissDialog();
  await refresh();
  if (wasDetail) restoreWorkspace(workspaceContext || fallbackWorkspace(kind === 'documents' ? 'documents' : 'issues'));
  rememberWorkspace();
  render();
  notify('已移至垃圾桶');
}
export async function reopen(kind, id, { saved = false, commentSent = false, owner = S.modal } = {}) {
  if (S.modal !== owner) return;
  const parent = nestedParent || (isObject(S.modal) ? captureObject() : null);
  if (commentSent && parent?.draft) parent.draft.comment = "";
  const pending = navigationIntent();
  if (!(await refreshNavigation(pending))) return;
  // Saving promotes a new document's identity; it is still the same object.
  if (saved) {
    returnedDrafts.delete(`${kind === "issues" ? "issue" : "document"}:${id}`);
    if (kind === "documents") returnedDrafts.delete(`document:new:${S.project}`);
    const record = get(kind, id);
    if (!record) throw Error("找不到已儲存的紀錄。");
    const history = await api("history/" + id);
    if (!isCurrentNavigation(pending)) return;
    nestedParent = null;
    restoreObject({ type: kind === "issues" ? "issue" : "document", record, history });
    return;
  }
  if (!saved && parent?.record.id === id && parent.type === (kind === "issues" ? "issue" : "document")) {
    const history = await api("history/" + id);
    if (!isCurrentNavigation(pending)) return;
    nestedParent = null;
    restoreObject({ ...parent, history });
    return;
  }
  nestedParent = null;
  render();
  if (kind === "issues") await openIssue(id);
  else await openDocument(id);
}
export async function action(a, { id, ids, kind, page, layout, status, issueDefaults } = {}) {
  if (a === "reload") {
    location.reload();
    return;
  }
  if (a === "retry-navigation") {
    if (retryNavigation) await retryNavigation();
    return;
  }
  if (a === "close") {
    closeDialog();
    return;
  }
  if (a === "back-object") return backObject();
  if (a === "trash-confirm") {
    const impact = await api(`trash/impact?kind=${encodeURIComponent(kind)}&id=${encodeURIComponent(id)}`);
    show({ type: "trash-confirm", kind, id, impact });
    return;
  }
  if (a === "trash-bulk-confirm") {
    const impact = await api('trash/impact', { kind: 'issues', ids });
    show({ type: 'trash-confirm', kind: 'issues', id: ids, impact });
    return;
  }
  if (a === "toggle-inspector") {
    if (window.innerWidth <= 1050) S.mobileInspector = !S.mobileInspector;
    else {
      S.inspector = !S.inspector;
      localStorage.setItem("lb.inspector", String(S.inspector));
    }
    render();
    return;
  }
  if (a === "menu") {
    S.menu = !S.menu;
    render();
    return;
  }
  if (a === "toggle-filters") {
    S.filtersOpen = !S.filtersOpen;
    rememberWorkspace();
    render();
    return;
  }
  if (a === "focus-search" || a === "search-issues") {
    if (a === "search-issues")
      await navigateWorkspace(() => {
        S.page = "issues";
        S.view = "all";
        S.q = S.category = S.status = S.milestone = "";
      });
    S.menu = false;
    S.filtersOpen = true;
    rememberWorkspace();
    render();
    requestAnimationFrame(() => document.getElementById("search")?.focus());
    return;
  }
  if (a === "nav" || a === "workspace-nav")
    return navigateWorkspace(() => {
      S.page = page;
      if (page === "issues") {
        S.view = "all";
        S.category = S.status = S.milestone = "";
      }
      S.q = "";
      S.selected = null;
      S.menu = false;
    });
  if (a === "view" || a === "all-view")
    return navigateWorkspace(() => {
      const view = id ? get("views", id) : null;
      if (id && (!view || view.archived)) throw Error("找不到此 View。");
      if (view) S.project = view.project_id;
      S.view = id || "all";
      S.page = "issues";
      S.q = "";
      S.category = S.status = S.milestone = "";
      S.selected = null;
      S.menu = false;
    });
  if (a === "layout") {
    S.layout = layout;
    localStorage.setItem("lb.layout", layout);
    rememberWorkspace();
    render();
    return;
  }
  if (a === "clear-filters") {
    S.q = S.category = S.status = S.milestone = "";
    rememberWorkspace();
    render();
    return;
  }
  if (a === "new-issue") return newIssue({ ...issueDefaults, ...(status === undefined ? {} : { status }) });
  if (a === "open-issue") return openIssue(id);
  if (a === "open-document") return openDocument(id);
  if (a === "new-document") return openDocument();
  if (a === "copy-link") {
    await navigator.clipboard.writeText(location.href);
    notify("已複製連結");
    return;
  }
  if (a === "upload") return show({ type: "upload", kind, id });
  if (a === "new-relation") return show({ type: "relation", id });
  if (a === "new-evidence") return editRecord("evidence", {}, { issue_id: id });
  if (a === "edit-record")
    return withLatestSnapshot(() => {
      const record = get(kind, id);
      if (!record) throw Error("找不到此紀錄。");
      editRecord(kind, record);
    });
  if (a === "edit-project")
    return withLatestSnapshot(() => editRecord("projects", project()));
  if (a === "edit-view")
    return withLatestSnapshot(() => editRecord("views", get("views", S.view)));
  const mapping = {
    "new-project": "projects",
    "new-team": "teams",
    "new-milestone": "milestones",
    "new-label": "labels",
    "new-view": "views",
    "new-batch": "batches",
    "new-dispatch": "dispatches",
  };
  if (mapping[a]) editRecord(mapping[a]);
}
export function selectProject(id) {
  requestedProject = id;
  return navigateWorkspace(() => { S.page = 'issues'; S.menu = false; });
}
export function setFilter(field, value) {
  S[field] = value;
  S.selected = null;
  rememberWorkspace();
  render();
}
export async function moveIssue(id, status) {
  try {
    await persist("issues", get("issues", id), { status });
    await refresh();
    render();
    notify("狀態已更新");
  } catch (error) {
    notify(error.message, true);
  }
}
export async function boot() {
  try {
    await refresh();
    caps = await api("capabilities");
    await routeHash({ fresh: false });
  } catch (error) {
    S.bootError = error.message;
    render();
  }
}
export function startNavigation() {
  const handler = () => routeHash();
  window.addEventListener("hashchange", handler);
  return () => window.removeEventListener("hashchange", handler);
}
async function routeHash({ fresh = true } = {}) {
  const pending = navigationIntent();
  try {
    if (fresh && !(await refreshNavigation(pending))) return;
    applyProjectSelection();
    const [type, id] = location.hash.replace(/^#\//, "").split("/");
    const saved = history.state?.linearboardWorkspace;
    if (type === "views" && id) {
      dismissDialog();
      const view = get("views", id);
      if (!view) {
        notify("找不到此 View。", true);
        return;
      }
      if (saved?.route === location.hash && saved.project === view.project_id)
        restoreWorkspace(saved);
      else
        restoreWorkspace({
          ...fallbackWorkspace("issues", view.project_id),
          view: id,
        });
      rememberWorkspace();
      render();
      return;
    }
    if (id) {
      const record = S.db[type] ? get(type, id) : null;
      if (!record) {
        dismissDialog();
        notify("紀錄已刪除或不存在。", true);
        return;
      }
      const page =
        type === "documents"
          ? "documents"
          : type === "milestones"
            ? "milestones"
            : ["batches", "dispatches"].includes(type)
              ? "delivery"
              : type === "projects"
                ? "overview"
                : ["teams", "labels"].includes(type)
                  ? "settings"
                  : "issues";
      workspaceContext ||=
        saved || fallbackWorkspace(page, record.project_id || S.project);
      if (record.project_id) S.project = record.project_id;
      if (["issues", "documents"].includes(type)) {
        S.page = type;
        render();
        if (type === "issues") await openIssue(id, { fresh: false });
        else await openDocument(id, { fresh: false });
        return;
      }
      dismissDialog();
      if (type === "projects") {
        S.project = id;
        S.page = "overview";
        rememberWorkspace();
        render();
        return;
      }
      if (type === "attachments" || type === "comments") {
        if (record.target_kind === "issues")
          return openIssue(record.target_id, { fresh: false });
        if (record.target_kind === "documents")
          return openDocument(record.target_id, { fresh: false });
      }
      if (type === "relations")
        return openIssue(record.source_id, { fresh: false });
      if (type === "evidence")
        return openIssue(record.issue_id, { fresh: false });
      S.page = page;
      render();
      if (["milestones", "batches", "dispatches"].includes(type))
        editRecord(type, record);
      return;
    }
    dismissDialog();
    const page = [
      "issues",
      "overview",
      "documents",
      "milestones",
      "delivery",
      "settings",
      "integration",
    ].includes(type)
      ? type
      : "issues";
    if (saved?.route === `#/${page}`) restoreWorkspace(saved);
    else
      restoreWorkspace({
        ...fallbackWorkspace(page),
        view: page === "issues" ? "all" : S.view,
      });
    rememberWorkspace();
    render();
  } catch (error) {
    if (isCurrentNavigation(pending))
      navigationFailure(error, () => routeHash());
  }
}

export {
  api,
  refresh,
  closeDialog,
  navigateWorkspace,
  teamStatuses,
  defaultStatus,
  list,
  get,
  project,
  labelName,
  milestoneName,
  dismissDialog,
};
