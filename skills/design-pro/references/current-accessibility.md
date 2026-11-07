# Current accessibility sources

Checked on **2026-10-25** against W3C/WAI primary documentation. These web criteria do not specify native iOS/Android dimensions. The Understanding pages explain WCAG; the linked success criteria are normative. This is a focused reference, not a full conformance checklist or certification.

## Non-text content

Verified 2026-10-25 against W3C's [Understanding SC 1.1.1](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html). Non-text information needs an equivalent-purpose text alternative, subject to the criterion's cases. Non-text controls need a name describing their purpose; purely decorative material should be ignorable by assistive technology. Complex diagrams may need more than a short label, and time-based media has additional requirements. A visual, mascot or static poster does not alone establish accessibility or equivalent information.

## Audio control

Verified 2026-10-25 against W3C's [Understanding SC 1.4.2](https://www.w3.org/WAI/WCAG22/Understanding/audio-control.html). Automatically playing Web audio lasting more than three seconds requires pause/stop or a volume control independent of system volume. The explanatory guidance recommends starting sound through a user's intentional action. This is distinct from controlling decorative motion and is not a claim that a muted video meets all media criteria.

## Target size

WCAG 2.2 SC 2.5.8 (AA) generally uses a 24×24 CSS-pixel minimum target, with spacing, equivalent-control, inline, user-agent and essential exceptions. The spacing exception uses centered 24-pixel circles, not a universal 24-pixel gap. This is a minimum criterion, not an ideal mobile control size or native-platform rule.

[W3C: Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

## Input errors

SC 3.3.1 (A) requires a detected input error to identify the affected item and describe the problem in text. The criterion does not mandate one display location. Recovery suggestions and programmatic association have related, distinct requirements.

[W3C: Error Identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html)

## Labels

SC 3.3.2 (A) requires labels or instructions when input is expected, including optional inputs. Programmatic names and relationships are covered separately; an invisible accessible name alone does not resolve every visible-label need.

[W3C: Labels or Instructions](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html)

## Contrast

SC 1.4.3 (AA) sets text contrast at 4.5:1, or 3:1 for qualifying large text, with specified incidental/logotype exceptions. Large text is defined as 18 pt or 14 pt bold (CSS points); do not treat every heading as large. Measure the actual pair without rounding a failing result upward.

[W3C: Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

## Non-text contrast

SC 1.4.11 (AA) uses at least 3:1 against adjacent colors for visual information needed to identify controls/states and meaningful graphic parts, with inactive, unmodified user-agent and essential-presentation exceptions. It does not require a border around every control or 3:1 between nonadjacent default/hover colors. Evaluate text separately under text contrast.

[W3C: Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

## Use of color

SC 1.4.1 (A) requires a visible way besides color alone to convey information, actions or distinctions. Text, shape or a meaningful lightness distinction can help; an accessible name by itself does not resolve a color-only cue for sighted users. Do not replace this with a mechanical rule that any two cosmetic changes prove accessibility.

[W3C: Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

## Moving and auto-updating content

SC 2.2.2 (A) requires user control for nonessential automatically started movement lasting over five seconds alongside other content. Auto-updating content alongside other content also needs pause/stop/hide or update-frequency control; it has no five-second exception. Stopping only while hover/focus is held is not a sufficient pause mechanism. Check the criterion's conditions rather than adopting a historical carousel timing heuristic.

[W3C: Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)

## Text spacing

SC 1.4.12 (AA) checks that user overrides do not lose content or functionality at line height 1.5×, paragraph spacing 2×, letter spacing 0.12× and word spacing 0.16× font size. These are override tests, not mandatory authored styling. Script-specific exceptions apply.

[W3C: Text Spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html)

## Reflow

SC 1.4.10 (AA) covers vertical-flow content at 320 CSS pixels wide, or horizontal-flow content at 256 CSS pixels high, without losing information/function or requiring two-axis scrolling. Content requiring a two-dimensional layout has an exception; it does not exempt the rest of the page.

[W3C: Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)

## Meaningful sequence

SC 1.3.2 (A) requires a correct reading sequence to be programmatically determinable when order affects meaning. More than one order may work; independent main/navigation sections need not have one compulsory order. CSS positioning must preserve meaningful relationships when linearized.

[W3C: Meaningful Sequence](https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html)

## Focus order

SC 2.4.3 (A) requires sequential focus order to preserve meaning and operability where sequence matters. It need not exactly match visual or reading order, but should remain logical for the relevant presentations. For a modal, focus belongs inside while other content is inert and returns appropriately on dismissal; this is an explanatory example, not proof that every overlay should be modal.

[W3C: Focus Order](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html)

## Keyboard operation

SC 2.1.1 (A) requires functionality through a keyboard interface without specific individual-keystroke timing, except underlying functions dependent on the movement path. A custom shortcut for every action is not required, nor must every redundant pointer control have its own focus stop if comparable functionality is available. Prefer established platform interaction conventions.

[W3C: Keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html)

## Bypassing repeated blocks

SC 2.4.1 (A) requires a mechanism to bypass blocks repeated across multiple related pages. A skip link is one technique; appropriate grouping/landmarks and user-agent-supported mechanisms are others. It does not require moving every navigation block to the bottom of the DOM.

[W3C: Bypass Blocks](https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html)

## Resize text

Checked 2026-10-25 against [W3C SC 1.4.4](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html). Except captions/images of text, text must resize up to 200% without losing content or functionality. This is a required supported enlargement range, not a direction to cap zoom. Responsive variations and intermediate offered steps must preserve the relevant behavior; check reflow separately.
