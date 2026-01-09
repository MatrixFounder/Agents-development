# Task 006.2: Implement Workflow Logic

## Use Case Connection
- UC-01, UC-02, UC-03, UC-04

## Task Goal
Fill the workflow files with the actual steps and nesting logic.

## Changes Description

### Changes in Existing Files (Stubs)
- `.agent/workflows/base-stub-first.md`: Add sequential steps (Analyst -> Architect -> Planner -> Developer).
- `.agent/workflows/vdd-adversarial.md`: Add adversarial loop steps.
- `.agent/workflows/vdd-enhanced.md`: Add nested calls to `base-stub-first` and `vdd-adversarial`.
- `.agent/workflows/full-robust.md`: Add nested calls to `vdd-enhanced`.

## Test Cases
### Manual Verification
1. **TC-MAN-01:** Verify content of each file matches the definitions in Task 006 description.

## Acceptance Criteria
- [ ] All files contain correct steps.
- [ ] Nested calls format (`Call /workflow-name`) is used correctly.
