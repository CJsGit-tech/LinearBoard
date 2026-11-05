# Create and refine visual references

`create-visuals <Project> <Milestone>` uses [$imagegen](../../.system/imagegen/SKILL.md) to turn canonical design direction/specifications into inspectable visual references and a local read-only HTML gallery. It does not implement UI or prove interaction. Read [design direction](design-direction.md) and apply it to prompts AND rendered critique. Another design skill is not required.

## Resolve the brief and choose the smallest useful study

Resolve exact workspace/team/project/native milestone and authorized screen/state scope. Read the vision, grouped story entries/legacy sources, PRDs, design overview/specification, confirmed feedback and exact approved references. Reuse existing originals, scope selections and gallery. Preserve product-wide styling unless a change is authorized; another milestone's palette does not select the composition of a new surface.

Use the recommended idea and reference analysis from `create-designs` as a working proposal without demanding another textual style approval. If those inputs are thin, inspect suitable references and form a bounded recommendation using the shared method; do not rewrite product rules or silently replace an approved direction. Missing specification entries or material behavior block the affected generation, not independent ready scope.

Before generating, state the mode, specific representative screen/data/viewport, planned image count for this batch, total requested screen/state coverage and reusable assets. Mark generation time/cost unknown unless the tool supplies it. This is a scope statement, not a repeated permission request. Do not treat the generation plan as approval of missing product decisions.

- **New surface or substantial uncertain composition:** normally compare two or three genuinely different compositions of ONE representative screen under the same supported content, actions, state and viewport. Choose the number for actual uncertainty; if the user specifies three, deliver three. New alternatives may differ in visual grammar when it is unapproved; preserve any approved palette/type/components. Do not generate a whole milestone before its composition direction is selected.
- **Bounded correction to an existing selected layout:** edit that layout directly, retaining its identity and source version. Do not force three new concepts for a spacing, grouping, density, typography or single-state correction. A change to binding identity or product behavior still requires the relevant decision.
- **Exact layout reuse already directed:** proceed to detail within that scope. Inherited colors or 'keep the style' alone do not establish exact layout reuse for a new surface.

Use imagegen for all UI design boards; HTML/CSS may implement the gallery, never substitute code-rendered UI for the requested images. Follow reference-image inspection and save-path rules. Do not generate images simply to satisfy a count when valid outputs already exist.

## Interaction and motion coverage

Read [interaction, loading and motion](interaction-loading-motion.md). Use the owning specification's applicable selected/hover/focus/pressed/busy/error/recovery cues in the scoped boards, and preserve its loading, timing, cancellation and reduced-motion contract in the canonical handoff. Static images cannot prove that those effects work. When the user separately authorizes code-based interactive mockups, operate the actual controls and report runtime checks separately from visual inspection and simulated request behavior. This does not authorize production implementation or a global change of generation tools.

## Compose, inspect, revise

For each prompt carry the product idea, focal point, attention path, content relationships/density, type/image balance and purposeful use of color/space, alongside exact supported labels/actions/state/viewport. Inspect relevant image references before editing and provide them to generation where supported. Keep the same data scenario across comparisons. Use source-backed or clearly labeled illustrative data with the correct content shape; it is not product evidence and must not add fields, claims or features.

Compare actual compositions, not their captions. A sidebar/card grid with new colors or adjectives is one repeated solution. When alternatives are too similar, change the information hierarchy, grouping, imagery role or reading path, then inspect again. No universal demand for asymmetry, decorative imagery, tiny type or oversized headings; the brief governs the choice.

Use the shared critique on every delivered board: task/experience fit, product-specific expression, full-composition hierarchy, realistic content, cross-screen grammar, platform fit, readable labels and relevant accessibility cues. Correct visible unsupported controls, missing essential information, malformed text and repeated framing that weakens the idea. State what changed after inspection. A prompt that asks for beautiful design is not evidence of quality. Retain failed attempts as useful history without presenting them as valid options. Follow the shared bounded revision rule; report unresolved limits instead of endless regeneration or false success.

Build and verify the gallery before presenting studies. Lead with the recommended image and concise task-grounded rationale/tradeoff; do not transfer all design judgment to the user. For new composition exploration, wait for an explicit visual selection, unless the user explicitly delegated composition selection. Delegation permits the agent to choose and continue, not to approve the complete design or upload. A rejected set returns to the specific visible weakness rather than an automatic new style questionnaire.

## Selection, progress and recovery

A concrete selection (including an unambiguous option letter for the active studies) continues the ORIGINAL requested detail scope. Do not stop after acknowledging it or demand another invocation. Theme approval, viewing a gallery, silence and elapsed time are not selection. Record source/version/scope and distinguish user selection from an agent choice under delegation.

As part of this command, maintain a concise native comment on the owning screen specification with current stage, direction/layout selection and its source, exact screen/version inventory, covered/pending screens/states, current gallery/original locations, and separate upload/design-approval/native-attachment states. Create/update it at review checkpoints; no extra permission to record the active workflow is needed. Use expected-version checks, preserve history and read it back. A local path identifies recovery material, not a web-accessible canonical attachment. On resume verify both canonical checkpoint and local originals. Recover missing originals first from the byte-identical gallery assets or verified canonical attachments, checking identity/version and bytes where available. If exact originals cannot be recovered, regeneration creates new draft artifact versions linked to the prior intent; it must not inherit the missing image's exact-image selection, upload permission or design approval. Retain the selected design intent only as guidance, present changed replacement images for review and obtain only the applicable missing selection/approval before those gates. Regenerate only missing/invalid material; do not relabel it as the recovered original. If LinearBoard cannot save the checkpoint, stop dependent work and report the blocker rather than claiming durable progress or keeping a local PM ledger.

After selection, generate every screen/component and relevant key state in the authorized scope using the selected visual grammar and originals as references where useful. For a large set, deliver reviewable batches covering a coherent flow, with covered/pending inventory; an intermediate batch is not full completion. Continue within the active scope unless waiting for material feedback, a changed brief, a tool/budget/access limit or the user asks to pause. Do not stop merely after the first batch. Describe motion/behavior in the canonical handoff; a still does not verify it. Rebuild and inspect the gallery with the complete requested set before calling detailed delivery complete.

## Gates and valid stopping points

| Stage | Action / stopping condition |
| --- | --- |
| New composition studies ready | Verified gallery delivered; wait for visual selection unless delegated. |
| Selected layout, bounded edit or directed exact reuse | Continue requested detail scope and verify its gallery; acknowledging selection alone is incomplete. |
| Complete detailed draft set | Stop for final-image selection, upload authorization or complete-set approval; report each separately. |
| Explicit selected-image upload authorization | Upload only those exact versions and verify; do not infer approval from upload. |
| Complete-set design approval | Record exact scope/versions/evidence, then create/reuse Design tickets and View via the post-approval reference. Upload authority is still separate. |

## Design approval and native attachment state

A user's explicit approval in chat or LinearBoard, recorded and read back on the owning specification with exact scope, versions and accessible image links, establishes **design approval** for Design tickets and downstream design-readiness checks. Partial approval covers only that subset; selecting a layout is not complete-set approval. If local-only approved images are inaccessible to downstream workers, report missing accessible references and request only the missing upload authority; do not request the same design approval again.

The attachment's native `approved` field is a separate user-controlled state. Upload as draft, never set it or impersonate the user. Report it accurately even when a recorded chat approval establishes design approval. Never call the native field approved without reading it back. Downstream work must have accessible exact references AND recorded applicable design approval; a draft field alone neither proves nor cancels that evidence. This does not authorize dispatch or implementation.

## Build and verify the HTML review gallery

This is a standard `create-visuals` deliverable, not an optional extra requiring another request. Use the same gallery for direction options and subsequent screen/state drafts, keeping the current review set clear.

- Reuse a supplied or existing visual-review page's layout and useful controls when available. Do not carry over its milestone, images, approval labels or product copy blindly.
- Default to `output/<project-slug>-<milestone-slug>-visual-review/index.html` in the current workspace, or use the user's requested artifact location. Keep a portable local bundle: the HTML plus relative image assets copied byte-for-byte from imagegen outputs, or embedded images when a single-file deliverable is requested. Preserve imagegen originals. Do not rely on expiring URLs, a remote CDN or generator-cache paths as the gallery's only image sources.
- Include every current in-scope board, with a compact contents navigation, readable title, applicable screen/version identifiers, concise state caption and links to its owning LinearBoard specification document plus screen/flow IDs; existing relevant FE issues may be linked as supplementary references but are not prerequisites. Show the image at its full aspect ratio without cropping. Use this presentation metadata only; do not duplicate PRDs, acceptance criteria, decisions, issue state or approval records into a local database or report.
- Support click-to-enlarge, previous/next images, a fit-to-window and readable-detail/original-size view, and Escape to close. Provide keyboard-operable controls, visible focus, useful image alt text and focus return after closing the viewer. Keep the page usable on desktop and narrow screens.
- Make basic browsing work offline with local assets and no mandatory external scripts, fonts or API calls. Loading the page must not regenerate images or mutate LinearBoard. Link to canonical LinearBoard records when network access is available.
- Mark unapproved images clearly as review drafts. If approved and draft references coexist, label each correctly from explicit evidence; opening, browsing or downloading the gallery does not approve an image. Do not implement local approval buttons or persistence that substitutes for canonical approval records.
- For revisions, show the latest intended draft prominently and distinguish retained alternatives or older versions. Reuse valid existing imagegen outputs rather than regenerating them just to build or refresh the gallery.
- Check that all intended images load, navigation reaches the correct board, enlargement and previous/next work, text can be inspected, Escape closes the viewer and keyboard focus returns. Inspect desktop and narrow layouts for clipping or overflow. Verify local image paths and that offline viewing requires no external resources. If a browser capability prevents a check, state that exact limitation rather than claiming it passed.
- Open the completed gallery in the available browser or artifact panel and return its primary HTML link. Individual image links may supplement it, not replace it. Keep the local gallery and copied image assets as a non-canonical convenience artifact; approved final images and product records still belong in LinearBoard.

## Authorized attachment and post-approval handoff

Attach only explicitly selected, upload-authorized finals to their existing owning screen/interaction specification entries. Missing entries block the affected upload; never create a work ticket as a substitute. Follow [application operations](linearboard-operations.md), retain originals and prior versions, and use exact title/screen/version metadata. Read back bytes, ownership and file URL, render the image at the owning entry and inspect the actual UI. Record concise upload verification in the workflow comment without rewriting product rules. Do not attach unselected concepts or duplicate images. Native attachment status remains user-controlled.

Only after explicit complete-set design approval continue with [post-approval Design tickets](create-design-tickets.md). Record the exact approved inventory; new tickets start in Backlog and existing issue states remain unchanged. Design approval does not authorize FE/BE creation, dispatch or deployment. An explicitly requested DESIGN.md-style handoff remains a rendered LinearBoard document linked from the owning entry; do not retain a local PM copy.

Lead the handoff with the gallery link, explain the product-specific idea and a consequential visual choice/revision, then report coverage, gallery checks, remaining limits and exact selection/upload/design-approval/native-field state. Include verified canonical image/ticket links when those stages were authorized. Do not claim usability, implementation or user acceptance from static visuals.
