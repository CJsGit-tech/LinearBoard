---
name: linearboard
description: "Initialize Codex project workflows and manage product planning, requirements, design with Approved JPG handoffs, FE/BE delivery, scoped dispatch, synchronization and verified review in the standalone local LinearBoard application. Use linear-tpm instead for the Linear SaaS service."
---

# LinearBoard

This skill's command router and local application rules are authoritative. Use `linear-tpm` instead for the Linear SaaS service. Read [application operations](references/linearboard-operations.md) before any LinearBoard operation.

## Destination and storage boundary

`init` is local engineering setup and `help` is offline command guidance; handle them before application preflight. Neither performs product-work mutations or advances project stages.

Default to `http://127.0.0.1:8765` and honor an explicitly supplied LinearBoard URL. Use connected `linearboard_*` tools when available; otherwise use `scripts/operate.py`, which performs the application preflight. Resolve the exact team, project and milestone with full pagination before acting.

LinearBoard's PostgreSQL-backed application is the canonical product-work store. Never edit its database or legacy backup directly, create another PM database, silently switch destinations or treat an application project as the product repository. Startup, payloads, attachments, Views and recoverable trash are defined in [application operations](references/linearboard-operations.md).


Manage the product-delivery chain for one resolved LinearBoard team and project:

```text
Planning → 4W1H vision Project Document → optional project Technical Baseline → native milestones and milestone document with grouped user stories → linked PRD issues → existing design context or brief → three locally reviewed HTML proposals → user style selection and recording in both design documents by create-designs → complete screen/component review → full design approval → Design tickets → FE/BE issues → dispatch → verified review
                                                  ↕ sync confirmed records within authorized scope
```

## Next-command selection and recommendation

End each LinearBoard command response with a **Recommended next step:** block. When recommending a command, lead with its name and why it moves the project forward. Then show the applicable scope choices for that same command. Choose the command using the user's current objective, chat context, and verified LinearBoard records, including completed work, remaining milestones, and dependencies. The last command's scope informs the recommendation. A prior run for one milestone alone does not limit the next recommendation to that milestone. Respect explicit limits on what the user wants considered. A recommendation grants no authority to execute.

Choose the form of the block in this order:

1. **Continue the current command when a reply is pending.** Name the exact response needed and the active command it resumes. PRD clarification, style selection, full visual approval and approval of a presented sync proposal are continuations. Put the question or approval scope above the block. Reuse an answer or approval that already covers the exact decision.
2. **Recommend a new command when its inputs are ready.** Use the [Commands](#commands) section for exact invocations in backticks, with resolved arguments. Show both choices when they offer distinct, meaningful scopes for the same command.
   - **Focused scope** · Give the invocation for the most relevant milestone, batch, issue selection, or other supported scope. Explain when to choose it.
   - **Full scope** · Cover all eligible work in the resolved project that serves the current objective. Give a supported project-wide invocation when available. If the command requires narrower arguments, list the exact invocations for the eligible scopes in dependency order where needed. Use an all-scope argument only when the command documents it.
   - Show one invocation when the command has only one applicable scope or the choices would be identical. Briefly identify any work excluded by an unmet prerequisite and distinguish it from work that can start now. If another supported command can resolve the prerequisite first, recommend that command when it better serves the objective. Preserve any explicit preview-only or read-only boundary.
3. **Name the immediate action when no command applies yet.** Examples include supplying the missing project or access, reviewing an item already in In Review, or opening a fresh project chat to load `init` configuration. Say when the requested workflow is complete. Avoid guessed arguments, invented commands, a generic `sync`, and a repeated `dispatch` that cannot make progress.

For offline `help` or chat-only planning, use the supplied context without looking up a candidate project. When the project is resolved, check relevant records and reuse completed work. Consider other milestones when they serve the user's current objective and flag any scope whose readiness cannot be verified.

Use this order for the applicable deliverables:

| Evidence for the relevant work | Next command or continuation |
| --- | --- |
| Vision needs clarification | Continue `planning`. When the vision is ready and the next deliverable is the native document, recommend `create-vision-document`. |
| A chosen stack or shared constraint warrants a missing technical baseline | `create-technical-baseline <Project>`. Otherwise proceed to milestones if they are missing. |
| Native milestones or their grouped stories are missing | `create-milestones`. |
| Required PRDs or their View are missing | `create-PRDs <Project> <Milestone>`. A consequential question on saved PRDs stays in the built-in clarification loop. |
| A confirmed decision needs material edits to linked records outside the current command | Recommend a scoped `sync` using the affected records or topic. If the proposal has been presented, ask for approval of those edits to continue the same run. |
| The design direction is open or its two canonical documents are incomplete, and the approved-static route below does not already satisfy design readiness | `create-designs <Project> <Milestone>`. Reuse a confirmed choice for the same scope and version. |
| A style is selected and the remaining visual coverage, complete-set approval or required Design handoff is pending, and the approved-static route below does not already satisfy design readiness | `create-visuals <Project> <Milestone>`, or continue that run if it is already awaiting approval or finishing the approved handoff. |
| Required frontend or backend tickets or their Views are missing | Give the exact `create-issues-FE` or `create-issues-BE` invocation for the missing side. If both are missing, choose the side that owns the first prerequisite and explain the other above the line. |
| Multiple delivery issues need ordering and no verified batch or explicit bounded selection exists | `organize-task-batch <Project> <Milestone>` with issue IDs if the scope is narrower. |
| A verified batch has ready work and the required references and execution target are accessible | `dispatch <Project> <Milestone> Batch <n>`. Keep the full batch in the command and explain its internal sequence above the line. A verified native `Batch N` label suffices. A separate saved batch record is optional. |
| A user-authorized issue subset is ready, or ready work has no applicable batch | `dispatch <Project> <Milestone> <issue IDs>`. |
| The only remaining gate is a user decision explicitly required for the issue | Ask for that decision on the named issue and its evidence. The assigned reviewer applies the status policy when the gate is met. |

Use applicable stages only. Canonical requirements can establish that a BE-only or non-visual scope can skip design and visuals. Skip both design routing rows when the user explicitly chooses approved static visuals and the verified approval and accessible images cover the exact scope and visual version. An explicitly requested design deliverable still applies. Follow [delivery issue readiness](references/create-delivery-issues.md#sources-and-scope) for this route. If dispatch preflight finds a material blocker, name it and use the rules above. Ready work in the same authorized scope can proceed independently.

## LinearBoard is the sole product-work system of record

When a delivery issue cites a visual reference, link the owning LinearBoard record or its native Approved JPG attachment and identify the screen and visual version. Verify that the JPG is accessible from the issue.

Exploratory planning and draft discussion may remain in chat; saving them as a canonical record requires an authorized LinearBoard write.

All saved project-management and product-delivery records must be created, read, updated, linked, reviewed, and retained in the LinearBoard app. This includes PRDs, user stories, acceptance criteria, requirements, decisions, research summaries, issue state, dispatch records, coding-agent reports, implementation evidence, approvals, and delivery audits.

- Never create or maintain a local PRD, issue database, ticket board, backlog, status file, traceability file, agent-report archive, or project-management document.
- Never treat a repository file, chat response, or coding-agent message as the canonical product record.
- Keep source code, tests, configuration, migrations, runtime assets, reproducible application artifacts, and repository engineering instructions such as `AGENTS.md` in the repository. Keep product-management records in LinearBoard.
- Except for the visual-review bundle below, a task-owned local file may be used only as temporary upload or conversion staging when LinearBoard cannot accept content directly. After upload, retrieve LinearBoard to verify the canonical copy, then remove the exact temporary file.
- If LinearBoard access, the target workspace/team/project, or required permission is unavailable, stop the affected operation and report the blocker. Do not fall back to local files.

Both `create-designs` and `create-visuals` deliver versioned, runnable HTML mockups with local assets, fixtures, direct links and an offline review index. Keep the bundle in the workspace and share its links in chat. In LinearBoard, record decisions, screen IDs, visual versions and approval. Do not put local filesystem paths, file URLs, or copyable prototype addresses in documents, issues or comments. Use native Approved JPG attachments and links between LinearBoard records for the visual handoff. Before complete-set approval, screenshots require a separate request. After approval, every Design issue must include its confirmed visual references uploaded as JPG images.

Skill-internal templates under `assets/templates/` are authoring instructions, not project records. Use them to create native, rendered LinearBoard content; never copy them into the product repository as deliverables.

Use English for new document titles and preserve official project and product names. Reuse existing document IDs when a title change is requested.

Use these English document title patterns:
- Product vision: `<Idea> — Product Vision`
- Technical baseline: `<Project> — Technical Baseline`
- Milestone plan: `<Product> Product Milestones`
- Design overview: `<Project> <Milestone> — Design Overview`
- Screen specification: `<Project> <Milestone> — Screen and Interaction Specification`

For project-wide design documents, omit the milestone and its separator.

For all milestone-scoped issue commands, follow [tracking labels](references/requirement-labels.md). Use native issue relationships for confirmed issue dependencies and readable links to document sections. Keep source-tracking schemas out of generated descriptions and documents. Read-only commands report drift without repairing it.

## Commands

Interpret a leading command when supplied. Otherwise run the smallest command sequence that satisfies the request.

- `init <Project> [repository path]`: resolve the project/repository, then create or safely refresh AGENTS.md and project Codex agents. Preserve customization, define command/agent responsibilities and linked-document impact review, and show each agent with one-sentence `role` and supported `commands`. Run no product workflow or hook installation. Read [initialization](references/init.md).
- `help`: read only the bundled [help list](references/help.md). Return each command and its argument syntax verbatim as a bullet, with one nested, one-line purpose in the user's preferred response language. Omit examples and surrounding commentary except for the required final recommendation. Handle help offline before application preflight or project selection.
- `planning`: develop a What / Why / Who / Where / How vision in chat and check official sources when the user has chosen a tech stack. Ask which project the user means before any project-specific operation if the destination is uncertain. Save only when requested. Read [planning](references/planning.md).
- `create-vision-document`: create or revise the native vision Project Document. Read [vision workflow](references/create-vision-document.md) and [template](assets/templates/vision-template.md).
- `create-technical-baseline <Project>`: create or revise one project-wide native Project Document covering technical requirements, feasibility, limitations, built-in features, suggested checks and open decisions. See [baseline workflow](references/create-technical-baseline.md) and [template](assets/templates/technical-baseline-template.md).
- `create-milestones`: derive meaningful delivery or learning outcomes from the vision, create native milestones, and document them with supporting stories where applicable. Read [milestone workflow](references/create-milestones.md) and [template](assets/templates/milestones-template.md). Creates no UserStory issues or View. `create-userstories`, `user-stories` and `stories` are compatibility aliases for this same merged command, not a separate issue-creation stage.
- `create-PRDs <Project> <Milestone>` (`create-prds`, `prd`): create or revise milestone-linked ProductRequirement issues, relations, labels and saved View, then automatically begin PRD demystification from the saved items: use the [live QA format](references/create-prds.md#format-each-live-qa-question) for one consequential question at a time and verify each answer in its owning PRD body and comment. Read [PRD workflow](references/create-prds.md), [requirements chain](references/requirements-chain.md), [labels](references/requirement-labels.md), [issue governance](references/issue-governance.md) and [Views](references/issue-views.md).
- `create-designs <Project> <Milestone>` (aliases: `prototype-ui-issues`, `Prototype UI Issues`, `prototype-ui`, `Prototype UI`): read existing design documents or use the brief when either is missing. Use that context to build exactly three distinct brand directions. Apply the design principles, including task-based navigation across screens, and review the complete journey as specified in the design workflow. Use HTML, Tailwind CSS and JavaScript for motion and component feedback. Present the runnable versions and record the user’s style choice here. See [design workflow](references/create-designs.md).
- `create-issues-FE <Project> <Milestone>` (`create-issues-fe`, `build-ui-issues`, `Build UI Issues`, `build-ui`, `Build UI`) and `create-issues-BE` (`create-issues-be`): create or revise the requested implementation side and saved category View. Read [delivery issues](references/create-delivery-issues.md), [issue governance](references/issue-governance.md) and [Views](references/issue-views.md). New issues remain in Backlog; dispatch is separate.
- `organize-task-batch <Project> <Milestone> [issue IDs]`: organize delivery checkpoints and apply one filterable native Batch N label to each selected FE/BE issue. Read [task-batch organization](references/organize-task-batch.md).
- `create-visuals <Project> <Milestone>`: extend the direction selected in `create-designs` across the remaining scoped screens and states and submit the complete set for review. See [visual workflow](references/create-visuals.md).

- `dispatch <Project> <Milestone> [Batch <n> | issue IDs]`: dispatch only the authorized issue selection, validate worker plans, then assign independent verification and ticket status updates. Read [dispatch](references/coding-dispatch.md) and [issue governance](references/issue-governance.md).
- `debug [Project] [Milestone] [report or issue IDs]`: the coding agent records the report and expectation in its BUG ticket, investigates, fixes, verifies and comments directly there. Triage-only stops after recording. Read [debug](references/debug.md), [issue governance](references/issue-governance.md) and [Views](references/issue-views.md).
- `sync <Project> <Milestone> [scope or new request]`: review affected documents, milestones, issues, acceptance criteria and relations. First show one proposed from/to block per affected record in chat and wait for explicit approval. Apply only approved changes, including specified UI evidence updates, then read back the results. Read [sync](references/sync.md).

Planning checks a user-chosen stack against the core product flows. Detailed SDK and deployment research starts at FE/BE issue creation. Carry unresolved implementation questions forward to those issues. Technology lookup and selection run internally within `create-issues-FE` and `create-issues-BE`; they are not separate user commands.

Creating a draft in LinearBoard is a mutation and requires a user request that authorizes creation or editing. A read-only review or explanation preserves the board. An authorized delivery review includes the scoped evidence and status updates defined below.

Every actual issue-creation command also creates or reuses its project/category LinearBoard View as part of the authorized output, including when matching issues already exist. Follow [issue Views](references/issue-views.md) for `create-PRDs`, `create-issues-FE`, `create-issues-BE` and their aliases, plus the post-approval Design-ticket stage of `create-visuals`; `debug` BUG tickets reuse the matching FE/BE View or create it if missing. `create-designs` and the merged `create-milestones`/story aliases create no issues or View. A label, unsaved filter or chat link is not a saved View. Read-only commands do not create Views.

## Shared command invariants

Apply the [shared change review](references/change-review.md) when creating or clarifying PRDs, handling a user change or worker conflict in any command, reconciling affected records, and at dispatch readiness and final handoff.

Both design commands apply [shared design integration](references/design-direction.md). Use the bundled [design-pro skill](../design-pro/SKILL.md) within the current command for creative judgment and focused critique, and the Uiverse MCP for suitable component references when needed. LinearBoard controls deliverables, board writes, user selection and complete-set approval.

For all UI design, build, dispatch and review, resolve the requested target platform/stack using [platform scope](references/design-direction.md#target-platform). Never add paired Web/Mobile layout checks or screenshots by default; their separate application stacks require separate authorized scopes.

Use supplied context and do not rerun earlier stages as a ritual. Ask only when missing information materially changes destination, scope or product behavior. Preserve unknowns instead of inventing evidence, ownership, estimates, dates, approvals or decisions.

Vision, Technical Baseline, grouped milestone/story overview and design specifications are native Project Documents. User stories are stable entries in the milestone document; PRDs are native milestone-linked issues. Existing UserStory issues and QA documents are preserved historical sources, not mandatory new outputs. Record shared technical requirements in the baseline when available. Record feature-specific frontend and backend decisions in the delivery tickets that own the work. Read back native parents, fields, labels, relations, rendered content and requested View membership; prose alone does not establish an association.

Creation commands authorize only their named artifacts, including local mockup code for both design commands. They do not authorize later commands, production implementation, dispatch, unrelated uploads or status changes. A new product may receive the minimal project container required for explicitly requested artifacts only when destination and scope are clear.

For any issue creation or classification, follow [issue governance](references/issue-governance.md). For any application write, read [application operations](references/linearboard-operations.md). Read only the command references routed above.

## Issue governance

Use [issue governance](references/issue-governance.md) as the single authority for Category labels, delivery issue shape and titles, allowed status transitions and the post-write issue audit. A command-specific instruction to preserve status or forbid issue creation always takes precedence.

## Conditional references

The command list above is the routing map; do not load unrelated references. For every LinearBoard mutation, also read [application operations](references/linearboard-operations.md). For issue mutations, read [issue governance](references/issue-governance.md). When the resolved project is PocketStocks and the authorized scope contains user-visible UI delivery, additionally read [PocketStocks delivery exception](references/pocketstocks-delivery.md).

## Review handoff and final acceptance

Across LinearBoard projects, the assigned delivery reviewer independently verifies
the delivered work, records evidence on each assigned issue, applies the
appropriate status and reads it back. The main agent fills that role when no
reviewer is assigned. The user's standing instruction authorizes the reviewer
to apply these outcomes within an authorized delivery review.

- **Done:** All applicable required acceptance checks passed on the specified
  target and any explicitly required user acceptance is recorded. Use the
  native LinearBoard UI for Done.
- **Todo:** A required check could not run because of an evidenced test
  restriction, such as unavailable test credentials, devices, environment or
  a user-deferred live check. Record what passed, what remains untested and
  the prerequisite to resume. Use the team's existing Todo equivalent when
  named differently.
- **In Progress or Blocked:** A product defect, implementation gap or failed
  required check needs remediation. Record the failure and route it back.
- **In Review:** The review is still underway or an explicit issue-specific
  acceptance decision is pending. Record the outstanding gate.

For a test restriction, identify the exact criterion, environment, observed
restriction, impact and next verification action. Record it as `Not tested` or
`Environment-blocked`. Preserve the actual results and supporting evidence.
A substitute environment only satisfies a requirement if the accepted test
contract permits it. If the reviewer lacks access to complete an authorized
status action, hand the exact issue and evidence to the main agent for the
supported action and verify the result before reporting it as changed.

## Dispatch and independent review

Dispatch only the explicitly authorized issue selection. The TPM retains dispatch records and integration. Each implementer owns one bounded, non-overlapping issue. The delivery reviewer owns its assigned verification evidence and status. Use at most three concurrent workers, validate each plan before implementation, and require reports for acknowledgment, completion, blockage or failure. A report is a claim, not verification.

Read [coding dispatch](references/coding-dispatch.md) for readiness, worker lifecycle and independent checks. Operate the actual target UI for user-visible work; passing tests, deployment status, static inspection or a worker screenshot alone do not prove the flow. Use credentials only when the authorized test requires them, project instructions permit them and they are safely available; never expose or modify them. Project-specific PocketStocks rules live only in [PocketStocks delivery exception](references/pocketstocks-delivery.md).

## UI implementation review gate

Every dispatched issue that changes or verifies user-visible UI must pass the independent gate in [coding dispatch](references/coding-dispatch.md#ui-implementation-review-gate) before closure. An evidenced test restriction on the required target or comparison follows the Todo rule. Evidence screenshots prove the inspected implementation state; they never become a canonical design.

## Authorization boundaries

- Creating or editing LinearBoard records requires an explicit request that covers the target scope.
- During proposal review, `create-designs` reads LinearBoard and delivers three local HTML proposals and an index. Keep pending decisions and proposal checks out of LinearBoard, including comments. Only after explicit user confirmation of the direction may it update the two design documents with the selected version and styling. Production changes, issue creation, Views and dispatch require their own stages.
- `create-visuals` authorizes isolated mockup code, browser checks, an HTML review index and canonical workflow comments within scope. Production code/live integrations remain outside it. Follow [the visual workflow](references/create-visuals.md) for style confirmation and complete-set approval. Complete-set approval authorizes the required JPG uploads to the owning Design issues. Confirmed Design JPGs inherit the user’s recorded set approval; other manual attachment approvals belong to the user. Record existing approval once; do not repeat it or infer it from selection. After complete-set approval create/reuse Design tickets/View, preserving existing issue states and product rules.

- `dispatch` authorizes workers only for the exact issues or bounded selection resolved from the user's command. It never authorizes scope expansion, destructive actions or unrelated deployment.
- Status transitions follow [issue governance](references/issue-governance.md). Standing authority never overrides a command that preserves state or forbids status changes.
- The assigned reviewer applies the [review status policy](#review-handoff-and-final-acceptance) within the authorized issue scope. Respect any explicit issue-specific acceptance gate.
- Deletion, reassignment, scheduling, scope changes, uploads and external publication require authority appropriate to that action. Record deletion uses impact preview and recoverable trash; permanent deletion remains a user UI action.
- The TPM writes dispatch records and validates worker handoffs. Under `debug`, the assigned coding agent creates or reuses its BUG ticket and posts its own report and result. The delivery reviewer owns independent verification and its resulting evidence and status.
- Never claim approval, implementation, verification, or completion from an agent's self-report alone.

## Completion criteria

For `organize-task-batch`, completion means the requested FE/BE scope has been reviewed and an ordered checkpoint proposal returned in the required format, with issue coverage, dependencies and blockers explicit. Read back each batch by team, project, native milestone, FE/BE category and Batch N label. Its membership must match the reported issue IDs. Organization does not dispatch work.

For `create-visuals`, follow [stage completion](references/create-visuals.md#gates-and-valid-stopping-points). Verify runnable HTML and the index, record coverage and wait for the applicable user decision. Complete-set approval additionally requires verified Design tickets/View.

For issue creation, completion includes the saved category View, correct team/project/category filters, requested placement and verified membership. Report issue creation and View creation separately if either is blocked.

A `sync` review stops after presenting its proposal. Only if the user approves proposed design or UI evidence updates does completion require the screenshot reconciliation in [sync](references/sync.md): inspect current image coverage, capture missing or stale actual UI states, verify uploaded images in the owning records, and identify any unavailable state without substituting a mockup or claiming screenshot completeness.

For `debug`, verify the report, expectation and source links on the BUG ticket. After implementation verify the coding agent’s concise status, cause, action and check comment on that same ticket. Triage-only ends after ticket readback.

For commands that mutate LinearBoard records or dispatch implementation, complete only after every check applicable to that command and authorized scope has been verified. Command-specific completion criteria above take precedence; do not require issues, agents, implementation evidence, status transitions or LinearBoard uploads from commands that do not produce them. Never claim an applicable check passed when it was not performed, and retain no prohibited task-scoped local product-management artifacts.

## Final report

Report only the items applicable to the command: the resolved LinearBoard team/project; canonical documents or issues changed; traceability; visual-review artifacts; agents and reports; verification; ticket transitions; approvals; blockers; and confirmation that no prohibited local product-management copies were retained. Distinguish draft, implementation complete, ready for review, remaining environment checks and final-user acceptance where relevant; do not collapse them into a blanket completion claim.

Place the recommendation defined in [Next-command selection and recommendation](#next-command-selection-and-recommendation) after all report text and links, including for read-only, partially completed and blocked commands.
