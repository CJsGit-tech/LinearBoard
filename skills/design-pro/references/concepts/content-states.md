# Content states and recovery

Design four states separately: empty collection, pending operation, completed result and failed operation *(synthesis)*. [M06, pp. 123–124, 131–132](../books/M06.md#content-and-interface-states); [M04, pp. 83–91](../books/M04.md#microinteractions-and-feedback)

## DO

- Explain why a view is empty and offer a relevant next step. [M06, pp. 123–124](../books/M06.md)
- Attach progress to the action it represents and make it look different from a finished result. [M04, pp. 83–91](../books/M04.md)
- Preserve useful work and put the recovery action beside the affected operation *(synthesis)*; see [forms and errors](forms-and-errors.md) for input cases.
- Offer undo only when the operation can be restored. [M06, pp. 47–48](../books/M06.md#input-and-action)
- Make Save and Refresh do what they say and report real persistence and freshness *(synthesis; rejects [X07, pp. 11–14](../books/X07.md#deliberate-rejection-of-deceptive-controls))*.
- Make error explanations actionable, and match undo or review to how reversible the action is. [X10, pp. 25–26](../books/X10.md#usability-task-structure-and-recovery)

## DON'T

*(synthesis)*

- Do not show a first-use empty state when data failed to load; show the failure.
- Do not hide an essential error in collapsed metadata.
- Do not show success while a request is pending, or a spinner with no status.
- Do not offer a retry that duplicates user work or discards a draft.
- Do not add fake waiting to imply personalization or live computation. [X07, pp. 15–17](../books/X07.md#reject-invented-effort-and-certainty)

## Guidelines and example

Secondary metadata can expand on demand; information needed to decide or recover stays visible. [M06, pp. 105–106, 121–122](../books/M06.md#content-and-interface-states)

In chat, a failed response leaves the user's question intact, says no reply was obtained and offers retry for that turn. A new conversation offers starting prompts instead. Test retry and conversation switching while a response is in progress.

## Persistence is distinct from delivery

Model draft editing, pending save, completed persistence, failed save and external delivery as separate states where those capabilities exist. Show "Saving…" only while saving and "Saved" only once the data is durable. Define the real destination and the interruption/retry behavior. [U09, pp. 161–162](../books/U09.md#content-management-needs-state-persistence-and-recovery)

For a chatbot prototype, state its actual storage boundary and that responses are simulated; label a tab-only message as local. A failed response keeps the question for retry, and a failed draft save gets its own recovery *(synthesis)*.
