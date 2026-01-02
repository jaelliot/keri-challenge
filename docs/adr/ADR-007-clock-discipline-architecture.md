<!-- Copyright (c) Vaidya Solutions -->
<!-- SPDX-License-Identifier: BSD-3-Clause -->

# ADR-007: Clock Discipline Architecture

**Status**: ✅ Accepted (Implemented)  
**Date**: 2026-01-01  
**Deciders**: Architecture Team

---

## Context

### Problem Statement

The KERI protocol relies heavily on event timing and timestamping. Direct usage of system time (`datetime.now()`, `time.sleep()`) causes significant issues:

**1. Flaky Tests**
- Tests using `time.sleep()` are slow and non-deterministic.
- No way to control time progression in tests.

**2. Distributed Systems Issues**
- Clock skew between nodes can cause false positives in expiration checks.
- Lack of tolerance window for timestamp validation.

**3. Non-Deterministic Behavior**
- Retries depend on real-time delays.
- Circuit breakers use wall-clock timestamps.

### Requirements

1. **Testability**: Tests must run instantly without real time delays.
2. **Determinism**: Time-dependent logic must be predictable.
3. **Isolation**: Each test must control its own clock independently.
4. **UTC Everywhere**: All timestamps must be UTC.

---

## Decision

**Implement a clock abstraction layer using `Protocol` and dependency injection.**

### Architecture

**Core Protocol** (`src/keri/core/clock.py`):
```python
from typing import Protocol
from datetime import datetime, timedelta

class Clock(Protocol):
    def now(self) -> datetime: ...
    async def sleep(self, seconds: float) -> None: ...
```

**Two Implementations**:
1. **Real Clock** (`src/keri/core/clock/real.py`) - Production, wraps `datetime.now(timezone.utc)` and `asyncio.sleep()`.
2. **Fake Clock** (`tests/clock/fake.py`) - Testing, manual control.

**Dependency Injection**:
- Clock provided via constructor injection.
- No global clock state.

---

## Rationale

### Why Interface-Based Abstraction?

1. **Testability**: `FakeClock` enables instant, deterministic tests.
2. **Isolation**: Each component gets its own clock instance.
3. **Type Safety**: Python type hints enforce usage.

### Why NOT Global Clock State?

- **Testing Isolation**: Global state causes test interference.
- **Async Safety**: Explicit injection is safer in async contexts.

---

## Consequences

### Positive

✅ **Test Performance**: Test suite runs faster (no real sleeps).
✅ **Deterministic Testing**: Time-dependent logic is predictable.
✅ **Context Awareness**: `asyncio.sleep` respects cancellation.

### Negative

❌ **Boilerplate**: Every component requires clock injection.

---

## Implementation Guidance

1. **Never import `datetime` for current time**.
2. **Never import `time.sleep`**.
3. **Always use `self.clock.now()` and `await self.clock.sleep()`**.
