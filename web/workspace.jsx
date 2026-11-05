import React, { useEffect, useState, useLayoutEffect, useRef } from "react";
import {
  S,
  list,
  get,
  project,
  selectProject,
  navigateWorkspace,
  notify,
} from "./model.js";
import { Button, Icon } from "./ui.jsx";
const projectPages = [
  ["overview", "總覽", "folder"],
  ["issues", "任務", "layout-list"],
  ["documents", "文件", "file-text"],
  ["milestones", "里程碑", "flag"],
];
function ProjectTabs({ inspectorOpen }) {
  const scroll = useRef();
  useLayoutEffect(() => {
    const reveal = () =>
      scroll.current
        ?.querySelector('[aria-current="page"]')
        ?.scrollIntoView({ block: "nearest", inline: "nearest" });
    reveal();
    const observer = new ResizeObserver(reveal);
    observer.observe(scroll.current);
    return () => observer.disconnect();
  }, [S.page, S.view]);
  return (
    <nav className="project-tabs" aria-label="專案分頁">
      <div className="project-tab-scroll" ref={scroll}>
        {projectPages.map(([page, name, icon]) => (
          <Button
            key={page}
            action="nav"
            page={page}
            icon={icon}
            className={
              "project-tab" +
              (S.page === page && (page !== "issues" || S.view === "all")
                ? " active"
                : "")
            }
            aria-current={
              S.page === page && (page !== "issues" || S.view === "all")
                ? "page"
                : undefined
            }
          >
            {name}
          </Button>
        ))}
        {list("views")
          .filter((v) => v.placement === "tabs")
          .map((v) => (
            <Button
              key={v.id}
              action="view"
              id={v.id}
              icon="columns-3"
              className={
                "project-tab" +
                (S.page === "issues" && S.view === v.id ? " active" : "")
              }
              aria-current={
                S.page === "issues" && S.view === v.id ? "page" : undefined
              }
            >
              {v.name.replace(project().name + "-", "")}
            </Button>
          ))}
        <Button
          action="new-view"
          icon="plus"
          aria-label="新增分頁 View"
          className="icon-button"
        />
      </div>
      <div className="project-tab-tools">
        {S.page === "issues" && (
          <>
            <Button
              action="focus-search"
              icon="search"
              aria-label="搜尋目前任務"
              className="icon-button"
            />
            <Button
              action="toggle-filters"
              icon="list-filter"
              aria-label="篩選任務"
              aria-expanded={Boolean(S.filtersOpen)}
              className="icon-button"
            />
            <Button
              action="layout"
              layout="list"
              icon="layout-list"
              aria-label="清單檢視"
              className={
                "icon-button" + (S.layout === "list" ? " selected" : "")
              }
            />
            <Button
              action="layout"
              layout="board"
              icon="columns-3"
              aria-label="看板檢視"
              className={
                "icon-button" + (S.layout === "board" ? " selected" : "")
              }
            />
          </>
        )}

        {S.page === "issues" && S.view !== "all" && (
          <><Button
            action="edit-view"
            icon="settings-2"
            aria-label="編輯目前 View"
            className="icon-button"
          /><Button action="trash-confirm" kind="views" id={S.view} icon="trash" aria-label="刪除目前 View" className="icon-button" /></>
        )}
        <Button
          action="toggle-inspector"
          icon="panel-right"
          aria-label={inspectorOpen ? "收合專案資訊" : "顯示專案資訊"}
          aria-expanded={inspectorOpen}
          className={"icon-button" + (inspectorOpen ? " selected" : "")}
        />
      </div>
    </nav>
  );
}
export function ProjectInspector() {
  const p = project(),
    issues = list("issues"),
    done = issues.filter((i) => i.status === "Done").length,
    review = issues.filter((i) => i.status === "In Review").length;
  const milestoneIssues = (m) => issues.filter((i) => i.milestone_id === m.id);
  const showMilestone = (id) =>
    navigateWorkspace(() => {
      S.page = "issues";
      S.view = "all";
      S.milestone = id;
      S.filtersOpen = true;
      S.q = S.category = S.status = "";
    });
  return (
    <aside className="project-inspector" aria-label="專案資訊">
      <details className="inspector-section" open>
        <summary>專案屬性</summary>
        <div className="inspector-properties">
          <span>團隊</span>
          <strong>{get("teams", p.team_id)?.name}</strong>
          <span>任務</span>
          <strong>{issues.length}</strong>
          <span>待審閱</span>
          <strong>{review}</strong>
          <span>已驗收</span>
          <strong>{done} / {issues.length}</strong>
        </div>
      </details>
      {!["milestones", "overview"].includes(S.page) && <details className="inspector-section" open>
        <summary>里程碑</summary>
        <div className="inspector-milestones">
          {list("milestones").map((m) => {
            const rows = milestoneIssues(m),
              count = rows.filter((i) => i.status === "Done").length;
            return (
              <button
                type="button"
                key={m.id}
                onClick={() => showMilestone(m.id)}
                className="inspector-milestone"
              >
                <Icon name="flag" />
                <span>{m.name}</span>
                <small>
                  {count}/{rows.length}
                </small>
              </button>
            );
          })}
          {!list("milestones").length && (
            <span className="small muted">尚無里程碑</span>
          )}
        </div>
        <Button
          action="new-milestone"
          icon="plus"
          className="quiet inspector-add"
        >
          新增里程碑
        </Button>
      </details>}
    </aside>
  );
}
export function Shell({ children }) {
  const [narrow, setNarrow] = useState(() => window.innerWidth <= 1050);
  useEffect(() => {
    const media = window.matchMedia("(max-width:1050px)");
    const update = () => setNarrow(media.matches);
    media.addEventListener("change", update);
    return () => media.removeEventListener("change", update);
  }, []);
  const inspectorOpen = narrow ? Boolean(S.mobileInspector) : S.inspector;
  const p = project(),
    team = get("teams", p?.team_id),
    projectContext = p && !["settings", "integration"].includes(S.page);
  return (
    <>
      <aside id="workspace-navigation" className={"sidebar" + (S.menu ? " mobile-open" : "")}>
        <div className="workspace-brand">
          <span className="brand-mark">
            <Icon name="layers" />
          </span>
          <strong>LinearBoard</strong>
          <div className="brand-actions">
            <Button
              action="search-issues"
              icon="search"
              aria-label="前往任務搜尋"
              className="icon-button"
            />
          </div>
        </div>
        <div className="team-name">
          <Icon name="circle" />
          <span>{team?.name || "個人工作區"}</span>
        </div>
        <div className="sidebar-project-title">
          <span>專案</span>
          <Button
            action="new-project"
            icon="plus"
            aria-label="建立專案"
            className="icon-button"
          />
        </div>
        <nav className="project-list" aria-label="專案清單">
          {S.db.projects.filter(item => !item.archived).map(item => <div key={item.id} className="project-list-group">
          <div className={'project-list-row' + (S.project === item.id ? ' active' : '')}>
          <button type="button" className="project-list-item" data-project-id={item.id}
            aria-current={S.project === item.id ? 'page' : undefined} title={item.name}
            onClick={() => selectProject(item.id).catch(error => notify(error.message, true))}>
            <Icon name="boxes" /><span>{item.name}</span>
          </button>
          <Button
            action="trash-confirm"
            kind="projects"
            id={item.id}
            icon="trash"
            aria-label={'刪除專案 ' + item.name}
            title={'刪除專案 ' + item.name}
            className="icon-button project-delete"
          />
          </div>
          {S.project === item.id && <div className="project-tools">
          <Button action="nav" page="delivery" icon="git-branch"
            className={"nav-item" + (S.page === "delivery" ? " active" : "")}
            aria-current={S.page === "delivery" ? "page" : undefined}>
            交付
          </Button>
          </div>}
          </div>)}
        </nav>
        {list("views").some((v) => v.placement === "shared") && <div className="sidebar-heading">
          共享 Views{" "}
          <Button
            action="new-view"
            icon="plus"
            aria-label="建立 View"
            className="icon-button"
          />
        </div>}
        <div className="saved-views">
          {list("views")
            .filter((v) => v.placement === "shared")
            .map((v) => (
              <Button
                key={v.id}
                action="view"
                id={v.id}
                icon="list-filter"
                className={
                  "nav-item" +
                  (S.view === v.id && S.page === "issues" ? " active" : "")
                }
              >
                {v.name}
              </Button>
            ))}
        </div>
        <div className="sidebar-bottom">
          <Button
            action="nav"
            page="settings"
            icon="settings-2"
            className="nav-item"
          >
            工作區設定
          </Button>
        </div>
      </aside>
      <main className="workspace-frame">
        <header className="topbar">
          <Button
            action="menu"
            icon={S.menu ? "x" : "menu"}
            aria-label={S.menu ? "關閉導覽" : "開啟導覽"}
            aria-expanded={Boolean(S.menu)}
            aria-controls="workspace-navigation"
            className="icon-button mobile-only navigation-toggle"
          />
          <div className="breadcrumb">
            <span className="breadcrumb-team">{team?.name || "工作區"}</span>
            <Icon name="chevron-right" />
            <Icon name="boxes" />
            <b>{p?.name || "LinearBoard"}</b>
          </div>
          <div className="top-actions">
            {!projectContext && p && (
              <Button
                action="nav"
                page="issues"
                icon="arrow-left"
                className="quiet compact"
              >
                返回專案
              </Button>
            )}

            <Button
              action="new-issue"
              icon="plus"
              className="quiet compact"
              aria-label="在專案新增任務"
            >
              新增任務
            </Button>
          </div>
        </header>
        {projectContext && <ProjectTabs inspectorOpen={inspectorOpen} />}
        <div className="workspace-body">
          <div className={"workspace-content page-" + S.page}>{children}</div>
          {projectContext && inspectorOpen && <ProjectInspector />}
        </div>
      </main>
    </>
  );
}
