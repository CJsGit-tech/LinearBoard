# Command routing

Commands select a responsibility, not an automatic style filter. Read [execution](../execution.md), the selected command and the relevant mode; do not load every command or book.

## Usage

```text
$design-pro <command> [web|mobile] "target, desired outcome and preservation constraints"
```

Interpret these in conversation; there is no shell executable or registered slash-command parser. `--review` produces a proposal without target-source edits. `--platform ios|android|mobile-web` disambiguates Mobile only when needed. Interpret options outside quoted query/content. Ordinary natural-language constraints are equally valid.

Preserve `help`, `help <command>`, `init web|mobile`, `context` and `query "concept"`. `query "mobile spacing"` is a concept query, not an improvement invocation. Help explains effect boundaries, both modes and relevant examples; use the [tutorial](../tutorial.md) for a walkthrough. Unknown commands/options receive a brief correction before any mutation; suggest the closest responsibility without silently executing it.

## Choose the responsibility

| Command | Responsibility | Default effect |
| --- | --- | --- |
| [diagnose](diagnose.md) | 找出問題與原因 | Inspect and report |
| [compose](compose.md) | 建立內容與任務層次 | Scoped improvement; --review disables target edits |
| [unframe](unframe.md) | 解除多餘視覺分割 | Scoped improvement; --review disables target edits |
| [craft](craft.md) | 打磨元件造型與狀態 | Scoped improvement; --review disables target edits |
| [identity](identity.md) | 建立產品辨識度 | Scoped improvement; --review disables target edits |
| [journey](journey.md) | 接好跨畫面任務 | Scoped improvement; --review disables target edits |
| [recover](recover.md) | 處理失敗與中斷 | Scoped improvement; --review disables target edits |
| [fit](fit.md) | 適配使用條件 | Scoped improvement; --review disables target edits |
| [reconcile](reconcile.md) | 修正意外的設計漂移 | Scoped improvement; --review disables target edits |
| [compare](compare.md) | 比較不同設計假設 | Isolated alternatives; adoption requires selection/authority |
| [prove](prove.md) | 以證據檢查完成主張 | Inspect and report |
| [resolve](resolve.md) | 完成指定設計問題 | Scoped improvement; --review disables target edits |

## Distinguish nearby responsibilities

- `compose` changes information arrangement; `unframe` removes redundant enclosing structure while preserving meaningful grouping.
- `craft` works on component anatomy and states; `identity` connects product character across expressive choices.
- `journey` checks task completion across transitions; `recover` traces failure, operation ownership, commit and retry guarantees.
- `fit` changes conditions of use; `reconcile` repairs accidental divergence within the established product contract.
- `compare` clarifies a design decision; `prove` checks completion evidence; `diagnose` explains causes; `resolve` completes a scoped correction.

## Creative work with existing commands

Use `identity` to develop a content-derived visual idea; `compose` to translate it into spatial hierarchy; `craft` for expressive component anatomy. `diagnose` critiques the cause of sameness, `compare` evaluates distinct directions, `prove` checks formal/behavioral claims, and `resolve` chooses the necessary work for an authorized outcome. Their creative sections link to the matching lens in [creative design](../concepts/creative-design.md). There is no additional command family or style preset. `query "visual tension"`, `query "concept development"` and `query "expressive shape"` return cited guidance without implementation.

## Natural-language routing

Route by requested outcome. For a fragmented page use `unframe`; for unclear order use `compose`; for a late reply attached to the wrong conversation use `recover`; for a named problem to fix end-to-end use `resolve`. A request to explain what is wrong remains a diagnosis. Respect existing action authorization and --review. Do not turn every task into a multi-command pipeline or run prove as an excuse for a full unrelated audit.

For mixed tasks, preserve one outcome and edit boundary while using the needed responsibilities. If the platform conflicts with the target implementation (for example, --platform ios on a static HTML target), resolve the consequential target/platform conflict; do not silently migrate the application.
