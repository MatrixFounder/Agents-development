# Technical Specification: Comprehensive Skills Documentation

## 0. Meta Information
- **Task ID:** 011
- **Slug:** skills-documentation-refining

## 1. General Description
The objective is to upgrade `docs/SKILLS.md` into a self-sufficient guide for the Skills System. This will allow any contributor to understand valid skills usage, dynamic loading mechanisms, and how to test skills in isolation without needing to reverse-engineer the Orchestrator code. The update covers documentation of the dynamic loading process, isolated testing methods (Python & n8n), and best practices.

## 2. List of Use Cases

### UC-01: Developer Comprehends Dynamic Loading
**Actors:** Developer/Contributor
**Preconditions:** User opens `docs/SKILLS.md`.
**Main Scenario:**
1. User reads the "Dynamic Loading" section.
2. User understands how the Orchestrator assembles the final prompt by combining the Base Role, Active Skills list, and Skill definitions.
3. User sees a concrete example using `08_agent_developer.md`.

### UC-02: Developer Tests Skill in Isolation (Python)
**Actors:** Developer
**Preconditions:** Developer wants to verify a prompt change in a skill.
**Main Scenario:**
1. Developer references the "Isolated Testing" section.
2. Developer copies the provided Python script template (`examples/skill-testing/test_skill.py`).
3. Developer runs the script with their specific skill and mock task.
4. Developer verifies the LLM output against expected behavior.

### UC-03: Developer Tests Skill in Isolation (n8n)
**Actors:** Developer (Low-Code preference)
**Preconditions:** Developer uses n8n for workflows.
**Main Scenario:**
1. Developer imports the provided JSON workflow for n8n.
2. Developer configures the nodes with Role, Skills, and Task.
3. Developer executes the node to observe the assembled prompt and model response.

## 3. Requirements & Acceptance Criteria

### 3.1 Content Requirements
- **Dynamic Loading Section:** Must explain the prompt assembly steps.
- **Isolated Testing Section:** Must provide **working** code examples for Python and n8n.
- **Best Practices Section:** Must cover size limits, anti-patterns, and versioing.
- **Table of Contents:** Updated with new sections and anchors.

### 3.2 Technical Requirements
- **File Format:** Markdown (`.md`).
- **Code Blocks:** Syntax highlighting for `python`, `json`, `markdown`.
- **Artifacts:**
    - `docs/SKILLS.md`: Updated content.
    - `examples/skill-testing/test_skill.py`: New file implementing the example.

## 4. Constraints and Assumptions
- Examples must be "copy-paste" ready (modulo API keys).
- The Python script should use a standard library or minimal dependencies (`openai` package).
- The documentation should be consistent with the actual Orchestrator logic.

## 5. Open Questions
- None.
