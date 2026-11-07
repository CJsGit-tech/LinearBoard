# Review changes and their effects

The main agent owns change review. The assigned coding agent writes its own BUG ticket and result comment under the debug workflow. Apply this workflow within the active command and its existing permissions.

## When to review

- When creating or revising a PRD, check its upstream stories, milestone, confirmed decisions and feasibility assumptions. For a revised requirement, also check downstream uses. An explicitly learning-only milestone with no delivery behavior needs no PRD or category View; report that outcome. Missing sources for actual delivery work remain a gap.
- During PRD clarification, use already available feasibility evidence when it could change the options you present. Review the effects of each confirmed answer before saving it or asking a dependent question. Several answers about the same rule can share one review. A tentative suggestion stays open.
- During any command, a user change or worker-reported conflict triggers review as soon as it is received. During a build, tell affected workers which work to pause; independent work continues. If the code violates a clear requirement, fix the implementation within authorized delivery scope. If technical evidence challenges the promise, bring the product choice to the user. An explicit, clear user decision already settles that choice.
- At dispatch readiness, identify the current versions of the ticket, its owning requirements and relevant approved design references. Include their IDs, versions and applicable criteria in the existing assignment record so the final review has a baseline.

## Find the impact and verify feasibility

Compare the previous and proposed behavior. Follow native relations and story/document links in both directions. Search the scoped project for the old rule, capability, or user-facing wording to catch missing links. Identify the specific rules, screens, tickets, acceptance checks and tests affected. The main agent may delegate this read-only investigation to an impact reviewer. Batch related changes; a wording edit with no effect needs no downstream rewrite.

Follow the [planning workflow](planning.md) for the brief official-source check of a user-chosen stack. Detailed SDK and deployment research belongs in create-issues-FE or create-issues-BE. Other earlier commands, including PRD clarification and visual design, use available evidence and record unresolved assumptions for the owning delivery ticket. Continue reviewing affected requirements when a decision changes. During delivery issue creation, check current official platform documentation or the upstream SDK documentation/repository for the scoped capability. A feasibility researcher may do this independently within existing worker limits. Record the source, date, supported finding and remaining uncertainty in the owning record when authorized. If a runtime or hosted experiment is needed, specify the smallest check and its execution target; run it only within authorized execution scope. Keep implementation choices that preserve the promise in the engineering ticket.

## Return an actionable impact result

For a consequential change, identify the triggering decision/source and each affected record/section. State the observed current behavior, specific proposed update, confirmed/proposed/conflicting/unverified status, and the acceptance or dependency effect. Distinguish owning-record edits authorized by the active command from cross-record changes needing sync approval. Follow the existing record-by-record from/to format rather than inventing a second change ledger.

After creating/revising PRDs, changed clarification answers, requested scope changes or design/delivery conflicts, do not finish with a generic reminder to sync. Name the actual affected records and propose the bounded `sync <Project> <Milestone> [scope or new request]` when that is the next missing gate. If the inspected records remain consistent, say so briefly; no sync is needed. Unknown or inaccessible records remain unverified.

This is an in-command review, not a background watcher or a grant to edit linked records. Keep the review in chat until the current workflow authorizes recording it. Do not create local PM audit files. Initialization generates guidance for this method; it does not install hooks or prove an audit ran.

## Reconcile and close

Apply confirmed changes to records authorized by the active command. For sync, present the proposed from/to blocks in chat and wait for the user to approve those specific edits before writing, even when the underlying decision is already confirmed. For anything outside scope, identify its record, precise mismatch and needed action. Never infer authority to change requirements from a worker report. Re-read affected records and use expected versions for writes; on conflict, compare the latest content before retrying. Resume affected workers with verified criteria and source versions and obtain acknowledgment. A partial update or a pending product decision keeps the dependent work paused.

Immediately before moving an issue to In Review, retrieve its current ticket, source requirements and applicable approved references again. Compare them with the versions used for implementation and independent verification. For changes, inspect the actual difference: repeat only affected checks. Hold the transition for a material unresolved mismatch, stale verification or unverified essential behavior. Record the reviewed versions and evidence in the existing handoff. Apply the existing UI, environment-limitation and final-user acceptance rules.
