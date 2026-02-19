---
description: Ensure documentation is up to date
---
1. **Task Rotation Check**:
   - If `docs/TASK.md` exists and contains a *different* completed task:
     - Apply `skill-archive-task` to move it to `docs/tasks/`.
     - Create a fresh `docs/TASK.md` for this workflow.
2. Check if `docs/TASK.md` matches the current codebase state.
3. Check if `docs/ARCHITECTURE.md` matches the current codebase state.
   - If outdated, apply `skill-reverse-engineering` to regenerate from code.
4. Check if `.AGENTS.md` files are up to date.
   - Apply `skill-update-memory` to analyze recent changes and propose updates.
   - For external project onboarding/migration, run:
     - `python3 .agent/skills/skill-update-memory/scripts/suggest_updates.py --mode bootstrap --create-missing --development-root src`
5. Update any outdated documentation.
