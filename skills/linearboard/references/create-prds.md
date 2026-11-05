# Create PRD issues

Use `create-PRDs <Project> <Milestone>` (aliases `create-prds`, `prd`) to create or revise native ProductRequirement issues and their saved category View. Resolve the exact team/project/native milestone and read the current vision and milestone overview. This command saves drafts; it does not implement, dispatch or change existing issue states.

## Source and grouping

The milestone document owns user stories grouped by native milestone, with stable story IDs, explicit anchors and the `linearboard-story-index-v1` index defined in [create-milestones](create-milestones.md). Read the complete document and relevant story entries, not just the index. Existing story issues remain usable legacy sources; do not require new UserStory issues or migrate old records automatically.

Group related stories from the SAME native milestone into a coherent user task. A PRD may cover multiple stories; one PRD per story is not required. Split independent capabilities. Shared rules have one owner linked by consumers; do not create cross-milestone PRDs in the new flow. Preserve existing cross-milestone records and report them for an explicitly authorized restructuring rather than choosing a primary milestone arbitrarily.

Search all pages of existing PRDs and legacy documents by stable ID, outcome and story coverage. Preserve IDs, user titles, status, unrelated content and metadata. Never infer a source story number from an application issue key. Missing or conflicting source stories block dependent creation; report the gap without regenerating milestones automatically.

## Content and provenance

Use [the PRD template](../assets/templates/prd-template.md): purpose/scope, flow, product rules, acceptance, dependencies/follow-up. Keep one owner per rule and stable requirement IDs. Distinguish confirmed behavior, hypotheses and consequential open boundary/scope questions. Do not fabricate detailed answers, technical feasibility, research, dates or approval. Drafts may contain unresolved questions; those questions block affected dispatch, not saving the draft.

Link every source story using the actual milestone document URL plus its explicit anchor and readable story ID. Include one machine-readable provenance block in the PRD body, without duplicating story prose:

```json
{"schema":"linearboard-prd-sources-v1","document_id":"<actual milestone document ID>","story_ids":["US-01","US-02"]}
```

The source document/story identities determine provenance; the PRD's native `milestone_id` must match every selected source story's native milestone. The native project is the scope boundary. M/US labels are optional query aids in the new flow, not identity or readiness gates. Preserve existing labels; do not invent labels or remove legacy labels to enforce this format. If indexed sources have actual legacy issue IDs, retain/add native Related relations to those issues; document sections cannot be issue relations. Never create fake story issues to obtain relations.

## Save and verify

Create new issues in Backlog with the exact project/team, native milestone and ProductRequirement category. Update existing issues with optimistic version checks, preserving lifecycle, labels and unrelated relations. Retrieve every changed record and source; verify full content, source anchors, native milestone, category, status, absence of duplicates and accessible links. Verify legacy relations only when actual legacy issues are sources.

Use [the traceability operation](traceability.md) to audit explicit PRD IDs after saving. Its read-only default detects source/milestone errors. Metadata repair requires the command's authorized scope and explicit `--apply`, project and issue IDs; it never decides product behavior or changes story grouping. Report successful writes separately from unresolved/failed operations and retry only missing work.

Create/reuse the ProductRequirement View using [issue Views](issue-views.md), and verify intended issue membership independently of the category filter. Return PRD and View links, covered story IDs and unresolved scope questions. PRD creation does not authorize source-story edits, restoration, design, implementation or dispatch.

If consequential open questions remain, offer `prd-demystify` once, unless the user already asked to clarify now. Do not force an interview or create a QA document. If the user defers, leave the questions visible in their owning PRDs.

## Legacy representations

An explicit edit of a legacy PRD Project Document preserves that representation and does not create issues or a View. Verify its project, content and links. Legacy issue-based story provenance remains readable without mandatory migration; the traceability script reports unsupported/unindexed provenance for manual review rather than rewriting it. Restoring deleted records or restructuring existing PRDs requires its own authorized scope; read [restructure PRDs](restructure-prds.md) only then.
