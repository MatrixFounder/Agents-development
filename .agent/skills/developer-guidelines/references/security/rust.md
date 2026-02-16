# Rust Security Quick-Reference

> **Source**: `developer-guidelines/references/security/rust.md`
> **Standard**: RustSec / OWASP

## 1. LLM Anti-Patterns ( DO NOT DO THIS )
- **Unwrap in Prod**: NEVER use `.unwrap()` or `.expect()` in production code. It causes panics (DoS).
    - *Bad*: `let val = Option::None.unwrap();`
    - *Good*: `let val = option.ok_or(Error::Missing)?;`
- **Blind Unsafe**: NEVER write `unsafe` code without a `// SAFETY:` comment explaining why it's sound.
- **Ignoring Results**: NEVER use `let _ = function_returning_result();`. Always handle or propagate errors.
- **Arithmetic Blindness**: NEVER assume integer arithmetic is safe in Release mode (it wraps by default). Use `checked_add` or explicit wrapping types if overflow matters.

## 2. Critical Grep Patterns (Audit These First)
| Pattern | Risk | Check |
| :--- | :--- | :--- |
| `unsafe \{` | Memory Safety | Audit manually. Ensure invariants are upheld. Check `// SAFETY:` comments. |
| `\.unwrap\(\)` | DoS (Panic) | Replace with `?` context-aware error handling. |
| `\.expect\(` | DoS (Panic) | Audit string. Ensure strictly unreachable in prod. |
| `extern "C"` | FFI / Memory | Verify input validation at the boundary. |
| `no_mangle` | FFI / Linking | Verify exposed naming doesn't conflict. |
| `transmute` | Type Confusion | Highly dangerous. Prefer pointer casting or `bytemuck`. |
| `static mut` | Data Race | Deprecated/Dangerous. Use `Atomic` or `Mutex`. |
| `build\.rs` | RCE Risk | Audit build, scripts for malicious code (network/fs access). |
| `unsafe_op_in_unsafe_fn`| Safety Boundary | Ensure this lint is allowed/verified. Unsafe fns should separate unsafe ops. |

## 3. Critical Vulnerabilities & Patterns

### Denial of Service (DoS) via Panic
Rust panics on `unwrap()`, `expect()`, `panic!()`, and `Index Out of Bounds`.
**Secure Pattern**:
```rust
// Vulnerable
fn get_item(idx: usize) -> u8 {
    let arr = [1, 2, 3];
    arr[idx] // Panics if out of bounds
}

// Secure
fn get_item(idx: usize) -> Option<u8> {
    let arr = [1, 2, 3];
    arr.get(idx).copied() // Returns None, no panic
}
```

### Unsafe Code Policy
- **Avoidance**: 99% of code should be Safe Rust.
- **Isolation**: Wrap `unsafe` blocks in safe interfaces.
- **Documentation**: MUST include `/// # Safety` section in doc comments and `// SAFETY:` inside implementation.

### Integer Overflow
By default, Rust **panics** in Debug but **wraps** in Release.
**Mitigation**:
1. Enable `overflow-checks = true` in `Cargo.toml` for Release profile (if perf allows).
2. Use `saturating_add`, `checked_add`, or `wrapping_add` explicitly.

### Supply Chain
- **Cargo Audit**: Run `cargo audit` in CI to check dependencies against RUSTSEC advisory database.
- **Version Pinning**: Commit `Cargo.lock` for binaries.

## 4. Dangerous Crates
- **`unsafe` reliant crates**: Audit dependencies that use excessive `unsafe` (e.g., `actix-web` v1.0 era, though simplified now).
- **Serialization**: `serde` is standard, but beware of `serde_json::from_str` depth limits (recursion DoS).
