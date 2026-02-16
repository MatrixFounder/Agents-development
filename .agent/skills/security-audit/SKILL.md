---
name: security-audit
description: Use when performing security vulnerability assessment (OWASP, secrets, dependencies) or when "thinking like a hacker" to find exploits.
tier: 2
version: 2.1
---

# Security Audit

## 1. Red Flags (Anti-Rationalization)
**STOP and READ THIS if you are thinking:**
- "I'll skip the script because I just checked the code manually" -> **WRONG**. Humans miss regex patterns. **EXECUTE** the script.
- "This is an internal tool, so AuthZ doesn't matter" -> **WRONG**. Zero Trust applies everywhere.
- "Dependencies are probably fine" -> **WRONG**. Supply chain attacks are the #1 vector in 2025.
- "I don't have time for a full audit" -> **WRONG**. Breach cleanup takes 100x longer.

## 2. Automated Detection
**EXECUTE** the unified audit script to detect vulnerabilities:
```bash
python3 .agent/skills/security-audit/scripts/run_audit.py [project_path] [--scan-type all|deps|secrets|patterns|config|external]
```
- **Analysis**: Review the output. If tools fail or report Critical/High issues, they are **BLOCKERS**.
- **Scope**: The script checks Secrets (OWASP A02), Dependencies (A06), Code Patterns / Injection (A03), and Config / Misconfiguration (A05).
- **External Tools**: It also auto-runs `slither`, `bandit`, `npm audit`, or `cargo audit` if project types are detected.
- **Self-Exclusion**: The scanner skips its own source files to prevent false positives.

## 3. "Think Like a Hacker" (Adversarial Review)

**Refuse to merge/approve until you have manually verified the code against the relevant checklist.**

### 🛡️ Smart Contracts (Solidity)
**MANDATORY:** Read `references/checklists/solidity_security.md`.
**Top 3 Checks:**
1. **Reentrancy**: Are checks-effects-interactions followed? `nonReentrant` used?
2. **Access Control**: Who owns the contract? `onlyOwner` checks?
3. **Price Manipulation**: Are spot prices used? (Use Oracles).
4. **Fuzzing**: See `references/checklists/fuzzing_invariants.md`.

### 🦀 Smart Contracts (Solana/Rust)
**MANDATORY:** Read `references/checklists/solana_security.md`.
**Top 3 Checks:**
1. **Account Validation**: Are ALL accounts checked for ownership and signer status?
2. **PDA bumps**: Are bumps strictly validated?
3. **Arithmetic**: Is `overflow_checks` on?

### 🌐 Web/API (OWASP Top 10:2025)
**MANDATORY:** Read `references/checklists/owasp_top_10.md`.
**Top 3 Checks:**
1. **Broken Access Control (A01)**: Can user A access user B's data? (IDOR).
2. **Supply Chain (A03)**: Are lock files committed? Are deps pinned?
3. **Exceptional Conditions (A10)**: Does it fail secure?

## 4. Attack Surface Mapping
Before declaring "Secure", map the surface:
1. **Entry Points**: APIs, forms, file uploads, webhooks.
2. **Data Flows**: Where does user input go? (Logs? DB? Shell?).
3. **Assets**: Secrets, PII, Money.

## 5. Reporting
- **Critical**: Immediate Blocker (RCE, Auth Bypass, Secrets). **Fix immediately**.
- **High**: Must fix before release (XSS, CSRF, Dep Vulns).
- **Medium**: Document in Backlog (Missing headers, best practices).

## 6. Rationalization Table

| Agent Excuse | Reality / Counter-Argument |
| :--- | :--- |
| "The script reported [OK], so it's clean" | Check `skipped_files` count. Silent skips = false negatives. |
| "This is a test/dev environment" | Attackers pivot from dev to prod. Zero Trust applies everywhere. |
| "Dependencies are only dev dependencies" | `devDependencies` run during build. Supply chain attacks don't discriminate. |
| "The flag is a false positive" | Verify manually. Never dismiss without proof. |
| "I'll fix it later" | Later = Never. Critical/High = Blocker NOW. |
