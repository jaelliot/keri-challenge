| Rule File | Type | Globs | Description | Version |
| :--- | :--- | :--- | :--- | :--- |
| 00-style-canon.mdc | Always | ["**/*.py", "**/*.ipynb", "pyproject.toml"] | DOs and DON'Ts: Mandatory coding rules for Python/KERI development | 1.1.0 |
| 01-project-charter.mdc | Always | ["**/*"] | Project Charter - KERI Foundation Mission, Core Values, and Architectural Manifesto | 1.0.0 |
| 02-lazy-engineering-antipattern.mdc | Always | ["**/*.py"] | The "Lazy Engineering" manifesto: Anti-over-engineering, "Humans as Services", and Python stack mandates | 1.1.0 |
| 05-system-flow.mdc | Auto | ["**/*.py"] | High-level data flow and pipeline stages (Ingestion, Processing, Transformation) | 1.0.0 |
| 10-architecture-py.mdc | Auto | ["app/**/*.py", "src/**/*.py"] | Modular Monolith architecture, domain-driven design, and core design patterns | 1.0.0 |
| 12-time-discipline.mdc | Auto | ["**/*.py"] | Time discipline: Clock abstraction, UTC enforcement, and deterministic testing | 1.0.0 |
| 15-settings.mdc | Auto | ["app/core/config/**/*.py", "app/core/config/models/*.py", "**/*settings.py"] | Standards for application configuration and settings management | 1.0.0 |
| 20-security.mdc | Auto | ["**/*.py", "**/*.tf", "**/*.hcl"] | KERI Security Standards: Cryptography, Key Management, Secret Redaction, and IAM Hardening | 1.0.0 |
| 22-api-design.mdc | Auto | ["app/api/**/*.py", "app/schemas/**/*.py"] | Standards for API design, versioning, and response structure | 1.0.0 |
| 25-authentication.mdc | Auto | ["app/modules/auth/**/*.py", "app/core/security/**/*.py"] | Standards for PASETO v4 authentication, token management, and security | 1.0.0 |
| 30-errors.mdc | Auto | ["**/*.py"] | Standardized error handling, exception hierarchy, and logging using Loguru | 1.1.0 |
| 35-resilience.mdc | Auto | ["**/*.py"] | Resilience Over Everything: Retries, circuit breakers, and timeouts using Tenacity | 1.0.0 |
| 40-validation.mdc | Auto | ["**/*.py"] | Input validation standards using Pydantic and CESR parsing | 1.0.0 |
| 45-persistence.mdc | Auto | ["app/infrastructure/persistence/**/*.py", "app/domain/**/*.py", "**/*repository.py"] | Persistence layer standards using Repository Pattern and MongoDB | 1.0.0 |
| 50-testing.mdc | Auto | ["tests/**/*.py", "**/*_test.py", "**/conftest.py"] | Testing standards and practices using Pytest | 1.0.0 |
| 55-api-contract-testing.mdc | Agent Requested | ["**/*.json", "Documentation/Usage-Docs/*.json"] | API Contract Verification with Postman and Newman | 1.0.0 |
| 65-content-processing.mdc | Auto | ["app/modules/harvester/**/*.py", "app/modules/content_processing/**/*.py"] | Standards for the Content Processing System (Harvesting, Validation, Normalization) | 1.0.0 |
| 66-content-upload.mdc | Auto | ["app/modules/upload/**/*.py", "app/api/**/upload.py", "app/modules/content_upload/**/*.py"] | Standards for the Content Upload System (Ingestion, Progress Tracking, Validation) | 1.0.0 |
| 71-task-management-polyglot.mdc | Auto | ["docs/tasks/**/*", "docs/deferred/**/*"] | Task lifecycle management: Active, Completed, Deferred, and ADR generation | 1.0.0 |
| 70-async-events.mdc | Auto | ["app/worker/**/*.py", "app/modules/**/tasks.py", "app/modules/**/events.py", "**/celery_app.py"] | Standards for event-driven architecture, Celery task queues, and asynchronous processing | 1.0.0 |
| 74-documentation-first-workflow-polyglot.mdc | Auto | ["docs/**/*", "**/*.md"] | The 5-Phase Documentation-First Development Workflow (Plan -> Doc -> Rule -> Gate -> Code) | 1.0.0 |
| 75-transformation-pipeline.mdc | Auto | ["app/modules/transformation/**/*.py", "app/modules/llm/**/*.py"] | Standards for the Data Transformation System (Pipeline, Strategy, LLM Integration) | 1.0.0 |
| 80-tooling.mdc | Agent Requested | ["Dockerfile*", "docker-compose*.yml", ".dockerignore"] | Docker usage, build standards, and container security | 1.0.0 |
| 85-vscode.mdc | Auto | [".vscode/*.json", ".vscode/README.md"] | VS Code configuration standards and selective inclusion patterns | 1.0.0 |
| 90-deployment-strategy.mdc | Auto | ["deploy/**/*.yaml", ".github/workflows/**/*.yaml", "docker-compose*.yml"] | Standards for deployment environments, parity, and release strategies | 1.0.0 |
| 95-code-generation.mdc | Always | ["**/*.py"] | KERI-compliant Python code generation, strict typing, and documentation standards | 1.1.0 |
