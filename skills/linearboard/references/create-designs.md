# Create design direction and screen specifications

`create-designs <Project> <Milestone>` (including existing `prototype-ui` aliases) creates/revises only two native Project Documents: the design overview and screen/interaction specification. It produces no images, prototype, issues, View, implementation, dispatch or approval. Resolve omitted arguments from explicit context; ask only for a material ambiguity.

## Read and preserve

Resolve team/project/native milestone. Read its vision, grouped story entries, PRDs and confirmed decisions, current design documents, existing product screens and approved references, and available Technical Baseline. Search all pages before creating. Reuse canonical documents and stable SCREEN/flow IDs; preserve unrelated content, source mappings, approved constraints and history. Existing Design issues are historical sources, not new outputs. Do not rewrite source requirements or infer approval from an agent-authored document.

Missing visuals do not block written design drafts. Missing consequential product behavior remains an open item or returns to its owning PRD; do not solve it by inventing a control. References that are unavailable remain unverified.

## Develop one purposeful design direction

Apply [design direction](design-direction.md). Establish the product-specific brief, inspect useful references and derive a visual idea from the product rather than choosing a generic component template. Use real content structure and the intended player experience for games. Save reference observations and the recommendation in the two authorized documents, not a separate local brief.

Recommend one direction with concrete consequences for hierarchy, grouping, typography, imagery and interaction emphasis. Give alternatives only when there is a meaningful unresolved tradeoff or the user requests them. Do not require a textual concept-selection round before the user can see visual studies. Within a clear brief the agent can develop a recommended proposal; it must remain labeled proposed, not user approved. Ask and wait only when missing intent or a change to an approved constraint materially changes the result. Honor explicit delegation without repeated aesthetic permission questions.

A textual direction explains **what the design should communicate and how to judge it**; a visual study tests **how it is composed on the screen**. Do not make an illustrative font, card, poster heading or geometry binding just because it appeared in a concept. Preserve genuinely approved identity/layout at its actual scope. Small revisions reuse the current direction rather than reopening discovery.

## Two canonical documents

Create/reuse and cross-link:

- `<Project> <Milestone>-設計總覽`: user/player outcome, primary task and role, ranked task/risk criteria, recommended visual idea and product-specific reason, inspected references with observed principles and planned transformations, concise visual grammar and its confirmed/proposed status. Link to source PRDs/story entries and detailed specification. Distinguish constraints, preferences and replaceable examples; include only material unknowns.
- `<Project> <Milestone>-畫面與互動規格`: stable SCREEN/flow index with purpose, entry/exit, supported content/actions, transitions, relevant normal/loading/empty/error/permission/cancel/retry/persistence states, source story/PRD links and applicable acceptance. Keep each screen's design intent, binding constraints, creative space and review checks beside it. Shared typography/color/grouping/assets/platform guidance has one owner linked by consumers. Distinguish planned assets from supplied/licensed/generated assets.

The specification also identifies a representative surface that tests the idea under realistic content, required viewports and the requested visual scope. Do not demand one image for every trivial state or silently omit required coverage; propose representative shared-state boards only when they remain independently inspectable. No generation occurs in this command.

## Specify interaction, loading and motion

Read [interaction, loading and motion](interaction-loading-motion.md). In the existing screen specification, define applicable component state transitions, loading/refresh/retry behavior, cancellation and newer-response handling, keyboard/touch paths, focus return, motion tokens/purpose and reduced-motion alternatives. Keep shared contracts once and link consumers. Derive the per-region state inventory before the layout is considered complete, then write the trigger → immediate response → waiting/input availability → success/failure/cancel/timeout contract. Name which controls pause, remain usable or supersede work. A list saying "hover/loading/error" without triggers and observable behavior is insufficient. Unknown behavior remains a proposal or PRD question; do not invent product features. Written motion rules do not claim a working effect.

## Feedback, verification and next action

Reconcile feedback into its owning entry, preserve superseded decisions in native history/comments, and keep only current instructions active. Do not create QA documents or modify issues/states. Preserve source detail when moving content and read back the destination before removing moved text.

Retrieve both documents and verify native project/milestone placement, reciprocal links, stable IDs, story/PRD and acceptance coverage, preserved constraints, inspected-reference provenance and explicit proposal status. Check that the visual idea translates into observable design choices and is not interchangeable mood words or an unexplained UI kit. Written direction is not visual approval or usability evidence.

Recommend the first incomplete applicable deliverable using the root router and live canonical records. Do not always recommend `create-visuals`: an existing valid visual set may only need its written specification reconciled. Never run the next command automatically.
