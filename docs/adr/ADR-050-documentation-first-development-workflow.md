<!-- Copyright (c) Vaidya Solutions -->
<!-- SPDX-License-Identifier: BSD-3-Clause -->

# ADR-050: Documentation-First Development Workflow

**Status**: Accepted  
**Date**: 2026-01-01  
**Deciders**: Architecture Team  
**Related**: ADR-047 (Unified Documentation Structure)

---

## Context

As a solo developer building a production-grade KERI implementation with SOC 2 requirements, traditional "code-first" development creates:
1. **Inconsistent architecture**: Code diverges from design.
2. **Cognitive overload**: Holding the entire system in head.
3. **Documentation drift**: Docs become stale.

**The Gap**: Need a systematic workflow that ensures documentation leads development.

---

## Decision

We adopt a **5-phase documentation-first development workflow** for all architectural changes and new features:

### Phase 1: Architecture Planning
- Research technical approaches.
- Create architectural diagrams.
- Write decision record (ADR).

### Phase 2: Documentation Update
- Update `docs/` to describe **target state**.
- Add migration status documents if current code differs.
- Include code examples showing target patterns.

### Phase 3: Instructions Update
- Update `.github/instructions/*.instructions.md`.
- Ensure glob patterns match affected files.
- Document anti-patterns.

### Phase 4: Quality Gates Update
- Add linter rules (e.g., `flake8-forbidigo` equivalent).
- Create architecture tests (e.g., enforcing import boundaries).

### Phase 5: Code Update
- Implement code following patterns.
- Run quality gates continuously.

---

## Rationale

1. **Solo Developer Sustainability**: Documentation serves as external memory.
2. **Quality Assurance**: Quality gates enforce documented patterns.
3. **Audit Readiness**: Documentation exists before code (SOC 2 requirement).

---

## Consequences

### Positive
✅ **Architectural consistency**  
✅ **Reduced cognitive load**  
✅ **Regression prevention**

### Negative
❌ **Upfront time investment**

---

## Implementation Guidance

**Always use for**:
- Architectural changes.
- New features spanning multiple modules.
- Security-sensitive changes.

**Can skip for**:
- Bug fixes.
- Typo corrections.
