# Prototypes and fidelity

Choose a prototype to answer a consequential uncertainty: structure, content, transition, detailed interaction or visual treatment. Fidelity can differ across these dimensions; a compulsory sequence of artifacts is unnecessary. [X12, pp. 67–82](../books/X12.md#prototype-the-uncertainty-not-a-compulsory-fidelity-ladder)

## DO

- Give each testable control an understandable purpose and specify the states/transitions needed for the task.
- Use realistic, relevant content and important edge cases, such as a long result description or a failed operation.
- Explain which services/interactions are simulated; distinguish a representation's limits from a usability failure.
- Reuse existing components or suitable simple elements, with enough meaning to support the question. [U05, pp. 29–47](../books/U05.md#make-the-process-and-exceptions-concrete); [X17, p. 8](../books/X17.md#usability-prototypes-and-comparison)

## DON'T

- Do not let an unlabeled gray box hide whether it is content, an input or an action.
- Do not call a screenshot proof of behavior, or claim high visual fidelity proves production feasibility.
- Do not require a lo-fi wireframe for a small well-specified correction, or require a particular tool when the environment supports a suitable alternative.
- Do not coach a participant through the intended route and count it as unaided success. [U05, pp. 29–43](../books/U05.md); [X15, pp. 64–89](../books/X15.md)

## Guidelines and example

A pattern name is shorthand, not a complete behavior specification. For a modal or gallery, define its content, entry/exit, focus and return behavior as relevant. A designer/implementer walkthrough reveals implementation questions; intended-user task observation provides different evidence. Keep that distinction in evaluation. [U05, pp. 26–39](../books/U05.md)

For a chatbot, a runnable local prototype can show composing, response progress and retry with a simulated service. It should preserve the affected message/draft and identify the service boundary honestly. Desktop viewport checks cannot prove physical mobile keyboard behavior or native accessibility. These are design-pro applications and verification limits, not findings that a specific prototype works.

## Mockups and useful feedback

A visual mockup can explore hierarchy, type and color and support a focused discussion; it does not establish interaction behavior. State the user problem and the feedback needed before presenting it. Preserve structure and interaction reasoning without requiring a separate wireframe artifact for every task. The source itself combines a contextual process with a contradictory absolute wireframing prescription. [U10, pp. 4–5, 7–17, 23–24](../books/U10.md)

Clarify who owns the decision and weigh evidence and constraints. Avoid turning “design by committee” criticism into a rule that dismisses the product owner or other consequential input. A visual review, a runnable interaction check and an intended-user task study provide different evidence. [U10, pp. 16, 21–24](../books/U10.md#present-context-and-use-explicit-decision-ownership)

## A maintainable behavior and asset contract

Show the states/transitions that matter, attach notes to the affected component, use realistic text, and identify the correct asset/version. Representative layouts need rules between widths and content extremes; duplicating every page or breakpoint is not a substitute. Review feasibility in the target runtime, because a clickable mockup cannot establish browser chrome, keyboard or native behavior. These are design-pro adaptations of [P01, *Building UI Mockups Developers Won't Hate*, exact filename and PDF pp. 12–28](../books/P01.md#pages-components-and-state-coverage). The source's long compatibility/plugin lists are historical, and its claim to cover every possible situation so developers need not think is rejected. Preserve a feedback route through implementation rather than a one-way handoff.

## Match fidelity to the evidence sought

A rough flow can reveal route/state gaps without proving final reading, visual hierarchy, native behavior or live-service reliability. Specify each consequential trigger, effect and before/after journey; system events count too. In a tabbed interface, selected tab and displayed panel must stay matched. A simulated send/retry must preserve the intended message without implying server success. These are design-pro adaptations of [P02, *The Guide to Interactive Wireframing*, exact filename and PDF pp. 39–54](../books/P02.md#what-rapid-prototype-evidence-can-establish). The source's claim that low/high fidelity always produce the same usability data is rejected, and its ten-versus-two example is not a measured productivity ratio. Neither a clickable wireframe nor stakeholder buy-in alone establishes an MVP.

## Reconcile artifacts, reality and outcomes

Choose representation, precision, interaction coverage and intended lifecycle independently. A mockup can refine type/color while a plain coded flow exercises recovery; neither requires a compulsory wireframe→mockup→prototype ladder. Paper can retain versions too. Reused Yelp/tab examples across the guides are not independent outcome studies. [P03, *The Guide to Mockups*, PDF pp. 7–30, 64–70](../books/P03.md); [P04, *The Guide to Wireframing*, pp. 12–33, 102–113](../books/P04.md); [P05, *The Ultimate Guide to Wireframing*, pp. 8–13, 23–26, 40–50](../books/P05.md)

For each consequential transition, write entry conditions → trigger → affected state → observable outcome → failure/recovery. A late response belongs to the originating task/conversation. Request completion, displayed thanks, a hidden-input update and durable success are distinct. This is design-pro synthesis prompted by [P06, *The Ultimate Guide to Prototyping*, pp. 107–119](../books/P06.md#historical-import-and-interaction-tutorials) and [P07, *The Woork Handbook*, pp. 73–85, 108–110](../books/P07.md#asynchronous-feedback-without-false-success), whose examples contain omissions rather than demonstrating a correct production implementation.

Keep essential fields reachable across viewport sizes and keyboard operation. Preserve labels while typing; do not gate a required form behind a fixed scroll offset or replace real validation/request outcome with click→thanks. [P06, pp. 115–119, 129–131](../books/P06.md#historical-import-and-interaction-tutorials); compare [current labels and input-error criteria](../current-accessibility.md#labels). Keep stable operable targets rather than moving a menu away on hover. [P07, pp. 92–107](../books/P07.md#effects-input-limits-and-ordering)

Use relevant sample content and explicit criteria; do not invent research participants, interpret stakeholder buy-in as usability, or assume a five/twenty-person threshold guarantees validity. Report a scripted browser check as implementation evidence, a model walkthrough as synthesis, and representative-user observation as user evidence. [P06, pp. 60–85](../books/P06.md#usability-evidence-and-task-design)
