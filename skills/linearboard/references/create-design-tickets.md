# Post-approval Design tickets

This is the final stage of an active `create-visuals <Project> <Milestone>` request, not an early output of `create-designs`. It may also run when the user explicitly requests Design tickets for an already approved complete design set.

## Gate and scope

Confirm that the user confirmed the style, every requested screen/component and relevant key state has inspected visual coverage, and the user explicitly approved the complete set. New or revised coverage comes from operated, versioned React Native prototypes; valid approved legacy images remain usable. Style selection alone, silence, partial approval or an agent report does not satisfy this gate. Record the approval source, exact screen/component IDs and visual version on the owning specification or comment. Exact-set chat approval is sufficient. Downstream reviewers use the native Approved JPGs and linked specification. Share the local prototype launch details in chat when needed. Follow [the visual approval gates](create-visuals.md#design-approval-and-native-attachment-state). Native attachment approval remains distinct, user-controlled and accurately reported.

A skill-update request alone does not authorize retroactive project writes. Apply the new stage to an active authorized visual workflow or an explicit ticket-creation request. If required artifacts or approval are missing, report the exact gap and keep tickets uncreated; do not generate extra scope or fill gaps with placeholders.

## Create or reuse

Read [application operations](linearboard-operations.md), [issue governance](issue-governance.md) and [issue Views](issue-views.md). Resolve project, milestone, source US/PRDs, specification entries, reviewed originals and approval evidence. Search all applicable issues before creating anything. Reuse a genuinely matching legacy Design issue by screen/flow and version; preserve its identity and lifecycle, and do not restore trashed records without authorization.

Apply the native milestone, its stable M-number tag and each mapped source-story tag. Reuse active team labels (for example, M1 and US1 for US-01); resolve ambiguous mappings before writing. Preserve unrelated labels. Create one Design ticket per coherent screen/flow handoff, grouping its component and state boards where appropriate. Do not create one ticket per PNG, checkbox or error state. Use `DESIGN — {screen or flow} [v#] — {purpose}`, with a real established visual version. Set the exact project and milestone and exactly one native Category child `Design`; preserve applicable source labels. New tickets start in Backlog. Full design approval is not permission to move tickets to Done, create FE/BE work, implement, dispatch or deploy.

Each ticket identifies the expected design handoff and includes:

- Stable SCREEN/flow IDs and the owning specification section.
- Source User Stories, PRDs and applicable acceptance scenarios, with native relations only for actual issue sources; grouped story entries use readable document links.
- Exact approved visual titles and versions. Attach the confirmed JPGs directly to each owning issue, including reused tickets, and identify the screen, state and viewport.
- Declared platform/stack, layout/component/state guidance and required view sizes from the approved specification. Separate observed local behavior, static-visual limits and unverified app behavior; another platform is a separate scope.
- The user's recorded approval evidence and its exact scope, distinguished from the native attachment approval field.

The specification remains the canonical design definition; tickets index the approved handoff rather than inventing new product rules or duplicating full PRDs. Link tickets back from the corresponding specification entries. Create/reuse the project Design View, and verify filters and complete expected membership.

## Required JPG references

For every new or reused Design issue, upload actual JPEG image bytes as native attachments of that issue (filename ending in `.jpg`, MIME `image/jpeg`). Capture the approved version or convert its verified original image. Cover the screens, materially distinct states, and review sizes assigned to that ticket. Name each file by screen, state, version and viewport. Use the owning specification for behavior and keep interactive originals in the workspace. Keep local paths and prototype addresses out of all LinearBoard records. A document attachment, prototype link, or PNG alone does not satisfy the issue handoff.

Search existing issue attachments first and reuse an exact matching JPG. Preserve original files and prior versions. After the user approves the complete visual set, record its scope in an approval comment beginning with **Approved:** (Markdown prefix `**Approved:`) on the owning screen specification. Before uploading, register each confirmed JPG in the specification’s native `confirmed_jpgs` field, preserving existing entries, with issue_id, filename (name), screen, visual_version, SHA-256 of the final JPG bytes (sha256), and approval_comment_id. Upload those exact bytes. LinearBoard inherits Approved on creation. For an existing matching draft, set approval to approved using its current version. Verify the returned approval is approved and inherited_from_comment matches the decision. Other files require their own approval. Download the saved JPG, compare it with the intended bytes, and open the ticket to verify the thumbnail renders. If any required image is missing or fails verification, report the affected issue and keep the handoff incomplete.

## Verify and report

Read back every ticket, source relation, image link, project/milestone/category, version and preserved state. Verify rendered content, access to the approved JPGs, no duplicates, and the saved Design View. Report ticket links and the View with its actual count. Distinguish approved design handoff from implementation evidence and native attachment state.
