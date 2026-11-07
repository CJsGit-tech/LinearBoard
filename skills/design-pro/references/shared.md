# Shared design decisions

This reference distinguishes reviewed source guidance from design-pro applications. Source details and limitations live in the linked book notes; current web requirements live separately from historical examples.

## Start with a task and a decision

State who is trying to accomplish what and in which setting. Research should address motivation and context alongside performance; select exploratory versus evaluative methods for the uncertainty rather than choosing a tool first. A fictional brief or a conversation with the requester does not replace evidence from representative users. [M02, pp. 13–23](books/M02.md#research-selection)

Use usefulness, usability, findability, credibility, desirability, accessibility and value as prompts for missing considerations. They are not equally weighted scores or a formula guaranteeing success. An entertaining game can be useful for enjoyment; an attractive irrelevant feature can still fail the task. [X09, pp. 21–34](books/X09.md)

Define observable success before measuring: completing the intended task matters more than minimizing clicks. Observe discovery, task completion and recovery, not just whether a participant likes a screen. [M02, pp. 21–22, 28, 32–35](books/M02.md#metrics-and-task-design)

Connect a proposed change to an expected outcome and what would contradict it. Avoid adding a feature solely because one request exists; also avoid dismissing an essential task solely because it is infrequent. The latter is design-pro qualification of a strict feature-pruning process. [X01, pp. 11–12](books/X01.md#hypotheses-critique-and-evaluation); [X03, pp. 3–12](books/X03.md)

Use [strategy and criteria](concepts/strategy-and-criteria.md) when the decision spans features or releases. Map the task to necessary flows/states and define acceptance before evaluating the result. Scale documents to the uncertainty rather than requiring a canvas, persona, wireframe and full specification for every request. [X11, pp. 44–52](books/X11.md); [X12, pp. 7–21, 83–93](books/X12.md)

## Group meaning before drawing containers

Keep an object and its related labels/actions perceptually together. Separation should express a new thought; do not put a border around every item to manufacture hierarchy. A card is useful for a coherent actionable unit or summary/detail relationship, not all information. [M03, pp. 8–10, 19, 21–27](books/M03.md#principles-and-applications); [T01, pp. 12–14](books/T01.md#decisions-worth-retaining)

**User's default visual preference:** use an open, continuous composition in both modes. Establish groups with whitespace, alignment and type size/weight. Repeated outlined controls, cards, pills, divider bars and nested surfaces can fragment the page; do not use them as the default grouping system. This is a personal preference, not a universal rule attributed to the books.

**Design-pro application:** use a surface or boundary when it adds a clear distinction for a meaningful unit, action, state or layer. For dense comparison, assess a table/list rather than assuming cards. Preserve discoverability, target size, focus, error and selection cues. Review the whole page for redundant frames; lowering their contrast alone does not resolve fragmented grouping. Respect an explicit project direction or established product contract that requires a different treatment.

## Keep expression and reading in balance

An expressive heading can carry brand identity while body text supports comprehension. Check its contrast against the actual image crop and keep important subjects visible. Do not solve a narrow canvas by shrinking necessary text or removing meaningful semantic structure. [T02, pp. 11–24](books/T02.md#practical-techniques); [T01, pp. 6–7, 20–26](books/T01.md#decisions-worth-retaining)

Source heuristics about line length, leading, specific font families or fashionable sizes are starting points, not standards. Test actual content and user-adjusted text settings. Use [current accessibility sources](current-accessibility.md) for the relevant web criteria rather than treating a 2015 screenshot as compliance evidence.

## Reuse with context

Choose a mood board for atmosphere, a style tile for concrete visual choices without layout, and a component/pattern reference for repeatable implementation. A major project need not generate every possible design document. [S01, pp. 10–23](books/S01.md#choose-the-artifact-for-the-decision)

Record semantic roles, relevant variants, conditions of use and implementation beside examples. Preserve deliberate variation for different tasks rather than normalizing all buttons or layouts. [S02, pp. 27–41, 46–48](books/S02.md#practical-guidance)

**Design-pro application:** inspect the existing product first, choose the closest reusable pattern, extend it if necessary, and state a reason for a genuinely new one. For a new product, choose the smallest coherent set of tokens and components that supports its tasks.

Compare patterns' trigger, visibility and actual behavior, not only their appearance. A familiar cue must match the operation available; selective novelty should support a task rather than claim a universal psychological effect. [X05, pp. 24–48](books/X05.md)

Use honest feedback to address uncertainty about saving or freshness. Design-pro deliberately rejects no-op controls and fabricated loading intended to manufacture reassurance or value. A simulation can show pending/error behavior when its service boundary is clear. [X07, pp. 11–17](books/X07.md#deliberate-rejection-of-deceptive-controls)

## Evidence and verification

A static example shows composition, not the behavior of its original product. Distinguish screenshot review, interaction tests, representative-user research and accessibility evaluation. Verify the specific risk: visual wrapping for typography, actual tap/click regions for adjacent controls, and state recovery for a failed operation. [S02, pp. 32–34](books/S02.md#practical-guidance); [M02, pp. 19–28](books/M02.md)

An implementation walkthrough checks conformance and craft; acceptance work exercises a core workflow; user research evaluates use by the intended people. The historical guide explicitly separates the first from usability testing. Report those boundaries in the demos. [X04, pp. 27–30](books/X04.md#verification-methods-are-different)

Choose prototype dimensions by the unanswered question and define the expected transition before wiring a control. Retain failure/recovery even when infrequent. Mockup galleries and repeated examples do not prove success; visual realism, functional coverage and lifecycle differ. Load [prototyping](concepts/prototyping.md) for fidelity choices, simulated services and implementation-state contracts.
