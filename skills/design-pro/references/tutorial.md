# design-pro 使用教學

`design-pro` 是在 Codex 對話中使用的技能。它會依任務讀取指令、Web／Mobile 規則與相關來源，再做判斷、修改或驗證。下列文字貼到對話框，不是在 Terminal 執行的指令，也不代表另外註冊了 `/unframe` 等 slash command。

## 快速開始

先開啟目標專案，或提供可存取的檔案／網址與目標畫面。已提供過的背景不必重寫。

```text
$design-pro help
$design-pro help recover
```

不知道問題出在哪裡，先檢視：

```text
$design-pro diagnose web "遊戲首頁，請找出最影響理解與操作的問題，先不要改"
```

已知道要改善什麼，可以直接請它完成：

```text
$design-pro resolve mobile "聊天首頁太割裂，請直接改善，保留功能、配色與草稿" --platform mobile-web
```

只想看方案時加上 `--review`：

```text
$design-pro unframe web "首頁導覽與玩法切換" --review
```

## 模式與語法

```text
$design-pro <指令> [web|mobile] "目標、希望改善什麼、需要保留什麼" [--review] [--platform ios|android|mobile-web]
```

`web` 是瀏覽器應用，也包含公開宣傳頁。`mobile` 是以手機產品體驗為目標，再區分 iOS、Android 或 Mobile Web。Web 的窄版不會自動變成原生 Mobile App。模式可從實際專案判斷時會沿用；平台與檔案類型矛盾、且會影響正確作法時，才詢問一個關鍵問題。

`--review` 表示不修改目標程式、專案 brief、技能或設定。`--platform` 只有在需要區分 Mobile 平台時才填；也可以用自然語言寫「這是 SwiftUI iOS 專案」。選項放在引號外，查詢中的文字不會被當成選項。

## 選擇指令

| 指令 | 適合的問題 | 會交付什麼 |
| --- | --- | --- |
| `diagnose` | 覺得不對，但不知道原因 | 有位置與證據的診斷、優先處理項目；不改程式 |
| `compose` | 內容齊全，主次與排列不清楚 | 任務導向的資訊分組、構圖與畫面驗證 |
| `unframe` | 外框、卡片、膠囊把畫面切碎 | 移除冗餘包裝，以留白與排版保留分組 |
| `craft` | 元件造型或操作狀態不成熟 | 符合角色的元件及適用狀態檢查 |
| `identity` | 介面缺少產品自己的個性 | 從產品目的形成連貫的字體、色彩、圖像與語氣 |
| `journey` | 畫面之間的任務接不起來 | 任務／狀態圖、銜接修正與完整操作路徑 |
| `recover` | 失敗、中斷、晚到的結果造成混亂 | 操作歸屬、輸入保留、取消與重試的修正及證據 |
| `fit` | 尺寸、內容或輸入方式改變就不好用 | 保留主任務的適配與已檢查條件 |
| `reconcile` | 不同頁面越改越不一致 | 區分刻意變體與意外漂移，再做必要修正 |
| `compare` | 不知道哪一種設計安排比較適合 | 獨立的不同方案、相同條件下的比較及取捨 |
| `prove` | 想確認「改好了」的證據 | 已證實、失敗、未驗證的主張對照；不偷偷修正 |
| `resolve` | 希望描述問題後處理到完成 | 選擇必要工作、完成授權修正並驗證結果 |

詳盡的範圍與完成條件見 [指令索引](commands/index.md)。小修改不會強迫執行全部 12 個指令，也不會固定產生三套方案。

## 教學一：改善遊戲宣傳頁的連續感

假設你已開啟遊戲頁專案，希望保留插畫、品牌與功能。

```text
$design-pro unframe web "遊戲首頁：移除多餘導覽膠囊、箭頭圓底與區塊框線，保留玩法選取和上市提醒功能"
```

預期工作是判斷每個邊界的用途、移除冗餘包裝，並用留白、對齊和字級保留關係。資料表格的必要邊界、操作中的焦點及錯誤提示不會被一律刪除。

接著檢查這次修改的主張：

```text
$design-pro prove web "確認首頁在窄版不溢出，鍵盤可切換玩法、開啟與關閉上市提醒，錯誤提示仍清楚"
```

`prove` 應回報實際觀察與未驗證項目；若找到問題，再用具體修正要求或 `resolve` 處理。

## 教學二：聊天失敗、重試與對話切換

```text
$design-pro journey mobile "輸入草稿、切到新對話，再從紀錄回來；保留原本草稿與焦點" --platform mobile-web
```

它會檢查任務銜接、返回路徑和資料保留。針對非同步失敗，可再聚焦：

```text
$design-pro recover mobile "等待回覆時切換對話，晚到的結果必須回到原對話；失敗後重試不能多新增一則使用者訊息" --platform mobile-web
```

這裡要追查的是請求與對話的歸屬、完成時間點、輸入保留及重試行為。外觀調整不能取代對這些行為的驗證。實際服務的重試保證，需要依服務本身的實作確認。

## 教學三：空間適配與元件細節

```text
$design-pro fit mobile "聊天輸入框在短可用高度仍可操作，多行草稿不可把傳送鍵推到畫面外" --platform mobile-web
$design-pro craft mobile "讓傳送鍵的可用、等待與停用狀態清楚，維持可用操作範圍" --platform mobile-web
```

瀏覽器縮放／改變視窗尺寸能提供版面證據。真實手機鍵盤、IME、原生安全區域或輔助科技，要在相符環境測試；缺少環境時應明確說明。

## 教學四：比較方案，保留已確認方向

```text
$design-pro compare web "比較兩種玩法介紹安排：保留相同內容、插畫與操作，用相同螢幕寬度呈現"
```

候選方案應測試不同安排假設，不能只換顏色就宣稱是不同方向。它們保持獨立；選定方案或明確授權採用後，才修改主要版本。`identity` 針對產品辨識度，`reconcile` 則修正既有規則下的意外漂移，不會把所有有用途的變體硬做成一樣。

## 讓模型負責創意判斷

已有 brief 時，可以直接委託它研究、發展並選擇方向，不必先替模型指定「極簡風」等風格：

```text
$design-pro identity web "依既有 brief 發展有辨識度的構圖與視覺主題，由你研究並推薦方向。保留必要資訊、主要操作、留白與少外框的偏好。書籍參考須有 GitHub 可下載 PDF，請核對內文，不要只列書單。"
$design-pro identity mobile "保留聊天任務、紙色與森林色，從未完成的想法發展視覺語言；請用空白、輸入中和失敗重試狀態檢查這個方向。" --platform mobile-web
$design-pro query "art direction 與 design sense"
```

它應從看過的內頁提取關係，轉成與專案內容有關的構想，作出選擇，再檢視實際畫面並修正。可在構圖、字體、造型或敘事中表達創意，不會把每個專案套成同一風格，也不會把「少外框」解讀為只能用米色、綠色與柔和字體。來源與閱讀範圍見 [創意閱讀筆記](creative-sources.md)。這是可重用的設計脈絡與工作方法，不表示模型權重已重新訓練。

## 把創意問題交給對應指令

創意方法已接進下列七個既有指令；整體仍為原來的 12 個任務指令。

| 你想改善什麼 | 指令 | 新增的判斷 |
| --- | --- | --- |
| 沒有屬於產品的視覺想法 | `identity` | 由 brief 的題材、動作與關係發展概念，再連接造型、圖像與排版 |
| 內容齊全但畫面平淡 | `compose` | 檢查視覺重量、主次、不同跨度與疏密節奏 |
| 想讓元件有個性 | `craft` | 分開考慮造型層、文字、操作範圍與狀態；也可能保留簡單元件 |
| 覺得千篇一律，想知道原因 | `diagnose` | 指出具體視覺關係與題材連結的缺口；只診斷 |
| 已有不同構想，想選方向 | `compare` | 在相同內容與尺寸下比較表現方式、構圖及取捨；候選獨立 |
| 想確認「更有特色」的依據 | `prove` | 檢查可見差異、brief 與實際操作；不把主觀喜好當成成效 |
| 希望由模型決定怎麼改到完成 | `resolve` | 先分辨缺概念、構圖弱或元件問題，再選必要方法並驗證 |

例如：

```text
$design-pro compose web "內容與功能保留，改善目前每段都一樣的節奏。請用構圖與比例建立特色，不增加卡片。"
$design-pro craft web "主要按鈕可有符合主題的造型，但文字保持清楚，focus、等待、失敗、完成與操作範圍都要保留。"
$design-pro diagnose mobile "請指出這個 App 為什麼像通用模板，區分合理的熟悉操作與缺乏產品特色；先不要改。" --platform mobile-web
```

想先了解方法可直接查詢，會回覆 DOs、DON'Ts、guidelines、例外及書籍頁碼引用：

```text
$design-pro query "concept development"
$design-pro query "visual tension"
$design-pro query "expressive shape"
$design-pro query "mobile unique design taste"
```

查詢不會修改專案；`--review`、`diagnose`、`prove` 的範圍不因加入創意方法而放寬。來源引用仍留在參考筆記或設計理由，不進入產品文案。

## 初始背景、既有決策與概念查詢

```text
$design-pro init web
$design-pro init mobile
$design-pro context
$design-pro query "mobile spacing"
$design-pro query "component styling"
```

`init` 只補問會改變設計的資訊，產出專案 brief；它不代表開始實作。`context` 核對已載入的專案背景。`query` 回答適用情境、DOs、DON'Ts、guidelines、例外及來源引用，不會修改檔案。

來源留在支援參考或設計理由中，不會塞進產品畫面。會區分書中內容、design-pro 的綜合判斷、你的偏好與目前平台要求。

## 預設視覺方向

Web 與 Mobile 都優先用留白、對齊、字級與字重建立層次。外框、卡片、膠囊、分隔線與巢狀底色須有明確用途；焦點、選取、錯誤與必要操作提示要清楚。已確認的專案方向或既有產品規則可以要求不同處理。

## 結果應該怎麼讀

一次改善會交代改了什麼、原因、實際檢查與未驗證範圍。截圖、程式檢查、瀏覽器操作、原生測試與使用者研究是不同證據。教學中的例子是預期行為；交付的 demo 驗證報告另外記錄本次實際執行結果。

若只說「全面通過」而沒有對應範圍，可用 `prove` 指定主張。只有截圖時也可用 `diagnose`，但不能據此確認點擊、儲存或網路行為。

## 找不到技能或指令

先用 `$design-pro help` 明確指定技能。這些任務詞不需要另外安裝 shell 程式或建立十二個獨立技能。Codex 官方文件說明技能使用 `$` 指定，並會自動偵測檔案更新；沒有出現時再重新啟動。此安裝的使用者全域位置是 `~/.agents/skills/design-pro`，目前 `~/.codex/skills/design-pro` 是指向它的相容連結。[使用技能](https://learn.chatgpt.com/docs/skills-and-plugins)、[建立與載入技能](https://learn.chatgpt.com/docs/build-skills)。
