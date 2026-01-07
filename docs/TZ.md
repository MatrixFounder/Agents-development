# TZ: Bilingual Synchronization Rules (Task 006)

## 1. Description
**Task:** Configure workspace rules to ensure synchronization between English and Russian documentation and agent prompts.
**Goal:** Maintain consistency between `README.md`/`README.ru.md` and `System/Agents`/`System/Agents_ru`.
**Source:** User Request.

## 2. Use Cases

### UC-01: Synchronize README
**Actor:** Agent (Developer/Orchestrator)
**Precondition:** User or Agent updates `README.md`.
**Scenario:**
1. Agent detects changes in `README.md`.
2. Agent applies corresponding semantic changes to `README.ru.md`.
**Postcondition:** Both README files carry the same information in respective languages.

### UC-02: Synchronize Agent Prompts
**Actor:** Agent (Developer/Orchestrator)
**Precondition:** User or Agent updates any file in `System/Agents`.
**Scenario:**
1. Agent detects changes in an agent prompt (e.g., `02_analyst_prompt.md`).
2. Agent locates the corresponding file in `System/Agents_ru`.
3. Agent applies corresponding semantic changes to the Russian file.
**Postcondition:** Agent behavior descriptions are consistent across languages.

## 3. Implementation Requirements
- **Rule Placement 1:** Rules must be added to `.cursorrules` as this is the "System Instructions" file for the agent in this workspace.
- **Rule Placement 2:** Rules must also be added to `.agent/rules` (create if doesn't exist).
- **Note on Gitignore:** The user requested adding these to `.gitignore`. This is technically incorrect as `.gitignore` is for file exclusion. The implementation will place them in `.cursorrules` and `.agent/rules` to ensure they are actionable by the AI.

## 4. Acceptance Criteria
- ✅ `.cursorrules` contains explicit instructions to sync `README.md` -> `README.ru.md`.
- ✅ `.cursorrules` contains explicit instructions to sync `System/Agents` -> `System/Agents_ru`.
- ✅ `.agent/rules` contains the corresponding rules file (e.g., `bilingual_sync.md`).
