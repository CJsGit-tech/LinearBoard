# fit — 適配使用條件

## Responsibility

Does this task still work under the target space and input conditions?

Read the [shared execution contract](../execution.md) and the applicable mode.

## Execute

Identify assumptions made by the original composition about dimensions, text length, content quantity and input. Recompose or change controls only where those assumptions fail. Preserve the same job and essential facts rather than hiding them to satisfy a screenshot. Use realistic long/localized content and relevant intermediate states. Keep platform migration separate from responsive adjustment unless migration is requested.

## Platform focus

- **Web:** check actual overflow, meaningful comparison, intermediate widths, focus and hover alternatives.
- **Mobile:** inspect keyboard/available height, safe areas, orientation, text enlargement, touch and tablet use as relevant. Do not relabel CSS pixels as native units.

## Deliver and finish

the adapted interface and a bounded matrix of observed conditions.

Completion: the named job remains reachable and readable in the checked conditions; unsupported device claims remain explicit.

## Example

```text
$design-pro fit mobile "Chat composer at short available heights" --platform mobile-web
```

## Supporting design references

Load only the concepts needed for this target; follow their citations for source evidence. Command procedures are design-pro synthesis, not instructions attributed to a book.

- [responsive-and-continuity](../concepts/responsive-and-continuity.md)
- [spacing](../concepts/spacing.md)
- [accessibility](../concepts/accessibility.md)
