# Walkthrough: Evolved TDD Implementation

## Summary
To enhance the reliability of the Agentic Framework, we implemented an "Evolved TDD" strategy that distinguishes between strict mechanical verification (Tier 3) and universal behavioral protocols (Tier 1).

## Changes Implemented

### 1. New Skill: `tdd-strict` (Tier 3)
Created a new, self-contained High Assurance skill for critical tasks.
- **Protocol**: Mandates `EXPECTED_FAIL_REASON` and "Minimalism Law".
- **Location**: `.agent/skills/tdd-strict/SKILL.md`

### 2. Updated: `developer-guidelines` (Tier 1)
Appended a universal **Bug Fixing Protocol**.
- **Rule**: "No fix without a reproducing failing test."
- **Status**: Applies to ALL developers always.

### 3. Updated Checklists
- **`code-review-checklist`**: Added "High Assurance" section (active only when Tier 3 is active).
- **`plan-review-checklist`**: Added check for planning Strict Mode usage.

### 4. Workflow Optimization
Updated `.agent/workflows/full-robust.md`:
- Automatically loads `tdd-strict` when running the robust pipeline.

## Verification
We verified that:
1.  `tdd-strict` exists and follows the `skill-creator` standard (Tier 3).
2.  `developer-guidelines` contains the new Protocol in Section 6.
3.  Checklists contain the new verification items.
4.  Workflow explicitly loads the new skill.

## Usage
To use the new Strict Mode:
- **Manually**: Add `Load Skill: tdd-strict` to your prompt.
- **Automatically**: Run the `/full-robust` workflow.
