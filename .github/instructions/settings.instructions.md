---
applyTo: "src/**/config/**/*.py,src/**/settings.py,**/*_config.py"
# Standards for application configuration, KERI bootstrapping, and secrets management
---
## Use when
- Defining application configuration (ports, database paths, log levels).
- Bootstrapping KERI AIDs, witnesses, or OOBI URLs.
- Handling environment variables and secrets.
- Configuring crypto-system parameters (e.g., salt, algorithms).

## Do
- **Library**: Use `pydantic-settings` for type-safe, validated configuration management.
- **Separation of Concerns**:
    - **Operational Config**: Store ephemeral operational data (host, port, log level) in environment variables or `.env` files.
    - **Identity Config**: Store KERI-specific bootstrapping data (witness lists, OOBI URLs) in configuration files or `pydantic` models.
    - **Secrets/Keys**: **NEVER** store private keys or salts in plain text settings files. Use the **Wallet** abstraction or secure keystores.
    - **Exception for Challenge**: For test fixtures, it is acceptable to configure constants (like salts for temporary Habs) directly in the test setup `conftest.py` or fixture code.
- **Validation**: Enforce strict types (e.g., `HttpUrl` for OOBIs, `DirectoryPath` for database storage).
- **Defaults**: Provide sensible defaults for *Development* environments (e.g., "indirect" mode, local witnesses), but fail fast if critical *Production* secrets are missing.
- **Immutability**: Settings should be loaded once at startup and treated as immutable during runtime.

## Don't
- **Hardcoding**: Don't hardcode AIDs, public keys, or OOBIs in source code; load them from config.
- **Key Leaks**: Don't put private keys, seeds, or salts in `settings.py` or `.env` files committed to git.
- **Complex Logic**: Don't put complex logic (like key derivation) inside settings classes. Keep settings simple and declarative.
- **Global Mutable State**: Avoid global mutable configuration objects. Use dependency injection to pass settings to components.

## Notes / Examples

### Pydantic Settings Example
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath, HttpUrl

class KeriSettings(BaseSettings):
    # Operational
    log_level: str = "INFO"
    base_dir: DirectoryPath = "/var/lib/keri"
    
    # KERI Bootstrapping
    witness_oobis: list[HttpUrl] = []
    indirect_mode: bool = True
    
    model_config = SettingsConfigDict(env_prefix="KERI_")

# Usage
settings = KeriSettings()
```

### Key Storage vs. Configuration
- **Configuration**: "Where do I connect?" (Witness URL), "Where do I store logs?" (File Path).
- **Wallet/Keystore**: "Who am I?" (Private Keys, Salts). *Do not mix these.*