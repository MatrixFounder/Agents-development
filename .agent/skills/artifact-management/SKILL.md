---
name: artifact-management
description: "Rules for managing local .AGENTS.md and global artifacts (TASK.md, ARCHITECTURE.md)."
tier: 0
version: 1.0
---
# Artifact Management

## Local .AGENTS.md (Per-Directory)
- **Purpose:** Distributed long-term memory for specific directories.
- **Location:** In every source code directory (e.g., `src/services/.AGENTS.md`).
- **Single Writer:** ONLY the **Developer** agent is allowed to create or update these files. All other agents (Analyst, Reviewer, etc.) must only READ them.
- **Format:**
  ```markdown
  # Directory: src/services/

  ## Purpose
  [Brief description of the directory's purpose]

  ## Files

  ### [filename.py]
  **Classes/Functions:**
  - `[ClassName]` — [Description]
    - `[method_name]` — [Description]
  ```

## Global Artifacts
- **TASK.md:** Technical Specification. Managed by Analyst.
- **ARCHITECTURE.md:** System Architecture. Managed by Architect.
- **PLAN.md:** Development Plan. Managed by Planner.

## Dual State Tracking (CRITICAL)

You serve TWO masters:
1. **Agentic Mode (Internal):** You have an internal `<appDataDir>/brain/.../task.md` for YOUR mental state. This is ephemeral and for your eyes only.
2. **Project Protocol (External):** You MUST maintain `docs/TASK.md` as the persistent Source of Truth for the TEAM.

**Resolution Rule:**
> **NEVER** let your internal `task.md` replace or obsolete the Project `docs/TASK.md`.
> You must keep `docs/TASK.md` up-to-date even if you are tracking granular steps internally.
> When "Creating a TASK", you create `docs/TASK.md`.


## Archiving Protocol (CRITICAL)

> [!IMPORTANT]
> **Complete protocol is in `skill-archive-task`.**
> This skill depends on `skill-archive-task` for archiving `docs/TASK.md`.

Before creating a NEW `docs/TASK.md`:
1. **Apply Skill**: `skill-archive-task`
2. Follow the 6-step protocol defined there

See `skill-archive-task` for:
- When to Archive (conditions)
- Decision Logic (new vs refinement)
- Protocol Steps (6 steps)
- Filename generation (tool or manual fallback)

### Safe Commands (Auto-Run without Approval)

> See **`skill-safe-commands`** for the complete list of commands safe for auto-execution.

Key commands: `mv docs/TASK.md docs/tasks/...`, `ls`, `cat` — read-only validation.

## Protocol
1. **Read First:** Before starting work, read relevant artifacts.
2. **Update Immediately:** Update artifacts corresponding to your changes (Developer updates `.AGENTS.md`, Analyst updates `TASK.md`).
3. **Consistency:** Ensure artifacts match the actual code state.
