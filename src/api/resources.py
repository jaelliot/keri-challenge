# src/api/resources.py
"""Falcon resource classes for /register and /read endpoints."""

import json
import falcon

from keri.core import coring
from keri.end import ending

from . import storage


class RegisterResource:
    """POST /register - Register user name for an AID."""
    
    def __init__(self, server_hab, client_verfers_lookup):
        """Initialize with server habitat and client verifier lookup.
        
        Args:
            server_hab: Server's KERI habitat (for signing responses)
            client_verfers_lookup: Callable that takes AID and returns list of Verfers
        """
        self.hab = server_hab
        self.get_client_verfers = client_verfers_lookup
    
    def on_post(self, req, resp):
        """Handle POST request to register data.
        
        Request must have:
        - JSON body with {"d": SAID, "i": AID, "n": name}
        - Signature header signed by client AID
        
        Response:
        - 201 with same JSON body
        - Signature header signed by server AID
        """
        # 1. Read and parse body
        body_bytes = req.bounded_stream.read()
        try:
            body_data = json.loads(body_bytes)
        except (json.JSONDecodeError, ValueError):
            raise falcon.HTTPBadRequest(description="Invalid JSON body")
        
        # 2. Validate required fields
        if not all(k in body_data for k in ["d", "i", "n"]):
            raise falcon.HTTPBadRequest(description="Missing required fields: d, i, n")
        
        # 3. Verify signature header exists
        sig_header = req.get_header('Signature')
        if not sig_header:
            raise falcon.HTTPUnauthorized(description="Missing Signature header")
        
        # 4. Verify SAID matches body
        try:
            # Make a copy with empty SAID to recompute it
            sad_for_verification = body_data.copy()
            sad_for_verification["d"] = ""
            computed_saider = coring.Saider.saidify(sad=sad_for_verification, label=coring.Saids.d)[0]
            computed_said = computed_saider.qb64
        except Exception as e:
            raise falcon.HTTPBadRequest(description=f"SAID computation error: {e}")
        if body_data["d"] != computed_said:
            raise falcon.HTTPBadRequest(description="SAID mismatch")
        
        # 5. Verify signature
        client_aid = body_data["i"]
        try:
            verfers = self.get_client_verfers(client_aid)
        except KeyError:
            raise falcon.HTTPUnauthorized(description=f"Unknown AID: {client_aid}")
        
        if not self._verify_signature(sig_header, body_bytes, verfers):
            raise falcon.HTTPUnauthorized(description="Signature verification failed")
        
        # 6. Store data
        storage.register(body_data)
        
        # 7. Generate response signature
        response_body = body_data.copy()
        sigers = self.hab.sign(ser=body_data["d"].encode('utf-8'), verfers=self.hab.kever.verfers)
        signage = ending.Signage(markers=sigers, indexed=True, signer=None, ordinal=None,
                                digest=None, kind=None)
        sig_headers = ending.signature([signage])
        
        # 8. Set response
        resp.status = falcon.HTTP_201
        resp.media = response_body
        resp.set_header('Signature', sig_headers['Signature'])
    
    def _verify_signature(self, sig_header: str, body_bytes: bytes, verfers: list) -> bool:
        """Verify signature header against body using verfers.
        
        Args:
            sig_header: Signature header value
            body_bytes: Raw request body bytes
            verfers: List of Verfer objects for the signer
            
        Returns:
            True if signature valid, False otherwise
        """
        try:
            signages = ending.designature(sig_header)
            if not signages:
                return False
            
            signage = signages[0]
            markers = signage.markers
            
            # Verify each indexed signature
            for idx, verfer in enumerate(verfers):
                key = str(idx)
                if key not in markers:
                    return False
                
                siger = markers[key]
                siger.verfer = verfer
                
                if not verfer.verify(siger.raw, body_bytes):
                    return False
            
            return True
        except Exception:
            return False


class ReadResource:
    """GET /read - Read data by query parameter."""
    
    def __init__(self, server_hab, client_verfers_lookup):
        """Initialize with server habitat and client verifier lookup.
        
        Args:
            server_hab: Server's KERI habitat (for signing responses)
            client_verfers_lookup: Callable that takes AID and returns list of Verfers
        """
        self.hab = server_hab
        self.get_client_verfers = client_verfers_lookup
    
    def on_get(self, req, resp):
        """Handle GET request to read data.
        
        Query params: ?name=X or ?AID=X or ?SAID=X
        Request must have Signature header signing the query string
        
        Response:
        - 200 with JSON body
        - Signature header signed by server AID
        """
        # 1. Verify signature header exists
        sig_header = req.get_header('Signature')
        if not sig_header:
            raise falcon.HTTPUnauthorized(description="Missing Signature header")
        
        # 2. Get signer AID from signature or require it in header
        # For simplicity, we'll extract from signature
        try:
            signages = ending.designature(sig_header)
            if signages and signages[0].signer:
                client_aid = signages[0].signer
            else:
                # If not in signature, require KERI-AID header
                client_aid = req.get_header('KERI-AID')
                if not client_aid:
                    raise falcon.HTTPBadRequest(description="Cannot determine signer AID")
        except Exception:
            raise falcon.HTTPBadRequest(description="Invalid Signature header")
        
        # 3. Get query string and verify signature
        query_string = req.query_string
        if not query_string:
            raise falcon.HTTPBadRequest(description="Missing query parameter")
        
        try:
            verfers = self.get_client_verfers(client_aid)
        except KeyError:
            raise falcon.HTTPUnauthorized(description=f"Unknown AID: {client_aid}")
        
        if not self._verify_signature(sig_header, query_string.encode('utf-8'), verfers):
            raise falcon.HTTPUnauthorized(description="Signature verification failed")
        
        # 4. Parse query params
        name = req.get_param('name')
        aid = req.get_param('AID')
        said = req.get_param('SAID')
        
        if not any([name, aid, said]):
            raise falcon.HTTPBadRequest(description="Must provide name, AID, or SAID parameter")
        
        # 5. Query storage
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
            raise falcon.HTTPNotFound(description="No matching records found")
        
        # 6. Generate response
        response_data = results[0] if len(results) == 1 else results
        
        # 7. Generate response signature (sign the SAID of response)
        if isinstance(response_data, list):
            # For lists, sign a combined representation
            response_said = coring.Saider.saidify(sad={"data": response_data}, label=coring.Saids.d)[0].qb64
        else:
            response_said = response_data["d"]
        
        sigers = self.hab.sign(ser=response_said.encode('utf-8'), verfers=self.hab.kever.verfers)
        signage = ending.Signage(markers=sigers, indexed=True, signer=None, ordinal=None,
                                digest=None, kind=None)
        sig_headers = ending.signature([signage])
        
        # 8. Set response
        resp.status = falcon.HTTP_200
        resp.media = response_data
        resp.set_header('Signature', sig_headers['Signature'])
    
    def _verify_signature(self, sig_header: str, query_bytes: bytes, verfers: list) -> bool:
        """Verify signature header against query string using verfers.
        
        Args:
            sig_header: Signature header value
            query_bytes: Raw query string bytes
            verfers: List of Verfer objects for the signer
            
        Returns:
            True if signature valid, False otherwise
        """
        try:
            signages = ending.designature(sig_header)
            if not signages:
                return False
            
            signage = signages[0]
            markers = signage.markers
            
            # Verify each indexed signature
            for idx, verfer in enumerate(verfers):
                key = str(idx)
                if key not in markers:
                    return False
                
                siger = markers[key]
                siger.verfer = verfer
                
                if not verfer.verify(siger.raw, query_bytes):
                    return False
            
            return True
        except Exception:
            return False
