# Navigation, discovery and continuity

Navigation exposes the main task, preserves orientation and lets people return without losing context. Choose the pattern from the task and the available room. [M06, pp. 6–9, 58–79](../books/M06.md#navigation-and-continuity)

## DO

- Keep frequent actions accessible; place secondary options in a contextual overflow or drawer. [M06, pp. 24–25, 53–55, 71–73](../books/M06.md)
- Preserve selection and position on return from detail. [M06, pp. 58–59](../books/M06.md#navigation-and-continuity)
- Signal additional content and unfamiliar gestures where they occur; teach in context. [M08, p. 19](../books/M08.md#progressive-enhancement-and-navigation)
- Keep a usable route to each important action when hover or gestures are unavailable. [M08, p. 13](../books/M08.md#adapt-interaction-not-just-width); [M04, pp. 15–21](../books/M04.md#gestures)

## DON'T

*(synthesis; corrects [M06, pp. 38–44](../books/M06.md#contradictions-and-evidence-limits))*

- Do not hide the primary task to reduce visible controls.
- Do not give browsing and destructive actions similar gestures in the same context.
- Do not ship a drawer, overlay or sticky header without testing its keyboard and focus behavior.
- Do not drop useful content because its hover presentation fails on touch; give it another route.
- Do not hide a decision-critical action in an accordion or make a carousel the only route to necessary content. [X08, pp. 39–42](../books/X08.md#access-navigation-and-selection)

## Guidelines and example

Use persistent navigation when frequent switching justifies its screen cost, and check it does not cover content. For a contextual popover, decide whether it is modal and implement the matching focus and dismissal behavior. [M06, pp. 63–70](../books/M06.md#navigation-and-continuity)

If content moves or updates automatically, apply [current pause/stop/hide criteria](../current-accessibility.md#moving-and-auto-updating-content). [X08, p. 42](../books/X08.md#access-navigation-and-selection)

In a mobile chat app, a labeled conversations control opens a list, selecting a conversation returns to its saved transcript position, and closing the list returns to the prior task. On wider web layouts the list can stay visible *(synthesis)*.

## Thematic and persistent controls

A themed or spatial navigation surface still shows understandable destinations, current position and a return path. A fixed bar trades access for space; test it for obstruction, zoom and focus. Keyboard navigation is a first-class route. [W08, PDF pp. 102–133](../books/W08.md#motion-and-navigation)
