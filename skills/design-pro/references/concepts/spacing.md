# Spacing and target area

Spacing expresses relationships and supports interaction. Evaluate layout gaps, text rhythm and activation area as three separate things *(synthesis)*.

## DO

- Keep related labels, content and actions together; increase separation at a change in thought. [T01, pp. 12–14](../books/T01.md#decisions-worth-retaining)
- Inspect neighboring controls' usable regions as well as their artwork. [M01, p. 15](../books/M01.md#useful-guidance)
- Use padding to extend a control's interactive region and margin to separate controls, then inspect the rendered target. [M08, p. 8](../books/M08.md#adapt-interaction-not-just-width)
- Reuse role-based project spacing values and define purposeful exceptions. [S02, pp. 27–28](../books/S02.md#practical-guidance)
- Test density with realistic text and the actual task; action-focused and reading-heavy screens need different spacing. [T01, pp. 12–13](../books/T01.md)

## DON'T

*(synthesis from [T01, pp. 6–7, 12–14, 25–26](../books/T01.md) and [S02, pp. 24–28](../books/S02.md))*

- Do not enforce one numerical gap across labels, paragraphs, controls and sections; each relationship needs its own value.
- Do not take an icon's visible size as its hit area; measure the control.
- Do not justify a layout by a golden ratio or fixed grid; justify it by the task.
- Do not shrink essential text to keep a fixed-height layout; let the layout grow.

## Guidelines and example

Start with the existing system, then evaluate grouping, reading and activation separately. For mobile web, use [current target-size criteria](../current-accessibility.md#target-size) as the minimum check; get native pt/dp values from the platform. For text, design authored leading and separately test [user spacing overrides](../current-accessibility.md#text-spacing).

In a chat composer, give the attach icon and send button activation regions larger than their artwork, without overlap. Group the text field with send, and separate conversation turns more than lines within a paragraph *(synthesis)*.

Compare spacing inside a functional group with separation between groups; too much distance disconnects a label or action from its content. [U07, PDF pp. 27–31](../books/U07.md#spacing-communicates-grouping-without-fixed-quotas)

## Scale, emphasis and functional limits

Inspect macro separation between sections and micro rhythm within text and controls. Add space until relationships are clear, then add emphasis where it helps the task. [U16, pp. 6–17](../books/U16.md#space-communicates-relationships-at-different-scales)

Keep required terms, status and recovery visible when reducing visual weight. Judge density by grouping, reading and interaction with actual content. [U16, pp. 16–28](../books/U16.md#simplification-has-a-functional-boundary)

## Text rhythm and navigation density

Keep a heading close enough to its content to show ownership, and make paragraph boundaries larger than line rhythm. Space header and footer for their own tasks. Use 1em/1.5–1.75em recipes as starting points and check the rendered result. [U18, PDF pp. 27, 42–57](../books/U18.md#text-and-navigation-limits)

A cramped inner column can sit inside excessive outer space. Diagnose grouping, readable measure and traversal separately before changing gaps. Ratios and visual overlays are ways to generate alternatives to test. [U19, PDF pp. 27–40, 62–71](../books/U19.md#practice-ratios-and-tools)
