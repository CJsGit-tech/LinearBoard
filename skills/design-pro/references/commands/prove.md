# prove — 以證據檢查完成主張

## Responsibility

What evidence supports the claim that this change works?

Read the [shared execution contract](../execution.md) and the applicable mode.

## Execute

Derive checks from the requested outcome and the actual changed behavior. Inspect the rendered target and exercise the affected main path plus relevant failure/return/input conditions. Distinguish code inspection, screenshots, automated checks, browser behavior, native tests and representative-user research. Inspect required artifacts rather than accepting a manifest or self-reported pass. Report observed failures and missing evidence; do not silently change source under this review command. Avoid broad repeated testing once the relevant checks pass without new concerns.

## Creative application

For a claim of greater creativity or stronger identity, use [critique and selection](../concepts/creative-design.md#critique-and-selection). Inspect the actual concept-to-form relationship and relevant comparison: distinct spatial organization, connected motifs, legible contrast, and preserved brief/task/state requirements. A cited book or a differently colored screenshot alone does not substantiate the claim.

Report visible formal differences as observations and their suitability as design judgments. Attention, preference, recognition and conversion remain unproven without evidence of matching scope. Include a contradictory observation when the motif disappears at narrow width, a required fact is missing or the expressive control no longer works. Keep this command read-only even if the correction seems obvious.

## Platform focus

- **Web:** gather actual browser evidence for affected layouts, focus/navigation and state changes.
- **Mobile:** use the appropriate native runtime or mobile-web browser and name exactly which physical keyboard/IME/device/assistive behaviors remain untested.

## Deliver and finish

a claim-to-evidence record with supported, failed and unverified outcomes.

Completion: every requested completion claim is bounded by evidence of matching scope. This is not a universal production-readiness certificate.

## Example

```text
$design-pro prove mobile "Confirm the send/retry and conversation-switch behavior after the chat update"
```

## Supporting design references

Load only the concepts needed for this target; follow their citations for source evidence. Command procedures are design-pro synthesis, not instructions attributed to a book.

- [research](../concepts/research.md)
- [accessibility](../concepts/accessibility.md)
- [prototyping](../concepts/prototyping.md)
