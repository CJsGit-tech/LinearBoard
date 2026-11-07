# Create PRD issues

Use `create-PRDs <Project> <Milestone>` (aliases `create-prds`, `prd`) to create or revise native ProductRequirement issues and their saved category View. Resolve the exact team/project/native milestone and read the current vision and milestone overview. Consult the existing Technical Baseline when a shared constraint affects product scope or acceptance. This command saves drafts; it does not implement, dispatch or change existing issue states.

## Source and grouping

Apply [shared change review](change-review.md) before drafting, including the learning-only scope check, flagging unverified technical assumptions for FE/BE issue creation and downstream review for revised rules.

The milestone document owns user stories grouped by native milestone, with stable story IDs, explicit anchors and numbered milestone sections defined in [create-milestones](create-milestones.md). Read the complete document and verify the relevant stories under their owning milestone headings. Existing story issues remain usable legacy sources; do not require new UserStory issues or migrate old records automatically.

Group related stories from the SAME native milestone into a coherent user task. A PRD may cover multiple stories; one PRD per story is not required. Split independent capabilities. Shared rules have one owner linked by consumers; do not create cross-milestone PRDs in the new flow. Preserve existing cross-milestone records and report them for an explicitly authorized restructuring rather than choosing a primary milestone arbitrarily.

Search all pages of existing PRDs and legacy documents by stable ID, outcome and story coverage. Preserve IDs, user titles, status, unrelated content and metadata. Never infer a source story number from an application issue key. Missing or conflicting source stories block dependent creation; report the gap without regenerating milestones automatically.

## Content and provenance

Use [the PRD template](../assets/templates/prd-template.md): purpose/scope, flow, product rules, acceptance, dependencies/follow-up. Keep one owner per rule and stable requirement IDs. Distinguish confirmed behavior, hypotheses and consequential open boundary/scope questions. Do not fabricate detailed answers, technical feasibility, research, dates or approval. Drafts may contain unresolved questions; those questions block affected dispatch, not saving the draft.

Begin the purpose section with one visible **Source stories:** line. Link each exact stable story ID to its milestone-document URL and explicit anchor, for example `**Source stories:** [US-01](<document-url>#us-01)`. Put only declared source stories on that line. Keep machine schemas out of issue descriptions. Apply the native milestone, its stable M-number tag and each mapped source-story tag. Reuse active team labels (for example, M1 and US1 for US-01); resolve ambiguous mappings before writing. Preserve unrelated labels. Verify every source belongs to this project and native milestone. Use native Related for verified legacy story issues. Record explicit issue dependencies as native blocks relations from prerequisite to dependent and verify direction after saving. Document sections use links.

## Save and verify

Create new issues in Backlog with the exact project/team, native milestone and ProductRequirement category. Update existing issues with optimistic version checks, preserving lifecycle, labels and unrelated relations. Retrieve every changed record and source; verify full content, source anchors, native milestone, category, status, absence of duplicates and accessible links. Verify legacy relations only when actual legacy issues are sources.

Use [the traceability operation](traceability.md) to audit explicit PRD IDs after saving. Its read-only default detects source/milestone errors. Metadata repair requires the command's authorized scope and explicit `--apply`, project and issue IDs; it never decides product behavior or changes story grouping. Report successful writes separately from unresolved/failed operations and retry only missing work.

Create/reuse the ProductRequirement View using [issue Views](issue-views.md), and verify intended issue membership independently of the category filter. Include PRD and View links, covered story IDs and any deferred scope questions in the final report. PRD creation does not authorize source-story edits, restoration, design, implementation or dispatch.

## Automatic PRD demystification

Creating and verifying the PRD issues and saved View is the first stage of this command. Immediately read back the created or revised items and begin PRD demystification in the same conversation. Do not finish with an offer or recommendation to run a separate clarification command when a consequential decision remains. The first clarification question is part of the create-PRDs response after the saved-item summary. If the response ends while waiting for an answer, identify the reply as a continuation of `create-PRDs`.

Derive questions from the actual saved PRDs, their source stories, existing decisions and Technical Baseline. For each included user journey, examine first-use prerequisites, actor identity and overlapping roles, permitted actions, entry and return destinations, state changes, failure/retry outcomes and observable acceptance. Identify decisions that the PRD leaves implicit even if its open-question section is empty. Ask only about consequential product ambiguity; routine wording and visual treatment belong to design.

Name the owning PRD issue and concrete scenario with each question. Ask one focused question, wait for the user's answer, save and verify the resulting rule and acceptance changes plus its answer comment, then ask the next unresolved question. The sections below define that loop. Reuse confirmed answers and stop when the scoped consequential decisions are resolved. If none remain, report that result. If the user requests drafts only or defers clarification, leave the unanswered decisions visible in their owning PRDs and report them.

After a new/revised PRD or a changed answer, return the applicable [linked-record impact result](change-review.md#return-an-actionable-impact-result). Update and verify the owning PRD within this command’s authority; identify actual upstream/downstream mismatches and suggest bounded sync proposals for edits outside it. Do not silently propagate a confirmed answer into every linked document or invent a standalone clarification command.

## Find questions that need a decision

Consolidate unresolved choices affecting included/excluded scope, expected behavior or acceptance boundaries. Reuse answered questions; do not repeat them to complete a questionnaire. Technical research and routine design/engineering choices are follow-up work, not product questions. Preserve uncertainties rather than inventing feasible promises.

Before asking, name two plausible answers and the meaningful difference a user or the business would experience. Ask only if existing decisions leave that trade-off open and it needs the user's judgment. Follow established conventions for minor details, or leave them to design or engineering. Never turn an inferred default into an approved requirement. For example, ordinary button wording can wait; whether confirming the action charges a cancellation fee merits a question. If only minor choices remain, finish without asking another question.

Resolve prerequisites first, then prioritize the answer that unblocks the most in-scope work.

### Format each live QA question

Present one consequential product question at a time in the user's preferred response language, including on retries. Prefer the native selectable question card when available.

- Put the owning PRD ID and direct question in the prompt. Add a short concrete example when it helps distinguish the choices.
- Give two or three concise, action-oriented options. If there is a clear recommendation, put it first and label it `(Recommended)`.
- When the card supports option descriptions, use one or two sentences under each option to explain what happens and the main benefit and drawback. When it only supports option text, include the key trade-off in the option text. Use the card's built-in free-text choice for a different rule.
- If no question card is available, use this Markdown layout.

**Question:**

<question>

**Example:**

<concrete example>

**Options**

- **A:** <statement describing what happens>
  - **Advantages:** <statement>
  - **Disadvantages:** <statement>
- **B:** <statement describing what happens>
  - **Advantages:** <statement>
  - **Disadvantages:** <statement>

For the Markdown fallback, link the owning PRD in the preceding status line. Use the question or rule ID in the decision record. Add **C:** in the same format only for a distinct, meaningful alternative. Put the behavior in the option statement and keep the advantages and disadvantages specific to the example. If an answer needs a simple clarification, ask briefly without repeating the full option list.

Wait for the answer before asking the next product question. Accept a free-form rule or several volunteered decisions in one answer. A recommendation, silence, or elapsed time does not count as agreement. A request to pause leaves unanswered questions open.

## Update the owning PRDs directly

Apply [shared change review](change-review.md) when preparing choices and propagating confirmed answers. Keep cross-record follow-up within the authorized scope.

Translate each confirmed answer into the smallest precise change to scope, flow, rules and observable acceptance. Keep the five-section PRD structure, stable IDs and one owner per shared rule; consumers link the owner. Remove resolved open-question wording, preserve unaffected content, source provenance, labels, relations and status. Do not add unapproved behavior.

Read each target immediately before updating with expected_version; retrieve and verify the saved behavior before asking a dependent next question. After processing each answer, give a one-line update naming the verified PRD changes and any pending edits or sync work before moving on. Record each confirmed answer as a native comment on its owning PRD issue. Include the question or rule ID and the user's answer, preserving exact wording when it matters. Retrieve the comment from that issue and verify its parent and content. Keep the current rule and acceptance criteria in the issue body. When retrying, read existing comments first and reuse a matching answer. Report any missing comment or body update separately and retry only the missing write.

For a decision affecting several PRDs, report exactly which updates were verified and which remain pending after a partial failure. Recover the answer from conversation, saved PRD revisions/comments or existing evidence; never infer an answer from a failed write or ask it again merely because propagation failed. Re-read unresolved targets and apply only missing updates. Do not advance a dependent decision while its prerequisite answer or write outcome is ambiguous.

If an answer conflicts with a source story or broader milestone commitment, report that conflict and ask only for the missing scope authorization; do not silently rewrite those sources. Independent PRD updates can continue.

## Finish

Return affected PRD links and remaining boundary/scope questions or unsynced updates. If none exist, say so without creating a QA artifact or dialogue. Decisions are complete only when the answer comments and corresponding body updates are read back; deferred questions remain unresolved. Technical validation remains separate from product decisions. Recommend the first incomplete applicable deliverable using the skill router; this command never establishes design approval, passing tests or implementation completion.

## Legacy representations

An explicit edit of a legacy PRD Project Document preserves that representation and does not create issues or a View. Verify its project, content and links. Legacy issue-based story provenance remains readable without mandatory migration; the traceability script reports unsupported/unindexed provenance for manual review rather than rewriting it. Restoring deleted records or restructuring existing PRDs requires its own authorized scope; read [restructure PRDs](restructure-prds.md) only then.
