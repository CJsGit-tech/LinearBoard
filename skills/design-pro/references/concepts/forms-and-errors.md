# Web forms and input errors

Make the expected input understandable, identify detected mistakes and support correction. The W3C items are current external requirements, not book claims.

## DO

- Give every input a visible label or the instructions it needs, including optional fields. [W3C labels](../current-accessibility.md#labels)
- For a detected input error, identify the affected field and explain the problem in text. [W3C input errors](../current-accessibility.md#input-errors)
- Preserve valid entries, keep feedback with the affected task, and tell invalid input apart from a service failure *(synthesis)*.
- Connect feedback to its control with the project's accessible implementation pattern, then test keyboard and assistive-technology behavior.
- Match the input keyboard to the expected data and make defaults and suggestions correctable. Verify current HTML or native API behavior in the implementation. [M06, pp. 16–20](../books/M06.md#input-and-action); [M08, pp. 9–11](../books/M08.md#adapt-interaction-not-just-width)
- Have a reason for each field. Test completion and data quality together. [X02, pp. 13–16](../books/X02.md#request-only-useful-information)
- Keep validation in the affected context and time it to when the value is plausibly complete, such as on leaving the field or on submit. [X08, pp. 26–28](../books/X08.md#input-and-recovery)

## DON'T

- Do not rely on a red border alone to explain failure; add text.
- Do not clear the whole form because one value needs correction.
- Do not flag incomplete typing as a mistake, or treat a recognized card logo as a verified payment. [X08, pp. 26–28](../books/X08.md#input-and-recovery)
- Do not present a simulated submission as an actual subscription or delivery.
- Do not say the error-identification criterion requires inline placement or one focus policy; it requires identification in text.

## Guidelines and example

Choose inline feedback, a summary or both by form length and recovery path. State the problem and a useful next step. Displaying an error, associating it programmatically and suggesting a correction are three separate requirements. [W3C input errors](../current-accessibility.md#input-errors)

Example: "Enter an email address such as name@example.com" names the expected format. For a simulated signup, disclose the simulation and keep the entry on failure. In chat, show a network failure as retry for that message, not as invalid wording *(synthesis)*.

## Suggestions and interpretation

Let users correct defaults, and show a suggestion as distinct from the selected value. For a consequential natural-language entry, show the interpreted date, unit or destination before acting. [U09, pp. 30–34, 51–53](../books/U09.md#input-and-navigation-decision-rules)

Announce an error once the person has finished entering the value. Make a profile-completion percentage represent a useful, explainable goal and leave optional personal data optional. [U09, pp. 35–42](../books/U09.md#getting-input-inspected-examples-and-qualified-uses)

## Historical code is not a complete form contract

Keep labels visible during entry, associate each label with its field in code, identify the affected field in text, preserve recoverable values and show the actual request result. Use semantic controls and current project patterns in place of historical fixed-width floats or anchor-based submit scripts *(synthesis; corrects [P07, *The Woork Handbook*, exact filename and PDF pp. 28–34, 51–55, 73–85](../books/P07.md#pagination-forms-and-disclosure-states) and [P06, *The Ultimate Guide to Prototyping*, pp. 115–119](../books/P06.md#historical-import-and-interaction-tutorials))*. Verify native form behavior on the native platform.
