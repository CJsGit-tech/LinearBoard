# Organize task batches

Use for `organize-task-batch <Project> <Milestone> [issue IDs]`. Review existing FE/BE delivery issues and propose batches that each lead to a reviewable delivery checkpoint. The invocation authorizes applying native batch labels to selected delivery issues and reporting the ordered checkpoints. An explicit preview-only request skips all writes. Save a separate batch record only when explicitly requested. Do not implement or dispatch agents.

## Review the requested scope

- Resolve the exact LinearBoard team, project and milestone from the arguments or existing context. Accept an explicit issue selection without forcing repeated project arguments. Ask only when the destination or selection is genuinely ambiguous.
- Retrieve all in-scope FrontEnd and BackEnd issues with pagination, including descriptions, acceptance criteria, current status, native dependencies and source US/PRD links. Use native Category membership and issue content rather than title prefixes alone; flag conflicting or unclear classification without changing it.
- Read the relevant source requirements, milestone completion gate, shared contract owners and approved design references needed to understand the checkpoint. Treat confirmed app-local data/service work as BE where that is the project's scope; do not assume BE requires a server.
- Account for every selected FE/BE issue exactly once in the proposed work batches or explicitly explain why it is excluded. Completed, canceled and duplicate records provide context rather than proposed new work; distinguish review-ready and active work from work yet to start. If a required record is inaccessible, state the resulting coverage gap instead of claiming a complete review.

## Form delivery checkpoints

Group by a coherent user outcome or a necessary shared capability with observable acceptance. Prefer a usable flow that joins its FE and BE work when both are needed. Avoid grouping only by implementation layer, similar titles or arbitrary issue counts. A batch may contain only FE or only BE when it delivers a meaningful checkpoint; write `None` for the empty side.

Order batches by real prerequisites. Identify shared contract owners, integration order and external dependencies under the grouping rationale. Distinguish recorded dependency relations from inferred sequencing recommendations. Flag cycles, missing contracts, ambiguous requirements and unavailable references; do not silently resolve them or invent tickets. Do not duplicate a shared owner across batches: link its owning batch as a prerequisite for consumers.

A delivery batch is not a concurrent worker allocation. Do not impose the dispatch workflow's three-worker limit on batch size or imply that all issues in one batch can execute simultaneously. Keep existing issue boundaries; propose a split only as an unresolved recommendation when an issue prevents an independently reviewable checkpoint.

Define expected checkpoint outcomes as observable behavior or concrete service/data results grounded in the existing acceptance criteria. State the relevant verification scenario and any prerequisite that prevents it. These are future completion criteria, not claims that implementation or tests have passed. Do not invent estimates, dates, approvals or new product scope.

## Tag and verify the checkpoints

Use reusable, active team labels named exactly `Batch 1`, `Batch 2`, etc. Resolve a batch with the exact project AND native milestone AND that label, across both FrontEnd and BackEnd. A label by itself is team-wide. Keep the native milestone, M-number, US, Coder, Category and unrelated labels.

Before writing, page through existing labels, tagged FE/BE issues and saved batches. Reuse matching assignments on reruns. For partial selections, preserve existing checkpoint numbers and members outside the selection. Do not merge new work into an unrelated numbered batch. Surface conflicts with saved membership or ambiguous label definitions before modifying affected issues.

Create missing batch labels once. For each selected eligible ticket, read its current version and replace only conflicting numbered batch labels with its intended label. Skip already-correct tickets. Use the ordinary versioned issue update and stable retry keys. Re-read on conflicts. Do not change status, assignee or dependency relations.

For each checkpoint, query both categories by project, milestone and label with pagination. Compare IDs against the intended full membership (including retained members for partial selections). Check each changed issue has exactly one numbered batch label and preserves all other labels. Report verified counts or exact outstanding mismatches. If a write fails partway, report the verified subset and resume idempotently before dispatch. A verified label selects the full batch in `dispatch <Project> <Milestone> Batch <n>`. Use that form in the final recommendation for the first actionable checkpoint. Explain the order of ready prerequisites and dependent issues above the line. Dispatch applies its own readiness checks.

## Required output

Start with a short scope line naming the resolved team/project/milestone or explicit selection. Repeat the following five headings exactly, in this order, for each batch; put the actual batch name below `### Batch Name`. Use Markdown, not a shell code block.

```markdown
### Batch Name
Batch 1 — <checkpoint name>

### FE Issues
- [<issue identifier> — <title>](<LinearBoard issue URL>) — <contribution to this checkpoint>

### BE Issues
- [<issue identifier> — <title>](<LinearBoard issue URL>) — <contribution to this checkpoint>

### Why the above issues are grouped
<Shared outcome, integration relationship, prerequisite batches and relevant blockers.>

### Expected Checkpoint Outcomes
- <Observable outcome and the scenario or check that would demonstrate it.>
```

Use real issue identifiers, titles and links retrieved from LinearBoard. Place status qualifications beside affected issues. After the batches, briefly account for excluded records and unresolved coverage gaps when present. If there is no eligible work, say so directly rather than producing empty batches. Do not add a full delivery/dispatch report to this proposal.
