# Initialize a Codex project

`init <Project> [repository path]` prepares local engineering instructions and
Codex agent definitions for a resolved project. It does not create a LinearBoard
project/document/issue, audit live records, install hooks, dispatch agents or
deploy. Handle its local setup before application preflight; use application
operations only if a separate project-identity lookup is actually necessary.

## Resolve the destination

Use the explicit project and repository or an already unambiguous selection in
this conversation. Quote multiword arguments when showing examples. Do not infer
the destination from cwd, an open browser, or a similarly named project. If the
project or engineering target is unclear, ask one focused question before local
writes or project-specific board access. A repository must already exist.

Initialization can run offline with an explicitly chosen project name. State
that the board binding is unverified and resolve the canonical team/project
before any later board operation. Do not invent an ID or create a container.

Read existing AGENTS.md files relevant to the selected directory, existing
`.codex/config.toml`, effective inherited agent settings, local/ancestor agent definitions and current project
conventions. Preserve application-specific rules and manual customization. A
multi-application repository needs an explicit target/mapping; never transplant
another project's AppDeploy IDs, styling or product rules into this setup.

## Prepare, inspect and apply

Use the bundled helper from the installed skill (Python 3.11 or newer; no
third-party Python packages):

```sh
python3 <skill>/scripts/init_project.py --project "<Project>" --repo "<repository path>" --json
```

The default is a dry run. It renders a managed workflow block in AGENTS.md,
creates missing supported agent roles, updates marker-owned instructions in
previously generated roles, and preserves existing custom roles/settings. It
does not overwrite a custom agent just because the filename differs. Existing
models, disabled-agent choices and concurrency limits are retained. New roles
inherit the parent's model/reasoning/permissions; the project workflow uses at
most three concurrent specialists and respects a lower configured limit.

Inspect the plan and all reused custom instructions. Resolve conflicts in
writing/approval ownership, application mapping, roles or stage permissions.
The helper checks file structure, not whether prose instructions are compatible.
Preservation is not proof of compatibility. Apply routine compatible setup
without another user confirmation; ask only for a material unresolved choice.
Do not force-enable explicitly disabled subagents. A new default configuration
does not set `agents.enabled`; inherited activation choices still apply.

After reviewing the exact plan, apply it with its hash:

```sh
python3 <skill>/scripts/init_project.py --project "<Project>" --repo "<repository path>" --apply --expect-plan <plan_sha256>
```

The helper refuses stale plans, ambiguous markers/project rebinding, invalid
TOML, duplicate role names, filename collisions and symlinked config paths.
It changes only AGENTS.md and the required `.codex` files; rerunning a consistent
setup leaves bytes/mtimes unchanged. On a partial I/O failure keep verified
completed files, inspect the reported remainder and re-plan; do not blindly
overwrite or delete successful work. Do not save the dry-run JSON as a project
status ledger.

## Required generated guidance

The reusable assets are `assets/init/AGENTS.template.md` and
`assets/init/agents.json`. Keep responsibilities and displayed command lists in
that shared registry. Generated guidance references the installed skill/router,
current templates and shared change-review method rather than duplicating them.

The main agent routes commands and coordinates sources, decisions, integration
and independent verification. Ordinary board writes remain with the main
agent; debug ownership follows the skill unless existing project instructions
explicitly require main-only writes. Preserve that distinction in the generated
roles instead of silently changing a repository's policy.

Explain when to use each stage, prerequisites and approval gates, bounded agent
ownership and acknowledgment/release, plus which checks each specialist performs.
Do not make delegation mandatory for simple tasks or let a supported-command
list authorize the next workflow stage.

Document impact review must trigger after PRD creation/revision, changed
clarification answers, requested scope/behavior changes and conflicts discovered
in design/delivery. Follow relevant native relations and document/story links,
then scoped wording searches to catch missing links. Identify exact affected
records/rules, confirmed versus proposed differences and needed acceptance or
dependency updates. Use [change review](change-review.md) as the single method.

Apply owning-record updates already authorized by the active command and verify
their body/comment readback. For edits outside that authority, suggest the
existing sync command with bounded record IDs/topic and concrete from/to
proposals; wait for approval of the presented edits. Do not revive a standalone
PRD clarification command, rewrite requirements to match code, or treat a
tentative answer as a confirmed rule. Pause dependent work only when needed.

Use current command templates and relevant existing traceability checks for
document structure/links. Initialization installs workflow guidance and local
configuration, not an automatic hook or new document-validation subsystem.
Executable validation, semantic review and proposed automation must be reported
separately. Never claim a live scan or enforceable check from prose alone.

## Verify and report

Read back every changed file, parse generated/reused TOML and verify managed
block boundaries and preserved custom content. Report disabled agents or
unresolved custom-role conflicts as limitations; do not claim complete readiness.
Use installed Codex discovery diagnostics when they expose actual role metadata;
otherwise state that dispatch/discovery is not tested and use a fresh project
chat to load the definitions. Do not make a model call just to test setup.

The user must receive the agent structure even when this is a repeat run or
machine-readable helper output was used. Show the main orchestrator separately,
then each configured specialist in this exact shape:

```text
<agent name>
- role: <one-sentence responsibility>
- commands: <supported LinearBoard commands>
```

Commands describe the stage responsibilities each agent supports; the main agent
still routes and owns the overall command. Include preserved extra custom agents;
if their command mapping is unknown, say it is not declared rather than inventing
ownership. Report the selected project/repository, created/updated/reused files,
checks actually performed and any unverified binding/activation. End with one
recommended next step using the root rule. For setup-only work, name opening a
fresh project chat as the immediate action. Name a later command only when the
scope and missing deliverable are already known.
