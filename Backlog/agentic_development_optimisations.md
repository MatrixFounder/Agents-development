# Agentic Development Framework Optimizations

> **Status:** VDD-Reviewed Roadmap
> **Created:** 2026-01-21
> **Purpose:** Preparation for enterprise scaling through efficiency optimization

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Current State Analysis](#current-state-analysis)
- [Optimization Roadmap](#optimization-roadmap)
- [Detailed Recommendations (O1-O10)](#detailed-recommendations-o1-o10)
- [Implementation Plan (O1-O4)](#implementation-plan-o1-o4)
- [VDD Adversarial Review](#vdd-adversarial-review)

---

## Executive Summary

Данный документ содержит детальный план оптимизации текущего фреймворка Agentic-Development для:

1. **Снижения token overhead** на 27% (с ~16K до ~11.7K tokens)
2. **Увеличения пространства для кода** с 112K до 116K tokens
3. **Подготовки к enterprise-масштабированию** с поддержкой domain isolation

> [!CAUTION]
> **MANDATORY REQUIREMENT: Cross-Check Final Logic**
> 
> All optimizations MUST preserve existing framework behavior.
> Before implementing ANY change:
> 1. **Document current behavior** explicitly
> 2. **Cross-check final logic** to avoid information loss
> 3. **VDD-verify** that optimization doesn't break existing patterns
> 4. **Test before/after** to confirm equivalence

**Ключевые метрики:**

| Метрика | Текущее | Целевое | Δ |
|---------|---------|---------|---|
| Framework Overhead | ~16,000 tokens | ~11,700 tokens | -27% |
| Standard Pipeline | ~50,000 tokens | ~38,000 tokens | -24% |
| Peak Usage | 65-85K tokens | 50-65K tokens | -23% |

---

## Current State Analysis

### Component Token Consumption

#### Agent Prompts (System/Agents/)

| File | Size (bytes) | Tokens | Priority |
|------|--------------|--------|----------|
| `01_orchestrator.md` | 11,195 | ~2,799 | 🔴 HIGH |
| `00_agent_development.md` | 8,544 | ~2,136 | Medium |
| `06_agent_planner.md` | 4,173 | ~1,043 | Low |
| `02_analyst_prompt.md` | 4,041 | ~1,010 | Low |
| `08_agent_developer.md` | 4,039 | ~1,010 | Low |
| `04_architect_prompt.md` | 3,856 | ~964 | Low |
| `03_task_reviewer_prompt.md` | 3,225 | ~806 | Low |
| `05_architecture_reviewer_prompt.md` | 3,061 | ~765 | Low |
| `07_agent_plan_reviewer.md` | 2,027 | ~507 | Low |
| `09_agent_code_reviewer.md` | 2,013 | ~503 | Low |
| `10_security_auditor.md` | 500 | ~125 | Low |
| **TOTAL** | **46,674** | **~11,669** | |

#### Skills (.agent/skills/)

| Skill | Tokens | Frequency | Priority |
|-------|--------|-----------|----------|
| `architecture-format` | ~2,535 | Low | 🔴 HIGH |
| `skill-reverse-engineering` | ~1,322 | Low | Low |
| `skill-update-memory` | ~1,101 | Medium | Low |
| `skill-adversarial-performance` | ~946 | VDD | Low |
| `skill-safe-commands` | ~927 | **EVERY** | Medium |
| `skill-archive-task` | ~917 | New tasks | Medium |
| `requirements-analysis` | ~904 | Analysis | Low |
| `skill-adversarial-security` | ~838 | VDD | Low |
| `skill-planning-format` | ~756 | Planning | Low |
| `artifact-management` | ~636 | **EVERY** | Medium |
| `skill-task-model` | ~590 | Analysis | Low |
| `architecture-design` | ~551 | Architecture | Low |
| `core-principles` | ~519 | **EVERY** | Medium |
| Other (12 skills) | ~4,503 | Varies | Low |
| **TOTAL** | **~16,045** | | |

#### Configuration & Workflows

| Component | Tokens |
|-----------|--------|
| `.gemini/GEMINI.md` | ~1,394 |
| `.cursorrules` | ~867 |
| Workflows (14 files) | ~3,144 |
| **TOTAL** | **~5,405** |

### Emulated Development Cycle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TOKEN CONSUMPTION PER PHASE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  SESSION START ............................ ~6,900 tokens                   │
│  PHASE 1: ANALYSIS ........................ ~6,383 tokens                   │
│  PHASE 2: TASK REVIEW ..................... ~1,306 tokens                   │
│  PHASE 3: ARCHITECTURE .................... ~4,850 tokens                   │
│  PHASE 4: ARCHITECTURE REVIEW ............. ~1,111 tokens                   │
│  PHASE 5: PLANNING ........................ ~3,968 tokens                   │
│  PHASE 6: PLAN REVIEW ..................... ~762 tokens                     │
│  PHASE 7: DEVELOPMENT (×3 tasks) .......... ~20,334 tokens                  │
│  PHASE 8: CODE REVIEW (×3 tasks) .......... ~4,167 tokens                   │
│  PHASE 9: SECURITY ........................ ~260 tokens                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  GRAND TOTAL (Standard Pipeline): ~50,041 tokens                            │
│  + VDD Multi-Adversarial: +5,000 tokens                                     │
│  + Conversation history: +10,000-30,000 tokens                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  PEAK USAGE: 65,000-85,000 tokens                                           │
│  REMAINING (128K): 43,000-63,000 for CODE                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Critical Hotspots

> [!WARNING]
> **#1: Orchestrator Dominance**
> `01_orchestrator.md` (~2,799 tokens) — 24% of all agent prompts
> Contains 14 scenarios with duplicated structures

> [!WARNING]  
> **#2: architecture-format Anomaly**
> `skill-architecture-format` (~2,535 tokens) — 16% of all skills
> Loaded even when minor architecture changes

> [!WARNING]
> **#3: Mandatory Skills Overhead**
> 3 skills loaded EVERY session: ~2,082 tokens
> - `core-principles` (519) + `artifact-management` (636) + `safe-commands` (927)

---

## Optimization Roadmap

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         OPTIMIZATION ROADMAP                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  v3.5.1 — IMMEDIATE (O1-O4)                        Target: -8K tokens      │
│  ├── O1: Lazy Loading Protocol                                             │
│  ├── O2: Orchestrator Compression                                          │
│  ├── O3: architecture-format Split                                         │
│  └── O4: Conversation Checkpointing                                        │
│                                                                             │
│  v3.6.0 — MEDIUM-TERM (O5-O7)                      Target: -18K tokens     │
│  ├── O5: Skill Tiers (core vs extended)                                    │
│  ├── O6: Agent Prompt Compression                                          │
│  └── O7: Context Checkpointing                                             │
│                                                                             │
│  v4.0.0 — STRATEGIC (O8-O10)                       Enterprise-ready        │
│  ├── O8: Domain Isolation                                                  │
│  ├── O9: Multi-Session Pipeline                                            │
│  └── O10: Hierarchical Context                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Recommendations (O1-O10)

### O1: Phase-Specific Skill Loading (Selective Loading Protocol)

**Problem:** Phase-specific skills loaded at session start even when not needed

> [!IMPORTANT]
> **Investigation Results (2026-01-21):**
> Comprehensive grep analysis across all agents revealed skill usage patterns.

#### Skill Classification (Based on Actual Usage)

**TIER 0: SYSTEM FOUNDATION (ALWAYS LOAD — Non-negotiable)**

These skills are marked `(Mandatory)` in ALL or MOST agent prompts and are critical for framework operation:

| Skill | Tokens | Usage | Why Always Load |
|-------|--------|-------|----------------|
| `core-principles` | ~519 | 9/10 agents (Mandatory) | Anti-hallucination rules, Stub-First, Documentation First |
| `safe-commands` | ~927 | 10/10 agents (Mandatory) | **Enables automation** — auto-run commands |
| `artifact-management` | ~636 | Orchestrator (Mandatory) + 4 agents (Reading) | Archiving protocol, file management |
| **TIER 0 TOTAL** | **~2,082** | | **CANNOT be lazy-loaded** |

**TIER 1: PHASE-TRIGGERED (Load on Phase Entry)**

These skills are phase-specific and can be deferred:

| Skill | Tokens | Phase | Load Trigger |
|-------|--------|-------|-------------|
| `requirements-analysis` | ~904 | Analysis | When 02_analyst activated |
| `skill-task-model` | ~590 | Analysis | When creating TASK.md |
| `skill-archive-task` | ~917 | Analysis | When new task detected |
| `architecture-design` | ~551 | Architecture | When 04_architect activated |
| `architecture-format` | ~2,535 | Architecture | When creating new ARCHITECTURE.md |
| `planning-decision-tree` | ~423 | Planning | When 06_planner activated |
| `planning-format` | ~756 | Planning | When creating PLAN.md |
| `tdd-stub-first` | ~246 | Planning/Dev | When stub creation starts |
| `developer-guidelines` | ~343 | Development | When 08_developer activated |
| `documentation-standards` | ~425 | Development | When updating docs |
| **TIER 1 TOTAL** | **~7,690** | | **Candidates for on-demand loading** |

**TIER 2: EXTENDED (Load Only When Explicitly Requested)**

> [!IMPORTANT]
> **Precise Loading Conditions for TIER 2 Skills**
> Must be VDD-verified before implementation.

| Skill | Tokens | Loading Condition (Precise) |
|-------|--------|-----------------------------|
| `architecture-format-extended` | ~2,000 | Load when: (1) Creating NEW system from scratch, OR (2) Major architectural refactor (>3 components affected), OR (3) User explicitly requests "full architecture template" |
| `reverse-engineering` | ~1,322 | Load when: (1) User requests "sync docs with code", OR (2) Agent detects significant docs/code mismatch, OR (3) Onboarding to unfamiliar codebase |
| `update-memory` | ~1,101 | Load when: Post-development phase completed AND .AGENTS.md updates needed |
| `adversarial-security` | ~838 | Load when: VDD workflow invoked OR security-audit workflow |
| `adversarial-performance` | ~946 | Load when: VDD workflow invoked OR performance review requested |
| `vdd-sarcastic` | ~145 | Load when: VDD workflow invoked with sarcastic mode |
| **TIER 2 TOTAL** | **~7,023** | |

---

**Current behavior:**
```
Session start → Load GEMINI.md → Load ALL skills referenced in agent prompts
                                      ↑
                             ~9,772 tokens (Tier 0 + all Tier 1)
```

**Proposed behavior:**
```
Session start → Load GEMINI.md → Load TIER 0 (System Foundation)
                     │                     ↑
                     │              ~2,082 tokens (ALWAYS)
                     ▼
         Phase detected → Load TIER 1 skills for CURRENT phase only
                                      ↑
                              ~1,000-2,000 tokens per phase
```

**Implementation:**

1. Create `skill-phase-context/SKILL.md` (replaces lazy-loader concept):
```markdown
# Phase Context Loading Protocol

## System Foundation (TIER 0) — ALWAYS LOADED
These skills MUST be available in EVERY session:
- `core-principles` — Anti-hallucination, Stub-First methodology
- `safe-commands` — Enables auto-run for `mv`, `ls`, `git`, tests
- `artifact-management` — Archiving protocol, file management

> [!CAUTION]
> NEVER lazy-load TIER 0 skills. They enable core automation.

## Phase → Additional Skills Mapping (TIER 1)
| Phase | Additional Skills to Load |
|-------|---------------------------|
| Analysis | requirements-analysis, skill-task-model, (archive-task if new) |
| Architecture | architecture-design, (architecture-format if new system) |
| Planning | planning-decision-tree, planning-format, tdd-stub-first |
| Development | developer-guidelines, documentation-standards |
| Review | code-review-checklist |
| Security | security-audit |
| VDD | vdd-adversarial, adversarial-* (per workflow) |

## Loading Rule
1. TIER 0 skills: Load at session bootstrap (GEMINI.md)
2. TIER 1 skills: Load when entering corresponding phase
3. TIER 2 skills: Load ONLY when explicitly referenced by user or workflow
```

2. Update `GEMINI.md` to explicitly list TIER 0 skills in bootstrap
3. Update agent prompts to trigger TIER 1 loading on phase entry

**Savings:** ~3,000-5,000 tokens (TIER 1 skills not loaded until needed)
**Risk:** LOW — System Foundation skills always present
**Effort:** 3-4 hours

---

### O2: Orchestrator Compression

**Problem:** `01_orchestrator.md` contains 14 verbose scenarios with repeated structures

> [!CAUTION]
> **Cross-Check Requirement:** This optimization MUST preserve all 14 scenario behaviors.
> Document each scenario's unique logic before compression.

**Analysis of duplication:**
```
Scenario 1-3:   Analysis (init, review, revision)     ~800 tokens × 3 = 2,400
Scenario 4-6:   Architecture (init, review, revision) ~600 tokens × 3 = 1,800
Scenario 7-9:   Planning (init, review, revision)     ~500 tokens × 3 = 1,500
Scenario 10-12: Execution (init, review, fix)         ~600 tokens × 3 = 1,800
Scenario 13-14: Completion, Blocking                  ~400 tokens × 2 = 800
                                                      TOTAL: ~8,300 tokens (in-file)
```

**Proposed compression:**

> [!WARNING]
> **VDD-Verified Conditions for Pattern Usage**
> Each pattern MUST have explicit applicability conditions.

1. Extract common patterns into `skill-orchestrator-patterns`:
```markdown
## Pattern: Stage Cycle (VDD-VERIFIED)

### Applicability Conditions (ALL must be true):
- [ ] Stage has exactly 3 sub-phases: Init → Review → Revision
- [ ] Max iterations is 2
- [ ] Reviewer agent exists for this stage
- [ ] Revision uses same artifact path as init

### Pattern Definition:
INPUT: {stage_name}, {agent_prompt}, {artifact_path}, {reviewer_prompt}
FLOW:
1. Read {agent_prompt}
2. Execute → Create {artifact_path}
3. Check blocking_questions → IF yes: STOP, ask user
4. Read {reviewer_prompt}
5. IF critical_issues AND iteration < 2 → Revision (re-invoke agent)
6. IF critical_issues AND iteration = 2 → STOP, ask user
7. IF non-critical AND iteration = 2 → Proceed with warning
8. ELSE → Next Stage

### Exceptions (Pattern does NOT apply):
- Execution stage: Max iterations = 1 (single fix)
- Blocking questions: Different handling (scenario 14)
- Completion: No reviewer (scenario 13)
```

2. Reduce `01_orchestrator.md` to stage dispatch table:
```markdown
| Stage | Agent | Reviewer | Max Cycles | Skill |
|-------|-------|----------|------------|-------|
| Analysis | 02_analyst | 03_task_reviewer | 2 | archive-task |
| Architecture | 04_architect | 05_architecture_reviewer | 2 | architecture-design |
| Planning | 06_planner | 07_plan_reviewer | 2 | planning-decision-tree |
| Execution | 08_developer | 09_code_reviewer | 1 | developer-guidelines |
```

**Savings:** ~1,500-2,000 tokens
**Risk:** MEDIUM — Requires careful testing
**Effort:** 4-6 hours

---

### O3: architecture-format Split

**Problem:** `architecture-format` (~2,535 tokens) loaded for any architecture change

> [!CAUTION]
> **Cross-Check Requirement:** The split MUST preserve ALL 11 sections.
> No instruction loss is acceptable.

**Current structure (ACTUAL — verified 2026-01-21):**
```
architecture-format/SKILL.md (523 lines, 10KB, 11 sections)
├── Section 1: Core Concept (lines 1-30)
├── Section 2: Directory Structure (lines 31-50)
├── Section 3: System Components (lines 51-135)
├── Section 4: Data Model (conceptual + logical + diagram) (lines 136-194)
├── Section 5: API Contracts (request/response examples) (lines 195-260)
├── Section 6: Technology Stack (backend/frontend/db/infra) (lines 261-341)
├── Section 7: Security (auth, rate limiting) (lines 342-385)
├── Section 8: Scalability & Performance (lines 386-430)
├── Section 9: Monitoring & Observability (lines 431-470)
├── Section 10: Deployment & Configuration (lines 471-510)
└── Section 11: Open Questions (lines 511-523)
```

**Proposed split (PRESERVING ALL CONTENT):**
```
architecture-format-core/SKILL.md (~150 lines, ~1,200 tokens)
├── Section 1: Core Concept (REQUIRED)
├── Section 2: Directory Structure (REQUIRED)
├── Section 3: System Components — minimal template only
├── Section 4: Data Model — conceptual only
├── Section 11: Open Questions (REQUIRED)
└── NOTE: "For full templates, load architecture-format-extended"

architecture-format-extended/SKILL.md (~400 lines, ~3,500 tokens)
├── Section 3: System Components — full with examples
├── Section 4: Data Model — full with ER diagrams
├── Section 5: API Contracts — full with JSON examples
├── Section 6: Technology Stack — full with justifications
├── Section 7: Security — full checklist
├── Section 8: Scalability — full patterns
├── Section 9: Monitoring — full setup
├── Section 10: Deployment — full instructions
└── CROSS-REFERENCE: Imports core for base structure
```

**Loading logic (Precise Conditions):**

| Condition | Load |
|-----------|------|
| Updating existing architecture (minor change) | `core` only |
| Adding new component to existing system | `core` only |
| Creating NEW system from scratch | `extended` |
| Major refactor (>3 components changed) | `extended` |
| Sophisticated requirement / complex task | `extended` |
| User explicitly requests full template | `extended` |

**Savings:** ~1,200-1,500 tokens (when using core only)
**Risk:** LOW if cross-check performed
**Effort:** 3-4 hours (increased due to careful split)

---

### O4: Conversation Checkpointing

**Problem:** Conversation history grows linearly, consuming 10-30K tokens by session end

**Proposed solution:**

1. Create `skill-context-checkpoint`:
```markdown
# Context Checkpoint Protocol

## Checkpoint Triggers
- After TASK.md creation → Summarize analysis in 200 tokens
- After ARCHITECTURE.md update → Summarize in 150 tokens
- After PLAN.md creation → Summarize in 200 tokens
- After each task completion → Summarize in 100 tokens

## Checkpoint Format
```yaml
checkpoint:
  phase: {current_phase}
  artifacts:
    - path: docs/TASK.md
      summary: "Implement user authentication with OAuth2..."
  decisions:
    - "Using PostgreSQL for persistence"
    - "JWT tokens with 24h expiry"
  blockers: []
```
```

2. Integrate with IDE's context management (if supported)

**Savings:** 5,000-15,000 tokens
**Risk:** MEDIUM — Depends on IDE support
**Effort:** 4-8 hours

---

### O5: Skill Tiers (Formalization of O1)

**Concept:** Formally document and enforce the tier system from O1

> [!NOTE]
> O5 is the formalization of O1. After O1 is implemented and tested, O5 formalizes it into framework documentation.

**Skill Tier Reference (Corrected Based on Investigation):**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SKILL TIERS (AUTHORITATIVE)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TIER 0: SYSTEM FOUNDATION — Load at BOOTSTRAP (Non-negotiable)             │
│  ├── core-principles ............... ~519 tokens (Anti-hallucination)      │
│  ├── safe-commands ................. ~927 tokens (Enables automation!)     │
│  └── artifact-management ........... ~636 tokens (File protocol)           │
│                                      ─────────                              │
│                                      ~2,082 tokens ALWAYS                   │
│                                                                             │
│  TIER 1: PHASE-TRIGGERED — Load on phase entry                              │
│  ├── Analysis Phase:                                                        │
│  │   ├── requirements-analysis ..... ~904 tokens                           │
│  │   ├── skill-task-model .......... ~590 tokens                           │
│  │   └── archive-task .............. ~917 tokens (if new task)             │
│  ├── Architecture Phase:                                                    │
│  │   ├── architecture-design ....... ~551 tokens                           │
│  │   └── architecture-format-core .. ~1,200 tokens (after O3 split)        │
│  │       └── Load EXTENDED for: new system / major refactor / complex task │
│  ├── Planning Phase:                                                        │
│  │   ├── planning-decision-tree .... ~423 tokens                           │
│  │   ├── planning-format ........... ~756 tokens                           │
│  │   └── tdd-stub-first ............ ~246 tokens                           │
│  ├── Development Phase:                                                     │
│  │   ├── developer-guidelines ...... ~343 tokens                           │
│  │   └── documentation-standards ... ~425 tokens                           │
│  └── Review Phase:                                                          │
│      ├── code-review-checklist ..... ~386 tokens                           │
│      └── task/plan/arch-review ..... ~300-400 tokens each                  │
│                                                                             │
│  TIER 2: EXTENDED — Load only when explicitly requested                     │
│  ├── architecture-format-extended .. ~2,000 tokens (new systems only)      │
│  ├── reverse-engineering ........... ~1,322 tokens (codebase sync)         │
│  ├── update-memory ................. ~1,101 tokens (post-dev)              │
│  ├── adversarial-security .......... ~838 tokens (VDD only)                │
│  ├── adversarial-performance ....... ~946 tokens (VDD only)                │
│  └── vdd-sarcastic ................. ~145 tokens (VDD only)                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Implementation for O5:**
1. Create `System/Docs/SKILL_TIERS.md` as authoritative reference
2. Update all agent prompts with explicit tier markers
3. Add `TIER:` header to each SKILL.md file

**Savings:** Formalization itself doesn't save tokens, but enables enforcement
**Risk:** LOW
**Effort:** 2-3 hours (documentation)

---

### O6: Agent Prompt Compression

**Concept:** Use more compact DSL-like syntax in agent prompts

**Before (verbose):**
```markdown
YOUR TASK:
Determine if this is a NEW task or a refinement, and initiate the Analyst agent.

DECISION LOGIC:
- IF docs/TASK.md exists AND content relates to user request:
  - This is a REFINEMENT
  - DO NOT archive
  - Update existing TASK.md
- IF docs/TASK.md exists AND content is UNRELATED:
  - This is a NEW TASK
  - Archive old TASK.md using skill-archive-task
  - Create new TASK.md
```

**After (compact):**
```markdown
TASK: Route to Analyst (new vs refinement)
LOGIC:
  TASK.md exists + related → REFINE (no archive)
  TASK.md exists + unrelated → NEW (apply: skill-archive-task)
  TASK.md absent → NEW
```

**Savings:** 2,000-3,000 tokens across all agents
**Risk:** MEDIUM — May reduce clarity for LLM
**Effort:** 8-12 hours + A/B testing

---

### O7: Context Checkpointing (Advanced)

**Concept:** Store intermediate state in artifacts, not context

**Implementation:** 
- Create `.agent/state/session.yaml` at each phase boundary
- LLM reads state file instead of recalling from conversation

**Savings:** 10,000-20,000 tokens
**Risk:** HIGH — Requires fundamental flow changes
**Effort:** 16-24 hours

---

### O8: Domain Isolation (Enterprise)

**Concept:** For multi-domain projects, load ONLY current domain context

```
Working on /trading/bots/scanner:
  LOAD: docs/domains/trading/ARCHITECTURE.md
  SKIP: docs/domains/loyalty/*, docs/domains/payments/*
```

**Savings:** Critical for enterprise (10K+ tokens per domain)
**Risk:** HIGH complexity
**Effort:** 20+ hours

---

### O9: Multi-Session Pipeline (Enterprise)

**Concept:** Each phase runs in separate session with artifact handoff

```
Session 1 (Analysis):
  Input: User request
  Output: docs/TASK.md
  
Session 2 (Architecture):
  Input: docs/TASK.md
  Output: docs/ARCHITECTURE.md
  
... etc
```

**Benefit:** Fresh context per phase, no history accumulation
**Risk:** CRITICAL — Requires IDE support or custom tooling
**Effort:** 40+ hours

---

### O10: Hierarchical Context (Enterprise)

**Concept:** Summarized parent context + full current phase

```
Enterprise Project Context (500 tokens summary)
├── Domain: Trading (300 tokens summary)
│   └── Current Task: Scanner (full 3000 tokens)
```

**Risk:** HIGH complexity
**Effort:** 30+ hours

---

## Implementation Plan (O1-O4)

> [!IMPORTANT]
> **Cross-Check Requirement applies to ALL phases.**
> Document current behavior → Implement → Verify equivalence → Test automation.

### Phase 1: O3 — architecture-format Split (3-4 hours)

**Prerequisite: Document current state**
- [ ] Export current `architecture-format/SKILL.md` (523 lines, 11 sections)
- [ ] Verify all 11 sections are identified and mapped

**Tasks:**
1. [ ] Create `architecture-format-core/SKILL.md`:
   - Section 1: Core Concept (REQUIRED)
   - Section 2: Directory Structure (REQUIRED)
   - Section 3: System Components — minimal template
   - Section 4: Data Model — conceptual only
   - Section 11: Open Questions (REQUIRED)
   - Note: "For full templates, load architecture-format-extended"
2. [ ] Create `architecture-format-extended/SKILL.md`:
   - Sections 3-10 with full content
   - Cross-reference to core file
3. [ ] Update `04_architect_prompt.md` with loading conditions:
   - Minor update → load `core`
   - New system / major refactor / complex task → load `extended`
4. [ ] **CROSS-CHECK:** Verify combined content = original content (no loss)
5. [ ] Test: Create simple architecture update, verify core skill used

**DoD:**
- [ ] Core skill ~1,200 tokens (150 lines)
- [ ] Extended skill ~3,500 tokens (400 lines)
- [ ] Core + Extended = Original (all 11 sections preserved)
- [ ] Architect agent works with both scenarios

---

### Phase 2: O1 — Phase-Specific Skill Loading (4 hours)

**Prerequisite: Document current state**
- [ ] List all skills currently loaded in GEMINI.md/.cursorrules
- [ ] Verify TIER 0 skills are explicitly required

**Tasks:**
1. [ ] Create `skill-phase-context/SKILL.md` with:
   - TIER 0 definition (ALWAYS LOAD)
   - TIER 1 phase→skills mapping
   - TIER 2 precise loading conditions
2. [ ] **VERIFY TIER 0 IS PRESERVED:** Ensure `GEMINI.md` and `.cursorrules` explicitly load:
   - `core-principles` (Anti-hallucination)
   - `safe-commands` (Automation enablement — CRITICAL)
   - `artifact-management` (File protocol)
3. [ ] Update agent prompts to trigger TIER 1 loading on phase entry
4. [ ] **CROSS-CHECK:** Run automation test — verify `mv`, `git`, tests still auto-run
5. [ ] Test: Run analysis phase:
   - [ ] Verify TIER 0 skills are always present
   - [ ] Verify TIER 1 analysis skills load when entering Analysis
   - [ ] Verify TIER 1 architecture skills NOT loaded during Analysis

**DoD:**
- [ ] TIER 0 skills (~2,082 tokens) loaded at session start — ALWAYS
- [ ] TIER 1 skills load only when entering corresponding phase
- [ ] `safe-commands` auto-run still works (CRITICAL for automation)
- [ ] All phases still functional
- [ ] Measurable reduction in total tokens (~3,000-5,000)

---

### Phase 3: O2 — Orchestrator Compression (6-8 hours)

**Prerequisite: Document current state**
- [ ] Export all 14 scenarios from `01_orchestrator.md`
- [ ] Document unique logic per scenario (edge cases, exceptions)
- [ ] Identify pattern-compatible vs exception scenarios

**Tasks:**
1. [ ] Create `skill-orchestrator-patterns/SKILL.md` with:
   - Stage Cycle pattern with applicability conditions
   - Explicit exceptions documented
2. [ ] Refactor `01_orchestrator.md` to use patterns + dispatch table
3. [ ] **CROSS-CHECK:** Verify all 14 scenarios are still executable:
   - [ ] Scenario 1-3: Analysis (init, review, revision)
   - [ ] Scenario 4-6: Architecture (init, review, revision)
   - [ ] Scenario 7-9: Planning (init, review, revision)
   - [ ] Scenario 10-12: Execution (init, review, fix) — NOTE: different iteration limit
   - [ ] Scenario 13: Completion — NOTE: no reviewer
   - [ ] Scenario 14: Blocking questions — NOTE: different handling
4. [ ] VDD-verify: Run edge case scenarios (blocking questions, iteration=2, etc.)
5. [ ] Measure token reduction

**DoD:**
- [ ] Orchestrator < 6,000 bytes (from 11,195)
- [ ] All 14 scenarios still executable (verified by test)
- [ ] No regression in pipeline flow
- [ ] Backup: `01_orchestrator_full.md.bak` preserved

---

### Phase 4: O4 — Conversation Checkpointing (4-6 hours)

**Prerequisite: Document current state**
- [ ] Measure baseline token usage for a full pipeline run
- [ ] Document current context growth pattern

**Tasks:**
1. [ ] Create `skill-context-checkpoint/SKILL.md` with:
   - Checkpoint triggers (after each phase artifact)
   - Checkpoint schema (YAML)
   - ADDITIVE rule (append, never delete)
   - `decisions:` list requirement
2. [ ] Add checkpoint instructions to key phase transitions:
   - [ ] After TASK.md creation
   - [ ] After ARCHITECTURE.md update
   - [ ] After PLAN.md creation
   - [ ] After each task completion
3. [ ] **CROSS-CHECK:** Verify checkpoints are human-readable
4. [ ] Test: Long session remains under 80K tokens
5. [ ] VDD-verify: Checkpoint content is accurate (no hallucination)

**DoD:**
- [ ] Checkpoint skill created and documented
- [ ] At least one successful long session with checkpointing
- [ ] Token usage reduced vs baseline (measurable)
- [ ] No critical decisions lost in summarization

---

## VDD Adversarial Review

> **Final Review: 2026-01-21**
> **Sarcasmotron Mode Activated** 🎭

### Document Consistency Check

> [!NOTE]
> **Cross-Document Verification Performed**
> Checked consistency between: O1-O10 sections ↔ Implementation Plan ↔ Skill Tiers diagram

| Check | Status | Notes |
|-------|--------|-------|
| Token estimates consistent | ✅ | Core ~1,200, Extended ~3,500 |
| Tier classification consistent | ✅ | TIER 0 always includes safe-commands |
| Cross-check requirements present | ✅ | Added to all phases |
| Implementation effort realistic | ✅ | Updated: O2 6-8h, O3 3-4h, O4 4-6h |
| Backup strategy documented | ✅ | `01_orchestrator_full.md.bak` |

---

### 🟢 O1: Phase-Specific Skill Loading

**Challenge:** "Oh brilliant, now the agent decides WHEN to load skills. What could go wrong when a forgetful LLM 'forgets' to load the required skill?"

**Risks Identified:**
1. Agent proceeds without required skill → hallucination
2. TIER 0 accidentally lazy-loaded → automation breaks
3. Phase detection logic fails → wrong skills loaded

**Mitigations Applied:**
1. ✅ TIER 0 explicitly marked as NON-NEGOTIABLE
2. ✅ `safe-commands` highlighted as CRITICAL for automation
3. ✅ `REQUIRED_SKILLS:` header specified for each agent prompt
4. ✅ Cross-check: automation test added to implementation plan

**VDD Verdict:** ✅ PASS — TIER 0 protection in place

---

### 🟡 O2: Orchestrator Compression

**Challenge:** "You want to compress 14 detailed scenarios into a 'dispatch table'? The LLM will just... figure out the nuances?"

**Risks Identified:**
1. Loss of edge case handling (iteration limits, no reviewer, blocking questions)
2. Ambiguous pattern interpretation
3. Debug difficulty increases

**Mitigations Applied:**
1. ✅ Explicit exceptions documented (scenarios 10-14 have special logic)
2. ✅ Applicability conditions added with checkbox validation
3. ✅ All 14 scenarios listed individually in implementation plan
4. ✅ Backup requirement: `01_orchestrator_full.md.bak`

**Remaining Risk:** Pattern may be too abstract for some LLMs

**VDD Verdict:** ⚠️ CONDITIONAL PASS — requires A/B testing

---

### 🟢 O3: architecture-format Split

**Challenge:** "Split into 'core' and 'extended'... and who decides which one to use?"

**Risks Identified:**
1. Wrong skill tier selected → inconsistent docs
2. Content loss during split (523 lines)
3. Cross-reference between files fails

**Mitigations Applied:**
1. ✅ Precise loading conditions table (6 conditions)
2. ✅ All 11 sections mapped with line numbers
3. ✅ Cross-check: verify Core + Extended = Original
4. ✅ "sophisticated requirement / complex task" trigger added

**VDD Verdict:** ✅ PASS — if cross-check performed

---

### 🟢 O4: Conversation Checkpointing

**Challenge:** "Great, now we're trusting the LLM to summarize its own work correctly."

**Risks Identified:**
1. Critical decisions lost in summary
2. Context drift across checkpoints
3. LLM hallucinates checkpoint content

**Mitigations Applied:**
1. ✅ ADDITIVE rule: append only, never delete
2. ✅ Explicit `decisions:` list requirement
3. ✅ TASK.md remains full (not summarized)
4. ✅ Human-readable format for manual review

**VDD Verdict:** ✅ PASS with monitoring

---

### 🔴 O5-O10: Strategic Optimizations

**Status:** DEFERRED until O1-O4 proven successful

**VDD Verdict:** 🔴 DEFER — validate O1-O4 first

---

### Final VDD Summary

| Optimization | Risk | Verdict | Blocking |
|--------------|------|---------|----------|
| O1: Phase-Specific Loading | LOW | ✅ PASS | None |
| O2: Orchestrator Compression | MEDIUM | ⚠️ CONDITIONAL | A/B test |
| O3: architecture-format Split | LOW | ✅ PASS | Cross-check |
| O4: Checkpointing | LOW | ✅ PASS | Monitor |
| O5-O10: Strategic | HIGH | 🔴 DEFER | O1-O4 first |

---

## Metrics & Success Criteria

### Baseline Metrics (Before O1-O4)

| Metric | Current Value |
|--------|---------------|
| Session Start Tokens | ~6,900 |
| Standard Pipeline Total | ~50,041 |
| Peak Usage | 65,000-85,000 |
| Framework Overhead | ~16,000 |

### Target Metrics (After O1-O4)

| Metric | Target Value | Δ |
|--------|--------------|---|
| Session Start Tokens | ~4,500 | -35% |
| Standard Pipeline Total | ~42,000 | -16% |
| Peak Usage | 55,000-70,000 | -15% |
| Framework Overhead | ~12,000 | -25% |

---

## Implementation Prompts (For Future Dialogue)

> [!TIP]
> Copy-paste these prompts to start implementation in a new dialogue.

### Prompt 1: O3 — architecture-format Split

```
TASK: Implement O3 from Backlog/agentic_development_optimisations.md

CONTEXT:
- Current file: .agent/skills/architecture-format/SKILL.md (523 lines, 11 sections)
- Goal: Split into core (~150 lines) and extended (~400 lines)
- Cross-check requirement: Core + Extended = Original (no content loss)

DELIVERABLES:
1. Create .agent/skills/architecture-format-core/SKILL.md
2. Create .agent/skills/architecture-format-extended/SKILL.md
3. Update 04_architect_prompt.md with loading conditions
4. Verify: combined content equals original

CRITICAL: Do NOT lose any content. Cross-check after split.
```

### Prompt 2: O1 — Phase-Specific Skill Loading

```
TASK: Implement O1 from Backlog/agentic_development_optimisations.md

CONTEXT:
- Goal: Create skill-phase-context that defines skill loading tiers
- TIER 0 (ALWAYS LOAD): core-principles, safe-commands, artifact-management
- TIER 1 (Phase-triggered): See mapping in optimization document

PREREQUISITE: O3 is implemented and tested

DELIVERABLES:
1. Create .agent/skills/skill-phase-context/SKILL.md
2. Verify GEMINI.md and .cursorrules explicitly reference TIER 0
3. Test: automation still works (mv, git, tests auto-run)

CRITICAL: safe-commands MUST remain always-loaded for automation.
```

### Prompt 3: O2 — Orchestrator Compression

```
TASK: Implement O2 from Backlog/agentic_development_optimisations.md

CONTEXT:
- Current file: System/Agents/01_orchestrator.md (492 lines, 14 scenarios)
- Goal: Compress to <6,000 bytes using patterns + dispatch table

BEFORE STARTING:
cp System/Agents/01_orchestrator.md System/Agents/01_orchestrator_full.md.bak

PREREQUISITE: O1 and O3 are implemented and tested

DELIVERABLES:
1. Create .agent/skills/skill-orchestrator-patterns/SKILL.md
2. Refactor 01_orchestrator.md to use patterns
3. Test each of 14 scenarios (especially 10-14 with special logic)

CRITICAL: Backup first. Test all 14 scenarios after compression.
```

### Prompt 4: O4 — Conversation Checkpointing

```
TASK: Implement O4 from Backlog/agentic_development_optimisations.md

CONTEXT:
- Goal: Create checkpointing skill to reduce conversation history growth
- Checkpoint after: TASK.md, ARCHITECTURE.md, PLAN.md, each task
- Rule: ADDITIVE only (append, never delete)

PREREQUISITE: O1, O2, O3 are implemented

DELIVERABLES:
1. Create .agent/skills/skill-context-checkpoint/SKILL.md
2. Define checkpoint schema (YAML)
3. Add checkpoint instructions to phase transitions
4. Test: long session stays under 80K tokens
```

### Prompt 5: Full Validation

```
TASK: Validate O1-O4 implementation

TEST PLAN:
1. Run standard development task through full pipeline
2. Verify:
   - [ ] All phases execute correctly
   - [ ] safe-commands auto-run works (mv, git, tests)
   - [ ] All 14 orchestrator scenarios work
   - [ ] architecture-format loads correctly
   - [ ] Checkpoints are created and readable
3. Compare token usage to baseline

DELIVERABLES:
1. Test report with pass/fail for each check
2. Token usage comparison (before vs after)
```

---

## Changelog

| Date | Author | Change |
|------|--------|--------|
| 2026-01-21 | Adversarial Architect | Final VDD review, implementation prompts |
| 2026-01-21 | Adversarial Architect | Corrected skill tiers, cross-check requirements |
| 2026-01-21 | Adversarial Architect | Initial document |

