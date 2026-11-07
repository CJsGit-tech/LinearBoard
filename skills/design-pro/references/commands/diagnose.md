# diagnose — 找出問題與原因

## Responsibility

What is actually making this interface difficult or visually incoherent?

Read the [shared execution contract](../execution.md) and the applicable mode.

## Execute

Read the visible composition and the relevant implementation together. Trace a symptom to plausible causes, distinguishing a layout/grouping issue from a component/state/data issue. Prioritize findings by task blockage, loss risk, repeated effort and then visual distraction; do not manufacture a fixed count. For each actionable finding, name its location, observed symptom, likely cause, smallest useful intervention and how to check it. Recommend one first intervention, not a stack of unrelated commands.

## Creative application

When the complaint concerns taste or sameness, use [critique and selection](../concepts/creative-design.md#critique-and-selection). Identify a visible relationship: equal emphasis leaves no focal point, a repeated section rhythm ignores different content roles, or a motif has no connection to the subject. Distinguish deliberate restraint and familiar usable patterns from accidental uniformity. Name what evidence would change the judgment.

A name/content swap can prompt a specificity check, but cannot prove copying or originality. Diagnose the cause before recommending new imagery or effects. Read-only output should separate an observed formal symptom, its implication for the brief and an interpretation that needs user research. Do not modify the target or give unexplained aesthetic scores.

## Platform focus

- **Web:** distinguish content width, DOM order and actual focus/navigation behavior from visual impression.
- **Mobile:** inspect available space and input mode; do not attribute a screenshot's clipping to the OS keyboard without evidence.

## Deliver and finish

prioritized evidence-backed diagnosis and recommended next command. No source edits.

Completion: each reported defect has supporting evidence or an explicit hypothesis label, and the next action resolves the named uncertainty.

## Example

```text
$design-pro diagnose web "Game homepage: why does the navigation feel detached?"
```

## Supporting design references

Load only the concepts needed for this target; follow their citations for source evidence. Command procedures are design-pro synthesis, not instructions attributed to a book.

- [research](../concepts/research.md)
- [strategy-and-criteria](../concepts/strategy-and-criteria.md)
- [component-anatomy](../concepts/component-anatomy.md)
