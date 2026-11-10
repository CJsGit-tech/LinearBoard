# LinearBoard design and UX method

## Start from the task

Read the source PRDs, their acceptance criteria and any existing design documents. During `create-designs`, use the brief where a document is missing and keep LinearBoard read-only until the user selects a direction. For `create-visuals`, start from the recorded selection and matching specification. Separate required behavior, confirmed platform and brand constraints from proposed layouts. Use the overview to identify who is acting, their most important task and what they need to notice first. A coach checking the next appointment needs time and member grouped together; a manager comparing utilization needs aligned values. Choose the composition that serves the task.

## Explain the design before building

Before writing or revising mockup code, share a short design rationale in chat. Ground it in the brief and existing decisions. Name the audience, the task they came to complete and what success looks like. Explain what they need to notice first, what they can open later, and how they reach the main action. Tie each important choice of layout, labels, icons or motion to a user need. Mention a reference only when it helps make that choice concrete.

For `create-designs`, state what the proposals will hold in common and give one meaningful difference and tradeoff per direction. For `create-visuals`, carry the selected direction forward and explain how it applies to the remaining screens or states. Name the interaction that will test the design assumption. Then proceed within the authorized scope unless an open decision materially changes the design.

## Target platform

Scope the declared platform and requested review sizes. Follow its navigation, input and accessibility conventions. Both commands author every draft and review screen as React Native components. Use the project's compatible React Native tooling in an isolated prototype, or default to Expo for a new prototype. Production stack selection stays with the product's delivery work.

- For iOS or Android, launch and operate the prototype on the scoped simulator, emulator or device. For a web target, use React Native Web from the same React Native source. Review only the requested target and sizes. If the required runtime is unavailable, keep the source, report the blocker and unverified screens or states, and complete the required checks before requesting the dependent selection or approval.
- Keep the versioned prototype source, package manifest and lockfile, local assets and fictional fixtures together. Provide an in-app review menu with labeled proposal, screen and state entries. Share the project location, install and launch commands, required runtime, and menu entries or tested deep links in chat. For an Expo prototype, use the scoped option such as `npx expo start --ios`, `npx expo start --android` or `npx expo start --web` with the required dependencies installed. See [Expo launch instructions](https://docs.expo.dev/get-started/start-developing/) and [web setup](https://docs.expo.dev/workflow/web/).
- Do not deliver standalone HTML drafts, DOM/CSS mockups, or an HTML review index. A React Native Web preview is evidence only for the web rendering that was operated.

## Design direction

Inspect existing product screens and supplied references first. If a visual decision remains open, inspect relevant design examples and record which observation informed the choice. Explore hierarchy, density, type, imagery and grouping within confirmed constraints. Use spacing to group related content, alignment to aid comparison and contrast to distinguish the primary action. Reserve strong emphasis for information that deserves attention. Choose labels in the product locale and omit filler. Test long names, real units and realistic content density.

## Apply design-pro within the current stage

Read the bundled sibling [design-pro skill](../../design-pro/SKILL.md) and the guidance for the requested platform and design task. Resolve the link relative to this file so both commands use the version shipped alongside LinearBoard. Reuse the brief, requirements, design system and applicable Technical Baseline. Apply its methods within the isolated draft and current LinearBoard stage. If the bundled skill is missing, report the missing dependency and continue with the shared design method here.

For an open direction, use identity and composition to turn the product’s subject and primary task into different ideas about what readers or users notice, compare or do first. Compare the rendered options against the same brief and recommend one with a specific reason and tradeoff. The user selects. For an established direction, choose the lens that addresses the observed problem, such as craft for an unclear control, recover for an interrupted task, or reconcile for inconsistent screens. Revise and recheck the affected journey.

## Find resources for runnable drafts

Start with the project's design system, selected references and [React Native components](https://reactnative.dev/docs/components-and-apis). For gaps, prefer compatible native controls or a maintained React Native package. Use [Lucide](https://lucide.dev/icons/) as the default icon family. Uiverse may supply visual inspiration when relevant. Recreate any useful pattern with React Native components and styles. Check license, dependencies, platform support, interaction states and reduced motion before adopting a resource.

For each external resource used, show the screen/control/state, exact component or asset name, source link and credited author when available, what was adapted and why it fits. Prefer a pinned source link when available. Document shared choices once and reuse them wherever the same interaction recurs. Keep these references alongside the proposal for review. After the user chooses a direction, carry its mappings into the screen specification. During `create-visuals`, reuse those choices and look up only what newly covered states need.

Bundle required assets and attribution locally. Launch the prototype and check that icons render, controls work and reduced motion preserves the same feedback. Use local fixtures so checks need no live product services.

## Controls and interactions

Choose between an icon alone and an icon with a visible text label based on the action, its context and the audience. An icon can stand alone for a familiar, unambiguous action, such as closing an open dialog. Give every icon-only control an accessible name that describes the action. Pair the icon with a concise visible label for unfamiliar, ambiguous or consequential actions, or when people need to distinguish similar choices. When text already names the action, hide a decorative icon from assistive technology so the label is announced once. During draft review, check whether someone could predict the action before clicking, including on touchscreens where hover hints are unavailable.

- Use visible options for a few important choices and a labeled dropdown when space or option count warrants it. Specify the open panel, selected item, keyboard movement, confirmation, dismissal and focus return.
- Forms need persistent labels and clear submission behavior. Keep entered values on failure, show actionable feedback beside the relevant field and prevent duplicate submits while pending.
- Use dialogs for bounded tasks. Provide a clear exit and restore focus to the initiating control. For lists distinguish no data, no matching results and load failure, each with an appropriate next action.
- Keep keyboard focus visible, preserve reading order and convey status through text or shape as well as color. Motion should explain a state change and respect reduced-motion preferences. Apply [interaction guidance](interaction-loading-motion.md) for applicable loading, retry and recovery behavior.

## Build and review the runnable prototype

After sharing the rationale, use this sequence for each new draft. For a revision, start with the step affected by the change and recheck the affected journey.

1. Map the screens. Name the job of each destination, its entry point, the main action and the return path. Decide what stays visible and what opens on demand.
2. Build the screens with React Native components such as `View`, `Text`, `Pressable` and `TextInput`. Use the same sample scenario across competing proposals and give interactive controls accessible labels and roles.
3. Apply the visual direction with React Native styling. Use type, spacing, alignment and contrast to show priority and grouping. Check safe areas, layout and realistic content at the intended sizes.
4. Wire navigation, selections and applicable pending, success, failure and retry states with local fixtures. Preserve meaningful context when the visitor returns.
5. Open each entry from the in-app review menu on the scoped runtime. Follow the main task and its return path, then exercise alternate states and relevant touch, keyboard, focus and reduced-motion behavior.
6. Fix and verify. Repeat the affected checks and hand over launch instructions, menu entries, observed results and any untested paths.

## From written decisions to observed results

During proposal review keep rationale and checks with the local proposals. After the user selects a direction, record its visual priorities and reasons in the overview. In the screen specification connect the screen ID and requirement to the intended action, outcome and relevant state. Mark flexible presentation choices as proposals. In the visual study vary only open choices while holding task, data and viewport constant.

After style confirmation, operate each scoped flow using realistic fixtures. Check the controls while open, after input, and on applicable failure/recovery paths. Inspect the rendered hierarchy, copy, clipping and focus. Repair and recheck affected states. Record observed results and remaining coverage against the same screen IDs. Keep mockup evidence separate from production verification.
