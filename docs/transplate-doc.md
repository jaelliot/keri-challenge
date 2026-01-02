# 🐍 PROMPT: Code Implementation — Transplant Legacy Python Rules to `.cursor/rules`

> 🛠️ **Purpose**: Move **exactly one** legacy rule snippet (e.g., from `old_guidelines.md` or a legacy `cursorrules.yml`) into a new **Python-focused** `.mdc` ruleset under `.cursor/rules/`. If no suitable target exists, create a new `.mdc` and update the index. Remove the migrated snippet from the source.
> 📍 Context: **Python Monorepo** (Library + Scripts + Notebooks)
> 🎯 Targets: `.cursor/rules/*.mdc` and `.cursor/rules/RULES_INDEX.md`
> 🧭 Scope: **Python-only** (e.g., `pyproject.toml` tooling, `pydantic`, `pytest`)

---

## 🧪 IMPLEMENTATION PROMPT

### **⚠️ CRITICAL INSTRUCTION**

This is an **action-oriented implementation task**. Migrate **one** snippet per run. **Deduplicate** but **preserve helpful nuance** via a concise "Notes / Examples" section.

**1) Plan & Structure**
*   **1a. Identify** the snippet by its header or delimiter.
*   **1b. Route** to the correct target using the **Routing Matrix (Python)** below.
*   **1c. Transform** into concise, imperative bullets (Do/Don't) but **retain non-redundant nuance** under **Notes / Examples**.
*   **1d. Create** a new `.mdc` if needed (pick `NN` gap and proper `globs`), then **update `RULES_INDEX.md`**.

**2) Review & Amend Rules**
*   **Scan for overlap** in existing `.mdc` files.
*   **Universal Rules:** If a rule applies to *all* Python code (e.g., "Always use `ruff`"), place it in `00-style-canon.mdc`.
*   **Conflict Resolution:** If legacy rules conflict with modern standards (e.g., `pylint` vs `ruff`), **discard the legacy rule** in favor of the modern standard, noting the decision.

**3) Implement (Docs Edits)**
*   Extract → Transform → Write to target `.mdc`.
*   **Remove** the migrated block from the source file.
*   If a **new** `.mdc` is added, **append** a row in `RULES_INDEX.md`.

---

### 🏷️ TASK: Transplant `[SNIPPET_TITLE]`

**You must process exactly one snippet**: `[SNIPPET_TITLE]`.

---

### 🛠️ Implementation Requirements

#### Step 1: Route to the Correct `.mdc` (Python)

**Routing Matrix**

| Destination `.mdc` | Choose when (keywords/themes) | Rule Type | Default Globs |
| :--- | :--- | :--- | :--- |
| `00-style-canon.mdc` | Universal invariants (`ruff`, `mypy`), project-wide norms (`uv`) | **Always** | `["**/*.py", "**/*.ipynb"]` |
| `10-architecture-py.mdc` | Package structure, `src` layout, imports, dependency injection | Auto Attached | `["src/**/*.py", "pyproject.toml"]` |
| `20-security.mdc` | Secrets, PII redaction, input validation (`pydantic`), serialization | Auto Attached | `["**/*.py"]` |
| `30-errors.mdc` | Exception hierarchy, logging (`structlog`), error wrapping | Auto Attached | `["**/*.py"]` |
| `40-validation.mdc` | `Pydantic` models, argument validation, type guards | Auto Attached | `["src/**/*.py"]` |
| `50-testing.mdc` | `pytest` fixtures, coverage, mocking, notebooks-as-tests | Auto Attached | `["tests/**/*.py", "**/*_test.py"]` |
| `60-notebooks.mdc` | Jupyter hygiene, "no hidden state", clearing outputs | Auto Attached | `["**/*.ipynb"]` |
| `80-tooling.mdc` | `uv`, `pre-commit`, `make`, Docker builds | Agent Requested | n/a |
| **NEW:** `NN-topic.mdc` | If none fit (e.g., `65-data-pipelines.mdc`, `75-ml-models.mdc`) | Auto/Agent | Choose specific globs |

---

#### Step 2: Transform & Write

**Target:** `.cursor/rules/[TARGET_FILE].mdc`
**Goal:** Convert the snippet into concise rules while preserving **useful nuance**.

**Nuance Preservation Rules (Python Specifics)**
1.  **Do / Don't** lists must be tight.
2.  **Notes / Examples** should capture specific library usage or patterns.
    *   *Example:* `pydantic` usage: "Use `Field(..., description="...")` for API models."
    *   *Example:* `pytest` usage: "Prefer `tmp_path` fixture over manual `tempfile`."
    *   *Example:* Type hints: "Use `beartype` or `typeguard` for runtime checking if needed."

**MDC Template:**
```markdown
---
description: [One-line purpose distilled from SNIPPET title]
globs: [OPTIONAL: "**/*.py", "tests/**/*.py"]
alwaysApply: [true|false]
---

## Use when
- [Files/situations this applies to]

## Do
- [Imperative bullet(s) extracted & normalized]
- [Example: Use `uv run` for deterministic execution]

## Don't
- [Anti-patterns converted from prohibitions]
- [Example: Don't use `os.environ` directly; use `pydantic-settings`]

## Notes / Examples
- [Concise rationale or examples]
- [Example: `class Config(BaseSettings): ...`]
```

---

#### Step 3: Update `RULES_INDEX.md` (if new file)

**File:** `.cursor/rules/RULES_INDEX.md`
**Action:** Append a row:
```markdown
| NN-topic.mdc | [Always|Auto|Agent] | [globs] | [One-line purpose] | 1.0.0 |
```

---

#### Step 4: Remove Migrated Block

**Action:** Delete the extracted snippet from the source file to prevent double-migration.

---

### ✅ Verification Steps

1.  [ ] Front-matter YAML valid; **Python-only** globs.
2.  [ ] Cursor Agent shows rule under intended type.
3.  [ ] No duplicate bullets in destination `.mdc`.
4.  [ ] Source file no longer contains the transplanted block.
5.  [ ] Update changelog.