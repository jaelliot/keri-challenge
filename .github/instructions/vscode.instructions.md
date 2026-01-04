---
applyTo: ".vscode/*.json,.vscode/README.md"
# VS Code configuration standards and selective inclusion patterns for KERI Python development
---
## Use when
- Configuring VS Code settings for the KERI project.
- Editing files in `.vscode/`.
- Setting up development environment consistency for the "5 Ws" (Wallets, Witnesses, Watchers, Web, Wizards).

## Do
- **Selective Inclusion**:
  - Keep project-wide settings versioned while ignoring user-specific overrides.
  - Pattern: Ignore `.vscode/*` in `.gitignore` but force include `settings.json`, `extensions.json`, `tasks.json`, and `README.md`.
- **Python-Specific Settings**:
  - Configure `python.analysis.typeCheckingMode` to `strict` (MyPy/Pylance) to enforce the "Signed-Everything" rigor.
  - Set `python.defaultInterpreterPath` to `${workspaceFolder}/.venv/bin/python`.
  - Enable `ruff` for linting and formatting (replaces Black, Isort, Flake8).
  - Enable `pytest` integration with auto-discovery.
- **Extensions**:
  - Recommend `ms-python.python` for core Python support.
  - Recommend `astral-sh.ruff` (formerly `charliermarsh.ruff`) for high-performance linting/formatting.
  - Recommend `tamasfe.even-better-toml` for `pyproject.toml` support.
  - Recommend `redhat.vscode-yaml` for configuration files.
  - Recommend `streetsidesoftware.code-spell-checker` for catching typos in specs/docs (KERI/CESR jargon).
- **Cleanup**:
  - **Audit**: actively remove legacy extensions from `extensions.json` that are not relevant to KERI/Python (e.g., Redis, Mongo, Node.js).
- **Tasks**:
  - Define tasks for common KERI operations: `pytest`, `mypy`, `ruff check`, `ruff format`.
  - Include tasks for KERI-specific workflows if applicable (e.g., launching a witness).

## Don't
- **Secrets**: NEVER commit `.env` files or credentials (keys, seeds, salts) in `.vscode` config.
- **Paths**: Don't use absolute paths; use `${workspaceFolder}` for portability.
- **Polyglot Clutter**: Don't include Node.js, Docker, Redis, or other non-Python extensions unless strictly required for a specific "Wizard" or tool. Focus on the core Python library (`keripy`).
- **User Overrides**: Don't commit `.vscode/launch.json` unless it contains generic, shared debug configurations for the core library.

## Notes / Examples
- **Gitignore Pattern**:
  ```gitignore
  .vscode/*
  !.vscode/settings.json
  !.vscode/extensions.json
  !.vscode/tasks.json
  !.vscode/README.md
  ```
- **Extensions (`extensions.json`)**:
  ```json
  {
    "recommendations": [
      "ms-python.python",
      "astral-sh.ruff",
      "tamasfe.even-better-toml"
    ],
    "unwantedRecommendations": [
      "ms-azuretools.vscode-docker",
      "ms-vscode.azure-account"
    ]
  }
  ```
- **Settings (`settings.json`)**:
  ```json
  {
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.analysis.typeCheckingMode": "strict",
    "python.testing.pytestEnabled": true,
    "[python]": {
      "editor.defaultFormatter": "astral-sh.ruff",
      "editor.formatOnSave": true,
      "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
      }
    },
    "files.exclude": {
      "**/__pycache__": true,
      "**/*.pyc": true
    }
  }
  ```