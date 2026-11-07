# Strategy, design criteria and success

Use this when deciding which experience to create, what a requested feature should achieve, or how to assess competing designs. A strategy connects purpose, use circumstances, constraints and criteria; a feature list alone does not. [X11, pp. 6–14, 44–52](../books/X11.md)

## DO

- Reuse the product's history, current research and known constraints before asking for more context.
- Turn “intuitive” into an observable task criterion, such as “a returning user can locate and retry the failed message without rewriting it.” This is a design-pro example, not a measured finding.
- Connect each necessary feature/flow to an intended outcome and a way to verify it.
- Track important side effects: a higher signup rate with worse retention may not meet the goal. [X11, pp. 17–27, 47–52, 82–91](../books/X11.md)

## DON'T

- Do not equate agreement in a persuasive presentation with validated demand or usability.
- Do not hide uncertainties to discourage criticism, or lower release criteria to whatever has already been implemented.
- Do not use a generic revenue, click or time-spent target for every product. [X11, pp. 56–65, 82–91](../books/X11.md); [X12, pp. 83–89](../books/X12.md#trace-requirements-through-behavior-and-verification)

## Guidelines and example

Keep a short working brief; create a canvas, persona or PRD only when it resolves a real decision. Mark evidence, assumptions and unresolved questions separately. Set verification appropriate to the claim: browser operation can establish that a retry works locally; it cannot establish that intended users find it. [X12, pp. 7–21, 25–36, 44–48](../books/X12.md)

For a game page: intended outcome = understand the game and release information; design criterion = identity, gameplay, supported platform and next action are findable at narrow/wide layouts; verification = inspect real content, operate links/controls and check focus/reflow. Whether visitors understand or choose the game requires user evidence. This is design-pro synthesis for both modes.

## Separate architecture choice from promised UX outcomes

Before replacing a frontend or backend, identify the actual experience constraint, existing reusable capabilities and who owns delivery, integrations and maintenance. API separation may change dependencies; it does not itself prove better conversion, accessibility or permanent freedom from migrations. A vendor diagram and testimonials are proposals to evaluate, not comparative evidence. [W04, PDF pp. 4–14](../books/W04.md)

## Discover before prescribing a technique

For a public page, establish the audience, actual offer, important problem/interest, truthful promise and desired next action before choosing a visual pattern or acquisition tactic. A channel, theme or reusable component still needs assessment in that context; neither a template nor custom work guarantees quality or outcomes. Preserve a collaborative brief and ask only consequential missing questions, even though the source proposes a much longer interview. These are design-pro adaptations of [W10, *Web Design Is Dead*, exact filename and PDF pp. 30–42](../books/W10.md#discovery-questions-without-interview-quotas), not a mandate to turn every app task into a marketing engagement. Revisit assumptions using actual evidence; a local prototype check cannot prove audience demand or post-launch revenue ([W10, PDF pp. 42–45](../books/W10.md#delivery-learning-and-operation)).
