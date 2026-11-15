# Strategy, design criteria and success

Use this when deciding which experience to create, what a requested feature should achieve, or how to assess competing designs. A strategy connects purpose, circumstances of use, constraints and criteria. [X11, pp. 6–14, 44–52](../books/X11.md)

## DO

[X11, pp. 17–27, 47–52, 82–91](../books/X11.md)

- Reuse the product's history, current research and known constraints before asking for more context.
- Turn "intuitive" into an observable task criterion, such as "a returning user can locate and retry the failed message without rewriting it" *(synthesis)*.
- Connect each necessary feature or flow to an intended outcome and a way to verify it.
- Track important side effects, such as a higher signup rate with worse retention.

## DON'T

[X11, pp. 56–65, 82–91](../books/X11.md); [X12, pp. 83–89](../books/X12.md#trace-requirements-through-behavior-and-verification)

- Do not count agreement in a presentation as validated demand or usability.
- Do not hide uncertainties to avoid criticism, or lower release criteria to match what is already built.
- Do not reuse a generic revenue, click or time-spent target; derive the target from this product's outcome.

## Guidelines and example

Keep a short working brief, and create a canvas, persona or PRD only to resolve a real decision. Mark evidence, assumptions and unresolved questions separately. Match verification to the claim: a browser check establishes that retry works locally; whether intended users find it needs user evidence. [X12, pp. 7–21, 25–36, 44–48](../books/X12.md)

For a game page *(synthesis)*:

- **Intended outcome:** understand the game and its release information.
- **Design criterion:** identity, gameplay, supported platform and next action are findable at narrow and wide layouts.
- **Verification:** inspect real content, operate links and controls, check focus and reflow.

## Separate architecture choice from promised UX outcomes

Before replacing a frontend or backend, identify the actual experience constraint, the existing reusable capabilities and who owns delivery, integrations and maintenance. Evaluate a vendor diagram or testimonial as a proposal. [W04, PDF pp. 4–14](../books/W04.md)

## Discover before prescribing a technique

For a public page, establish the audience, the actual offer, the problem or interest it addresses, a truthful promise and the desired next action before choosing a visual pattern or acquisition tactic. Assess any channel, theme or reusable component in that context. Keep the brief collaborative and ask only consequential missing questions *(synthesis from [W10, *Web Design Is Dead*, exact filename and PDF pp. 30–42](../books/W10.md#discovery-questions-without-interview-quotas))*. Revisit assumptions with actual evidence after launch. [W10, PDF pp. 42–45](../books/W10.md#delivery-learning-and-operation)
