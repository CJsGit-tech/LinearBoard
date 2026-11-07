# Content states and recovery

Distinguish an empty collection, pending operation, completed result and failed operation. The specific state model is design-pro synthesis; historical sources support meaningful empty states and visible feedback. [M06, pp. 123–124, 131–132](../books/M06.md#content-and-interface-states); [M04, pp. 83–91](../books/M04.md#microinteractions-and-feedback)

## DO

- Explain why a view is empty and offer a relevant next step, as ticket/trip examples do. [M06, pp. 123–124](../books/M06.md)
- Connect progress to the action it represents and distinguish it from a finished result. [M04, pp. 83–91](../books/M04.md)
- Preserve useful work and provide a recovery action close to the affected operation. This is design-pro recovery guidance; see [forms and errors](forms-and-errors.md) for input-specific cases.
- Use undo only when the operation can actually be restored. [M06, pp. 47–48](../books/M06.md#input-and-action)
- Make Save/Refresh do what they imply and report accurate persistence/freshness. These are design-pro alternatives to the deceptive controls advocated in [X07, pp. 11–14](../books/X07.md#deliberate-rejection-of-deceptive-controls).
- Keep error explanation actionable and preserve meaningful undo/review according to reversibility. A book that favors undo also explicitly recognizes consequential exceptions. [X10, pp. 25–26](../books/X10.md#usability-task-structure-and-recovery)

## DON'T

- Do not show a first-use empty state when data failed to load.
- Do not hide an essential error in collapsed metadata to make a screen cleaner.
- Do not claim success while a request is pending, or add an endless decorative spinner without meaningful status.
- Do not offer retry that creates duplicate user work or silently discards a draft.
- Do not add fake waiting to imply expensive personalization or live AI computation. The historical Quora timing claim is unsupported in the source. [X07, pp. 15–17](../books/X07.md#reject-invented-effort-and-certainty)

The error/pending/retry distinctions are design-pro implementation decisions, not behaviors demonstrated by the sources' static screenshots.

## Guidelines and example

Secondary metadata can expand on demand, but information required to decide or recover should remain visible. [M06, pp. 105–106, 121–122](../books/M06.md#content-and-interface-states)

In chat, a failed response should leave the user's question intact, identify that a reply was not obtained, and provide retry for that turn. A new conversation instead offers useful starting prompts. Test retry and conversation switching during progress; neither a screenshot nor a simulated service proves live-model reliability.

## Persistence is distinct from delivery

Model draft editing, pending save, completed persistence, failed save and external delivery separately where those capabilities exist. Medium's historical **Saving...** header is a useful visible example of a pending operation, not evidence that data is already durable. Define the real destination and interruption/retry behavior; do not promise flawless autosave or a fake Save action. [U09, pp. 161–162](../books/U09.md#content-management-needs-state-persistence-and-recovery)

For a chatbot prototype, disclose its actual storage boundary and simulated response. If a message remains in the current tab only, do not label it cloud-synced. A failed response can retain the question for retry while a failed draft save may require different recovery. This distinction is design-pro application; the screenshots do not demonstrate a chatbot implementation.
