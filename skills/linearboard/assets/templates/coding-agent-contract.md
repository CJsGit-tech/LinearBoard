# Coding-agent request template

Populate this Markdown template in the dispatch prompt. Omit inapplicable fields, resolve placeholders and include essential source content alongside canonical links. Do not save populated requests or reports as project files; the TPM records accepted plans, reports and evidence in LinearBoard.

## Assignment: [LinearBoard issue ID — title]

### Scope

- **Dispatch scope:** [user command, resolved LinearBoard project/team, native milestone, optional batch and authorized issue-ID snapshot]
- **Product execution target:** [verified repository and primary app scheme/run target or deployment URL; required auxiliary targets and real product entry points]
- **Assignment identity:** [issue ID, agent/run identity, source versions; include in every report]
- **Research and contract ownership:** [engineering question, evidence/check, owning ticket and consumers; omit if none]
- **Issue and outcome:** [canonical URL and expected user outcome]
- **Acceptance criteria:** [current issue criteria]
- **Sources:** [linked grouped story document entry or existing legacy issue and acceptance criteria, or selected legacy document and existing test cases; requirements, existing technical context if available, approved design handoff and visual versions]
- **Ownership:** [files, modules or managed delivery target]
- **Exclusions and dependencies:** [non-goals, areas to avoid and prerequisites]
- **Environment:** [repository starting state or managed deployment, routes and test scenario]
- **Checks and evidence:** [required verification and evidence]
- **Report to:** [TPM agent or chat]

The current issue and canonical references define scope; conversation history does not expand it. Follow `AGENTS.md`, preserve others' changes and do not update LinearBoard.

### 1. Review

Read the issue and listed sources. Inspect existing implementation and reusable patterns through the authorized workflow.

For UI work, open and inspect the exact approved visuals and current target routes and states at the project-required viewports. A visual description is not image inspection.

Report inaccessible sources, conflicting requirements or unresolved dependencies; do not assume missing context.

### 2. Plan

Send the TPM:

- **Status:** `acknowledged` or `blocked`
- **Issue and understood ownership**
- **Sources reviewed:** documents and visual titles/versions
- **UI inspected, when applicable:** routes, states, viewports and differences from approved references; distinguish data differences from defects
- **Implementation steps:** bounded changes and reused patterns
- **Verification plan:**

| Acceptance criterion / linked story test case | Planned change | Check |
| --- | --- | --- |
| [criterion or source-qualified case] | [change] | [observable result] |

- **Blockers:** specific unresolved items, or `None`

Wait for explicit TPM validation before implementing. This is an internal checkpoint, not a request for user permission.

### 3. Execute

Research and implement the validated plan within your ownership. Report technical findings, supporting evidence, chosen contract and consumer impact to the TPM before dependent integration. Escalate any choice that changes confirmed product behavior; do not invent it. Approved images can be sufficient design input; no separate clickable prototype or Technical Baseline is required. Report material scope or plan changes before proceeding with dependent work.

Follow any project-specific delivery reference supplied by the TPM. Coordinate shared-target writes, wait for terminal deployment status when applicable, and inspect the actual QA/runtime result.

### 4. Verify and Report

Check each acceptance criterion and applicable linked story test case. For UI changes, operate the changed actual target in the project-required environment at the required routes, viewports and states; compare it with approved visuals, fix in-scope discrepancies and repeat affected checks.

Return:

- **Status:** `completed`, `blocked` or `failed`
- **Issue, delivered changes and ownership**
- **Delivery:** changed files where applicable, or managed app/environment/deployment version and terminal status
- **How to run/review:** primary app scheme or deployed URL, included extensions/auxiliary targets, verified product entry points and any required setup; distinguish fixture/debug-only entry points
- **Results:**

| Acceptance criterion / linked story test case | Pass / Fail / Not tested | Evidence or limitation |
| --- | --- | --- |
| [criterion or source-qualified case] | [result] | [evidence] |

- **UI evidence, when applicable:** routes, states, viewports, visual versions compared, resolved discrepancies and project-required screenshots or visual evidence
- **Remaining discrepancies, scope deviations, risks or blockers:** distinguish product defects/essential verification gaps from narrowly evidenced environment-only limitations; include affected criteria, cause evidence, impact and next verification action. Keep unverified checks `Not tested` or `Environment-blocked`.
- **Recommended ticket state:** state whether implementation is ready for human review and why; an environment-limited check is not automatically unfinished implementation.

Keep credentials out of reports and evidence. The TPM independently verifies results and reviews the actual target UI before `In Review`, applying [review handoff and final acceptance](../../SKILL.md#review-handoff-and-final-acceptance). A qualifying environment limitation stays explicit in the handoff; only the user owns final acceptance and `Done`.
