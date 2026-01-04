---
applyTo: "src/**/*.py"
# Persistence layer standards for KERI Key Event Logs (KELs) and key state
---
## Use when
- Implementing storage for Key Event Logs (KELs), Key Event Receipt Logs (KERLs), or Key State.
- Managing database interfaces for LMDB (Lightning Memory-Mapped Database).
- Handling append-only log structures and immutable event storage.

## Do
- **Database Choice**: Use **LMDB** as the primary storage engine for production.
  - **Exception for Challenge**: For test fixtures and this specific challenge, **in-memory storage** (module-level dicts) is explicitly permitted and encouraged for simplicity.
- **Data Structure**:
  - Treat the **KEL (Key Event Log)** as the source of truth. It is an append-only, ordered log of cryptographically signed events.
  - Store events in their raw **CESR** serialized format to ensure signature verification remains valid (byte-for-byte fidelity).
  - Use `fn` (First-Seen Number) to strictly order event acceptance time, separate from `sn` (Sequence Number).
- **Pattern**:
  - Implement a **Database Abstraction Layer** (e.g., `hio` base classes or similar) to decouple the LMDB specific logic from the business logic.
  - Use **iterators** for traversing KELs to handle potentially large event logs efficiently.
- **Integrity**:
  - **Duplicity Detection**: The persistence layer must support checking for conflicting events at the same sequence number (`sn`) for the same AID.
  - **Immutability**: Once an event is "First-Seen" and accepted, it must never be mutated. Superseding events (recovery) fork the log but do not delete the old event.
- **Key State**:
  - Derive current key state by replaying the KEL. Caching the current state is permitted for performance but must always be reconcilable with the log.

## Don't
- **Relational Models**: Don't try to force KERI events into a normalized relational schema (SQL). KERI is inherently log-based.
- **Mutation**: Never update an existing event record. KERI is append-only. Updates are new events.
- **Cloud Databases**: Avoid heavy dependencies on cloud-native DBs (DynamoDB, Firestore) for the core library. The core must run on the edge (Wallets/Witnesses).
- **Serialization Mutation**: Don't decode to JSON and re-encode to store. Store the exact bytes received to preserve signatures.

## Notes / Examples
- **LMDB Usage**:
  - Use lexicographical key ordering for efficient range scans of sequence numbers.
  - Key design: `{AID}.{SN}.{Digest}` enables quick lookup of specific events.
- **Directory Structure**:
  - `data/db/`: Default location for LMDB files.
  - `keystore/`: Secure storage for private keys (separate from the public KEL).
- **First-Seen Policy**:
  - The persistence layer is the enforcer of "First-Seen". If an event arrives that conflicts with an existing First-Seen event, it is either dropped or marked as duplicity evidence (depending on the mode).