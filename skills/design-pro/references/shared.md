# Shared design decisions

Rules cite the book passage they come from. A rule marked *(synthesis)* is design-pro's own; any citation beside it is the passage it builds on or corrects. Source limits and rejected recommendations live in the linked book notes. Current web requirements live in [current accessibility sources](current-accessibility.md).

## Start with a task and a decision

State who is trying to accomplish what, and in which setting. Research motivation and context alongside performance, and pick an exploratory or evaluative method by the uncertainty before picking a tool. Get evidence from representative users; a fictional brief or a conversation with the requester stands in for it only as a labeled assumption. [M02, pp. 13–23](books/M02.md#research-selection)

Use usefulness, usability, findability, credibility, desirability, accessibility and value as prompts for what is missing. Weigh them by the task: enjoyment can be the use of a game, and an attractive feature that serves no task still fails. [X09, pp. 21–34](books/X09.md)

Define observable success before measuring. Measure discovery, task completion and recovery; completing the task matters more than click count or liking a screen. [M02, pp. 21–22, 28, 32–35](books/M02.md#metrics-and-task-design)

Tie each proposed change to an expected outcome and to what would contradict it. Add a feature when it serves a task, and keep an essential task even when it is infrequent *(synthesis)*. [X01, pp. 11–12](books/X01.md#hypotheses-critique-and-evaluation); [X03, pp. 3–12](books/X03.md)

When the decision spans features or releases, use [strategy and criteria](concepts/strategy-and-criteria.md). Map the task to its flows and states and set acceptance before evaluating. Size the documents to the uncertainty. [X11, pp. 44–52](books/X11.md); [X12, pp. 7–21, 83–93](books/X12.md)

## Group meaning before drawing containers

Keep an object and its labels and actions perceptually together. Use separation to mark a new thought. Use a card for a coherent actionable unit or a summary/detail relationship. [M03, pp. 8–10, 19, 21–27](books/M03.md#principles-and-applications); [T01, pp. 12–14](books/T01.md#decisions-worth-retaining)

**User's default visual preference:** use an open, continuous composition in both modes. Form groups with whitespace, alignment and type size/weight. This is the user's preference, not a rule from the books; an explicit project direction or established product contract overrides it.

**Applying it** *(synthesis)*:

- Add a surface or boundary when it marks a meaningful unit, action, state or layer.
- For dense comparison, try a table or list before cards.
- Keep controls discoverable, with usable targets and visible focus, error and selection cues.
- Before delivery, review the whole page for repeated frames (outlined controls, cards, pills, divider bars, nested surfaces) and remove the structure itself. Fading a border's color leaves the grouping fragmented.

## Keep expression and reading in balance

Let an expressive heading carry brand identity while body text supports comprehension. Check heading contrast against the actual image crop and keep important subjects visible. On a narrow canvas, reflow or re-rank content; keep necessary text at a readable size and keep semantic structure. [T02, pp. 11–24](books/T02.md#practical-techniques); [T01, pp. 6–7, 20–26](books/T01.md#decisions-worth-retaining)

Treat source figures for line length, leading, font family and size as starting points. Set them by testing actual content with user-adjusted text settings, and take web criteria from [current accessibility sources](current-accessibility.md).

## Reuse with context

Choose a mood board for atmosphere, a style tile for concrete visual choices without layout, and a component/pattern reference for repeatable implementation. Produce only the documents the decision needs. [S01, pp. 10–23](books/S01.md#choose-the-artifact-for-the-decision)

Record semantic roles, variants, conditions of use and implementation beside examples. Keep deliberate variation between buttons or layouts that serve different tasks. [S02, pp. 27–41, 46–48](books/S02.md#practical-guidance)

Inspect the existing product first, choose the closest reusable pattern, extend it if needed, and give a reason for a genuinely new one. For a new product, choose the smallest coherent set of tokens and components that supports its tasks *(synthesis)*.

Compare patterns by trigger, visibility and actual behavior as well as appearance. Make a familiar cue match the operation available, and use novelty where it supports a task. [X05, pp. 24–48](books/X05.md)

Give honest feedback about saving and freshness. Every control does what it implies; loading appears only while something is loading. A simulation may show pending and error behavior when its service boundary is labeled *(synthesis; rejects the deceptive controls in [X07, pp. 11–17](books/X07.md#deliberate-rejection-of-deceptive-controls))*.

## Evidence and verification

Name the evidence each claim rests on, using these four levels, and report what was untested:

| Evidence | Establishes |
| --- | --- |
| Screenshot or static example | Composition at that size and state |
| Implementation walkthrough | Conformance and craft |
| Interaction test in the target runtime | The exercised behavior: wrapping, actual tap/click regions, state recovery |
| Representative-user research or accessibility evaluation | Use by the intended people |

Verify the specific risk: visual wrapping for typography, activation regions for adjacent controls, state recovery for a failed operation. [S02, pp. 32–34](books/S02.md#practical-guidance); [M02, pp. 19–28](books/M02.md); [X04, pp. 27–30](books/X04.md#verification-methods-are-different)

Choose prototype dimensions by the unanswered question and define each expected transition before wiring its control. Keep failure and recovery in the prototype even when infrequent. Load [prototyping](concepts/prototyping.md) for fidelity choices, simulated services and implementation-state contracts.
