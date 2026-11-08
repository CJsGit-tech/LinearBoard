# Coding-agent dispatch

Read this reference before spawning any coding agent. `dispatch` is an implementation orchestration command tied to named LinearBoard issues. Dispatch does not authorize scope expansion, destructive operations, unrelated deployment or marking work complete. Load a project-specific delivery reference only after resolving the project and scope.

## Invocation and bounded selection

- Parse a command only when the user asks to run dispatch. Editing or explaining the skill, or quoting an example, does not start implementation.
- A dispatch request authorizes readiness preflight for its bounded selection, not creation of missing upstream artifacts. Product-decision completion alone is never dispatch readiness. If design records, approved UI references, FE/BE issues, execution access or another material input is missing, leave the affected issues unchanged, report the exact missing gate and recommend the first incomplete applicable command using [the skill router](../SKILL.md#next-command-selection-and-recommendation). If a supported upstream command can resolve the blocker, recommend that command. If user action or access is needed, name the exact prerequisite. When resuming is possible, keep the original batch or issue selection in any conditional dispatch recommendation.
- `dispatch <Project> <Milestone> [Batch <n> | issue IDs]`: the explicit arguments control the scope. Resolve the exact LinearBoard project/team and native milestone, including milestone aliases such as `M1`. Do not substitute the current browser View, latest milestone, previous batch, working-directory name or remembered project.
- With no batch or issue IDs, inventory all existing FrontEnd/BackEnd implementation issues in that project’s native milestone, with pagination. Apply status eligibility and readiness separately; include both FE and BE rather than only the visible View. Report excluded and unready issues with reasons. If none are eligible and ready, report no dispatchable work without reopening review/completed tickets or creating replacement work.
- With `Batch <n>`, resolve the exact active team label `Batch <n>`, then query both FE and BE issues by the resolved project, native milestone and label ID with full pagination. Freeze the resulting IDs before readiness checks. Reject multiple batch tags on a member. When a saved batch exists, compare its IDs to tagged membership and pause on disagreement or partial tagging. For historical untagged batches only, use an unambiguous saved or previously agreed exact selection after checking scope. Never expand an empty or ambiguous batch to the whole milestone.
- With issue IDs, include only those IDs and verify their project/milestone membership. Existing `dispatch <issue IDs>` and other explicitly bounded selections remain supported; resolve omitted project/milestone from current records. Ask only when a material boundary is ambiguous.
- Before spawning, state the resolved project/team, native milestone, optional batch, exact issue-ID snapshot and execution target. This is a scope statement, not a repeated approval request.
- Work only within the resolved snapshot. Do not enroll newly created tickets or out-of-scope prerequisites automatically. Report outside-scope blockers and continue independent ready work.
- A batch invocation authorizes the full frozen membership as the work scope. Start ready prerequisites first and keep internally dependent issues in that same invocation. Recheck and start a dependent issue when its prerequisite contract has been verified and its own readiness gates pass. No second dispatch request is needed for that issue. Report any issue that remains unready and the prerequisite that still prevents it from starting.
- Inspect current assignment comments and live agent/thread/worktree evidence before spawning. Reuse or wait for an authorized live assignment with the same scope; never spawn a second worker for the same ticket or steal ownership. A stale comment alone does not prove a worker is running. If activity cannot be determined, report that ticket as unresolved rather than duplicate it.
- Approved images, design documents/screen specifications, PRDs and US are sufficient product inputs when they cover the assigned scope. A Design issue or clickable prototype is optional. Use [the visual approval gates](create-visuals.md#design-approval-and-native-attachment-state): exact-scope recorded design approval plus accessible exact images is sufficient; the native attachment field remains separately user-controlled. Read applicable technical decisions in the owning frontend or backend tickets.

## Product integration and execution target

The command selects the product and milestone, not a test host or an auxiliary target. Resolve the repository and actual product entry point from current LinearBoard records, repository instructions and build/deployment configuration. The project name may differ from the repository, app name or scheme; verify the mapping rather than using the command text as a build target.

Record the primary app scheme/run target or deployed service URL and any required extensions, packages or secondary targets in each assignment. Keep their responsibilities distinct. Integrate the scoped features into the existing product and verify their real entry points; fixture screens or a separately launched extension do not establish main-product integration. Do not create a second standalone app merely to host an assigned feature.

For native apps with extensions, verify that the normal main-app build includes the required extension and that each feature is reachable through its intended main-app or system entry point. The handoff must state which main scheme the user should Build/Run, what is included, and when a separate extension scheme is useful for debugging. Preserve project-specific deployment and test rules.

## Research and dependency scheduling

An unresolved engineering solution is work, not automatically a readiness failure. Let the owning FE/BE ticket research implementation choices within confirmed product scope. Its initial plan must identify the question, evidence/check, technical decision and consumers. A missing product behavior or a choice that changes scope, privacy, data results or approved interaction requires a user decision; do not silently decide it as engineering.

Give each shared contract (data model, stable identity, file format or service interface) one owning ticket. Start that owner's investigation and validate its resulting contract before dependent integration. Consumers may do independent preparation, but must not implement against speculative contracts. Record the chosen contract and rationale on the owning ticket and link consumers instead of duplicating competing definitions. Detect dependency cycles and surface the concrete cycle; do not pretend an arbitrary order resolves it.

## Status eligibility

Dispatch is prohibited only for issues whose current status is `Canceled`, `Duplicate`, `In Review`, or `Done`. Every other team status is status-eligible; do not exclude an issue based on another status name alone. Status eligibility does not waive the readiness gate: unresolved material blockers, dependencies, missing scope, or missing required inputs still make an issue unready.

## Dispatch readiness gate

Use [shared change review](change-review.md) to baseline source versions, respond immediately to mid-build changes, and compare the latest criteria and references immediately before applying the review outcome.

Retrieve each target issue and its canonical LinearBoard sources. Dispatch only when material product inputs and execution access are available; explicitly owned engineering research may remain as planned work:

- issue identity, team, project, and current state;
- source PRD requirements and product goal;
- primary grouped story entry in the milestone document and acceptance criteria, or an existing legacy story issue/document and its applicable cases;
- dependencies and blockers;
- current approved UI design or UX reference, routes, relevant states, required viewports and the project-required test scenario;
- repository, `AGENTS.md`, starting state, and relevant conventions;
- required tests and verification evidence;
- bounded, non-overlapping ownership for every agent.

Leave unready issues unchanged and report the missing decision or evidence. Other independent ready issues may proceed.

Dispatch only issue IDs or a bounded issue selection the user explicitly authorizes. For a selection such as eligible tickets in a named project, resolve exact IDs during preflight and dispatch only the ready issues that satisfy it. If the project, filter, or scope boundary is ambiguous, report candidates and ask before spawning.

Dispatch every ready issue within the explicitly authorized issue-ID set or bounded selection to a subagent. Process independent issues in parallel in batches of no more than three active workers. Start the next batch only as capacity opens; do not exceed three concurrent workers. Keep tightly coupled integration and TPM review with the main agent. Require every worker to report directly to the TPM agent after acknowledgment, completion, blockage, or failure. Review each completed result before accepting it or proceeding with dependent work.

## Crew selection

Use the smallest crew that fits the work. Keep tightly coupled integration in the TPM/main agent.

- Small isolated change: one implementer, with main-agent review.
- Normal feature: implementer plus independent reviewer.
- Independent frontend/backend scopes: frontend implementer, backend implementer, and reviewer.
- Larger separable feature: data/model, service/API, UI and integration reviewer, staged in batches that never exceed three active workers.
- Existing implementation: spec, code-quality, and test-coverage reviewers as needed.

Never assign two agents overlapping write ownership at the same time. Tell every worker that other agents may be working in the repository and that they must preserve others' edits.

## Required dispatch request format

Populate [the Markdown request template](../assets/templates/coding-agent-contract.md) from the current issue and canonical sources. Every request uses **Scope → Review → Plan → Execute → Verify and Report**. Include the acceptance criteria, relevant source content and canonical links, ownership, exclusions, dependencies, environment, checks and report recipient; do not rely on inherited chat history to carry essential instructions. For UI work, supply the exact approved visual links and versions, routes, states, viewports and test scenario. Workers must open the visuals, not merely read their descriptions.

Use the issue's acceptance criteria and linked story criteria or test cases where specified. `TC-xx` identifies an existing case within a legacy story document, not a separate ticket. Story issues need no new test-case document or invented case IDs. Qualify numbered cases with their source, such as `US-05 / TC-06`; do not invent case IDs or require new TC issues.

The worker first reviews the sources and existing implementation. For UI work, it also inspects the approved visuals and current deployed UI. Its `acknowledged` report must identify sources and visual versions actually reviewed, routes/states/viewports inspected, observed differences, a bounded plan and a criterion-to-check table. Missing access or conflicting requirements require a specific `blocked` report.

The TPM checks source coverage, scope, visual understanding, ownership and planned verification, then explicitly releases the worker to execute. An acknowledgment alone does not authorize implementation. This is a TPM checkpoint, not a new user-permission request. Return incomplete plans for correction. Material discoveries that invalidate the plan require another TPM check before dependent work continues.

Preserve applicable repository and project-specific delivery rules in the request. Worker checks never replace independent delivery review.

## Mandatory report-back lifecycle

Apply the [review status policy](../SKILL.md#review-handoff-and-final-acceptance) to the actual evidence for each issue.

The TPM owns dispatch and integration records. The assigned reviewer owns verification evidence and resulting status for each assigned issue. Under `debug`, the coding agent records the report and result on its own BUG before independent review.

```text
LinearBoard issue ready
    ↓
TPM dispatches agent
    ↓
Agent reviews context and reports acknowledged with plan, or blocked
    ↓
TPM validates the context review and plan, then explicitly releases execution
    ↓
Acknowledged → TPM may update LinearBoard to In Progress
    ↓
Agent implements and reports completed, blocked, or failed
    ↓
TPM validates the completed handoff and may move it to Ready for Test
    ↓
Reviewer independently inspects the delivered target, runs required checks and applies the UI gate
    ↓
Verified → Done via native UI
Required test blocked by a restriction → Todo
Product failure → remediation in an active or blocked state
Explicit acceptance decision pending → In Review
```

Hard invariants:

- Sending dispatch alone is not evidence for a status transition. Scoped dispatch authorizes assignment records and, after their gates, own-ticket plans, technical decisions, reports and evidence.
- The TPM must validate the context-review acknowledgment and plan before releasing implementation or moving a ticket to `In Progress`.
- The TPM must receive a later implementation report before any subsequent implementation-status update. A validated completed handoff may use the team’s existing `Ready for Test` equivalent while TPM review is pending; if absent, retain the active state and record review pending. Do not create a status.
- Agent silence, ambiguous identity, or an incomplete report leaves the ticket unchanged.
- A `completed` report is a claim, not verification.
- The reviewer must inspect the delivered target, apply the UI gate and follow applicable project-specific rules before closing the issue.
- Passing checks, static inspection, a coding-agent screenshot, or a coding-agent claim never substitutes for independent visual review.
- Never claim success from a worker's self-report alone.
- Every transition must satisfy [issue governance](issue-governance.md#status-authority) and the applicable report and verification gates.
- The assigned reviewer records the review evidence, applies the status and verifies it. For `Done`, use the native UI. If unavailable to the reviewer, the main agent handles the supported action using the reviewer’s exact issue and evidence.

## Agent report contract

Use the Plan and Verify and Report sections of the request template. A completion handoff must identify the exact issue, delivered changes, source or deployment details, criterion/test-case results and evidence, UI comparison where applicable, remaining discrepancies, scope deviations and blockers. Report `Pass`, `Fail` or `Not tested` for each applicable criterion; a blanket completion claim is insufficient.

## Verification and LinearBoard reconciliation

On report receipt:

1. Match the report to the dispatched agent and exact LinearBoard issue.
2. Compare claimed scope with the dispatch contract.
3. Inspect current source files and diffs, or the actual deployment/runtime results when the project uses a managed deployment workflow; do not rely on message text alone.
4. Run the relevant checks and evaluate applicable linked user-story test cases alongside the delivery issue's own acceptance checks.
5. For user-visible UI work, apply the UI implementation review gate and any project-specific delivery reference.
6. If findings require correction, return a focused task to the responsible agent and wait for a new report. Repeat the UI inspection after every relevant visual remediation.
7. Write the accepted report summary and verification evidence to the issue in LinearBoard, including any project-required visual evidence.
8. The reviewer applies the shared status policy after independent verification. Use `Done` for verified work through the native UI, `Todo` for a required test blocked by restrictions, and the applicable active or blocked state for product failures. Record any explicit acceptance gate that is still pending.
9. Retrieve the issue and verify the comment, evidence, links, attachments and state.

Do not store agent reports in repository files. The canonical accepted report and evidence belong on the LinearBoard issue.

## UI implementation review gate

Apply this gate to every dispatched issue that changes or verifies user-visible UI. A worker's completed report is a handoff for independent review.

Before closing the issue, the reviewer must:

1. Retrieve the applicable story acceptance, requirements, approved visual reference, routes, states and required viewports.
2. Operate the actual target application after the change is present in the project-required environment; record environment, route, session and data scenario.
3. Inspect every required viewport and affected normal, loading, empty, error, interaction, changed and recovery state.
4. Compare behavior and presentation with the canonical sources, separating real data differences from product defects.
5. Return material discrepancies for focused remediation, wait for a new worker report and repeat affected checks.
6. Record dated evidence identifying what was inspected, references compared, findings resolved, checks, limitations and review conclusion. Retrieve the issue and verify its evidence and state.

Passing builds, tests, deployment status, static inspection or worker evidence does not waive this gate. If a test restriction prevents a required target check, record the missing check and apply the shared Todo rule.

If the resolved project is PocketStocks, read [PocketStocks delivery exception](pocketstocks-delivery.md) for AppDeploy, viewport and JPG evidence requirements.

## Automatic own-ticket records and cross-record sync

The TPM records the assignment identity, validated plan, technical decisions, blockers and worker handoff on the owning issue. The assigned reviewer records independent verification and updates that issue’s status. Reuse matching entries and avoid a separate `sync` for routine review. Implementers report to the TPM during ordinary dispatch.

A dispatch does not implicitly authorize rewriting source US, PRDs, QA, Design documents or unrelated Views. When a confirmed decision has authorized cross-record effects, apply [sync](sync.md) within that scope. Otherwise list the affected records and obtain only the missing material edit authorization. Preserve original QA answers and revisions; do not turn an engineering proposal into a confirmed product decision.

For FE, verification includes the actual affected UI interaction and comparison to the exact approved visual. For BE, verify resulting data and applicable deduplication, write consistency, partial failure, retry and recovery behavior. Verify only applicable criteria; report unavailable hardware or runtime evidence as unverified/environment-blocked at the criterion level. Apply the shared status policy to distinguish a blocked test from unfinished implementation. Neither static images nor a passing unit test prove an untested end-to-end flow.
