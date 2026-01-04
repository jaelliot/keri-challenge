# KERI Signature Challenge - Falcon API

**Falcon-based REST API demonstrating HTTP signature authentication using KERI (Key Event Receipt Infrastructure)**

This implementation fulfills the [KERI Foundation Programming Challenge](docs/rubric.md) requirements:
- ✅ Falcon web framework with indexed signatures (RFC 9421)
- ✅ POST /register endpoint with SAID verification
- ✅ GET /read endpoint with query parameter signatures
- ✅ Full signature verification on all requests and responses
- ✅ In-memory storage (no database required)
- ✅ Comprehensive test suite with failure scenarios

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd keri-challenge

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
```

### Run Tests

```bash
# Run the API integration tests
pytest tests/api/test_registration.py -v

# Expected output:
# ========================== 11 passed in ~6s ==========================
```

## 📋 Challenge Requirements

See [docs/rubric.md](docs/rubric.md) for the complete challenge specification.

### Implemented Features

**POST /register**
- Registers user name for a given AID
- Request body: JSON with SAID (`d`), AID (`i`), and name (`n`)
- Request must include `Signature` header with indexed signatures
- Response returns same JSON with server's signature

**GET /read**
- Query by `?name=`, `?AID=`, or `?SAID=`
- Request signature covers the query parameter string
- Response includes signed JSON body

**Signature Verification**
- All requests verified by server
- All responses signed by server
- Tests include invalid/tampered signature rejection

## 📁 Project Structure

```
.
├── src/
│   ├── api/                 # Challenge implementation
│   │   ├── app.py          # Falcon application factory
│   │   ├── resources.py    # POST /register, GET /read endpoints
│   │   └── storage.py      # In-memory dict storage
│   └── keri/               # KERI core library (keripy)
│
├── tests/
│   └── api/
│       └── test_registration.py  # 11 integration tests
│
├── docs/
│   ├── rubric.md           # Challenge specification
│   └── action-plan.md      # Implementation guide
│
├── API-README.md           # Detailed API documentation
└── pyproject.toml          # Python package configuration
```

## 🧪 Test Coverage

All 11 tests pass, covering:

**Happy Paths:**
- ✅ POST with valid signature → 201
- ✅ GET by SAID/AID/name → 200
- ✅ Response signatures present and valid

**Failure Scenarios:**
- ✅ Missing signature → 401
- ✅ Invalid/tampered signature → 401
- ✅ Tampered request body → 400/401
- ✅ Invalid SAID → 400
- ✅ Not found → 404

## 📖 Documentation

- **[API-README.md](API-README.md)** - Complete API documentation with examples
- **[docs/rubric.md](docs/rubric.md)** - Original challenge specification
- **[docs/action-plan.md](docs/action-plan.md)** - Implementation roadmap

## 🔑 Key Implementation Details

### Signature Generation

```python
from keri.end import ending

sigers = hab.sign(ser=body_bytes, verfers=hab.kever.verfers)
signage = ending.Signage(markers=sigers, indexed=True, signer=None, 
                        ordinal=None, digest=None, kind=None)
header = ending.signature([signage])
# Returns: {'Signature': 'indexed="?1";0="AAC...";1="ABD..."'}
```

### SAID Computation

```python
from keri.core import coring

data = {"d": "", "i": aid, "n": "John Doe"}
saider, data_with_said = coring.Saider.saidify(sad=data, label=coring.Saids.d)
# data_with_said["d"] now contains the computed SAID
```

## 🛠️ Technology Stack

- **Web Framework:** Falcon 4.2.0
- **KERI Library:** keripy 2.0.0-dev3
- **Testing:** pytest 9.0.2 with Falcon Test Client
- **Python:** 3.12+
- **Signatures:** RFC 9421 HTTP Message Signatures
- **Storage:** In-memory Python dict (as per rubric)

## 📚 References

- [RFC 9421 - HTTP Message Signatures](https://datatracker.ietf.org/doc/html/rfc9421)
- [RFC 8941 - Structured Field Values](https://www.rfc-editor.org/rfc/rfc8941.html)
- [keripy Library](https://github.com/WebOfTrust/keripy)
- [KERI Specification](https://github.com/WebOfTrust/keri)
- [Falcon Framework](https://falcon.readthedocs.io/)

## ✅ Verification Checklist

For evaluators running the challenge:

```bash
# 1. Install
pip install -e ".[dev]"

# 2. Run tests
pytest tests/api/test_registration.py -v

# 3. Verify all pass
# Expected: 11 passed in ~6 seconds
```

## 📄 License

Apache Software License 2.0
