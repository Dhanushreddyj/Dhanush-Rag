# Enterprise AI Platform — Controlled Cline Prompt Registry

**Status:** CL-001 `ARCHITECT_APPROVED` — EXECUTION AUTHORIZED
**Version:** 1.0
**Last Updated:** 2026-08-07
**Implementation State:** EXECUTION AUTHORIZED — CL-001 is the ONLY EXECUTABLE CLINE PROMPT

## 1. Purpose

This document controls implementation prompts sent to Cline/local Qwen. It prevents broad AI-generated rewrites and ensures each prompt references current architecture, scope, tests, and review expectations.

Prompt text is generated just-in-time after preceding task review. We intentionally do **not** pre-generate the entire project because later prompts must reflect the actual reviewed code state.

## 2. Prompt Lifecycle

`DRAFT -> ARCHITECT_APPROVED -> EXECUTED -> REVIEW -> ACCEPTED/REWORK`

Only prompts explicitly marked `ARCHITECT_APPROVED` are executable. All other prompts/tasks remain blocked until their dependency review is accepted.

## 3. Mandatory Prompt Header

Every implementation prompt states:

- task ID and single logical objective;
- architecture is already approved and must not be redesigned;
- required governance documents/ADRs;
- explicitly allowed files;
- prohibited files/changes;
- acceptance criteria;
- required tests/commands;
- completion report requirements;
- instruction to stop/report blockers rather than broaden scope.

## 4. Prompt Registry

| Prompt | Task | Status | Notes |
| --- | --- | --- | --- |
| CL-001 | FND-001 Configuration/startup validation | ARCHITECT_APPROVED | ONLY EXECUTABLE CLINE PROMPT; EXECUTION AUTHORIZED |
| CL-002+ | subsequent tasks | NOT GENERATED | generate only after preceding diff/review |

## 5. CL-001 — FND-001 Configuration/Startup Validation

**Status: `ARCHITECT_APPROVED` — EXECUTION AUTHORIZED — EXECUTE FND-001 ONLY**

```text
You are implementing FND-001 for the Enterprise AI Platform for Real Estate.

ROLE

You are the scoped implementation engineer (Cline/local Qwen).
Architecture is already approved. Do not redesign, simplify, or replace it.

READ FIRST

- docs/MASTER_CONTEXT.md
- docs/PROJECT_VISION.md
- docs/ARCHITECTURE.md
- docs/CODE_STYLE.md
- docs/CONTRIBUTING.md
- docs/TESTING.md
- docs/SECURITY.md
- docs/ADR/ADR-001-qdrant-only-vector-store.md
- docs/ADR/ADR-002-provider-pattern-single-active-provider.md
- docs/ADR/ADR-005-development-production-provider-strategy.md

TASK

Implement only the configuration/startup validation boundary.

CURRENT EVIDENCE

The audited/live baseline has app.main importing validate_settings from
app.config while app.config does not currently define validate_settings.

Do not fix other audited defects inside this task.

ALLOWED FILES

- app/config.py
- tests/test_config.py

Do not modify any other file without stopping and reporting the blocker.

ARCHITECTURE CONSTRAINTS

- CPython 3.14.7 only / Pydantic settings.
- Provider selection is configuration/composition-owned.
- Development LLM is local Qwen 3.6 through LM Studio's OpenAI-compatible
  endpoint.
- Production LLM uses AWS Bedrock models.
- Production embeddings use AWS Bedrock Embedding Models.
- Development embeddings remain configuration-driven; do not invent a
  permanent vendor/model.
- Qdrant is the sole V1 vector database.
- Chroma is not an approved runtime path, but broad Chroma dependency/provider
  removal belongs to FND-005. Do not edit unrelated files here.
- Never hard-code LAN IPs/ports, API keys, credentials, or production model IDs.
- Configuration must not instantiate provider/Qdrant/AWS clients.

REQUIREMENTS

1. Add a real validate_settings() boundary required by startup.
2. Validation must fail fast with clear, typed/safe configuration errors.
3. Validate numeric/range invariants that belong to configuration (for example
   positive/top-k/chunk/dimension settings and overlap relationships where
   applicable to existing settings).
4. Validate required provider-selection/configuration presence without making
   network calls.
5. Preserve provider neutrality and external configuration.
6. Do not add business logic, provider initialization, retrieval logic, or
   HTTP behavior to app/config.py.
7. Do not silently repair invalid settings.
8. Do not select any technology currently DEFERRED by ADR.

TESTS

Create/update tests/test_config.py covering at minimum:

- valid development configuration validation;
- invalid numeric/range configuration;
- missing/invalid required provider configuration;
- Qdrant V1 vector-store requirement where owned by config;
- validate_settings() success and failure paths;
- no test requires LM Studio, Qdrant, AWS, network access, or real credentials.

Do not weaken tests to accept startup/runtime failure.

OUT OF SCOPE

- provider factory fixes;
- embedding factory naming mismatch;
- Qdrant SDK fixes;
- async RAG/ingestion fixes;
- FastAPI controller refactor;
- Chroma package/provider deletion outside app/config.py;
- Bedrock implementation changes;
- README/general documentation rewrite.

DELIVERABLE

Return:

1. concise summary;
2. exact files changed;
3. behavior/invariants implemented;
4. tests added/updated;
5. exact test command(s) and result(s);
6. blockers/out-of-scope defects discovered;
7. git diff for senior-engineer review.

Stop after FND-001. Do not begin FND-002.
```

## 6. Review Rule

After Cline executes an approved prompt, the Principal Architect/Senior Engineer reviews the actual diff and test evidence. Only after that review is accepted may the next task/prompt be generated.

If the implementation changes assumptions relevant to a later task, update `TASKS.md`/future prompt scope rather than forcing the old plan onto the code.
