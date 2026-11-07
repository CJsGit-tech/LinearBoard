# Web forms and input errors

Make the expected input understandable, identify detected mistakes, and support correction. The specific standards below are current external guidance, not claims attributed to the reviewed books.

## DO

- Provide visible labels or necessary instructions for input, including optional fields. [W3C labels](../current-accessibility.md#labels)
- For a detected input error, identify the affected field and explain the problem in text. [W3C input errors](../current-accessibility.md#input-errors)
- Preserve valid entries, keep feedback relevant to the affected task, and distinguish invalid input from a service failure. These are design-pro recovery recommendations.
- Connect the feedback to its control using the project's accessible implementation pattern; test keyboard and assistive-technology behavior rather than assuming visual proximity proves it.
- Match the input keyboard to the expected data, and make defaults or suggestions correctable. Historical examples support the principle, while current HTML or native API behavior needs implementation-specific verification. [M06, pp. 16–20](../books/M06.md#input-and-action); [M08, pp. 9–11](../books/M08.md#adapt-interaction-not-just-width)
- Require a reason for each field; no fixed number of fields suits every task. Test completion and necessary data quality together. [X02, pp. 13–16](../books/X02.md#request-only-useful-information)
- Keep validation in the affected context, with timing appropriate to the entry process. Do not mark incomplete typing as a confirmed mistake or treat a recognized card logo as proof a payment will succeed. [X08, pp. 26–28](../books/X08.md#input-and-recovery)

## DON'T

- Do not rely on a red border alone to explain failure.
- Do not clear a user's entire form because one value needs correction.
- Do not claim that the error-identification criterion mandates inline placement or one exact focus policy.
- Do not present a simulated submission as an actual subscription or message delivery.

## Guidelines and example

Choose inline feedback, a summary or both based on form length and the recovery path. State the problem and a useful next step; programmatic relationships and recovery suggestions involve distinct requirements from merely displaying an error. [W3C input errors](../current-accessibility.md#input-errors)

Example: “Enter an email address such as name@example.com” identifies an expected format. For a simulated game announcement signup, disclose the simulation and retain the entry on failure. In chat, a network-style failure belongs with retry for that message, rather than being described as invalid user wording. These examples are design-pro synthesis.

## Suggestions and interpretation

Let users correct defaults and distinguish a suggestion from the value actually selected. For a consequential natural-language entry, expose the interpreted date, unit or destination before acting; forgiving formatting is not proof of language understanding. [U09, pp. 30–34, 51–53](../books/U09.md#input-and-navigation-decision-rules)

Use validation timing that fits the entry process. The source's recommendation to validate as people type does not justify announcing errors before they have finished entering a value. Profile-completion percentages must represent a useful, explainable goal rather than pressure to disclose optional personal information. [U09, pp. 35–42](../books/U09.md#getting-input-inspected-examples-and-qualified-uses)

## Historical code is not a complete form contract

A visible label and aligned field do not prove their programmatic association, and a displayed success string does not prove a successful request. Keep labels during entry, identify the affected field in text, preserve recoverable values and show the actual result. Reuse semantic controls and current project patterns rather than copying historical fixed-width floats or anchor-based submit scripts. These are design-pro applications, qualifying [P07, *The Woork Handbook*, exact filename and PDF pp. 28–34, 51–55, 73–85](../books/P07.md#pagination-forms-and-disclosure-states) and [P06, *The Ultimate Guide to Prototyping*, pp. 115–119](../books/P06.md#historical-import-and-interaction-tutorials). Native form behavior requires native verification; the source tutorials are browser examples.
