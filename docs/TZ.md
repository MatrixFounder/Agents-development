## 0. Meta Information
- **Task ID:** 006
- **Slug:** nested-workflows

## 1. General Description
The goal is to implement support for "nested workflows" in the Google Antigravity system. This involves creating a set of modular workflow definitions in `.agent/workflows/` that can reference each other (e.g., a "VVD Enhanced" workflow calling a "Base Stub-First" workflow). This enhances scalability, reduces duplication, and makes the system more composable. We also need to update the system prompt (`.gemini/GEMINI.md`) and documentation (`README.md`, `docs/WORKFLOWS.md`) to expose these new capabilities.

## 2. List of Use Cases

### UC-01: Execute Base Stub-First Workflow
**Actors:** User, Orchestrator
**Preconditions:** User initiates the workflow via specific slash command or instruction.
**Main Scenario:**
1. Orchestrator receives request to start `/base-stub-first`.
2. Orchestrator executes steps sequentially: Analyst -> Review -> Architect -> Review -> Planner -> Review -> Development Loop.
**Postconditions:** Feature implemented using Stub-First and TDD approach.

### UC-02: Execute VDD Adversarial Refinement
**Actors:** User, Orchestrator (Adversary Role)
**Preconditions:** Core feature implementation is complete.
**Main Scenario:**
1. Orchestrator activates "Sarcasmotron" (Adversary).
2. Adversary reviews code/tests and provides critique.
3. If issues found, Developer fixes and Reviewer checks.
4. Cycle repeats until "zero-slop" achieved.
**Postconditions:** Code robust against adversarial critique.

### UC-03: Execute VDD Enhanced Workflow (Nested)
**Actors:** User, Orchestrator
**Preconditions:** None.
**Main Scenario:**
1. Orchestrator calls `/base-stub-first`.
2. Upon completion of base workflow, Orchestrator calls `/vdd-adversarial`.
**Postconditions:** Feature implemented and hardened via VDD.

### UC-04: Execute Full Robust Workflow (Nested)
**Actors:** User, Orchestrator
**Preconditions:** None.
**Main Scenario:**
1. Orchestrator calls `/vdd-enhanced`.
2. (Optional/Future) Orchestrator calls `/security-audit`.
3. Orchestrator updates final documentation.
**Postconditions:** Maximum reliability achieved.

## 3. Non-functional Requirements
- **Composability:** Workflows must be modular and callable by name.
- **Integration:** Must work seamlessly with the existing `task_boundary` and tool usage patterns.
- **Documentation:** All new workflows must be documented in `docs/WORKFLOWS.md` and `README.md`.

## 4. Constraints and Assumptions
- Assumes Antigravity framework supports parsing "Call /workflow-name".
- Assumes `.gemini/GEMINI.md` is the writable integration point for system prompts.
- Assumes `.agent/workflows` is the correct location for workflow files.

## 5. Open Questions
- None.
