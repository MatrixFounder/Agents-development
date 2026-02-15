# Usage Example: Adversarial Critique

## Input

The Builder submits a user authentication function:

```python
def login(username, password):
    user = db.get_user(username)
    if user and user.password == password:
        return create_session(user)
    return None
```

## Adversarial Critique (using `assets/template_critique.md`)

### 1. Executive Summary
- **Verdict**: FAIL
- **Confidence**: High
- **Summary**: Critical security flaws in authentication logic. Plaintext password comparison, no rate limiting, timing attack vulnerability.

### 2. Risk Analysis

| Severity | Category | Issue | Impact | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **HIGH** | Security | Plaintext password comparison | Credential theft if DB is compromised | Use bcrypt/argon2 hash comparison |
| **HIGH** | Security | No rate limiting | Brute-force attacks | Add exponential backoff after N failures |
| **MED** | Security | Timing attack on `==` | Password length leak | Use `hmac.compare_digest()` |
| **MED** | Logic | `None` return hides failure reason | No distinction between "user not found" and "wrong password" | Return typed error codes |
| **LOW** | Resilience | No DB error handling | Unhandled exception if DB is down | Wrap in try/except with graceful degradation |

### 3. Hallucination Check
- [x] **Files**: No external files cited.
- [x] **Line Numbers**: Code reviewed matches submitted snippet.
