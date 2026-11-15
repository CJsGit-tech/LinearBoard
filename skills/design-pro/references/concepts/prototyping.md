# Prototypes and fidelity

Build a prototype to answer one consequential uncertainty: structure, content, transition, detailed interaction or visual treatment. Set fidelity separately on each of those dimensions. [X12, pp. 67–82](../books/X12.md#prototype-the-uncertainty-not-a-compulsory-fidelity-ladder)

## DO

[U05, pp. 29–47](../books/U05.md#make-the-process-and-exceptions-concrete); [X17, p. 8](../books/X17.md#usability-prototypes-and-comparison)

- Give each testable control a clear purpose and specify the states and transitions the task needs.
- Use realistic content and important edge cases, such as a long result description or a failed operation.
- Label which services and interactions are simulated, and record a representation's limit separately from a usability failure.
- Reuse existing components or simple elements that carry enough meaning for the question.

## DON'T

[U05, pp. 29–43](../books/U05.md); [X15, pp. 64–89](../books/X15.md)

- Do not leave a gray box unlabeled; say whether it is content, an input or an action.
- Do not offer a screenshot as proof of behavior; exercise the behavior.
- Do not require a lo-fi wireframe or a particular tool for a small, well-specified correction.
- Do not coach a participant through the intended route and count it as unaided success.

## Guidelines and example

A pattern name is shorthand. For a modal or gallery, define content, entry/exit, focus and return behavior. A designer/implementer walkthrough surfaces implementation questions; observing intended users gives different evidence, so report them separately. [U05, pp. 26–39](../books/U05.md)

For a chatbot, a runnable local prototype can show composing, response progress and retry against a simulated service. It keeps the affected message and draft and labels the service boundary *(synthesis)*.

## Mockups and useful feedback

Use a visual mockup to explore hierarchy, type and color and to focus a discussion. State the user problem and the feedback wanted before presenting it. Carry structure and interaction reasoning in whatever artifact the task already has. [U10, pp. 4–5, 7–17, 23–24](../books/U10.md)

Name who owns the decision and weigh evidence and constraints, including the product owner's input. [U10, pp. 16, 21–24](../books/U10.md#present-context-and-use-explicit-decision-ownership)

## A maintainable behavior and asset contract

Show the states and transitions that matter, attach notes to the affected component, use realistic text and identify the correct asset and version. Give rules between widths and content extremes for representative layouts. Review feasibility in the target runtime and keep a feedback route open through implementation *(synthesis from [P01, *Building UI Mockups Developers Won't Hate*, exact filename and PDF pp. 12–28](../books/P01.md#pages-components-and-state-coverage))*.

## Match fidelity to the evidence sought

Use a rough flow to find route and state gaps. Specify each consequential trigger, effect and before/after journey, including system events. In a tabbed interface, keep the selected tab and displayed panel matched. A simulated send/retry keeps the intended message and labels the simulation *(synthesis from [P02, *The Guide to Interactive Wireframing*, exact filename and PDF pp. 39–54](../books/P02.md#what-rapid-prototype-evidence-can-establish))*.

## Reconcile artifacts, reality and outcomes

Choose representation, precision, interaction coverage and intended lifecycle independently. A mockup can refine type and color while a plain coded flow exercises recovery. [P03, *The Guide to Mockups*, PDF pp. 7–30, 64–70](../books/P03.md); [P04, *The Guide to Wireframing*, pp. 12–33, 102–113](../books/P04.md); [P05, *The Ultimate Guide to Wireframing*, pp. 8–13, 23–26, 40–50](../books/P05.md)

For each consequential transition, write: entry conditions → trigger → affected state → observable outcome → failure/recovery. Attach a late response to the task or conversation that started it. Treat request completion, displayed thanks, a hidden-input update and durable success as four distinct states *(synthesis prompted by [P06, *The Ultimate Guide to Prototyping*, pp. 107–119](../books/P06.md#historical-import-and-interaction-tutorials) and [P07, *The Woork Handbook*, pp. 73–85, 108–110](../books/P07.md#asynchronous-feedback-without-false-success))*.

Keep essential fields reachable at every viewport size and by keyboard. Keep labels visible while typing, validate for real, and show the actual request outcome. Keep targets stable under hover. [P06, pp. 115–119, 129–131](../books/P06.md#historical-import-and-interaction-tutorials); [current labels and input-error criteria](../current-accessibility.md#labels); [P07, pp. 92–107](../books/P07.md#effects-input-limits-and-ordering)

Use relevant sample content and explicit criteria. Report a scripted browser check as implementation evidence, a model walkthrough as synthesis, and observation of representative users as user evidence. [P06, pp. 60–85](../books/P06.md#usability-evidence-and-task-design)
