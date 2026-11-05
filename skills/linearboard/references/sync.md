# Synchronize confirmed LinearBoard records

## Invocation and scope

`sync <Project> <Milestone> [scope]` accepts a bounded natural-language scope or explicit record IDs. Preserve existing free-form invocations. Resolve the exact workspace/team/project/native milestone, inventory in-scope records with pagination and state the resolved boundary. An omitted narrower scope covers confirmed consistency repairs among that milestone's existing records, not new product features or a rewrite of every document. Ask only if the destination or material boundary cannot be resolved. A request to explain or preview sync is read-only.

Read [LinearBoard operations](linearboard-operations.md), [issue Views](issue-views.md) and current records before mutation. LinearBoard is canonical; do not create a local product mirror or synchronization ledger. No coding agents, implementation, background watcher, schedule or automatic Git-to-LinearBoard synchronization is started by this command.

## Authority by responsibility

Use the record responsible for the specific fact; a newer timestamp never wins by itself:

- Product behavior and acceptance: owning PRD, linked to source US.
- Screen interaction and visual appearance: screen specification and exact user-approved visual version; substantive disagreement with a PRD is a conflict.
- Technical contract: owning FE/BE engineering ticket and validated research evidence.
- Decision provenance: owning PRD revisions/comments and any historical QA document, preserving actual answers and revision history.
- Milestone-wide scope and constraints: milestone overview and native milestone.

A demonstrably user-approved later revision may require updating its owning current record. Verify the approval and lineage before propagating it. If sources disagree about intended behavior and no confirmed supersession resolves them, report a conflict. Never invent missing answers, options, rationale, research results or historical decisions.

## Difference report and reconciliation

Before writing, use a compact table (in chat or an authorized LinearBoard record):

| Record / field | Current value | Confirmed expected value and source | Classification | Action / result |
| --- | --- | --- | --- | --- |
| Exact record link and field | Observed value | Evidence link or explicit unknown | Consistent / Missing / Stale / Conflict / Unverified | Keep / repair / defer, with readback result |

- **Consistent:** no write.
- **Missing:** add confirmed content or metadata only when evidence establishes the value.
- **Stale:** replace only the superseded current rule; preserve historical answers and revisions in native PRD history/comments or an existing authorized QA record.
- **Conflict:** leave the disputed field unchanged, explain the alternatives and ask only the unresolved consequential question. Continue independent repairs.
- **Unverified:** access or evidence is unavailable; do not claim consistency or fabricate a repair.

Reconcile only applicable items in the authorized scope:

- Current requirements and design/engineering references; link to owners rather than copying long rules everywhere.
- Native project milestone and source document/story IDs, optional legacy M/US labels only when their maintenance is authorized, exactly one Category child, and applicable execution-role labels. Preserve unrelated labels.
- Source Related links and genuine blocking relations. Do not send Related and BlockedBy for the same endpoint pair if the API makes them overwrite one another; retain the blocking relation and a source reference in the body, then read back both endpoints.
- Existing project/category Views: actual team/project/category filters, expected placement and membership. Reuse canonical Views and preserve unrelated user customization. Create a missing required category View only within the authorized reconciliation scope; do not silently delete duplicate Views.

Do not reset issue progress, renumber stable IDs, silently expand scope, reapprove images or infer implementation completion from a requirement/design state. `sync` never moves an issue to Done. Preserve status by default; any explicitly requested non-Done transition still needs the normal evidence and team workflow gates.

Immediately before each write, reread the target and check for concurrent changes. Apply the smallest patch; preserve unrelated fields, relations and history. After partial failure, retain verified successful operations, reread unresolved targets and retry only missing operations. Search before replaying any creation.

## Current UI screenshots

Design or UI changes require screenshot reconciliation as part of an authorized sync; do not stop after updating prose or links to old images. Treat text documents, current design references and implemented UI screenshots as separate synchronization outputs; changes to layout, styling, components or interaction states trigger an image-freshness check even when the written requirements did not change. Audit the in-scope Design and user-visible delivery issues plus their owning screen specifications. Map each affected screen and key changed state to its current reference and implementation evidence.

- Inspect the actual target UI and existing captures. Reuse a screenshot only when its depicted layout, content structure and relevant state still match the current interface; a recent timestamp alone is insufficient. Capture new screenshots when coverage is missing or stale. Cover the changed surface at the relevant desktop/mobile sizes and the changed interaction states (for example, a collapsed card and its open dialog); do not regenerate unrelated screens as a ritual.
- Record the screen/version or owning change, role, route without secret query values, viewport, capture date and scenario. Identify published, private-preview and test-fixture states accurately. Use existing authorized test access; never change credentials or publish company content solely to obtain screenshots. If access or a required state is unavailable, mark that coverage Unverified and report the specific remaining capture.
- Upload actual captures as `evidence` using [application operations](linearboard-operations.md), verify ownership and downloaded bytes, and open the owning record to confirm the image renders. Maintain a clearly identified current screenshot section on each affected issue, with direct images or accessible canonical attachment links. Update the owning screen-specification index and affected Design/delivery references; link a shared capture rather than uploading duplicate bytes to every issue.
- Keep original design references, approvals, before-images and earlier verification evidence as history. Clearly identify which captures are current and which earlier images depict superseded UI; do not silently relabel old screenshots, delete history or change issue status/approval as part of screenshot refresh.
- Keep the current selected design reference linked from the owning specification and Design/delivery issues alongside implementation captures. A superseded reference belongs in clearly labeled history; an adjusted but unapproved design remains a draft. Do not silently regenerate, replace or approve the selected design during sync.
- Use renderable Markdown sections for the current screenshot index. Verify the actual image format/MIME and observed viewport rather than assuming a PNG extension or a requested viewport size proves them.
- A screenshot of the implemented UI is evidence, not a newly approved canonical design. Preserve the exact selected design/version separately. If a confirmed design has not been implemented, say so and retain its design reference; do not manufacture a screenshot or run implementation/image generation merely to fill the gap. New visual exploration still follows `create-visuals` authorization.

The difference report includes screenshot coverage as Missing, Stale, Consistent or Unverified, with the capture/link action. Sync is complete only after available missing/stale captures and their issue/specification references are refreshed and read back; unavailable coverage must remain explicitly reported. Screenshot files used only for upload staging are removed after canonical verification, following the existing visual-review-bundle exception.

## Image cleanup when requested

Cleanup is separate from ordinary sync and runs only when the user requests it. Audit the exact project images against selected designs (including explicit chat selections), canonical attachments and record links, review-gallery assets, runtime source assets and verification history. Check content hashes and provenance as well as filenames: converted or cropped source originals can still be required. A draft flag, old timestamp or absent filename match alone never means unused.

After current images and references have been verified, remove only positively identified unselected/unreferenced exploration images and redundant temporary copies within the requested scope. Prefer recoverable trash; preserve selected originals, approved/history references, Before images and test evidence. Leave uncertain candidates in place and report them. For LinearBoard attachments use the impact-preview and recoverable-trash workflow; for local files report the exact cleanup scope, count and recovery location. Never delete runtime assets or break gallery/record links merely because their design is older.

## Readback and result

Retrieve each changed record and verify rendered content, current screenshot coverage and image rendering, fields, reciprocal relations, accessible references and saved View placement/filters/membership as applicable. A successful write response is not sufficient evidence.

Report actual links in four groups: updated and verified; already consistent; unresolved conflicts; unverified/blocked. State remaining work without claiming all records converged. Dispatch already records its own plans, decisions, reports and evidence; use sync for authorized cross-record reconciliation rather than as a required step after every worker report.
