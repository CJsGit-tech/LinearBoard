# Create design direction and screen specifications

`create-designs <Project> <Milestone>` (including `prototype-ui` aliases) owns the two native design documents, three interactive UI proposals for an open direction, and the user’s style decision. Apply the [shared design method](design-direction.md).

## Resolve and recommend

Resolve exact team/project/native milestone. Read vision, grouped stories/legacy sources, PRDs, confirmed decisions, current design documents, actual screens/approved references and relevant technical constraints already recorded in frontend or backend tickets. Search all pages before creating; preserve canonical identities, stable SCREEN/flow IDs, mappings, constraints, unrelated content and history. Missing visuals do not block written drafts. Consequential behavior gaps remain open in the owning PRD; never invent a control to fill them.

Consult an existing Technical Baseline where platform limits affect the interaction. Use available design documents and the supplied brief to establish the audience, main task and constraints against which all three proposals will be judged. If the overview is a draft, preserve its assumptions as proposals. Identify any binding styling separately. Resolve material product questions with the owner and use shared illustrative data for the comparison.

## Two canonical documents

During proposal generation and retries, treat LinearBoard as read-only. Keep Design Overview and Screen and Interaction Specification as-is, including their links. Present proposals in chat using the local HTML index. Do not save proposal lists, checks, pending-selection notes or comments to LinearBoard. If a document is absent, use the supplied brief or ask for missing context. Only after the user explicitly selects a direction may you create/reuse and cross-link the following documents to record the selected style:

- `<Project> <Milestone> — Design Overview`: outcome, primary task/role, ranked task/risk priorities, experience priorities and their rationale, inspected references with relevant observations, and any established brand constraints. Link to source US/PRDs and the detailed specification; retain only material unknowns.
- `<Project> <Milestone> — Screen and Interaction Specification`: stable SCREEN/flow entries with target platform/stack, purpose, entry/exit, supported content/actions/outcomes, relevant states and source acceptance IDs. Specify information relationships, accessible control behavior (including open panels), and target-specific content priorities. Record concrete appearance rules only when grounded in a user decision, an applicable design system or an approved reference. After selection, record the chosen proposal’s concrete appearance rules. Place shared rules once and link consumers; preserve platform conventions and asset provenance.

Use [interaction handoff](interaction-loading-motion.md) for the lifecycle and motion contract, including enforceable input policy, recovery and focus. Specify actual concise labels and necessary guidance using the shared copy methods. Keep planned behavior/checks distinct from observed results.

## Build and select three proposals

Build exactly three runnable proposals, A, B and C, for the same audience, task, sample content, starting state and viewport. Apply these principles:

1. **Start with the visitor’s journey.** Read the Design Overview and Screen and Interaction Specification together. Identify the entry point, what the visitor needs to understand or compare, and the action and outcome the proposal must demonstrate. Use the missing-document rule above where applicable.
2. **Give each proposal a distinct brand idea.** Choose a creative direction grounded in the audience and product. Carry it from entry through the main action using composition, imagery, typography, color and interaction within confirmed brand constraints. Explain one concrete tradeoff for each proposal.
3. **Guide the eye across the whole page.** Decide what visitors should notice first and next. Use scale, contrast and shared alignment to make that order visible.
4. **Group with spacing first.** Use proximity and whitespace to show relationships. Add a border or background when it clarifies a group, control or state.
5. **Match the format to the task.** Let narrative content flow through text and imagery. Align values people need to compare. Reserve cards for independent items people browse individually.
6. **Make interactions clear.** Build with semantic HTML, local or compiled Tailwind CSS, and JavaScript for working controls, motion and component feedback. Show what is selectable, what changed and where keyboard focus is. Preserve the same feedback with reduced motion.
7. **Use navigation to give each task enough space.** Decide what visitors need at entry and what they can open when relevant. Multi-screen journeys and interaction designs are valid. Choose direct links, dedicated screens, or in-place disclosure according to the task. Use descriptive destinations, indicate the current screen, support Back and keyboard focus, and retain meaningful selection or filter context when visitors return. Keep the primary next action discoverable. Before building, name the job of each destination and how visitors reach it. When an entry screen feels crowded, move a secondary task to a clearly labeled destination and keep a direct route to the main action. During review, follow that route and return to verify that the visitor keeps their place.
8. **Review each complete rendered proposal.** Open every version from the offline index, inspect each scoped screen at its intended width, and exercise the entry, forward and return paths. Compare the directions side by side. If sections read as interchangeable tiles or the brand idea disappears beyond the opening, revise and inspect again. Distinguish observed checks from assumptions.

Use the [design-pro comparison method](design-direction.md#apply-design-pro-within-the-current-stage) to recommend one rendered direction and explain its tradeoff. Present the references actually used alongside each local proposal. Save versioned entries and the offline index under the isolated review bundle. Browser review is required. Capture screenshots only when explicitly requested, and upload only with separate authorization. Provide all three direct HTML links.

Ask the user to select the exact proposal/version or request revisions. Until they choose, leave the decision pending in create-designs and resume it here. Record their selection, scope and exact visual version in Design Overview; carry its palette, type, layout, controls and motion rules into Screen and Interaction Specification. Keep the local HTML links in chat and the review bundle. A selection confirms the style only. For a bounded edit with an already confirmed direction for the same scope/version, reuse the selection; reopen comparison when a new direction is requested.

## Verify and hand off

After selection, reconcile feedback in its owner, preserving superseded decisions in native history/comments. Preserve source detail and read back destinations before removing moved content. Create no QA document and change no issue/state.

Retrieve both documents and verify native project/milestone placement, reciprocal/source links, stable IDs, acceptance coverage, preserved constraints and reference provenance. Verify that LinearBoard records contain no local paths or prototype addresses. Confirm that the document has observable UX, component and state criteria for later mockup inspection; method links or “modern/polished” adjectives alone are insufficient. Check proposed versus approved status and planned versus tested claims. Written design is not usability evidence or visual approval.

Use the root recommendation rule. While the style choice is pending, ask for the exact proposal/version and identify the reply as a continuation of `create-designs`. Recommend a later command after verifying the selection and checking the next applicable deliverable.
