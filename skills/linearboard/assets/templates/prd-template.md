# PRD issue template

Authoring guidance for a native LinearBoard PRD issue, not a local product deliverable. Title `[Stable PRD ID] — [User task or capability]`; preserve established IDs when revising.

Begin the purpose section with one visible **Source stories:** line. Link each exact stable story ID to its milestone-document URL and explicit anchor, for example `**Source stories:** [US-01](<document-url>#us-01)`. Put only declared source stories on that line. Keep machine schemas out of issue descriptions. Apply the native milestone, its stable M-number tag and each mapped source-story tag. Reuse active team labels (for example, M1 and US1 for US-01); resolve ambiguous mappings before writing. Preserve unrelated labels. Native Related links apply only to actual legacy issue sources. New PRDs start in Backlog. Metadata belongs in native fields; readable source links may be a short opening line. For an explicitly selected legacy PRD Project Document, preserve that representation and skip issue-only metadata.

Keep the body to the five sections below by default; adapt when an actual product need justifies it. Do not add placeholders, forced length quotas or duplicated shared policy. Necessary evidence, goals and success context belong in purpose/scope or acceptance; useful decision history belongs in native PRD comments/revisions.

## 1. Purpose and scope

Who needs this task, the desired outcome and its known evidence or source stories. State what this PRD includes and the nearby responsibilities it excludes or delegates. Distinguish confirmed facts from proposals. Link milestone-wide platform, storage, privacy and completion constraints instead of copying them.

## 2. User flow

A short end-to-end flow from entry to completion. Include meaningful alternatives; explain user-visible state transitions without reproducing every rule. Reference other task PRDs at the handoff.

## 3. Product rules

Atomic, current requirements with stable IDs, rationale/evidence when needed, and clear source-story document entry or explicit user-decision provenance. Define each rule once in its primary owner. Reference another PRD's canonical rule rather than copy its text. Preserve imported stable IDs or record old-to-new mappings when merging or splitting existing requirements.

## 4. Acceptance

Unchecked observable outcomes tied to the current requirements and applicable story criteria. Cover success and relevant empty/error/cancel/retry/permission/persistence cases. Group redundant scenarios without losing distinct behaviors or thresholds. Refer to shared milestone checks where applicable; do not copy a long global test checklist into every issue. Record success metrics only when supported; distinguish product evidence from a release/verification gate.

## 5. Dependencies and follow-up

Links to source stories when not already listed, owning PRDs for shared rules, the milestone document, and any relevant historical decision source. Keep consequential unresolved product decisions visible, separately from design and engineering work or unverified capabilities. Include concrete evidence links when available; do not invent owners, dates, estimates or test completion.

A settled PRD contains the final behavior and short relevant boundaries. Record each confirmed answer as a native comment on its owning PRD issue and verify it by reading the comment back; do not create a separate QA report. Preserve existing historical QA documents when present.
