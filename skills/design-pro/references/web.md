# Web Apps mode

Use this for browser applications and adapt it for public-facing pages. Select the interaction model for the task rather than applying a generic dashboard skin.

## Responsive structure

Reflow content deliberately; do not make every breakpoint a smaller copy of the same composition. Keep actionable units coherent, but do not assume everything belongs in a card. [M03, pp. 8–10, 21–27](books/M03.md); [T01, pp. 25–26](books/T01.md)

For an existing app, reuse its layout and component contracts. Document spacing, type roles, color roles and intentional pattern variants alongside implementation examples. A sample twelve-column grid in a style guide is not a universal requirement. [S02, pp. 27–41](books/S02.md#practical-guidance)

Check [current reflow criteria](current-accessibility.md#reflow), including exceptions where two-dimensional presentation carries meaning. A table's necessary horizontal scroll should not force the whole page to scroll in both directions.

Use [responsive structure and continuity](concepts/responsive-and-continuity.md) for breakpoint and cross-device questions. Test real content and task access; layout adaptation does not establish synchronization, performance or device-specific usability. [X14, pp. 34–69](books/X14.md)

## Public-facing composition

A distinct title, imagery and clear primary action may serve a release page. Keep supporting release/platform information readable and compatible with the artwork. Evaluate text on images at all relevant crops; do not obscure the important subject. [T02, pp. 11–24](books/T02.md#practical-techniques)

**Design-pro application:** make the visitor's next action specific and honest. Do not manufacture a release date, platform availability, review score or customer quote. A fictional demo must identify sample content without implying a real release.

For a narrative public page, load [visual storytelling](concepts/visual-storytelling.md). Interaction can support explanation, but the main task must remain visible without discovering easter eggs or completing a forced animated sequence. [U01, pp. 6–7, 21–26](books/U01.md)

## Forms and feedback

Load [forms and errors](concepts/forms-and-errors.md) for input-heavy flows. Readable labels and textual errors need usable programmatic relationships as well; visual styling alone is insufficient. Preserve entered values when correction is possible. The latter is design-pro recovery guidance, not a claim that one WCAG criterion prescribes all form behavior.

## Complex applications

For [information architecture and flows](concepts/information-architecture.md), connect content categories with actual tasks and compare sensible menu/filter patterns before polishing individual controls. A short outline can expose a missing choice or recovery step. [X10, pp. 29–31, 60–71](books/X10.md)

Avoid hover-only access to required content or actions; the full detail route may work better on touch than a desktop quick-view overlay. Preserve equivalent task access across the available inputs. [M08, p. 13](books/M08.md#adapt-interaction-not-just-width)

**Design-pro implementation considerations:** choose navigation for the user's main tasks and the existing app structure; use a table for meaningful cross-record comparison and a list/card where independent summaries fit better. Model selection, editing, saving, pending requests and failed operations explicitly. Avoid hiding essential actions behind hover alone. Test keyboard traversal, focus entry/return and visible state changes in the actual implementation. These choices require task-specific evidence; they are not automatically validated by a style-guide screenshot.

## Verification focus

Use [keyboard functionality](current-accessibility.md#keyboard-operation), [meaningful sequence](current-accessibility.md#meaningful-sequence), [focus order](current-accessibility.md#focus-order) and [bypass routes](current-accessibility.md#bypassing-repeated-blocks) according to their conditions. Custom shortcuts, DOM reordering and visual alignment do not substitute for testing the actual interaction.

Assess the delivery constraints before proposing a PWA, separate codebase or new architecture. Existing content/data sources, release ownership, integration quality and maintenance cost affect the feasible experience. Enterprise vendor comparisons do not prove that one architecture guarantees speed or revenue. [M09, pp. 4–14, 16–17](books/M09.md#transferable-decisions)

Use realistic long labels, empty/populated data and error states. Exercise keyboard and pointer flows, resizing, text enlargement, loading and recovery. Inspect focus and overflow rather than relying on static screenshots. Representative-user usability and assistive-technology checks must be reported separately from a browser smoke test. [M02, pp. 21–28](books/M02.md) explains behavioral versus attitudinal evidence; [S02, p. 34](books/S02.md) illustrates why behavior needs more than a still image.
