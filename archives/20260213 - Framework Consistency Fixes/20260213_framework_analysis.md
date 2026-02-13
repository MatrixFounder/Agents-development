# Framework Consistency Analysis

## 1. Overview
I have analyzed the framework (21 workflows, 17 agent prompts, and key scripts) to identify gaps in adhering to global protocols, specifically **Task Archiving (`skill-archive-task`)** and **Memory Updates (`skill-update-memory`)**.

The reference fix in `GEMINI.md` and `.agent/workflows/04-update-docs.md` correctly establishes a "Task Rotation Check" that archives existing tasks before overwriting them.

## 2. Critical Findings (Data Loss Risks)

### 🚨 `product-handoff` Script Overwrites TASK.md
**File:** `.agent/skills/skill-product-handoff/scripts/trigger_technical.py`
**Issue:** The script blindly overwrites `docs/TASK.md` without checking if it exists or verifying previous task completion.
**Impact:** If a user runs the product pipeline while a technical task is in progress (or if a previous task wasn't cleaned up), the **previous task data will be permanently lost**.
**Recommendation:** 
- Modify `trigger_technical.py` to check for `docs/TASK.md`.
- If it exists, either error out (asking user to run archive) or implement the archiving logic directly (renaming to `docs/tasks/...`).

## 3. Process Gaps (Protocol Violations)

### ⚠️ Light Mode Skips Memory Updates
**File:** `.agent/workflows/light-02-develop-task.md`
**Issue:** The workflow does not explicitly include a step to update `.AGENTS.md` (`skill-update-memory`).
- While the `08_agent_developer` prompt mentions it, Light Mode emphasizes speed ("Implement the fix directly"), which increases the risk of this step being skipped.
**Impact:** The agent memory (`.AGENTS.md`) will drift from the codebase state, leading to hallucinations in future tasks.
**Recommendation:** Add an explicit step: `3. **Memory Update**: Update .AGENTS.md to reflect changes.`

### ⚠️ VDD Start-Feature Inconsistency
**File:** `.agent/workflows/vdd-01-start-feature.md`
**Issue:** The workflow describes the archiving process ("Check if docs/TASK.md exists... Archive it...") but does not explicitly call `skill-archive-task`.
**Impact:** Minor inconsistency. If the skill changes, this hardcoded instruction might become outdated.
**Recommendation:** Update to explicitly say `Apply skill-archive-task`.

## 5. Summary of Status

| Component | Check | Status | Notes |
| :--- | :--- | :--- | :--- |
| `04-update-docs.md` | Task Rotation | ✅ Fixed | Reference implementation. |
| `01-start-feature.md` | Task Rotation | ✅ Safe | Explicitly calls skill. |
| `trigger_technical.py` | Task Rotation | ❌ **CRITICAL** | Overwrites without archive. |
| `light-02-develop-task` | Memory Update | ⚠️ **Risk** | Missing explicit step. |
| `vdd-01-start-feature` | Task Rotation | ⚠️ Inconsistent | Hardcoded instructions vs Skill call. |

## 6. Proposed Action Items
1.  **Patch `trigger_technical.py`**: Add safguards to prevent overwriting `docs/TASK.md`.
2.  **Update `light-02-develop-task.md`**: Add mandatory `.AGENTS.md` update step.
3.  **Standardize `vdd-01-start-feature.md`**: Switch to using `skill-archive-task`.
