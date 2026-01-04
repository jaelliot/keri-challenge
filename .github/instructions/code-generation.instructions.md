---
applyTo: "**/*.py"
# KERI-compliant Python code generation, strict typing, and documentation standards
---
## Use when
- Generating new Python code for the KERI project.
- Refactoring existing code to match KERI/ToIP standards.
- Implementing KERI specifications (KEL, CESR, ACDC).

## Do
- **File Management**:
  - **Check Existence**: Verify if a target module exists before creating a new one.
  - **Domain Structure**: Place functionality in `keri` domain modules (e.g., `keri/core` for primitives, `keri/app` for logic, `keri/db` for storage).
  - **Exception for Challenge**: For this single-purpose challenge, a simplified structure (e.g., `src/app.py` and `tests/test_app.py`) is permitted.
  - **Path Comments**: Include a single-line comment at the top of every file indicating its path (e.g., `# src/keri/core/eventing.py`).
- **Patterns**:
  - **Immutability**: Use `dataclasses.dataclass(frozen=True)` or `typing.NamedTuple` for data transfer objects (events, messages).
  - **AsyncIO**: Implement I/O-bound operations as `async` functions/methods. Use `asyncio` context managers for resources.
  - **Generators**: Use generators for processing streams of events (CESR streams) to handle backpressure and memory efficiency.
  - **Context Managers**: Use `with` statements for resource management (DB handles, file I/O, locks).
- **Typing (Strict)**:
  - **Explicit Types**: Use `bytes` for raw crypto material and `str` for CESR-encoded (Base64) text. Never mix them.
  - **Type Hints**: Fully type hint all functions (`def func(a: int) -> str:`).
  - **No Any**: Avoid `typing.Any` unless interacting with untyped 3rd-party libraries (and document why).
- **Serialization**:
  - **Canonical JSON**: When using JSON, ensure no whitespace and sorted keys (required for KERI hashing).
  - **CESR**: Prefer CESR encoding for internal representation of crypto primitives.

## Don't
- **Anti-Patterns**:
  - **Mutable Defaults**: Never use mutable default arguments (e.g., `def foo(l=[])`).
  - **Implicit Casting**: Don't rely on implicit `str` to `bytes` conversion.
  - **Global State**: Avoid global mutable state. Use dependency injection or context objects (`Context`).
  - **Generic Utils**: Don't create `utils.py`. Put the function where it belongs (e.g., `hashing.py`, `encoding.py`).
- **Dependencies**:
  - Don't introduce heavy external dependencies (e.g., Redis, Kafka) when internal KERI mechanisms (witnesses, direct mode) suffice.
  - Don't use `float` for precise calculations; use `decimal.Decimal` or integer math.

## Notes / Examples
- **File Path Comment**:
  ```python
  # src/keri/core/coring.py
  import dataclasses
  ...
  ```
- **Immutable Event Class**:
  ```python
  @dataclasses.dataclass(frozen=True)
  class InceptionEvent:
      v: str  # Version string
      t: str  # Type (icp)
      d: str  # Digest
      ...
  ```
- **Canonical JSON Serialization**:
  ```python
  import json
  # Ensure strict ordering and no whitespace for stable hashing
  raw = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
  ```
- **Rationale**: "Used `frozen=True` for `RotationEvent` to ensure the event content cannot be modified after signing, preserving hash integrity."