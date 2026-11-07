# journey — 接好跨畫面任務

## Responsibility

Can someone finish the intended job across screens and transitions?

Read the [shared execution contract](../execution.md) and the applicable mode.

## Execute

Model the initiating situation, required information, user choices, system responses, committed result and return/resume paths for one named job. Inspect actual routes/state ownership rather than inferring completion from connected screens. Find missing or ambiguous transitions and fix them within the feature. Preserve relevant values, selection and position where the task requires continuity. Distinguish interface state, local persistence and confirmed remote completion. Hand off a specific complex failure investigation to recover only when needed.

## Platform focus

- **Web:** inspect routing, navigation history, forms, selections and return from detail.
- **Mobile:** inspect back/sheet behavior, keyboard transitions and task resumption in the actual platform.

## Deliver and finish

a compact task/state map, repaired gaps and a demonstrated end-to-end path.

Completion: the agreed starting state reaches its real completion condition and essential return/resume paths preserve their required context.

## Example

```text
$design-pro journey mobile "Write a draft, switch conversations and return without losing it"
```

## Supporting design references

Load only the concepts needed for this target; follow their citations for source evidence. Command procedures are design-pro synthesis, not instructions attributed to a book.

- [information-architecture](../concepts/information-architecture.md)
- [navigation](../concepts/navigation.md)
- [responsive-and-continuity](../concepts/responsive-and-continuity.md)
