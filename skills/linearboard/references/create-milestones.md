# Create milestones and grouped user stories

`create-milestones` combines story generation and milestone planning. Derive user stories from the product vision, group them into coherent outcomes, then create/revise native milestones and **one milestone-overview Project Document containing the stories grouped by milestone**. Do not create UserStory issues or a UserStories View.

`create-userstories`, `user-stories` and `stories` are compatibility aliases for this merged command. State the merged output before acting so the expanded artifact scope is visible; no separate story-issue workflow runs.

## Read and resolve

Resolve the team/project and read its vision, supplied planning decisions, native milestones, existing milestone documents, and relevant legacy stories/PRDs. Follow pagination and match by purpose, stable ID and outcome. A supplied vision can serve as an identified source when no native vision exists; do not silently run another creation command.

Reuse the canonical milestone overview, existing native milestones, stable story IDs and established names. Existing UserStory issues are legacy sources: link a verified matching issue when useful, preserving its content, labels, relations and lifecycle. Do not migrate, duplicate, restore, rename or delete legacy issues merely to adopt this document model.

## Generate stories, then group milestones

First identify the independently understandable user/player outcomes supported by the vision. Use [the story-entry guidance](../assets/templates/user-story-template.md): a specific role, intended action and benefit, with core observable acceptance. For games, describe player actions and resulting experience rather than inventing business roles. Do not turn PM approval or engineering tasks into artificial user stories.

Keep detailed edge cases, thresholds, permissions and technical rules for PRDs unless already confirmed and needed to explain the outcome. Preserve supplied rules; mark material unknowns explicitly instead of inventing them or conducting a second detailed interview.

Group stories by a coherent user/player outcome or useful learning/delivery checkpoint. Derive the number, names and order of milestones from those groups; do not impose a fixed roadmap count. Explain prerequisites, value and risk without fabricated dates, estimates, capacity, owners or scores. Research/validation milestones may have decision outcomes without fake feature stories.

Assign each story to one native milestone. Preserve IDs across wording changes or reassignment; reuse an existing convention such as `PM-US-01`, otherwise use a project-wide `US-01` sequence after checking existing IDs. Never derive IDs or milestone numbers from current list position. Use native milestone IDs for identity; numeric `M1` aliases may be reused only when an established mapping exists. No new M/US labels are required by this command.

## Canonical document and traceability index

Use [the milestone template](../assets/templates/milestones-template.md). Each milestone section identifies its native milestone and contains its grouped story entries. Each entry has a stable explicit anchor, stable story ID, outcome/story and core acceptance. Native milestone descriptions retain concise outcome and exit conditions; the document owns grouped story detail and ordering rationale.

Include exactly one fenced `json` block with this structural index in the canonical document:

```json
{"schema":"linearboard-story-index-v1","stories":[{"id":"US-01","milestone_id":"native-milestone-id","anchor":"us-01"}]}
```

Use actual native IDs, not placeholders, when saving. Add `legacy_issue_id` only for a verified existing source issue; omit it otherwise. Each story ID and anchor must be unique in the document. Put an explicit `<a id="us-01"></a>` immediately before the corresponding readable story heading. The index contains identities and grouping only; it does not duplicate story prose, approval or issue status. Downstream PRDs reference this native document ID and exact story IDs, not invented source issues. Verify fragment navigation in the actual renderer when available; if unsupported, retain the document URL plus readable section ID and report the navigation limitation rather than claiming a fragment works.

## Save, reconcile and verify

1. Create missing native milestones or update authorized fields on matching ones. Preserve existing IDs, progress, assignments and dates unless explicitly authorized to change them.
2. Create/update the single native milestone-overview Project Document, linked to the vision, with grouped stories, native milestone links and the structural index using the returned actual IDs.
3. Read back every affected milestone and the complete document. Verify each story appears once, every index entry matches its readable section and grouping, each referenced milestone belongs to the project, links/anchors are usable as supported, and legacy sources remain unchanged. Reconcile partial writes from current state instead of replaying successful creations.
4. When a requested split, merge or reassignment affects existing PRDs/delivery records, identify the old/new mapping and affected records. Do not silently rewrite downstream records, delete milestones, or expand scope; report any unsynchronized consequence.

Return the canonical document URL, native milestones, grouped story coverage and unresolved questions. Distinguish saved plans from delivered milestones. No issue, View, dispatch, status transition or implementation is an output of this command.
