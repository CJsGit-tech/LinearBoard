# LinearBoard operations

Use this reference for issue CRUD, document creation or revision, synchronization, and any workflow that changes LinearBoard.

## LinearBoard-only invariant

LinearBoard is the authoritative location for all product-management items. Never create a local mirror, backlog, project plan, requirements document, ticket export, status ledger, traceability matrix, or agent-report archive. If LinearBoard cannot be reached or written, stop and report the blocker.

The repository may contain application source code, application-required artifacts, and engineering instructions such as `AGENTS.md`. Both design commands keep versioned React Native source, assets, fixtures and an in-app review menu in isolated local prototype projects. Keep screenshots and capture metadata there when capture was explicitly requested. Share prototype launch details in chat. Keep local filesystem paths, file URLs and copyable prototype addresses out of LinearBoard documents, issues and comments. Product-management records belong in LinearBoard. Other task-owned upload intermediates are allowed only when direct entry is impossible; delete them after verifying the canonical copy.

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
| PRD | Native requirement issue; source milestone document/story IDs and readable links, matching native milestone; Related links only to actual legacy issue sources; required milestone and mapped source-story tags |
| Vision and selling points | Native Project Document linked to its project |
| Technical baseline | One native Project Document per project, reused by identity, with shared technical decisions and evidence |
| Milestone overview | Native Project Document based on the vision, owning story entries grouped under numbered milestone headings |
| Milestone | Native project milestone; a heading or label alone is insufficient |
| User story | Stable entry with explicit anchor and core acceptance in the milestone Project Document, indexed by native milestone ID; existing UserStory issues remain legacy |
| User expectation test | Story-entry core acceptance and detailed PRD acceptance; existing legacy `TC-xx` cases may also apply |
| Design overview and screen/interaction specification | Two native Project Documents updated by `create-designs` only after the user selects a locally reviewed proposal, linked to each other and source US/PRDs through stable screen/flow entries; no Design issue or View |
| Design reference | Canonical specification entry with screen/version, links to the owning Design issue or its native Approved JPGs, and recorded design approval; report the separate native attachment field accurately; no intermediate work ticket |
| Final mockup visual | Keep the versioned runnable original. After complete-set approval, upload confirmed JPG images directly to each owning Design issue and verify the rendered previews under [Design tickets](create-design-tickets.md). Link the issue gallery from the specification. Confirmed Design JPGs inherit the recorded visual-set approval as described in the Design-ticket workflow. Other manual approvals belong to the user. |
| Screen-specific DESIGN.md handoff | Explicitly requested rendered LinearBoard handoff linked from the owning screen specification entry and final visual; include source story/cases, visual-critical details, and missing asset/icon guidance when requested |
| Bug report (`debug`) | Coding agent creates or reuses the owning BUG ticket and records the user report, expectation and affected source links. |
| Debug result feedback | Coding agent comments directly on that BUG ticket with status, cause, action and verification, then reads back the comment. |
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
- Native milestone association is `milestone_id`; category is the exact enum UserStory / ProductRequirement / Design / FrontEnd / BackEnd. Creation automatically adds its Category child; preserve existing M/US/Coder label IDs; apply the milestone and mapped source-story tags and verify exactly one Category child.
- Relations use `{source_id,target_id,relation}` with related / blocks / supersedes / duplicate. A related relation is reciprocal in the UI; do not create an extra reverse duplicate. Blocks direction is blocker to blocked issue. Document links remain Markdown record links.
- Batches optionally persist explicitly authorized checkpoint proposals via `batches`; dispatches are separate `dispatches`, each with exactly one FE/BE issue and a maximum of three active assignments. Store the acknowledgement/plan in review state, then the TPM-accepted plan before executing; record worker reports and independent verification separately. A dispatch row does not spawn a worker.
- Evidence uses `evidence` with project/issue, criterion, environment, result and body; actual evidence and external tool output must substantiate every Pass.
- Do not invent cycles, estimates, permissions, user directories or other absent Linear SaaS features. Assignee is an application string. Placement is tabs or shared within the selected application project.
- The automation API cannot set Done. For an authorized Done transition use the normal LinearBoard UI, following the applicable browser tool rules. Do not spoof `X-LinearBoard-Actor:user` or bypass the API gate. Confirmed Design JPGs may inherit a recorded user approval through the Design-ticket workflow. Other attachment approvals retain their own user-controlled gate.

## Image attachments

LinearBoard has no signed-upload prepare/PUT/finalize workflow. For an authorized file, create `attachments` with target_kind, target_id, name, MIME, screen/version metadata, and content_base64 (maximum decoded size 15 MB), or external_url for an accessible HTTP(S) reference. Use native Approved JPGs and links to their owning LinearBoard records for design review. Use draft for unapproved visuals and evidence for verified implementation captures. Except for confirmed Design JPGs inheriting their recorded approval, only the user marks the native attachment field approved in the application; read back that field before describing it as natively approved. Recorded exact-scope design approval from chat follows [the visual approval gates](create-visuals.md#design-approval-and-native-attachment-state) and does not change the native field. Do not impersonate the user to bypass the server gate.

Read back the attachment and compare downloaded bytes with the selected capture, then open `/api/files/{attachment_id}` and the owning record in the actual UI. Link/render that file URL in the exact authorized document/issue section. Verify actual format/MIME, title, version, ownership and visible image; keep capture scenario/viewport provenance in rendered content, using only supported attachment fields. For required JPG conversion, inspect the derivative and retain the original capture; preserve legacy design originals. Clean up temporary staging after successful readback, retaining the visual-review bundle exception.

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

Use [issue governance](issue-governance.md#status-authority). A status change must be part of the invoked command's defined workflow or explicitly requested; generic mutation authority never overrides a preserve-state rule. Retrieve before and after each transition. Use the native UI for authorized `Done` transitions. Use the supported API or UI for `Todo` and other permitted states.

## Dispatch-related transitions

Use [coding dispatch](coding-dispatch.md) for the worker lifecycle and [issue governance](issue-governance.md#status-authority) for transitions. The TPM owns dispatch records. The assigned delivery reviewer owns independent verification evidence and review status updates. Under `debug`, the assigned coding agent creates or reuses its BUG ticket and records its result there. Read [PocketStocks delivery exception](pocketstocks-delivery.md) only when that resolved project and UI scope apply.

## Post-write audit

Retrieve every affected record and apply the invoked command's verification checklist. For issue work, also apply [issue governance](issue-governance.md#post-write-audit). Report exact records changed, anything intentionally unchanged, and confirmation that no prohibited local product-management copy remains.
