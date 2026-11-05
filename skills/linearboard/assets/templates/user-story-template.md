# Grouped user-story entry guidance

Write each story inside its owning milestone section in the single native milestone-overview Project Document. This is part of `create-milestones`; do not create a native story issue, per-story document or UserStories View.

Preserve a stable story ID such as `US-01` or an existing project convention. Give it a unique explicit anchor and match that anchor/ID/native milestone in the document's `linearboard-story-index-v1` JSON block.

```md
<a id="us-01"></a>

#### US-01 — [Readable user/player outcome]

- **Story:** As [specific user/player in a situation], I want [action], so that [benefit or intended play experience].
- **Core acceptance:** [Observable successful outcome].
- **Open boundary:** [Material undecided scope only, when present].
- **Legacy source:** [Verified existing source issue, when present].
```

Use the user's language. Keep acceptance at the outcome level; detailed failure/recovery, permission, persistence, thresholds and implementation rules belong in PRDs unless supplied and necessary to explain the outcome. Do not invent them to fill a checklist.

On reruns, match IDs and outcomes, preserve IDs across regrouping, and do not reset legacy issue lifecycle or metadata. Link an existing legacy issue where useful and include its verified ID as optional `legacy_issue_id` in the structural index; no issue is created merely to support a PRD relation.
