# Rust Developer Guidelines

## Core Principles
- **Borrow Checker:** Work *with* the borrow checker, not against it. Avoid `clone()` unless necessary for ownership transfer.
- **Safety:** STRICTLY prefer safe Rust. Use `unsafe` blocks ONLY when absolutely necessary and document WHY.
- **Error Handling:**
  - Use `Result<T, E>` for recoverable errors.
  - **Libraries**: Use `thiserror` for meaningful, structured errors.
  - **Applications**: Use `anyhow` for easy error propagation.
  - Avoid `.unwrap()`. Use `?`, `.expect("context")`, or match.
- **Clippy:** Ensure code passes `cargo clippy --all-targets --all-features -- -D warnings`.
  - Use `#[expect(clippy::lint)]` (Rust 1.81+) instead of `#[allow]` to ensure the lint is actually triggering.

- **Formatting:** Adhere to `cargo fmt`.

## Design Patterns
- **Type State Pattern**: Encode state in the type system to enforce valid transitions at compile time (e.g., `Builder<Ready>`).
- **Newtype Pattern**: Use `struct UserId(u64)` instead of plain `u64` for type safety.

## Testing
- Use `#[test]` for unit tests within the same file (usually in a `tests` module).
- Use `tests/` directory for integration tests.
- **Snapshot Testing**: Consider `insta` for complex output verification.

## Resources
- [Apollo GraphQL Rust Best Practices](https://github.com/apollographql/skills/tree/main/skills/rust-best-practices)
