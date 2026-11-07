# reconcile — 修正意外的設計漂移

## Responsibility

Which differences between screens/components are intentional, and which are accidental drift?

Read the [shared execution contract](../execution.md) and the applicable mode.

## Execute

Inspect the applicable design contract and actual repeated patterns across the selected scope. Compare semantic roles, behavior and state before comparing CSS values. Preserve deliberate variants for different tasks and consequences. Reuse canonical components/tokens where they already express the right role; consolidate accidental divergence with the smallest compatible changes. Surface genuine contradictions in the source of truth rather than inventing a replacement system.

## Platform focus

- **Web:** compare repeated controls, content density, theme roles and responsive variants within the selected pages.
- **Mobile:** compare repeated navigation/input/surface behavior while respecting native platform conventions.

## Deliver and finish

an intentional-variant versus drift map, scoped corrections and any updated project design contract.

Completion: accidental drift is corrected and meaningful variants still express their distinct roles. Uniform radius or color everywhere is not the goal.

## Example

```text
$design-pro reconcile web "Compare primary actions on settings, profile and checkout; preserve their different consequences"
```

## Supporting design references

Load only the concepts needed for this target; follow their citations for source evidence. Command procedures are design-pro synthesis, not instructions attributed to a book.

- [style-guides](../concepts/style-guides.md)
- [pattern-selection](../concepts/pattern-selection.md)
- [component-anatomy](../concepts/component-anatomy.md)
