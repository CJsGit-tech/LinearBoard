# Personalization and customization

Personalization adapts an experience from signals; customization lets the person choose preferences explicitly. Use either for a concrete task benefit. [X14, pp. 70–80](../books/X14.md#personalization-must-have-a-useful-correctable-purpose)

## DO

- State what becomes easier, such as a relevant suggestion or less repeated input.
- Use only signals relevant to that benefit, and keep explicit choices, observations and inferred preferences distinct.
- Make consequential suggestions understandable and correctable, with a usable fallback when a guess is wrong.
- Evaluate task outcomes and unwanted effects as well as recommendation clicks *(synthesis; qualifies [X14, pp. 75–93](../books/X14.md))*.

## DON'T

- Do not read purchases, browsing, age, gender or job title as certain evidence of motive.
- Do not collect every available signal, or take continued use as consent to unrelated assumptions.
- Do not say simulated chat replies learn preferences, or add a recommendation engine to a simple local demo.
- Do not rank explicit customization below passive "magic". [X14, pp. 72–87](../books/X14.md)

## Guidelines and example

First ask whether adaptation improves the task enough to justify its complexity and data use. Explain a recommendation's basis where useful and let people correct it. [X14, pp. 87–93](../books/X14.md)

For a chatbot, "Short replies" can be an explicit preference with a predictable effect; offer it as a control instead of inferring it. In a local prototype, document where the preference is stored and what is simulated. Check native permission rules, current privacy law and production model behavior against their own current sources.
