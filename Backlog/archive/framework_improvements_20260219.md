# Framework Improvements Specification (Enterprise Readiness)

Date: 2026-02-20
Status: Done

## 1. Document Purpose

This document defines a complete hardening and modernization backlog to move the framework to **enterprise-ready** quality.

It covers all identified gaps:
- Tool execution security and sandbox integrity
- Workflow/prompt consistency and operability
- Skills quality and governance
- Validation reliability (VDD/TDD gates)
- Python environment reproducibility
- Documentation alignment and installation quality
- Automation reliability and CI coverage

---

## 2. Target State (Enterprise Definition)

The framework is considered enterprise-ready only when all target conditions below are met:

1. **Security**
   - No command-injection paths in native tools.
   - No path traversal bypasses.
   - Tool execution constrained to project root and explicit allowlists.
2. **Deterministic Operation**
   - All referenced prompts/skills/workflows resolve to existing files.
   - No broken workflow entry points.
3. **Quality Gates**
   - Validators produce correct results (no false negatives/false positives on required formats).
   - CI enforces regression checks for tools, skills, workflows.
4. **Reproducible Environment**
   - Clean Python bootstrap with pinned minimal dependencies and clear virtualenv policy.
   - Installation instructions are runnable as-is.
5. **Governance**
   - Single naming convention for skills/prompts/artifacts.
   - Versioned change control and release checklist.

---

## 3. Current-State Findings (Complete List)

### 3.1 Critical Security Findings

1. **Command injection in `run_tests`**
   - File: `System/scripts/tool_runner.py`
   - Root cause: prefix-only command validation + `shell=True`
   - Impact: arbitrary command execution and possible test-result masking.

2. **Path validation bypass via prefix collision**
   - File: `System/scripts/tool_runner.py`
   - Root cause: `str(target_path).startswith(str(repo_root))`
   - Impact: absolute paths outside project may pass validation when prefix matches.

3. **Unbounded command execution risk**
   - File: `System/scripts/tool_runner.py`
   - Root cause: no timeout/process constraints for test command execution.
   - Impact: hangs/DoS behavior in automation loops.

### 3.2 Major Reliability Findings

4. **Broken workflow references to missing prompt files**
   - Affected workflows reference non-existing files:
     - `System/Agents/06_agent_planner.md`
     - `System/Agents/07_agent_plan_reviewer.md`
     - `System/Agents/08_agent_developer.md`
     - `System/Agents/09_agent_code_reviewer.md`
   - Actual files are `*_prompt.md` variants.

5. **VDD plan validator always reports missing IDs**
   - File: `.agent/skills/skill-spec-validator/scripts/validate.py`
   - Root cause: escaped token compared via plain substring (`re.escape` + `in`).

6. **Artifact naming conflict: `AGENTS.md` vs `.AGENTS.md`**
   - Prompts/workflows/skills require `.AGENTS.md` updates.
   - Current repo keeps root `AGENTS.md` and no `.AGENTS.md` files.
   - Result: memory update automation and expectations diverge.

7. **Product handoff `sign_off.py` CLI unsafe behavior**
   - File: `.agent/skills/skill-product-handoff/scripts/sign_off.py`
   - Root cause: no argument parser/help mode; positional misuse mutates unintended files.

### 3.3 Quality/Standards Findings

8. **Skill standards non-compliance across large subset**
   - Local validator results: 22/43 skills failing.
   - Typical failures:
     - Description prefix policy violation
     - Missing frontmatter keys (`tier`, `version`)
     - Invalid tier values (e.g., `tier: 3` while validator allows 0..2)
     - Oversized inline code blocks.

9. **Tool docs and implementation drift**
   - Docs mention allowed commands/patterns not fully aligned with real runner behavior.
   - Examples include command forms not accepted by implementation.

10. **Docs/workflow references stale in multiple places**
    - README/workflows reference old prompt filenames.
    - Leads to operational confusion and brittle onboarding.

### 3.4 Environment/Operational Findings

11. **Test execution not runnable in clean environment**
    - `pytest` missing by default in current environment.

12. **Global skill tooling dependency gaps**
    - Global `skill-creator` scripts require `PyYAML`, missing by default.
    - Causes failures for quick validation/init flows outside local project tooling.

13. **Git-dependent scripts with non-git workspace behavior undefined**
    - Some helper scripts rely on `git diff` but no fallback policy when `.git` is absent.

---

## 4. Program Structure (Workstreams)

## WS-01: Tooling Security Hardening (P0)

### Objective
Eliminate command execution and path traversal vulnerabilities in native tool runner.

### Scope
- `System/scripts/tool_runner.py`
- `.agent/tools/schemas.py`
- `System/Docs/ORCHESTRATOR.md`
- New/updated tests in `.agent/tools/`

### Requirements (MUST)
1. Replace `shell=True` in `run_tests` with argument-list execution.
2. Parse and validate command tokens, not raw prefix strings.
3. Enforce strict command allowlist with exact executable + argument policy.
4. Enforce root-safe `cwd` resolution (`repo_root` containment).
5. Add command timeout and deterministic error return on timeout.
6. Replace `startswith` path security check with `Path.resolve()` + `relative_to` containment.
7. Add unit tests for:
   - separator injection (`;`, `&&`, `|`, `$()`)
   - traversal attempts
   - absolute path prefix-collision attempts
   - invalid cwd values.

### Acceptance Criteria
- Injection test vectors fail with `success: false`.
- Out-of-root read/write/list operations blocked.
- Timeout test returns controlled error.
- Security regression tests pass in CI.

---

## WS-02: Workflow and Prompt Reference Repair (P1)

### Objective
Ensure every workflow and docs reference points to existing prompt files.

### Scope
- `AGENTS.md`
- `.agent/workflows/*.md`
- `README.md` role table and workflow examples
- `System/Docs/WORKFLOWS.md` and related docs

### Requirements (MUST)
1. Replace all stale references:
   - `06_agent_planner.md` -> `06_planner_prompt.md`
   - `07_agent_plan_reviewer.md` -> `07_plan_reviewer_prompt.md`
   - `08_agent_developer.md` -> `08_developer_prompt.md`
   - `09_agent_code_reviewer.md` -> `09_code_reviewer_prompt.md`
2. Add automated link/reference checker script for `System/Agents/*.md` references.
3. Add CI gate: fail if any referenced local file does not exist.

### Acceptance Criteria
- `rg`-based reference audit reports zero missing prompt files.
- Workflow smoke test executes each workflow file without missing-path failures.

---

## WS-03: Artifact Memory Model Normalization (P1)

### Objective
Resolve `AGENTS.md` vs `.AGENTS.md` contract ambiguity.

### Options (decision required, pick one and apply globally)
1. **Option A (Recommended):** Keep `AGENTS.md` as root policy, use `.AGENTS.md` only for per-directory memory.
2. **Option B:** Standardize everything on `AGENTS.md`.

**Decision:** Option A.
- `AGENTS.md`/`GEMINI.md` remain root system policy files.
- `.AGENTS.md` remains per-directory memory for source-code folders in the target development project.
- Creation policy for `.AGENTS.md` in source-code development folders is preserved.

### Requirements (MUST)
1. Define canonical artifact map in one authoritative doc.
2. Update all skills/prompts/workflows/scripts to same naming contract.
3. Update `skill-update-memory` logic to discover canonical target files reliably.
4. Add migration automation for existing projects:
   - bootstrap missing `.AGENTS.md` files in source-code folders
   - keep legacy variants untouched unless explicit migration task is requested.

### Acceptance Criteria
- No contradictory instructions across prompts/skills/docs.
- Memory update scripts generate deterministic target suggestions and support bootstrap creation for missing files.
- `.AGENTS.md` creation/update policy is consistent across docs and prompts for source-code target folders.

---

## WS-04: Validator Correctness and Quality Gates (P1)

### Objective
Make validation gates trustworthy and deterministic.

### Scope
- `.agent/skills/skill-spec-validator/scripts/validate.py`
- tests for validator behavior
- VDD workflow docs

### Requirements (MUST)
1. Fix RTM ID coverage matching logic to correctly detect `[ID]` entries.
2. Add test matrix:
   - IDs with dots/hyphens (`R1.1`, `R-2`)
   - mixed checklist formats
   - bypass flag behavior.
3. Preserve explicit non-zero exit codes on validation failure.
4. Document supported RTM/PLAN formats with examples.

### Acceptance Criteria
- Known valid samples pass.
- Known invalid samples fail for correct reason.
- No false-negative on standard `[R1]` and `[R1.1]` markers.

---

## WS-05: Skills Standardization Program (P2)

### Objective
Bring all skills to a single enforceable quality standard.

### Scope
- `.agent/skills/*/SKILL.md`
- `.agent/skills/skill-creator/scripts/validate_skill.py` policy
- related docs (`System/Docs/SKILLS.md`, `System/Docs/SKILL_TIERS.md`)

### Requirements (MUST)
1. Decide tier model compatibility:
   - either allow tier 3 in validator and docs consistently
   - or migrate all skills to 0/1/2.
2. Batch-fix frontmatter consistency (`name`, `description`, `tier`, `version`).
3. Normalize description trigger style based on chosen CSO policy.
4. Move oversized inline examples to `examples/` or `references/`.
5. Add CI gate: skill validation must pass for all skills.

### Acceptance Criteria
- 43/43 skills pass local validator.
- Tier model is consistent across:
  - validator rules
  - `SKILL_TIERS.md`
  - each skill frontmatter.

---

## WS-06: Product Handoff Script Hardening (P2)

### Objective
Make product handoff scripts safe and production-grade.

### Scope
- `.agent/skills/skill-product-handoff/scripts/sign_off.py`
- `.agent/skills/skill-product-handoff/scripts/verify_gate.py`
- `.agent/skills/skill-product-handoff/scripts/compile_brd.py`

### Requirements (MUST)
1. Add `argparse` to all scripts with proper `--help`.
2. Require explicit `--file` arguments and validate file existence.
3. Prevent accidental writes to unintended targets.
4. Return explicit non-zero codes on failures.
5. Add unit tests for:
   - help mode
   - invalid path
   - missing file
   - success path.

### Acceptance Criteria
- `--help` prints usage and exits without mutations.
- Invalid arguments never create files.

---

## WS-07: Python Environment Standardization (P1)

### Objective
Provide deterministic, secure Python runtime setup for all framework tooling.

### Scope
- `README.md` Installation section
- optional `requirements-dev.txt` / `pyproject.toml`
- bootstrap script(s)

### Requirements (MUST)
1. [DONE] Define minimum supported Python version (recommended `>=3.11`).
2. [DONE] Define pinned minimal dependencies for framework tooling (`requirements-dev.txt`).
3. [DONE] Provide one canonical setup flow:
   - create virtualenv
   - install dependencies
   - verify with smoke checks.
4. [DONE] Add troubleshooting for:
   - `No module named pytest`
   - `No module named yaml`.
5. [DONE] Add optional local preflight script (`System/scripts/doctor.py`).

### Acceptance Criteria
- Fresh clone setup succeeds end-to-end from docs only.
- All local script entrypoints run without missing dependency errors.

---

## WS-08: CI/CD Gatekeeping and Regression Defense (P1)

### Objective
Automate enforcement of framework contracts.

### Scope
- CI pipeline config (provider-agnostic)
- test/validation scripts

### Required CI Jobs (MUST)
1. **Tooling tests:** `.agent/tools` test suite.
2. **Skill lint/validate:** validate every skill folder.
3. **Reference integrity:** check all local file links in workflows/docs.
4. **Security lint:** static checks for forbidden `shell=True` and unsafe path checks.
5. **Smoke workflows:** parse/resolve key workflows (`base-stub-first`, `vdd-enhanced`, `light-*`).

### Acceptance Criteria
- PR cannot merge if any gate fails.
- Critical gates run under 5 minutes on standard runner.

---

## WS-09: Documentation and Governance Alignment (P2)

### Objective
Make docs authoritative and conflict-free.

### Scope
- `README.md`
- `AGENTS.md`
- `System/Docs/*.md`

### Requirements (MUST)
1. Update role file mappings and workflow commands to actual files.
2. Align naming conventions across:
   - `skill-*` mentions
   - directory names
   - workflow command forms.
3. Add a “single source of truth” map for:
   - prompts
   - skills
   - workflows
   - tool schemas.
4. Add release checklist for framework version bumps.

### Acceptance Criteria
- No contradictory path/name instructions between major docs.
- New contributor can bootstrap without undocumented assumptions.

---

## 5. Prioritized Backlog (Execution Order)

| ID | Workstream | Priority | Effort | Dependency | Status |
|---|---|---|---|---|---|
| BI-001 | WS-01 Tooling Security Hardening | P0 | M | None | Done (local hardening + tests + docs; CI enforcement tracked in BI-005) |
| BI-002 | WS-02 Workflow Reference Repair | P1 | S | BI-001 optional | Done (active refs repaired + checker script; CI wiring tracked in BI-005) |
| BI-003 | WS-04 Validator Correctness | P1 | S | None | Done (ID matching fixed + regression tests) |
| BI-004 | WS-07 Python Standardization | P1 | S | None | Done (pinned deps + doctor preflight + README updates) |
| BI-005 | WS-08 CI Gatekeeping | P1 | M | BI-001..004 | Done (GitHub Actions gates added in .github/workflows/framework-gates.yml; branch protection configured in VCS settings) |
| BI-006 | WS-03 Artifact Memory Normalization | P1 | M | BI-002 | Done (Option A policy fixed; canonical contract documented; migration automation added via `suggest_updates.py --mode bootstrap --create-missing`; policy-level docs aligned) |
| BI-007 | WS-05 Skills Standardization | P2 | L | BI-005 partial | In Progress (CSO prefix enforcement relaxed for existing skills; metadata gaps fixed; remaining 2 inline-block findings intentionally deferred) |
| BI-008 | WS-06 Product Script Hardening | P2 | S | None | Done (argparse + explicit file args + safe path validation + unit tests) |
| BI-009 | WS-09 Docs/Governance Alignment | P2 | M | BI-002, BI-006 | Done (docs/governance aligned; source-of-truth map + release checklist added; command/path naming normalized) |

---

## 6. Detailed Technical Requirements by Component

## 6.1 `System/scripts/tool_runner.py`

### Mandatory design updates
1. Introduce secure command model:
   - parse command using `shlex.split`
   - enforce executable and args policy
   - reject shell operators and subshell syntax.
2. Execute via `subprocess.run([...], shell=False, timeout=...)`.
3. Add `cwd` normalization:
   - resolve against `repo_root`
   - verify containment using `Path.relative_to`.
4. Harden path checks with canonical containment helper shared by all file tools.
5. Return normalized error schema:
   - `success: false`
   - `error_code`
   - `error`.

### Regression tests
- injection separators
- escaped separators
- absolute path traversal
- timeout behavior
- command allowlist matrix.

## 6.2 `.agent/skills/skill-spec-validator/scripts/validate.py`

### Mandatory fixes
1. Replace broken matching:
   - current: `pattern = re.escape(...)` + `if pattern not in ...`
   - required: proper regex search or literal token search.
2. Add parser tests for markdown tables and RTM variants.
3. Keep strict error messages with actionable context.

## 6.3 Workflow files

### Mandatory fixes
1. Rename stale prompt references to existing `*_prompt.md`.
2. Add lint script that validates every `System/Agents/*.md` path in workflows.
3. For slash command names, document canonical command table and aliases.

## 6.4 Skills catalog and SKILL frontmatter

### Mandatory fixes
1. Harmonize tier policy (0/1/2 vs 0/1/2/3) and update validator accordingly.
2. Standardize frontmatter fields and naming.
3. Ensure all listed skills are discoverable and validated.

## 6.5 Product handoff scripts

### Mandatory fixes
1. Convert scripts to robust CLI interfaces.
2. Validate files before mutation.
3. Add idempotent behavior where possible and explicit failure semantics.

---

## 7. Non-Functional Requirements (Enterprise NFRs)

1. **Security**
   - High-severity vulnerabilities in tool runner: 0 open.
2. **Reliability**
   - Workflow path resolution errors: 0.
3. **Maintainability**
   - Skill validation pass rate: 100%.
4. **Observability**
   - All validators/tools return machine-parseable status.
5. **Onboarding**
   - Fresh setup time <= 15 minutes using README only.

---

## 8. Test and Verification Strategy

### 8.1 Unit Tests
- Tool runner security and path checks.
- Validators and parser edge cases.
- Product handoff CLI behavior.

### 8.2 Integration Tests
- Execute representative workflows with dry-run and path checks.
- Validate prompt/skill/workflow reference graph.

### 8.3 Security Tests
- Injection payload suite for test runner.
- Traversal/path escape suite.

### 8.4 Compliance Tests
- Full skills validation run as CI gate.
- Docs link/reference consistency checks.

---

## 9. Rollout Plan

1. **Phase 1 (Week 1):** P0 security fixes + validator bug fix.
2. **Phase 2 (Week 2):** workflow/doc reference repair + Python installation hardening.
3. **Phase 3 (Week 3):** CI gate rollout + artifact model normalization.
4. **Phase 4 (Week 4+):** full skill standardization and governance cleanup.

Release policy:
- No feature rollout without passing all P0/P1 gates.
- Use tagged versions with migration notes.

---

## 10. Risks and Mitigations

1. **Risk:** Breaking backward compatibility for command formats.
   - Mitigation: add compatibility matrix and migration warnings.
2. **Risk:** Large effort for skill refactoring.
   - Mitigation: batch by tier; enforce CI only after staged fixes.
3. **Risk:** Docs drift reappears.
   - Mitigation: automated reference checks in CI.
4. **Risk:** Diverse user environments.
   - Mitigation: explicit Python preflight checks and troubleshooting section.

---

## 11. Open Decisions (Must Be Finalized)

1. Tier model: keep Tier-3 or unify to Tier-2 max?
2. Canonical memory file naming: `AGENTS.md` + optional `.AGENTS.md`, or single-file standard?
3. CI provider and minimum branch protection policy.
4. Whether `run_tests` should support multi-language test commands (`pytest`, `npm test`, `cargo test`) in one policy.

---

## 12. Ready-to-Insert Section for README Installation Instructions (Python Environment)

Use the block below in `README.md` under **Installation & Setup**.

Status: **DONE** (already applied to `README.md` and `README.ru.md`).

````markdown
### 3. Installation Requirements (Python, Enterprise Mode)

This framework requires a reproducible Python environment for tool execution, validators, and test automation.

#### Supported Python
- **Required:** Python `3.11+` (recommended)
- **Minimum:** Python `3.9+` (legacy compatibility)

#### Virtual Environment (Mandatory)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

#### Install Dependencies
```bash
pip install pytest pyyaml
# Optional:
pip install openai python-dotenv
```

#### Smoke Check (Must Pass)
```bash
python --version
python -m pytest --version
python -c "import yaml; print('pyyaml: ok')"
python .agent/skills/skill-creator/scripts/init_skill.py --help
python .agent/skills/skill-creator/scripts/validate_skill.py .agent/skills/skill-creator
```

#### Troubleshooting
- `No module named pytest`
  - Run: `pip install pytest`
- `No module named yaml`
  - Run: `pip install pyyaml`
- If global Python conflicts occur:
  - Deactivate and recreate `.venv`, then reinstall only required packages.

> [!IMPORTANT]
> Do not install dependencies globally. Use `.venv` for all framework tooling.
````

---

## 13. Definition of Done (Program Completion)

Program is complete only if:
1. All P0/P1 backlog items delivered and accepted.
2. CI gates active and enforced on protected branches.
3. Skills validation is 100% pass.
4. README installation process is reproducible on clean machine.
5. Security regression suite shows no known injection/traversal bypass.
