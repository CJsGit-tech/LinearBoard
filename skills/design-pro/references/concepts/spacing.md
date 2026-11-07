# Spacing and target area

Spacing expresses relationships and supports interaction. Distinguish layout gaps, text rhythm and actual activation area; changing one does not automatically fix the others. This framing is design-pro synthesis from the sources below.

## DO

- Keep related labels, content and actions perceptually together; increase separation at a change in thought. [T01, pp. 12–14](../books/T01.md#decisions-worth-retaining)
- Inspect neighboring controls' usable regions, not just their artwork. [M01, p. 15](../books/M01.md#useful-guidance)
- Distinguish padding that extends a control's interactive region from margin that separates controls. Inspect the rendered implementation rather than assuming CSS spacing alone proves a usable target. [M08, p. 8](../books/M08.md#adapt-interaction-not-just-width)
- Reuse role-based project spacing values and define purposeful exceptions. [S02, pp. 27–28](../books/S02.md#practical-guidance)
- Test density with realistic text and the actual task: action-focused and reading-heavy screens can need different spacing. [T01, pp. 12–13](../books/T01.md)

## DON'T

- Do not enforce one numerical gap across labels, paragraphs, controls and screen sections.
- Do not call an icon's visible dimensions its hit area without checking the control.
- Do not cite a golden ratio or a fixed grid as a universal usability requirement.
- Do not shrink essential text to preserve a fixed-height layout.

These cautions are design-pro synthesis of [T01, pp. 6–7, 12–14, 25–26](../books/T01.md) and [S02, pp. 24–28](../books/S02.md).

## Guidelines and example

Start with the existing system, then evaluate grouping, reading and activation separately. For mobile web, use [current target-size criteria](../current-accessibility.md#target-size) for minimum checks; they do not define a universal gutter or native pt/dp value. For text, distinguish authored leading from [user spacing overrides](../current-accessibility.md#text-spacing).

For a chat composer, an attach icon and send button can look small while their actual controls have larger, non-overlapping activation regions. Keep the text field clearly grouped with send, and separate conversation turns more than lines in the same paragraph. These are applications, not measurements prescribed by the books.

Compare spacing inside a functional group with separation between groups; excessive distance can disconnect a label/action from its content. Neither a 15-point attention budget nor an asserted 20% comprehension gain establishes a numerical spacing rule. These are historical source claims with explicit limits, not prescribed measurements. [U07, PDF pp. 27–31](../books/U07.md#spacing-communicates-grouping-without-fixed-quotas)

## Scale, emphasis and functional limits

Inspect both macro separation between sections and micro rhythm within text/controls. Use enough space to make relationships clear, then add emphasis where it helps the task. “Passive” versus “active” describes the intended role, not fixed numerical categories or a guaranteed gaze route. [U16, pp. 6–17](../books/U16.md#space-communicates-relationships-at-different-scales)

Do not squeeze required terms/status or hide recovery to reduce visual weight. A sparse page does not prove luxury, a dense collection does not prove low quality, and deleting until the interface nearly fails is not a compulsory method. Test useful grouping, reading and interaction with actual content. [U16, pp. 16–28](../books/U16.md#simplification-has-a-functional-boundary)

## Text rhythm and navigation density

Keep a heading close enough to its content to show ownership, and distinguish paragraph boundaries from line rhythm. More space can weaken grouping or increase traversal; it does not force attention. Header/footer spacing may differ with their tasks, while actual text and controls remain usable. Treat 1em/1.5–1.75em recipes as contextual starting points, not identical cross-browser dimensions or accessibility requirements. [U18, PDF pp. 27, 42–57](../books/U18.md#text-and-navigation-limits)

A cramped inner column can coexist with excessive outer space. Diagnose grouping, readable measure and traversal separately before adding or removing gaps. Optional ratios and visual overlays can generate alternatives; neither a spiral nor a designer's eye alone establishes task success. [U19, PDF pp. 27–40, 62–71](../books/U19.md#practice-ratios-and-tools)
