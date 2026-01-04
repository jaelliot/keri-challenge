# KERI Challenge Instructions & Context

This directory contains the "Context Protocol" for the KERI Programming Challenge.

## 🤖 Copilot Instructions

The primary instructions for AI assistants (GitHub Copilot, Cursor) are located in:
**[.github/copilot-instructions.md](./copilot-instructions.md)**

This file defines the Persona, Critical Constraints (Falcon, Memory, etc.), and Coding Standards.

## 📂 Detailed Instruction Modules

Specific implementation details are broken down by topic in the `instructions/` directory:

| File | Purpose |
| :--- | :--- |
| **`lazy-engineering-antipattern`** | Defines the "Happy Path" and minimal tech stack (Falcon/Memory). |
| **`api-design`** | Specifies the POST (Register) and GET (Read) contract. |
| **`authentication`** | Details the Signature Header verification logic. |
| **`persistence`** | Explains the allowed in-memory storage pattern. |
| **`testing`** | Standards for Pytest and Falcon Test Client. |
| **`validation`** | Defines the Pydantic schemas (`d`, `i`, `n`). |
| **`code-generation`** | Python style guide and typing rules. |
| **`style-canon`** | Naming conventions for KERI domain objects (`hab`, `aid`). |

## 🚀 Getting Started

1.  Read the `docs/resources/rubric.md` (The source of truth).
2.  Review `copilot-instructions.md` for the summary constraints.
3.  Implement the solution using `falcon` and `keripy`.
