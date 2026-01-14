# Task 011.1: Update Skills Documentation & Add Examples

## Use Case Connection
- UC-01: Developer Comprehends Dynamic Loading
- UC-02: Developer Tests Skill in Isolation (Python)
- UC-03: Developer Tests Skill in Isolation (n8n)

## Task Goal
Make `docs/SKILLS.md` a self-sufficient guide by adding detailed sections on dynamic loading, isolated testing, and best practices. Create the corresponding example script.

## Changes Description

### New Files
- `examples/skill-testing/test_skill.py` — Python script for isolated skill testing.
- `docs/tasks/task-011-01-doc-update.md` — This file.

### Changes in Existing Files

#### File: `docs/SKILLS.md`
- **Sections to Add:**
    - `Dynamic Loading`: Explain how Orchestrator assembles the prompt.
    - `Isolated Testing`: Add Python and n8n examples.
    - `Best Practices`: Add guidelines for skill creation.
- **Update:** Refine Table of Contents with new anchors.

## Test Cases

### Manual Verification
1. **TC-MANUAL-01:** Read `docs/SKILLS.md` and verify all internal links works.
2. **TC-MANUAL-02:** Run `python examples/skill-testing/test_skill.py` (after setting up a dummy key or just checking it imports/starts correctly).
3. **TC-MANUAL-03:** Verify `docs/SKILLS.md` rendering in IDE preview.

## Acceptance Criteria
- [ ] `docs/SKILLS.md` contains all new sections (Dynamic Loading, Testing, Best Practices).
- [ ] `examples/skill-testing/test_skill.py` exists and follows the template.
