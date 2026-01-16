---
description: Ensure documentation is synchronized between languages.
---

# Localization Synchronization Rule

## Core Principle
The **English** version of documentation (`README.md`, `CHANGELOG.md`, `docs/*.md`) is the **Primary Source of Truth**. The **Russian** version (`README.ru.md`, localized docs) must effectively mirror the English version to ensure all users have access to the same information.

## Rules

1.  **README Sync**:
    -   IF you modify `README.md` (e.g., adding a new section, link, or instruction),
    -   THEN you MUST immediately update `README.ru.md` with the translated equivalent.

2.  **CHANGELOG Sync**:
    -   Release notes must be provided in both English and Russian sections of `CHANGELOG.md`.

3.  **Critical Artifacts**:
    -   If a new critical documentation file is created (e.g., `docs/ORCHESTRATOR.md`), consider if a translation is needed or if `README.ru.md` should link to it with a note.

## Enforcement
-   Agents (Orchestrator, Developer) updating documentation must check for `*.ru.md` counterparts.
