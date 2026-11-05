import React, { useEffect, useRef, useState } from "react";
import * as ContextMenu from "@radix-ui/react-context-menu";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { S, api, action, render, refresh, notify, get, list, teamStatuses, filteredIssues, milestoneName, setFilter, moveIssue } from "./model.js";
import { cats, statusClass, statusLabel, stamp } from "./labels.js";
import { Button, Icon, StatusIcon, Picker, Empty } from "./ui.jsx";

const menuClass = "action-menu";

function StatusMenu({ parts: M, ids, busy, onStatus }) {
  return (
    <M.Sub>
      <M.SubTrigger className="menu-item" disabled={busy || !ids.length}>
        <Icon name="circle-dot" />變更狀態<Icon name="chevron-right" />
      </M.SubTrigger>
      <M.Portal>
        <M.SubContent className={menuClass + " status-submenu"} sideOffset={5} collisionPadding={10}>
          {teamStatuses().map(status => (
            <M.Item key={status} className="menu-item" onSelect={() => onStatus(ids, status)}>
              <span className={"status-symbol " + statusClass(status)}><StatusIcon status={status} /></span>
              {statusLabel(status)}
              {ids.every(id => get("issues", id)?.status === status) && <Icon name="check" />}
            </M.Item>
          ))}
        </M.SubContent>
      </M.Portal>
    </M.Sub>
  );
}

function GroupMenuItems({ parts: M, collapsed, allCollapsed, disabled, empty, onToggle, onAllToggle, onSelectAll, onHide }) {
  return <>
    <M.Item className="menu-item" onSelect={onToggle} disabled={disabled}>
      {collapsed ? "展開群組" : "收合群組"}
    </M.Item>
    <M.Item className="menu-item" onSelect={onAllToggle} disabled={disabled}>
      {allCollapsed ? "展開全部群組" : "收合全部群組"}
    </M.Item>
    <M.Separator className="menu-separator" />
    <M.Item className="menu-item" onSelect={onSelectAll} disabled={disabled || empty}>
      全選此群組
    </M.Item>
    <M.Item className="menu-item" onSelect={onHide} disabled={disabled}>隱藏群組</M.Item>
  </>;
}

function IssueRow({ record: r, selected, selectedIds, busy, onToggle, onSelectOnly, onStatus }) {
  const [labelsExpanded, setLabelsExpanded] = useState(false);
  const ids = selected ? selectedIds : [r.id];
  const milestone = r.milestone_id ? milestoneName(r.milestone_id) : '';
  const milestoneLabel = milestone.match(/^M\d+(?=\s|[—·-]|$)/i)?.[0] || milestone;
  const labels = (r.label_ids || []).map(id => get('labels', id)).filter(label =>
    label && !label.is_group && get('labels', label.parent_id)?.name !== 'Category' && label.name !== milestoneLabel);
  return (
    <ContextMenu.Root>
      <ContextMenu.Trigger asChild>
        <div className={"issue-entry" + (selected ? " is-selected" : "")}
          data-selected={selected || undefined}
          onContextMenu={() => { if (!selected) onSelectOnly(r.id); }}>
          <label className="issue-selection-area">
          <input type="checkbox" className="issue-checkbox"
            aria-label={"選取 " + r.identifier} checked={selected} disabled={busy}
            onChange={() => onToggle(r.id)} />
          </label>
          <Button action="open-issue" id={r.id} className="issue-row" disabled={busy}
            draggable={S.layout === "board" && !busy}
            onDragStart={e => {
              e.dataTransfer.setData("text/plain", r.id);
              e.dataTransfer.effectAllowed = "move";
            }}>
            <span className={"status-symbol " + statusClass(r.status)}><StatusIcon status={r.status} /></span>
            <span className="identifier">{r.identifier}</span>
            <strong>{r.title}</strong>
            <span className="row-meta">
              {get("views", S.view)?.category !== r.category && <span className={"badge cat-" + r.category}>{cats[r.category]}</span>}
              {milestone && <span className="badge milestone-tag" title={milestone}>{milestoneLabel}</span>}
              {(labelsExpanded ? [] : labels.slice(0, 3)).map(label => <span key={label.id} className="badge custom-label" title={label.name}>{label.name}</span>)}
              <span className="small muted">{stamp(r.updated_at)}</span>
            </span>
          </Button>
          {labels.length > 3 && <button type="button" className="quiet issue-label-toggle"
            aria-label={(labelsExpanded ? '收合 ' : '展開 ') + r.identifier + ' 標籤'}
            aria-expanded={labelsExpanded} disabled={busy}
            onClick={event => { event.stopPropagation(); setLabelsExpanded(value => !value); }}>
            {labelsExpanded ? '收合' : `+${labels.length - 3}`}
          </button>}
          {labelsExpanded && labels.length > 3 && <div className="issue-labels-expanded" role="group" aria-label={r.identifier + ' 所有標籤'}>
            {labels.map(label => <span key={label.id} className="badge" title={label.name}>{label.name}</span>)}
          </div>}
        </div>
      </ContextMenu.Trigger>
      <ContextMenu.Portal>
        <ContextMenu.Content className={menuClass} collisionPadding={10}>
          <ContextMenu.Label className="menu-label">{ids.length} 個任務</ContextMenu.Label>
          <StatusMenu parts={ContextMenu} ids={ids} busy={busy} onStatus={onStatus} />
          <ContextMenu.Separator className="menu-separator" />
          <ContextMenu.Item className="menu-item" disabled={busy} onSelect={() => {
            setTimeout(() => action("open-issue", { id: r.id }).catch(error => notify(error.message, true)), 0);
          }}><Icon name="arrow-up-right" />開啟任務</ContextMenu.Item>
          <ContextMenu.Item className="menu-item" onSelect={() => {
            navigator.clipboard.writeText(new URL(r.url, location.origin).href)
              .then(() => notify("已複製連結"), error => notify(error.message, true));
          }}><Icon name="link-2" />複製任務連結</ContextMenu.Item>
          <ContextMenu.Item className="menu-item" disabled={busy} onSelect={() => {
            setTimeout(() => action(ids.length > 1 ? 'trash-bulk-confirm' : 'trash-confirm', ids.length > 1 ? { ids } : { kind: 'issues', id: r.id }).catch(error => notify(error.message, true)), 0);
          }}><Icon name="trash" />刪除</ContextMenu.Item>
        </ContextMenu.Content>
      </ContextMenu.Portal>
    </ContextMenu.Root>
  );
}

export default function Issues() {
  const [selected, setSelected] = useState(() => new Set());
  const [collapsed, setCollapsed] = useState(() => new Set());
  const [hidden, setHidden] = useState(() => new Set());
  const [busy, setBusy] = useState(false);
  const busyRef = useRef(false);
  const mounted = useRef(true);
  useEffect(() => () => { mounted.current = false; }, []);
  const contextKey = JSON.stringify([S.project, S.view, S.category, S.status, S.milestone, S.q]);
  const context = useRef(contextKey);
  context.current = contextKey;
  useEffect(() => {
    setSelected(new Set());
    setCollapsed(new Set());
    setHidden(new Set());
  }, [contextKey]);
  const rows = filteredIssues(),
    v = get("views", S.view),
    group = v?.group_by || "status";
  const groups =
    group === "status"
      ? [
          ...new Set([
            ...teamStatuses(),
            ...rows.map((r) => r.status).filter(Boolean),
          ]),
        ].sort((a, b) => {
          const rank = status => status === "Done" ? 0 : status === "Todo" ? 2 : status === "Backlog" ? 3 : 1;
          return rank(a) - rank(b);
        })
      : group === "category"
        ? S.db.categories
        : group === "priority"
          ? ["Urgent", "High", "Medium", "Low", "No priority"]
          : ["", ...list("milestones").map((m) => m.id)];
  const groupName = (k) =>
    group === "status"
      ? statusLabel(k)
      : group === "category"
        ? cats[k]
        : group === "milestone_id"
          ? milestoneName(k)
          : k;
  const matchingGroups = groups.filter(k => S.layout === "board" || rows.some(r => (r[group] || "") === k));
  const shownGroups = matchingGroups.filter(k => !hidden.has(k));
  const availableRows = rows.filter(r => !hidden.has(r[group] || ""));
  const selectedIds = availableRows.filter(r => selected.has(r.id)).map(r => r.id);
  const availableKey = availableRows.map(r => r.id).join(",");
  useEffect(() => {
    const available = new Set(availableKey.split(","));
    setSelected(previous => {
      const next = new Set([...previous].filter(id => available.has(id)));
      return next.size === previous.size ? previous : next;
    });
  }, [availableKey]);
  const toggleSelection = id => setSelected(previous => {
    const next = new Set(previous);
    next.has(id) ? next.delete(id) : next.add(id);
    return next;
  });
  const toggleGroup = key => setCollapsed(previous => {
    const next = new Set(previous);
    next.has(key) ? next.delete(key) : next.add(key);
    return next;
  });
  const allCollapsed = shownGroups.length > 0 && shownGroups.every(k => collapsed.has(k));
  async function changeStatus(ids, status) {
    if (busyRef.current || !ids.length) return;
    busyRef.current = true;
    setBusy(true);
    const origin = context.current;
    const expected_versions = Object.fromEntries(ids.map(id => [id, get("issues", id).version]));
    try {
      const result = await api("issues/bulk-status", { issue_ids: ids, expected_versions, status });
      await refresh();
      render();
      notify(result.updated ? `已更新 ${result.updated} 個任務的狀態。` : "選取的任務已是此狀態。");
    } catch (error) {
      try { await refresh(); render(); } catch { /* The original error remains actionable. */ }
      notify(error.message, true);
    } finally {
      busyRef.current = false;
      setBusy(false);
      requestAnimationFrame(() => {
        if (mounted.current && origin === context.current && S.page === "issues")
          (document.querySelector(".bulk-actions-trigger") || document.querySelector('.project-tab[aria-current="page"]'))?.focus();
      });
    }
  }
  return (
    <>
      <section className="issues-page">
        <h1 className="visually-hidden">
          {v?.name || "所有任務"}
        </h1>
        {selectedIds.length > 0 && <div className="selection-bar" aria-label="已選取任務" aria-busy={busy}>
          <strong aria-live="polite">已選取 {selectedIds.length} 個任務</strong>
          <DropdownMenu.Root>
            <DropdownMenu.Trigger className="quiet compact bulk-actions-trigger" disabled={busy}>
              {busy ? "更新中…" : "動作"}<Icon name="chevron-down" />
            </DropdownMenu.Trigger>
            <DropdownMenu.Portal>
              <DropdownMenu.Content className={menuClass} sideOffset={5} collisionPadding={10}>
                <StatusMenu parts={DropdownMenu} ids={selectedIds} busy={busy} onStatus={changeStatus} />
                <DropdownMenu.Separator className="menu-separator" />
                <DropdownMenu.Item className="menu-item" disabled={busy} onSelect={() => {
                  setTimeout(() => action('trash-bulk-confirm', { ids: selectedIds }).catch(error => notify(error.message, true)), 0);
                }}><Icon name="trash" />刪除</DropdownMenu.Item>
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>
          <button type="button" className="icon-button" aria-label="取消選取" disabled={busy} onClick={() => setSelected(new Set())}><Icon name="x" /></button>
        </div>}
        <div className="filters" hidden={!S.filtersOpen}>
          <label className="search-field">
            <Icon name="search" />
            <input
              id="search"
              placeholder="搜尋任務…"
              aria-label="搜尋任務"
              value={S.q}
              onChange={(e) => setFilter("q", e.target.value)}
            />
            <kbd>/</kbd>
          </label>
          <Picker
            id="filter-category"
              aria-label="篩選類別"
            value={S.category}
            onValueChange={(value) => setFilter("category", value)}
              items={S.db.categories.map((c) => ({ id: c, name: cats[c] }))}
              blank="所有類別"
          />
          <Picker
            id="filter-status"
            aria-label="篩選狀態"
            value={S.status}
            onValueChange={(value) => setFilter("status", value)}
              items={teamStatuses().map((s) => ({
                id: s,
                name: statusLabel(s),
              }))}
              blank="所有狀態"
          />
          <Picker
            id="filter-milestone"
            aria-label="篩選里程碑"
            value={S.milestone}
            onValueChange={(value) => setFilter("milestone", value)}
            items={list("milestones")} blank="所有里程碑"
          />
          {(S.q || S.category || S.status || S.milestone) && (
            <Button action="clear-filters" icon="x" className="quiet">
              清除
            </Button>
          )}
          <span className="filter-spacer" />
          <span className="small muted desktop-only">
            <Icon name="sliders-horizontal" />依{" "}
            {
              {
                status: "狀態",
                category: "類別",
                milestone_id: "里程碑",
                priority: "優先級",
              }[group]
            }{" "}
            分組
          </span>
        </div>
        <div className={"results " + (S.layout === "board" ? "board" : "list")}>
          {rows.length > 0 && !shownGroups.length && <Empty title="所有群組皆已隱藏" />}
          {rows.length ? (
            shownGroups.map((k) => (
                <section
                  key={k}
                  className="issue-group"
                  data-drop-status={
                    S.layout === "board" && group === "status" ? k : undefined
                  }
                  onDragOver={(e) => {
                    if (group === "status") {
                      e.preventDefault();
                      e.dataTransfer.dropEffect = "move";
                    }
                  }}
                  onDrop={(e) => {
                    if (group === "status") {
                      e.preventDefault();
                      moveIssue(e.dataTransfer.getData("text/plain"), k);
                    }
                  }}
                >
                  <ContextMenu.Root>
                    <ContextMenu.Trigger asChild>
                      <div className="group-heading" data-group={k}>
                        <button type="button" className="quiet group-toggle" aria-expanded={!collapsed.has(k)}
                          aria-label={(collapsed.has(k) ? "展開" : "收合") + groupName(k) + "群組"} onClick={() => toggleGroup(k)}>
                          <Icon name="chevron-right" />
                          <span className={"status-symbol " + statusClass(k)}>
                            {group === "status" ? <StatusIcon status={k} /> : <Icon name="circle" />}
                          </span>
                          <strong>{groupName(k)}</strong>
                          <span className="count">{rows.filter(r => (r[group] || "") === k).length}</span>
                        </button>
                        <DropdownMenu.Root>
                          <DropdownMenu.Trigger className="icon-button group-menu-trigger" aria-label={groupName(k) + "群組選單"}>
                            <Icon name="more-horizontal" />
                          </DropdownMenu.Trigger>
                          <DropdownMenu.Portal>
                            <DropdownMenu.Content className={menuClass} sideOffset={5} collisionPadding={10}>
                              <GroupMenuItems parts={DropdownMenu} collapsed={collapsed.has(k)} allCollapsed={allCollapsed} disabled={busy} empty={!rows.some(r => (r[group] || "") === k)}
                                onToggle={() => toggleGroup(k)} onAllToggle={() => setCollapsed(allCollapsed ? new Set() : new Set(shownGroups))}
                                onSelectAll={() => setSelected(new Set(rows.filter(r => (r[group] || "") === k).map(r => r.id)))}
                                onHide={() => setHidden(previous => new Set([...previous, k]))} />
                            </DropdownMenu.Content>
                          </DropdownMenu.Portal>
                        </DropdownMenu.Root>
                        <Button action="new-issue" icon="plus" status={group === "status" ? k : undefined}
                          issueDefaults={{ [group]: k }} aria-label={"在" + groupName(k) + "新增任務"} className="icon-button" />
                      </div>
                    </ContextMenu.Trigger>
                    <ContextMenu.Portal>
                      <ContextMenu.Content className={menuClass} collisionPadding={10}>
                        <GroupMenuItems parts={ContextMenu} collapsed={collapsed.has(k)} allCollapsed={allCollapsed} disabled={busy} empty={!rows.some(r => (r[group] || "") === k)}
                          onToggle={() => toggleGroup(k)} onAllToggle={() => setCollapsed(allCollapsed ? new Set() : new Set(shownGroups))}
                          onSelectAll={() => setSelected(new Set(rows.filter(r => (r[group] || "") === k).map(r => r.id)))}
                          onHide={() => setHidden(previous => new Set([...previous, k]))} />
                      </ContextMenu.Content>
                    </ContextMenu.Portal>
                  </ContextMenu.Root>
                  <div className="group-items" hidden={collapsed.has(k)}>
                    {rows
                      .filter((r) => (r[group] || "") === k)
                      .map((r) => (
                        <IssueRow key={r.id} record={r} selected={selected.has(r.id)} selectedIds={selectedIds} busy={busy}
                          onToggle={toggleSelection} onSelectOnly={id => setSelected(new Set([id]))} onStatus={changeStatus} />
                      ))}
                    {S.layout === "board" && (
                      <Button
                        action="new-issue"
                        status={group === "status" ? k : undefined}
                        issueDefaults={{ [group]: k }}
                        icon="plus"
                        className="board-add"
                      >
                        新增任務
                      </Button>
                    )}
                  </div>
                </section>
              ))
          ) : (
            <Empty
              title="沒有符合的任務"
              detail={
                S.q || S.category || S.status || S.milestone
                  ? "調整篩選條件，或清除搜尋。"
                  : undefined
              }
            />
          )}
        </div>
        <footer className="results-footer">
          <span>{rows.length} 個任務</span>
          {hidden.size > 0 && <button type="button" className="quiet compact" onClick={() => setHidden(new Set())}>顯示隱藏的群組（{hidden.size}）</button>}
        </footer>
      </section>
    </>
  );
}
