# Research and evidence

Select a method for the uncertainty, accounting for product stage, context and available resources. [M02, pp. 13–28](../books/M02.md#research-selection)

## DO

- Distinguish context/motivation from task performance and attitudes from observed behavior.
- Use early concepts to question underlying assumptions; use functional tasks to examine completion and recovery.
- Define success, error and abandonment before collecting metrics.
- Explain participant and environment limits when interpreting outcomes.
- Separate a recorded action from an inferred motive and an evaluative judgment. The source's descriptive/inferential/evaluative note model makes those differences explicit. [X09, pp. 36–40](../books/X09.md#interviewing-and-interpretation)

Sources: [M02, pp. 15–28, 32–35](../books/M02.md).

Choose card sorting for grouping questions, an expert review for candidate issues, contextual work for setting/workarounds, and task observation for completion/recovery. A persona summarizes research; it does not create evidence. Eye tracking indicates gaze, not comprehension by itself. These distinctions qualify the method gallery in [X09, pp. 43–49](../books/X09.md#select-research-for-its-output).

## DON'T

- Do not equate liking a mockup with completing a task.
- Do not infer that remote testing automatically reproduces natural context.
- Do not use historical vendor speed claims, prices, incentive amounts or sample rules as current universal advice.
- Do not claim a fictional user or model walkthrough represents real-user research.

See the source's [historical and sample limitations](../books/M02.md#exceptions-contradictions-and-historical-limits).

## Guidelines and example

For a game page, a task might ask someone to find release/platform information and explain the main action. For chat, ask them to recover a failed send. Observe the path and result before asking for impressions. These are design-pro applications; without recruited participants they remain test scenarios, not usability findings.

## Match the method to the claim

| Uncertainty | Useful method | Evidence limit |
| --- | --- | --- |
| Can someone complete/recover a task? | Observed usability task with relevant people | Record assistance and prototype limits; preference alone is insufficient. |
| Where would people expect content? | Card sort for grouping; tree test for findability | A text hierarchy does not validate the visual navigation. |
| Did usability change over versions? | Comparable benchmark tasks/measures | Keep conditions and participants comparable; a before/after change alone is not causal proof. |
| What happens across repeated use? | Longitudinal/diary work | Track missing entries, burden and self-report limits. |
| How does a task span devices? | One journey across touchpoints | Separate this from different groups attempting the same task on each device. |

Sources and qualifications: [X17, pp. 6–18](../books/X17.md). Quantitative/qualitative and attitudes/behavior are separate dimensions; each method should address the actual question. Neither sample size alone nor confident interpretation establishes validity.

Multivariate testing varies multiple elements/combinations; it is not defined by having three versions. Do not describe a model walkthrough, prototype preference exercise or local browser check as a production experiment. See the [source correction and primary definition](../books/X17.md#experiment-terminology-needs-correction).

For a task script, describe the goal without revealing the intended control: “Find a suitable gift” preserves route choice better than “Use search to find a gift.” State success and any help given. In reports, separate observation → consequence → possible explanation → proposed change; a repeated difficulty does not by itself prove its root cause. [X15, pp. 90–96](../books/X15.md#reports-should-preserve-observation-consequence-and-uncertainty)

## Walkthrough, observation and measurement

A cognitive walkthrough predicts whether the specified users would want an action's effect, notice its control, understand the mapping and recognize useful feedback. Start with a known correct sequence and sufficiently detailed design; record a failed assumption and continue examining later actions. Exploration to discover the sequence is preparation, and the resulting predictions are not actual user-test findings. [U06, PDF pp. 66–74](../books/U06.md#cognitive-walkthrough-a-predicted-first-use-path)

Independent heuristic reviews and task walkthroughs have different coverage gaps. One model running several perspectives is not several independent human evaluators. Do not promise a fixed percentage of problems found. Use an informal action sequence to expose prerequisites, memory/transcription effort and recovery before investing in detailed timing models; historical action times are not contemporary-device measurements. [U06, PDF pp. 74–95](../books/U06.md#action-analysis-and-heuristics-answer-different-questions)

In observed testing, use neutral prompts, record assistance and retain unexpected choices/prototype limits. Stop respectfully when needed; do not invent an equipment failure. Preserve an incomplete task's actual stopping condition and observed elapsed time rather than inventing a large time/error value. Think-aloud, recall and preference are evidence with limits, not complete explanations of motive or unaided timing. [U06, PDF pp. 97–116](../books/U06.md#usability-testing-assistance-and-participant-protection)

For quantitative claims, define the measure, sample, failure/missing-data treatment and uncertainty before interpreting differences. Do not copy U06's historical statistical recipes: the pooled-deviation expression is erroneous in the original image and ±2SE is not a universal confidence procedure. Focused NIST verification and its limits are in the [source correction](../books/U06.md#statistical-recipes-require-correction). This guidance is not an executed experiment or a guarantee of statistical power.
