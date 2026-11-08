import { t } from "./i18n.js";
import React, { useLayoutEffect, useRef, useState, useId } from "react";
import { marked } from "marked";
import DOMPurify from "dompurify";
import * as SelectPrimitive from "@radix-ui/react-select";
import { approvalOptions } from "./labels.js";
import {
  Layers,
  Search,
  Plus,
  ChevronRight,
  Circle,
  CircleDashed,
  CircleDot,
  CircleX,
  Copy,
  FlaskConical,
  CheckCircle2,
  Clock3,
  LayoutList,
  Columns3,
  SlidersHorizontal,
  FileText,
  Flag,
  Settings2,
  X,
  ArrowUpRight,
  Link2,
  Paperclip,
  History,
  Terminal,
  Folder,
  Menu,
  Download,
  Send,
  Boxes,
  ListFilter,
  GitBranch,
  ChevronDown,
  PanelRight,
  ArrowLeft,
  MoreHorizontal,
  Check,
  Trash2,
} from "lucide-react";
import {
  action,
  notify,
  S,
  list,
  get,
  project,
  teamStatuses,
  persist,
  refresh,
  render,
} from "./model.js";
const icons = {
  layers: Layers,
  search: Search,
  plus: Plus,
  "chevron-right": ChevronRight,
  circle: Circle,
  "circle-dashed": CircleDashed,
  "circle-dot": CircleDot,
  "circle-x": CircleX,
  copy: Copy,
  "flask-conical": FlaskConical,
  "check-circle-2": CheckCircle2,
  "clock-3": Clock3,
  "layout-list": LayoutList,
  "columns-3": Columns3,
  "sliders-horizontal": SlidersHorizontal,
  "file-text": FileText,
  flag: Flag,
  "settings-2": Settings2,
  x: X,
  "arrow-up-right": ArrowUpRight,
  "link-2": Link2,
  paperclip: Paperclip,
  history: History,
  terminal: Terminal,
  folder: Folder,
  menu: Menu,
  download: Download,
  send: Send,
  boxes: Boxes,
  "list-filter": ListFilter,
  "git-branch": GitBranch,
  "chevron-down": ChevronDown,
  "panel-right": PanelRight,
  "arrow-left": ArrowLeft,
  "more-horizontal": MoreHorizontal,
  check: Check,
  trash: Trash2,
};
export function Icon({ name }) {
  const Component = icons[name] || Circle;
  return <Component aria-hidden="true" />;
}
const statusIcons = new Map([
  ["In Review", "clock-3"],
  ["Ready for Test", "flask-conical"],
  ["Todo", "circle-dot"],
  ["Backlog", "circle-dashed"],
  ["Done", "check-circle-2"],
  ["Canceled", "circle-x"],
  ["Blocked", "circle-x"],
  ["Duplicate", "copy"],
]);
export function StatusIcon({ status }) {
  if (status === "In Progress") {
    return <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
      <circle cx="12" cy="12" r="9" />
      <path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor" stroke="none" />
    </svg>;
  }
  return <Icon name={statusIcons.get(status) || "circle"} />;
}
export function Button({
  action: name,
  children,
  icon,
  className = "",
  id,
  kind,
  page,
  layout,
  status,
  issueDefaults,
  ...props
}) {
  return (
    <button
      type="button"
      className={className}
      data-action={name}
      data-id={id}
      data-kind={kind}
      data-page={page}
      data-layout={layout}
      data-status={status}
      onClick={() =>
        action(name, { id, kind, page, layout, status, issueDefaults }).catch((error) =>
          notify(error.message, true),
        )
      }
      {...props}
    >
      {icon && <Icon name={icon} />} {children}
    </button>
  );
}
export function Markdown({ body = "", className = "", ...props }) {
  const html = DOMPurify.sanitize(marked.parse(body), {
    ADD_ATTR: ["target"],
    FORBID_TAGS: ["style", "iframe", "form"],
  });
  return (
    <div
      className={"markdown " + className}
      dangerouslySetInnerHTML={{ __html: html }}
      {...props}
    />
  );
}
export function Picker({ name, items = [], value, defaultValue, blank = "", placeholder = "", onValueChange,
  disabled, required, className = "", ...props }) {
  const trigger = useRef();
  const [container, setContainer] = useState();
  const options = items.map(item => typeof item === "string"
    ? { id: item, name: item } : { ...item, name: item.name || item.title });
  if (blank) options.unshift({ id: "", name: blank });
  const initial = options.some(item => item.id === defaultValue)
    ? defaultValue : options[0]?.id ?? "";
  const [localValue, setLocalValue] = useState(initial);
  const selected = value !== undefined ? value ?? "" : localValue;
  // Native dialogs occupy the top layer; their popups must stay inside that dialog.
  useLayoutEffect(() => { setContainer(trigger.current?.closest("dialog") || undefined); }, []);
  return (
    <SelectPrimitive.Root name={name} value={selected} required={required}
      disabled={disabled || !options.length}
      onValueChange={next => {
        if (value === undefined) setLocalValue(next);
        onValueChange?.(next);
      }}>
      <SelectPrimitive.Trigger ref={trigger} className={"select-trigger " + className}
        data-value={selected} {...props}>
        <SelectPrimitive.Value placeholder={placeholder || blank || t("請選擇")} />
        <SelectPrimitive.Icon className="select-chevron"><Icon name="chevron-down" /></SelectPrimitive.Icon>
      </SelectPrimitive.Trigger>
      <SelectPrimitive.Portal container={container}>
        <SelectPrimitive.Content className="action-menu select-menu" position="popper"
          align="start" sideOffset={5} collisionPadding={10}>
          <SelectPrimitive.ScrollUpButton className="select-scroll select-scroll-up"><Icon name="chevron-down" /></SelectPrimitive.ScrollUpButton>
          <SelectPrimitive.Viewport className="select-viewport">
            {options.map(item => (
              <SelectPrimitive.Item key={item.id} value={item.id} disabled={item.disabled}
                className="menu-item select-option" data-value={item.id} textValue={item.name}>
                <SelectPrimitive.ItemText className="select-option-text">{item.name}</SelectPrimitive.ItemText>
                <SelectPrimitive.ItemIndicator className="select-check"><Icon name="check" /></SelectPrimitive.ItemIndicator>
              </SelectPrimitive.Item>
            ))}
          </SelectPrimitive.Viewport>
          <SelectPrimitive.ScrollDownButton className="select-scroll"><Icon name="chevron-down" /></SelectPrimitive.ScrollDownButton>
        </SelectPrimitive.Content>
      </SelectPrimitive.Portal>
    </SelectPrimitive.Root>
  );
}
export function Select({ name, items, value = "", blank = "", ...props }) {
  return <Picker name={name} items={items} defaultValue={value ?? ""} blank={blank} {...props} />;
}
export function Field({ label, children }) {
  const id = useId();
  const labelable =
    React.isValidElement(children) &&
    [Input, Area, Select, Picker, "input", "textarea", "select"].includes(
      children.type,
    );
  if (labelable) {
    const controlId = children.props.id || id;
    return (
      <label className="field" htmlFor={controlId}>
        <span>{label}</span>
        {React.cloneElement(children, { id: controlId })}
      </label>
    );
  }
  return (
    <div className="field">
      <span id={id}>{label}</span>
      <div role="group" aria-labelledby={id}>
        {children}
      </div>
    </div>
  );
}
export function Input({ name, value = "", ...props }) {
  return <input name={name} defaultValue={value ?? ""} {...props} />;
}
export function Area({ name, value = "", rows = 6, ...props }) {
  return (
    <textarea name={name} defaultValue={value ?? ""} rows={rows} {...props} />
  );
}
export function MilestoneField({ record }) {
  return (
    <Field label={t("里程碑")}>
      <Select
        name="milestone_id"
        items={list("milestones")}
        value={record.milestone_id}
        blank={t("無里程碑")}
      />
    </Field>
  );
}
export function LabelsSelect({ selected = [] }) {
  const labels = S.db.labels.filter(
    (l) =>
      !l.archived &&
      !l.is_group &&
      l.team_id === project()?.team_id &&
      get("labels", l.parent_id)?.name !== "Category",
  );
  return (
    <div className="checkbox-grid labels-select">
      {labels.map((l) => (
        <label key={l.id}>
          <input
            type="checkbox"
            name="label_ids"
            value={l.id}
            defaultChecked={selected.includes(l.id)}
          />
          {l.name}
        </label>
      ))}
      {!labels.length && (
        <span className="muted small">{t("在工作區設定新增 M／US 或角色標籤。")}</span>
      )}
    </div>
  );
}
export function Empty({ title, detail }) {
  return (
    <div className="empty">
      <span>
        <Icon name="circle" />
      </span>
      <h3>{title}</h3>
      {detail && <p>{detail}</p>}
    </div>
  );
}
export function IssueChip({ id, showTitle = false }) {
  const r = get("issues", id);
  return r ? (
    <Button action="open-issue" id={id} icon="circle" className="issue-chip">
      {r.identifier}
      {showTitle ? " " + r.title : ""}
    </Button>
  ) : null;
}
const isPreviewImage = a => !a.external_url && ["image/png", "image/jpeg"].includes(a.mime);

export function AttachmentSections({ records, kind, id, children }) {
  const strip = useRef();
  const [edges, setEdges] = useState({ previous: false, next: false });
  const visuals = records.filter(isPreviewImage), files = records.filter(a => !isPreviewImage(a));
  const updateEdges = () => {
    const el = strip.current;
    if (el) setEdges({ previous: el.scrollLeft > 2, next: el.scrollLeft + el.clientWidth < el.scrollWidth - 2 });
  };
  useLayoutEffect(() => {
    const el = strip.current;
    if (!el) return;
    updateEdges();
    const observer = new ResizeObserver(updateEdges);
    observer.observe(el);
    return () => observer.disconnect();
  }, [visuals.length]);
  const move = direction => {
    const el = strip.current;
    const step = el.querySelector('.reference-card')?.getBoundingClientRect().width || el.clientWidth;
    el.scrollBy({ left: direction * (step + 16), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  };
  return <>
    <section className="detail-section visual-references">
      <div className="section-title">
        <h3>{t("視覺參考")}</h3>
        <div className="reference-actions">
          {visuals.length > 0 && <>
            <button type="button" className="icon-button reference-previous" aria-label={t("上一個視覺參考")} disabled={!edges.previous} onClick={() => move(-1)}><Icon name="chevron-right" /></button>
            <button type="button" className="icon-button" aria-label={t("下一個視覺參考")} disabled={!edges.next} onClick={() => move(1)}><Icon name="chevron-right" /></button>
          </>}
          <Button action="upload" kind={kind} id={id} icon="paperclip" className="quiet">{t("新增視覺參考")}</Button>
        </div>
      </div>
      {children}
      {visuals.length ? <div className="reference-strip" ref={strip} role="region" aria-label={t("視覺參考")} tabIndex={0}
        onScroll={updateEdges} onKeyDown={event => {
          if (event.target === event.currentTarget && ['ArrowLeft', 'ArrowRight'].includes(event.key)) {
            event.preventDefault(); move(event.key === 'ArrowLeft' ? -1 : 1);
          }
        }}>
        {visuals.map(a => <Attachment key={a.id} record={a} visual />)}
      </div> : <p className="muted small attachment-empty">{t("尚無視覺參考")}</p>}
    </section>
    <section className="detail-section file-attachments">
      <div className="section-title">
        <h3>{t("附件")}</h3>
        <Button action="upload" kind={kind} id={id} icon="paperclip" className="quiet">{t("新增附件")}</Button>
      </div>
      {files.length ? <div className="attachment-file-list">{files.map(a => <Attachment key={a.id} record={a} />)}</div>
        : <p className="muted small attachment-empty">{t("尚無附件")}</p>}
    </section>
  </>;
}

export function Attachment({ record: a, visual = false }) {
  const [busy, setBusy] = useState(false);
  const url = a.external_url || "/api/files/" + a.id;
  const image = isPreviewImage(a);
  return (
    <div className={"attachment " + (visual ? "reference-card" : "file-attachment")}>
      <a href={url} target="_blank" rel="noopener" title={a.name}>
        {image ? (
          <img src={"/api/files/" + a.id} alt="" />
        ) : (
          <Icon name="paperclip" />
        )}
        <span className="attachment-label">
          <span className="attachment-name">{a.name}</span>
          <small>
            {a.screen || ""}
            {a.visual_version ? " · " + a.visual_version : ""}
          </small>
        </span>
        <Icon name="arrow-up-right" />
      </a>
      <div className="attachment-controls"><Picker
        aria-label={a.name + t("審閱標記")}
        data-approval={a.id}
        value={a.approval}
        disabled={busy}
        aria-busy={busy}
        onValueChange={async (value) => {
          if (busy) return;
          setBusy(true);
          try {
            await persist("attachments", a, { approval: value });
            await refresh();
            render();
            notify(t("已更新審閱標記"));
          } catch (error) {
            notify(error.message, true);
          } finally {
            setBusy(false);
          }
        }}
        items={approvalOptions}
      />
      <Button action="trash-confirm" kind="attachments" id={a.id} icon="trash" className="icon-button" aria-label={t("刪除附件 ") + a.name} />
      </div>
    </div>
  );
}
export function AutoTitle({ value, label, ...props }) {
  const ref = useRef();
  const resize = () => {
    const el = ref.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = el.scrollHeight + "px";
    }
  };
  useLayoutEffect(() => {
    resize();
    let width = ref.current.clientWidth;
    const observer = new ResizeObserver(() => {
      if (ref.current && ref.current.clientWidth !== width) {
        width = ref.current.clientWidth;
        resize();
      }
    });
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  return (
    <textarea
      ref={ref}
      className="title-input"
      rows={1}
      name="title"
      required
      aria-label={label}
      defaultValue={value || ""}
      onInput={resize}
      {...props}
    />
  );
}
export { BodyEditor, revealAnchor } from "./editor.jsx";
