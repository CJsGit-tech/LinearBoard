# Accessibility across modes

Identify the people, the task and the input/output paths before selecting a check. Consider sensory, motor, cognitive and situational constraints, and take requirements from the applicable current platform or standard. [X10, pp. 72–86](../books/X10.md#accessibility-retain-the-intent-check-the-implementation); [M05, pp. 218–225](../books/M05.md#accessibility-and-independent-use)

## DO

- Expose understandable names, state and feedback through the chosen platform, and verify operation as well as appearance. [M05, pp. 218–225](../books/M05.md)
- For web, check [keyboard functionality](../current-accessibility.md#keyboard-operation), [focus order](../current-accessibility.md#focus-order) and [reading sequence](../current-accessibility.md#meaningful-sequence) as three separate requirements.
- Explain each detected input error in text beside any color or icon cue. [Current input-error guidance](../current-accessibility.md#input-errors); [X08, pp. 18, 26](../books/X08.md)
- Evaluate [text contrast](../current-accessibility.md#contrast), [control/graphic contrast](../current-accessibility.md#non-text-contrast) and [color cues](../current-accessibility.md#use-of-color) separately.
- Test enlargement/reflow, actual activation regions and the relevant nonvisual and alternate-input use. Report which checks ran and which did not. [M05](../books/M05.md#accessibility-and-independent-use); [current web references](../current-accessibility.md)

## DON'T

- Do not reuse a 30px, 40pt, 44px or 72px example as a target rule; take web minimums from the current criteria and native values from the platform. [X09, p. 60](../books/X09.md#mobile-web-qualifications); [X10, pp. 84–85](../books/X10.md); [M06, pp. 29–31](../books/M06.md)
- Do not offer custom shortcuts in place of keyboard-operable functionality, or add a focus stop to static content. [Current keyboard guidance](../current-accessibility.md#keyboard-operation)
- Do not reorder navigation in the DOM to "fix screen readers"; check meaning, focus and bypass routes in the actual layout. [X10, pp. 83–84 and qualifications](../books/X10.md#accessibility-retain-the-intent-check-the-implementation)
- Do not claim compliance from a grayscale filter, a famous product example, an old checklist or an automated scan alone; list the behavior each left untested. [X10, pp. 83–86](../books/X10.md)

## Guidelines and example

For a broad concept question, explain shared access principles directly. Ask native versus mobile web only when a requested dimension, API or test depends on it. The [current web criteria](../current-accessibility.md) are focused and dated; they cover web only and are not a certification.

For the chatbot demo, inspect labeled composition/send/retry controls, meaningful message order, pending/error feedback, draft retention and keyboard access. Name physical phone keyboard, native accessibility and screen-reader behavior as untested unless exercised *(synthesis)*.
