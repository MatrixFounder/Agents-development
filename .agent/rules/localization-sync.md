---
name: localization-sync
description: "Mandatory synchronization rule: Changes in System/Agents must be reflected in Translations/."
---

# Localization Synchronization Rule

## Context
The project supports multiple languages (currently English and Russian).
- **English (Primary):** Located in `System/Agents` and `.agent/skills`.
- **Russian:** Located in `Translations/RU`.

## The Rule
**ANY change made to the primary English prompts (`System/Agents`) MUST be immediately mirrored in the corresponding Russian prompts (`Translations/RU/Agents`).**

### Scope
1.  **System Agents:** If you modify `System/Agents/02_analyst_prompt.md`, you MUST check and update `Translations/RU/Agents/02_analyst_prompt.md`.
2.  **Skills:** If you modify `.agent/skills/[skill]/SKILL.md` logic, you MUST check if a Russian version exists (future scope) or ensure the translation files are updated.

### Execution Process
1.  **Modify English File:** Apply changes to `System/Agents/...`.
2.  **Identify Counterpart:** Locate the corresponding file in `Translations/RU/...`.
3.  **Translate & Apply:** Translate the specific change (instruction, rule, checklist item) and apply it to the Russian file.
4.  **Verify:** Ensure both files enforce the same process logic, even if the language differs.

## Criticality
Failure to synchronize leads to "Process Drift," where the Russian version of the agent behaves differently (often poorly) compared to the updated English version. This is **FORBIDDEN**.
