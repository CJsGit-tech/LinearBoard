# Interaction, loading and motion specification

Apply during `create-designs` and `create-visuals` to the interactions actually in scope. These rules develop the user's supplied interaction/loading/motion guidance. Timing values below are starting points to tune against the task and observed response, not universal performance guarantees. Do not add tooltips, drag/drop, optimistic actions, offline queues or progress widgets to a product that does not need them.

## Describe behavior, not a state-name checklist

For each meaningful control or shared component pattern, record the trigger, default/hover/focus/pressed/selected/unavailable/busy treatment as applicable, resulting content/state, persistence, and focus destination. Shared behavior has one owner linked by screens. Do not manufacture every state for every element. Separate current location from selection: use aria-current for location, aria-pressed for toggle/filter buttons, and aria-selected only in a supporting widget pattern. Labels and semantics must match real behavior.

Selection persists after the pointer leaves; hover is temporary; focus remains independently visible. Combine them without losing legibility. Make click targets identifiable without hover. A whole row/card gets a pointer and activation treatment only when its whole surface truly activates; avoid nested interactive targets. Keep secondary actions available to keyboard and touch.

## Plan states and reactions before visual polish

During flow mapping identify time/data/network boundaries; during screen specification inventory applicable initial/loaded/empty/refresh/partial/error/stale/not-found states by region. Add action and input states only where those controls exist. Carry them through visual references, an explicitly requested interactive prototype and delivery acceptance; do not leave essential waiting/recovery behavior until an end-stage polish pass. A design document or still image establishes intent, not implemented behavior.

For each meaningful trigger, keep a compact contract in its owning specification:

| Trigger / affected region | Immediate acknowledgment | Waiting feedback / timing | Input availability | Success | Failure / timeout / cancel | Focus / preserved state |
| --- | --- | --- | --- | --- | --- | --- |
| Actual scoped action | Observable response before the result arrives | Specific operation and region, visible status and any delayed decoration | Explicitly list controls that stay enabled, pause, supersede work or cancel | Result and announcement | Recovery and exact restoration | Destination and retained inputs/filter/scroll |

Do not fill every possible state merely to complete a template. A no-results filter state differs from first-use empty content. Static/local operations need no fake loading. Progress or optimistic behavior must be supported, not inferred from a long wait or a generic example.

### Pending-input policy must be enforceable

Choose by the actual task: safely allow new input to supersede old work, pause conflicting input until completion, or keep an independent region usable. State that choice explicitly and make it obvious to the user. Race protection alone does not explain what the user can do, and a loading label alone does not block input.

If input is paused, use real activation guards/native disabled controls and an appropriate focus/accessibility mechanism for the affected content. Dimming, pointer-events, aria-busy or aria-disabled by themselves do not block every mouse/keyboard path. Keep the status and any cancel/close control outside an inert/busy content region. Do not put an invisible full-page blocker over unrelated navigation. Explain what is paused and how to continue.

Show the pending operation and scope immediately; delaying a decorative spinner must not leave the user unsure whether the action was received. Restore controls on success, error, cancel and timeout. If cancellation/failure leaves old results visible, restore the matching committed filter instead of labeling them with the failed pending choice. Have a finite timeout/recovery path; never keep a loader or input lock indefinitely. When timing out, late success must not silently erase the error or reopen closed UI.

Verify the policy with actual pointer and keyboard attempts, not only style inspection or attribute checks. Test cancel/error/timeout release as well as the successful path. For one independent widget, scope its lock/error locally rather than treating all loading as a reason to freeze the whole interface.

## Loading and recovery contract

Specify what stays visible, what becomes busy, the completion/failure route, whether repeat activation is blocked, and what happens on cancel/navigation/newer input. Preserve filters, entered data and browsing position where relevant. Old responses must not replace a newer selection; closing an overlay must cancel or ignore its late work. Never announce success from an unconfirmed request.

- Fast/local results appear immediately. A roughly 150–300 ms delayed visual indicator can avoid flicker; immediate pressed feedback or a short status label can still acknowledge input. Do not add simulated delay to production interactions or hold ready content merely to satisfy a minimum loader duration.
- Use skeletons for a predictable initial content layout; match grouping, image proportions and responsive placement. Reserve image dimensions/space. A gentle pulse is optional and becomes static under reduced motion. Do not show a full-page skeleton for an action or replace useful loaded content during refresh.
- Use an inline indeterminate indicator for an action. Keep the action's dimensions stable and prevent duplicate activation while it is pending; leave close, cancel and independent navigation usable. Completion may be evident from the updated result rather than a redundant success toast.
- Longer work needs a truthful status and recovery path. Use determinate progress only when progress is measurable, never a fabricated percentage. Cancel/background execution require supported product behavior. A slow action is not proof that a service is offline.
- During refresh keep valid old results with an explicit updating/stale explanation. Preserve successful regions on partial failure when applicable. Clear stale/busy labels on completion and retain actionable failure information on error. A confirmed offline mode may show cached content or queue supported safe work; do not invent it from a generic failure.
- Optimistic changes apply only where the product can tolerate reconciliation and a defined rollback. Do not apply them to payments, destructive or consequential irreversible actions by default. Specify failure recovery before promising optimistic behavior.

Use aria-busy on the affected region, with concise status announcements that remain available while that region is busy. Avoid repeated announcements from every skeleton cell. Restore meaningful focus if a retry or refresh replaces the previously focused control.

## Hover, touch and hints

Use subtle tint/underline/transform feedback without reflow or hidden essential information. Limit hover-only effects to suitable pointer/hover media conditions; touch gets immediate pressed feedback and visible activation paths. Hover must not be the sole way to discover or perform an action.

Keep focus-visible styling distinct with adequate contrast; do not remove keyboard focus without replacement. Unavailable controls must stay understandable, with a reason when needed; reduced opacity alone is not an explanation. Native disabled buttons prevent duplicate input; custom aria-disabled controls also need actual activation guards.

Tooltips are for nonessential short explanations, not a substitute for labels or accessible names. If needed, reveal on focus and after a short hover delay, allow Escape dismissal, and retain them while the pointer is over the trigger/content. Essential help must have a visible/touch-accessible route. Interactive content belongs in a suitable popover, not a tooltip. Do not add icon-only actions just to demonstrate tooltip behavior.

## Purposeful motion

State the purpose, animated properties, duration/easing, interruption behavior and reduced-motion alternative once per shared pattern. Prefer opacity/transform for short transitions and keep layout/input responsive. Repeated layout changes, large movement, distracting loops and flashing are not polish.

Useful starting tokens: hover/state changes about 100–150 ms, controls about 150–200 ms, menus about 150–250 ms, modal entrances about 200–350 ms with a shorter exit where appropriate. Use ease-out for entrance, ease-in for exit and linear only for continuous loops such as an indeterminate spinner. These values may change with the actual interface. Respect prefers-reduced-motion in both CSS AND JavaScript animation paths; static labels/cues must still communicate state. Do not force shakes, zooms or bouncing as universal feedback.

## Review evidence

Written specifications and images can establish intended state cues, not working hover, loading completion, focus behavior or animation. For authorized interactive mockups, operate them: fast/slow completion, failure/retry, repeat activation, rapid input, closing mid-load, keyboard/focus return, narrow/touch paths and reduced-motion where available. Mark simulated requests and unavailable checks. Do not call static inspection a runtime pass or claim screen-reader/accessibility conformance from a visible focus ring. Carry applicable contracts into delivery acceptance without expanding the product scope.
