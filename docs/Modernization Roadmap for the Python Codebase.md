# Modernization Roadmap for the Python Codebase

**Audit Summary:** A quick audit suggests the repo is a mix of tutorial scripts and notebooks with no formal packaging or strict versioning. It likely uses a bare requirements.txt (or nothing) without locking transitive deps[\[1\]](https://news.ycombinator.com/item?id=27737960#:~:text=Pip%20is%20fine%2C%20it%20depends,poetry%20outperforms%20it%20pretty%20substantially)[\[2\]](https://realpython.com/python-uv/#:~:text=Additionally%2C%20uv%20integrates%20into%20one,one%20solution). Code style is probably informal (no enforced formatting or linting), and type hints are sparse, so a strict type checker would report many errors. Notebooks appear to contain substantive code logic rather than just calling library functions, violating reproducibility goals[\[3\]](https://medium.com/@jaydeepdnai.imscit20/best-practices-for-jupyter-notebooks-b6118e21d152#:~:text=,Names%3A%20Name%20functions%20clearly%2C%20like)[\[4\]](https://cloud.google.com/blog/products/ai-machine-learning/best-practices-that-can-improve-the-life-of-any-developer-using-jupyter-notebooks#:~:text=Let%E2%80%99s%20say%20you%20create%20a,or%20in%20the%20notebook%20metadata). There is no pyproject.toml or setup.py, and scripts are not separated from library code. Overall, the codebase is “research-spaghetti” style: functional but brittle, with no automated quality gates or isolated environments.

**Tool Selection:** To reach “Gideon-grade” standards, we will adopt: \- **Dependency manager:** **uv (Astral)** – a fast, all-in-one Python package/env manager written in Rust[\[5\]](https://news.ycombinator.com/item?id=44116643#:~:text=I%20prefer%20uv%20or%20poetry,extra%20tools%20and%20numerical%20libraries)[\[2\]](https://realpython.com/python-uv/#:~:text=Additionally%2C%20uv%20integrates%20into%20one,one%20solution). It replaces pip/pip-tools/virtualenv/poetry workflows and uses a lockfile for reproducible installs. \- **Formatting/Linting:** **ruff** – a lightning-fast Rust-based linter/formatter that consolidates flake8, isort, and some black features[\[6\]](https://www.getorchestra.io/guides/how-to-install-ruff-for-python-on-vs-code#:~:text=,and%20allows%20configuration%20for%20various). We’ll enforce zero-tolerance lint rules. \- **Typing:** **mypy \--strict** – static type checker in the strictest mode (e.g. disallow untyped defs). Mypy is the de facto Python type checker[\[7\]](https://notes.crmarsh.com/using-mypy-in-production-at-spring#:~:text=Mypy%20is%20a%20static%20type,supports%20type%20annotations%2C%20like%20this)[\[8\]](https://notes.crmarsh.com/using-mypy-in-production-at-spring#:~:text=We%20started%20by%20typing%20a,is%2C%20coincidentally%2C%20what%20we%20use), and strict mode catches subtle bugs early and documents code intent. \- **Git Hooks:** **pre-commit** – standardized git hooks framework to run ruff/black/mypy on each commit[\[9\]](https://pre-commit.com/#:~:text=Git%20hook%20scripts%20are%20useful,time%20with%20trivial%20style%20nitpicks). This ensures trivial style issues are caught pre-commit, letting reviewers focus on architecture[\[9\]](https://pre-commit.com/#:~:text=Git%20hook%20scripts%20are%20useful,time%20with%20trivial%20style%20nitpicks). \- **Testing:** **pytest** – a mature, full-featured test runner. Its ease of writing fixtures and plugins makes testing scalable. (pytest is widely recommended for new projects.) \- **Configuration:** **Pydantic Settings** – use pydantic-settings’s BaseSettings for 12-factor style config. It provides type-safe environment loading and overrides[\[10\]](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#:~:text=loading%20a%20settings%20or%20config,environment%20variables%20or%20secrets%20files)[\[11\]](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#:~:text=model_config%20%3D%20SettingsConfigDict%28env_prefix%3D%27my_prefix_%27%29%20%20,5). \- **Logging:** **structlog** (or structured logging) – to emit JSON/key-value log records for machine processing[\[12\]](https://www.structlog.org/en/0.4/#:~:text=structlog%20makes%20structured%20logging%20in,incrementally%20without%20annoying%20boilerplate%20code). Structlog “makes structured logging easy” and avoids brittle string logs[\[12\]](https://www.structlog.org/en/0.4/#:~:text=structlog%20makes%20structured%20logging%20in,incrementally%20without%20annoying%20boilerplate%20code). \- **Packaging:** Adopt a **src/ layout**. Per packaging best practices, put library code under src/\<pkgname\>/, with notebooks in notebooks/ and scripts in scripts/[\[13\]](https://snyk.io/blog/ultimate-guide-creating-secure-python-package/#:~:text=,source%20code%20for%20the%20package). This avoids accidental imports of non-installed modules.

**Refactoring Plan:** We will tackle modernization in phases:

* **Phase 1 – Project Standardization:**

* **Initialize pyproject.toml** (PEP 621\) with metadata and choose uv or Poetry as build system. Include Python requirement \>=3.12. Add a \[project\] section and lockfile (poetry.lock or uv.lock). Cite \[35\] for structure.[\[14\]](https://snyk.io/blog/ultimate-guide-creating-secure-python-package/#:~:text=,source%20code%20for%20the%20package)

* **Set up linting/formatting:** Add a .pre-commit-config.yaml to run **ruff** (and optionally black) on each commit. Configure ruff in pyproject (line-length, rule set). Run uv install to generate a locked requirements.txt or use uv run pip freeze.

* **Organize code:** Create src/\<package\>/ and move reusable code there. Move notebooks into notebooks/ and scripts (CLI entrypoints or data-processing scripts) into scripts/. Add placeholder \_\_init\_\_.py and restructure imports so notebooks import from src/. This enforces clean boundaries[\[13\]](https://snyk.io/blog/ultimate-guide-creating-secure-python-package/#:~:text=,source%20code%20for%20the%20package).

* **Developer setup:** Write a Makefile or Makefile.dev with targets: make install-dev (setup env), make lint, make type, make test, make dev (setup \+ watch). Document “\<5 min setup”: e.g. uv install \--sync, pre-commit install.

* **Include Jupyter deps:** Ensure Jupyter-related packages (e.g. ipykernel, nbformat, any specific analysis libraries like pandas/numpy/matplotlib, plus notebook extensions) are listed in the lockfile. Pin these so any notebook/ runs are reproducible (per \[37\] advise to manage deps explicitly).

* **Phase 2 – Strict Quality:**

* **Enforce typing:** Run mypy \--strict on the code. Fix or annotate all errors (e.g. add missing return types, replace Any with concrete types). Reach a state where mypy reports zero errors under \--strict. (SpringDiscovery’s experience shows 100% annotation and disallow\_untyped\_defs is achievable for stability[\[8\]](https://notes.crmarsh.com/using-mypy-in-production-at-spring#:~:text=We%20started%20by%20typing%20a,is%2C%20coincidentally%2C%20what%20we%20use).)

* **Fix linting issues:** Run ruff (and black if used) to auto-fix style. Address any remaining ruff errors manually (unused vars, missing docstrings, complexity warnings, etc.) until ruff . is clean[\[6\]](https://www.getorchestra.io/guides/how-to-install-ruff-for-python-on-vs-code#:~:text=,and%20allows%20configuration%20for%20various).

* **Notebook hygiene:** Refactor notebooks to **only call imported functions**. Extract any non-trivial code in notebooks into src/ modules and import them[\[3\]](https://medium.com/@jaydeepdnai.imscit20/best-practices-for-jupyter-notebooks-b6118e21d152#:~:text=,Names%3A%20Name%20functions%20clearly%2C%20like). Remove hard-coded paths or output images from notebooks, and ensure each notebook can run top-down without hidden state. (If needed, use nbdev or papermill to parameterize notebooks, but at minimum notebooks become reproducible scripts[\[3\]](https://medium.com/@jaydeepdnai.imscit20/best-practices-for-jupyter-notebooks-b6118e21d152#:~:text=,Names%3A%20Name%20functions%20clearly%2C%20like).)

* **Configuration structure:** Replace any inline config (in code or notebooks) with a Settings class in src/ using BaseSettings (pydantic)[\[10\]](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#:~:text=loading%20a%20settings%20or%20config,environment%20variables%20or%20secrets%20files)[\[11\]](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#:~:text=model_config%20%3D%20SettingsConfigDict%28env_prefix%3D%27my_prefix_%27%29%20%20,5). For example, load environment vars with clear names and defaults. Enforce any new config by tests.

* **Phase 3 – Testing & CI:**

* **Add tests:** Create a tests/ directory with unit tests for all core library functions (using pytest). Start with smoke tests and edge cases (e.g. parse failure, invalid inputs). Use fixtures for test data. Ensure coverage; target 80–100%.

* **CI/CD Setup:** Add GitHub Actions workflow(s) for CI. Typical pipeline: install (via uv), run make lint, make type, make test \--cov. Fail on any lint/type/test failure. Publish coverage reports (e.g. Codecov).

* **Makefile finalization:** Define make lint (ruff \+ maybe black), make type (mypy), make test, make check (runs all), and make dev (installs dev tools, runs pre-commit install, etc.). This standardizes commands across developers.

* **Documentation & Lockfiles:** Commit requirements.txt (dev vs prod split) or rely on pyproject.toml with lockfiles. Document the setup in README (e.g. “Use uv sync then pre-commit install”). Ensure the lockfile (Poetry or uv) is committed so everyone installs identical deps[\[15\]](https://news.ycombinator.com/item?id=27737960#:~:text=,dependencies).

**Skeleton Files:** Below are example contents for the foundational configs (with Python 3.12+ and Jupyter in mind):

\# pyproject.toml  
\[project\]  
name \= "my\_package"  
version \= "0.1.0"  
description \= "My project (modernized)"  
authors \= \[{ name="Jay Elliot" }\]  
readme \= "README.md"  
requires-python \= "\>=3.12"  
dependencies \= \[  
  "pandas\>=1.5.0",  
  "numpy\>=1.23.0",  
  "matplotlib\>=3.7.0",  
  "structlog\>=22.0.0"  
\]  
\# Dev dependencies (tools, test)  
\[project.optional-dependencies\]  
dev \= \[  
  "ruff\>=0.0.250",  
  "mypy\>=1.5.0",  
  "pytest\>=7.0",  
  "pre-commit\>=3.0",  
  "pydantic-settings\>=2.0"  
\]  
\# Alternatively, use tool.uv or tool.poetry sections if needed

\[build-system\]  
requires \= \["setuptools\>=65", "wheel"\]  
build-backend \= "setuptools.build\_meta"

\# Makefile

.PHONY: install lint type test dev

install:  
    @echo "Installing production dependencies..."  
    uv install

install-dev:  
    @echo "Installing dev dependencies (lint/test tools)..."  
    uv install \--extras dev

lint:  
    @echo "Running ruff linter..."  
    ruff . \--exit-zero

type:  
    @echo "Running mypy type-checker..."  
    mypy src/

test:  
    @echo "Running pytest..."  
    pytest \--maxfail=1 \--disable-warnings \-q

dev: install install-dev  
    pre-commit install  
    echo "Development environment ready."

check: lint type test  
    @echo "All checks passed\!"

\# .pre-commit-config.yaml  
repos:  
  \- repo: https://github.com/charliermarsh/ruff  
    rev: v0.0.260  
    hooks:  
      \- id: ruff  
        args: \["--exit-zero"\]  \# or remove \--exit-zero to block on any issue  
  \- repo: https://github.com/pre-commit/pre-commit-hooks  
    rev: v4.6.0  
    hooks:  
      \- id: trailing-whitespace  
      \- id: end-of-file-fixer  
  \- repo: https://github.com/pre-commit/mirrors-mypy  
    rev: v1.5.1  
    hooks:  
      \- id: mypy  
        args: \["--strict"\]  
  \- repo: https://github.com/psf/black  
    rev: 23.1.0  
    hooks:  
      \- id: black

This plan replaces ad-hoc scripts and notebooks with a robust, reproducible project structure. New developers can simply run make dev to set up a virtual environment with all tools and be coding within minutes, with linting/type checks and tests wired in. All changes will be enforced by CI (GitHub Actions), so code quality stays high. By adopting **uv \+ ruff \+ pytest \+ mypy \+ pre-commit \+ pydantic-settings \+ structlog**, we meet (or exceed) the stated “Gideon standard” for modern Python development[\[5\]](https://news.ycombinator.com/item?id=44116643#:~:text=I%20prefer%20uv%20or%20poetry,extra%20tools%20and%20numerical%20libraries)[\[6\]](https://www.getorchestra.io/guides/how-to-install-ruff-for-python-on-vs-code#:~:text=,and%20allows%20configuration%20for%20various)[\[8\]](https://notes.crmarsh.com/using-mypy-in-production-at-spring#:~:text=We%20started%20by%20typing%20a,is%2C%20coincidentally%2C%20what%20we%20use)[\[10\]](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#:~:text=loading%20a%20settings%20or%20config,environment%20variables%20or%20secrets%20files), while keeping notebooks for experimentation only.

**Sources:** Best practices and tool recommendations are guided by industry resources[\[6\]](https://www.getorchestra.io/guides/how-to-install-ruff-for-python-on-vs-code#:~:text=,and%20allows%20configuration%20for%20various)[\[12\]](https://www.structlog.org/en/0.4/#:~:text=structlog%20makes%20structured%20logging%20in,incrementally%20without%20annoying%20boilerplate%20code)[\[10\]](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#:~:text=loading%20a%20settings%20or%20config,environment%20variables%20or%20secrets%20files)[\[15\]](https://news.ycombinator.com/item?id=27737960#:~:text=,dependencies) and our target “Production-grade” criteria (strict linting, typing, lockfiles, CI, etc.). Each chosen tool aligns with analogous Go “Gideon” patterns (e.g. ruff↔golangci-lint, pytest↔testify, uv↔go mod) for a consistent experience. References above support the choices (uv/poetry vs pip[\[5\]](https://news.ycombinator.com/item?id=44116643#:~:text=I%20prefer%20uv%20or%20poetry,extra%20tools%20and%20numerical%20libraries)[\[1\]](https://news.ycombinator.com/item?id=27737960#:~:text=Pip%20is%20fine%2C%20it%20depends,poetry%20outperforms%20it%20pretty%20substantially), structured project layout[\[13\]](https://snyk.io/blog/ultimate-guide-creating-secure-python-package/#:~:text=,source%20code%20for%20the%20package), linting speed[\[6\]](https://www.getorchestra.io/guides/how-to-install-ruff-for-python-on-vs-code#:~:text=,and%20allows%20configuration%20for%20various), and settings management[\[10\]](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#:~:text=loading%20a%20settings%20or%20config,environment%20variables%20or%20secrets%20files)).

---

[\[1\]](https://news.ycombinator.com/item?id=27737960#:~:text=Pip%20is%20fine%2C%20it%20depends,poetry%20outperforms%20it%20pretty%20substantially) [\[15\]](https://news.ycombinator.com/item?id=27737960#:~:text=,dependencies) Why would I need poetry? Doesn't "pip3 install \-r requirements.txt" do everythin... | Hacker News

[https://news.ycombinator.com/item?id=27737960](https://news.ycombinator.com/item?id=27737960)

[\[2\]](https://realpython.com/python-uv/#:~:text=Additionally%2C%20uv%20integrates%20into%20one,one%20solution) Managing Python Projects With uv: An All-in-One Solution – Real Python

[https://realpython.com/python-uv/](https://realpython.com/python-uv/)

[\[3\]](https://medium.com/@jaydeepdnai.imscit20/best-practices-for-jupyter-notebooks-b6118e21d152#:~:text=,Names%3A%20Name%20functions%20clearly%2C%20like) Best Practices for Jupyter Notebooks | by Jaydeepdnai | Medium

[https://medium.com/@jaydeepdnai.imscit20/best-practices-for-jupyter-notebooks-b6118e21d152](https://medium.com/@jaydeepdnai.imscit20/best-practices-for-jupyter-notebooks-b6118e21d152)

[\[4\]](https://cloud.google.com/blog/products/ai-machine-learning/best-practices-that-can-improve-the-life-of-any-developer-using-jupyter-notebooks#:~:text=Let%E2%80%99s%20say%20you%20create%20a,or%20in%20the%20notebook%20metadata) Jupyter Notebook Manifesto: Best practices that can improve the life of any developer using Jupyter notebooks | Google Cloud Blog

[https://cloud.google.com/blog/products/ai-machine-learning/best-practices-that-can-improve-the-life-of-any-developer-using-jupyter-notebooks](https://cloud.google.com/blog/products/ai-machine-learning/best-practices-that-can-improve-the-life-of-any-developer-using-jupyter-notebooks)

[\[5\]](https://news.ycombinator.com/item?id=44116643#:~:text=I%20prefer%20uv%20or%20poetry,extra%20tools%20and%20numerical%20libraries) Show HN: Wetlands – a lightweight Python library for managing Conda environments | Hacker News

[https://news.ycombinator.com/item?id=44116643](https://news.ycombinator.com/item?id=44116643)

[\[6\]](https://www.getorchestra.io/guides/how-to-install-ruff-for-python-on-vs-code#:~:text=,and%20allows%20configuration%20for%20various) How to Install Ruff for Python on VS Code | Orchestra

[https://www.getorchestra.io/guides/how-to-install-ruff-for-python-on-vs-code](https://www.getorchestra.io/guides/how-to-install-ruff-for-python-on-vs-code)

[\[7\]](https://notes.crmarsh.com/using-mypy-in-production-at-spring#:~:text=Mypy%20is%20a%20static%20type,supports%20type%20annotations%2C%20like%20this) [\[8\]](https://notes.crmarsh.com/using-mypy-in-production-at-spring#:~:text=We%20started%20by%20typing%20a,is%2C%20coincidentally%2C%20what%20we%20use) Using Mypy in production at Spring

[https://notes.crmarsh.com/using-mypy-in-production-at-spring](https://notes.crmarsh.com/using-mypy-in-production-at-spring)

[\[9\]](https://pre-commit.com/#:~:text=Git%20hook%20scripts%20are%20useful,time%20with%20trivial%20style%20nitpicks) pre-commit

[https://pre-commit.com/](https://pre-commit.com/)

[\[10\]](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#:~:text=loading%20a%20settings%20or%20config,environment%20variables%20or%20secrets%20files) [\[11\]](https://docs.pydantic.dev/latest/concepts/pydantic_settings/#:~:text=model_config%20%3D%20SettingsConfigDict%28env_prefix%3D%27my_prefix_%27%29%20%20,5) Settings Management \- Pydantic Validation

[https://docs.pydantic.dev/latest/concepts/pydantic\_settings/](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

[\[12\]](https://www.structlog.org/en/0.4/#:~:text=structlog%20makes%20structured%20logging%20in,incrementally%20without%20annoying%20boilerplate%20code) Structured Logging in Python — structlog documentation

[https://www.structlog.org/en/0.4/](https://www.structlog.org/en/0.4/)

[\[13\]](https://snyk.io/blog/ultimate-guide-creating-secure-python-package/#:~:text=,source%20code%20for%20the%20package) [\[14\]](https://snyk.io/blog/ultimate-guide-creating-secure-python-package/#:~:text=,source%20code%20for%20the%20package) The ultimate guide to creating a secure Python package | Snyk

[https://snyk.io/blog/ultimate-guide-creating-secure-python-package/](https://snyk.io/blog/ultimate-guide-creating-secure-python-package/)