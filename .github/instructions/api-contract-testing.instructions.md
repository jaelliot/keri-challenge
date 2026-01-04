---
applyTo: "tests/**/*.py,tests/integration/**/*.py"
# API Contract Verification and Testing Standards for KERI
---
## Use when
- Verifying communication between KERI components (e.g., Wallet ↔ Witness, Watcher ↔ Witness).
- Validating CESR stream parsing and serialization contracts.
- Testing OOBI (Out-Of-Band Introduction) resolution and discovery.
- Ensuring compliance with KERI, ACDC, and CESR specifications.

## Do
- **Protocol Adherence**:
    - Verify strict adherence to **CESR** encoding rules (text/binary domains, pre-padding).
    - Validate KERI event message structures (`icp`, `rot`, `ixn`, `rpy`) against the spec.
- **Tools**:
    - Use `pytest` for all integration and contract tests.
    - Leverage `keripy` core libraries for generating valid/invalid test vectors.
- **End-Verifiability**:
    - Test that all messages are cryptographically verifiable (signatures match keys).
    - Verify that KELs (Key Event Logs) maintain strict ordering and hash-linking.
- **Scenarios**:
    - **Happy Path**: Successful OOBI resolution, valid event witnessing, correct KEL appending.
    - **Duplicity**: Simulate duplicity scenarios (two events, same SN) and verify "First-Seen" rejection.
    - **Serialization**: Test round-trip serialization (CESR → Object → CESR) for lossless fidelity.
- **Mocking**:
    - Use `hio` (Hierarchical I/O) or `asyncio` mocks to simulate network transport, ensuring tests focus on protocol logic, not network reliability.
- **Integration**:
    - Test the "5 Ws" interactions: Wallet posting to Witness, Watcher polling Witness.
    - **Exception for Challenge**: Focus exclusively on the **Register (POST)** and **Read (GET)** endpoints defined in the rubric. Test the signature verification logic for these specific transactions.

## Don't
- **Web-Only Tools**: Don't rely on HTTP-centric tools like Postman/Newman as primary verifiers; KERI is transport-agnostic (TCP/UDP/HTTP).
- **Loose Schemas**: Don't use generic JSON schema validators if they cannot validate CESR primitives (e.g., qualifying crypto material).
- **Ignore State**: Don't test messages in isolation; KERI is state-dependent (KEL history matters).
- **Network Dependency**: Don't rely on external networks for contract tests; use local fixtures or simulated streams.

## Notes / Examples
- **CESR Verification**:
    ```python
    from keri.core import coring
    def test_cesr_serialization():
        # ... setup serder ...
        raw = serder.raw
        assert coring.Matter(raw=raw).qb64 == expected_qb64
    ```
- **Duplicity Test**:
    - Generate `icp` event.
    - Generate two conflicting `rot` events for SN 1.
    - Submit first `rot` to Witness -> Expect `202 Accepted`.
    - Submit second `rot` to Witness -> Expect `409 Conflict` (or equivalent duplicity rejection).
- **OOBI Resolution**:
    - Verify that resolving an OOBI URL correctly returns the expected AID and endpoint proofs.