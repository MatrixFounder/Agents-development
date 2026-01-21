# Product Development Vision

> **Status:** VDD-Reviewed Vision Document
> **Created:** 2026-01-21
> **Purpose:** Target architecture for enterprise product development extension

---

## Table of Contents

- [Vision Statement](#vision-statement)
- [Core Principles](#core-principles)
- [Target Architecture](#target-architecture)
- [Agent Model](#agent-model)
- [Skills & Workflows](#skills--workflows)
- [Folder Structure](#folder-structure)
- [Integration Strategy](#integration-strategy)
- [VDD Review](#vdd-review)
- [Open Questions](#open-questions)

---

## Vision Statement

Расширить фреймворк Agentic-Development для поддержки **бизнес-ориентированного планирования продуктов** с минимальным overhead и максимальной устойчивостью к галлюцинациям.

### Goals

1. **Business Layer Integration** — добавить Product Analysis фазу перед техническим pipeline
2. **Artifact-Centric Communication** — агенты общаются через файлы, не через "оркестрацию"
3. **Domain Isolation** — поддержка многодоменных enterprise-проектов
4. **Near-Zero Hallucinations** — VDD на каждом уровне, включая бизнес-артефакты

### Non-Goals

- ❌ SAFe-style иерархия (PO → Orchestrator → Coordinator)
- ❌ Real-time параллелизм агентов (невозможен в текущих IDE)
- ❌ External integrations (API, market data) — Phase 3+
- ❌ Замена текущего фреймворка — extension, не rewrite

---

## Core Principles

### 1. Artifact-Centric Architecture

> **Ключевой инсайт:** Агенты не общаются напрямую. Они общаются через артефакты.

```
User Request
     │
     ▼
┌─────────────────┐
│ PRODUCT_VISION  │ ◄── Created by Product Analyst (Session 1)
│      .md        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PRODUCT_BACKLOG │ ◄── Created by Product Analyst (Session 1)
│      .md        │     Reviewed by Product Reviewer (Session 2)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ APPROVED_BACKLOG│ ◄── Output of VDD Review
│      .md        │
└────────┬────────┘
         │
         ▼
   ┌─────┴─────┐
   │           │
   ▼           ▼
Domain 1    Domain 2    ◄── Standard Agentic Pipeline per domain
TASK.md     TASK.md
```

### 2. Sequential Sessions (Not Parallel Agents)

**Reality Check:**
- Cursor/Antigravity/VSCode = 1 LLM session at a time
- "Orchestrator" — это prompt, не процесс
- "Parallel pipelines" возможны только через:
  - Разные IDE instances
  - Человек переключается между доменами
  - Artifact-based async handoff

### 3. VDD at Every Level

```
User Input ─────┐
                │
                ▼
        ┌───────────────┐
        │ Product       │──────▶ VDD: "Is this achievable?"
        │ Analyst       │               "ROI realistic?"
        └───────────────┘               "Market validated?"
                │
                ▼
        ┌───────────────┐
        │ Product       │──────▶ VDD: "WSJF correct?"
        │ Reviewer      │               "Dependencies considered?"
        └───────────────┘               "Edge cases?"
                │
                ▼
        [ Standard Technical Pipeline with existing VDD ]
```

### 4. Token Budget Awareness

> [!IMPORTANT]
> Product Development фаза добавляет overhead. Budget:
> - `p01_product_analyst.md` — MAX 3,000 tokens
> - `p02_product_reviewer.md` — MAX 2,000 tokens  
> - `skill-product-analysis` — MAX 1,500 tokens
> - `skill-backlog-prioritization` — MAX 1,000 tokens
> 
> **Total Product Phase overhead: < 8,000 tokens**

---

## Target Architecture

### Phase Model

| Phase | Session | Agent | Input | Output |
|-------|---------|-------|-------|--------|
| 1. Vision | 1 | p01_product_analyst | User request | `PRODUCT_VISION.md` |
| 2. Backlog | 1 | p01_product_analyst | Vision | `PRODUCT_BACKLOG.md` |
| 3. Review | 2 | p02_product_reviewer | Backlog | Approval or Comments |
| 4. Domain Split | 3 | Orchestrator | Approved Backlog | Domain TASK.md files |
| 5+ | N+ | Standard Pipeline | Domain TASK.md | Code |

### Artifact Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ARTIFACT FLOW                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  docs/                                                                      │
│  ├── PRODUCT_VISION.md        # High-level vision (created Phase 1)        │
│  │   └── Sections:                                                          │
│  │       ├── Problem Statement                                              │
│  │       ├── Target Users                                                   │
│  │       ├── Success Metrics                                                │
│  │       └── Constraints                                                    │
│  │                                                                          │
│  ├── PRODUCT_BACKLOG.md       # Prioritized backlog (created Phase 2)      │
│  │   └── Sections:                                                          │
│  │       ├── Epics (WSJF-prioritized)                                       │
│  │       ├── Stories (INVEST-compliant)                                     │
│  │       └── Domain Assignments                                             │
│  │                                                                          │
│  └── domains/                                                               │
│      ├── {domain}/                                                          │
│      │   ├── ARCHITECTURE.md  # Domain-specific                             │
│      │   ├── current/                                                       │
│      │   │   ├── TASK.md      # Active task                                 │
│      │   │   └── PLAN.md                                                    │
│      │   └── archive/                                                       │
│      └── ...                                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Agent Model

### New Agents (Minimal Set)

#### p01_product_analyst.md

```markdown
# Product Analyst

## ROLE
Analyze user product requests and create structured backlog.

## ACTIVE SKILLS
- skill-product-analysis (REQUIRED)
- skill-backlog-prioritization (REQUIRED)
- core-principles (REQUIRED)

## INPUT
- User product request
- PRODUCT_VISION.md (if exists, for updates)

## OUTPUT
1. PRODUCT_VISION.md — Vision document
2. PRODUCT_BACKLOG.md — Prioritized backlog

## PROCESS
1. Read user request
2. IF PRODUCT_VISION.md exists → determine if UPDATE or NEW
3. Extract: Problem, Users, Metrics, Constraints
4. Create/Update PRODUCT_VISION.md
5. Breakdown vision into Epics → Stories
6. Prioritize using WSJF (skill-backlog-prioritization)
7. Assign domains to stories
8. Create PRODUCT_BACKLOG.md

## TOKEN BUDGET: < 3,000 tokens
```

#### p02_product_reviewer.md

```markdown
# Product Reviewer (VDD-Adversarial)

## ROLE
Challenge product artifacts using adversarial analysis.

## ACTIVE SKILLS
- vdd-adversarial (REQUIRED)
- skill-backlog-prioritization (for verification)

## INPUT
- PRODUCT_BACKLOG.md
- PRODUCT_VISION.md

## OUTPUT
- Review comments OR approval

## VDD CHECKLIST
1. [ ] Vision clear and achievable?
2. [ ] ROI/metrics measurable?
3. [ ] Epics properly decomposed?
4. [ ] Stories meet INVEST criteria?
5. [ ] WSJF priorities justified?
6. [ ] Domain assignments logical?
7. [ ] Dependencies identified?
8. [ ] Edge cases / risks documented?

## TONE
Use `vdd-sarcastic` approach:
- "So you expect 100x growth in 3 months? With what team?"
- "ROI based on 'market trends'? Which trends exactly?"

## TOKEN BUDGET: < 2,000 tokens
```

### Rejected Agents

| Original Proposal | Rejection Reason |
|-------------------|------------------|
| `p00_product_development.md` | Meta-prompt unnecessary — GEMINI.md handles bootstrap |
| `p01_product_orchestrator.md` | Orchestration via artifacts, not dedicated agent |
| `p04_product_architect.md` | Use existing `04_architect_prompt.md` with domain context |
| `p05_product_architecture_review.md` | Use existing `05_architecture_reviewer_prompt.md` |
| `01_module_coordinator.md` | Function covered by artifact structure |

---

## Skills & Workflows

### New Skills

#### skill-product-analysis (MAX 1,500 tokens)

```markdown
# Product Analysis

## Vision Document Structure
- Problem Statement (50-100 words)
- Target Users (personas)
- Success Metrics (SMART)
- Constraints (time, budget, tech)

## Epic Breakdown
For each epic:
- Clear business goal
- Measurable outcome
- Rough scope estimate (T-shirt size: S/M/L/XL)

## Story Extraction
Apply INVEST:
- Independent
- Negotiable
- Valuable
- Estimable
- Small
- Testable
```

#### skill-backlog-prioritization (MAX 1,000 tokens)

```markdown
# Backlog Prioritization

## WSJF Formula
WSJF = (Business Value + Time Criticality + Risk Reduction) / Effort

## Ranking Table
| Epic | BV | TC | RR | Effort | WSJF | Priority |
|------|----|----|----|----|------|----------|
| ...  | 1-10 | 1-10 | 1-10 | 1-10 | calc | sorted |

## Priority Rules
1. WSJF > 5 → High Priority
2. WSJF 2-5 → Medium Priority
3. WSJF < 2 → Low Priority / Backlog
```

#### skill-domain-decomposition (MAX 1,000 tokens)

```markdown
# Domain Decomposition

## Bounded Context Rules
1. Each domain has clear ownership
2. Minimal dependencies between domains
3. Shared kernel explicitly documented

## Domain → Folder Mapping
Epic "User Authentication" → domain: auth
Epic "Trading Bots" → domain: trading
Epic "Loyalty Points" → domain: loyalty
```

### New Workflows

#### product-vision.md

```yaml
---
description: Create or update Product Vision and Backlog
---
1. Read docs/PRODUCT_VISION.md (if exists)
2. Load skill: skill-product-analysis
3. Execute p01_product_analyst
4. Create/Update docs/PRODUCT_VISION.md
5. Load skill: skill-backlog-prioritization
6. Create docs/PRODUCT_BACKLOG.md
7. Notify user: "Vision and Backlog ready for review"
```

#### product-review.md

```yaml
---
description: VDD Review of Product Backlog
---
1. Read docs/PRODUCT_BACKLOG.md
2. Read docs/PRODUCT_VISION.md
3. Load skill: vdd-adversarial
4. Execute p02_product_reviewer
5. IF issues found:
   - Create review comments
   - Return to product-vision workflow
6. IF approved:
   - Rename to docs/APPROVED_BACKLOG.md
   - Proceed to domain-start workflow
```

#### domain-start.md

```yaml
---
description: Create domain-specific TASK.md from approved backlog
---
1. Read docs/APPROVED_BACKLOG.md
2. Load skill: skill-domain-decomposition
3. For each domain in backlog:
   - Create docs/domains/{domain}/current/TASK.md
   - Apply standard /01-start-feature workflow
```

---

## Folder Structure

```
project-root/
├── .gemini/GEMINI.md                    # Extended with product phase
├── .agent/
│   ├── skills/
│   │   ├── skill-product-analysis/       # NEW
│   │   ├── skill-backlog-prioritization/ # NEW
│   │   ├── skill-domain-decomposition/   # NEW
│   │   └── ... (existing skills)
│   └── workflows/
│       ├── product-vision.md             # NEW
│       ├── product-review.md             # NEW
│       ├── domain-start.md               # NEW
│       └── ... (existing workflows)
├── System/
│   └── Agents/
│       ├── p01_product_analyst.md        # NEW
│       ├── p02_product_reviewer.md       # NEW
│       └── ... (existing agents)
├── docs/
│   ├── PRODUCT_VISION.md                 # NEW: High-level vision
│   ├── PRODUCT_BACKLOG.md                # NEW: Prioritized backlog
│   ├── APPROVED_BACKLOG.md               # NEW: After VDD review
│   └── domains/
│       ├── {domain}/
│       │   ├── ARCHITECTURE.md           # Domain-specific
│       │   ├── KNOWN_ISSUES.md
│       │   └── current/                  # Single active task
│       │       ├── TASK.md
│       │       └── PLAN.md
│       └── archive/                      # Completed tasks
└── src/{domain}/                          # Code by domain
```

---

## Integration Strategy

### Phase 0: Skills & Agents (No Pipeline Changes)

1. Create 3 new skills (product-analysis, backlog-prioritization, domain-decomposition)
2. Create 2 new agents (p01_product_analyst, p02_product_reviewer)
3. Test in isolation — не интегрировать в main pipeline

**DoD:** Skills pass token budget, agents produce valid artifacts

### Phase 1: Workflows Integration

1. Create 3 new workflows
2. Update GEMINI.md to recognize `/product-*` commands
3. Test: `/product-vision` creates valid PRODUCT_VISION.md

**DoD:** User can invoke product workflows explicitly

### Phase 2: Domain Structure

1. Create domain folder template
2. Update Orchestrator to read from APPROVED_BACKLOG.md
3. Test: Multi-domain task creation works

**DoD:** Standard pipeline works with domain-specific TASK.md

### Phase 3: Full Integration (After O1-O4 optimizations)

1. Integrate product phase as optional pre-step in main pipeline
2. User can start with `/01-start-feature` (technical) OR `/product-vision` (business)

**DoD:** Both entry points work seamlessly

---

## VDD Review

> **Sarcasmotron Mode** 🎭

### Challenge 1: "Business metrics are hard to verify"

**Issue:** Unlike code (tests pass/fail), business metrics (ROI, WSJF) are subjective.

**Risk:** LLM hallucinates business justifications that sound plausible but are wrong.

**Mitigation:**
1. WSJF requires explicit scoring (1-10) with rationale
2. Product Reviewer enforces "Show your work" — no scores without explanation
3. User is ALWAYS in the loop for business decisions

**VDD Verdict:** PASS with human oversight mandatory

---

### Challenge 2: "Domain assignment is non-trivial"

**Issue:** Deciding which epic belongs to which domain requires deep understanding.

**Risk:** Incorrect domain → wrong architecture → refactoring hell

**Mitigation:**
1. Domain decomposition skill includes clear rules
2. Dependencies between domains must be explicitly stated
3. Architecture phase validates domain boundaries

**VDD Verdict:** PASS with architecture validation

---

### Challenge 3: "Another layer = more complexity"

**Issue:** Adding product phase increases pipeline length.

**Risk:** More phases = more potential failures = longer feedback loop

**Mitigation:**
1. Product phase is OPTIONAL — technical-only projects skip it
2. Product phase happens ONCE per major initiative, not per task
3. Output is reusable across multiple development cycles

**VDD Verdict:** PASS — complexity justified for enterprise scale

---

### Challenge 4: "Token budget will be exceeded"

**Issue:** New skills + agents = more tokens

**Calculation:**
```
Existing: ~50,000 tokens (standard pipeline)
Product Phase:
  + p01_product_analyst: ~3,000
  + p02_product_reviewer: ~2,000
  + skill-product-analysis: ~1,500
  + skill-backlog-prioritization: ~1,000
  + skill-domain-decomposition: ~1,000
  = ~8,500 tokens additional

Total with Product: ~58,500 tokens
Peak with history: ~75,000-90,000 tokens
```

**VDD Verdict:** MARGINAL — requires O1-O4 optimizations first

---

## Open Questions

### Resolved (by this document)

| Question | Resolution |
|----------|------------|
| "How to handle hallucinations in PO?" | VDD-review mandatory via p02_product_reviewer |
| "Need parallel agents?" | No — artifact-based handoff instead |
| "Separate PM framework?" | No — start as extension, extract if needed |

### Still Open

| Question | Owner | Blocker For |
|----------|-------|-------------|
| "How to persist context between sessions?" | To research | Multi-session pipeline |
| "How to validate business metrics?" | Human oversight | Full automation |
| "IDE support for domain switching?" | IDE vendor | Seamless UX |

---

## Implementation Timeline

```
Week 1: Phase 0
├── Create skill-product-analysis
├── Create skill-backlog-prioritization
├── Create p01_product_analyst
└── Create p02_product_reviewer

Week 2: Phase 1
├── Create product workflows
├── Test workflows in isolation
└── Document usage examples

Week 3: Phase 2
├── Create domain folder structure
├── Update Orchestrator
└── Test multi-domain scenario

Week 4+: Validation
├── Test on real project (Trading Platform example)
├── Measure token usage
├── Iterate based on feedback
```

---

## Changelog

| Date | Author | Change |
|------|--------|--------|
| 2026-01-21 | Adversarial Architect | Initial vision with VDD review |
