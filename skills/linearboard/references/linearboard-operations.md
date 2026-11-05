# LinearBoard operations

Use this reference for issue CRUD, document creation or revision, synchronization, and any workflow that changes LinearBoard.

## LinearBoard-only invariant

LinearBoard is the authoritative location for all product-management items. Never create a local mirror, backlog, project plan, requirements document, ticket export, status ledger, traceability matrix, or agent-report archive. If LinearBoard cannot be reached or written, stop and report the blocker.

The repository may contain application source code, application-required artifacts, and engineering instructions such as `AGENTS.md`. Product-management records belong in LinearBoard. A local task-owned upload intermediate is allowed only when direct LinearBoard entry is impossible; delete it after retrieving LinearBoard and verifying the uploaded canonical copy.

For `sync`, also apply the bounded difference classification and reconciliation contract in [sync](sync.md). Dispatch records its own validated plans, research decisions and evidence automatically; cross-record repairs follow the authorized sync scope.

## Preflight

Before a write:

1. Resolve the LinearBoard workspace, exact team, and exact project. Do not invent any destination.
2. Search titles, aliases, related issues, documents, and prior feature names for the canonical record and duplicates.
3. Retrieve current team conventions: states, labels, issue hierarchy, priority, assignee strings, milestones, and document patterns supported by application capabilities.
4. Retrieve the current target record immediately before updating it.
5. Identify whether the request authorizes creation, content editing, upload, transition or destructive action.
6. For issue work, apply [issue governance](issue-governance.md); preserve a historic title or status unless the command authorizes changing it.

## Artifact placement

| Item | LinearBoard destination |
| --- | --- |
| PRD | Native requirement issue; source milestone document/story IDs and readable links, matching native milestone; Related links only to actual legacy issue sources; M/US labels optional |
| Technical Baseline | Canonical project document titled `Technical Baseline — [Product] [Stage]` |
| Vision and selling points | Native Project Document linked to its project |
| Milestone overview | Native Project Document based on the vision, owning grouped story entries and the structural story index |
| Milestone | Native project milestone; a heading or label alone is insufficient |
| User story | Stable entry with explicit anchor and core acceptance in the milestone Project Document, indexed by native milestone ID; existing UserStory issues remain legacy |
| User expectation test | Story-entry core acceptance and detailed PRD acceptance; existing legacy `TC-xx` cases may also apply |
| Design overview and screen/interaction specification | Two native Project Documents maintained by document-only `create-designs`, linked to each other and source US/PRDs through stable screen/flow entries; no Design issue or View |
| Design reference | Canonical specification entry with screen/version, accessible exact image and recorded design approval; report the separate native attachment field accurately; no intermediate work ticket |
| Final prototype visual | Image attachment on the owning screen/interaction specification document, with screen/version metadata and source US/PRD links; attach only explicitly selected, upload-authorized finals; recorded exact-scope design approval follows create-visuals, while native attachment approval requires user action and readback |
| Screen-specific DESIGN.md handoff | Explicitly requested rendered LinearBoard handoff linked from the owning screen specification entry and final visual; include source story/cases, visual-critical details, and missing asset/icon guidance when requested |
| Bug report (`debug`) | Native project Bugs Project Document; find/reuse or create if absent, append Datetime / User Report bullets in the existing style before FIX work; analysis and acceptance remain in FIX issues |
| Debug result feedback | Native comment on that Bugs document after independent verification, grouped by report batch with FIX links and concise results; detailed evidence remains on the owning FIX issue |
| Implementation report | Comment on the corresponding delivery issue |
| Verification evidence | Comment or attachment on the corresponding issue |
| Current UI screenshots during sync | Verified evidence attachments with a current screenshot section on affected issues and a linked owning screen-specification index; preserve earlier images as history |
| Approval | Dated comment or approved state according to team convention |

## Application transport and payloads

Use connected `linearboard_*` tools, or run the bundled client with JSON on stdin:

```sh
python3 <skill-folder>/scripts/operate.py linearboard_capabilities
python3 <skill-folder>/scripts/operate.py linearboard_list --args-file /path/to/temporary-input.json
```

`--url` defaults to `LINEARBOARD_URL` or `http://127.0.0.1:8765`. Before using connected MCP tools, run `scripts/ensure_running.py`; `scripts/operate.py` runs the same preflight automatically. A healthy PostgreSQL-backed LinearBoard is reused without restarting it. If stopped, the helper verifies the existing Compose project, secret and named volume, starts Docker Desktop if needed, then runs `docker compose up -d --no-build --pull never --wait --wait-timeout 90 db app`. It checks health and application identity before executing the requested tool. Startup progress goes to stderr; tool results stay JSON on stdout.

Automatic startup is scoped to the local port 8765 and the existing `/Users/chuang/Desktop/projects/LinearBoard/compose.yaml`; override the project directory with `LINEARBOARD_PROJECT_DIR` or `--project-dir` only for a resolved existing deployment. `--no-autostart` opts out for an explicitly managed alternate test/development URL. If startup fails, report the blocker and stop dependent writes. Do not retry by creating volumes, rotating credentials, running migration or reverting to SQLite. API writes still use the automation actor. The service stores attachments, history, retry keys and trash in PostgreSQL. The backup API returns custom-format `linearboard.pgdump`; legacy SQLite files are retained historical backups, not the live data source.

Read capability `resources` for exact fields and `statuses_by_team` from `/api/state` for actual workflow states. Tools are transport operations; the command procedures in this skill remain the orchestration layer. For unavailable capabilities, stop the affected operation rather than inventing unsupported fields or switching to Linear SaaS.

- `linearboard_list`: `{kind, filters?, cursor?, limit?}`. Follow `next_cursor` until null; `--all` collects every page. Exact scalar filters are ANDed; array fields accept exact arrays or scalar membership.
- `linearboard_get`: `{kind,id}`; `history:true` returns revisions, `members:true` for views returns actual membership. Preserve returned stable IDs and use absolute service-origin URLs derived from `url`.
- `linearboard_create`: `{kind,data,idempotency_key}`. Search before create; use a stable key for the same logical attempt. The server does not deduplicate identical titles automatically.
- `linearboard_update`: `{kind,id,data,idempotency_key}` with `data.expected_version` from the latest read. On conflict, re-read and reconcile; never force-write a stale draft. Retrying a lost response reuses the original payload/version/key, not a new version with an old key. After a write independently read back identity, fields and relationships.
- Project Documents use `documents` with `project_id`, optional `milestone_id`, `doc_type`, `title`, `body` (Markdown rendered by the UI). Comments target `documents`, `issues`, or `projects` through `target_kind` and `target_id`.
- Native milestone association is `milestone_id`; category is the exact enum UserStory / ProductRequirement / Design / FrontEnd / BackEnd. Creation automatically adds its Category child; preserve existing M/US/Coder label IDs; new M/US labels are optional and verify exactly one Category child.
- Relations use `{source_id,target_id,relation}` with related / blocks / supersedes / duplicate. A related relation is reciprocal in the UI; do not create an extra reverse duplicate. Blocks direction is blocker to blocked issue. Document links remain Markdown record links.
- Batches optionally persist explicitly authorized checkpoint proposals via `batches`; dispatches are separate `dispatches`, each with exactly one FE/BE issue and a maximum of three active assignments. Store the acknowledgement/plan in review state, then the TPM-accepted plan before executing; record worker reports and independent verification separately. A dispatch row does not spawn a worker.
- Evidence uses `evidence` with project/issue, criterion, environment, result and body; actual evidence and external tool output must substantiate every Pass.
- Do not invent cycles, estimates, permissions, user directories or other absent Linear SaaS features. Assignee is an application string. Placement is tabs or shared within the selected application project.
- Automation cannot set Done or set the native attachment approval field. The final user controls those UI actions; do not spoof `X-LinearBoard-Actor:user` in the client. An actual user design approval in chat may be recorded as exact-scope evidence under the create-visuals gates; recording it is not setting that native field.

## Image attachments

LinearBoard has no signed-upload prepare/PUT/finalize workflow. For an authorized file, create `attachments` with target_kind, target_id, name, MIME, screen/version metadata, and content_base64 (maximum decoded size 15 MB), or external_url for an accessible HTTP(S) reference. Local filesystem paths alone are not accessible record attachments. Use draft for unapproved visuals and evidence for verified implementation captures. Only the user marks the native attachment field approved in the application; read back that field before describing it as natively approved. Recorded exact-scope design approval from chat follows [the visual approval gates](create-visuals.md#design-approval-and-native-attachment-state) and does not change the native field. Do not impersonate the user to bypass the server gate.

Read back the attachment, then open `/api/files/{attachment_id}` and the owning record in the actual UI. Link/render the returned file URL using Markdown image syntax in the exact authorized issue/document section. For evidence requiring JPG, convert and inspect before upload; original imagegen design artifacts remain unchanged. Verify titles, version, target identity and visible image. Clean up only task-owned temporary upload staging after successful readback, retaining the read-only gallery exception.

## Saved Views

Persist `views` using project_id, exact category, placement (tabs default, shared only when requested), group_by, optional milestone_id, statuses and label_ids. Use empty statuses and no milestone filter for category-wide Views across all statuses and milestones. Preserve existing user customization on reuse. Retrieve actual members with `linearboard_get {kind:"views",id,members:true}` and compare against independently assembled expected issue IDs; verify placement in the running UI. No SaaS `list_issues/customView` parameter or team Views page is needed.

## Recoverable deletion

Only remove explicitly authorized records. Use `linearboard_trash_impact {kind,ids}`; inspect the returned affected records, then `linearboard_trash_move {kind,ids,fingerprint,idempotency_key}` using that exact preview. Re-preview after a conflict. `linearboard_trash_list` lists recoverable batches and `linearboard_trash_restore {batch_id,idempotency_key}` restores a batch. Descendant issues are included with their parent; restore required team/project/parent records first. Archive is unsupported. The skill provides no permanent-delete tool; the user manually confirms that action in the application UI.

## Issue records

For issue categories, delivery shape, titles, allowed transitions and post-write checks, use [issue governance](issue-governance.md). Command-specific story, PRD, delivery, debug and dispatch references add their own content requirements. Application operations do not independently authorize issue creation or transition.

## CRUD rules

### Create

- Search for the canonical record and likely duplicates first.
- Use the resolved team/project and existing conventions.
- Validate issue category, title and shape against [issue governance](issue-governance.md) and the invoked command reference.
- For delivery issues, include clear purpose, a source story link, applicable acceptance criteria or existing `TC-xx` cases, delivery acceptance checks, dependencies, and initial state. The merged `create-milestones`/story aliases create document entries, not story issues.
- Link canonical documents instead of pasting stale copies.

- After any issue-creation command, create or reuse its project/category saved View and verify placement, filters and membership using [issue Views](issue-views.md). Repeated commands reuse matching issues and Views.

### Read

- Retrieve the current record before reporting status, dispatching work, or planning a mutation.
- Distinguish recorded fact from inference and unresolved intent.

### Update

- Apply the smallest authorized change.
- Preserve useful history, relationships, fields, labels, ownership, and content outside scope.
- Stop and surface conflicts rather than overwriting newly discovered changes.
- After the write, retrieve and verify exact fields, links, project/team membership, rendered content, and state.

### Delete a record

- Require explicit authorization naming the exact target and intended action.
- Recheck identity, project/team, relationships, and current state immediately before the action.
- Prefer a recoverable lifecycle state when it satisfies the user's intent and team conventions.
- Never delete merely because a record appears duplicated.

## Issue status authority

Use [issue governance](issue-governance.md#status-authority). A status change must be part of the invoked command's defined workflow or explicitly requested; generic mutation authority never overrides a preserve-state rule. Retrieve before and after every authorized transition. Only the final user decides `Done`.

## Dispatch-related transitions

Use [coding dispatch](coding-dispatch.md) for the worker lifecycle and [issue governance](issue-governance.md#status-authority) for transitions. Workers never write LinearBoard. Read [PocketStocks delivery exception](pocketstocks-delivery.md) only when that resolved project and UI scope apply.

## Post-write audit

Retrieve every affected record and apply the invoked command's verification checklist. For issue work, also apply [issue governance](issue-governance.md#post-write-audit). Report exact records changed, anything intentionally unchanged, and confirmation that no prohibited local product-management copy remains.
