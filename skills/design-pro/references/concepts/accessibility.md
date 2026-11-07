# Accessibility across modes

Identify the people, task and input/output paths before selecting a check. A polished screenshot, readable text or keyboard smoke test cannot establish complete access. Historical sources support considering sensory, motor, cognitive and situational constraints; current requirements must come from the applicable platform or standard. [X10, pp. 72–86](../books/X10.md#accessibility-retain-the-intent-check-the-implementation); [M05, pp. 218–225](../books/M05.md#accessibility-and-independent-use)

## DO

- Expose understandable names, state and feedback through the chosen platform, and verify meaningful operation rather than appearance alone. [M05, pp. 218–225](../books/M05.md)
- For web, check [keyboard functionality](../current-accessibility.md#keyboard-operation), [focus order](../current-accessibility.md#focus-order) and [reading sequence](../current-accessibility.md#meaningful-sequence). Their requirements are related but distinct.
- Give detected input errors textual explanation; do not rely on a red outline or warning icon alone. [Current input-error guidance](../current-accessibility.md#input-errors); [X08, pp. 18, 26](../books/X08.md)
- Evaluate [text contrast](../current-accessibility.md#contrast), [control/graphic contrast](../current-accessibility.md#non-text-contrast) and [color cues](../current-accessibility.md#use-of-color) separately.
- Test enlargement/reflow, actual activation regions and relevant nonvisual/alternate-input use. Report which checks were executed and which remain untested. [M05](../books/M05.md#accessibility-and-independent-use); [current web references](../current-accessibility.md)

## DON'T

- Do not transfer 30px, 40pt, 44px or 72px examples into a universal target rule. Web CSS pixels and native units need the relevant context. [X09, p. 60](../books/X09.md#mobile-web-qualifications); [X10, pp. 84–85](../books/X10.md); [M06, pp. 29–31](../books/M06.md)
- Do not treat custom shortcuts as a substitute for keyboard-operable functionality or add a focus stop to every static fragment without purpose. [Current keyboard guidance](../current-accessibility.md#keyboard-operation)
- Do not blindly reorder navigation in the DOM to “fix screen readers”; check meaning, focus and bypass routes in the actual layout. [X10, pp. 83–84 and qualifications](../books/X10.md#accessibility-retain-the-intent-check-the-implementation)
- Do not claim compliance from a grayscale filter, a famous product example, an old checklist or an automated scan alone. Those methods leave material behavior untested. [X10, pp. 83–86](../books/X10.md)

## Guidelines and example

For broad concept questions, explain shared access principles without demanding a product interview. Clarify native versus mobile web only when a requested dimension, API or test changes. The [current web criteria](../current-accessibility.md) are focused, dated references and do not constitute native platform guidance or full certification.

For the chatbot demo, inspect labeled composition/send/retry controls, meaningful message order, pending/error feedback, draft retention and keyboard access. A narrow desktop browser test does not prove a physical phone keyboard, native accessibility or screen-reader success. These are design-pro test applications.
