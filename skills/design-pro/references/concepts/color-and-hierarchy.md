# Color, contrast and visual hierarchy

Define the role of each color and each level of emphasis, so another person knows where to apply it and which combinations work. [S02, pp. 29–32](../books/S02.md#practical-guidance)

## DO

- Reuse existing semantic roles for text, surfaces, actions and state, with purposeful variants. Document combinations and context. [S02, pp. 31–32, 40–41](../books/S02.md)
- Express priority with type roles, alignment, spacing and selective emphasis, with color as one cue among them. [S02, pp. 27–32](../books/S02.md); [current use-of-color guidance](../current-accessibility.md#use-of-color)
- Evaluate actual foreground/background pairs, including over images and across states. Check [text contrast](../current-accessibility.md#contrast) and [non-text control/graphic contrast](../current-accessibility.md#non-text-contrast) separately.
- Check the page's task hierarchy with realistic content at the relevant widths, and reserve the strongest color for the highest priority. [X10, pp. 23–25](../books/X10.md#usability-task-structure-and-recovery)

## DON'T

- Do not explain a form error with a red outline alone; add text and an accessible relationship. [Current error guidance](../current-accessibility.md#input-errors)
- Do not apply 4.5:1 to every border, icon, disabled element and text size; each criterion has its own scope. [Current contrast references](../current-accessibility.md#contrast)
- Do not choose blue or rounded corners to signal safety or trust. [X10, pp. 89–90](../books/X10.md#credibility-and-truthful-evidence)
- Do not add borders or nested surfaces to make every piece stand out; equal emphasis erases priority *(synthesis; see [cards](cards.md))*.

## Guidelines and example

For web, normal text generally needs 4.5:1 and qualifying large text 3:1; visual information needed to identify controls and states generally needs 3:1 against adjacent colors. Apply each criterion's exceptions. [Current text contrast](../current-accessibility.md#contrast); [non-text contrast](../current-accessibility.md#non-text-contrast)

A game page can use expressive display type and a distinctive action color while release details stay readable over the artwork. Chat can reserve emphasis for the active task and use explicit "Reply failed" text with a retry action. Measure the rendered colors *(synthesis)*.

## Palette alternatives

Use monochromatic, analogous, complementary, triadic and tetradic relationships to generate alternatives. Then choose explicit values and functional roles and test the actual combinations for contrast. [U02, pp. 16–32, including the source corrections and primary HSL definition](../books/U02.md#distinguish-palette-relationships-from-usable-contrast)

A flat surface, a selective depth cue, a photograph and an outlined button can coexist when each serves the task. Test the actual control/background/state combinations, and keep essential meaning available without hover or color alone. [U04, pp. 19–30, 43–52](../books/U04.md)

Scale, position, grouping, color and imagery interact; judge their combined effect on the task. A page can have one focal point and still needs each task-relevant priority visible. Check visual salience separately from hit area, reading order and keyboard access. [U07, PDF pp. 8–31](../books/U07.md#layout-patterns-need-the-actual-platform-and-task)

An outlined action carries less visual weight and can lose recognition against imagery; inspect its label, boundary and states on the real background. Take platform rules from current platform guidance. [U14, pp. 13–24](../books/U14.md#tools-and-qualifications)

A monochromatic scheme still needs readable pairs and distinguishable states. Check a tinted image, texture or gradient with its actual text or control foreground at the relevant crops and states. Label sections and variants in text as well as color. [U15, pp. 11–28](../books/U15.md#apply-actual-roles-and-explicit-meaning)
