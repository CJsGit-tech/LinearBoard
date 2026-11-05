# Create FE and BE delivery issues

Use for `create-issues-FE <Project> <Milestone>`, `create-issues-BE <Project> <Milestone>` and existing FE aliases. These commands create or revise tickets and their category Views; they do not implement, dispatch, assign people, schedule work, or approve untested behavior.

## Sources and scope

- Resolve the exact team, project and native milestone, then search the complete issue set for duplicates. Reuse matching delivery tickets on repeat invocations.
- Read current grouped story entries and acceptance criteria, owning PRDs, milestone constraints, design overview/screen specifications and exact approved visual versions. Preserve source issue IDs, history, labels, statuses and relations. Reconcile an already confirmed decision into its owner only when synchronization is authorized; do not invent new product rules.
- Perform the internal technology lookup and selection below for the requested FE or BE scope. Read an existing Technical Baseline when available; a missing standalone technical document does not prevent creating scoped research/implementation tickets.
- Approved static visuals can be sufficient inputs when the user chooses to skip a clickable prototype. Do not require a Design issue, another prototype or repeated approval; check exact-scope recorded design approval and accessible image versions using [the visual approval gates](create-visuals.md#design-approval-and-native-attachment-state); report the native attachment field separately and ask only for genuinely missing evidence or upload access. Runtime behavior, keyboard, accessibility and services still require actual implementation evidence.
- FE covers native or web UI and interaction. BE covers the confirmed backend/data/service scope, including app-local persistence only when the product sources define it. Do not infer a server, account, cloud synchronization or other infrastructure merely from the `BackEnd` category.

## Internal technology lookup and selection

This work is included in `create-issues-FE` and `create-issues-BE`, not exposed as a separate user command. Do not send the user to run a technical-baseline step before creating tickets.

1. Inspect applicable `AGENTS.md`, the relevant implementation, configuration and pinned dependencies, plus existing technical references. Distinguish implemented facts, confirmed planned choices and unverified candidates; record missing access or evidence instead of guessing versions or reuse locations.
2. Reuse suitable existing code and dependencies. When a capability needs a different framework, SDK or API, research its primary official documentation and check compatibility with the actual platform, runtime and confirmed data/service boundaries. Documentation availability does not prove entitlement, account access or runtime success.
3. Record the selected approach, reason, source paths or official links, constraints and remaining verification in the owning ticket's **Technical investigation and decisions** section. Routine compatible engineering choices belong to the agent; choices that change confirmed product behavior or approved visuals return to the user.
4. Assign shared contracts and unresolved experiments to one owning ticket and link consumers. Live integration, implementation and experiments requiring execution remain for authorized dispatch; issue creation alone does not authorize them or establish a passing result.

An existing Technical Baseline is an optional lookup reference. Technical findings and decisions go into the owning FE/BE tickets without requiring a new baseline document. When maintaining that document is also within the authorized scope, use the [Technical Baseline reference rules](requirements-chain.md#technical-baseline-reference) and its template; preserve existing records and avoid duplicate documents.

## Split and link

- Use one independently reviewable screen or coherent capability per ticket. Do not impose a fixed count or split every field/error into a separate ticket.
- FE titles follow the canonical design document's screen name, established visual version and outcome, replacing only the prefix with `Build UI Feature` or the appropriate revision prefix. BE titles use `Build BE Feature — {capability} — {outcome}`; omit a version unless one is established.
- Apply the resolved native milestone, preserve existing optional M/US labels, exactly one Category child (`FrontEnd` or `BackEnd`) and the single Coder-role label in the initial create call. Reuse or create missing active team-scoped labels without adding Designer.
- Keep issues standalone by default. Add native Related relations to applicable PRDs and actual legacy source issues; link grouped story document entries in the body, not as invented issue relations; link design documents/screen entries in the body because document links are not issue relations. Preserve existing legacy Design relations unless their removal is separately authorized, but do not create or require Design work tickets. Link the exact approved artifact with title/version and its canonical document attachment location; an expiring download URL alone is insufficient.
- Identify a single owning ticket for shared data models, stable identity, validation or a file format. Consumer tickets link that owner; do not independently select incompatible contracts. Reuse existing counterpart tickets. Creating FE alone does not authorize creating BE, or vice versa.
- Use native Blocked by/Blocks for real integration prerequisites, not merely Related or a sentence in the description. Do not send conflicting relation types for the same pair; keep source references in text when needed. Read back all relations and check for cycles. Research can proceed before an integration prerequisite is delivered.

## Human-readable ticket body

Use these sections, omitting empty or irrelevant material:

1. **Expected output**: tangible code/service/interface outputs near the top.
2. **Requirements and approved references**: primary User story, all affected stories, owning PRDs, applicable criteria, canonical design documents/screen entries and exact approved visuals.
3. **Implementation scope**: controls, transitions, data effects, errors, cancellation and recovery owned by this ticket. Link shared rules rather than copying complete PRDs.
4. **Technical investigation and decisions**: questions to research, owner boundaries, existing code/SDKs to inspect, and contracts to coordinate. Label candidates and unperformed experiments honestly.
5. **Dependencies and boundaries**: native prerequisite links, interfaces, non-goals and scope limits.
6. **Acceptance criteria**: observable outcomes covering applicable normal, loading, empty, error, retry, privacy and persistence cases.
7. **Verification and report-back**: focused checks and platform-required evidence; a report to TPM containing changes, decisions, sources/experiments, results and remaining limits. UI tickets include the existing actual-application review gate and a place for implementation screenshots, not reference images presented as test evidence.

Use unchecked task lists for outputs, actions and acceptance. Use ordinary bullets/prose for context and references. Preserve real requirement IDs; do not invent historical case IDs.

## Engineering decisions during later execution

The owning agent continues unresolved investigation from the ticket-creation lookup, using existing code, official SDK documentation and necessary small experiments within the dispatched scope. Record the choice, reason, alternatives where useful, evidence, limitations, contract and affected consumers in the owning LinearBoard ticket through the TPM. Do not turn future investigation into a claimed completed finding. Changes to confirmed product behavior or approved visuals return to the user; routine compatible engineering details do not require a new product interview. These creation commands do not themselves authorize agent dispatch.

## Finish

Leave new tickets in Backlog. Retrieve each to verify destination, milestone, Category/Coder labels and preserved optional M/US labels, source relations, exact visual references, acceptance and dependency direction. Preserve existing issue lifecycle unless a transition is separately in scope. Then create or reuse the corresponding saved View using [issue Views](issue-views.md), verify its full membership, and return ticket and View links. Do not claim implementation or tests passed from ticket creation.
