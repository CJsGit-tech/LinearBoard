# Requirement identity and optional legacy labels

New user stories live in the native milestone document with stable story IDs and explicit anchors. PRDs identify their source document/story IDs and carry the matching native milestone. Use [traceability](traceability.md) for deterministic validation and bounded metadata repair.

M/US labels are optional query aids, not identity. Do not require creating them in the new document-story flow. Preserve existing labels and unrelated metadata. For explicitly requested legacy label maintenance, derive M tokens only from an established native milestone mapping and US numbers only from actual stable story IDs; never use list order or application issue keys. Resolve ambiguous mappings rather than inventing suffixes, renaming shared labels or changing lifecycle.

Category remains required for actual issues: ProductRequirement, Design, FrontEnd or BackEnd as appropriate. Existing UserStory issues retain their category and history; new milestones do not create them. A label does not replace a native milestone or source reference.
