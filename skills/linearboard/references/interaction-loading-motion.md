# Interaction handoff

Use this local interaction guide together with the [LinearBoard design method](design-direction.md) in both commands.

## Canonical contract

In `create-designs`, use the lifecycle paragraph/fields from behavior-and-timing inside the owning screen specification, linked to current US/PRD/acceptance IDs. Record shared behavior once; consumers link it. Specify only states the task can reach. Include pending-input policy, preserved data/focus, cancellation/timeout ownership and how to reach states for later checks. For motion, record purpose, properties, duration/easing, interruption and reduced-motion alternative once per shared pattern.

Distinguish location, toggling and widget selection with appropriate semantics (aria-current, aria-pressed, aria-selected only in a supporting pattern), independently of hover/focus. If tooltips exist, support focus access, pointer retention and Escape dismissal. Reduced-motion alternatives must cover CSS and JavaScript animation paths.

Keep the input policy enforceable: say what pauses, remains usable or supersedes earlier work. Dimming, pointer-events, aria-busy or aria-disabled alone cannot block all activation; use appropriate native/handler guards and focus semantics. Keep status/cancel reachable outside inert content. Release controls on completion/failure/cancel/timeout; retained results must keep their matching committed filter, and late responses must not erase timeout or reopen closed UI. These are scoped policy decisions, not a reason to lock unrelated work.

## Mockup and delivery evidence

In `create-visuals`, implement the contract, then use the shared [rendered review](design-direction.md#from-written-decisions-to-observed-results) pass to operate its relevant pointer/keyboard and recovery paths. Label fixtures and unavailable checks; instant local work needs no fake waiting. Put observed results in the existing LinearBoard record, not another local report. Carry the contract into delivery acceptance, where actual-product verification remains necessary. Written rules, stills and local simulations prove different things; none establishes untested screen-reader/native behavior.
