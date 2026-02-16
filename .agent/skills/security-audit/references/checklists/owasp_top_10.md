# OWASP Top 10:2025 Checklist

> **Source:** Based on OWASP 2025 Draft & Backlog Analysis.

## A01: Broken Access Control
- [ ] **Enforcement:** Is access denied by default?
- [ ] **IDOR:** Can User A access User B's resources by changing an ID?
- [ ] **SSRF:** Are external resource fetches validated against an allow-list? (Merged into A01 in 2025).
- [ ] **CORS:** Is it too permissive (`*`)?

## A02: Cryptographic Failures
- [ ] **Transmission:** Is TLS 1.3 enforced?
- [ ] **Storage:** Are passwords hashed (Argon2id/bcrypt)?
- [ ] **Secrets:** Are keys hardcoded? (Use `run_audit.py` to check).
- [ ] **Randomness:** Is `Math.random()` used for crypto? (Use `crypto.getRandomValues`).

## A03: Software and Data Integrity Failures (Supply Chain) 🆕
- [ ] **Dependencies:** Is `npm audit` / `cargo audit` clean?
- [ ] **Lockfiles:** Are `package-lock.json` / `Cargo.lock` present and committed?
- [ ] **CI/CD:** Is the build pipeline secured against tampering?
- [ ] **Verification:** Are signatures verified for external artifacts?
- [ ] **Updates:** Is there an unsigned update mechanism?
- [ ] **Deserialization:** Is user data deserialized unsafely?

## A04: Insecure Design
- [ ] **Threat Modeling:** Was a threat model created for this feature?
- [ ] **Rate Limiting:** Is it implemented to prevent abuse?
- [ ] **Logic:** Are business flows protected against manipulation (e.g., buying negative quantity)?

## A05: Security Misconfiguration
- [ ] **Hardening:** Are unused features/ports disabled?
- [ ] **Error Messages:** Do stack traces leak to users? (Disable `DEBUG` mode).
- [ ] **Headers:** Are security headers (`CSP`, `HSTS`, `X-Frame-Options`) configured?

## A06: Vulnerable and Outdated Components
- [ ] **Scanning:** Is automated SCA (Software Composition Analysis) running?
- [ ] **End-of-Life:** Are we using EOL OS or libraries?

## A07: Identification and Authentication Failures
- [ ] **MFA:** Is Multi-Factor Authentication available/enforced?
- [ ] **Sessions:** Do sessions expire absolute and idle?
- [ ] **Brute Force:** Is there lockout/delay logic?

## A08: Identification and Authentication Failures
> Items from original A08 (Integrity) merged into A03 above.

*(Section reserved for future use if OWASP 2025 final introduces a new A08)*

## A09: Security Logging and Monitoring Failures
- [ ] **Audit Trail:** Are login, access, and failure events logged?
- [ ] **Protection:** Are logs protected from tampering?
- [ ] **Alerting:** Do critical failures trigger real-time alerts?

## A10: Exceptional Conditions 🆕
- [ ] **SSRF:** Do we allow users to specify domains/IPs? Is the server isolated from internal metadata services (AWS IMDS)?
- [ ] **Fail Safe:** Does the system fail closed (deny access) on error?
- [ ] **Race Conditions:** Are check-then-act patterns atomic?
- [ ] **Resource Exhaustion:** Can a user trigger OOM or CPU spikes?
