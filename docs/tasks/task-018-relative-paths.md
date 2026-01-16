### 0. Meta Information
- **Task ID:** 018
- **Slug:** relative-paths-enforcement
- **Status:** Completed

# TASK: Enforce Relative Paths in Prompts and Skills

## Goal
Ensure that `System/Agents/02_analyst_prompt.md`, `System/Agents/03_task_reviewer_prompt.md`, and all `skills` use strictly relative paths (relative to the project root) for file references.

## Scope
1.  **Prompts:**
    - `System/Agents/02_analyst_prompt.md`
    - `System/Agents/03_task_reviewer_prompt.md`
2.  **Skills:**
    - All files in `.agent/skills/`

## Acceptance Criteria
- All file paths in the target files are relative (e.g., `docs/TASK.md`, not `/Users/.../docs/TASK.md`).
- No absolute paths used in examples or instructions unless dealing with system internals (which shouldn't be the case here).
