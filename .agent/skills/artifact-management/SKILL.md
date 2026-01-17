---
name: artifact-management
description: "Rules for managing local .AGENTS.md and global artifacts (TASK.md, ARCHITECTURE.md)."
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


## Archiving Protocol (CRITICAL)
Before creating a NEW `docs/TASK.md` (Analyst) or starting a new major phase:
1.  **Check Condition**: Does `docs/TASK.md` exist and contain a different/completed task?
2.  **Extract Metadata**: Read `Task ID` and `Slug` from "0. Meta Information".
3.  **Generate Filename**: Call the `generate_task_archive_filename` tool:
    ```python
    # Auto-generate next ID:
    result = generate_task_archive_filename(slug="my-task-slug")
    # Or validate a proposed ID:
    result = generate_task_archive_filename(slug="my-task-slug", proposed_id="032")
    ```
    - If `status == "generated"` or `status == "corrected"`: use `result["filename"]`
    - If `status == "conflict"`: notify user of the conflict
    - If `status == "error"`: handle the error
4.  **Update Task ID**: Before archiving, update the `Task ID` in TASK.md's Meta Information to match `result["used_id"]`.
5.  **Archive**: Move the file to `docs/tasks/{filename}`.
    -   Command: `mv docs/TASK.md docs/tasks/{filename}`
6.  **Validation**: Verify the file was moved before creating the new one.

### Execution Rule
- The archive command (`mv docs/TASK.md docs/tasks/...`) is **SAFE TO AUTO-RUN**.
- **DO NOT** wait for user approval for this operation.
- This is a mandatory, non-destructive operation (move, not delete).

### Safe Commands (Auto-Run without Approval)
The following commands are **SAFE TO AUTO-RUN** and do NOT require user confirmation:

| Category | Commands |
|----------|----------|
| **Read-only** | `ls`, `cat`, `head`, `tail`, `find`, `grep`, `tree`, `wc` |
| **File info** | `stat`, `file`, `du`, `df` |
| **Git read** | `git status`, `git log`, `git diff`, `git show`, `git branch` |
| **Archiving** | `mv docs/TASK.md docs/tasks/...`, `mv docs/PLAN.md docs/plans/...` |
| **Tool calls** | `generate_task_archive_filename`, `list_directory`, `read_file` |

> [!IMPORTANT]
> These commands are idempotent or read-only. Always auto-run them to avoid blocking workflow.

## Protocol
1. **Read First:** Before starting work, read relevant artifacts.
2. **Update Immediately:** Update artifacts corresponding to your changes (Developer updates `.AGENTS.md`, Analyst updates `TASK.md`).
3. **Consistency:** Ensure artifacts match the actual code state.
