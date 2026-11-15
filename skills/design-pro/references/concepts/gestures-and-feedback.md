# Gestures and microinteraction feedback

A gesture needs a task, a discoverable route and a comprehensible result. Examine a microinteraction as trigger, rules, feedback and repetition/modes, a model the source attributes to Dan Saffer. [M04, pp. 8–21, 83–91](../books/M04.md)

## DO

[M04, pp. 15, 17–21, 86–91](../books/M04.md#gestures)

- Define what starts, changes and ends the action, including what happens when it is interrupted.
- Provide a usable alternative when a complex gesture is a shortcut.
- Connect feedback to the affected object and the user's task.
- Check repeated use and different device holds.

## DON'T

- Do not rely on a familiar motion carrying the same meaning in a new context; add a signifier.
- Do not hide essential actions to make an interface look simpler.
- Do not reuse historical gesture sizes or animation timings; take them from the current platform and product.
- Do not show an operation as completed while it is pending or failed *(synthesis)*.
- Do not make motion the only feedback, or add a flourish that disrupts on repetition.

## Guidelines and example

For a chat send, specify the trigger (send), rule (submit this turn), feedback (pending, response, failure) and repeat behavior (retry or another turn). On a failed send, keep the message and offer a next action *(synthesis from [M04, pp. 83–91](../books/M04.md#microinteractions-and-feedback))*.

When the platform is unknown, take animation duration and hit-area values from the product's existing behavior and current platform requirements.

## Motion is optional; operation state is essential

Use motion when it explains a relationship or supports a task. Keep the baseline label and action understandable before hover, and keep access immediate on repeated use. A pending indicator shows that work is in progress and nothing more. *(synthesis; corrects [W09, *Web Design Book of Trends 2015–2016*, exact filename and PDF pp. 80–99](../books/W09.md#motion-truthful-feedback-and-control))* Apply [current moving-content checks](../current-accessibility.md#moving-and-auto-updating-content) when implementing.
