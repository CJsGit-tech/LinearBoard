# Synchronize confirmed LinearBoard records

## Invocation and scope

`sync <Project> <Milestone> [scope or new request]` accepts a proposed product change, bounded topic or explicit record IDs. Resolve the destination and inventory the scoped records with pagination. Without narrower scope, review the named milestone. Every invocation starts read-only. This also applies when another command routes work here. Show the proposal in chat and stop until the user explicitly approves the presented blocks. This gate covers every mutation, including comments, links, labels, Views, uploads and cleanup. A command invocation, earlier product decision or silence cannot approve a proposal.

Read [LinearBoard operations](linearboard-operations.md), [issue Views](issue-views.md) and current records before mutation. LinearBoard is canonical; do not create a local product mirror or synchronization ledger. No coding agents, implementation, background watcher, schedule or automatic Git-to-LinearBoard synchronization is started by this command.

## Authority by responsibility

Use the record responsible for the specific fact; a newer timestamp never wins by itself:

- Product behavior and acceptance: owning PRD, linked to source US.
- Screen interaction and visual appearance: screen specification and exact user-approved visual version; substantive disagreement with a PRD is a conflict.
- Shared technical requirements: the project Technical Baseline, when present. Include proposed baseline changes in the approval review.
- Feature-specific technical contract: owning FE/BE engineering ticket and validated research evidence.
- Decision provenance: owning PRD revisions/comments and any historical QA document, preserving actual answers and revision history.
- Milestone-wide scope and constraints: milestone overview and native milestone.

A demonstrably user-approved later revision may require updating its owning current record. Verify the approval and lineage before propagating it. If sources disagree about intended behavior and no confirmed supersession resolves them, report a conflict. Never invent missing answers, options, rationale, research results or historical decisions.

## Difference report and reconciliation

For a changed decision, apply [shared change review](change-review.md) to identify affected records and verify the authorized updates.

1. Review the request against the milestone goal, documents, story and PRD acceptance criteria, affected Design and FE/BE issues, and their source links and dependencies. Trace the effect of the new behavior through these records. Identify conflicts, missing evidence and any affected UI captures.
2. First respond in chat using the [file-change-summary format](../../file-change-summary/SKILL.md), adapted to board records. Give one proposed block per affected record, identified by title/ID and link. Combine edits to the same record. Include precise changes to acceptance criteria, relationships and evidence where applicable.

```text
<record title or ID> — <section or field>

- from: <observed current value or missing item>
- to: <specific proposed change and observable result>
```

3. List unresolved questions separately. If nothing needs changing, report that finding. Wait for explicit user approval of the presented blocks before any board write, upload or status change. A new request or previously confirmed product rule is input to the proposal. A preview-only request ends with the proposal. While approval is pending, the next step is to approve the specific blocks to continue this run. After the approved edits are verified, check the next applicable deliverable within the requested scope.
4. Apply only approved blocks, including a subset if specified. Reread each target first. If changed content materially alters the proposed edit, present a revised block for approval. Verify each approved update and report deferred, conflicted and unverified items. Product implementation belongs to a separate command.

Classify differences during review:

- **Consistent:** no write.
- **Missing:** add confirmed content or metadata only when evidence establishes the value.
- **Stale:** replace only the superseded current rule; preserve historical answers and revisions in native PRD history/comments or an existing authorized QA record.
- **Conflict:** leave the disputed field unchanged, explain the alternatives and ask only the unresolved consequential question. Continue reviewing independent items and apply only blocks the user has approved.
- **Unverified:** access or evidence is unavailable; do not claim consistency or fabricate a repair.

Reconcile only applicable items in the authorized scope:

- Current requirements and design/engineering references; link to owners rather than copying long rules everywhere.
- Native project milestone and source document/story IDs, required milestone and mapped source-story tags (report drift in read-only scope), exactly one Category child, and applicable execution-role labels. Preserve unrelated labels.
- Source Related links and genuine blocking relations. Do not send Related and BlockedBy for the same endpoint pair if the API makes them overwrite one another; retain the blocking relation and a source reference in the body, then read back both endpoints.
- Existing project/category Views: actual team/project/category filters, expected placement and membership. Reuse canonical Views and preserve unrelated user customization. Create a missing required category View only within the authorized reconciliation scope; do not silently delete duplicate Views.

Do not reset issue progress, renumber stable IDs, silently expand scope, reapprove images or infer implementation completion from a requirement/design state. `sync` never moves an issue to Done. Preserve status by default; any explicitly requested non-Done transition still needs the normal evidence and team workflow gates.

Immediately before each write, reread the target and check for concurrent changes. Apply the smallest patch; preserve unrelated fields, relations and history. After partial failure, retain verified successful operations, reread unresolved targets and retry only missing operations. Search before replaying any creation.

## Current UI screenshots

A reference-only cleanup removes local paths and prototype addresses from current record bodies and retains native Approved JPGs and LinearBoard links. Verify that the retained screenshots still render. Preserve historical approval comments and revision history. Refresh captures only when the visual content or required coverage changes.

Design or UI changes require screenshot reconciliation as part of an authorized sync; do not stop after updating prose or links to old images. Treat text documents, current design references and implemented UI screenshots as separate synchronization outputs; changes to layout, styling, components or interaction states trigger an image-freshness check even when the written requirements did not change. Audit the in-scope Design and user-visible delivery issues plus their owning screen specifications. Map each affected screen and key changed state to its current reference and implementation evidence.

- Inspect the scoped target application's actual UI and existing captures. Reuse only captures whose layout/content/state still match; timestamps alone are insufficient. Refresh missing/stale affected states at that platform's declared view sizes. Do not add a counterpart Web/Mobile application or paired-size checks during sync.
- Record the screen/version or owning change, role, route without secret query values, viewport, capture date and scenario. Identify published, private-preview and test-fixture states accurately. Use existing authorized test access; never change credentials or publish company content solely to obtain screenshots. If access or a required state is unavailable, mark that coverage Unverified and report the specific remaining capture.
- Upload actual captures as `evidence` using [application operations](linearboard-operations.md), verify ownership and downloaded bytes, and open the owning record to confirm the image renders. Maintain a clearly identified current screenshot section on each affected issue, with direct images or accessible canonical attachment links. Update the owning screen-specification index and affected Design/delivery references; link a shared capture rather than uploading duplicate bytes to every issue.
- Keep original design references, approvals, before-images and earlier verification evidence as history. Clearly identify which captures are current and which earlier images depict superseded UI; do not silently relabel old screenshots, delete history or change issue status/approval as part of screenshot refresh.
- Keep the current selected design reference linked from the owning specification and Design/delivery issues alongside implementation captures. A superseded reference belongs in clearly labeled history; an adjusted but unapproved design remains a draft. Do not silently regenerate, replace or approve the selected design during sync.
- Use renderable Markdown sections for the current screenshot index. Verify the actual image format/MIME and observed viewport rather than assuming a PNG extension or a requested viewport size proves them.
- A screenshot of the implemented UI is evidence, not a newly approved canonical design. Preserve the exact selected design/version separately. If a confirmed design is unimplemented, say so and retain its design reference; do not manufacture evidence by building a mockup or changing production merely to fill the gap. A browser mockup capture remains a design reference. New visual exploration follows `create-visuals` authorization.

The difference report includes screenshot coverage as Missing, Stale, Consistent or Unverified, with the capture/link action. For approved screenshot updates, the write phase is complete only after available missing/stale captures and their issue/specification references are refreshed and read back; unavailable coverage must remain explicitly reported. Screenshot files used only for upload staging are removed after canonical verification, following the existing visual-review-bundle exception.

## Image cleanup when requested

Cleanup is separate from ordinary sync and runs only when the user requests it. Audit the exact project images against selected designs (including explicit chat selections), canonical attachments and record links, review-gallery assets, runtime source assets and verification history. Check content hashes and provenance as well as filenames: converted or cropped source originals can still be required. A draft flag, old timestamp or absent filename match alone never means unused.

After current images and references have been verified, remove only positively identified unselected/unreferenced exploration images and redundant temporary copies within the requested scope. Prefer recoverable trash; preserve selected originals, approved/history references, Before images and test evidence. Leave uncertain candidates in place and report them. For LinearBoard attachments use the impact-preview and recoverable-trash workflow; for local files report the exact cleanup scope, count and recovery location. Never delete runtime assets or break gallery/record links merely because their design is older.

## Readback and result

Retrieve each changed record and verify rendered content, current screenshot coverage and image rendering, fields, reciprocal relations, accessible references and saved View placement/filters/membership as applicable. A successful write response is not sufficient evidence.

Report actual links in four groups: updated and verified; already consistent; unresolved conflicts; unverified/blocked. State remaining work without claiming all records converged. Dispatch already records its own plans, decisions, reports and evidence; use sync for authorized cross-record reconciliation rather than as a required step after every worker report.
