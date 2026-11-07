# Mobile mode

Use this with the shared guidance. Establish native app versus mobile web when it changes navigation, components or verification. The reviewed historical examples do not establish current native platform rules.

## Context and touch

Ask about the actual setting instead of assuming every phone user is moving or every tablet user is at home. Account for interruptions, constrained attention and task resumption where relevant; these are design-pro applications of contextual research. [M02, pp. 13–18](books/M02.md#research-selection)

Give important adjacent actions enough actual activation area and separation to avoid accidental selections. Inspect the interactive region, not only the icon's drawn size. [M01, p. 15](books/M01.md#useful-guidance)

For mobile web, distinguish the [WCAG target minimum and its exceptions](current-accessibility.md#target-size) from a comfortable control size. For native work, check the current platform guidance and existing components before stating pt/dp requirements. CSS pixels, native points and density-independent pixels are not interchangeable labels.

## Reading and grouping

Choose type for the user and script; do not compress an entire desktop composition into a phone. Allow wrapping and user enlargement. Use spacing to distinguish a paragraph, message or new task step, while keeping related information close. [T01, pp. 6–17, 22–26](books/T01.md#decisions-worth-retaining)

For conversation screens, proximity can associate message and sender without a separate panel around each turn. Attach relevant status and recovery to the affected message; this latter behavior is design-pro synthesis rather than a source requirement. [M03, p. 19](books/M03.md#principles-and-applications)

## Navigation and adaptation

Choose [navigation](concepts/navigation.md) by frequency and task: expose primary actions, retain useful position on returning from details, and make secondary surfaces understandable to open and close. [M06, pp. 24–25, 53–79](books/M06.md#navigation-and-continuity)

Use complex gestures as shortcuts alongside a usable route, and distinguish their start, continuation and end. Familiar motions can have different meanings across apps; signifiers and context matter. [M04, pp. 15–21](books/M04.md#gestures)

Preserve the main task and useful context as information expands or the available space changes. The map detail and summary/detail examples illustrate this relationship, but do not prescribe a particular modern native sheet API. [M03, pp. 21–22, 30](books/M03.md#visual-examples)

For cross-device or resized work, load [responsive structure and continuity](concepts/responsive-and-continuity.md). A changed layout should not silently discard the draft or change which task is available. For first use, choose [onboarding](concepts/onboarding.md) proportionate to the first useful action rather than requiring a tour. [X14, pp. 64–69, 148–154](books/X14.md)

**Design-pro implementation considerations:** use the actual platform's established navigation and back behavior; inspect keyboard occlusion, safe areas, text-size changes, orientation, larger-device layouts and restoration after interruptions. Request permissions at the relevant task when needed and explain denial recovery. These are checks to resolve with the chosen platform and product, not claims sourced to a historical flat-design book. Verify current platform specifics before supplying numerical or API requirements.

Permission denial is explicitly considered in [M05, p. 76](books/M05.md#platform-implementation-chapters), and contextual requests appear on p. 119. Accessible names, state, nonvisual information and assistive-technology operation are addressed on [pp. 218–225](books/M05.md#accessibility-and-independent-use). Use actual platform APIs and test the result; a native-looking custom control is not automatically accessible.

For mobile web and tablets, preserve user zoom, avoid hover-only access and evaluate both available dimensions and input methods. The historical instruction to disable page zoom is deliberately rejected. [M08, pp. 13–20](books/M08.md#rejected-and-dated-guidance)

For [notifications](concepts/notifications.md), establish the event's value before permission, respect refusal and measure fatigue as well as clicks. Do not import the old browser-support matrix or notification marketing benchmarks as current facts. [M07, pp. 18–24](books/M07.md)

## Verification focus

For small interactions, define trigger, actual state change, user feedback and repeated-use behavior. Keep pending, failed and completed results distinguishable; the state distinction is design-pro synthesis. Avoid making every repeated operation a decorative animation. [M04, pp. 83–91](books/M04.md#microinteractions-and-feedback)

Exercise the primary flow and a failure/recovery path at a narrow width with realistic text. For a chat prototype, check long text, draft retention, response progress, retry, conversation switching and the composer when the keyboard appears. A desktop browser with a narrow viewport does not prove physical-device keyboard or native accessibility behavior. [M02, pp. 21–28](books/M02.md#research-selection) supports task-based evaluation; the specific chat cases are design-pro applications.
