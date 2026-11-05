# Technical Baseline document template

Use this template to create or revise one native LinearBoard **project document** that developers can use to find the system's application type, operating system, language, frameworks, SDKs, APIs, data contracts, and data/privacy/security boundaries. This file is a skill instruction, not a project deliverable; do not copy it into the repository.

Technology lookup and selection run internally during FE/BE issue creation. Use this template when maintaining a shared Technical Baseline is within the authorized scope; the document is an optional developer reference, not a separate user command or prerequisite. Keep technical investigation and choices in their owning tickets.

## Document title

`Technical Baseline — [Product] [Stage]`

Preserve the existing canonical title when revising an established Technical Baseline.

## Document body

```md
## Last reviewed

- [YYYY-MM-DDTHH:mm:ssZ] — [Short revision message]

## Purpose

This is the canonical developer reference for [Product] [Stage]. Use it to find the application type, operating system, language, frameworks, SDKs, APIs, storage, and service boundaries implemented in the product.

## App profile

| Topic | Value | Where defined |
| --- | --- | --- |
| App type | | |
| Operating system / runtime | | |
| Devices / environments | | |
| Language | | |
| Distribution | | |
| Application backend | | |

## Technology stack

| Framework / API / SDK | Why this | Responsibility | Constraints | Version / support | Where used | Official docs |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## APIs and data contracts

| API / service | Use case | Data sent / received | Contract or endpoint | Failure / fallback | Where used |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## Data, privacy, and security

| Topic | Approach | Constraint |
| --- | --- | --- |
| Data ownership and location | | |
| Saved-record freshness | | |
| External data sharing | | |
| Authentication and authorization | | |
| Location or other device permission | | |
| Secrets and configuration | | |
| Privacy disclosure or requirement | | |
```

## Authoring rules

- Add a new `Last reviewed` entry at the top for every substantive change. Keep prior entries and use the exact `- ISO-8601 UTC timestamp — short message` format.
- Ground each entry in current source, configuration, repository instructions, or approved product scope. Use `Not recorded` or `None` when that is the fact; never fill a field from assumption.
- In **Version / support**, record only a pinned/versioned configuration or supported runtime that the source actually establishes. Do not infer a compiler, SDK, or deployment version.
- In **Where used**, name the source module, target, route, or runtime owner that lets a developer locate the implementation.
- In **Official docs**, link directly to the relevant primary documentation when it is available.
- Do not include Related documents, user-story links, decision summaries, quality constraints, architecture-boundary prose, deferred decisions, change control, or a sources section.
