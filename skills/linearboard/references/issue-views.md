# Saved issue Views

Read this after an issue-creation command: `create-PRDs`, `create-issues-FE`, `create-issues-BE`, or an alias. Creating the matching View is part of the command output, not optional follow-up work. `debug` creates no Debug View; each BUG ticket reuses or creates the project's FE or BE View according to its actual Category. `create-designs` delivers local proposals and records the selected direction in native documents. It creates no issues or Views. Read-only planning/reviews and pre-approval mockup studies/captures do not create Views. After full design-set approval, the Design-ticket stage of `create-visuals` creates or reuses the Design View. Do not recreate a legacy Design View as a prerequisite for documents or images. Preserve existing UserStories Views as historical navigation; the merged milestone command does not require creating or repairing one.

## View mapping

| Command | Category child filter | Default saved View name |
| --- | --- | --- |
| create-milestones and story aliases | None — document entries only | No new View |
| create-PRDs | ProductRequirement | {Project}-PRDs |
| create-visuals, after full design-set approval | Design | {Project}-Designs |
| create-issues-FE | FrontEnd | {Project}-FE |
| create-issues-BE | BackEnd | {Project}-BE |

Reuse a semantically matching existing View even if its established name differs; do not rename it without authorization or create duplicates on repeat invocations.

## Filters, placement and verification

- Discover current accessible Views with pagination before creating anything. Metadata alone may not expose filters: inspect actual matching issues and visible saved filter controls.
- Resolve the project's exact ID and the team's active Category child. Combine **Project equals resolved project AND label includes that exact Category child**. Do not filter by title prefix, Coder alone, or the Category container.
- Default category Views span all project milestones and statuses, so future issues appear and completed records remain discoverable. Do not accidentally inherit Active/Backlog or current milestone restrictions. A user-requested milestone-specific View may add the native milestone condition and include that milestone in its name.
- Use the supported application Views API: project_id plus exact category, placement tabs by default or shared when requested, group_by status unless established otherwise. There is no separate team Views page or SaaS customView filter. Read [application operations](linearboard-operations.md) for payloads.
- Reload the actual application View and verify its visible placement and filters. Read complete members with `linearboard_get {kind:"views",id,members:true}` and compare project/category membership and grouped counts.
- Build an expected issue-ID set from the command's intended outputs before filtering by category, including reused and user-authorized restored records. Verify that every expected ID is in the saved View; comparing the View only with a category-filtered query can hide the same missing-category defect in both results. If a record is absent, inspect its category and the saved filters, repair only within authorized scope, and repeat the membership check.
- Return the saved View URL and actual count. Report a concrete View blocker separately while retaining successfully created issues; do not duplicate issues to fix a View or change their labels/status just to match an incorrect filter.
