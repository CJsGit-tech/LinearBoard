- `init <Project> [repository path]`
  - Set up project AGENTS.md and Codex specialists, preserve customization, and display each agent’s role and supported commands.

- `help`
  - 列出指令與用途。

- `planning`
  - Clarify the 4W1H vision and briefly check a user-chosen stack against official sources.

- `create-vision-document`
  - Create or revise the product vision from Planning.

- `create-technical-baseline <Project>`
  - Record shared technical requirements, feasibility findings and open decisions in one project document.

- `create-milestones`
  - 依願景建立成果或學習里程碑，在總覽文件記錄完成條件及適用的使用者故事。

- `create-PRDs <Project> <Milestone>`
  - Create and verify milestone PRDs and their saved View, then automatically ask clarification questions from those items and record confirmed answers.

- `create-designs <Project> <Milestone>`
  - Build three runnable React Native proposals from the Design Overview and record the selected style only after confirmation.

- `create-visuals <Project> <Milestone>`
  - Extend the selected direction in React Native, verify the scoped screens and states, and create Design tickets after complete-set approval.

- `create-issues-FE <Project> <Milestone>`
  - 建立或修訂前端開發 issues 與分類 View。

- `create-issues-BE <Project> <Milestone>`
  - 建立或修訂後端開發 issues 與分類 View。

- `organize-task-batch <Project> <Milestone> [issue IDs]`
  - 依相依性排列執行批次，為前後端議題加上 Batch N 標籤，並驗證篩選結果。

- `dispatch <Project> <Milestone> [Batch <n> | issue IDs]`
  - Dispatch a verified milestone batch or explicit issue IDs, sequence dependencies, and independently verify the results.

- `debug [Project] [Milestone] [report or issue IDs]`
  - Record, fix and verify a reported defect on its BUG ticket, then comment there with cause and action.

- `sync <Project> <Milestone> [scope or new request]`
  - Review affected records, propose from/to changes, and apply them after user approval.
