# Organize task batches

Use for `organize-task-batch <Project> <Milestone> [issue IDs]`. Review existing FE/BE delivery issues and propose batches that each lead to a reviewable delivery checkpoint. This command is read-only and returns a proposal in chat. It does not create or edit issues, relations, labels, statuses, milestones, Views, assignments or dates; save a canonical plan in LinearBoard only when explicitly requested. Do not implement or dispatch agents.

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
