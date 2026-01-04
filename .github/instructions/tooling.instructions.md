---
applyTo: "Dockerfile*,docker-compose*.yml,.dockerignore"
# Docker usage, build standards, and container security for KERI components
---
## Use when
- Editing `Dockerfile`, `docker-compose.yml`, or related container configuration.
- Building or deploying containerized KERI applications (Witnesses, Watchers, Agents, Controllers).
- Configuring development environments using Docker.

## Do
- **Base Image**: Strictly use `python:3.12.10-slim-bookworm` (or newer patch version) as the base image to match the project charter.
- **System Dependencies**:
    - Install `libsodium-dev` (or `libsodium23` runtime) as it is required for `pysodium`.
    - Install build tools (`build-essential`) in a multi-stage build if compiling `blake3` or other extensions from source.
- **Security**:
    - Create and run as a **dedicated non-root user** (e.g., `keri` UID 1000).
    - Use `COPY` with `--chown=keri:keri` to ensure permissions are correct.
    - Use ephemeral or read-only root filesystems where possible, with writable volumes *only* for KEL/DB storage.
- **Optimization**:
    - Use **multi-stage builds** to keep the runtime image minimal.
    - Leverage layer caching by installing dependencies (via `pip`) before copying source code.
    - Clean up apt caches (`rm -rf /var/lib/apt/lists/*`) in the same layer as installation.
- **Configuration**:
    - Use **environment variables** for configuration.
    - Set `PYTHONUNBUFFERED=1` to ensure logs flow to stdout/stderr immediately.
    - Set `PYTHONDONTWRITEBYTECODE=1` to avoid `.pyc` clutter in containers.
- **Persistence**:
    - Define explicit volumes for KERI data directories (default `~/.keri` or `/usr/local/var/keri`) to persist Key Event Logs (KELs) and identifiers.
- **Networking**:
    - Expose only necessary ports (e.g., HTTP 5642, TCP 5643 for Witnesses).
    - Use Docker networks to isolate Witness/Watcher pools from other services.

## Don't
- **Never** run KERI components as `root`.
- **Never** embed private keys, salts, or passcodes in the image. Use secrets management or environment variables at runtime.
- **Never** use `latest` tags for base images; pin to specific SHA or version tags.
- **Avoid** installing unnecessary system packages (like `redis-tools`, `netcat`, `vim`) in the production runtime image.
- **Avoid** complex entrypoint scripts if possible; prefer direct command execution or a simple shell wrapper handling signals.

## Notes / Examples

### KERI Component Dockerfile (Multi-stage)

```dockerfile
# Build Stage
FROM python:3.12.10-slim-bookworm as builder

WORKDIR /app

# Install build dependencies for crypto (libsodium, blake3)
RUN apt-get update && apt-get install -y \
    build-essential \
    libsodium-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY pyproject.toml .
# Assuming using pip or similar tool to install into a virtualenv or user install
RUN pip install --no-cache-dir --prefix=/install .

# Runtime Stage
FROM python:3.12.10-slim-bookworm as runtime

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash keri

# Install runtime libs (libsodium is needed for pysodium)
RUN apt-get update && apt-get install -y \
    libsodium23 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

WORKDIR /home/keri

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Switch to user
USER keri

# Default command (can be overridden)
ENTRYPOINT ["kli"]
CMD ["--help"]
```

### Docker Compose Service (Witness)

```yaml
services:
  witness:
    image: keri-witness:1.0.0
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    ports:
      - "5642:5642" # HTTP
      - "5643:5643" # TCP
    volumes:
      - witness-data:/home/keri/.keri
    environment:
      - KERI_SCRIPT_DIR=/home/keri/scripts
      - KERI_KLI_WITNESS_DEMO=true
    networks:
      - keri-net

volumes:
  witness-data:

networks:
  keri-net:
    driver: bridge
```