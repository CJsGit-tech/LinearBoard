# Component shape, surface and states

Search terms: component styling, component anatomy, shape, radius, rounded corners, border, shadow, elevation, button, input, segmented control, 元件造型, 圓角, 輪廓, 邊框, 陰影, 層次.

A component's silhouette and surface should communicate its role and state. Appearance and behavior are designed together. These decision rules are design-pro synthesis, supported by the reviewed sources below; the books do not prescribe one universal radius or shadow recipe.

Apply the [user's default visual preference](../shared.md#group-meaning-before-drawing-containers): establish hierarchy through whitespace, alignment and typography, with an open composition across both modes. Enclosing borders, cards and pills are optional tools for a clear purpose. This preference is distinct from the source-backed guidance below.

## DO

- Start with anatomy: label/content, optional icon and surface/boundary, focus indicator and relevant status. Make the interactive region match the intended control rather than its artwork alone. [M01, *Flat Mobile Design Evolved.pdf*, PDF pp. 14–16](../books/M01.md#useful-guidance).
- Use a small role-based family of shapes: for example, a compact action, a grouped segmented selector and a larger dialog surface. Select radii by scale, content and existing brand; record actual project values. A circular icon button and rounded multiline composer can coexist purposefully. [S02, *The Critical Components Of Web UI Style Guides.pdf*, pp. 27–41, 46–48](../books/S02.md#practical-guidance).
- Use selective boundary, tonal change or depth to clarify an actionable or raised surface. Check the actual background and all relevant states; removing every depth cue is not a goal. [M01, pp. 6–9, 14–16](../books/M01.md); [U14, *Web UI Trends Present & Future - The Evolution of Flat Design.pdf*, pp. 6–14, 23–24](../books/U14.md#tools-and-qualifications).
- Define default, hover where supported, focus, pressed, disabled and relevant pending/error/completed states. State changes must preserve understandable meaning and a stable activation area. Use current platform behavior and [accessibility references](../current-accessibility.md) for actual requirements.
- Preserve shape relationships when resizing or enlarging text. A pill needs enough vertical/horizontal room; a fixed-height capsule must not clip a translated or enlarged label. This is implementation guidance, not a fixed book measurement.

## DON'T

- Do not round every element identically merely for consistency, or erase intentional primary/destructive/secondary variants. [S02, pp. 40–41](../books/S02.md).
- Do not infer trust or friendliness solely from rounded corners, or treat square versus round as a guarantee of an audience's feelings. [color/hierarchy qualifications](color-and-hierarchy.md).
- Do not make an outlined button disappear against imagery to preserve the illustration. The source explicitly praises an outlined treatment while admitting it may not look actionable. [U14, p. 13](../books/U14.md#tools-and-qualifications).
- Do not stack decorative borders, inner panels, glows and shadows around every nested part. Use the least surface treatment that communicates the relationship. [cards/grouping](cards.md).
- Do not import repeated card wrappers, icon circles, pills or inset edges merely because a component library's example includes them. Assess the whole composition and remove redundant framing while retaining meaningful interaction cues.
- Do not add perpetual decorative motion or hide the working control until hover. An animated rim is optional; a stable label, reachable action and visible focus remain necessary. [pattern selection](pattern-selection.md).

## Rules of thumb and examples

**Surface follows role.** If two components look equally prominent, check whether their priority and consequences really are equal. A high-emphasis game CTA can use one solid fill; secondary navigation can remain plain text. An enclosing outline, inset edge or nested arrow capsule needs a reason beyond decoration.

**One group, one useful relationship.** A chat composer can group text and send through alignment and one quiet tonal surface. Do not automatically add a persistent outline or separately frame its label, textarea, send group and outer panel. Keep the field discoverable and its active focus visible.

**Shape is a family, not one number.** Choose a few documented radius/border/elevation roles and allow justified exceptions. Specific CSS values in a project are implementation choices, not native pt/dp requirements or universal book prescriptions.

**A completed animation is not a completed operation.** Tie pending, failure and success visuals to actual state. For a simulated prototype, identify the simulation. See [content states](content-states.md) and [prototyping](prototyping.md).

For external component libraries, inspect current source/access/dependencies and compare the mechanism with the existing stack. A React demo can inspire an original HTML/CSS implementation without requiring a framework migration; identify that adaptation rather than claiming a vendor component was installed. Historical books do not establish current library availability or licensing.
