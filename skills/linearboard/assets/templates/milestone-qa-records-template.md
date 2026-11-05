# Milestone QA records

Authoring guidance for the native Project Document `<Project> <Milestone>-工能釐清QA紀錄`; not a local product deliverable. QA means questions and answers, not test results.

## Document-wide format

Use headings plus bullet lists throughout the generated QA document, including context, PRD references, final-decision summaries, question options, revisions and requirement migration references. Do not use tables in this report. Group questions by topic and preserve actual question numbers when available; use unnumbered topic headings when original numbering was not retained. Do not copy a product-specific question count into another record.

Use the user's language for headings and field labels. The fields below may be expressed in natural Traditional Chinese, for example 範例、行為、優點、缺點、當時建議與理由、使用者回答（原文）、最終決策、決策修訂、狀態、對應 PRD. Do not publish empty scaffold placeholders.

## Context and reading notes

- Resolved project and milestone; record status (Incomplete / Product decisions complete); actual review date.
- Whether this is a live interview or a retrospective organization of existing material.
- Source PRD and milestone links, formatted as bullets; use nested bullets for responsibility and User Story mapping if needed.
- Which original details are available or missing. Missing historical evidence is distinct from an unresolved product decision.

## Current decisions

- Group the final rules by product topic and link their primary PRDs.
- Keep superseded choices in history, clearly separated from currently effective requirements.

## Question and answer history

Use one heading per actual question, retaining its original number when known. For a documented live question, use this order:

### Q<number> — <question>

- **Example:** the concrete scenario actually used, or identify it as a retrospective paraphrase.
- **Option A — <name>**
  - **Behavior:** the behavior proposed at the time.
  - **Advantages:** the benefits stated at the time.
  - **Disadvantages:** the tradeoffs stated at the time.
- **Option B — <name>**
  - **Behavior:** the behavior proposed at the time.
  - **Advantages:** the benefits stated at the time.
  - **Disadvantages:** the tradeoffs stated at the time.
- **Recommendation at the time:** option and actual rationale, explicitly not user approval.
- **Original user answer:** quote the available original answer accurately, including a free-form answer rather than forcing it into A/B. When only a summary survives, label it as a prior summary/paraphrase and do not present it as a quotation.
- **Final decision:** the currently accepted rule, or explicitly unanswered/not applicable.
- **Revision history:** nested bullets preserving the earlier answer, later correction, actual sequence/date when known, and which decision it supersedes. Keep the original answer visible rather than overwrite it with the final rule.
- **Status:** confirmed / deferred / superseded / not applicable, distinguishing an old answer's status from the current final decision.
- **PRD references and synchronization:** original source links, current primary owner when it changed, requirement IDs and verified/pending/failed update status when known.

Provide only choices and fields supported by the source. If examples, options, advantages, disadvantages or recommendations were not retained, state that explicitly instead of inventing plausible alternatives. A compact missing-detail bullet can replace unavailable fields; do not create fake A/B choices or repeat empty placeholder lists. Preserve the existing answer/decision summary alongside recovered original answers rather than silently replace the older record.

An unclear input followed by clarification is not an accepted choice. A recommendation is not a user answer. A question invalidated by a later scope revision is not applicable, not implicitly resolved by its recommended option.

## Remaining questions

- Unanswered product questions and affected PRDs.
- Confirmed answers still awaiting successful synchronization, separately identified.
- State explicitly when no product questions remain; do not turn missing historical options into new interview questions.

## Design and engineering follow-up

- Unverified capabilities, design details and implementation validation, separated from accepted product decisions.
- Findings that may require a later product tradeoff, without inventing approval.

## Decision archive and restructure traceability (when applicable)

- Retain moved decision entries and their original issue provenance before replacing source text. Preserve different answers and later corrections; only remove exact duplicates when their provenance is retained.
- For each moved or merged requirement, use a bullet for its original ID and nested bullets for the old issue, current owner/canonical rule or alias, and explicit not-applicable disposition where relevant.
- Link actual new issues once created. Current behavior remains readable in PRDs; common constraints remain in the milestone document.

## Evidence boundary

- This report records product decisions, not implementation, runtime verification, release approval or issue-state transitions.
- A format-only edit does not change the accepted rules, PRD states or record identity.
