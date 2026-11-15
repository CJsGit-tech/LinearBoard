# Mobile mode

Use this with the shared guidance. Establish native app versus mobile web when it changes navigation, components or verification. Take native platform rules from current platform guidance; the book examples here are historical.

## Context and touch

Ask about the actual setting: who is using the device, where, and with how much attention. Account for interruptions, constrained attention and task resumption where relevant *(synthesis)*. [M02, pp. 13–18](books/M02.md#research-selection)

Give important adjacent actions enough activation area and separation to avoid accidental selection. Inspect the interactive region as well as the icon's drawn size. [M01, p. 15](books/M01.md#useful-guidance)

For mobile web, apply the [WCAG target minimum and its exceptions](current-accessibility.md#target-size) as a floor and size controls for comfort above it. For native work, check current platform guidance and existing components before stating pt/dp values. CSS pixels, native points and density-independent pixels are different units.

## Reading and grouping

Choose type for the user and script, and recompose for the phone instead of compressing a desktop layout. Allow wrapping and user enlargement. Use spacing to mark a paragraph, message or new task step while keeping related information close. [T01, pp. 6–17, 22–26](books/T01.md#decisions-worth-retaining)

On conversation screens, associate message and sender by proximity without a panel around each turn. Attach status and recovery to the affected message *(synthesis)*. [M03, p. 19](books/M03.md#principles-and-applications)

## Navigation and adaptation

Choose [navigation](concepts/navigation.md) by frequency and task: expose primary actions, keep position on return from details, and make secondary surfaces clear to open and close. [M06, pp. 24–25, 53–79](books/M06.md#navigation-and-continuity)

Offer complex gestures as shortcuts beside a usable route, and make their start, continuation and end distinct. Add a signifier where a familiar motion has an app-specific meaning. [M04, pp. 15–21](books/M04.md#gestures)

Keep the main task and useful context in place as information expands or space changes. Pick the native sheet or detail component from the current platform. [M03, pp. 21–22, 30](books/M03.md#visual-examples)

For cross-device or resized work, load [responsive structure and continuity](concepts/responsive-and-continuity.md); a layout change keeps the draft and the available task. For first use, size [onboarding](concepts/onboarding.md) to the first useful action. [X14, pp. 64–69, 148–154](books/X14.md)

**Implementation** *(synthesis)*:

- Use the platform's established navigation and back behavior.
- Inspect keyboard occlusion, safe areas, text-size changes, orientation, larger-device layouts and restoration after interruption.
- Request each permission at the task that needs it and design the path after denial. [M05, pp. 76, 119](books/M05.md#platform-implementation-chapters)
- Expose names, state and nonvisual information through the platform's accessibility APIs and test the result with them. [M05, pp. 218–225](books/M05.md#accessibility-and-independent-use)
- Verify current platform specifics before giving numerical or API requirements.

For mobile web and tablets, keep user zoom enabled, give required content a route that works without hover, and evaluate both dimensions and all input methods. [M08, pp. 13–20](books/M08.md#rejected-and-dated-guidance)

For [notifications](concepts/notifications.md), establish the event's value before asking permission, respect refusal, and measure fatigue as well as clicks. Take browser support and benchmarks from current sources. [M07, pp. 18–24](books/M07.md)

## Verification focus

For small interactions, define trigger, actual state change, user feedback and repeated-use behavior. Keep pending, failed and completed results visibly distinct *(synthesis)*. Reserve animation for operations where it explains something. [M04, pp. 83–91](books/M04.md#microinteractions-and-feedback)

Exercise the primary flow and one failure/recovery path at a narrow width with realistic text. For a chat prototype, check long text, draft retention, response progress, retry, conversation switching and the composer with the keyboard open *(synthesis)*. [M02, pp. 21–28](books/M02.md#research-selection)

Report a narrow desktop browser as layout evidence. Name physical-device keyboard, native behavior and assistive-technology behavior as untested unless they were exercised on the device.
