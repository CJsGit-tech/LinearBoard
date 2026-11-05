# Story → PRD traceability

Use this operation during `create-PRDs` verification and authorized metadata reconciliation. The canonical chain is **milestone document story entry → PRD issue → that story group's native milestone**. Source IDs are opaque stable strings, not numbers inferred from issue keys or list position. Native relations apply only to real legacy story issues; document entries are linked by their document URL and stable section ID. New M/US labels are unnecessary. Preserve existing labels and legacy links.

## Canonical indexes

`create-milestones` places one JSON block in its native milestone overview Project Document. It is a compact identity/grouping index alongside the readable grouped stories, not a separate database or local artifact:

```json
{"schema":"linearboard-story-index-v1","stories":[{"id":"US-01","milestone_id":"<native milestone ID>","anchor":"us-01"}]}
```

Each anchor has an explicit `<a id="us-01"></a>` beside its readable story heading. Include `legacy_issue_id` only for a verified existing UserStory issue in the same project/milestone. Preserve established story prefixes and IDs on reruns. Renderer fragment navigation must be checked in the actual UI; if unsupported, the source link still names the stable story ID and owning document, and no working deep-link claim is made.

Each new PRD contains one provenance block, plus readable links to all its source story entries:

```json
{"schema":"linearboard-prd-sources-v1","document_id":"<native milestone document ID>","story_ids":["US-01"]}
```

All source stories in one PRD belong to the same native milestone. If a proposed PRD crosses milestones, split it into milestone-scoped PRDs or resolve the grouping explicitly before creation. Do not choose a primary milestone arbitrarily. Existing cross-milestone/legacy PRDs without this index are reported for an authorized migration; never guess provenance from titles or labels.

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
