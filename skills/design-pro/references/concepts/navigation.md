# Navigation, discovery and continuity

Navigation should expose the main task, preserve orientation and let people return without losing useful context. Choose a pattern for the task and available room, rather than copying a popular app. [M06, pp. 6–9, 58–79](../books/M06.md#navigation-and-continuity)

## DO

- Keep frequent actions accessible; place genuinely secondary options in a contextual overflow or drawer. [M06, pp. 24–25, 53–55, 71–73](../books/M06.md)
- Preserve relevant selection and position on return from detail. The source's Tinder example retains the selected photo. [M06, pp. 58–59](../books/M06.md#navigation-and-continuity)
- Signal additional content or unfamiliar gestures where needed; teach in context rather than requiring a long tutorial. [M08, p. 19](../books/M08.md#progressive-enhancement-and-navigation)
- Keep a usable route to an important action when hover or gestures are unavailable. [M08, p. 13](../books/M08.md#adapt-interaction-not-just-width); [M04, pp. 15–21](../books/M04.md#gestures)

## DON'T

- Do not hide the primary task just to reduce visible controls.
- Do not assign browsing and destructive actions confusingly similar gestures in the same context.
- Do not assume a familiar-looking drawer, overlay or sticky header has correct keyboard or focus behavior.
- Do not remove useful content merely because a hover presentation is unsuitable for touch.
- Do not hide a decision-critical action in an accordion or make a carousel the only route to necessary content. [X08, pp. 39–42](../books/X08.md#access-navigation-and-selection)

These are design-pro qualifications of the historical patterns, including the gesture-only claim rejected in [M06, pp. 38–44](../books/M06.md#contradictions-and-evidence-limits).

## Guidelines and example

Use persistent navigation when frequent switching justifies its screen cost; verify it does not obscure content. A contextual popover can retain the background task, but decide whether it is modal and implement its corresponding focus/dismissal behavior. The book's mixed examples do not prescribe one policy. [M06, pp. 63–70](../books/M06.md#navigation-and-continuity)

If content moves or updates automatically, check [current pause/stop/hide criteria](../current-accessibility.md#moving-and-auto-updating-content). A historical carousel's 5–7-second timing or hover-only pause is not a conformance rule. [X08, p. 42](../books/X08.md#access-navigation-and-selection)

In a mobile chat app, a labeled conversations control can open a list, selecting a conversation returns to its saved transcript position, and closing the list returns to the prior task. On wider web layouts the list may remain visible. This is a design-pro application to verify, not a platform-specific API requirement.

## Thematic and persistent controls

A themed or spatial navigation surface still needs understandable destinations, current position and a usable return path. A fixed bar trades access against occupied space; test obstruction, zoom and focus instead of making it compulsory. Historical screenshots illustrate options without verifying input behavior, and the source's claim that keyboard navigation is generally inferior is rejected. [W08, PDF pp. 102–133](../books/W08.md#motion-and-navigation)
