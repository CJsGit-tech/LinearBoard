# Notifications and interruption

A notification helps a recipient act on a relevant event. Decide benefit, urgency and channel before designing the prompt. An in-app badge, an in-app status message and an OS/browser push have different purposes and permission requirements. [M07, pp. 7, 10–12](../books/M07.md#principles-worth-retaining); [M06, pp. 35–37](../books/M06.md#input-and-action)

## DO

- Explain the benefit at a moment when the user has enough context to choose, and send only the kind of message promised. [M07, pp. 18–19](../books/M07.md#principles-worth-retaining)
- Make the action clear and take the recipient to the relevant destination. [M07, pp. 12, 21–22](../books/M07.md)
- Set frequency, timezone and urgency by recipient preference. Track fatigue and opt-outs alongside task outcomes. [M07, pp. 22, 24](../books/M07.md)
- For an in-app update, convey new activity with more than a colored dot *(synthesis from [M06, pp. 35–37](../books/M06.md))*.

## DON'T

See [M07 evidence limitations](../books/M07.md#evidence-limitations).

- Do not ask again after refusal, or send promotion dressed as a service alert.
- Do not invent urgency, or use location/history data without authorization for that use.
- Do not read opted-in versus opted-out retention as a causal effect.
- Do not count delivery as seen or understood.

## Guidelines and example

Check truncation with the actual language and presentation; the source's 60–120 characters is a starting point. Verify current native/browser permissions and support from primary sources for the chosen platform. [M07, pp. 11, 19, 21](../books/M07.md#boundaries-and-disagreements)

A game page can offer an optional release reminder after the visitor chooses to follow the game. In a local demo, label the signup as simulated and request no real push permission *(synthesis)*.
