# KERI Signature Challenge - Falcon API Implementation

A Falcon-based REST API demonstrating HTTP signature authentication using KERI (Key Event Receipt Infrastructure).

## Features

- ✅ **POST /register** - Register user names for AIDs with signature verification
- ✅ **GET /read** - Query registrations by SAID, AID, or name with signature verification
- ✅ **Indexed Signatures** - Uses KERI indexed signatures (RFC 9421 compliant)
- ✅ **In-Memory Storage** - Simple dict-based storage for demonstration
- ✅ **Comprehensive Tests** - 11 integration tests covering happy paths and failure scenarios

## Installation

### Prerequisites

- Python 3.12 or higher
- pip

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd keri-challenge

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all API tests
python -m pytest tests/api/test_registration.py -v

# Run with coverage
python -m pytest tests/api/ --cov=src/api --cov-report=html

# Run a specific test
python -m pytest tests/api/test_registration.py::test_post_register_valid_signature -v
```

### Expected Output

```
tests/api/test_registration.py::test_post_register_valid_signature PASSED
tests/api/test_registration.py::test_get_by_said_valid_signature PASSED
tests/api/test_registration.py::test_get_by_aid_valid_signature PASSED
tests/api/test_registration.py::test_get_by_name_valid_signature PASSED
tests/api/test_registration.py::test_post_missing_signature_fails PASSED
tests/api/test_registration.py::test_post_invalid_signature_fails PASSED
tests/api/test_registration.py::test_post_tampered_body_fails PASSED
tests/api/test_registration.py::test_post_invalid_said_fails PASSED
tests/api/test_registration.py::test_get_missing_signature_fails PASSED
tests/api/test_registration.py::test_get_invalid_signature_fails PASSED
tests/api/test_registration.py::test_get_not_found PASSED

========================== 11 passed in 6.21s ==========================
```

## API Documentation

### POST /register

Register a user name for a given AID.

**Request:**
- **Headers:**
  - `Signature`: Indexed signature of request body (RFC 9421)
- **Body:** JSON with SAID
  ```json
  {
    "d": "EBWlLYZbAPb94YfGJu8SzZjC0YQkQWb5Kx2zcQ6HvYxQ",
    "i": "EOBYmfTYa_of-bk5JUSR96HB_ylfu0YFyM_GriR7aKfQ",
    "n": "John Doe"
  }
  ```

**Response:** 201 Created
- **Headers:**
  - `Signature`: Server's indexed signature of response body
- **Body:** Same as request

**Errors:**
- `400` - Missing fields, invalid JSON, or SAID mismatch
- `401` - Missing or invalid signature

### GET /read

Read registration data by query parameter.

**Request:**
- **Headers:**
  - `Signature`: Indexed signature of query string (RFC 9421)
  - `KERI-AID`: Signer's AID (if not in signature)
- **Query Parameters:** One of:
  - `SAID=<said>` - Look up by SAID
  - `AID=<aid>` - Look up by AID
  - `name=<name>` - Look up by name

**Response:** 200 OK
- **Headers:**
  - `Signature`: Server's indexed signature of response body
- **Body:** Registration dict (single) or list (multiple matches)

**Errors:**
- `400` - Missing query parameter or invalid signature header
- `401` - Missing or invalid signature
- `404` - No matching records

## Architecture

```
src/
├── api/
│   ├── __init__.py
│   ├── app.py          # Falcon app factory
│   ├── resources.py    # RegisterResource, ReadResource
│   └── storage.py      # In-memory dict storage
tests/
└── api/
    ├── __init__.py
    └── test_registration.py  # Integration tests
```

### Key Components

- **storage.py**: Module-level dict for in-memory data persistence
- **resources.py**: Falcon resource classes with signature verification
- **app.py**: Falcon application factory with route registration
- **test_registration.py**: Comprehensive test suite using Falcon Test Client

## Implementation Details

### Signature Generation

Uses KERI's `ending.signature()` to create RFC 9421 compliant signature headers:

```python
from keri.end import ending

sigers = hab.sign(ser=body_bytes, verfers=hab.kever.verfers)
signage = ending.Signage(markers=sigers, indexed=True, signer=None, 
                        ordinal=None, digest=None, kind=None)
header = ending.signature([signage])
# Returns: {'Signature': 'indexed="?1";0="AAC...";1="ABD...";2="ACD..."'}
```

### Signature Verification

Uses KERI's `ending.designature()` to parse and verify signatures:

```python
from keri.end import ending

signages = ending.designature(signature_header)
signage = signages[0]
markers = signage.markers

for idx, verfer in enumerate(verfers):
    siger = markers[str(idx)]
    siger.verfer = verfer
    if not verfer.verify(siger.raw, body_bytes):
        return False
```

### SAID Generation

Uses KERI's `Saider.saidify()` to compute Self-Addressing Identifiers:

```python
from keri.core import coring

data = {"d": "", "i": aid, "n": "John Doe"}
saider, data_with_said = coring.Saider.saidify(sad=data, label=coring.Saids.d)
# data_with_said now has computed SAID in "d" field
```

## Test Coverage

- ✅ Valid POST with signature verification
- ✅ Valid GET by SAID, AID, and name
- ✅ Missing signature rejection (401)
- ✅ Invalid/tampered signature rejection (401)
- ✅ Tampered body rejection (400/401)
- ✅ Invalid SAID rejection (400)
- ✅ Not found handling (404)

## References

- [RFC 9421 - HTTP Message Signatures](https://datatracker.ietf.org/doc/html/rfc9421)
- [RFC 8941 - Structured Field Values](https://www.rfc-editor.org/rfc/rfc8941.html)
- [KERI Specification](https://github.com/WebOfTrust/keri)
- [keripy Library](https://github.com/WebOfTrust/keripy)
- [Falcon Framework](https://falcon.readthedocs.io/)

## License

Apache 2.0
