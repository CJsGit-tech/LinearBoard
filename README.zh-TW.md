# LinearBoard

[English](README.md) · [繁體中文](README.zh-TW.md)

獨立的個人產品交付工作區。React UI、Compose 管理的 PostgreSQL 資料庫、REST API 和 MCP stdio adapter；運作不需要 Linear 帳號。

## 介面語言

支援 English 與繁體中文。首次使用依瀏覽器語言選擇；可從側欄「語言」切換，選擇儲存在瀏覽器。切換保留目前畫面與未儲存表單；使用者輸入的專案名稱、文件、留言與自訂狀態不會翻譯。API 錯誤可用 `Accept-Language: en` 選擇英文，未指定時沿用中文。

## 啟動

正式服務使用下方 Docker Compose 啟動方式。以下為可選的 SQLite 開發模式，需要 Python 3.12+、Node.js 20+。從 GitHub clone 後先執行 `npm ci` 與 `npm run build` 產生 `web/dist/app.js`；沿用 esbuild，不另加開發伺服器。

```sh
npm ci
npm run build
python3 server.py
```

開啟 http://127.0.0.1:8765 。也可指定 `--port 9000 --db /absolute/path/workspace.sqlite3`。

初次啟動只建立 Personal workspace 團隊。從「建立專案」開始；不預填正式任務。`linearboard-guide.html` 保留為操作參考，不會執行裡面的範例。

- 任務：清單／看板、篩選、搜尋、編輯、父子任務、優先級、負責人、關聯與依賴。
- 文件：rich text／Markdown 編輯、專案與里程碑歸屬、留言與完整修訂。
- Views：專案 AND Category／標籤／狀態／里程碑，依狀態、Category、優先級或里程碑分組；支援分頁列和側邊位置。
- 附件：本機檔案或外部連結、畫面識別、版本與明確審閱標記。
- 交付：FE／BE 批次、checkpoint、派工計畫和回報、獨立驗證證據。
- 設定：團隊、單選標籤群組、垃圾桶、資料庫備份。

`C` 新增任務，`/` 搜尋；看板可拖曳變更狀態，也可用任務表單和鍵盤操作。表單使用明確的儲存按鈕。

## 資料與備份

正式資料存於 PostgreSQL named volume `linearboard_postgres_data`；附件 bytes、版本歷史、重試紀錄與垃圾桶同樣存在 PostgreSQL。localStorage 只保存目前專案與顯示偏好。

設定頁「下載資料庫備份」在 Compose 模式下載 PostgreSQL custom-format `linearboard.pgdump`。還原時使用 `pg_restore` 到新的空資料庫，核對後再切換；詳細操作見下方 Docker Compose 段落。

可選的 SQLite 開發模式預設使用 `data/linearboard.sqlite3`，在該模式下載的是 SQLite 備份。不要在服務執行中直接覆蓋資料庫，或只複製主檔而忽略 WAL。遷移前的 SQLite 是歷史備份，不會繼續同步 PostgreSQL 的新寫入。

垃圾桶保留原 ID 和歷史直到手動永久刪除。舊版的封存紀錄會分別移入垃圾桶；若紀錄有上層團隊或標籤群組，須先還原上層紀錄。刪除任務會包含子任務，刪除專案會包含其所屬紀錄；刪除前會列出影響，還原時不覆蓋後續改動。永久刪除會移除資料、修訂與本機附件，但既有備份仍可能包含這些資料。服務只監聽 loopback，設計供同機擁有者使用。`X-LinearBoard-Actor: user` 是本機人工操作標記，不是網路身份認證。

## REST 契約

`GET /api/capabilities` 是可讀取的資源欄位、16 個主要指令與別名契約。這是應用程式介面說明，不是開發 backlog 或驗證報告。

| 操作 | 路徑 |
| --- | --- |
| 分頁讀取 | `GET /api/{kind}?filters={URL-encoded JSON}&cursor=0&limit=100` |
| 讀取單筆 | `GET /api/{kind}/{id}`（issues 也接受 identifier） |
| 建立 | `POST /api/{kind}` |
| 修改 | `PATCH /api/{kind}/{id}` |
| 原始版本歷史 | `GET /api/history/{id}` |
| Saved View 實際成員 | `GET /api/views/{id}/members` |
| 附件內容 | `GET /api/files/{id}` |
| 一致性備份 | `GET /api/backup` |

`kind`：teams、projects、milestones、labels、issues、documents、views、comments、relations、attachments、batches、dispatches、evidence。

寫入使用 `Content-Type: application/json`。PATCH 必須帶目前的 `expected_version`；衝突回傳 409，不會覆蓋較新的資料。為每次邏輯寫入指定 `Idempotency-Key`；重試時重用相同 key 與相同 payload。相同 key 搭配不同 payload 會回傳 409。未指定 key 的一般建立不會自動把相同標題當成同一筆紀錄；工作流程應先搜尋並重用，再建立。

各紀錄包含 `url`（相對於目前服務的穩定 UI 連結），例如 `/#/issues/{id}`、`/#/documents/{id}` 和 `/#/views/{id}`。重新開啟 View 會恢復其專案、儲存的 AND 條件與分組。

類別是唯一 Category 子標籤；一般 M／US／Coder labels 與原生 milestone 分開。PRD-to-US 與 delivery-to-source 使用 `relations`，文件來源使用 Markdown record links。`blocks` 禁止循環與跨專案關係。派工只接受 FE／BE、每筆一張任務、最多三筆 active，並拒絕重複 active assignment。計畫和完成回報有必填檢查，但真實 readiness、產品驗證和授權仍由執行端負責；資料存在不代表驗收。

Automation 可建立 draft／evidence 附件，不能核准視覺或把 issue 轉為 Done；這兩項由使用者在 UI 操作。一般 metadata 修訂會保留 Done。附件上傳以 `content_base64` 提供，或使用 `external_url`，上限 15 MB。Markdown 經 DOMPurify 清理；只有辨識為 PNG/JPEG 的 bytes 會 inline，其餘以下載提供。

## MCP 與 linear-tpm 邊界

```json
{
  "mcpServers": {
    "linearboard": {
      "command": "python3",
      "args": [
        "/absolute/path/to/LinearBoard/mcp_server.py",
        "--url", "http://127.0.0.1:8765"
      ]
    }
  }
}
```

這是供支援 MCP 的客戶端手動設定的範例；本專案沒有變更 Codex 設定或已安裝的 skill。先啟動 HTTP App，再啟動 MCP。Adapter 使用 [MCP stdio 2024-11-05](https://modelcontextprotocol.io/specification/2024-11-05/basic/transports) 和 [tools protocol](https://modelcontextprotocol.io/specification/2024-11-05/server/tools)。

工具：

- `linearboard_capabilities {}`：取得欄位與指令 input/output 契約。
- `linearboard_list {kind, filters?, cursor?, limit?}`：完整分頁搜尋。
- `linearboard_get {kind, id, history?, members?}`：讀回資料／修訂／View 成員。
- `linearboard_create {kind, data, idempotency_key}`：建立紀錄。
- `linearboard_update {kind, id, data, idempotency_key}`：`data.expected_version` 必填。
- `linearboard_update_issue_statuses {issue_ids, expected_versions, status, idempotency_key}`：批次變更同一專案的任務狀態；所有版本都符合才整批寫入。相同狀態不新增修訂，工具仍不可代替使用者完成最終驗收。
- `linearboard_trash_list {}`、`linearboard_trash_impact {kind, ids}`：列出垃圾桶，或讀取刪除影響與 fingerprint。
- `linearboard_trash_move {kind, ids, fingerprint, idempotency_key}`、`linearboard_trash_restore {batch_id, idempotency_key}`：依已確認的影響移入與還原整批；永久清除由使用者透過介面操作。

必須區分三層：

1. **LinearBoard** 提供可持久化的紀錄、關聯、Views、附件、歷史與驗證資料。
2. **Codex／外部工具** 解讀 `planning`、產出產品文字、訪談、生成視覺與 gallery、選擇批次、執行 coding agents、實際操作待測產品並做獨立驗證。
3. **目的地轉接** 將 skill 的 Linear CRUD／document／View 操作改用上述 LinearBoard 工具。原 skill 的 Linear-only 規則和工具名稱不會因 UI 相似就自動改變；在該工作流程明確授權 LinearBoard 為紀錄目的地之前，不能將原 skill 的 Linear 寫入靜默重新導向本機。

使用新目的地時需在該次工作指示中明確指定：「這次工作以 LinearBoard 為正式紀錄目的地，沿用 linear-tpm 的流程、授權、追溯及審閱規則，透過 linearboard MCP 工具讀寫；不要寫入真實 Linear。」這是使用者可選的轉接指示，本 README 不會自行執行它。

沒有內建 AI、API key、遠端同步、imagegen 或 agent runner。`dispatches` 是真實的派工紀錄，不是假裝已執行的 worker。`create-visuals` 的圖片生成與 HTML gallery 由現有外部工具完成，核准後才能保存正式 reference。不能將這些外部工作標成 App 已執行。

## 開發與可重現檢查

```sh
npm run build
npm test
npm run test:ui
npm run test:selects
```

UI 測試使用本機已安裝的 Google Chrome。它會在 8766 啟動獨立服務，使用臨時 SQLite 資料庫，結束時刪除測試資料；不碰預設工作區或真實 Linear。`test:selects` 在 8780 使用獨立臨時資料庫，檢查深色選單、鍵盤、長選項、rich text 與原文保留。截圖暫存於 `/tmp/linearboard-*.png`。資料測試使用 unittest，涵蓋各指令所需的 record 操作契約；這與在 Codex 中逐條執行完整 skill 是不同的驗證。

團隊工作流可在「工作區設定 → 編輯團隊」以每行一個名稱編輯。預設為 Backlog、Todo、In Progress、In Review、Done、Canceled、Duplicate；snapshot 的 `statuses_by_team` 保留每團隊集合。仍被任務或 View 引用的狀態不可移除。舊資料缺少欄位時，保留實際引用的舊狀態，不默默重設進度。

REST list 的 list-valued 欄位可用 scalar 做 membership，或用 array 做有序的確切比對；例如 `filters={"issue_ids":["actual-issue-id"]}` 可重新找到原派工。

`linearboard.client.Client` 是隨附的 MCP stdio client，可用 context manager 管理連線；`ensure` 先完整分頁搜尋後重用，避免重跑建票。相同 Client 的 `update` 會快取原請求以安全重試。跨 process 重試須保存原 payload（含 `expected_version`）；沒有原請求時不猜測成功。`create` 重試可讀回同一 identity 的合法較新版本，`update` 回傳原操作 response，最新狀態請另用 `get`。

暖碳黑／米白主題使用系統字型、底線分頁與無框資訊欄。專案分頁在內容區頂端，分類 Views 與總覽／任務／文件共用同一列。搜尋與篩選從分頁右側開啟；`/` 可直接展開搜尋。專案資訊欄可收合，窄版預設收合。任務與文件可直接以 rich text 編輯，支援標題、粗體、斜體、清單、待辦項目、連結與復原／重做，並保留 Markdown 切換。儲存按鈕位於頂部工具列，不會自動儲存；既有 Markdown 在未編輯時保持原文，含 HTML 的內容保留原文編輯以免轉換遺失。所有選擇欄位共用深色選單，包含屬性、篩選、附件及設定。 側欄直接列出專案，點選可切換至該專案任務頁，並保留設定入口；整合與指令、操作指南從設定頁進入。任務詳情預設呈現狀態、類別、里程碑、標籤與關聯，優先級、負責人及上層任務可展開「其他屬性」編輯；收合不會清除值。分類 View 不重複列出相同類別 badge。

UI 的 Saved View 返回 context 存在瀏覽器 history.state，包含專案、View、搜尋、篩選及顯示模式；關閉詳情與 Escape 使用相同返回路徑，重新載入可恢復。它不取代 SQLite 正式資料。

明確切換頁面、專案、View 或重新開啟紀錄時，UI 會讀取工具寫入的最新內容與版本；不需要先整頁重新載入。已開啟的編輯器不會被背景寫入覆蓋，讀取失敗會顯示重試入口。這是明確導覽時的讀取，不是背景同步。

`/visuals/` 可提供本機 `output/visual-review/v1/` 的受限白名單視覺草稿 gallery；此可選產物不包含在公開 repository 或 Docker image。這是可審閱的非正式視覺 bundle，不能寫入管理紀錄或核准設計。使用者的確認、需求與工作流驗證結果保存在 App 原生紀錄，不在此 README 鏡像。

工程結構：

- `linearboard/store.py`：transaction、驗證、分頁、版本和歷史。
- `linearboard/contracts.py`：機器可讀的 adapter 契約。
- `server.py`：只監聽本機的 HTTP/API/static server。
- `mcp_server.py`：MCP stdio ↔ HTTP bridge。
- `linearboard/client.py`：具讀回、分頁、重用與精確重試的 MCP client。
- `web/app.jsx`：React root 與鍵盤入口；`web/workspace.jsx`：專案路徑、分頁、團隊／專案導覽與可收合資訊欄；`web/pages.jsx`、`web/forms.jsx`、`web/ui.jsx`：頁面、表單與共用元件。
- `web/editor.jsx`：Tiptap rich text 與 Markdown 編輯；`web/model.js`：API、導航與訂閱狀態，透過 React useSyncExternalStore 更新畫面；`web/labels.js`：顯示名稱；`web/style.css`：既有樣式。
- `tests/`：可丟棄 fixture 的資料層和瀏覽器檢查。

UI 使用 React／ReactDOM（MIT）、系統字型與 [Lucide React](https://lucide.dev/guide/lucide)（ISC）；Markdown 使用 [Marked](https://marked.js.org/)（MIT）搭配 [DOMPurify](https://github.com/cure53/DOMPurify)（Apache-2.0 選項）清理。選單使用 [Radix Primitives](https://www.radix-ui.com/primitives/docs/components/select)（MIT），rich text 使用 [Tiptap](https://tiptap.dev/docs/editor/markdown)（MIT），資料仍以 Markdown 儲存。打包使用 esbuild（MIT）；瀏覽器測試使用 Playwright（Apache-2.0）。確切版本與依賴鎖定於 package-lock.json。安裝時不需要遠端字型或圖像；打包後正常使用沒有 CDN 依賴。

產品需求、開發派工與正式驗收紀錄不在 repository 另建副本；測試 fixture 是可重現的應用程式測試資料。

## Docker Compose 與 PostgreSQL

正式本機服務現在由 `compose.yaml` 管理：`app` 提供 React／Python，`db` 使用 PostgreSQL 17，資料持久化在 Docker named volume `linearboard_postgres_data`。只將應用程式公開到 `127.0.0.1:8765`，資料庫沒有主機連接埠。密碼透過 `data/docker/database-password` 的 Compose secret 掛載；該目錄限制為擁有者存取，勿刪除或提交此檔。

```sh
python3 scripts/setup_compose.py
docker compose up -d --build
docker compose ps
docker compose logs --tail 100 app
docker compose stop
docker compose start
```

`docker compose down` 保留資料卷；不要使用 `down -v`，那會刪除資料庫資料卷。映像重建不會覆蓋資料。API 和 MCP URL 保持不變，`GET /api/health` 可確認使用 `postgresql`。

既有 SQLite 僅保留為遷移來源／回復備份。停止舊 Python 服務後，用 SQLite backup API 建立一致性備份，然後：

```sh
docker compose up -d db
docker compose run --rm migrate /source/<SQLite備份檔名>
docker compose up -d app
```

遷移包含 records、history、requests、blobs、counters、trash_batches；在單一交易中逐表比對列數與 SHA-256，保留 ID、歷史順序、附件 bytes、標籤關係、垃圾桶和重試紀錄。若目標非空且不同，會拒絕覆寫；完全相同的重跑不改動資料。遷移期間不要啟動 app 寫入目標。不要將 SQLite 原檔當作遷移後的最新資料。

「下載資料庫備份」在 PostgreSQL 模式下載 `linearboard.pgdump`（custom format），包含全部正式資料與附件。以 `pg_restore` 還原到新的空資料庫，核對後再切換連線；不應直接覆蓋運行中的資料庫。SQLite 開發／既有測試模式仍支援 `python3 server.py --db <檔案>`，不設定 `DATABASE_URL` 即使用 SQLite。正式 Compose 使用 `DATABASE_URL` 和 `DATABASE_PASSWORD_FILE`。

PostgreSQL 交易目前使用應用程式層級的 advisory lock，保留原 SQLite 的序列化驗證與寫入語意，避免同時請求破壞派工上限、版本檢查或刪除影響預覽。適合目前個人工作區；高併發擴充時可再細化鎖定。


## 隨附 LinearBoard skill

完整管理 skill 位於 [`skills/linearboard/SKILL.md`](skills/linearboard/SKILL.md)，包含 references、工作流範本、agents metadata 與 Python 操作工具。這些是可重用的 authoring instructions，不是任何專案的 PRD、backlog 或驗收資料。此 bundle 是發布時的副本，更新個人安裝版本不會自動同步到 repository。

在 Codex 中可將 `skills/linearboard/` 複製到 `~/.codex/skills/linearboard/`（先保留既有版本）；或直接指定此 repository 內的 `SKILL.md`。圖片生成命令另需執行環境提供 `imagegen` skill 與圖片工具；本 bundle 不包含 imagegen。skill 的相對 imagegen 連結預期採用 Codex skill 安裝目錄結構。

若 checkout 不在原始作者的路徑，請在使用 skill 自動啟動服務前設定：

```sh
export LINEARBOARD_PROJECT_DIR="/absolute/path/to/LinearBoard"
```

首次安裝請先依上方 Compose 指令建立本機 secret、build 並啟動服務；skill 的 preflight 只重用或啟動既有部署，不負責初次建立資料卷、遷移或重設密碼。使用 `--url` 或 `LINEARBOARD_URL` 可指定服務位址，另行管理的開發服務可使用 `--no-autostart`。

公開 repository 僅包含應用程式、測試與可重用 skill；`data/`、`output/`、資料庫備份、Compose 密碼、環境變數檔與相依套件均由 `.gitignore` 排除。產品管理紀錄持續保存在各使用者的 LinearBoard 資料庫中。
