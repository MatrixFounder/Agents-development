# Task: Fix Framework Consistency Issues

> **Status:** [DONE]
> **Context:** Fixing critical data loss risks and protocol inconsistencies identified in `framework_analysis.md`.

## 1. Requirements

### Critical Fixes
- [x] **Patch `trigger_technical.py`**: Stop it from blindly overwriting `docs/TASK.md`. It should fail if the file exists.
- [x] **Update `light-02-develop-task.md`**: Add explicit step to update `.AGENTS.md` (`skill-update-memory`).
- [x] **Standardize `vdd-01-start-feature.md`**: Replace hardcoded archiving steps with `skill-archive-task`.

## 2. Implementation Plan

### `trigger_technical.py`
- Add a check at the start: `if os.path.exists(task_output_path): ...`
- Print a clear error message: "TASK.md already exists. Please archive it first using `skill-archive-task`."
- Return failure.

### `light-02-develop-task.md`
- Insert a new step in the "Development" or "Commit" section to update `.AGENTS.md`.

### `vdd-01-start-feature.md`
- Update Step 3 (Chainlink Decomposition) to explicitly call `skill-archive-task` instead of describing the manual steps.

## 3. Verification
- Manual review of the modified files.
- (Self-Correction) Ensure the new instructions are clear and follow the framework's tone.
