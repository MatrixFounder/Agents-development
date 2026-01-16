### 0. Meta Information
- **Task ID:** 021
- **Slug:** skills-optimization-planner-analyst
- **Status:** Completed

# TASK: Optimize Planner and Analyst Prompts via Skills

## Problem
`02_analyst_prompt.md` and `06_agent_planner.md` contain large static sections (templates, examples) that bloat the context window and reduce maintainability.

## Goal
Extract static content into dedicated skills, following the pattern established in Task 019 (Architect Refactor).

## Plan
1.  **Analyst Optimization:**
    -   Create `skill-task-model`: Move "Examples of Good/Bad Use Cases" and `TASK.md` structure here.
    -   Update `02_analyst_prompt.md` to reference the skill.
2.  **Planner Optimization:**
    -   Create `skill-planning-format`: Move `PLAN.md` and `task-{ID}-{SubID}.md` templates here.
    -   Update `06_agent_planner.md` to reference the skill.
3.  **Documentation:**
    -   Update `docs/SKILLS.md` with new skills.

## Acceptance Criteria
- Agents 02 and 06 are significantly smaller.
- New skills `skill-task-model` and `skill-planning-format` exist and are correct.
- `docs/SKILLS.md` is updated.
