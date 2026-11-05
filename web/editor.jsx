import React, { useMemo, useState } from "react";
import { EditorContent, useEditor } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import { Markdown as MarkdownExtension } from "@tiptap/markdown";
import { TaskList, TaskItem } from "@tiptap/extension-list";
import { TableKit } from "@tiptap/extension-table";
import Image from "@tiptap/extension-image";
import { marked } from "marked";
import { Bold, Italic, Heading2, List, ListOrdered, ListTodo, Code, Link2, Undo2, Redo2 } from "lucide-react";

function RichText({ value, onChange, label }) {
  const [linkOpen, setLinkOpen] = useState(false), [url, setUrl] = useState(""), [error, setError] = useState("");
  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        underline: false,
        link: { openOnClick: true, HTMLAttributes: { target: "_self", rel: "noopener noreferrer" } },
      }),
      TaskList, TaskItem.configure({ nested: true, a11y: {
        checkboxLabel: (node, checked) => `${checked ? "取消勾選" : "勾選"} ${node.textContent || "待辦事項"}`,
      } }), TableKit, Image,
      MarkdownExtension,
    ],
    content: value,
    contentType: "markdown",
    shouldRerenderOnTransaction: true,
    editorProps: { attributes: { class: "rich-text-content markdown", role: "textbox", "aria-multiline": "true", "aria-label": label } },
    onUpdate: ({ editor }) => onChange(editor.getMarkdown()),
  });
  if (!editor) return null;
  const controls = [
    ["標題", Heading2, () => editor.chain().focus().toggleHeading({ level: 2 }).run(), editor.isActive("heading", { level: 2 })],
    ["粗體", Bold, () => editor.chain().focus().toggleBold().run(), editor.isActive("bold")],
    ["斜體", Italic, () => editor.chain().focus().toggleItalic().run(), editor.isActive("italic")],
    ["項目清單", List, () => editor.chain().focus().toggleBulletList().run(), editor.isActive("bulletList")],
    ["編號清單", ListOrdered, () => editor.chain().focus().toggleOrderedList().run(), editor.isActive("orderedList")],
    ["待辦清單", ListTodo, () => editor.chain().focus().toggleTaskList().run(), editor.isActive("taskList")],
    ["程式碼", Code, () => editor.chain().focus().toggleCode().run(), editor.isActive("code")],
    ["連結", Link2, () => { setUrl(editor.getAttributes("link").href || ""); setError(""); setLinkOpen(v => !v); }, editor.isActive("link")],
    ["復原", Undo2, () => editor.chain().focus().undo().run(), false, !editor.can().undo()],
    ["重做", Redo2, () => editor.chain().focus().redo().run(), false, !editor.can().redo()],
  ];
  const applyLink = () => {
    try {
      const href = url.trim();
      if (!href || !["http:", "https:", "mailto:"].includes(new URL(href, location.origin).protocol))
        throw Error("請輸入有效的網址或紀錄連結。");
      editor.chain().focus().extendMarkRange("link").setLink({ href }).run();
      setLinkOpen(false);
    } catch { setError("請輸入有效的網址或紀錄連結。"); }
  };
  return <div className="rich-text-editor">
    <div role="toolbar" aria-label="文字格式" className="rich-text-toolbar">
      {controls.map(([name, Icon, run, active, disabled]) => <button key={name} type="button"
        className="icon-button" aria-label={name} title={name} aria-pressed={active} disabled={disabled}
        onMouseDown={event => event.preventDefault()} onClick={run}><Icon aria-hidden="true" /></button>)}
    </div>
    {linkOpen && <div className="rich-link-editor">
      <input aria-label="連結網址" value={url} autoFocus onChange={event => setUrl(event.target.value)}
        onKeyDown={event => { if (event.key === "Enter") { event.preventDefault(); applyLink(); } }} />
      <button type="button" onClick={applyLink}>套用</button>
      <button type="button" className="quiet" onClick={() => { editor.chain().focus().extendMarkRange("link").unsetLink().run(); setLinkOpen(false); }}>移除連結</button>
      <button type="button" className="quiet" onClick={() => setLinkOpen(false)}>取消</button>
      {error && <span role="alert">{error}</span>}
    </div>}
    <EditorContent editor={editor} id="body-preview" />
  </div>;
}

export function BodyEditor({ value = "", document = false, initialPreview = true }) {
  const [body, setBody] = useState(value);
  const hasHtml = useMemo(() => {
    let found = false;
    marked.walkTokens(marked.lexer(body), token => { if (token.type === "html") found = true; });
    return found;
  }, [body]);
  const [rich, setRich] = useState(initialPreview && !hasHtml);
  return <>
    <div className="editor-label">
      <h3>內容</h3>
      <button type="button" data-action="preview" className="quiet" aria-pressed={!rich}
        disabled={!rich && hasHtml} onClick={() => setRich(v => !v)}>{rich ? "Markdown" : "Rich text"}</button>
    </div>
    {hasHtml && !rich && <p className="muted small">此內容含 HTML，請使用 Markdown 編輯以保留原文。</p>}
    <textarea name="body" className={"body-editor" + (document ? " document-editor" : "")}
      rows={document ? 18 : 10} aria-label={document ? "文件 Markdown" : "任務 Markdown"}
      value={body} onChange={event => setBody(event.target.value)} hidden={rich} />
    {rich && <RichText value={body} onChange={setBody} label={document ? "文件內容" : "任務內容"} />}
  </>;
}
