# PocketStocks delivery exception

Read this reference only after the resolved LinearBoard project is PocketStocks and the authorized dispatch or debug scope contains user-visible UI work. These rules supplement, but do not expand, the selected issue scope.

## Execution target

PocketStocks frontend work uses the existing AppDeploy app. Explicit issue-scoped `dispatch`, or an implementation-scoped `debug` after its exact FIX issue IDs are resolved, authorizes building and deploying only that bounded issue scope after calling `get_deploy_instructions`. The same plan, scope, verification and destructive-action gates apply. Neither command authorizes unrelated deployment, ticket changes or scope expansion. Do not create a local replacement frontend, fixture application or build output.

The worker must wait for terminal deployment status, inspect AppDeploy QA/runtime results and report the deployed environment/version. Default review viewports are 1366 x 768 and 1440 x 900 unless the issue or approved reference specifies otherwise; mobile checks are not implied.

## Independent UI review

After the worker reports completion, the TPM must operate the deployed AppDeploy UI, inspect the affected routes and required states, and compare it with canonical story behavior and approved visuals. A worker screenshot, deployment status, backend response, passing build or static inspection does not replace this review.

Return material discrepancies for focused remediation and repeat affected checks after a new worker report. Unresolved product defects remain active or blocked. Apply the shared review-handoff policy only after the deployed UI is reviewable.

When discrepancies are resolved:

1. Capture final screenshots from the deployed UI using supported controls.
2. Create and inspect a collaboration-ready JPG; source PNGs are temporary intermediates.
3. Attach only the JPG to the exact implementation issue and render it inline under `UI design screenshots`.
4. Add dated evidence identifying AppDeploy environment/version, routes, session/data scenario, viewports and states, canonical references, resolved discrepancies, checks, limitations and review conclusion.
5. Retrieve the issue and verify the rendered image, attachment, comment and state.

These screenshots are implementation QA evidence, not a new canonical design.

## Authentication and safety

Use credentials only when the authorized test requires authentication, project instructions permit it and the matching credential is safely available. Read it in memory and sign in through the normal UI. Never expose the value in chat, commands, logs, screenshots, LinearBoard, source changes or reports; do not inspect or reveal it merely to confirm entry.

Credential availability does not authorize deletion, credential changes or bypassing tool restrictions. Use explicitly disposable records for destructive live tests and obtain any confirmation required by the irreversible action. Record unsupported or untested steps accurately.
