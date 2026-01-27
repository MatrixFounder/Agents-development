---
name: brainstorming
description: Use ONLY when the user EXPLICITLY asks for brainstorming ideas, research, or concept exploration (e.g. via /brainstorm command). NEVER works on code implementation.
tier: 2
version: 2.0
---

# Brainstorming & Concept Refinement

> [!IMPORTANT]
> **TRIGGER WARNING**: This skill is for **PRE-PLANNING** only.
> - **DO NOT USE** if the user asks you to "implement", "fix", or "write code".
> - **DO NOT USE** as part of the standard Analysis meant for `implementation_plan.md`.
> - **USE ONLY** when the user says: "Brainstorm ideas", "Research X", "What do you think about...", or uses `/brainstorm`.

## 1. Red Flags (Anti-hallucination)
**STOP and READ THIS if you are thinking:**
- "I'll just write some code to test this idea" -> **STOP**. You are in Brainstorm mode. **NO CODING**.
- "I'll update the implementation plan" -> **WRONG**. Write to `docs/YYYYMMDD-brainstorming-<topic>.md`.
- "The user wants a spec" -> **WRONG**. Hand off to `requirements-analysis` for formal specs.

## 2. The Process

### Phase 1: Context & Discovery
1.  **Read Context**: Check `SEARCH` or `REFERENCES` provided by the user.
2.  **Ask Clarifications**:
    *   Batch your questions. Do not be chatty.
    *   Ask about: Constraints, Goals, User Persona.

### Phase 2: Idea Generation
1.  **Diverge**: Propose 2-3 distinct approaches (e.g., "Low Code" vs "Custom Build", "Sql" vs "NoSql").
2.  **Trade-offs**: For each approach, list Pros/Cons.
3.  **YAGNI Audit**: Explicitly list features you recommend **cutting** to keep it simple.

### Phase 3: Artifact Generation
1.  **Create Artifact**:
    *   Filename format: `docs/YYYYMMDD-brainstorming-<topic>.md` (e.g. `20240127-brainstorming-login.md`).
    *   Structure:
        *   **Problem Statement**
        *   **Proposed Approaches** (Table)
        *   **Recommended Solution**
        *   **Next Steps** (Link to /iterative-design)

## 3. Best Practices

| DO THIS | DO NOT DO THIS |
| :--- | :--- |
| **Batch Questions**: "Here are 3 questions to clarify scope..." | **One-by-one**: "Question 1... [wait] ... Question 2..." |
| **Output Markdown**: Save specific artifact file. | **Chat Only**: dumping text in chat without saving. |
| **Strategy First**: Focus on "Why" and "What". | **Implementation First**: Focusing on "How" (code details). |

## 4. Examples

### Trigger
**User**: "Help me figure out how to add auth to this app."
**Agent**: (Activates `brainstorming`) "Sure. Let's explore options. Do you need OAuth or Email/Pass?..."

### Artifact Output
```markdown
# Brainstorming: Auth System
## Approaches
| Method | Pros | Cons |
|--------|------|------|
| Auth0  | Fast | Cost |
| Custom | Free | Security Risk |
```