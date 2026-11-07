# craft — 打磨元件造型與狀態

## Responsibility

Does this component's appearance communicate its actual role and state?

Read the [shared execution contract](../execution.md) and the applicable mode.

## Execute

Inspect the component's label/content, hit area, optional icon/surface, state logic and existing family. Resolve inconsistencies between visual cues and behavior. Choose shape, spacing, type, color and optional depth as a coherent role; keep the activation area stable through hover/focus/pressed/disabled/pending/error/success states that actually apply. Reuse the existing component or variant where suitable. Remove ornamental nested controls. Do not add pretend success or a decorative loading delay.

## Creative application

For expressive anatomy, use [expressive component shape](../concepts/creative-design.md#expressive-component-shape). Relate the silhouette to the chosen product idea, and separate the decorative layer from label/content, hit geometry and focus/state feedback. A transformed background can leave its label upright. The existing plain control may remain the best choice; unusual geometry is not a completion requirement.

Inspect the relevant states against the real background. A clipped corner must not clip a focus indicator or hide pending/error information; an expressive visual edge must not shrink the activation area or create nested ornamental controls. Report the actual shape/content relationship and demonstrated operation, rather than treating the presence of an effect as quality evidence. Preserve platform behavior in Mobile.

## Platform focus

- **Web:** inspect actual semantics, labels, keyboard operation and hit geometry.
- **Mobile:** distinguish drawn icon size from touch area; retain platform-appropriate controls and input behavior.

## Deliver and finish

a refined component/variant, its relevant state contract and demonstrated interaction.

Completion: its visible promise matches the operation, state changes are distinguishable, and its target remains usable.

## Example

```text
$design-pro craft web "Launch reminder action: one clear primary button with honest pending/error states"
```

## Supporting design references

Load only the concepts needed for this target; follow their citations for source evidence. Command procedures are design-pro synthesis, not instructions attributed to a book.

- [component-anatomy](../concepts/component-anatomy.md)
- [forms-and-errors](../concepts/forms-and-errors.md)
- [gestures-and-feedback](../concepts/gestures-and-feedback.md)
