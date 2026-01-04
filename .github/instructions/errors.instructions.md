---
applyTo: "**/*.py"
# Standards for error handling, exception hierarchy, and logging in KERI
---
## Use when
- Implementing logging in `keripy` or core libraries.
- Defining custom exception classes for KERI protocols (Validation, Crypto, State).
- Handling exceptions in asynchronous coroutines (`hio`, `asyncio`).
- Debugging distributed event logs.

## Do
- **Logging**:
    - Use **Loguru** exclusively; avoid `print()` or built-in `logging`.
    - Contextualize logs with **AIDs** (identifiers) and **SAIDs** (digests) to trace events across the distributed system.
    - Use `logger.trace` for low-level byte/stream parsing events.
    - Use `logger.exception` to capture stack traces for unexpected crashes.
- **Exception Hierarchy**:
    - Define a base `KeriError` (often in `keri.kering`).
    - Subclass for specific domains:
        - `ValidationError`: Malformed CESR, invalid signatures, schema violations.
        - `LikelyDuplicitousError`: Detected duplicity (forked KEL).
        - `MissingSignatureError`: Threshold not met.
        - `StateError`: Operation invalid for current key state.
- **Design**:
    - **Fail Fast**: Raise `ValidationError` immediately upon detecting invalid CESR streams to prevent cache poisoning.
    - **Crash-Only Software**: In the event of unrecoverable state corruption (e.g., KEL inconsistency on disk), prefer crashing/restarting over continuing in an undefined state.
    - **Exception for Challenge**: Error responses **do not** need to be signed with a signature header. Return standard HTTP error codes (400, 401, 404) with clear JSON bodies, but skip the signature overhead for errors.

## Don't
- **No Silent Failures**: Never suppress cryptographic verification errors.
- **No `print()`**: Use `logger.debug()` or `logger.info()` instead.
- **No Generic Exceptions**: Avoid raising bare `Exception` or `ValueError` for protocol logic; use specific KERI exceptions.
- **Sensitive Data**: **NEVER** log private keys or seeds. Be careful when logging raw event streams to not leak sensitive payload data if it exists.

## Notes / Examples

### Contextual Logging with AIDs
```python
from keri import help
logger = help.ogler.getLogger()

def process_event(event, aid):
    with logger.contextualize(aid=aid, said=event.said):
        logger.info("Processing rotation event")
        try:
            verify_signature(event)
        except ValidationError:
            logger.warning("Signature verification failed")
            raise
```

### Exception Hierarchy Pattern
```python
class KeriError(Exception):
    """Base class for all KERI exceptions"""

class ValidationError(KeriError):
    """Event validation failed (signature, structure)"""

class DuplicityError(ValidationError):
    """Duplicity detected in KEL"""
```