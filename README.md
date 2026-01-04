# KERI Programming Challenge

Python Implementation of the KERI Core Libraries with Challenge Extensions

## Project Structure

```
.
├── src/keri/           # KERI core library (from weboftrust/keripy)
├── tests/              # Full test suite
├── docs/
│   ├── adr/            # Architecture Decision Records
│   └── keri-spec/      # KERI specification
├── .github/
│   └── instructions/   # Development guidelines and patterns
├── Dockerfile          # Production container
├── docker-compose.yml  # Multi-service orchestration
├── pyproject.toml      # Modern Python packaging
└── Makefile            # Development commands
```

## Quick Start

### Local Development

```bash
# Install dependencies
make install

# Run tests
make test
```

### Docker Deployment

```bash
# Build image
make build

# Start services (witness, watcher, controller)
make up

# View logs
make logs

# Stop services
make down
```

## Requirements

- Python 3.12.1+
- libsodium 1.0.18+
- Docker (optional, for containerized deployment)

### libsodium Installation (macOS)

```bash
brew install libsodium
sudo ln -s /opt/homebrew/lib /usr/local/lib
```

## Development Commands

```bash
make help          # Show all available targets
make install       # Install in development mode
make test          # Run test suite
make test-cov      # Run tests with coverage
make clean         # Clean build artifacts
make clean-data    # Clean data volumes
```

## Architecture

This project follows KERI Foundation standards:
- **End-Verifiability**: Zero trust in infrastructure
- **Python-First**: Idiomatic Python 3.12+
- **Open Standards**: KERI, ACDC, CESR compliance
- **Production-Grade**: SOC 2 / eIDAS ready

See [docs/adr/](docs/adr/) for detailed architectural decisions.

## License

Apache Software License 2.0
