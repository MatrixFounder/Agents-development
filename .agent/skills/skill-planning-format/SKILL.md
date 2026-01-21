---
name: skill-planning-format
description: Standard structure and templates for Development Plans (docs/PLAN.md) and Tasks.
tier: 1
version: 1.0
---

# Planning Output Format

## 1. Development Plan Structure (`docs/PLAN.md`)

```markdown
# Development Plan: [Project Name]

## Task Execution Sequence

### Stage 1: Structure Creation and Stubs
- **Task {ID}.1** — [Brief description]
  - Use Cases: UC-01, UC-02
  - Description File: `docs/tasks/task-{ID}-01-{task-slug}.md`
  - Priority: Critical
  - Dependencies: none

- **Task {ID}.2** — [Brief description]
  - Use Cases: UC-01
  - Description File: `docs/tasks/task-{ID}-02-core-logic.md`
  - Priority: High
  - Dependencies: Task 1.1

### Stage 2: Core Functionality Implementation
[...]

### Stage 3: Testing
[...]

### Stage 4: Deployment
[...]

## Use Case Coverage

| Use Case | Tasks |
|-----------|--------|
| UC-01 | 1.1, 1.2, 2.1, 3.1 |
| UC-02 | 1.1, 2.3, 3.2 |
[...]
```

## 2. Detailed Task Description Structure

For each task create a separate file: `docs/tasks/task-{ID}-{SubID}-{slug}.md`

```markdown
# Task X.Y: [Task Name]

## Use Case Connection
- UC-XX: [Use Case Name]
- UC-YY: [Use Case Name]

## Task Goal
[Brief description of what must be achieved]

## Changes Description

### New Files
- `path/to/new_file.py` — [purpose of file]
- `path/to/.AGENTS.md` — [description of module] (MANDATORY for new directories)

### Changes in Existing Files

#### File: `path/to/existing_file.py`

**Class `ClassName`:**
- Add method `method_name(param1: Type1, param2: Type2) -> ReturnType`
  - Parameters:
    - `param1` — [description]
    - `param2` — [description]
  - Returns: [description]
  - Logic: [brief description of method logic]

**Function `function_name`:**
- Add parameter `new_param: Type` — [description]
- Change logic: [description of changes]

### Component Integration
[Description of how new components integrate with existing ones]

## Test Cases

### End-to-end Tests
1. **TC-E2E-01:** [Description of E2E test]
   - Input Data: [...]
   - Expected Result: [...]
   - Note: [At stub stage, hardcoded result is expected]

### Unit Tests
1. **TC-UNIT-01:** [Description of test]
   - Tested Function/Method: [...]
   - Input Data: [...]
   - Expected Result: [...]

### Regression Tests
- Run all existing tests from `tests/` directory
- Ensure functionality is not broken: [list critical scenarios]

## Acceptance Criteria
- [ ] All new classes/methods added
- [ ] All tests pass (including regression)
- [ ] Documentation updated
- [ ] Code complies with project standards

## Notes
[Additional information, implementation details]
```

## 3. Result Structure Rules

1. **`docs/PLAN.md` file** — general development plan with task sequence.
2. **`docs/tasks/task-{ID}-{SubID}-{Slug}.md` files** — detailed descriptions of each task.
3. **`docs/open_questions.md` file** — list of open questions (if any).
4. **CRITICAL:** Use only RELATIVE paths for file links (e.g., `[Link](docs/tasks/file.md)`), never absolute.
