# Skill Execution Policy

## 1. Purpose
Define a single enterprise-ready standard for how skills operate:
1. Where prompt-only execution is acceptable.
2. Where scripts are mandatory.
3. How to combine both safely and reproducibly.

## 2. Scope
This policy applies to all skills under:
1. `.agent/skills/*`
2. `.cursor/skills/*` (if symlinked/used)

## 3. Core Model
Every professional skill should follow a layered design:
1. Prompt Layer (`SKILL.md`): intent, decision logic, constraints, fallback behavior.
2. Script Layer (`scripts/`): deterministic operations on files/data/runtime.
3. Validation Layer (`tests/` and CI gates): objective pass/fail proof.

## 4. Decision Matrix

| Task Type | Primary Mode | Why | Required Evidence |
|---|---|---|---|
| File mutation by rules | Script-first | Must be deterministic and safe | Script output + diff |
| Path/security validation | Script-first | High risk, objective checks needed | Non-zero exit on violation |
| Linting/quality gates | Script-first | Repeatable and CI-friendly | CI pass/fail |
| Requirement analysis | Prompt-first | Requires context and judgement | Structured rationale |
| Architecture tradeoffs | Prompt-first | Non-deterministic reasoning | Alternatives + chosen option |
| Migration planning + execution | Hybrid | Reasoning + deterministic changes | Plan + script logs + validation |
| Documentation refresh from code | Hybrid | Analysis + repeatable extraction | Generated output + review notes |

## 5. When Scripts Are Mandatory
Scripts are required when at least one condition is true:
1. The task changes files using formal rules.
2. The output must be exactly reproducible.
3. The task is used as a quality/security gate.
4. The task can run in CI without human judgement.
5. Path handling, parsing, or bulk edits can cause damage if done manually.

## 6. When Prompt-Only Is Acceptable
Prompt-only execution is acceptable when:
1. The output is analytical, advisory, or exploratory.
2. There is no deterministic rule set to enforce.
3. Human judgement is the primary value.
4. No high-risk file mutation is performed.

## 7. Hybrid Execution Standard
Use this sequence for mixed tasks:
1. Prompt defines goal, constraints, and success criteria.
2. Script performs deterministic operations.
3. Prompt interprets script results and decides next step.
4. Validation confirms contract compliance.
5. Final output includes both rationale and machine-verifiable evidence.

## 8. Script Engineering Requirements
Every production-grade skill script must have:
1. `argparse` CLI with `--help`.
2. Explicit input arguments (no hidden globals).
3. Safe path normalization and containment checks.
4. Clear exit codes (`0` success, non-zero failure).
5. Idempotent behavior when feasible.
6. Dry-run mode when mutation risk exists.
7. Structured and readable output (`stdout` for results, `stderr` for errors).

## 9. Prompt Engineering Requirements
Every production-grade `SKILL.md` must define:
1. Purpose and trigger conditions.
2. Inputs and outputs.
3. Mandatory guardrails and stop conditions.
4. Script handoff contract (what script to run and when).
5. Failure handling and fallback path.

## 10. CI and Governance
For script-backed skills:
1. Add tests for success paths, failure paths, and security edge cases.
2. Integrate checks into CI (orchestrator gates).
3. Reject merges when critical skill checks fail.

## 11. Operational Safety Rules
Professional skills must enforce controlled automation boundaries:
1. All mutation-capable operations must have explicit scope inputs (path, module, or target set).
2. System/framework directories should be excluded by default unless explicitly targeted by the task.
3. Optional artifacts must be treated as non-blocking unless policy marks them mandatory.
4. Destructive behavior must be opt-in and never default.

## 12. Definition of Done for a Professional Skill
A skill is enterprise-ready only when all are true:
1. `SKILL.md` contract is clear and complete.
2. Deterministic parts are automated in scripts.
3. Scripts are tested and CI-enforced.
4. Safety constraints are explicit and validated.
5. Behavior is reproducible across local and CI runs.

## 13. Review Checklist
Use this checklist in skill reviews:
1. Is the prompt/script boundary explicit?
2. Are deterministic actions script-backed?
3. Are high-risk operations safety-checked?
4. Is CLI usage clear and documented?
5. Are tests present for core and edge behavior?
6. Is CI gate wired for this skill?
7. Is behavior idempotent or explicitly documented if not?

## 14. Anti-Patterns
Avoid these patterns:
1. Prompt-only automation for deterministic file mutations.
2. Script-only implementations for tasks that require real judgement.
3. Hidden side effects without explicit input flags.
4. Weak error signaling (success exit on failure).
5. Running wide-scope mutations without explicit scope controls.
