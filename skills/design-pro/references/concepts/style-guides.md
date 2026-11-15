# Style guides and reusable patterns

Choose the reference for the decision: a mood board explores atmosphere, a style tile fixes concrete visual choices without layout, a brand guide defines identity, and a front-end guide connects decisions with implementation. [S01, pp. 10–23](../books/S01.md)

## DO

[S01, pp. 8–9, 22–23](../books/S01.md); [S02, pp. 27–41, 46–48](../books/S02.md)

- Inspect existing components, tokens and legitimate variants before creating another.
- Record usage conditions and rationale beside appearance.
- Put implementation beside examples and use consistent terminology.
- Keep the guide proportional to the product and easy to find.

## DON'T

*(synthesis from the sources above)*

- Do not use a mood board as an interaction specification; write the states and transitions.
- Do not merge patterns that serve different tasks; check each one's purpose first.
- Do not copy another brand's values or a sample twelve-column grid; derive defaults from this product.
- Do not grow documentation to match a large company's manual.

## Guidelines and example

For a new demo, record the type roles, color roles, spacing relationships and control states it needs. For an existing product, extend its reference and component APIs. A colorful game page and a quiet chat interface can share decision principles with different themes.

A pattern is the underlying solution; a component is one implementation. Record the problem, use conditions, behavior/states and variants beside screenshots. Before propagating a change across shared elements, check for intentional differences. [U05, pp. 21–28, 40–58](../books/U05.md)

Components behave over time: entering a form, submitting, receiving a result, recovering from failure. Reuse those state contracts along with the styling. Atomic Design is one optional way to organize them. [W05, PDF pp. 18–21](../books/W05.md#design-the-useful-service-and-its-changing-states)

For silhouette, corner/boundary/depth roles and visual interaction states, load [component anatomy](component-anatomy.md). Keep project-specific tokens outside the reusable skill.
