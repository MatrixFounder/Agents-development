# Implementation Plan - Evolved TDD (Stub-First v2)

## Goal
Implement the "Evolved TDD" methodology into the framework's core skills to enforce strict verification ("Expected Fail Reason", "Minimal Code") and robust bug-fixing protocols.

## User Review Required
> [!IMPORTANT]
> This change modifies core skills (`tdd-stub-first`, `developer-guidelines`). All agents starting new tasks after this update will follow stricter protocols.

## Proposed Changes

### 1. New Skill: `tdd-strict` (Tier 3)
*Why: To avoid stifling bootstrapping creativity while enforcing reliability when needed.*
#### [NEW] [.agent/skills/tdd-strict/SKILL.md](file:///Users/sergey/Antigravity/agentic-development/.agent/skills/tdd-strict/SKILL.md)
- Creates a new High-Assurance skill (Self-Contained, NO inheritance from Tier 1).
- **Strict Cycle**: Test w/ Fail Reason -> Verify Fail -> Minimal Code -> Verify Pass.
- **Minimalism Law**: Explicit ban on speculation.

### 2. Skill: `developer-guidelines` (Tier 1)
Update to v1.1. Add **Bug Fixing Protocol** ONLY.
#### [MODIFY] [.agent/skills/developer-guidelines/SKILL.md](file:///Users/sergey/Antigravity/agentic-development/.agent/skills/developer-guidelines/SKILL.md)
- Add Section: **5. Bug Fixing Protocol** (Always applies, irrespective of Tier).
    - Steps: Reproduce -> Verify Fail -> Fix -> Verify Pass.
- *Excluded*: The "Minimalism Law" is NOT added here, it stays in Tier 3 `tdd-strict`.

### 3. Skill: `code-review-checklist` (Tier 1)
Update to v1.2. Add conditional checks.
#### [MODIFY] [.agent/skills/code-review-checklist/SKILL.md](file:///Users/sergey/Antigravity/agentic-development/.agent/skills/code-review-checklist/SKILL.md)
- Add Section: **High Assurance (If Tier 3 Active)**
- Check: "Fail Reason Verified?"
- Check: "Dead Code / Mutation Check?"

### 4. Workflows Update
Update workflows to include `tdd-strict` in robust pipelines.
#### [MODIFY] [.agent/workflows/full-robust.md](file:///Users/sergey/Antigravity/agentic-development/.agent/workflows/full-robust.md)
- Add: `Load Skill: tdd-strict` during Development Phase.

### 5. Skill: `plan-review-checklist`
Update to v1.1.
#### [MODIFY] [.agent/skills/plan-review-checklist/SKILL.md](file:///Users/sergey/Antigravity/agentic-development/.agent/skills/plan-review-checklist/SKILL.md)
- Add Check: Tasks must explicitly mention "Expect Fail" verification steps.

## Verification Plan

### Automated Verification
Since these are instructions for Agents (Markdown files), we cannot "run" them directly.
Verification will be **Manual Simulation**:
1.  **Read-Back**: I will read the modified skill files to ensure new sections are correctly formatted.
2.  **Self-Correction**: I will start a dummy task (simulated) to confirm the Analyst/Developer would see these new instructions.

### Manual Verification
- User can check if future agents adhere to the new protocols.
