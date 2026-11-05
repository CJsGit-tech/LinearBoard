# Post-approval Design tickets

This is the final stage of an active `create-visuals <Project> <Milestone>` request, not an early output of `create-designs`. It may also run when the user explicitly requests Design tickets for an already approved complete design set.

## Gate and scope

Confirm that the concrete layout was selected or selection explicitly delegated, all screens, required components and relevant key states in the requested scope were generated and inspected, and the user explicitly approved that complete set. Style selection alone, silence, partial approval or an agent report does not satisfy this gate. Record the user's approval with its source, exact screen/component IDs, visual versions and original image links in the owning LinearBoard specification/comment. Explicit chat approval recorded against the exact set/versions is sufficient for this Design-ticket gate and downstream design-readiness checks; do not require the user to repeat it in the application. Downstream workers must still have accessible exact image references. Follow [the visual approval gates](create-visuals.md#design-approval-and-native-attachment-state). Native attachment approval remains distinct: respect its API restrictions, never impersonate the user, and report the actual native field without mislabeling it.

A skill-update request alone does not authorize retroactive project writes. Apply the new stage to an active authorized visual workflow or an explicit ticket-creation request. If required artifacts or approval are missing, report the exact gap and keep tickets uncreated; do not generate extra scope or fill gaps with placeholders.

## Create or reuse

Read [application operations](linearboard-operations.md), [issue governance](issue-governance.md) and [issue Views](issue-views.md). Resolve project, milestone, source US/PRDs, specification entries, reviewed originals and approval evidence. Search all applicable issues before creating anything. Reuse a genuinely matching legacy Design issue by screen/flow and version; preserve its identity and lifecycle, and do not restore trashed records without authorization.

Create one Design ticket per coherent screen/flow handoff, grouping its component and state boards where appropriate. Do not create one ticket per PNG, checkbox or error state. Use `DESIGN — {screen or flow} [v#] — {purpose}`, with a real established visual version. Set the exact project and milestone and exactly one native Category child `Design`; preserve applicable source labels. New tickets start in Backlog. Full design approval is not permission to move tickets to Done, create FE/BE work, implement, dispatch or deploy.

Each ticket identifies the expected design handoff and includes:

- Stable SCREEN/flow IDs and the owning specification section.
- Source User Stories, PRDs and applicable acceptance scenarios, with native relations only for actual issue sources; grouped story entries use readable document links.
- Exact approved visual titles, versions and accessible original image links; shared boards may be linked without duplicate uploads.
- Concise layout/component, responsive and state guidance from the approved specification, plus any explicit limitations of static visuals.
- The user's recorded approval evidence and its exact scope, distinguished from the native attachment approval field.

The specification remains the canonical design definition; tickets index the approved handoff rather than inventing new product rules or duplicating full PRDs. Link tickets back from the corresponding specification entries. Create/reuse the project Design View, and verify filters and complete expected membership.

## Verify and report

Read back every ticket, source relation, image link, project/milestone/category, version and preserved state. Verify rendered content and access to originals, no duplicates, and the saved Design View. Report ticket links and the View with its actual count. Distinguish approved design handoff from implementation evidence and native attachment state.
