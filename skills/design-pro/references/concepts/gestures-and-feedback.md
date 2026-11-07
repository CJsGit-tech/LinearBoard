# Gestures and microinteraction feedback

Gestures need a task, a discoverable route and a comprehensible result. Microinteractions can be examined as trigger, rules, feedback and repetition/modes; the reviewed source attributes this model to Dan Saffer. [M04, pp. 8–21, 83–91](../books/M04.md)

## DO

- Define what starts, changes and ends the action, including what happens if it is interrupted.
- Provide a usable alternative when a complex gesture is a shortcut.
- Connect feedback to the affected object and user task.
- Check repeated use and different device holds rather than assuming one thumb.

These apply [M04, pp. 15, 17–21, 86–91](../books/M04.md#gestures).

## DON'T

- Do not assume a familiar motion means the same thing in every context.
- Do not hide essential actions to make an interface look simpler.
- Do not turn historical gesture-size numbers or animation examples into current platform requirements.
- Do not make an operation look completed while it is still pending or failed. This is design-pro synthesis of the source's feedback model, not a quoted source rule.
- Do not make motion the only feedback or add a flourish that becomes disruptive on repetition.

## Guidelines and example

For a chat send, specify the trigger (send), rule (submit this turn), feedback (pending, response, failure) and repeat behavior (retry or another turn). A failed send should preserve the message and offer a relevant next action. These are design-pro applications of [M04, pp. 83–91](../books/M04.md#microinteractions-and-feedback).

For an unknown platform, avoid asserting a universal animation duration or native hit-area measurement. Check the product's existing behavior and the current platform requirements when those details affect the task.

## Motion is optional; operation state is essential

Decide whether motion explains a relationship, supports a task or merely adds competing activity. A baseline label/action must remain understandable before hover; a repeated flourish must not delay access or stand in for actual completion. A pending indicator is not an ETA, success result or evidence that the technology is better. Treat historical 0.1-second/300ms examples as contextual, not universal requirements. These are design-pro decisions qualified against [W09, *Web Design Book of Trends 2015–2016*, exact filename and PDF pp. 80–99](../books/W09.md#motion-truthful-feedback-and-control), which also contains recommendations we reject, including unnecessary loading sequences and hover-only signifiers. Apply [current moving-content checks](../current-accessibility.md#moving-and-auto-updating-content) when implementing.
