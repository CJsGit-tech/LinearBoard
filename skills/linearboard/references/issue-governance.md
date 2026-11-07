# Issue governance

Read this reference for commands that create, restore, classify, rename or transition LinearBoard issues. Command-specific rules still control whether a field may change; this reference does not expand mutation authority.

## Category

Every new issue, and every reused or restored issue within an authorized creation or metadata-repair scope, carries exactly one child of the team's native single-select `Category` label group:

| Purpose | Category |
| --- | --- |
| Existing legacy user-story issue | `UserStory` |
| PRD issue | `ProductRequirement` |
| Approved design handoff issue | `Design` |
| UI/frontend implementation or fix, including native mobile UI | `FrontEnd` |
| Backend service/API or confirmed app-local data/service work | `BackEnd` |

Category describes responsibility; Status describes progress. Project Documents have no issue category. Do not invent another category or create workflow states for categories.

Read the team's accessible labels and groups. Reuse the active `Category` group and exact child; create a missing team-scoped group or child only within an authorized issue-creation scope. Never apply the group container, reuse an unrelated same-named label, reparent a shared label or create a duplicate group. Include the category on creation with applicable role labels and the milestone and mapped source-story tags, then retrieve the issue and verify exactly one Category child. Add a missing category to a reused issue only when the command authorizes that metadata repair; preserve unrelated fields and labels.

`create-designs` creates documents only. `create-visuals` creates or reuses Design issues only after explicit approval of its complete requested design set; follow [post-approval Design tickets](create-design-tickets.md). Earlier exploration and generation never create Design issues. Preserve existing legacy records unless their reuse is authorized by that stage.

## Delivery issue model and titles

Keep one delivery issue to one independently buildable and reviewable feature. Link its primary story entry in the milestone document and applicable acceptance criteria; legacy issue sources may be linked when they already exist. Do not create story issues to satisfy delivery traceability. Existing legacy documents and real `TC-xx` cases remain usable sources. Implementation issues retain the `Coder` role label and the appropriate category.

Place a tangible **Expected output** section near the top. Use unchecked task-list items for actionable scope, output, acceptance and report-back work. Keep context, dependencies, constraints and exclusions as prose or ordinary bullets.

User stories use `{stable story ID} — {user outcome}`. PRDs use `{stable PRD ID} — {capability or outcome}`. They do not use delivery prefixes.

Debug issues use `BUG {feature} — {observed problem}`. Other new or explicitly renamed delivery issues use:

```text
{Prefix} — {Screen or capability} [v#] — {shared outcome}
```

| Responsibility | Prefix |
| --- | --- |
| New UI capability or initial screen | `Build UI Feature` |
| Approved next visual version of an existing screen | `UI Revision` |
| UI behavior or presentation defect | `Fix UI Feature` |
| New backend capability | `Build BE Feature` |
| Backend defect | `Fix BE Feature` |

Use `[v#]` only when a real screen, API or product version is established. A UI fix names the version it corrects but does not create a new visual version. Derive versions and supersession from canonical records; do not invent lineage or bulk-rename historic issues.

## Status authority

Standing status authority is a permission boundary, not a transition directive. It never overrides a command contract that preserves state or forbids issue-state changes. Transition an issue only when the invoked command defines that transition, or the user explicitly requests it.

Within an authorized `dispatch`, implementation-scoped `debug` or explicit status operation, the TPM may apply any justified status other than `Done` after retrieving the current issue and verifying the relevant gate. A worker report alone is insufficient. Read-only commands, requirements/design creation, `create-visuals` and ordinary `sync` do not gain status authority.

- Dispatch sent without an acknowledged plan: leave status unchanged.
- Validated `acknowledged` plan: the issue may enter the team's `In Progress` equivalent.
- `blocked` or `failed`: verify and record the cause; retain the appropriate active/blocked state.
- Validated `completed` handoff: use the team's existing pre-review state when available, then independently verify.
- Independently verified, reviewable work: move to `In Review` and leave final acceptance to the user.
- Unfinished work, unresolved product defects or essential verification gaps: keep active or blocked.

Only the final user decides `Done`.

## Post-write audit

Retrieve every affected record and verify only the fields applicable to the command:

- exact team, project, milestone and canonical identity;
- rendered content and accessible attachments;
- required Category/role labels and verified milestone and mapped source-story tags and exactly one Category child;
- source-story, PRD, dependency and supersession relations;
- preserved lifecycle state and unrelated labels/relations;
- saved View placement, filters and complete expected membership for issue-creation commands;
- no accidental duplicate or unrelated mutation.

Use command-specific references for additional checks. Report exact records changed and anything intentionally left unchanged.
