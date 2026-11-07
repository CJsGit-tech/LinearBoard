# Create milestones and grouped user stories

`create-milestones` combines story generation and milestone planning. Identify what must become possible or what the team needs to learn. Create or revise native milestones and one overview Project Document, adding stories where they explain a milestone outcome. Do not create UserStory issues or a UserStories View.

`create-userstories`, `user-stories` and `stories` are compatibility aliases for this merged command. State the merged output before acting so the expanded artifact scope is visible; no separate story-issue workflow runs.

## Read and resolve

Resolve the team/project and read its vision, supplied planning decisions, native milestones, existing milestone documents, and relevant legacy stories/PRDs. Follow pagination and match by purpose, stable ID and outcome. A supplied vision can serve as an identified source when no native vision exists; do not silently run another creation command.

Reuse the canonical milestone overview, existing native milestones, stable story IDs and established names. Existing UserStory issues are legacy sources: link a verified matching issue when useful, preserving its content, labels, relations and lifecycle. Do not migrate, duplicate, restore, rename or delete legacy issues merely to adopt this document model.

## Define outcomes, then add supporting stories

Use the saved vision as the source of intent. Consult an existing Technical Baseline for constraints that affect milestone scope, order or feasibility. Use chat decisions to clarify the audience, value, experience and constraints. If a later decision conflicts with the saved vision in a way that changes the roadmap, surface the specific difference and resolve it before saving affected milestones. Ask a focused question only when its answer would materially change the checkpoints or their order.

Choose the smallest set of distinct checkpoints that together advance the vision. For each, explain why it matters, what must come first, and what observation would show it was reached. Order by dependencies and by which uncertainty is worth resolving early. Derive names and count from the idea. Use dates, targets, owners and estimates only when supplied.

For a service business, a pilot might demonstrate that customers can receive the service from booking to payment. For an app, a checkpoint might demonstrate a useful task end to end. For a game, it might let a player make a meaningful choice and experience its consequences. Mix these perspectives where the idea calls for it.

For a learning checkpoint, name the question, the evidence to gather and the decision that evidence will inform. A pilot can reach its learning milestone even when the evidence leads to changing or stopping the proposed approach.

Add [story entries](../assets/templates/user-story-template.md) for supported participant actions and benefits, with observable core acceptance. A decision-only milestone can stand on its evidence and decision. Keep detailed edge cases and technical rules for PRDs unless already confirmed and necessary to explain the outcome.

Assign each story to one native milestone. Preserve IDs across wording changes or reassignment; reuse an existing convention such as `PM-US-01`, otherwise use a project-wide `US-01` sequence after checking existing IDs. Require a stable visible M<number> prefix in each native milestone name, such as M1 — First confirmed class booking. For a new plan, assign numbers in the agreed roadmap order. Preserve existing numbers when milestones are reordered; assign new numbers after the highest established number. Never infer a number from the current UI list position. Use the same numbered name in the overview and section heading, group each story under its owning milestone, and verify the section links to that same native milestone ID. This document-only step records M and US identities for subsequent issue tagging.

## Canonical document and story grouping

Use [the milestone template](../assets/templates/milestones-template.md). Each milestone section identifies its native milestone and contains any applicable story entries. Each entry has a stable explicit anchor, stable story ID, outcome/story and core acceptance. Native milestone descriptions retain concise outcome and exit conditions; the document owns grouped story detail and ordering rationale.

Every milestone must show its stable M-number in the native name, overview, milestone heading and story-group heading. Use the milestone template’s native record link and explicit story anchors. Put each anchored story immediately beneath its owning group. Do not generate a Story Index, a JSON mapping, or a Decisions for the PRDs section. Defer PRD decisions to the PRD workflow. Verify fragment navigation in the actual renderer when available; if unsupported, retain the document URL plus readable section ID and report the navigation limitation rather than claiming a fragment works.

Use one **Outcome** and one **Exit check** per milestone. Under each stable story heading, write the participant’s goal as a paragraph, then a bold **Acceptance criteria** label and a Markdown list. Each bullet must describe one independently observable result. Separate distinct actions, access rules, and failure outcomes. Emphasize only decisive phrases and use italics for named screens or actions. On readback, check each story has its own nonempty list inside the correct M-numbered group.

## Save, reconcile and verify

1. Create missing native milestones or update authorized fields on matching ones. Preserve existing IDs, progress, assignments and dates unless explicitly authorized to change them.
2. Create/update the single native milestone-overview Project Document, linked to the vision, with grouped stories, native milestone links using the returned actual IDs.
3. Read back every affected milestone and the complete document. Verify each story appears once, every story anchor belongs to its numbered milestone section, each referenced milestone belongs to the project, links/anchors are usable as supported, and legacy sources remain unchanged. Reconcile partial writes from current state instead of replaying successful creations.
4. When a requested split, merge or reassignment affects existing PRDs/delivery records, identify the old/new mapping and affected records. Do not silently rewrite downstream records, delete milestones, or expand scope; report any unsynchronized consequence.

Return the canonical document URL, native milestones, grouped story coverage and unresolved questions. Distinguish saved plans from delivered milestones. No issue, View, dispatch, status transition or implementation is an output of this command.
