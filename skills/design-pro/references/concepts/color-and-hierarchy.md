# Color, contrast and visual hierarchy

Define the role of each color and level of emphasis. A palette is useful when another person knows where to apply it and which combinations work, rather than having only named swatches. [S02, pp. 29–32](../books/S02.md#practical-guidance)

## DO

- Reuse existing semantic roles for text, surfaces, actions and state, with purposeful variants. Document combinations and context. [S02, pp. 31–32, 40–41](../books/S02.md)
- Use type roles, alignment, spacing and selective emphasis to express priority; do not make color carry the whole distinction. [S02, pp. 27–32](../books/S02.md); [current use-of-color guidance](../current-accessibility.md#use-of-color)
- Evaluate actual foreground/background pairs, including images and state changes. Distinguish [text contrast](../current-accessibility.md#contrast) from [non-text control/graphic contrast](../current-accessibility.md#non-text-contrast).
- Check the page's task hierarchy with realistic content at relevant widths, rather than applying a single high-saturation color everywhere. The saturation suggestion is contextual, not a guarantee. [X10, pp. 23–25](../books/X10.md#usability-task-structure-and-recovery)

## DON'T

- Do not use a red outline alone to explain a form error; provide understandable text and an accessible relationship. [Current error guidance](../current-accessibility.md#input-errors)
- Do not apply one 4.5:1 rule indiscriminately to every border, icon, disabled element and text size. Criteria have distinct scopes and exceptions. [Current contrast references](../current-accessibility.md#contrast)
- Do not infer safety, trust or audience preference from a blue palette or rounded corners. These are source interpretations, not guaranteed effects. [X10, pp. 89–90](../books/X10.md#credibility-and-truthful-evidence)
- Do not add borders or nested surfaces merely to make every piece stand out; excessive equal emphasis erases priority. This is design-pro grouping judgment supported by [cards guidance](cards.md).

## Guidelines and example

For web, normal text generally needs 4.5:1 and qualifying large text 3:1; required non-text visual identification generally uses 3:1 against adjacent colors, with each criterion's exceptions. These are thresholds for specified purposes, not a complete design or conformance test. [Current text contrast](../current-accessibility.md#contrast); [non-text contrast](../current-accessibility.md#non-text-contrast)

A game page can use expressive display type and a distinctive action color while keeping release details readable over the artwork. Chat can reserve emphasis for the active task and use explicit “Reply failed” text with a retry action. These are design-pro examples; assess their actual rendered colors and behavior.

## Palette alternatives

Monochromatic, analogous, complementary, triadic and tetradic relationships can generate alternatives; they do not guarantee harmony, a particular emotion or usable contrast. Choose explicit values and functional roles, then test actual combinations. Same-hue light/dark variants are not technically complementary merely because they look good together. The source also mischaracterizes any neutral palette plus one accent as split-complementary; do not repeat that shortcut. [U02, pp. 16–32, including the source corrections and primary HSL definition](../books/U02.md#distinguish-palette-relationships-from-usable-contrast)

A flat surface, selective depth cue, photograph or outlined button can coexist when each serves the task. Neither a flat aesthetic nor a vivid accent guarantees discoverability, readability or speed. Test the actual control/background/state combinations; essential meaning must survive without hover or color alone. [U04, pp. 19–30, 43–52](../books/U04.md)

Scale, position, grouping, color and imagery interact. Judge their combined effect on the task rather than claiming one accent controls every viewer's eye. F/Z diagrams are possible layout hypotheses, not mandatory routes; a single focal point can be useful for a focused page but does not remove the need for multiple task-relevant priorities. Keep visual salience separate from usable hit area, meaningful reading order and keyboard access. [U07, PDF pp. 8–31](../books/U07.md#layout-patterns-need-the-actual-platform-and-task)

Do not quantify a hybrid as two-thirds flat and one-third skeuomorphic or infer that a specific texture ratio creates hierarchy. An outlined action can reduce visual weight while losing recognition against imagery; inspect actual labels, boundaries and states. Flat, minimal and Material are distinct ideas, and historical vendor examples do not establish today's platform rules. [U14, pp. 13–24](../books/U14.md#tools-and-qualifications)

A monochromatic scheme still needs readable pairs and distinguishable states. A tinted image, texture or gradient must be checked with its actual text/control foreground at relevant crops and states; hue difference alone does not establish the required contrast. Preserve section/variant labels instead of relying on rainbow navigation or unlabeled swatches. [U15, pp. 11–28](../books/U15.md#apply-actual-roles-and-explicit-meaning)
