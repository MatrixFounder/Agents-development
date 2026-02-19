---
name: skill-update-memory
description: "Auto-update .AGENTS.md files based on code changes."
tier: 2
version: 1.1
---
# Update Memory Skill

## Purpose
Prevent "Agent Amnesia" by keeping `.AGENTS.md` context files synchronized with code changes.

## When to Use
- Before committing code (Developer).
- During Code Review (Reviewer).
- In `04-update-docs` workflow.

## Strategy: Automated Detection + Manual Description

### Phase 1: Detect Changes
**Tool:** `scripts/suggest_updates.py`

**Usage:**
```bash
python3 .agent/skills/skill-update-memory/scripts/suggest_updates.py
```

**Bootstrap Migration Mode (optional):**
```bash
python3 .agent/skills/skill-update-memory/scripts/suggest_updates.py --mode bootstrap --create-missing --development-root src
```

**Output:**
- Identifies modified source files (ignoring build artifacts).
- Groups them by the closest `.AGENTS.md` (or suggested per-directory target in source folders).
- Generates a template for the update.
- In bootstrap mode, can create missing `.AGENTS.md` files without overwriting existing ones.
- Creation/suggestions are limited to explicit development roots (`--development-root`, default: `src`).
- `/.agent/skills/*` and `/.cursor/skills/*` are always excluded from memory target creation.

> [!NOTE]
> `.AGENTS.md` remains optional. If it does not exist, the helper must not fail.

### Phase 2: Generate Description (`.AGENTS.md` Update)

For each file listed by the script:
1. **Identify Change Type:**
    - New File -> Create entry.
    - Modified Logic -> Update description/functions.
    - Deleted -> Mark as `(Deleted)`.
2. **Write Description:**
    - Focus on **Purpose** (Why does it exist?).
    - List public **Classes/Functions**.

### Phase 3: Preservation

> [!IMPORTANT]
> **NEVER delete sections marked `[Human Knowledge]` or `<!-- PRESERVE -->`.**

Append new information below manual annotations.

## Example Update

```markdown
### [new_service.py]
**Purpose:** Handles user authentication.
**Classes:**
- `AuthService` — Main entry point.
  - `login()` — Validates credentials.
```

## Integration
- **Code Review:** Reviewer runs script to check if docs match code changes.
- **Pre-Commit:** Developer runs script to ensure no "Undocumented Code" is committed.
- **Migration/Onboarding:** Run bootstrap mode for external projects to create initial `.AGENTS.md` skeletons in source folders.
