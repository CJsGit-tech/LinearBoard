# Responsive layouts and task continuity

Consistency keeps meaning and task access recognizable across surfaces. Continuity keeps one task going as the person switches surfaces. Both allow different layouts. [X14, pp. 34–42, 64–69](../books/X14.md#consistent-continuous-and-complementary-experiences)

## DO

[X14, pp. 38–64](../books/X14.md); the state-transfer checks are *(synthesis)*.

- Inventory actual content and rank the main task before deciding columns or breakpoints.
- Adapt grouping, navigation, images and density when content no longer fits, keeping essential actions and information reachable.
- Preserve drafts, position and task state when the product promises continuity; say so when transfer or sync is unavailable.
- Test intermediate widths, long content, both orientations and the available inputs.

## DON'T

- Do not assume phone means hurried, tablet means home or desktop means mouse only.
- Do not hide a critical task, shrink required text or require hover to make the small layout fit.
- Do not copy a historical breakpoint list or require twelve columns; set breakpoints where this content fails. [X14, pp. 35–52](../books/X14.md)

## Guidelines and example

Choose breakpoints from content/interaction failures and existing component contracts. Start with the task that carries the most uncertainty; mobile-first is one way to clarify priorities. Let a necessary two-dimensional table scroll within its own region under the [current reflow criteria](../current-accessibility.md#reflow).

For chat, a wide layout can show conversation navigation beside the thread and a narrow one can use a separate navigation surface; returning restores the intended conversation and draft. Report browser resizing as layout evidence only. For a cross-device journey, test one task spanning devices, which differs from comparing devices separately. [X17, pp. 17–18](../books/X17.md#across-devices-and-with-people)

## Choosing an adaptation

Compare mostly-fluid, column-drop, layout-shift, small-tweak and off-canvas arrangements against the actual content and task. Check inner columns for cramping even when the outer canvas is spacious. Keep destinations recognizable and task access intact while changing their presentation. [W02, PDF pp. 23–43, 48–65](../books/W02.md#adapt-layout-and-navigation-meaningfully)

Exercise long and short content, input methods, zoom and keyboard-height changes. Keep zoom uncapped and take sizes from current criteria. [W02, PDF pp. 25–27, 45–47, 112–126](../books/W02.md); [current resize-text explanation](../current-accessibility.md#resize-text)

## Describe the promised continuity precisely

Complementary devices act together; a locally saved draft is local. When transfer is promised, define saved state, ownership, interruption/conflict behavior and return paths, then exercise them. [W06, PDF pp. 45–51](../books/W06.md#native-continuous-and-complementary-journeys)
