# recover — 處理失敗與中斷

## Responsibility

What happens when an operation is interrupted, fails or finishes late?

Read the [shared execution contract](../execution.md) and the applicable mode.

## Execute

Identify the operation's owner, input, pending state, commit point, failure signal, cancellation and retry semantics. Inspect what can be lost, duplicated or applied to the wrong object. Design truthful progress/recovery attached to the affected task. Preserve recoverable input and avoid duplicate submissions or false success. Exercise documented local/test failure paths when authorized; do not trigger harmful production failures or real duplicate transactions. A retry must respect the backend's actual guarantees, not a promise invented by the UI.

## Platform focus

- **Web:** check repeat submission, validation/network feedback and navigation during pending work.
- **Mobile:** check interrupted input, switching tasks/conversations, delayed responses and resumption relevant to the implementation.

## Deliver and finish

the specific recovery contract, repaired behavior and evidence from the exercised failure/retry path.

Completion: the tested failure leaves an understandable state and the recovery neither loses required input nor duplicates the affected operation. State any untested remote guarantee.

## Example

```text
$design-pro recover mobile "Late chat response must stay in its original conversation; retry must not duplicate my message"
```

## Supporting design references

Load only the concepts needed for this target; follow their citations for source evidence. Command procedures are design-pro synthesis, not instructions attributed to a book.

- [content-states](../concepts/content-states.md)
- [forms-and-errors](../concepts/forms-and-errors.md)
- [credibility](../concepts/credibility.md)
