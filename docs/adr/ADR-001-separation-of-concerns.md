<!-- Copyright (c) Vaidya Solutions -->
<!-- SPDX-License-Identifier: BSD-3-Clause -->
<!--
  docs/adr/ADR-001-separation-of-concerns.md
  @file docs/adr/ADR-001-separation-of-concerns.md
  @description Foundational principle: Separate domain model from execution model
  @update-policy Immutable once accepted - foundational principle
-->

# ADR-001: Separation of Domain Model from Execution Model

**Status**: ✅ Accepted  
**Date**: 2026-01-01  
**Deciders**: Architecture Team  
**Supersedes**: None (foundational principle)  
**Tags**: architecture, foundation, abstraction, principles

---

## Context

Software systems often conflate "what" (domain logic, business rules, contracts) with "how" (runtime implementation, process boundaries, transport mechanisms), leading to tight coupling, testing difficulties, and deployment inflexibility.

The KERI project requires:
- **Deployment flexibility**: Local library (direct mode), Remote Witness (indirect mode), CLI, SaaS.
- **Execution model variety**: In-process (`keripy` calls), Async (`asyncio`), Distributed (TCP/UDP/HTTP).
- **Transport independence**: KERI is transport-agnostic (TCP, UDP, HTTP, CoAP).
- **Storage abstraction**: LMDB (native), InMemory (testing), external SQL (if mandated by integration).

Without clear separation between domain model and execution model, these requirements would create combinatorial complexity and fragile coupling.

---

## Decision

**Core Architectural Principle:**

> **Always separate "what it is" (domain model/interface) from "how it runs" (backend/transport/process boundary) BEFORE implementing any feature.**

### Definitions

- **Domain Model (WHAT)**: Business logic, interfaces, contracts, invariants, API surface
  - Describes what the system does
  - Independent of runtime environment
  - Stable across deployments
  - Examples: `Hab` (Habitat), `Kevery` (Event Verifier), `Signer` interface.

- **Execution Model (HOW)**: Implementation details, runtime choices, process boundaries
  - Describes how the system does it
  - Varies by deployment/environment
  - Swappable without breaking contracts
  - Examples: `aiohttp` transport, `LMDB` backend, `asyncio` loop.

### Application Rules

1. **Define domain model FIRST** - Interfaces, contracts, invariants
2. **Choose execution model SECOND** - In-process, async task, HTTP, etc.
3. **Keep them separated** - Runtime details NEVER leak into domain interfaces
4. **Verify independence** - Can swap execution without changing domain model

### Design Workflow

Before implementing any feature:

```
Step 1: Define WHAT
├─ What does it expose to clients?
├─ What are the guarantees/invariants?
├─ What's the API surface?
└─ Write interface/Protocol (Python)

Step 2: Choose HOW
├─ In-process or subprocess?
├─ Synchronous or async?
├─ Stateless or stateful?
├─ Local or remote?
└─ Select implementation approach

Step 3: Verify Separation
├─ Can I swap implementations?
├─ Are runtime details hidden behind interface?
├─ Would different execution model require interface changes?
└─ If interface changes needed → Bad separation, refactor
```

---

## Examples

### Example 1: KERI Transport Independence

**Domain Model (WHAT):**
```python
# Protocol describes what a messenger DOES
class Messenger(Protocol):
    async def send(self, msg: bytes) -> None: ...
```

**Execution Models (HOW):**
- **Direct**: In-memory function call
- **HTTP**: `aiohttp` POST request
- **TCP**: Raw socket stream

**Separation:**
```python
# Business logic uses Protocol (WHAT)
class KeriAgent:
    def __init__(self, messenger: Messenger):
        self.messenger = messenger

    async def emit_event(self, event: bytes):
        await self.messenger.send(event)

# Execution model selected at startup (HOW)
if config.mode == "http":
    messenger = HttpMessenger(url="...")
elif config.mode == "direct":
    messenger = DirectMessenger(callback=...)
```

### Example 2: Database Abstraction

**Domain Model (WHAT):**
```python
# Interface describes storage contract
class Baser(Protocol):
    def get(self, keys: str) -> bytes | None: ...
    def put(self, keys: str, val: bytes) -> bool: ...
```

**Execution Models (HOW):**
- **LMDB**: Fast, memory-mapped, persistent
- **Memory**: Dict-based, ephemeral, testing

**Separation:**
```python
# Business logic uses interface (WHAT)
def process_event(db: Baser, event: Event):
    if db.get(event.digest):
        return  # Deduplication logic

# Execution model selected at startup (HOW)
def create_app(config: Config):
    if config.testing:
        db = DictBaser()
    else:
        db = LMDBBaser(path="/var/keri/db")
    return KeriApp(db=db)
```

---

## Anti-Patterns (What NOT to Do)

### ❌ Anti-Pattern 1: Execution Model in Interface

**BAD:**
```python
# ❌ Interface leaks HTTP execution model
class Notifier(Protocol):
    async def post_to_webhook(self, url: str, headers: dict) -> Response: ...
```

**Why Bad:**
- Can't implement with TCP or local callback
- Interface describes HOW, not WHAT

**GOOD:**
```python
# ✅ Interface describes domain, execution is implementation detail
class Notifier(Protocol):
    async def notify(self, event: Event) -> None: ...
```

### ❌ Anti-Pattern 2: Domain Model Importing Execution Packages

**BAD:**
```python
# ❌ Domain model imports aiohttp (execution detail)
import aiohttp

@dataclasses.dataclass
class Agent:
    session: aiohttp.ClientSession  # ❌ Leaks HTTP transport
```

**Why Bad:**
- Ties domain model to HTTP transport
- Can't use with other transports
- Can't test without HTTP mocking

**GOOD:**
```python
# ✅ Domain model has no execution dependencies
@dataclasses.dataclass
class Agent:
    transport: Transporter  # Protocol
```

---

## Compliance

### Pre-Implementation Checklist

Before writing ANY feature code:

- [ ] **WHAT defined** - Domain model, interface (`Protocol`), contract written
- [ ] **HOW chosen** - Execution model selected
- [ ] **Separation verified** - Runtime details don't leak into interface
- [ ] **Swappability tested** - Can change HOW without breaking WHAT

### Red Flags (Reject PR if present)

- ❌ Interface method names include "HTTP", "Lambda", "Redis"
- ❌ Domain classes have fields for `aiohttp.ClientSession`, `boto3`, etc.
- ❌ Business logic imports transport/runtime packages

---

## Implementation Guidance

1. **Start with WHAT**
   - Define `Protocol` or `ABC` in Python.
   - Focus on the *intent* (e.g., `store_event`, `send_message`).

2. **Then choose HOW**
   - Implement the protocol using specific libraries (`aiohttp`, `lmdb`).
   - Keep these implementations in separate modules (e.g., `keri.db.lmdb`, `keri.transport.http`).

3. **Verify separation**
   - Ensure domain logic tests can run with simple mocks, without spinning up containers or networks.
