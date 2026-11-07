---
name: design-pro
description: Design distinctive, brief-led Mobile and Web Apps interfaces with source-backed creative judgment, task-focused commands, intent discovery and verified prototypes or implementation.
---

# design-pro

Choose Mobile, Web Apps, or shared guidance from the request. `web` selects Web Apps, including public-facing pages. For native mobile versus mobile web, use the stated platform; clarify only if the difference changes the work. For mixed platforms, share the intent and distinguish the interactions.

## Default visual direction

For both modes, default to an open, continuous composition. Establish hierarchy with whitespace, alignment, and type size/weight. This is the user's visual preference; an explicit project direction or established product contract can call for another treatment.

Avoid routinely enclosing controls, icons or content in outlines, cards, pills, separator bars or nested surfaces. Add a boundary, fill or elevation only when it clarifies a meaningful unit, action, state or layer. Preserve discoverable controls, usable targets, visible focus, errors and selection. Before delivery, inspect the whole composition for repeated frames and fragmented grouping; simplify the structure rather than merely fading border colors.

This grouping preference does not prescribe one palette, font genre, mood or layout for every product. Bold color, expressive type, unusual imagery or dense composition may be appropriate to the brief.

## Creative judgment

For a new visual direction, substantial identity/composition work, or interchangeable-looking designs, load [creative judgment](references/creative-judgment.md), then the needed lens in [creative design](references/concepts/creative-design.md). Book citations and reading limits live in the separate [reading notes](references/creative-sources.md). Study observable relationships in book interiors, develop ideas from the project's subject, choose a direction against the brief, then critique and revise rendered work. Take responsibility for the creative recommendation when the user delegates it. Retain the brief's content, primary task and interaction requirements throughout. Do not reduce creativity to a style menu, random combinations or extra effects, or claim that reading retrains the model. Small corrections retain the existing direction.

## Commands

Accept `design-pro` and `$design-pro` equivalently in conversation. These are not shell commands. Natural-language requests may also activate the skill. For a task command, load [command routing](references/commands/index.md), [execution](references/execution.md), the selected command and applicable mode only.

```text
$design-pro <command> [web|mobile] "target, outcome and constraints" [--review] [--platform ios|android|mobile-web]
```

| Input | Action |
| --- | --- |
| `design-pro help` or `help <command>` | Explain commands, effect boundaries and both modes; use the [tutorial](references/tutorial.md) for worked examples. |
| `design-pro init mobile` | Gather only the missing consequential context, then produce a Mobile brief. |
| `design-pro init web` | Gather only the missing consequential context, then produce a Web Apps brief. |
| `design-pro context` | Show or reconcile the current project brief and decisions. |
| `design-pro query "mobile spacing"` | Answer the concept directly with DOs, DON'Ts, guidelines and citations. |
| `diagnose` / `compose` / `unframe` / `craft` | Explain causes; arrange content; remove redundant frames; refine component roles/states. |
| `identity` / `journey` / `recover` / `fit` | Connect product character; complete a task; handle failure/ownership; adapt conditions of use. |
| `reconcile` / `compare` / `prove` / `resolve` | Repair drift; compare distinct options; check claims with evidence; finish a scoped correction. |

`diagnose` and `prove` report without source changes; `compare` keeps alternatives isolated. Improvement commands honor `--review` without target edits. Infer mode from real context when unambiguous; resolve a material native/mobile-web mismatch before acting. For unknown commands/options, explain the relevant syntax before mutation. For a missing query concept or init mode, ask for that input without starting an unrelated workflow.

## Discovery and context

Read [discovery.md](references/discovery.md) for init or a context-dependent design request. Use the conversation and permitted project material first; do not repeat answered questions. Ask one focused question at a time only when its answer affects the design. A complete brief needs no interview. Label low-impact assumptions and preserve unresolved decisions that cannot safely be assumed.

Use [brief-template.md](references/brief-template.md) to summarize the necessary context without forcing empty fields. Keep project briefs outside this skill. When writing is authorized, save in the project and report the path. Across chats, load a saved brief before claiming continuity. For `context` with no available brief, say so; do not invent one.

Discovery is not implementation authorization. Respect the deliverable and the user's existing authorization; do not add approval gates already satisfied in the conversation.

## Concept queries

Load [concepts/index.md](references/concepts/index.md), then only the matching reference and relevant mode guidance. Resolve common synonyms. If mode is immaterial, answer shared guidance; clarify only when ambiguity changes the recommendation.

Return a short explanation of the applicable context, concrete DOs, DON'Ts with consequences, decision guidelines with exceptions, a small example if useful, and citations to supporting reference sections. Keep citations with the claims they support. Label synthesis and distinguish platform requirements from heuristics. Use exact titles/filenames from the linked source notes rather than reconstructing them from memory. Do not invent measurements or citations. For unsupported topics, state the knowledge gap and identify what evidence would be needed.

Query answers do not create designs or modify files.

## Design work

Load [shared.md](references/shared.md), then [mobile.md](references/mobile.md) or [web.md](references/web.md) as relevant. Inspect the existing product, instructions, reusable components and visual language first. Set the user task and success criteria before choosing screens or styling. For component shape, surface or visual-state work, load [component anatomy](references/concepts/component-anatomy.md). Map the main flow and relevant loading, empty, error, success and recovery states. Present consequential decisions, tradeoffs and change-appropriate verification.

Match the requested scope: advice, review, proposal, prototype or implementation. Identify simulated behavior. Keep research citations in companion design rationale, outside the product UI. Report what was actually observed versus assumed or untested.
