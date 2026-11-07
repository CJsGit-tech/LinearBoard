# Style guides and reusable patterns

Choose the reference for the decision: a mood board explores atmosphere, a style tile expresses concrete visual choices without layout, a brand guide defines identity, and a front-end guide connects decisions with implementation. [S01, pp. 10–23](../books/S01.md)

## DO

- Inspect existing components, tokens and legitimate variants before creating another.
- Include usage conditions and rationale as well as appearance.
- Put relevant implementation beside examples and use consistent terminology.
- Keep the guide proportional and findable.

Sources: [S01, pp. 8–9, 22–23](../books/S01.md); [S02, pp. 27–41, 46–48](../books/S02.md).

## DON'T

- Do not treat a mood board as an interaction specification.
- Do not normalize different patterns that serve different tasks without examining their purpose.
- Do not copy another brand's values or a sample twelve-column grid as universal defaults.
- Do not expand documentation merely to match a large company's manual.

These are design-pro applications of the sources above.

## Guidelines and example

For a new demo, record the necessary type roles, color roles, spacing relationships and control states. For an existing product, extend its actual reference and component APIs instead of establishing a competing system. A colorful game page and a quiet chat interface can share decision principles without an identical visual theme.

A pattern is the underlying solution; a component is an implementation. Record the problem, use conditions, behavior/states and relevant variants, not just screenshots. Reusable shared elements can reduce drift, but inspect intentional differences before propagating a change. [U05, pp. 21–28, 40–58](../books/U05.md)

Components also have time-dependent behavior: entering a form, submitting, receiving a result and recovering from failure. Reuse those state contracts, not only a rectangle's styling. Atomic Design is an optional organizing method; it does not require five code layers or indiscriminate copy/paste. [W05, PDF pp. 18–21](../books/W05.md#design-the-useful-service-and-its-changing-states)

For silhouette, corner/boundary/depth roles and visual interaction states, load [component anatomy](component-anatomy.md). Keep project-specific tokens outside the reusable skill.
