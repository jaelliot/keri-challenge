---
applyTo: "**/*.py,**/*.ipynb,pyproject.toml"
# Universal Python packaging, style standards, and naming conventions
---
## Use when
- Managing project dependencies and configuration
- Setting up new Python modules or files
- Configuring linters and formatters
- Naming variables, functions, classes, and modules
- Implementing core business logic, error handling, and observability

## Do

### Naming & Style
- **Naming**:
    - Use `snake_case` for modules, functions, and variables.
    - Use `PascalCase` for classes.
    - Use `UPPER_SNAKE_CASE` for constants.
    - **Domain Specifics**:
        - Prefer `keri` specific terms: `hab` (Habitat), `kel` (Key Event Log), `aid` (Autonomic ID), `evt` (Event).
        - Use `helping`, `keeping`, `doing`, `asking` for functional module roles (as seen in `keripy`).
    - Suffix classes with pattern roles: `Manager`, `Service`, `Error`.
    - Prefix error classes with domain name (e.g., `KeriValidationError`).
    - Use verbs for function names (e.g., `process_event`).
- **Typing (Strict)**:
    - Employ Python type hints for all function signatures, variable declarations, and class attributes.
    - Utilize MyPy in strict mode (`strict = true`) as the primary static type checker.
    - Aim to eliminate all type errors reported by MyPy; generated code **must** pass without errors.
    - Use specific types (e.g., `list[str]` instead of `list`, `dict[str, int]` instead of `dict`).
    - Use `typing.Any` sparingly and **only** with explicit inline justification.
- **Formatting**:
    - Enforce consistent formatting via configured tools (`ruff` or `black`).
    - **File Header**: Include a single-line comment at the very top of every file indicating its path relative to the project root (e.g., `# src/keri/app/keeping.py`).

### Configuration & Environment
- **Use `pydantic-settings` exclusively**: Load configuration via dependency injection.
    ```python
    class Settings(BaseSettings):
        log_level: str = "INFO"
    ```
- **Use `pyproject.toml` exclusively** for dependency management and tool configuration (PEP 517/518/621).
- Specify the exact Python version: `requires-python = '==3.14.2'`.

### Observability & Logging
- **Inject Logger via DI**: Use structured logging (`structlog` or `loguru`) injected into components.
    ```python
    def __init__(self, logger: structlog.BoundLogger):
        self.logger = logger
    ```
- **Redaction**: Ensure sensitive data (keys, tokens) is redacted before logging.

### Error Handling
- **Use Structured Exceptions**: Define custom exception hierarchies inheriting from a base `KeriError`.
- **Wrap Errors**: Catch low-level exceptions and raise domain-specific errors with context.
    ```python
    except FileNotFoundError as e:
        raise KeriIOError(f"Failed to load KEL: {path}") from e
    ```

### Resource Management
    - Use context managers (`with` statement) for managing resources (files, network connections, locks) to ensure automatic cleanup.
    - Explicitly close resources in a `finally` block if context managers are not available.

### Crypto & Encoding
    - Use CESR-native encoding where possible.
    - Treat all cryptographic primitives as `bytes` or CESR-encoded strings (Base64 URL-safe), not raw strings.

### Resilience & Transport
- **Resilience**: Use `tenacity` for all retries and circuit breakers.
- **HTTP Isolation**: Keep HTTP imports (`aiohttp`, `requests`) inside `src/transport` or `src/api`. Domain logic MUST be transport-agnostic.
- **Exception for Challenge**: Falcon resource classes can be implemented directly in the application module. `aiohttp` is likely not needed if using Falcon's `TestClient`.

## Don't

- **Configuration Anti-Patterns**:
    - ❌ **Direct `os.getenv()` calls**: Do not access environment variables directly in business logic.
    - ❌ Use `setup.py` or `requirements.txt` for primary dependency or configuration.
- **Logging Anti-Patterns**:
    - ❌ **Use `print()`**: Use structured loggers only.
    - ❌ **Create local loggers**: Don't instantiate loggers inside methods; inject them.
- **Error Handling Anti-Patterns**:
    - ❌ **Raise generic exceptions**: Avoid `raise Exception("fail")` or `raise ValueError` without context.
    - ❌ **Fail Open**: If a security check fails, STOP. Do not proceed with partial data.
- **Typing Anti-Patterns**:
    - Use `typing.Any` or overly broad types (e.g., `dict`) without justification.
    - Suppress type errors (e.g., `# type: ignore`) without a compelling, documented reason.
    - Treat type hints as optional or an afterthought.
- **Naming Anti-Patterns**:
    - Use generic or technical names (e.g., `data`, `utils`) without domain context.
    - Use single-letter variable names outside short loops.
- **Architecture Anti-Patterns**:
    - ❌ **HTTP in Business Logic**: Do not import `aiohttp` or `requests` in `src/keri/core`.
    - ❌ **Manual Retries**: Do not write `while` loops for retries; use `tenacity`.

## Notes / Examples

- **Build System**: Use `setuptools` with `build-backend = "setuptools.build_meta"` or `hatchling`.
- **Structure Example**:
  ```toml
  [project]
  name = "keri-core"
  requires-python = "==3.12.10"
  dependencies = ["pysodium>=0.7.17", "blake3>=0.3.3"]

  [tool.mypy]
  strict = true
  python_version = "3.12"
  ```
- **Error Hierarchy Example**:
  ```python
  class KeriError(Exception):
      """Base error for KERI operations."""
  
  class ValidationError(KeriError):
      """Validation failed."""
  ```