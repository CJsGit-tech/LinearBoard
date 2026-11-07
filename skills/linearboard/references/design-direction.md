# LinearBoard design and UX method

## Start from the task

Read the source PRDs, their acceptance criteria and any existing design documents. During `create-designs`, use the brief where a document is missing and keep LinearBoard read-only until the user selects a direction. For `create-visuals`, start from the recorded selection and matching specification. Separate required behavior, confirmed platform and brand constraints from proposed layouts. Use the overview to identify who is acting, their most important task and what they need to notice first. A coach checking the next appointment needs time and member grouped together; a manager comparing utilization needs aligned values. Choose the composition that serves the task.

## Explain the design before building

Before writing or revising mockup code, share a short design rationale in chat. Ground it in the brief and existing decisions. Name the audience, the task they came to complete and what success looks like. Explain what they need to notice first, what they can open later, and how they reach the main action. Tie each important choice of layout, labels, icons or motion to a user need. Mention a reference only when it helps make that choice concrete.

For `create-designs`, state what the proposals will hold in common and give one meaningful difference and tradeoff per direction. For `create-visuals`, carry the selected direction forward and explain how it applies to the remaining screens or states. Name the interaction that will test the design assumption. Then proceed within the authorized scope unless an open decision materially changes the design.

## Target platform

Scope the declared platform and requested view sizes. Follow existing navigation, terminology, controls and accessibility conventions for that platform. A browser depiction of a native screen is a design study. Defer SDK and deployment research to FE/BE issue creation.

## Design direction

Inspect existing product screens and supplied references first. If a visual decision remains open, inspect relevant design examples and record which observation informed the choice. Explore hierarchy, density, type, imagery and grouping within confirmed constraints. Use spacing to group related content, alignment to aid comparison and contrast to distinguish the primary action. Reserve strong emphasis for information that deserves attention. Choose labels in the product locale and omit filler. Test long names, real units and realistic content density.

## Apply design-pro within the current stage

Read the bundled sibling [design-pro skill](../../design-pro/SKILL.md) and the guidance for the requested platform and design task. Resolve the link relative to this file so both commands use the version shipped alongside LinearBoard. Reuse the brief, requirements, design system and applicable Technical Baseline. Apply its methods within the isolated draft and current LinearBoard stage. If the bundled skill is missing, report the missing dependency and continue with the shared design method here.

For an open direction, use identity and composition to turn the product’s subject and primary task into different ideas about what readers or users notice, compare or do first. Compare the rendered options against the same brief and recommend one with a specific reason and tradeoff. The user selects. For an established direction, choose the lens that addresses the observed problem, such as craft for an unclear control, recover for an interrupted task, or reconcile for inconsistent screens. Revise and recheck the affected journey.

## Find resources for runnable drafts

For both `create-designs` and `create-visuals`, start with the project's design system and any references already selected. When a draft needs an icon, reusable UI component or animation and there is no suitable reference yet, proactively look up the relevant asset or example in an official catalog, component guide or maintainer's repository. Choose what fits the action, visual direction and lightweight HTML/CSS/JavaScript draft. Use a native control or a simple CSS transition when it serves the interaction.

Use the Uiverse MCP when the project’s own components and native controls leave a concrete gap. Describe the screen, action, state, visual direction and platform in the search brief. Use search_components to find candidates and inspect_component and get_component_source to inspect promising examples. Check the source, author, license, dependencies, selector scope, input states and motion. Use preview_components when appearance or motion matters, then operate the adapted control in the rendered draft, including keyboard and reduced-motion behavior where applicable. A catalog preview establishes only what was observed there.

Choose as many or as few references as the task warrants, including zero. If the MCP is unavailable or no result fits, use a suitable local or native control. Disclose unavailable checks and cite only sources actually used.

Use these sites as starting points across projects. Browse the categories relevant to the draft and choose by audience, visual direction, intended interaction and target stack.

| Draft need | Reference sites |
| --- | --- |
| Icons | Use [Lucide](https://lucide.dev/icons/) as the default icon family. |
| Styled controls | Use [levxyca’s Uiverse button](https://uiverse.io/levxyca/tidy-mayfly-7) as an HTML/CSS reference when an outlined button suits the action. Check focus and pressed feedback in the draft and retain the license notice when copying code. |
| Motion or animation | Use [Uiverse](https://uiverse.io/) to find a specific effect when motion helps explain a state change. Link the exact example used and verify equivalent feedback with reduced motion. Motion is optional. |

Other official catalogs or maintainer examples may better fit a particular draft. For imagery, link the selected visual to the screen or section where it appears and identify whether it served as inspiration or was bundled.

For each external resource used, show the screen/control/state, exact component or asset name, source link and credited author when available, what was adapted and why it fits. Prefer the pinned source link returned by the MCP. Document shared choices once and reuse them wherever the same interaction recurs. Keep these references alongside the proposal for review. After the user chooses a direction, carry its mappings into the screen specification. During `create-visuals`, reuse those choices and look up only what newly covered states need.

Bundle any required assets and attribution locally. Open the draft offline and check that the icons render, the controls work and the same feedback is available with reduced motion.

## Controls and interactions

Choose between an icon alone and an icon with a visible text label based on the action, its context and the audience. An icon can stand alone for a familiar, unambiguous action, such as closing an open dialog. Give every icon-only control an accessible name that describes the action. Pair the icon with a concise visible label for unfamiliar, ambiguous or consequential actions, or when people need to distinguish similar choices. When text already names the action, hide a decorative icon from assistive technology so the label is announced once. During draft review, check whether someone could predict the action before clicking, including on touchscreens where hover hints are unavailable.

- Use visible options for a few important choices and a labeled dropdown when space or option count warrants it. Specify the open panel, selected item, keyboard movement, confirmation, dismissal and focus return.
- Forms need persistent labels and clear submission behavior. Keep entered values on failure, show actionable feedback beside the relevant field and prevent duplicate submits while pending.
- Use dialogs for bounded tasks. Provide a clear exit and restore focus to the initiating control. For lists distinguish no data, no matching results and load failure, each with an appropriate next action.
- Keep keyboard focus visible, preserve reading order and convey status through text or shape as well as color. Motion should explain a state change and respect reduced-motion preferences. Apply [interaction guidance](interaction-loading-motion.md) for applicable loading, retry and recovery behavior.

## Build and review the runnable page

After sharing the rationale, use this sequence for each new draft. For a revision, start with the step affected by the change and recheck the affected journey.

1. Map the screens. Name the job of each destination, its entry point, the main action and the return path. Decide what stays visible and what opens on demand.
2. Build the HTML. Put realistic content, headings, landmarks, links and controls in task order. Use the same sample scenario across competing proposals.
3. Apply the visual direction in CSS. Use type, spacing, alignment and contrast to make priority and grouping visible. Check the layout at the intended review sizes with realistic content.
4. Connect the interactions in JavaScript where needed. Wire navigation, selections and the applicable pending, success, failure and retry states using local sample data. Preserve meaningful context when the visitor returns.
5. Review in the browser. Open each entry from the offline index. Follow the primary task and its return path, then exercise relevant alternate states, keyboard controls and reduced motion. Check whether the rendered page supports the stated rationale.
6. Fix and verify. Revise the source where the layout or behavior makes the task harder, repeat the affected checks and hand over direct links with observed results and any untested paths.

## From written decisions to observed results

During proposal review keep rationale and checks with the local proposals. After the user selects a direction, record its visual priorities and reasons in the overview. In the screen specification connect the screen ID and requirement to the intended action, outcome and relevant state. Mark flexible presentation choices as proposals. In the visual study vary only open choices while holding task, data and viewport constant.

After style confirmation, operate each scoped flow using realistic fixtures. Check the controls while open, after input, and on applicable failure/recovery paths. Inspect the rendered hierarchy, copy, clipping and focus. Repair and recheck affected states. Record observed results and remaining coverage against the same screen IDs. Keep mockup evidence separate from production verification.
