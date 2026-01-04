# src/api/storage.py
"""In-memory storage for user registrations.

Stores data in module-level dict as per rubric requirements.
"""

# Module-level dict for registrations
# Key: SAID, Value: {"d": SAID, "i": AID, "n": name}
REGISTRY: dict[str, dict] = {}


def register(data: dict) -> None:
    """Store registration keyed by SAID.
    
    Args:
        data: Registration data with 'd' (SAID), 'i' (AID), 'n' (name)
    """
    REGISTRY[data["d"]] = data


def find_by_said(said: str) -> dict | None:
    """Retrieve registration by SAID.
    
    Args:
        said: SAID value to look up
        
    Returns:
        Registration dict or None if not found
    """
    return REGISTRY.get(said)


def find_by_aid(aid: str) -> list[dict]:
    """Retrieve all registrations for a given AID.
    
    Args:
        aid: AID value to search for
        
    Returns:
        List of registration dicts matching the AID
    """
    return [v for v in REGISTRY.values() if v["i"] == aid]


def find_by_name(name: str) -> list[dict]:
    """Retrieve all registrations for a given name.
    
    Args:
        name: Name to search for
        
    Returns:
        List of registration dicts matching the name
    """
    return [v for v in REGISTRY.values() if v["n"] == name]


def clear() -> None:
    """Clear all data (for tests)."""
    REGISTRY.clear()
