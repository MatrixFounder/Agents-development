# Task: Validate O1-O3 Implementation

## 0. Meta Information

| Field    | Value                   |
|----------|-------------------------|
| Task ID  | 036                     |
| Slug     | o1-o3-validation        |
| Status   | Completed               |
| Priority | High                    |

---

## 1. General Description
The goal is to strictly validate the implementation of Framework Optimizations O1 (Phase-Specific Skill Loading), O2 (Orchestrator Compression), and O3 (Architecture Format Split). This involves verifying that the new mechanisms work as expected, tokens are saved, and no regression is introduced in the standard development pipeline.

## 2. List of Use Cases

### 2.1. UC-01: Standard Pipeline Execution (O1 & O2 Verification)
**Actors:** Orchestrator, Analyst, Architect, Planner, Developer, Reviewers
**Preconditions:** System configured with O1-O3 changes.
**Main Scenario:**
1.  Run a standard development task (e.g., "Add a simple 'Hello World' feature").
2.  Verify that correct skills are loaded at each phase (O1 validation).
    -   Analysis: `requirements-analysis`, `skill-task-model` loaded.
    -   Architecture: `architecture-design`, `architecture-format-core` loaded.
    -   Planning: `planning-decision-tree`, `planning-format` loaded.
    -   Execution: `developer-guidelines` loaded.
    -   TIER 0 skills (`safe-commands`, `core-principles`, `artifact-management`) ALWAYS loaded.
3.  Verify that `01_orchestrator.md` correctly dispatches stages using the new compressed logic (O2 validation).
4.  Verify that automation (git, mv, tests) works without manual approval (O1 `safe-commands` check).

### 2.2. UC-02: Architecture Split Verification (O3)
**Actors:** Architect Agent
**Preconditions:** `docs/ARCHITECTURE.md` relates to existing system.
**Main Scenario (Core):**
1.  Trigger Architect for a minor update.
2.  Verify `architecture-format-core` is loaded.
3.  Verify `architecture-format-extended` is NOT loaded.
4.  Verify update is successful using the core format.

**Alternative Scenario (Extended):**
1.  Trigger Architect for a NEW system or explicit full template request.
2.  Verify `architecture-format-extended` is loaded.
3.  Verify full template is used.

### 2.3. UC-03: Token Usage Comparison
**Actors:** System / Tooling
**Preconditions:** Baseline token usage known or estimatable.
**Main Scenario:**
1.  Measure token usage for the standard pipeline run in UC-01.
2.  Compare with baseline (from `Backlog/agentic_development_optimisations.md`).
3.  Report savings.

## 3. Acceptance Criteria
- [ ] **O1:** TIER 0 skills are always loaded. TIER 1 skills load only in respective phases. `safe-commands` auto-run works.
- [ ] **O2:** All 14 orchestrator scenarios function correctly (Stages 1-14).
- [ ] **O3:** `architecture-format-core` used for minor updates, `extended` available on demand.
- [ ] **Deliverable:** Test report with pass/fail for each check.
- [ ] **Deliverable:** Token usage comparison.

## 4. Open Questions
None.
