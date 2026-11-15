# Web Apps mode

Use this for browser applications and adapt it for public-facing pages. Select the interaction model for the task before applying any dashboard pattern.

## Responsive structure

Reflow content deliberately: re-rank and regroup at each breakpoint. Keep actionable units coherent, and use a card only where the unit calls for one. [M03, pp. 8–10, 21–27](books/M03.md); [T01, pp. 25–26](books/T01.md)

For an existing app, reuse its layout and component contracts. Document spacing, type roles, color roles and intentional pattern variants beside implementation examples. Take the grid from the product, not from a style-guide sample. [S02, pp. 27–41](books/S02.md#practical-guidance)

Check [current reflow criteria](current-accessibility.md#reflow) and their exception for two-dimensional content. Let a table scroll horizontally inside its own region so the page scrolls on one axis.

Use [responsive structure and continuity](concepts/responsive-and-continuity.md) for breakpoint and cross-device questions. Test with real content and check task access at each width. [X14, pp. 34–69](books/X14.md)

## Public-facing composition

A release page can lead with a distinct title, imagery and one clear primary action. Keep release and platform information readable against the artwork. Check text on images at every relevant crop and keep the important subject visible. [T02, pp. 11–24](books/T02.md#practical-techniques)

Make the visitor's next action specific and honest. Use only real release dates, platform availability, review scores and customer quotes; label sample content in a fictional demo as sample *(synthesis)*.

For a narrative public page, load [visual storytelling](concepts/visual-storytelling.md). Keep the main task visible without easter eggs or a forced animated sequence. [U01, pp. 6–7, 21–26](books/U01.md)

## Forms and feedback

Load [forms and errors](concepts/forms-and-errors.md) for input-heavy flows. Give labels and textual errors a programmatic relationship to their controls as well as visual styling. Preserve entered values when correction is possible *(synthesis)*.

## Complex applications

For [information architecture and flows](concepts/information-architecture.md), connect content categories to actual tasks and compare menu/filter patterns before polishing individual controls. Write a short outline of the flow to expose a missing choice or recovery step. [X10, pp. 29–31, 60–71](books/X10.md)

Give every required action and piece of content a route that works without hover. On touch, a full detail route often serves better than a desktop quick-view overlay. Keep the task equivalent across the available inputs. [M08, p. 13](books/M08.md#adapt-interaction-not-just-width)

**Implementation** *(synthesis)*:

- Choose navigation from the user's main tasks and the existing app structure.
- Use a table for cross-record comparison and a list or card for independent summaries.
- Model selection, editing, saving, pending requests and failed operations explicitly.
- Test keyboard traversal, focus entry and return, and visible state changes in the actual implementation.

## Verification focus

Apply [keyboard functionality](current-accessibility.md#keyboard-operation), [meaningful sequence](current-accessibility.md#meaningful-sequence), [focus order](current-accessibility.md#focus-order) and [bypass routes](current-accessibility.md#bypassing-repeated-blocks) by their conditions, and test the actual interaction for each.

Before proposing a PWA, separate codebase or new architecture, assess delivery constraints: existing content and data sources, release ownership, integration quality and maintenance cost. [M09, pp. 4–14, 16–17](books/M09.md#transferable-decisions)

Exercise the result in a browser:

- realistic long labels, empty and populated data, and error states;
- keyboard and pointer flows, with focus and overflow inspected at each step;
- resizing, text enlargement, loading and recovery.

Report this as a browser check. Report representative-user usability and assistive-technology checks separately, and only when they were run. [M02, pp. 21–28](books/M02.md); [S02, p. 34](books/S02.md)
