# Action Plan - KERI Signature Challenge

## 🎯 Success Criteria (Pass/Fail)

The evaluator will:
1. Clone your public GitHub repo
2. Run `pytest` on their local machine
3. All tests must pass, demonstrating:
   - ✅ POST endpoint registers data with signature verification
   - ✅ GET endpoint retrieves data with signature verification
   - ✅ Invalid signatures are rejected with appropriate errors
   - ✅ Response signatures are generated and valid

---

## Phase 1: Learn the KERI Signature APIs (Study)

**Goal:** Understand how to use keripy's signature functions before writing any application code.

### 1.1 Read Reference Code
- [ ] Read `src/keri/end/ending.py` 
  - Focus on: `signature()` and `designature()` functions
  - Understand: `Signage` dataclass and how indexed signatures work
- [ ] Read `src/keri/app/httping.py`
  - Focus on: `SignatureValidationComponent` class
  - Understand: How to verify signature headers
- [ ] Read `src/keri/core/coring.py`
  - Focus on: `Saider` class for SAID generation
  - Understand: How to add SAIDs to dicts

### 1.2 Study Test Examples
- [ ] Read `tests/end/test_ending.py`
  - Find examples of calling `signature()` with indexed signers
  - Understand: How `hab.sign()` creates signers
- [ ] Read `tests/app/test_httping.py` (if exists)
  - Look for signature validation examples
- [ ] Run existing tests: `pytest tests/end/test_ending.py -v`
  - Observe how tests are structured
  - Note fixture patterns with `habbing.openHab()`

### 1.3 Experiment with Signatures (Optional)
- [ ] Create `scratch/experiment.py` to test signature generation:
  ```python
  from keri.app import habbing
  from keri.end import ending
  from keri.core import coring
  
  # Generate test AID and sign something
  with habbing.openHab(name="test", temp=True, salt=b'0123456789abcdef') as (hby, hab):
      # Test SAID generation
      data = {"i": hab.pre, "n": "John Doe"}
      saider = coring.Saider(qb64=coring.Saider.saidify(sad=data))
      
      # Test signing
      sigers = hab.sign(ser=saider.qb64b, verfers=hab.kever.verfers)
      
      # Generate signature header
      signage = ending.Signage(markers=sigers)
      header = ending.signature([signage])
      print(f"Header: {header}")
  ```

---

## Phase 2: Implement Core Components (Bottom-Up)

**Goal:** Build minimal, testable components in isolation.

### 2.1 In-Memory Storage
- [ ] Create `src/api/storage.py`:
  ```python
  # Module-level dict for registrations
  # Key: SAID, Value: {"d": SAID, "i": AID, "n": name}
  REGISTRY: dict[str, dict] = {}
  
  def register(data: dict) -> None:
      """Store registration keyed by SAID."""
      REGISTRY[data["d"]] = data
  
  def find_by_said(said: str) -> dict | None:
      """Retrieve by SAID."""
      return REGISTRY.get(said)
  
  def find_by_aid(aid: str) -> list[dict]:
      """Retrieve all registrations for AID."""
      return [v for v in REGISTRY.values() if v["i"] == aid]
  
  def find_by_name(name: str) -> list[dict]:
      """Retrieve all registrations for name."""
      return [v for v in REGISTRY.values() if v["n"] == name]
  
  def clear() -> None:
      """Clear all data (for tests)."""
      REGISTRY.clear()
  ```

### 2.2 Signature Utilities
- [ ] Create `src/api/signatures.py`:
  ```python
  from keri.end import ending
  from keri.core import coring
  
  def create_request_signature(hab, body_bytes: bytes) -> dict[str, str]:
      """Generate Signature header for request body."""
      sigers = hab.sign(ser=body_bytes, verfers=hab.kever.verfers)
      signage = ending.Signage(markers=sigers)
      return ending.signature([signage])
  
  def create_response_signature(hab, response_body: dict) -> dict[str, str]:
      """Generate Signature header for response body (with SAID)."""
      # Ensure response has SAID
      saider = coring.Saider(qb64=coring.Saider.saidify(sad=response_body))
      response_body["d"] = saider.qb64
      
      sigers = hab.sign(ser=saider.qb64b, verfers=hab.kever.verfers)
      signage = ending.Signage(markers=sigers)
      return ending.signature([signage])
  
  def verify_signature(signature_header: str, body_or_digest: bytes, verfers) -> bool:
      """Verify Signature header against body/digest."""
      # Use ending.designature() to parse header
      # Verify signatures using verfers
      # Return True if valid, False otherwise
      pass  # TODO: Implement
  ```

### 2.3 Test Storage & Signatures
- [ ] Create `tests/api/test_storage.py`:
  - Test registration, retrieval by SAID/AID/name
  - Test clear() function
- [ ] Create `tests/api/test_signatures.py`:
  - Test signature generation with test hab
  - Test signature verification with valid/invalid signatures

---

## Phase 3: Falcon API Implementation

**Goal:** Build Falcon resources with signature verification.

### 3.1 POST Endpoint - Register Data
- [ ] Create `src/api/resources.py`:
  ```python
  import falcon
  import json
  from keri.core import coring
  from keri.end import ending
  from . import storage
  from . import signatures
  
  class RegisterResource:
      def __init__(self, server_hab):
          self.hab = server_hab
      
      def on_post(self, req, resp):
          # 1. Read request body
          body_bytes = req.bounded_stream.read()
          body_data = json.loads(body_bytes)
          
          # 2. Verify signature header
          sig_header = req.get_header('Signature')
          if not sig_header:
              raise falcon.HTTPUnauthorized(description="Missing Signature header")
          
          # 3. Verify SAID in body matches computed SAID
          computed_said = coring.Saider.saidify(sad=body_data)
          if body_data.get("d") != computed_said:
              raise falcon.HTTPBadRequest(description="Invalid SAID")
          
          # 4. Verify signature (TODO: need client's verfers)
          # This requires looking up client AID from body_data["i"]
          
          # 5. Store data
          storage.register(body_data)
          
          # 6. Generate response signature
          response_headers = signatures.create_response_signature(self.hab, body_data)
          resp.set_headers(response_headers)
          
          resp.status = falcon.HTTP_201
          resp.media = body_data
  ```

### 3.2 GET Endpoint - Read Data
- [ ] Add to `src/api/resources.py`:
  ```python
  class ReadResource:
      def __init__(self, server_hab):
          self.hab = server_hab
      
      def on_get(self, req, resp):
          # 1. Verify signature on query string
          sig_header = req.get_header('Signature')
          if not sig_header:
              raise falcon.HTTPUnauthorized(description="Missing Signature header")
          
          # 2. Parse query params
          name = req.get_param('name')
          aid = req.get_param('AID')
          said = req.get_param('SAID')
          
          # 3. Query storage
          results = []
          if said:
              result = storage.find_by_said(said)
              if result:
                  results = [result]
          elif aid:
              results = storage.find_by_aid(aid)
          elif name:
              results = storage.find_by_name(name)
          
          if not results:
              raise falcon.HTTPNotFound()
          
          # 4. Generate response signature
          response_data = results[0] if len(results) == 1 else results
          response_headers = signatures.create_response_signature(self.hab, response_data)
          resp.set_headers(response_headers)
          
          resp.status = falcon.HTTP_200
          resp.media = response_data
  ```

### 3.3 Falcon App Factory
- [ ] Create `src/api/app.py`:
  ```python
  import falcon
  from .resources import RegisterResource, ReadResource
  
  def create_app(server_hab):
      """Create Falcon application with server habitat."""
      app = falcon.App()
      
      app.add_route('/register', RegisterResource(server_hab))
      app.add_route('/read', ReadResource(server_hab))
      
      return app
  ```

---

## Phase 4: Integration Tests (The Deliverable)

**Goal:** Write comprehensive pytest tests using Falcon Test Client.

### 4.1 Test Fixtures
- [ ] Create `tests/api/conftest.py`:
  ```python
  import pytest
  from keri.app import habbing
  from keri.core import coring
  from falcon import testing
  from api.app import create_app
  from api import storage
  
  @pytest.fixture(scope="function")
  def server_hab():
      """Server habitat (AID)."""
      with habbing.openHab(name="server", temp=True, salt=b'server__salt____') as (hby, hab):
          yield hab
  
  @pytest.fixture(scope="function")
  def client_hab():
      """Client habitat (AID)."""
      with habbing.openHab(name="client", temp=True, salt=b'client__salt____') as (hby, hab):
          yield hab
  
  @pytest.fixture(scope="function")
  def app(server_hab):
      """Falcon app with test server hab."""
      storage.clear()  # Clear storage before each test
      return create_app(server_hab)
  
  @pytest.fixture(scope="function")
  def client(app):
      """Falcon test client."""
      return testing.TestClient(app)
  ```

### 4.2 Happy Path Tests
- [ ] Create `tests/api/test_integration.py`:
  ```python
  def test_post_register_valid_signature(client, client_hab, server_hab):
      """POST with valid signature succeeds."""
      # 1. Create registration data
      data = {"i": client_hab.pre, "n": "John Doe"}
      saider = coring.Saider(qb64=coring.Saider.saidify(sad=data))
      data["d"] = saider.qb64
      
      # 2. Sign request body
      body_bytes = json.dumps(data).encode()
      sig_headers = signatures.create_request_signature(client_hab, body_bytes)
      
      # 3. POST request
      response = client.simulate_post(
          '/register',
          body=body_bytes,
          headers=sig_headers
      )
      
      # 4. Assert success
      assert response.status_code == 201
      assert response.json["d"] == data["d"]
      assert "Signature" in response.headers
      
      # 5. Verify response signature
      # TODO: verify server's signature
  
  def test_get_by_said_valid_signature(client, client_hab, server_hab):
      """GET with valid signature succeeds."""
      # 1. Setup: register data first
      # ... (similar to above)
      
      # 2. Sign query string
      query_string = f"SAID={said}"
      sig_headers = signatures.create_request_signature(client_hab, query_string.encode())
      
      # 3. GET request
      response = client.simulate_get(
          f'/read?{query_string}',
          headers=sig_headers
      )
      
      # 4. Assert success
      assert response.status_code == 200
      assert response.json["d"] == said
  ```

### 4.3 Failure Tests
- [ ] Add to `tests/api/test_integration.py`:
  ```python
  def test_post_missing_signature_fails(client, client_hab):
      """POST without Signature header returns 401."""
      data = {"i": client_hab.pre, "n": "John Doe", "d": "..."}
      response = client.simulate_post('/register', json=data)
      assert response.status_code == 401
  
  def test_post_invalid_signature_fails(client, client_hab, server_hab):
      """POST with tampered signature returns 401."""
      # Create valid request, then modify signature
      # ... 
      assert response.status_code == 401
  
  def test_post_tampered_body_fails(client, client_hab):
      """POST with valid signature but tampered body fails."""
      # Sign body, then modify body before sending
      # ...
      assert response.status_code in [400, 401]
  ```

---

## Phase 5: Documentation & Delivery

### 5.1 README
- [ ] Update `README.md`:
  - Installation instructions (`pip install -e .`)
  - How to run tests (`pytest tests/api/`)
  - API endpoints documentation
  - Example curl commands (if applicable)

### 5.2 Final Verification
- [ ] Run full test suite: `pytest tests/api/ -v`
- [ ] Ensure all tests pass
- [ ] Check test coverage: `pytest tests/api/ --cov=src/api`
- [ ] Clean up: Remove any `scratch/` or experimental code
- [ ] Commit and push to public GitHub repo

### 5.3 Pre-Submission Checklist
- [ ] Repository is public on GitHub
- [ ] `pytest` runs successfully from fresh clone
- [ ] README has clear installation/usage instructions
- [ ] All signature verifications are implemented (not stubbed)
- [ ] Tests include both success and failure cases
- [ ] Code uses `habbing.openHab()` for AID generation (as shown in rubric)
- [ ] Signatures use indexed format (as shown in rubric example)
- [ ] No database/LMDB/Docker dependencies

---

## 📚 Key Learning Resources

1. **RFC 9421** (HTTP Message Signatures): https://datatracker.ietf.org/doc/html/rfc9421
2. **RFC 8941** (Structured Field Values): https://www.rfc-editor.org/rfc/rfc8941.html
3. **keripy GitHub**: https://github.com/WebOfTrust/keripy
4. **Reference Tests**:
   - `tests/end/test_ending.py` - Signature generation
   - `tests/app/test_httping.py` - Signature validation
   - `tests/core/test_coring.py` - SAID generation

---

## 🚨 Common Pitfalls to Avoid

1. **Over-engineering**: Don't build complex architectures. This is a simple proof-of-concept.
2. **Database setup**: Use module-level dict, not LMDB.
3. **Forgetting to verify**: Both client AND server must verify signatures.
4. **Wrong signature format**: Use indexed signatures (as per rubric example).
5. **Not testing failures**: Must test invalid signature rejection.
6. **Missing response signatures**: Server must sign ALL responses (except errors).

---

**Estimated Timeline:**
- Phase 1 (Learning): 2-4 hours
- Phase 2 (Core): 2-3 hours
- Phase 3 (API): 2-3 hours
- Phase 4 (Tests): 3-4 hours
- Phase 5 (Docs): 1 hour

**Total: 10-15 hours**
