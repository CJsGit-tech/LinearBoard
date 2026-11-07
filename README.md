# LinearBoard

[English](README.md) · [繁體中文](README.zh-TW.md)

A local workspace for projects, tasks, documents, and delivery reviews. Use the app on its own, or connect Codex through the included LinearBoard skill. No Linear account is required.

[Quick start](#quick-start) · [Interface tour](#interface-tour) · [Hands-on guides](docs/linearboard-guides/index.html) · [Codex integration](#mcp-integration)

![LinearBoard issue list with grouped workflow states, category and milestone labels, and project details](docs/images/issue-list.jpg)

*Current English interface with fictional demo data. Your workspace starts without prefilled project tasks.*

- **Plan:** keep the vision, grouped stories, requirements, and milestones connected.
- **Organize:** switch between a compact list, a status board, and saved category Views.
- **Review:** keep descriptions, design references, comments, and verification evidence with the work.

## Quick start

Requires Docker with Compose. The image build installs its Node and Python dependencies.

```sh
git clone https://github.com/CJsGit-tech/LinearBoard.git
cd LinearBoard
python3 scripts/setup_compose.py
docker compose up -d --build
```

Open [http://127.0.0.1:8765](http://127.0.0.1:8765). The initial workspace contains a Personal team; create your first project in the app. No production tasks are prefilled.

```sh
docker compose ps
docker compose logs --tail 100 app
docker compose stop
docker compose start
```

The app is published only on the host's loopback address. PostgreSQL has no published host port. The generated password is mounted from `data/docker/database-password` as a Compose secret; setup preserves an existing password. Keep that file private and out of version control.

`docker compose down` retains the database volume. **Do not use `docker compose down -v` to stop the app:** it removes the database volume.

## Create your first project

1. Open the app and choose **Create project** beside **Project** in the sidebar.
2. Add a milestone, then choose **New issue**. Set its category, status, and milestone.
3. Open the issue to write a description or acceptance checklist. Choose **Save changes** in the top toolbar.
4. Switch to **Board view**, or create a saved View for the category you use most.

For guided product planning, start with the [English hands-on guide](docs/linearboard-guides/hands-on.en.html) or [繁體中文操作指南](docs/linearboard-guides/hands-on.zh-Hant.html). Both include copyable prompts, expected outputs, and checks to perform afterward. Replace `<Project>` and other placeholders before sending a prompt to Codex. Download or open the HTML files locally to use the interactive guides; a repository file viewer shows their source.

## Interface tour

### See work by status

Choose **List view** for scanning many tasks, or **Board view** to see work in columns and drag tasks between states. Right-click an issue or group for actions. To update several tasks, select them using the left edge of each row, or choose **Select all in group**, then use **Actions**.

![LinearBoard board view showing demo tasks in In Progress, In Review, Todo, and Backlog columns](docs/images/issue-board.jpg)

*The board supports horizontal scrolling. Unused groups can be hidden from their group menu.*

### Edit the task where you read it

Write headings, lists, links, and acceptance checklists in the rich-text editor, or switch to Markdown. Status, category, and milestone stay alongside the description. Use the top toolbar to save, go back, or delete; comments, attachments, evidence, and revision history continue below the editor.

![LinearBoard task detail with rich-text formatting, acceptance checkboxes, task properties, and a top-toolbar Save changes button](docs/images/issue-detail.jpg)

### Know where things live

| Area | What you do there |
| --- | --- |
| Project list in the sidebar | Click a project to switch its workspace. |
| Overview and Milestone | Read the project context and milestone outcomes. |
| Issues and saved Views | Work with tasks and reusable category/filter combinations. |
| Documents | Keep the vision, grouped stories, PRD-related notes, and design specifications. |
| Delivery beneath the selected project | Inspect saved batches, dispatch plans, and reports. |
| Workspace settings | Manage teams, labels, trash, and database backups. |

The interface uses a dark, warm-neutral palette, compact task rows, and consistent menus. The sidebar selects the project; top tabs organize its content; the optional right panel shows project details. This keeps navigation and task editing in the same workspace.

## Work manually or with Codex

**In the app:** create projects, write documents, organize tasks, and review changes directly. The app works without an AI model or API key.

**With Codex:** install the [included LinearBoard skill](skills/linearboard/SKILL.md) to guide planning, requirements, design, scoped implementation, and review. Start with `$linearboard help`; use the hands-on guide to choose the next command. The app stores records; Codex and external tools perform the requested work. A dispatch record alone does not start an agent.

**Final acceptance stays with you:** `In Review` means work is ready for your review. Only the user decides `Done`. Exact JPGs registered against the user's complete-set approval inherit Approved on their Design tickets.

## Language

The interface supports **English** and **Traditional Chinese**. On first use, Chinese browser locales select Traditional Chinese; other browser locales select English. Use **Language** in the sidebar to switch at any time. The choice is saved in that browser, and changing it preserves the current screen and unsaved form contents.

Navigation, forms, editor controls, accessibility labels, notifications, dates, and API validation messages follow the selected language. Project names, issue titles, documents, comments, labels, custom workflow states, and other user-authored content are preserved as entered. The skill is written in English. The app links English users to an English user guide.

## Optional SQLite development mode

Requires Python 3.12+ and Node.js 20+.

```sh
npm ci
npm run build
python3 server.py
```

Build the frontend after cloning or changing UI source; `web/dist/` is generated and is not committed. There is no separate frontend dev server. You can select a disposable database and alternate port:

```sh
python3 server.py --port 9000 --db /absolute/path/to/development.sqlite3
```

Without `DATABASE_URL`, the server uses SQLite (by default `data/linearboard.sqlite3`). Compose configures PostgreSQL using `DATABASE_URL` and `DATABASE_PASSWORD_FILE`.

## Features and shortcuts

- **Projects and milestones:** describe outcomes and group work under native milestones.
- **Issues:** use list or board layouts, filters, search, categories, priorities, assignees, parent issues, and relations. Drag issues between status columns or edit their status in the form.
- **Documents:** edit rich text or Markdown, attach documents to projects and milestones, and retain comments and revision history. Content containing HTML stays in source editing mode to preserve it.
- **Views:** save project-scoped filters with category, labels, states, milestone, grouping, and tab or shared-sidebar placement.
- **Attachments:** upload files or external links with screen/version metadata and review labels. Uploads are limited to 15 MB. Only recognized PNG/JPEG bytes render inline; other files download.
- **Delivery:** record FE/BE batches, dispatch plans and reports, and independent verification evidence. A dispatch record does not execute an agent.
- **Settings:** manage teams and workflow states, label groups, recoverable trash, database backups, and integration help.

Press **C** to create an issue and **/** to search outside editable controls. Forms use explicit Save buttons. Record details provide Back navigation and **Alt+←**. Updates from external tools appear on explicit navigation or reopening a record; an open editor is not overwritten by background writes.

Default workflow states: Backlog, Todo, In Progress, In Review, Done, Canceled, and Duplicate. Teams can define custom states. A referenced state cannot be removed. **Done** and native visual approval require a user action; automation cannot grant final acceptance.

## Data, backups, and trash

Compose stores canonical records, attachment bytes, history, retry keys, and trash in the named PostgreSQL volume `linearboard_postgres_data`. Browser local storage holds presentation preferences, the selected project, and language.

**Workspace settings → Download database backup** returns a PostgreSQL custom-format `linearboard.pgdump` in Compose mode, or a SQLite backup in SQLite mode. Restore PostgreSQL backups with `pg_restore` into a new empty database, verify the restored contents, then switch connections. Do not overwrite a running database or copy only a live SQLite main file while ignoring its WAL.

Trash retains IDs and history until the user permanently deletes records. Deleting an issue includes its descendants; deleting a project includes its owned records. The app previews the impact and restores without overwriting later changes. Restore required parent records first. Permanent deletion cannot be undone; older backups may still contain the deleted data.

The app is designed for its owner on the same machine. `X-LinearBoard-Actor: user` marks local manual actions; it is not network authentication. Do not expose this service to an untrusted network.

### Migrate an existing SQLite workspace

Retain a consistent SQLite backup as your migration source. Stop writes during migration and do not run the app against the destination until verification completes.

```sh
python3 scripts/setup_compose.py
docker compose up -d db
docker compose run --rm migrate /source/your-backup.sqlite3
docker compose up -d app
```

The migration service mounts local `data/` read only at `/source`. Migration verifies row counts and SHA-256 across records, history, requests, blobs, counters, and trash batches in one transaction. It preserves identities and rejects a different, nonempty destination. An identical rerun makes no changes. The old SQLite file is a historical backup, not a synchronized replica.

## MCP integration

Start the HTTP app first, then configure a stdio server in your MCP client:

```json
{
  "mcpServers": {
    "linearboard": {
      "command": "python3",
      "args": [
        "/absolute/path/to/LinearBoard/mcp_server.py",
        "--url", "http://127.0.0.1:8765"
      ]
    }
  }
}
```

Available tools include `linearboard_capabilities`, `linearboard_list`, `linearboard_get`, `linearboard_create`, `linearboard_update`, `linearboard_update_issue_statuses`, and the `linearboard_trash_*` operations. Inspect `/api/capabilities` for exact fields and contracts. List calls are paginated; follow every `next_cursor`. The supplied `linearboard.client.Client` supports MCP connections, readback, reuse, and exact retries.

LinearBoard persists records and exposes the 15 canonical commands and their aliases in the capability catalog. Codex and external tools interpret the skill, build and review local HTML prototypes, run agents, and inspect the actual target product. Share runnable prototype links in chat and link the owning Design tickets or their native Approved JPGs from LinearBoard records.

### Included management skill

The complete bundle is in [`skills/linearboard/`](skills/linearboard/): `SKILL.md`, references, reusable authoring templates, agent metadata, and Python tools. These are workflow instructions, not a copy of a project's requirements or delivery records.

Copy the folder to `~/.codex/skills/linearboard/` to install it for Codex, preserving any existing installation first, or point Codex directly at its `SKILL.md`. The design and sync workflows also reference the separately installed `design-pro` and `file-change-summary` skills. For a checkout at a different path, set:

```sh
export LINEARBOARD_PROJECT_DIR="/absolute/path/to/LinearBoard"
```

Perform the initial Compose setup yourself using the steps above. The skill's preflight reuses or starts an existing deployment; it does not initialize volumes, migrate data, or rotate passwords. Image-generation commands also require the host's `imagegen` skill and tools, which are not bundled here.

The bundle is a publication snapshot. Changes to a personal skill installation do not automatically update this repository. Product requirements, planning decisions, task states, approvals, and delivery evidence belong in the LinearBoard application rather than a parallel repository backlog.

## REST API

| Operation | Endpoint |
| --- | --- |
| Capabilities | `GET /api/capabilities` |
| Paginated list | `GET /api/{kind}?filters={URL-encoded JSON}&cursor=0&limit=100` |
| Get one record | `GET /api/{kind}/{id}` |
| Create | `POST /api/{kind}` |
| Update | `PATCH /api/{kind}/{id}` |
| History | `GET /api/history/{id}` |
| Actual View membership | `GET /api/views/{id}/members` |
| Attachment bytes | `GET /api/files/{id}` |
| Consistent backup | `GET /api/backup` |

Kinds include teams, projects, milestones, labels, issues, documents, views, comments, relations, attachments, batches, dispatches, and evidence. Stable record `url` fields are relative UI deep links.

Send JSON writes with `Content-Type: application/json`. PATCH requires the current `expected_version`; a stale version returns 409. Use one `Idempotency-Key` per logical write and reuse the same key and exact payload when retrying. Reusing a key with different content returns 409. A repeated title alone does not deduplicate a create operation.

Send `Accept-Language: en` for English API errors or `zh-TW` for Traditional Chinese. When omitted, API errors retain the Chinese default for existing clients. Localized errors return `Content-Language` and `Vary: Accept-Language`. Record data and identifiers are not translated.

## Development and checks

```sh
npm run build
npm test
npm run test:i18n
npm run test:guide
npm run test:ui
npm run test:selects
```

Browser tests use installed Google Chrome and disposable SQLite databases, not the canonical workspace. The localization suite checks English and Chinese navigation, editing, persistence, language switching, errors, and content preservation. The guide suite checks the current skill command directory, prompt composer, search, reading progress, mobile navigation, strict Content Security Policy, and working browser/server offline exports.

Main source areas: `web/` (React UI and message catalog), `linearboard/store.py` (validation and persistence), `linearboard/postgres.py` (PostgreSQL backend), `server.py` (HTTP routes), `mcp_server.py` (MCP bridge), and `tests/`. English API errors are in `linearboard/locales/en.json`.

The app uses React, Radix Primitives, Tiptap, Lucide, Marked, DOMPurify, esbuild, and Playwright. Exact dependency versions are locked in `package-lock.json`. The built app has no CDN, remote font, or image dependency. The optional local `/visuals/` review gallery is not included in Git or the Docker image.

Workspace databases, credentials, backups, generated review assets, dependencies, and build output are excluded by `.gitignore`.


## Inspired by Linear

This application and its companion management skill are inspired by [Linear](https://linear.app) and its approach to organizing product work. LinearBoard is developed independently as a standalone local workspace.
