---
applyTo: "docs/**/*,**/*.md"
# Documentation-First Development Workflow: 5-Phase Process
---

# Documentation-First Development Workflow

## Core Principle

**Document target state first, then update rules, then quality gates, then code.**

## 5-Phase Workflow

### Phase 1: Architecture Planning
- Research technical approaches.
- Create architectural diagrams.
- Write ADR if significant.

### Phase 2: Documentation Update
- **Document the TARGET state.**
- Add warnings if current code differs ("⚠️ TARGET ARCHITECTURE").
- Create `MIGRATION-STATUS.md` if needed.

### Phase 3: Rules Update
- Update `.cursor/rules/*.mdc`.
- Update `RULES_INDEX.md`.
- Document anti-patterns.

### Phase 4: Quality Gates Update
- Add linter rules (e.g., forbidding imports).
- Add architecture tests.

### Phase 5: Code Update
- Implement code following patterns.
- Fix violations immediately.

## When to Use

### Always Use For
✅ Architectural changes  
✅ New features spanning multiple files  
✅ Security-sensitive changes  

### Can Skip For
⚠️ Bug fixes  
⚠️ Typo corrections