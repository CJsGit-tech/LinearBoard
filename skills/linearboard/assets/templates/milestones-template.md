# Milestones and grouped stories Project Document template

Create/reuse one native Project Document titled `[Product] 產品里程碑` or its established title. It owns the grouped user stories; link the vision and actual native milestones. This is authoring guidance, not a local project deliverable.

## Overview and ordering

| Milestone | Outcome | Prerequisites |
| --- | --- | --- |
| [Actual native milestone link] | [User/player or learning outcome] | [Known prerequisite or none] |

Explain ordering through value, prerequisites and risk. Separate proposals from commitments; no invented dates, owners or capacity.

## [Milestone name]

- Native milestone: [actual record link and ID].
- Outcome, included scope, observable exit conditions and required evidence.
- Known constraints and material unknowns.

### Grouped user stories

<a id="us-01"></a>

#### US-01 — [User/player outcome]

- **Story:** As [specific user/player], I want [action], so that [value/experience].
- **Core acceptance:** [observable outcome supported by the vision or confirmed decisions].
- **Open boundary:** [only a material unresolved scope question, if any].
- **Legacy source:** [verified existing issue link, only when applicable].

Repeat the milestone/story structure for the actual groups, preserving stable story IDs and anchors. Do not create story issues or Views, require detailed edge cases, or invent unsupported stories.

## Story index

Exactly one fenced `json` block; replace all sample values with actual IDs before saving:

```json
{"schema":"linearboard-story-index-v1","stories":[{"id":"US-01","milestone_id":"native-milestone-id","anchor":"us-01"}]}
```

Use one unique entry per readable story. Optional `legacy_issue_id` identifies an existing verified source issue. Native milestone IDs establish grouping; numeric milestone aliases and M/US labels are not required.

## Dependencies, remaining questions and sources

Record genuine prerequisites and material unknowns. Link existing PRDs and the vision when present; no implementation status or approval is implied by this plan.
