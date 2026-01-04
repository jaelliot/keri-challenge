# tests/api/test_registration.py
"""Integration tests for the registration API using Falcon Test Client."""

import json
import pytest

from falcon import testing
from keri.app import habbing
from keri.core import coring
from keri.end import ending

from api.app import create_app
from api import storage


@pytest.fixture(scope="function")
def server_hab():
    """Server habitat (AID) for signing responses."""
    with habbing.openHab(name="server", temp=True, salt=b'server__salt____') as (hby, hab):  # type: ignore
        yield hab


@pytest.fixture(scope="function")
def client_hab():
    """Client habitat (AID) for signing requests."""
    with habbing.openHab(name="client", temp=True, salt=b'client__salt____') as (hby, hab):  # type: ignore
        yield hab


@pytest.fixture(scope="function")
def app(server_hab, client_hab):
    """Falcon app with test server hab and verifier lookup."""
    storage.clear()  # Clear storage before each test
    
    # Simple verifier lookup that knows about our test client
    verfers_registry = {
        client_hab.pre: client_hab.kever.verfers
    }
    
    def get_verfers(aid):
        if aid not in verfers_registry:
            raise KeyError(f"Unknown AID: {aid}")
        return verfers_registry[aid]
    
    return create_app(server_hab, get_verfers)


@pytest.fixture(scope="function")
def client(app):
    """Falcon test client."""
    return testing.TestClient(app)


# ========== Happy Path Tests ==========

def test_post_register_valid_signature(client, client_hab, server_hab):
    """POST with valid signature succeeds."""
    # 1. Create registration data
    data = {"d": "", "i": client_hab.pre, "n": "John Doe"}
    saider, data_with_said = coring.Saider.saidify(sad=data, label=coring.Saids.d)
    
    # 2. Serialize body
    body_bytes = json.dumps(data_with_said, separators=(',', ':')).encode('utf-8')
    
    # 3. Sign request body
    sigers = client_hab.sign(ser=body_bytes, verfers=client_hab.kever.verfers)
    signage = ending.Signage(markers=sigers, indexed=True, signer=None, ordinal=None,
                            digest=None, kind=None)
    sig_headers = ending.signature([signage])
    
    # 4. POST request
    response = client.simulate_post(
        '/register',
        body=body_bytes.decode('utf-8'),
        headers=sig_headers
    )
    
    # 5. Assert success
    assert response.status_code == 201
    assert response.json["d"] == saider.qb64
    assert response.json["i"] == client_hab.pre
    assert response.json["n"] == "John Doe"
    assert "Signature" in response.headers
    
    # 6. Verify response signature exists
    assert response.headers["Signature"] is not None


def test_get_by_said_valid_signature(client, client_hab, server_hab):
    """GET by SAID with valid signature succeeds."""
    # 1. Setup: register data first
    data = {"d": "", "i": client_hab.pre, "n": "Jane Doe"}
    saider, data_with_said = coring.Saider.saidify(sad=data, label=coring.Saids.d)
    storage.register(data_with_said)
    
    # 2. Sign query string
    query_string = f"SAID={saider.qb64}"
    sigers = client_hab.sign(ser=query_string.encode('utf-8'), verfers=client_hab.kever.verfers)
    signage = ending.Signage(markers=sigers, indexed=True, signer=client_hab.pre, ordinal=None,
                            digest=None, kind=None)
    sig_headers = ending.signature([signage])
    
    # 3. GET request
    response = client.simulate_get(
        f'/read?{query_string}',
        headers=sig_headers
    )
    
    # 4. Assert success
    assert response.status_code == 200
    assert response.json["d"] == saider.qb64
    assert response.json["n"] == "Jane Doe"
    assert "Signature" in response.headers


def test_get_by_aid_valid_signature(client, client_hab, server_hab):
    """GET by AID with valid signature succeeds."""
    # 1. Setup: register data
    data = {"d": "", "i": client_hab.pre, "n": "Bob Smith"}
    saider, data_with_said = coring.Saider.saidify(sad=data, label=coring.Saids.d)
    storage.register(data_with_said)
    
    # 2. Sign query string
    query_string = f"AID={client_hab.pre}"
    sigers = client_hab.sign(ser=query_string.encode('utf-8'), verfers=client_hab.kever.verfers)
    signage = ending.Signage(markers=sigers, indexed=True, signer=client_hab.pre, ordinal=None,
                            digest=None, kind=None)
    sig_headers = ending.signature([signage])
    
    # 3. GET request
    response = client.simulate_get(
        f'/read?{query_string}',
        headers=sig_headers
    )
    
    # 4. Assert success
    assert response.status_code == 200
    # Returns single dict when only one match
    assert isinstance(response.json, dict)
    assert response.json["i"] == client_hab.pre


def test_get_by_name_valid_signature(client, client_hab, server_hab):
    """GET by name with valid signature succeeds."""
    # 1. Setup: register data
    data = {"d": "", "i": client_hab.pre, "n": "Alice Wonder"}
    saider, data_with_said = coring.Saider.saidify(sad=data, label=coring.Saids.d)
    storage.register(data_with_said)
    
    # 2. Sign query string
    query_string = "name=Alice Wonder"
    sigers = client_hab.sign(ser=query_string.encode('utf-8'), verfers=client_hab.kever.verfers)
    signage = ending.Signage(markers=sigers, indexed=True, signer=client_hab.pre, ordinal=None,
                            digest=None, kind=None)
    sig_headers = ending.signature([signage])
    
    # 3. GET request
    response = client.simulate_get(
        f'/read?{query_string}',
        headers=sig_headers
    )
    
    # 4. Assert success
    assert response.status_code == 200
    # Returns single dict when only one match
    assert isinstance(response.json, dict)
    assert response.json["n"] == "Alice Wonder"


# ========== Failure Tests ==========

def test_post_missing_signature_fails(client, client_hab):
    """POST without Signature header returns 401."""
    data = {"d": "", "i": client_hab.pre, "n": "John Doe"}
    saider, data_with_said = coring.Saider.saidify(sad=data, label=coring.Saids.d)
    body_bytes = json.dumps(data_with_said).encode('utf-8')
    
    response = client.simulate_post(
        '/register',
        body=body_bytes.decode('utf-8')
    )
    
    assert response.status_code == 401


def test_post_invalid_signature_fails(client, client_hab, server_hab):
    """POST with tampered signature returns 401."""
    # 1. Create valid request
    data = {"d": "", "i": client_hab.pre, "n": "John Doe"}
    saider, data_with_said = coring.Saider.saidify(sad=data, label=coring.Saids.d)
    body_bytes = json.dumps(data_with_said, separators=(',', ':')).encode('utf-8')
    
    # 2. Sign it
    sigers = client_hab.sign(ser=body_bytes, verfers=client_hab.kever.verfers)
    signage = ending.Signage(markers=sigers, indexed=True, signer=None, ordinal=None,
                            digest=None, kind=None)
    sig_headers = ending.signature([signage])
    
    # 3. Tamper with signature
    sig_headers['Signature'] = sig_headers['Signature'].replace('AAC', 'BBB')
    
    # 4. POST request
    response = client.simulate_post(
        '/register',
        body=body_bytes.decode('utf-8'),
        headers=sig_headers
    )
    
    # 5. Assert failure
    assert response.status_code == 401


def test_post_tampered_body_fails(client, client_hab):
    """POST with valid signature but tampered body fails."""
    # 1. Create and sign original body
    data = {"d": "", "i": client_hab.pre, "n": "John Doe"}
    saider, data_with_said = coring.Saider.saidify(sad=data, label=coring.Saids.d)
    body_bytes = json.dumps(data_with_said, separators=(',', ':')).encode('utf-8')
    
    sigers = client_hab.sign(ser=body_bytes, verfers=client_hab.kever.verfers)
    signage = ending.Signage(markers=sigers, indexed=True, signer=None, ordinal=None,
                            digest=None, kind=None)
    sig_headers = ending.signature([signage])
    
    # 2. Tamper with body
    data_with_said["n"] = "Evil Hacker"
    tampered_body = json.dumps(data_with_said, separators=(',', ':')).encode('utf-8')
    
    # 3. POST request with tampered body
    response = client.simulate_post(
        '/register',
        body=tampered_body.decode('utf-8'),
        headers=sig_headers
    )
    
    # 4. Assert failure (400 for SAID mismatch or 401 for signature failure)
    assert response.status_code in [400, 401]


def test_post_invalid_said_fails(client, client_hab):
    """POST with mismatched SAID returns 400."""
    # 1. Create data with wrong SAID
    data = {
        "d": "EInvalidSAIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "i": client_hab.pre,
        "n": "John Doe"
    }
    body_bytes = json.dumps(data, separators=(',', ':')).encode('utf-8')
    
    # 2. Sign it (signature will be valid for this body)
    sigers = client_hab.sign(ser=body_bytes, verfers=client_hab.kever.verfers)
    signage = ending.Signage(markers=sigers, indexed=True, signer=None, ordinal=None,
                            digest=None, kind=None)
    sig_headers = ending.signature([signage])
    
    # 3. POST request
    response = client.simulate_post(
        '/register',
        body=body_bytes.decode('utf-8'),
        headers=sig_headers
    )
    
    # 4. Assert failure
    assert response.status_code == 400


def test_get_missing_signature_fails(client, client_hab):
    """GET without Signature header returns 401."""
    response = client.simulate_get('/read?name=John')
    assert response.status_code == 401


def test_get_invalid_signature_fails(client, client_hab, server_hab):
    """GET with tampered signature returns 401."""
    # 1. Setup: register data
    data = {"d": "", "i": client_hab.pre, "n": "Jane Doe"}
    saider, data_with_said = coring.Saider.saidify(sad=data, label=coring.Saids.d)
    storage.register(data_with_said)
    
    # 2. Sign query string
    query_string = f"SAID={saider.qb64}"
    sigers = client_hab.sign(ser=query_string.encode('utf-8'), verfers=client_hab.kever.verfers)
    signage = ending.Signage(markers=sigers, indexed=True, signer=client_hab.pre, ordinal=None,
                            digest=None, kind=None)
    sig_headers = ending.signature([signage])
    
    # 3. Tamper with signature more aggressively
    original_sig = sig_headers['Signature']
    # Flip some bits in the signature value
    tampered_sig = original_sig[:50] + ('Z' if original_sig[50] != 'Z' else 'A') + original_sig[51:]
    sig_headers['Signature'] = tampered_sig
    
    # 4. GET request
    response = client.simulate_get(
        f'/read?{query_string}',
        headers=sig_headers
    )
    
    # 5. Assert failure
    assert response.status_code == 401


def test_get_not_found(client, client_hab, server_hab):
    """GET for non-existent record returns 404."""
    # 1. Sign query string
    query_string = "name=NonExistent"
    sigers = client_hab.sign(ser=query_string.encode('utf-8'), verfers=client_hab.kever.verfers)
    signage = ending.Signage(markers=sigers, indexed=True, signer=client_hab.pre, ordinal=None,
                            digest=None, kind=None)
    sig_headers = ending.signature([signage])
    
    # 2. GET request
    response = client.simulate_get(
        f'/read?{query_string}',
        headers=sig_headers
    )
    
    # 3. Assert not found
    assert response.status_code == 404
