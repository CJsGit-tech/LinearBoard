"""Machine-readable adapter contracts, shipped as application capability metadata."""
CONTRACTS = [
    ('help', 'Installed command definitions', [], 'Capabilities and boundaries', 'Read /api/capabilities; no mutation'),
    ('planning', 'Idea and confirmed answers', [], 'Conversation; optional explicitly saved project document', 'No writes unless saving is requested'),
    ('create-vision-document', 'Resolved team/project and planning context', ['projects', 'documents'], 'Vision Project Document', 'Read back document and project_id'),
    ('create-milestones', 'Vision and outcome boundaries', ['milestones', 'documents'], 'Native milestones and overview document', 'Read milestone IDs, project ownership and overview'),
    ('create-userstories', 'Milestones and user outcomes', ['issues', 'labels', 'views'], 'Story issues, Category and saved View', 'Verify body, milestone, labels and View membership'),
    ('create-PRDs', 'Source story IDs and current decisions', ['issues', 'relations', 'labels', 'views'], 'PRD issues related to every source story', 'Verify native relations, M/US labels and View membership'),
    ('prd-demystify', 'Current PRDs and explicit user answers', ['issues', 'documents', 'comments'], 'Current PRD rules and preserved QA history', 'Re-read PRD revisions and QA original answers; unanswered stays unresolved'),
    ('create-designs', 'US/PRDs and confirmed decisions', ['documents', 'issues', 'relations', 'views'], 'Design overview, interaction specification, Design issues', 'Verify two linked documents, category, milestone and source links'),
    ('create-visuals', 'Design issues, direction and explicit image approvals', ['attachments', 'comments'], 'Versioned drafts and user-approved references', 'Open attachment, inspect approval/version; image generation and gallery are external'),
    ('create-issues-FE', 'Requirements, design and approved visual IDs', ['issues', 'relations', 'labels', 'views'], 'FrontEnd issues, Coder label and saved View', 'Verify Backlog, milestone, source links, all US labels and View membership'),
    ('create-issues-BE', 'Confirmed data/service scope and shared contracts', ['issues', 'relations', 'labels', 'views'], 'BackEnd issues and dependency ownership', 'Verify Backlog, contract owner, blockers and saved View'),
    ('organize-task-batch', 'Exact FE/BE IDs and dependencies', [], 'Read-only proposal in conversation', 'No mutation; optional explicitly saved batches preserve exact IDs/checkpoints'),
    ('dispatch', 'Exact authorized issue IDs, target and reviewed plan', ['dispatches', 'comments', 'issues', 'evidence'], 'Assignment, plan, report and independent verification', 'Record state, one issue per assignment, <=3 active, no duplicate assignment; agent execution external'),
    ('debug', 'Selected report batch and reproduction', ['documents', 'issues', 'comments', 'relations', 'views', 'evidence'], 'Bugs log, FIX issues and document result comments', 'Verify report text/history, FIX-to-report links, evidence and result comments; implementation external'),
    ('sync', 'Bounded scope and confirmed owner records', ['issues', 'documents', 'relations', 'views', 'labels'], 'Minimal reconciled records with history', 'Read versions, preserve Done/progress/history; reject stale writes and retry keys'),
    ('frd', 'Current stories and product rules', ['documents'], 'Linked FRD Project Document', 'Read document and its source issue links'),
]

def capabilities():
    return {
        'application': 'LinearBoard', 'api_version': 1,
        'resources': RESOURCE_FIELDS,
        'snapshot_fields': {'statuses':'default seven-state workflow for older clients', 'statuses_by_team':'mapping of team_id to ordered status-name arrays; use the selected project team'},
        'record_fields': {'id':'stable UUID', 'url':'relative application deep link; prepend running server origin', 'version':'integer; send as expected_version on PATCH', 'deleted_at':'trash time; deleted records are hidden from normal lists', 'created_at':'UTC ISO timestamp', 'updated_at':'UTC ISO timestamp'},
        'adapter': 'Native REST API + MCP stdio',
        'bulk_status': {'endpoint':'POST /api/issues/bulk-status', 'tool':'linearboard_update_issue_statuses', 'inputs':['issue_ids','expected_versions','status'], 'semantics':'Atomic; same project; all versions checked; unchanged status preserves history; Done requires user action'},
        'trash': {'preview':'linearboard_trash_impact', 'list':'linearboard_trash_list', 'move':'linearboard_trash_move', 'restore':'linearboard_trash_restore', 'purge':'Manual user action via UI', 'semantics':'Atomic impact-checked batches; descendant issues included; no automatic expiry'},
        'external': ['Codex command interpretation', 'Coding-agent execution', 'Image generation and review gallery', 'Independent product verification'],
        'commands': [dict(zip(['command', 'inputs', 'resources', 'outputs', 'verification'], item)) for item in CONTRACTS],
        'aliases': {'stories':'create-userstories', 'user-stories':'create-userstories', 'prd':'create-PRDs', 'create-prds':'create-PRDs', 'Prototype UI':'create-designs', 'Prototype UI Issues':'create-designs', 'Build UI':'create-issues-FE', 'Build UI Issues':'create-issues-FE', 'prototype-ui':'create-designs', 'prototype-ui-issues':'create-designs', 'build-ui':'create-issues-FE', 'build-ui-issues':'create-issues-FE', 'create-issues-fe':'create-issues-FE', 'create-issues-be':'create-issues-BE'},
        'verification': 'Capability contracts describe operations, not a claim that external orchestration has been tested.'
    }

# The adapter reads these contracts to construct payloads without guessing field names.
RESOURCE_FIELDS = {
    'teams': {'required':['name','key'], 'fields':{'name':'string','key':'2–10 uppercase alphanumeric characters','statuses':'nonempty unique array<string>; defaults to Backlog, Todo, In Progress, In Review, Done, Canceled, Duplicate; referenced states cannot be removed'}},
    'projects': {'required':['name','team_id'], 'fields':{'name':'string','team_id':'teams.id','body':'Markdown'}},
    'milestones': {'required':['name','project_id'], 'fields':{'name':'string','project_id':'projects.id','description':'string','target_date':'YYYY-MM-DD or empty; never invented'}},
    'labels': {'required':['name','team_id'], 'fields':{'name':'string','team_id':'teams.id','parent_id':'labels.id or null','is_group':'boolean','single_select':'boolean'}},
    'issues': {'required':['title','project_id'], 'fields':{'title':'string','project_id':'projects.id','milestone_id':'milestones.id or empty','category':'UserStory | ProductRequirement | Design | FrontEnd | BackEnd','status':'exact name from the project team workflow; defaults: Backlog | Todo | In Progress | In Review | Done | Canceled | Duplicate; Done requires user action','priority':'No priority | Urgent | High | Medium | Low','body':'Markdown','label_ids':'array<labels.id>; Category child automatically added on create','parent_id':'issues.id or empty','assignee':'string'}},
    'documents': {'required':['title','project_id'], 'fields':{'title':'string','project_id':'projects.id','milestone_id':'milestones.id or empty','doc_type':'Vision | Milestones | QA | Design overview | Screen specification | Bugs | FRD | Technical Baseline | Notes','body':'Markdown; link source records using their url'}},
    'views': {'required':['name','project_id'], 'fields':{'name':'string','project_id':'projects.id','category':'exact Category or empty','milestone_id':'milestones.id or empty','statuses':'array<exact project-team status names>; empty means all','label_ids':'array<labels.id>; AND membership','placement':'tabs | shared','group_by':'status | category | milestone_id | priority'}},
    'comments': {'required':['target_kind','target_id','body'], 'fields':{'target_kind':'issues | documents | projects','target_id':'target record id','body':'Markdown','author':'display name; not authentication'}},
    'relations': {'required':['source_id','target_id','relation'], 'fields':{'source_id':'issues.id','target_id':'issues.id','relation':'related | blocks | supersedes | duplicate'}},
    'attachments': {'required':['target_kind','target_id','name'], 'fields':{'target_kind':'issues | documents | projects','target_id':'target record id','name':'filename or title','content_base64':'base64 file bytes; max 15 MB; alternative to external_url','external_url':'http(s) URL; alternative to bytes','mime':'MIME type','screen':'screen identifier','visual_version':'e.g. v1','approval':'draft | evidence | approved | superseded; approved requires user'}},
    'batches': {'required':['name','project_id','issue_ids'], 'fields':{'name':'string','project_id':'projects.id','milestone_id':'milestones.id or empty','issue_ids':'distinct array<FE/BE issues.id>','rationale':'string','checkpoint':'observable outcome and scenario','dependencies':'prerequisites and blockers'}},
    'dispatches': {'required':['project_id','issue_ids'], 'fields':{'project_id':'projects.id','milestone_id':'milestones.id or empty','issue_ids':'exactly one FE/BE issue id','worker':'external agent/run identity','target':'actual repository/app target','scope':'authorized boundary and source versions','plan':'reviewed plan required before executing','state':'review | executing | completed | blocked | failed','report':'required when completed; a worker claim, not independent verification','verification':'TPM review results; do not invent'}},
    'evidence': {'required':['project_id','issue_id','criterion','environment','result'], 'fields':{'project_id':'projects.id','issue_id':'issues.id','criterion':'acceptance criterion','environment':'target, viewport, route and scenario','result':'Pass | Fail | Not tested | Environment-blocked','body':'actions, observed results, evidence links, limits and next check'}},
}
