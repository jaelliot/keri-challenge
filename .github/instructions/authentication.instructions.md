---
applyTo: "**/*.py,tests/**/*.py"
# Authentication standards using KERI AIDs, CESR signatures, and OOBI for decentralized identity
---
## Use when
- Implementing authentication flows (challenge/response).
- Verifying cryptographic signatures (CESR).
- Managing Controller identities (Wallets).
- Establishing connections via OOBI (Out-Of-Band Introduction).
- Validating Key Event Logs (KELs) for authorization.

## Do
- **Zero-Trust**: Authenticate via cryptographic verification of signatures against the current Key State (from KEL), not via passwords or shared secrets.
- **AID-Based Auth**: Use Autonomic Identifiers (AIDs) as the primary subject of authentication.
- **Challenge/Response**: Implement authentication using a challenge signed by the Controller's private key.
- **CESR Encoding**: Use CESR (Composable Event Streaming Representation) for all cryptographic primitives (keys, signatures).
- **OOBI Bootstrapping**: Use Out-Of-Band Introduction (OOBI) URLs to discover and authenticate initial connections.
- **Exception for Challenge**: For this challenge, OOBI is not required. You can assume the "Host AID" and "Requestor AID" are known or exchanged via the test fixture setup. Focus on verifying the **Signature Header** on the HTTP requests.
- **KEL Verification**: Always verify the KEL to establish the current authoritative public keys before accepting a signature.
- **Pass-through**: Forward OOBI/KEL requests to the core `keripy` logic for validation; do not reimplement KERI core logic in application layers.

## Don't
- **No Shared Secrets**: Do not use passwords, bearer tokens, or API keys for primary authentication.
- **No Centralized Auth**: Do not rely on a central identity provider (IdP) or OAuth/OIDC unless bridging to legacy systems.
- **Avoid JWTs**: Prefer CESR-encoded KERI events over JWTs for internal protocol messages.
- **Don't Hardcode Keys**: Never hardcode private keys or seeds. Use secure keystore abstractions.
- **Don't Trust Infrastructure**: Do not trust the network transport (TLS) alone; verify the end-to-end KERI signature.

## Notes / Examples
- **Authentication Flow**:
  1. **Challenge**: Verifier sends a random nonce.
  2. **Response**: Prover signs the nonce with their AID's current private key.
  3. **Verification**: Verifier checks the signature against the AID's current key state (derived from KEL).
- **OOBI Example**: `http://witness.example.com/oobi/{AID}` enables discovery.
- **Signature Verification**: Use `keripy` primitives to verify CESR-attached signatures.