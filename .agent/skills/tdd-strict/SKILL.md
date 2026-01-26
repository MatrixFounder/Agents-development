---
name: tdd-strict
description: "Use when high-assurance reliability is required (Bug fixes, Critical Features, Quality Hardening)."
tier: 3
version: 1.0
---
# Strict TDD Protocol (High Assurance)

This skill enforces a rigorous, evidence-based TDD cycle designed to eliminate "lucky passes" and "code hallucinations". It is stricter than the standard `tdd-stub-first`.

> [!IMPORTANT]
> **ACTIVATION:** This skill replaces the standard TDD cycle. When active, you MUST follow the **Strict Cycle** below.

## 1. The Strict Cycle (Red-Red-Green-Refactor)

You must strictly follow this 4-step loop for EVERY test case.

### Step 1: Write Test + `EXPECTED_FAIL_REASON`
Write the test case (or stub) and explicitly comment what exact error it *should* raise.
*   **Why**: Prove that you know *why* it fails.
*   *Example*:
    ```python
    # EXPECTED_FAIL_REASON: AssertionError: Expected 200 OK, got 404 because endpoint is not registered.
    def test_create_user(client):
        resp = client.post("/users", json={"name": "Alice"})
        assert resp.status_code == 200
    ```

### Step 2: Verify Fail (The "Red" Check)
Run the test. It **MUST FAIL**.
1.  **Check**: Does the actual error match `EXPECTED_FAIL_REASON`?
2.  **Pass (on Fail)**: If it fails as expected -> Proceed.
3.  **Fail (on Logic)**: If it crashes with `SyntaxError` or `ImportError` -> Fix the test, do not touch code.
4.  **Fail (on Pass)**: If the test passes immediately -> **STOP**. You have a Logic Leak or a bad test. Delete code and investigate.

### Step 3: Minimal Code Implementation (The "Minimalism Law")
Implement **ONLY** the code required to make the test pass.
*   **Prohibited**: "While I'm here, I'll add the update method too."
*   **Prohibited**: Adding generic exception handlers `try: ... except: pass` just to silence errors.
*   **Prohibited**: Speculative architecture not required by the test.

> [!CRITICAL]
> **Dead Code Rule**: If you write a line of code, ask: "If I delete this line, will the current test fail?" If the answer is No, DELETE IT.

### Step 4: Verify Pass + `EXPLAIN_PASS_REASON`
Run the test. It MUST PASS.
1.  **Log**: Explicitly state why it passed now.
    *   *Example*: "PASS: Validated that registration logic now writes to DB returning 200."
2.  **Refactor**: Now (and only now) you may clean up the code.

## 2. Red Flags (Stop Conditions)

*   🚩 **Lucky Pass**: You wrote a test and it passed immediately. **STOP**. Investigate why your test is ineffective.
*   🚩 **Speculation**: You are writing code for a "future requirement" not covered by the current failing test. **STOP**. Delete it.
*   🚩 **Silent Failures**: You saw a failure, didn't check the reason, and started coding. **STOP**. Verify the reason first.

## 3. Usage Context

*   **When to use**:
    *   Implementing Critical Core Features.
    *   Fixing Bugs (Regression prevention).
    *   When explicitly instructed to use "Strict Mode".
*   **When NOT to use**:
    *   Exploratory Prototyping (Spikes).
    *   Initial Project Bootstrapping (creating large empty class structures).
