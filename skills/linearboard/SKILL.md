---
name: linearboard
description: "Plan products and manage requirements, design, visual references, FE/BE delivery, scoped dispatch, synchronization and verified review in the standalone local LinearBoard application."
---

# LinearBoard

This standalone skill's command router and local application rules are authoritative. Read [application operations](references/linearboard-operations.md) before any LinearBoard operation.

## Destination and storage boundary

Default to `http://127.0.0.1:8765` and honor an explicitly supplied LinearBoard URL. Use connected `linearboard_*` tools when available; otherwise use `scripts/operate.py`, which performs the application preflight. Resolve the exact team, project and milestone with full pagination before acting.

LinearBoard's PostgreSQL-backed application is the canonical product-work store. Never edit its database or legacy backup directly, create another PM database, silently switch destinations or treat an application project as the product repository. Startup, payloads, attachments, Views and recoverable trash are defined in [application operations](references/linearboard-operations.md).


Manage the product-delivery chain for one resolved LinearBoard team and project:

```text
Planning → 4W1H vision Project Document → native milestones and milestone document with grouped user stories → linked PRD issues → Design documents with a reference-grounded visual idea → scope-sized visual studies or a bounded edit → layout selection or delegated choice → complete screen/component review → full design approval → Design tickets → FE/BE issues → dispatch → verified review
                                                  ↕ sync confirmed records within authorized scope
```

## Next-command selection and recommendation

When the user asks what to do next, or when a command's final report names a next action, inspect the live canonical records and recommend the **first incomplete applicable deliverable**. Completing the current command only clears that command's gate; it does not prove readiness for a later stage. A recommendation is not authorization to run the recommended command.

First check the building flow: missing vision → `create-vision-document`; missing native milestones or grouped story document → `create-milestones`; missing PRD coverage → `create-PRDs`; consequential open PRD scope decisions → offer `prd-demystify`. A draft alone does not establish readiness. Do not rerun completed stages.

Then, for user-visible scope, apply this evidence-based order while reusing anything already complete:

1. Missing or unverified design overview / screen-and-interaction specification → recommend `create-designs`.
2. Design documents exist but the current-scope layout, complete visual set, or required approval is missing → recommend or continue `create-visuals` at its actual state-machine stage.
3. The complete design set is approved but post-approval Design tickets are not verified → finish the post-approval stage of `create-visuals`.
4. Required FrontEnd or BackEnd delivery issues and their Views are missing → recommend the applicable `create-issues-FE` and/or `create-issues-BE`; do not infer one side merely because the other exists.
5. Several ready delivery issues need dependency-aware checkpoint ordering and no explicit issue selection or saved batch exists → recommend `organize-task-batch`; it is optional for an already bounded, ready issue selection.
6. Recommend `dispatch` only when existing, explicitly selectable FE/BE issues pass the dispatch readiness gate, including required approved UI references for user-visible work and accessible execution targets.

For a confirmed BE-only or non-visual scope, skip design/visual stages only when canonical requirements establish that they are not applicable. Do not rerun completed stages as a ritual. Never recommend `dispatch` merely because PRD/QA work finished, because an earlier dispatch request was blocked, or because implementation is the eventual goal. If the user explicitly requests `dispatch` before readiness, perform its read-only preflight, leave records unchanged, report the exact missing gate, and recommend the first missing authorized command rather than running that command automatically.

## LinearBoard is the sole product-work system of record

When a delivery issue cites a visual reference, attach or link the exact approved image or design artifact in the issue and identify its title and version. Verify that the reference is accessible from the issue. Do not describe an unreviewed draft as approved.

Exploratory planning and draft discussion may remain in chat; saving them as a canonical record requires an authorized LinearBoard write.

All saved project-management and product-delivery records must be created, read, updated, linked, reviewed, and retained in the LinearBoard app. This includes PRDs, user stories, acceptance criteria, requirements, decisions, research summaries, issue state, dispatch records, coding-agent reports, implementation evidence, approvals, and delivery audits.

- Never create or maintain a local PRD, issue database, ticket board, backlog, status file, traceability file, agent-report archive, or project-management document.
- Never treat a repository file, chat response, or coding-agent message as the canonical product record.
- Keep source code, tests, configuration, migrations, runtime assets, reproducible application artifacts, and repository engineering instructions such as `AGENTS.md` in the repository. Keep product-management records in LinearBoard.
- Except for the visual-review bundle below, a task-owned local file may be used only as temporary upload or conversion staging when LinearBoard cannot accept content directly. After upload, retrieve LinearBoard to verify the canonical copy, then remove the exact temporary file.
- If LinearBoard access, the target workspace/team/project, or required permission is unavailable, stop the affected operation and report the blocker. Do not fall back to local files.

`create-visuals` also delivers a local, read-only HTML gallery and its imagegen image assets for convenient visual review. This non-canonical review bundle may remain at the delivered path; it is not a local PM record. Limit its metadata to visual titles, screen/version identifiers, review labels and links to the owning LinearBoard issues/documents. Keep requirements, decisions, approval records and issue status in LinearBoard; the gallery cannot grant approval or write to LinearBoard.

Skill-internal templates under `assets/templates/` are authoring instructions, not project records. Use them to create native, rendered LinearBoard content; never copy them into the product repository as deliverables.

## Commands

Interpret a leading command when supplied. Otherwise run the smallest command sequence that satisfies the request.

- `help`: return only the bullet list in [help](references/help.md), translated into the user's language. Each top-level bullet is a command with one nested purpose bullet. No introduction, tables, workflow/gate notes, examples, next-step recommendation or closing explanation; read-only.
- `planning`: discuss and research product ideas; save only when requested. Read [planning](references/planning.md).
- `create-vision-document`: create or revise the native vision Project Document. Read [vision workflow](references/create-vision-document.md) and [template](assets/templates/vision-template.md).
- `create-milestones`: derive user stories from the vision, group them into outcome-based native milestones, and document grouped stories in the milestone Project Document. Read [milestone workflow](references/create-milestones.md) and [template](assets/templates/milestones-template.md). Creates no UserStory issues or View. `create-userstories`, `user-stories` and `stories` are compatibility aliases for this same merged command, not a separate issue-creation stage.
- `create-PRDs <Project> <Milestone>` (`create-prds`, `prd`): create or revise milestone-linked ProductRequirement issues, relations, labels and saved View. Read [PRD workflow](references/create-prds.md), [requirements chain](references/requirements-chain.md), [labels](references/requirement-labels.md), [issue governance](references/issue-governance.md) and [Views](references/issue-views.md).
- `prd-demystify <Milestone>`: clarify open-ended scope/boundary questions and update the owning PRDs directly; no new QA document. Read [decision workflow](references/prd-demystify.md).
- `create-designs <Project> <Milestone>` (`prototype-ui-issues`, `Prototype UI Issues`, `prototype-ui`, `Prototype UI`): create or revise only the design overview and screen/interaction specification Project Documents, with inspected references, a product-specific visual idea and a concrete recommendation. Read [design workflow](references/create-designs.md). It creates no issues or View and does not run `create-visuals`.
- `create-issues-FE <Project> <Milestone>` (`create-issues-fe`, `build-ui-issues`, `Build UI Issues`, `build-ui`, `Build UI`) and `create-issues-BE` (`create-issues-be`): create or revise the requested implementation side and saved category View. Read [delivery issues](references/create-delivery-issues.md), [issue governance](references/issue-governance.md) and [Views](references/issue-views.md). New issues remain in Backlog; dispatch is separate.
- `organize-task-batch <Project> <Milestone> [issue IDs]`: return a read-only ordered checkpoint proposal. Read [task-batch organization](references/organize-task-batch.md).
- `create-visuals <Project> <Milestone>`: turn the product-specific visual idea into inspected imagegen studies and a verified gallery. Explore a new composition with a justified small comparison (normally two or three); edit an existing selected layout directly for bounded corrections. State coverage and generation batches before starting. Concrete layout selection or explicit selection delegation continues the original detail scope. Record resumable checkpoints in the owning specification comment. Final-image upload, exact-scope design approval and native attachment approval are distinct; use the gate definitions in [visual workflow](references/create-visuals.md). Read it and [$imagegen](../.system/imagegen/SKILL.md); after complete-set design approval create/reuse Design tickets via [post-approval Design tickets](references/create-design-tickets.md). Do not change existing issue states.

- `dispatch <Project> <Milestone> [Batch <n> | issue IDs]`: dispatch only the authorized issue selection, validate worker plans, independently verify results and hand reviewable work to `In Review`. Read [dispatch](references/coding-dispatch.md) and [issue governance](references/issue-governance.md).
- `debug [Project] [Milestone] [report document or issue IDs]`: record reports in the Bugs Project Document, create/reuse bounded FIX issues and, unless triage-only, implement and verify them. Read [debug](references/debug.md), [dispatch](references/coding-dispatch.md), [issue governance](references/issue-governance.md) and [Views](references/issue-views.md).
- `sync <Project> <Milestone> [scope]`: reconcile confirmed records and current UI screenshots within the requested scope without implementation. Reconcile text documents, current design references and UI screenshots together. When layout, styling, components or interaction changes make screenshots missing or stale, capture the actual affected interface, upload verified evidence, and refresh Design/delivery issue and specification references while preserving history. Clean up unused images only when requested, after reference checks and canonical verification. Read [sync](references/sync.md).

Technology lookup and selection run internally within `create-issues-FE` and `create-issues-BE`; they are not separate user commands.

Creating a draft in LinearBoard is a mutation and requires a user request that authorizes creation or editing. A request to review or explain never authorizes a LinearBoard write.

Every actual issue-creation command also creates or reuses its project/category LinearBoard View as part of the authorized output, including when matching issues already exist. Follow [issue Views](references/issue-views.md) for `create-PRDs`, `create-issues-FE`, `create-issues-BE` and their aliases, plus the post-approval Design-ticket stage of `create-visuals`; `debug` FIX issues reuse the matching FE/BE View. `create-designs` and the merged `create-milestones`/story aliases create no issues or View. A label, unsaved filter or chat link is not a saved View. Read-only commands do not create Views.

## Shared command invariants

Use supplied context and do not rerun earlier stages as a ritual. Ask only when missing information materially changes destination, scope or product behavior. Preserve unknowns instead of inventing evidence, ownership, estimates, dates, approvals or decisions.

Vision, grouped milestone/story overview and design specifications are native Project Documents. User stories are stable entries in the milestone document; PRDs are native milestone-linked issues. Existing UserStory issues and QA documents are preserved historical sources, not mandatory new outputs. Delivery work uses FE/BE issues. Read back native parents, fields, labels, relations, rendered content and requested View membership; prose alone does not establish an association.

Creation commands authorize only their named artifacts. They do not authorize later commands, implementation, dispatch, uploads or status changes. A new product may receive the minimal project container required for explicitly requested artifacts only when destination and scope are clear.

For any issue creation or classification, follow [issue governance](references/issue-governance.md). For any application write, read [application operations](references/linearboard-operations.md). Read only the command references routed above.

## Issue governance

Use [issue governance](references/issue-governance.md) as the single authority for Category labels, delivery issue shape and titles, allowed status transitions and the post-write issue audit. A command-specific instruction to preserve status or forbid issue creation always takes precedence.

## Conditional references

The command list above is the routing map; do not load unrelated references. For every LinearBoard mutation, also read [application operations](references/linearboard-operations.md). For issue mutations, read [issue governance](references/issue-governance.md). When the resolved project is PocketStocks and the authorized scope contains user-visible UI delivery, additionally read [PocketStocks delivery exception](references/pocketstocks-delivery.md).

## Review handoff and final acceptance

`In Review` means the scoped implementation is ready for the final user to review. It does not mean final acceptance, production readiness, or that every check passed.

- **In Progress / blocked:** implementation or product remediation remains, or essential behavior cannot be independently verified. Crashes, incorrect data, broken core flows, and uncertain defect attribution remain here.
- **In Review:** the scoped implementation is complete, the TPM has independently checked the main behavior and applicable evidence, and a reviewable handoff is recorded in LinearBoard. Waiting for user acceptance is not ongoing development.
- **Done:** only the final user accepts the delivery and decides the disposition of any outstanding checks or risks.

A narrow environment-only limitation may remain in `In Review` when the actual target application and relevant flows have been inspected, available checks support review readiness, and independent evidence attributes the remaining limitation to the platform, runtime, or external test environment rather than unfinished product work. Do not keep otherwise reviewable work in `In Progress` solely for that limitation. No extra approval is required for this justified non-Done transition within an authorized scope.

Record the exact affected criterion and environment, reproduction and attribution evidence, verified results, remaining impact, and next verification action in the issue. Mark the affected check `Not tested` or `Environment-blocked`, never `Pass`; preserve actual failed results and screenshots. State that the issue is ready for review with this limitation and that final acceptance remains with the user. Update any current handoff conclusion that would otherwise contradict the new state, while retaining its evidence and history.

This is not a blanket waiver of UI review or testing. An unavailable target application, missing required deployment/reference, broadly uninspected UI, unverified core flow, or unresolved product defect still blocks review readiness. Do not silently substitute another environment or claim changed requirements as a passing check. Preserve existing authorization boundaries when changing environments or adding follow-up work.

## Dispatch and independent review

Dispatch only the explicitly authorized issue selection. The TPM retains LinearBoard writes, integration and acceptance review; each worker owns one bounded, non-overlapping issue. Use at most three concurrent workers, validate each plan before implementation, and require reports for acknowledgment, completion, blockage or failure. A report is a claim, not verification.

Read [coding dispatch](references/coding-dispatch.md) for readiness, worker lifecycle and independent checks. Operate the actual target UI for user-visible work; passing tests, deployment status, static inspection or a worker screenshot alone do not prove the flow. Use credentials only when the authorized test requires them, project instructions permit them and they are safely available; never expose or modify them. Project-specific PocketStocks rules live only in [PocketStocks delivery exception](references/pocketstocks-delivery.md).

## UI implementation review gate

Every dispatched issue that changes or verifies user-visible UI must pass the independent gate in [coding dispatch](references/coding-dispatch.md#ui-implementation-review-gate) before `In Review`. Missing access to the target application, required deployment/reference or essential UI comparison blocks review readiness. Evidence screenshots prove the inspected implementation state; they never become a canonical design.

## Authorization boundaries

- Creating or editing LinearBoard records requires an explicit request that covers the target scope.
- `create-designs` authorizes two canonical outputs: the design overview and screen/interaction specification. Add a native comment only when needed to preserve discussion history. It authorizes no issue, View, status change, visual generation, implementation or dispatch.
- `create-visuals` follows its scope-sized study/edit workflow and maintains a concise canonical progress comment on the owning specification. Layout selection or an explicitly delegated composition choice continues the requested detail scope; neither is complete-set approval. Upload only exact selected/upload-authorized finals. Record exact-scope design approval from chat or LinearBoard once; accessible exact images plus that recorded approval satisfy downstream design-readiness checks without repeating the approval. Native attachment approval remains a separate user-only field and must not be spoofed or mislabeled. After complete-set approval create/reuse Design tickets and their View. Workflow comments do not authorize rewriting product/design rules, expanding scope or changing existing issue states.

- `dispatch` authorizes workers only for the exact issues or bounded selection resolved from the user's command. It never authorizes scope expansion, destructive actions or unrelated deployment.
- Status transitions follow [issue governance](references/issue-governance.md). Standing authority never overrides a command that preserves state or forbids status changes.
- The final user owns the `In Review` → `Done` decision and makes that transition after considering the recorded completion evidence. The TPM never moves a ticket to `Done` or makes that decision on the user's behalf.
- Deletion, reassignment, scheduling, scope changes, uploads and external publication require authority appropriate to that action. Record deletion uses impact preview and recoverable trash; permanent deletion remains a user UI action.
- Coding agents never write to LinearBoard. They report to the TPM; the TPM verifies their reports and is the sole LinearBoard writer for dispatched work.
- Never claim approval, implementation, verification, or completion from an agent's self-report alone.

## Completion criteria

For `organize-task-batch`, completion means the requested FE/BE scope has been reviewed and an ordered checkpoint proposal returned in the required format, with issue coverage, dependencies and blockers explicit. No LinearBoard writes, agents or implementation evidence are required for this read-only command.

For `create-visuals`, a new-composition study handoff is complete after the justified comparison set is inspected, collected in a verified gallery and opened for visual selection, unless selection was explicitly delegated. Bounded corrections and exact selected-layout reuse skip unnecessary exploration. Selection/delegated choice continues the original requested detail scope: every requested screen/component and relevant key state must be covered, inspected and collected in the rebuilt verified gallery. Intermediate batches are not full completion. Maintain read-back-verified checkpoints and pending coverage on the owning specification. Preserve imagegen originals. Upload only explicitly authorized versions. Complete-set design approval additionally requires verified post-approval Design tickets and View; native attachment approval remains separately reported. The HTML review bundle is the existing non-canonical exception.

For issue creation, completion includes the saved category View, correct team/project/category filters, requested placement and verified membership. Report issue creation and View creation separately if either is blocked.

For `sync` involving design or UI changes, completion also requires the screenshot reconciliation in [sync](references/sync.md): inspect current image coverage, capture missing or stale actual UI states, verify uploaded images in the owning records, and identify any unavailable state without substituting a mockup or claiming screenshot completeness.

For `debug`, completion also requires every selected user report in the canonical Bugs Project Document, each FIX issue to identify that document's Datetime batch and report bullet, and native verified-result comments on the document linking back to FIX issues. Keep the document body as the user report log. Issue-only records do not complete this command. For triage-only work, record the reports and linked FIX issues without claiming a fix or adding a successful-result comment.

For commands that mutate LinearBoard records or dispatch implementation, complete only after every check applicable to that command and authorized scope has been verified. Command-specific completion criteria above take precedence; do not require issues, agents, implementation evidence, status transitions or LinearBoard uploads from commands that do not produce them. Never claim an applicable check passed when it was not performed, and retain no prohibited task-scoped local product-management artifacts.

## Final report

Report only the items applicable to the command: the resolved LinearBoard team/project; canonical documents or issues changed; traceability; visual-review artifacts; agents and reports; verification; ticket transitions; approvals; blockers; and confirmation that no prohibited local product-management copies were retained. Distinguish draft, implementation complete, ready for review, remaining environment checks and final-user acceptance where relevant; do not collapse them into a blanket completion claim.
