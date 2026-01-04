---
applyTo: "docs/tasks/**/*,docs/deferred/**/*"
# Task management workflow for KERI implementation
---
# Task Management Instructions

This document outlines the workflow for managing tasks in the KERI project.

## Overview

We use a structured approach to task management that enforces a lifecycle:
1. **Creation**: Tasks are created in `docs/tasks/active/` with a standardized structure.
2. **Execution**: Work is performed, and the task folder serves as a scratchpad.
3. **Completion**: Tasks are moved to `docs/tasks/completed/` and an ADR is created if architectural decisions were made.
4. **Deferral**: Future tasks go in `docs/deferred/` organized by category.

## Directory Structure

```
docs/
├── tasks/
│   ├── active/              # Currently being worked on
│   │   └── YYYY-MM-DD_task-name/
│   │       └── IMPLEMENTATION-PLAN.md
│   └── completed/           # Finished tasks
│       └── YYYY-MM-DD_task-name/
└── deferred/                # Future work, not ready yet
    ├── features/
    ├── infrastructure/
    ├── quality-assurance/
    ├── research/
    ├── security/
    └── cost-optimization/
```

## Workflow

### 1. Creating a New Task

Create a directory in `docs/tasks/active/` with the current date and task name.

```bash
mkdir -p docs/tasks/active/$(date +%F)_my-feature-name
touch docs/tasks/active/$(date +%F)_my-feature-name/IMPLEMENTATION-PLAN.md
```

**Action Required:**
- Fill out the `IMPLEMENTATION-PLAN.md` with objectives and implementation steps.

### 2. Working on a Task

The task directory is your workspace for documentation, notes, and scratch files related to the feature.

- Keep all relevant non-code artifacts in this directory.
- Use `todo_write` tool to track progress within the session.

### 3. Completing a Task

When the task is finished, move the task directory to `docs/tasks/completed/`.

```bash
mv docs/tasks/active/YYYY-MM-DD_my-feature-name docs/tasks/completed/
```

**ADR Requirement:**
If the task involved a significant architectural decision (e.g., choosing a new library, defining a new protocol interaction), create a new ADR in `docs/adr/`.

## Rules

1.  **No Orphaned Tasks**: Every significant feature or refactor MUST start with a task.
2.  **Archive on Completion**: Never manually delete a task folder; always archive it to preserve history.
3.  **ADR Requirement**: Significant changes require an ADR.
4.  **Extension Over Creation**: Prefer extending existing `src/keri/` packages over creating new modules.