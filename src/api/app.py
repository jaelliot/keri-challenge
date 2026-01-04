# src/api/app.py
"""Falcon application factory."""

import falcon
from .resources import RegisterResource, ReadResource


def create_app(server_hab, client_verfers_lookup):
    """Create and configure Falcon application.
    
    Args:
        server_hab: Server's KERI habitat (for signing responses)
        client_verfers_lookup: Callable that takes AID and returns list of Verfers
        
    Returns:
        Configured Falcon app instance
    """
    app = falcon.App()
    
    # Add routes
    app.add_route('/register', RegisterResource(server_hab, client_verfers_lookup))
    app.add_route('/read', ReadResource(server_hab, client_verfers_lookup))
    
    return app
