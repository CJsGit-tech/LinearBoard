# Responsive layouts and task continuity

Consistency preserves recognizable meaning and task access across surfaces; continuity preserves a task as the person switches surfaces. Neither requires identical layouts. [X14, pp. 34–42, 64–69](../books/X14.md#consistent-continuous-and-complementary-experiences)

## DO

- Inventory actual content and prioritize the main task before deciding columns or breakpoints.
- Adapt grouping, navigation, images and density when content no longer fits. Keep essential actions and information reachable.
- Preserve drafts, meaningful position and task state when the product promises continuity; explain unavailable transfer or synchronization.
- Test intermediate widths, long content, both orientation dimensions and available inputs. [X14, pp. 38–64](../books/X14.md); state-transfer checks are design-pro applications.

## DON'T

- Do not assume phone means hurried, tablet means home, or desktop means mouse only.
- Do not hide a critical task solely to simplify the small layout, shrink required text to fit, or require hover for access.
- Do not copy a historical six-breakpoint list, require twelve columns, or claim one architecture guarantees speed/search rank. [X14, pp. 35–52](../books/X14.md)

## Guidelines and example

Choose breakpoints from content/interaction failures and existing component contracts. Mobile-first can clarify priorities, but start with the task carrying consequential uncertainty. Responsive layout and server-side device adaptation are different implementation decisions. A necessary two-dimensional table can retain its structure without forcing the entire page into two-axis scrolling; apply [current reflow criteria](../current-accessibility.md#reflow) and their exceptions.

For chat, a wide layout may show conversation navigation beside the thread; a narrow layout may use a separate navigation surface. Returning must preserve the intended conversation and draft. Browser resizing verifies layout adaptation, not cross-device synchronization or real-device keyboard behavior. For an actual cross-device journey, distinguish separate-device comparison from one task spanning devices. [X17, pp. 17–18](../books/X17.md#across-devices-and-with-people)

## Choosing an adaptation

Compare mostly-fluid, column-drop, layout-shift, small-tweak and off-canvas arrangements against the actual content/task. These are candidate patterns, not a fixed taxonomy or breakpoint count. A narrow inner column can be cramped despite a spacious outer canvas. Preserve recognizable destinations and necessary task access while changing their presentation. [W02, PDF pp. 23–43, 48–65](../books/W02.md#adapt-layout-and-navigation-meaningfully)

Exercise long/short content, input methods, zoom and keyboard-height changes. Do not infer physical-device behavior from a resized desktop window, or use a historical 200% zoom cap, 23-point gap, universal corner placement or minimum 30rem layout. [W02, PDF pp. 25–27, 45–47, 112–126](../books/W02.md); [current resize-text explanation](../current-accessibility.md#resize-text).

## Describe the promised continuity precisely

Consistency preserves familiar meaning; continuity preserves one task across contexts; complementary devices act together. A local saved draft is not cross-device synchronization. When transfer is promised, define saved state, ownership, interruption/conflict behavior and return paths, then exercise them. Historical Gmail/controller screenshots illustrate the idea without verifying runtime transfer. [W06, PDF pp. 45–51](../books/W06.md#native-continuous-and-complementary-journeys)
