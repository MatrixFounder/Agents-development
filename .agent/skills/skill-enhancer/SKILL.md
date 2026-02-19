---
name: skill-enhancer
description: Use when you need to audit, fix, or improve an existing agent skill to meet Gold Standard compliance.
tier: 2
version: 1.1
---
# Skill Enhancer

**Purpose**: This meta-skill analyzes other skills for compliance with TDD, CSO, and Script-First standards, guiding the agent through upgrades.

## 1. Red Flags (Anti-Rationalization)
**STOP and READ THIS if you are thinking:**
- "I'll just add the sections blindly" -> **WRONG**. You must understand *why* the skill fails before fixing it.
- "The description is close enough" -> **WRONG**. It must start with "Use when".
- "Examples are optional" -> **WRONG**. "Rich Skills" mandate examples.
- "It's just a small 20-line example" -> **WRONG**. Inline blocks > 12 lines are prohibited. Extract them.
- "I'll instruct the agent to parse the file line-by-line in text" -> **WRONG**. Use "Script-First".

## 2. Capabilities
- **Audit**: Detect gaps (missing Red Flags, inline blocks > 12 lines, poor CSO, weak language) using `analyze_gaps.py`.
- **Execution Policy Audit**: Detect missing `Execution Mode`, `Script Contract`, `Safety Boundaries`, and `Validation Evidence` sections.
- **Security Remediation**: Fix vulnerabilities flagged by `skill-validator` (e.g., `curl | bash`, secrets, weak permissions).
- **Plan**: Propose specific content improvements using `references/refactoring_patterns.md`.
- **Execute**: Apply refactoring patterns to upgrade the skill.

## 2.5. Execution Mode
- **Mode**: `hybrid`
- **Rationale**: gap triage and refactoring decisions are prompt-driven, while gap detection is script-driven.

## 2.6. Script Contract
- **Primary Command**: `python3 scripts/analyze_gaps.py <target-skill-path> [--json]`
- **Inputs**: target skill path + optional output mode.
- **Outputs**: structured gap list and pass/fail status.
- **Failure Semantics**: non-zero exit when gaps exist (for deterministic gate behavior).

## 2.7. Safety Boundaries
- **Scope**: apply edits only to explicitly selected target skill.
- **Default Exclusions**: do not refactor unrelated skills or global docs by default.
- **Destructive Actions**: full-file overwrite is prohibited unless explicitly requested and reviewed.

## 2.8. Validation Evidence
- **Primary Evidence**: before/after `analyze_gaps.py` output.
- **Secondary Evidence**: targeted diffs proving that each reported gap was addressed.
- **Quality Gate**: no unresolved critical structure gaps after refactor.

## 3. Instructions

### Phase 1: Audit
1.  **Run Analyzer**: `python3 scripts/analyze_gaps.py <target-skill-path>`.
2.  **Manual Checks**:
    *   **Weak Language**: Does it use "should", "can", "try"? (Must be "MUST", "EXECUTE").
    *   **Script-First Gap**: Identify if complex logic steps (> 5 lines of text) **MUST** be converted to a `script/`.
3.  **Review Gaps**: Read the analyzer output and your manual findings.

### Phase 1.5: Execution-Policy Audit
1.  Verify `Execution Mode` section exists and is explicit (`prompt-first`, `script-first`, or `hybrid`).
2.  If skill uses `scripts/`, verify `Script Contract` section defines command, inputs, outputs, and exit behavior.
3.  Verify `Safety Boundaries` section defines scope limits and non-default destructive behavior.
4.  Verify `Validation Evidence` section defines objective verification outputs.
5.  Mark missing pieces as migration gaps (warning-first for legacy skills).

### Phase 2: Plan
1.  **Read Target Skill**: Read the content of the target skill.
2.  **Draft Improvements**:
    *   *Token Efficiency*: Identify blocks > 12 lines and plan extraction to `examples/`, `assets/`, or `references/`.
    *   *Script-First*: Identify logic blocks > 5 lines and plan extraction to `scripts/`.
    *   *Execution Policy*: Add missing policy sections and scope constraints.
    *   *Anti-Laziness*: Replace weak words with strong imperatives.
    *   *Red Flags*: Identify 2-3 likely agent excuses for *this specific task*.
    *   *CSO*: Rewrite description to "Use when [TRIGGER]...".
3.  **Confirm**: Ensure improvements align with the "Skills as Code" philosophy.

### Phase 3: Execute
1.  **Update File**: Edit the target `SKILL.md` to insert the new sections.
    *   **CRITICAL**: Use `replace_file_content` or `multi_replace_file_content`.
    *   **DO NOT** use `write_to_file` to overwrite existing content (Data Loss Risk).
    *   *Tip*: Use `references/refactoring_patterns.md` (Coming in Iteration 2) for style guide.
2.  **Verify**: Re-run `analyze_gaps.py`. Expect output "No Gaps Found".

### Phase 3.5: Security Repair (If triggered by Validator)
1.  **Analyze Report**: Read the `skill-validator` JSON output.
2.  **Consult Guide**: Use `references/security_refactoring.md` to find safe alternatives for flagged patterns.
3.  **Apply Fixes**:
    *   *Shell Injection*: Replace direct execution with argument arrays.
    *   *Downloads*: Replace `curl | bash` with download -> inspect -> execute.
    *   *Secrets*: Move hardcoded keys to environment variables.

### Phase 4: Final VDD Check
1.  **Read Checklist**: Open `references/vdd_checklist.md`.
2.  **Self-Correction**: Verify your work against the 5 criteria (Data Safety, Anti-Laziness, etc.).
3.  **Refine**: If any check fails (e.g., found "TODO", found "should"), fix it immediately.

## 4. Best Practices

| DO THIS | DO NOT DO THIS |
| :--- | :--- |
| **Specific Red Flags**: "Don't skip tests" | **Generic Red Flags**: "Don't be lazy" |
| **Trigger-Based Desc**: "Use when debugging race conditions" | **Summary Desc**: "Guide for debugging" |
| **Strong Verbs**: "MUST", "EXECUTE", "VERIFY" | **Weak Verbs**: "should", "consider", "try" |

### Rationalization Table
| Agent Excuse | Reality / Counter-Argument |
| :--- | :--- |
| "The skill is too simple for Red Flags" | Simple skills are skipped most often. Explicit rules prevent this. |
| "I don't have time to write examples" | Examples save time by preventing hallucinations later. |
| "It's easier to write logic in text" | Text logic is unreliable. Scripts are deterministic. |

## 5. Examples (Few-Shot)
> [!TIP]
> See `examples/usage_example.md` for a complete **Before & After** walkthrough of upgrading a legacy skill.

**Input:**
```bash
python3 scripts/analyze_gaps.py ../target-skill
```

**Output:**
```text
⚠️  Gaps Detected...
Recommendation: Run 'Execute Improvement Plan'...
```

## 6. Resources
- `scripts/analyze_gaps.py`: The gap detection tool.
- `references/writing_skills_best_practices_anthropic.md`: The authoritative "Gold Standard" guide used to verify compliance.
- `references/testing-skills-with-subagents.md`: Methodology for verifying fixes using TDD (Red-Green-Refactor).
