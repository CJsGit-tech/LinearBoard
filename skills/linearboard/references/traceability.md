# Story → PRD traceability

Use this operation during `create-PRDs` verification and authorized metadata reconciliation. The canonical chain is **milestone document story entry → PRD issue → that story group's native milestone**. Source IDs are opaque stable strings, not numbers inferred from issue keys or list position. Native relations apply only to real legacy story issues; document entries are linked by their document URL and stable section ID. Apply the native milestone, its stable M-number tag and each mapped source-story tag. Reuse active team labels (for example, M1 and US1 for US-01); resolve ambiguous mappings before writing. Preserve unrelated labels. Preserve existing labels and legacy links.

## Story groups and PRD sources

Read each story from its M-numbered section, the section’s native milestone link, and the explicit anchor immediately before its story heading. Preserve the story IDs across edits. Include a verified legacy issue link directly in the story when applicable. Older documents may retain their historical index. New documents require no index.

Begin the purpose section with one visible **Source stories:** line. Link each exact stable story ID to its milestone-document URL and explicit anchor, for example `**Source stories:** [US-01](<document-url>#us-01)`. Put only declared source stories on that line. Keep machine schemas out of issue descriptions. Historical PRDs with the older fenced source record remain readable.

All source stories in one PRD belong to the same native milestone. If a proposed PRD crosses milestones, split it into milestone-scoped PRDs or resolve the grouping explicitly before creation. Do not choose a primary milestone arbitrarily. Existing cross-milestone/legacy PRDs without verifiable source links or historical metadata are reported for an authorized migration; never guess provenance from titles or labels.

## Audit and bounded repair

Use the application's existing preflight first (`operate.py linearboard_capabilities`). The helper checks destination identity, accepts only loopback HTTP origins, and does not start another service, create a local mirror, or create missing source records.

```sh
python3 <skill-folder>/scripts/traceability.py --project-id <exact-project-id>
python3 <skill-folder>/scripts/traceability.py --project-id <exact-project-id> --issue-id <exact-prd-id>
```

Audit is read-only and follows every result page. Explicit issue selection is optional for audit and mandatory for apply. Only run apply when the current user request authorizes the reported metadata repair scope; a review or audit request never authorizes repair:

```sh
python3 <skill-folder>/scripts/traceability.py --project-id <exact-project-id> --issue-id <exact-prd-id> --apply
```

The helper derives the native milestone from the selected source group and adds missing reciprocal Related relations only for verified indexed legacy story issues. It never creates stories, issues, documents, labels or Views; never removes relations; never changes body, status, approval or other source/product content. Missing human-readable source links are warnings requiring a separately authorized content edit, not silently rewritten text. `--issue-id` takes the native record ID, not its display identifier.

Malformed/duplicate indexes, unknown stories, cross-project records, cross-milestone selections, invalid legacy mappings and source/issue changes block that target. Other explicitly selected independent targets can still be reported or repaired. Fresh record/version reads, expected-version updates, deterministic idempotency keys and readback protect retries. Retain successful repairs after a later failure; rerun audit, then apply only remaining authorized changes. Output goes to stdout and is not a saved PM record. Record accepted findings in LinearBoard when authorized.

The service has no atomic multi-record source-version guard: rereading immediately before each write detects observed concurrent changes, but cannot eliminate the final read/write interval. If competing edits are active, defer repair until they settle rather than treating this helper as a transaction. Review meaningful source/grouping changes before applying derived metadata repairs.

Exit codes: `0` consistent metadata without warnings; `1` drift, warning or blocked target; `2` invocation/transport failure outside individual target checks. `repaired` means only listed metadata repairs passed readback; it does not imply product approval or implementation.

Run offline tests without a live service:

```sh
python3 <skill-folder>/scripts/test_traceability.py
```
