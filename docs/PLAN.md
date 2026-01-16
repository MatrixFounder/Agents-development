# Implementation Plan - Skill Audit & Path Standards

## Goal Description
1.  Ensure all Skill definitions have valid YAML.
2.  Refactor `docs/PLAN.md` to use relative paths.
3.  Enforce "Relative Paths Only" rule in System Prompts and Documentation Standards.
4.  **Create Localization Sync Rule.**

## User Review Required
None.

## Proposed Changes

### 1. Skill Audit & Fixes (Completed)
- Fixed YAML in `core-principles`, `code-review-checklist`, etc.

### 2. Artifact Standards (Completed)
- Updated `documentation-standards` and `06_agent_planner`.
- Refactored `docs/PLAN.md`.

### 3. Localization Sync Rule
#### [NEW] [.agent/rules/localization-sync.md](.agent/rules/localization-sync.md)
- Create a new rule file.
- Content: "Mandatory Synchronization: Changes in `System/Agents` must be mirrored in `Translations`."

## Verification Plan
- **YAML Check:** Verify all skills start with valid YAML.
- **Link Check:** Verify links in `docs/PLAN.md` work (in IDE) and are relative.
- **Rule Check:** Verify creation of `.agent/rules/localization-sync.md`.
