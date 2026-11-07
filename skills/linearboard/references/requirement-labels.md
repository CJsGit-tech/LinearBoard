# Requirement identity and tracking labels

New user stories live in the native milestone document with stable story IDs and explicit anchors. PRDs identify their source document/story IDs and carry the matching native milestone. Use [traceability](traceability.md) for deterministic validation and bounded metadata repair.

Apply the native milestone, its stable M-number tag and each mapped source-story tag. Reuse active team labels (for example, M1 and US1 for US-01); resolve ambiguous mappings before writing. Preserve unrelated labels. Derive M from the established milestone name and US from the stable source ID, never from list order or an issue key. For IDs outside the standard US-number convention, resolve the established mapping. Within authorized issue creation or label repair, create a missing label only after checking all active team labels. Document-only commands keep M-numbers visible in headings and leave issue labels alone.

Category remains required for actual issues: ProductRequirement, Design, FrontEnd or BackEnd as appropriate. Existing UserStory issues retain their category and history; new milestones do not create them. A label does not replace a native milestone or source reference.
