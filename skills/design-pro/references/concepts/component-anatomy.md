# Component shape, surface and states

Search terms: component styling, component anatomy, shape, radius, rounded corners, border, shadow, elevation, button, input, segmented control, 元件造型, 圓角, 輪廓, 邊框, 陰影, 層次.

A component's silhouette and surface communicate its role and state; design appearance and behavior together. The decision rules here are *(synthesis)* built on the cited sources.

Apply the [user's default visual preference](../shared.md#group-meaning-before-drawing-containers): hierarchy through whitespace, alignment and typography, with an open composition in both modes. Use enclosing borders, cards and pills only for a clear purpose.

## DO

- Start with anatomy: label/content, optional icon, surface/boundary, focus indicator and status. Make the interactive region match the intended control. [M01, *Flat Mobile Design Evolved.pdf*, PDF pp. 14–16](../books/M01.md#useful-guidance).
- Use a small role-based family of shapes, such as a compact action, a grouped segmented selector and a larger dialog surface. Select radii by scale, content and existing brand, and record the project's values. [S02, *The Critical Components Of Web UI Style Guides.pdf*, pp. 27–41, 46–48](../books/S02.md#practical-guidance).
- Use a boundary, tonal change or depth to mark an actionable or raised surface. Check it against the actual background in every state. [M01, pp. 6–9, 14–16](../books/M01.md); [U14, *Web UI Trends Present & Future - The Evolution of Flat Design.pdf*, pp. 6–14, 23–24](../books/U14.md#tools-and-qualifications).
- Define default, hover where supported, focus, pressed, disabled and any pending/error/completed states. Keep meaning understandable and the activation area stable across them. Take requirements from current platform behavior and [accessibility references](../current-accessibility.md).
- Keep shape relationships when text is resized or translated: give a pill room to grow in both directions so a longer label is never clipped.

## DON'T

- Do not round every element identically or erase primary/destructive/secondary variants; keep role differences visible. [S02, pp. 40–41](../books/S02.md).
- Do not let an outlined button disappear against imagery; give it a fill or contrast that reads as actionable. [U14, p. 13](../books/U14.md#tools-and-qualifications).
- Do not stack borders, inner panels, glows and shadows around nested parts; use the least surface treatment that shows the relationship. [cards/grouping](cards.md).
- Do not import card wrappers, icon circles, pills or inset edges because a component library's example has them; keep only the cues the interaction needs.
- Do not hide the working control until hover or add perpetual decorative motion; keep a stable label, reachable action and visible focus. [pattern selection](pattern-selection.md).

## Rules of thumb and examples

**Surface follows role.** If two components look equally prominent, check that their priority and consequences are equal. A high-emphasis CTA can take one solid fill while secondary navigation stays plain text.

**One group, one useful relationship.** A chat composer can group text and send through alignment and one quiet tonal surface, with the field discoverable and focus visible. Leave its label, textarea, send group and outer panel unframed.

**Shape is a family, not one number.** Choose a few documented radius/border/elevation roles and allow justified exceptions. Project CSS values are implementation choices; native pt/dp values come from the platform.

**A completed animation is not a completed operation.** Tie pending, failure and success visuals to actual state, and label a simulated prototype. See [content states](content-states.md) and [prototyping](prototyping.md).

For external component libraries, inspect current source, access and dependencies and compare the mechanism with the existing stack. Adapt the idea into the existing stack, and describe it as an adaptation.
