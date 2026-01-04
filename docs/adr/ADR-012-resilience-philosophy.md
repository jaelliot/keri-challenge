<!-- Copyright (c) Vaidya Solutions -->
<!-- SPDX-License-Identifier: BSD-3-Clause -->
<!-- -->
<!-- docs/adr/ADR-012-resilience-philosophy.md -->
<!-- @file docs/adr/ADR-012-resilience-philosophy.md -->
<!-- @description Resilience Over Everything - Core Architectural Philosophy -->
<!-- @update-policy Immutable once accepted -->

# ADR-012: Resilience Over Everything - Core Architectural Philosophy

**Status:** ✅ Accepted  
**Date:** 2026-01-01  
**Deciders:** Architecture Team  
**Tags:** architecture, resilience, philosophy, operations

---

## Context

The KERI protocol and its implementations are designed to be the "Trust Spanning Layer" of the internet. This layer must be more resilient than the applications built on top of it. In distributed identity and verifiable data systems, downtime or data inconsistency can lead to permanent loss of control authority (key compromise) or inability to verify critical transactions.

### Problem Statement

How should we prioritize architectural decisions when trade-offs arise between:
- Development velocity vs. operational resilience?
- Feature richness vs. failure isolation?
- Complexity vs. self-healing capabilities?
- Online-only vs. offline capability?

### Driving Forces

1. **End-Verifiability**: The core KERI value. Verification must work even if the original issuer is offline (via Witnesses/Watchers).
2. **High-Stakes Consequences**: Failures in key management or event logging can result in **loss of identity control**.
3. **Unpredictable Infrastructure**: Network connectivity, DNS, and cloud services cannot be assumed to be reliable or trustworthy ("Zero Trust in Infrastructure").
4. **Solo Developer Operations**: The system architect is often the sole technical resource.

## Decision

**We adopt "Resilience Over Everything" as our core architectural philosophy.**

All architectural decisions prioritize:

1. **Autonomous Recovery**: System must survive and recover without human intervention.
2. **Graceful Degradation**: Offline operation is a first-class mode.
3. **Deterministic Behavior**: Failures and time-sensitive operations must be predictable.
4. **Context Adaptability**: Adapt to transport/storage availability (direct vs indirect mode).

### Concrete Implications

#### ✅ Prioritize
- **Tenacity**: Retries, circuit breakers, and timeouts on every external integration.
- **AsyncIO Resilience**: Handling long-lived streams (TCP/HTTP) with automatic reconnection.
- **Fallback Behaviors**: Caching KELs locally; using multiple Witnesses.
- **Audit Trails**: Every event logged with tamper-evident signatures (KEL).
- **Deterministic Time**: `clock.Clock` abstraction for testable time-sensitive behavior.
- **Zero-Dependency Core**: Logic works without external databases or networks.

#### ❌ Deprioritize
- "Move fast and break things" velocity.
- Reliance on single external services without fallbacks.
- Assuming infrastructure reliability.
- Silent failures.

## Consequences

### Benefits

- **Operational Independence**: Identity control persists even if parts of the network fail.
- **Diagnostic Completeness**: KELs provide a cryptographic audit trail of all state changes.
- **Solo Developer Sustainability**: Self-healing reduces operational burden.

### Costs

- **Development Complexity**: Every integration requires fallback paths and timeout configuration.
- **Testing Burden**: Must test failure modes (network partitions, witness unavailability).
- **Performance Overhead**: Signature verification and event logging add latency.

## Implementation Strategy

### Phase 1: Current
- ✅ Operation-level resilience: Retries/Circuit Breakers via `tenacity`.
- ✅ Deterministic time: `Clock` protocol.
- ✅ Transport independence: `aiohttp`/`tcp` separation.

### Phase 2: Planned
- Enhanced chaos testing (simulating witness failures).
- Automated Witness rotation on failure.

## Example: Resilience in Action

**Without "Resilience Over Everything":**
```python
async def post_event(url, event):
    async with aiohttp.ClientSession() as session:
        await session.post(url, data=event)  # Hope it works!
```

**With "Resilience Over Everything":**
```python
@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(),
    retry=tenacity.retry_if_exception_type(aiohttp.ClientError)
)
async def post_event_resilient(clock: Clock, url: str, event: bytes):
    # 1. Timeout ensures bounded latency
    # 2. Retries handle transient network issues
    # 3. Structured logging provides diagnostic context
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=event, timeout=30) as resp:
                resp.raise_for_status()
                return await resp.read()
    except Exception as e:
        logger.warning(f"Event posting failed: {e}")
        # Fallback logic here if needed
        raise
```

## Validation Criteria

1. **Autonomy**: System runs without manual intervention despite network flakes.
2. **Observability**: Post-incident analysis has complete context.
3. **Offline Capability**: Core logic works without internet.

## References

- [Project Charter Instructions](../../.github/instructions/project-charter.instructions.md)
- [Resilience Instructions](../../.github/instructions/resilience.instructions.md)
- [Clock Architecture ADR](ADR-007-clock-discipline-architecture.md)
- [Separation of Concerns ADR](ADR-001-separation-of-concerns.md)
