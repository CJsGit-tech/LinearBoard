# Clarify open PRD scope decisions

Use `prd-demystify <Milestone>` or `prd-demystify <Project> <Milestone>`. Resolve the exact project and native milestone from current records. Read in-scope PRDs, their source story entries in the milestone document and existing confirmed decisions. This command updates PRDs where open-ended boundary or scope questions require a user decision. It does not create or maintain a separate QA report, delivery issues, implementation or status transitions.

## Find questions that need a decision

Consolidate unresolved choices affecting included/excluded scope, expected behavior or acceptance boundaries. Reuse answered questions; do not repeat them to complete a questionnaire. Technical research and routine design/engineering choices are follow-up work, not product questions. Preserve uncertainties rather than inventing feasible promises.

Ask one consequential question at a time in the user's language. Explain a concrete scenario and meaningful alternatives only when they help; do not require a fixed option/pros/cons format. Accept a free-form rule or several volunteered decisions in one answer. Silence or elapsed time is not agreement. A request to pause leaves unanswered questions open.

## Update the owning PRDs directly

Translate each confirmed answer into the smallest precise change to scope, flow, rules and observable acceptance. Keep the five-section PRD structure, stable IDs and one owner per shared rule; consumers link the owner. Remove resolved open-question wording, preserve unaffected content, source provenance, labels, relations and status. Do not add unapproved behavior.

Read each target immediately before updating with expected_version; retrieve and verify the saved behavior before asking a dependent next question. A concise native comment on the owning PRD can preserve the actual answer and superseded decision when useful; do not build a duplicate interview log or invent historical wording. Existing QA documents remain historical sources and are not rewritten by this command.

For a decision affecting several PRDs, report exactly which updates were verified and which remain pending after a partial failure. Recover the answer from conversation, saved PRD revisions/comments or existing evidence; never infer an answer from a failed write or ask it again merely because propagation failed. Re-read unresolved targets and apply only missing updates. Do not advance a dependent decision while its prerequisite answer or write outcome is ambiguous.

If an answer conflicts with a source story or broader milestone commitment, report that conflict and ask only for the missing scope authorization; do not silently rewrite those sources. Independent PRD updates can continue.

## Finish

Return affected PRD links and remaining boundary/scope questions or unsynced updates. If none exist, say so without creating a QA artifact or dialogue. Decisions are complete only when confirmed updates are read back; deferred questions remain unresolved. Technical validation remains separate from product decisions. Recommend the first incomplete applicable deliverable using the skill router; this command never establishes design approval, passing tests or implementation completion.
