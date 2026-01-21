# Task 039: Formalize Skill Tiers (O5)

> **Status:** ACTIVE
> **Created:** 2026-01-21
> **Owner:** Orchestrator

## 0. Meta Information
- **Task ID:** 039
- **Slug:** `skill-tiers-formalization`

## 1. Goal
Formalize the "Skill Tiers" mechanism by creating authoritative documentation and enforcing metadata in all `SKILL.md` files. This locks in the gains from Optimization O1 (Lazy Loading).

## 2. Scope
- **Source of Truth:** `Backlog/agentic_development_optimisations.md` (Section O5).
- **New Document:** `System/Docs/SKILL_TIERS.md`.
- **Modifications:** All `SKILL.md` files in `.agent/skills/`.

## 3. Deliverables
1.  [x] `System/Docs/SKILL_TIERS.md` — Authoritative definition of Tiers 0, 1, 2.
2.  [x] Updated `SKILL.md` files with `tier: [0|1|2]` in YAML frontmatter.
    -   [x] Tier 0: `core-principles`, `safe-commands`, `artifact-management`.
    -   [x] Tier 1: Phase-specific skills (mapped in docs).
    -   [x] Tier 2: All others (default).
3.  [x] Verification Report (via Walkthrough).

## 4. Implementation Plan
1.  **Documentation:** Create `System/Docs/SKILL_TIERS.md` based on Backlog table.
2.  **Updates:** Iterate through all skills:
    -   Read header.
    -   Inject `tier: X` property.
    -   Save.
3.  **Verification:**
    -   Grep for `tier:` to ensure coverage.
    -   Verify Tier 0 specifically.
