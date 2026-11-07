# Requirements chain

The canonical building flow is Planning discussion → 4W1H vision Project Document → native milestones and one milestone document containing grouped user stories → milestone-scoped PRD issues → decisions updated directly in PRDs. Reuse existing work instead of rerunning stages. All saved product records remain in LinearBoard.

## Ownership and identity

- Vision: What, Why, Who, Where, How based on Planning. Business products express pain and intended solution; games express intended player experience.
- Milestones: native records with outcomes; the milestone overview Project Document owns grouped story entries, stable story IDs, explicit anchors and core observable acceptance under numbered milestone headings.
- PRDs: native ProductRequirement issues with source document/story IDs and one matching native milestone. Related story issues are only required when those sources actually exist as legacy issues. Apply the native milestone, its stable M-number tag and each mapped source-story tag. Reuse active team labels (for example, M1 and US1 for US-01); resolve ambiguous mappings before writing. Preserve unrelated labels.
- Decisions: current scope/rules/acceptance in owning PRDs; each confirmed answer is recorded and verified as a native comment on its owning PRD issue. Existing QA documents are historical sources, not a new mandatory artifact.
- Design and delivery: link to the actual story document entry (or existing legacy issue), owning PRD and applicable acceptance; never create story issues merely to satisfy downstream relations.

A task-specific rule has one PRD owner. The milestone document owns milestone-wide scope, outcomes and story grouping. Consumers link shared owners instead of copying rules. Preserve stable requirement/story IDs and history; restructuring or moving sources needs authorized scope.

## Traceability

Read [traceability](traceability.md) when auditing or repairing PRD source/milestone consistency. Its default is read-only; explicit project and issue selection plus --apply are required for bounded metadata repair. New PRDs must not span multiple source milestones; split coherent tasks or report the unresolved boundary. Preserve legacy cross-milestone records without silently migrating them.

## Drafts and readiness

Draft PRDs may preserve open boundary/scope questions. `create-PRDs` asks about consequential open decisions in the same conversation and updates PRDs directly; it creates no QA document or delivery tickets. Unresolved material behavior blocks affected dispatch, not draft creation. Record creation and decision completion prove neither implementation nor acceptance.

## Technical decisions in delivery tickets

Select technologies during frontend and backend issue creation. Record verified choices and shared interface ownership in the responsible delivery tickets, with evidence from actual configuration or official sources. Link dependent tickets to the decision.
