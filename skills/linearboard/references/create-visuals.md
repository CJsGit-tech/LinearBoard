# Build mockups for interactive review

`create-visuals <Project> <Milestone>` turns canonical specifications into isolated HTML/CSS/JS mockups, with a local HTML index and direct links to each runnable study. Apply [shared design integration](design-direction.md): the same LinearBoard principles used in `create-designs` now govern implementation and rendered review. Build UI in code; do not use imagegen for layouts or manufactured screenshots. Separately requested raster artwork is a different asset task.

Consume the existing overview/specification and US/PRDs under the shared ownership and platform-scope contract. Build/check only the declared target and review sizes, without automatic Web/Mobile or desktop/phone pairs. An HTML depiction of an explicitly requested app target remains a design study, not that app's implementation or validation.

## Receive the selected direction

Read the selection recorded by create-designs in Design Overview and the matching Screen and Interaction Specification. Verify the scope, version and runnable artifact. Reuse an existing exact-scope user confirmation, including valid legacy references. If the style decision is missing, return to [create-designs](create-designs.md) for the proposals and selection. For a bounded correction within the chosen direction, revise the affected source and preserve its history.

## Step 2 — Remaining screens and component designs

Begin only after the user explicitly confirms the displayed style/version for this scope. Cover every scoped screen and applicable component state, including opened dropdowns, filled forms, validation, loading and recovery.

Use [LinearBoard’s design method](design-direction.md) to apply the user-selected visual direction to the specified tasks, components and content. Keep source/fixtures inside the isolated review bundle, separate from production. Use local/mock state; no live submissions, credentials or backend integration merely for screenshots.

Reuse the component references recorded for the selected proposal. Apply the [focused design-pro critique](design-direction.md#apply-design-pro-within-the-current-stage) to observed issues, and search Uiverse only for newly covered states that need a reference. Include any new mappings in the scoped handoff.

Run the shared [rendered review](design-direction.md#from-written-decisions-to-observed-results), including actual exposed component states and the mandatory UI-copy audit, against the owning specification. Apply [interaction handoff](interaction-loading-motion.md) to scoped lifecycle checks and task-based visual critique to material visual work. Repair source, re-render and re-operate affected states before handoff; screenshots alone do not finish this step. Record corrections, observed checks, fixtures and limits once in the owning specification/comment, not a duplicate local checklist/report.

## Deliver interactive HTML

Keep versioned runnable HTML entry points, scripts, assets and reproducible fixtures together under `output/<project>-<scope>-visual-review/`. Provide an offline index and direct HTML links in chat per concept or screen. Make component states reachable through working controls or stable scenario links. Open each entry from the delivered index in a browser and exercise its interactions. Before approval, capture screenshots only on request. After complete-set approval, upload the confirmed references as JPG images on each owning Design issue as part of handoff.

## Selection, progress and recovery

Resume from the selected version. Record the visual version, screen IDs, covered and pending states, and complete-set decisions in the owning specification or comment. Keep local HTML locations and prototype addresses in the workspace and chat. After approval, link the owning Design issues and their native Approved JPG references from the specification.

## Gates and valid stopping points

After style selection, build and check the remaining scoped screens and states, then return the complete index and request complete-set design approval. The approval reply resumes `create-visuals` for the reviewed scope and version. Record explicit approval against exact versions and scope. Only then create or reuse [Design tickets and their View](create-design-tickets.md). Verify downstream reviewers can access the exact approved JPGs on their owning Design issues and that their previews render; other sharing or uploads require their own scope.

## Design approval and native attachment state

Style selection, complete-set approval, required issue JPG uploads and user-controlled attachment approval are distinct. Preserve applicable legacy references. For explicitly requested uploads follow [application operations](linearboard-operations.md) and verify the exact version.
