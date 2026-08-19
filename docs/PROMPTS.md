# Nofeez AI Platform — Controlled Cline Prompt Registry

**Status:** ACTIVE
**Version:** 2.0
**Last Updated:** 2026-08-20
**Implementation State:** CL-002 ARCHITECT_APPROVED — FND-002 ONLY

## 1. Purpose

This registry controls implementation prompts sent to Cline/local models. The authoritative Nofeez requirements materially changed the V1 scope after CL-001 was prepared.

The project owner and principal architect maintain this registry. Cline may read it but must not edit governance documents, task status, prompt authorization, review records, ADRs, or workspace rules. Cline is used only for implementation and test-code generation under an already ARCHITECT_APPROVED prompt.

## 2. Current Authorization

CL-001 remains suspended as a historical prompt prepared before the accepted Nofeez requirements alignment.

CL-001-R1 is ACCEPTED after successful FND-001 implementation and review.

CL-002 is the only ARCHITECT_APPROVED and executable implementation prompt. It authorizes only FND-002. CL-003 and every later prompt are NOT GENERATED and remain non-executable.

## 3. Prompt Lifecycle

DRAFT -> ARCHITECT_APPROVED -> EXECUTED -> REVIEW -> ACCEPTED or REWORK

Only ARCHITECT_APPROVED prompts are executable.

## 4. Registry

| Prompt | Task | Status | Notes |
| --- | --- | --- | --- |
| CL-001 | Former FND-001 prompt | SUSPENDED | Superseded by CL-001-R1 |
| CL-001-R1 | FND-001 configuration/startup validation | ACCEPTED | Implemented and accepted through PR #7 |
| CL-002 | FND-002 platform error taxonomy | ARCHITECT_APPROVED | Only executable implementation prompt |
| CL-003+ | Later tasks | NOT GENERATED | Blocked until FND-002 is accepted |

## 5. Mandatory Prompt Controls

Every prompt must name one objective, allowed files, prohibited scope, governing ADRs, deterministic tests, required evidence and stop conditions. Cline must use editor-native changes rather than shell-generated source files and must stop after repeated tool or syntax failure.

Cline prompts authorize code and test generation only. They never authorize Cline to edit this registry, other governance documents, ADRs, review records, or workspace rules.

## 6. Current Rule

Only CL-002 may execute. It authorizes only FND-002 and must stop after implementation, focused testing and evidence collection. It must not commit, push or begin FND-003.

## 7. CL-001-R1 — FND-001 Configuration and Startup Validation

**Status:** ACCEPTED

### Objective

Implement deterministic, provider-aware configuration validation at the application startup boundary without network calls or SDK-client creation.

### Allowed Files

- `app/config.py`
- `tests/test_config.py`

`app/main.py` already invokes `validate_settings()` from the FastAPI lifespan and must not be modified.

### Required Behavior

Add this public function to `app/config.py`:

`def validate_settings(candidate: Settings | None = None) -> None`

When `candidate` is `None`, validate the module-level `settings` instance.

Validate these invariants:

- `TOP_K > 0`;
- `MAX_CHUNK_SIZE > 0`;
- `0 <= CHUNK_OVERLAP < MAX_CHUNK_SIZE`;
- `EMBEDDING_DIMENSION > 0`;
- `MIN_QUERY_LENGTH > 0`;
- `MAX_QUERY_LENGTH > 0`;
- `MIN_QUERY_LENGTH <= MAX_QUERY_LENGTH`;
- `MAX_CONTEXT_DOCS > 0`;
- `RATE_LIMIT_PER_MINUTE > 0`;
- `RATE_LIMIT_WINDOW_SECONDS > 0`;
- `CACHE_TTL_SECONDS > 0`;
- `MAX_CACHE_SIZE > 0`;
- `ENV`, `LLM_PROVIDER` and `EMBEDDING_PROVIDER` are non-empty strings;
- `VECTOR_STORE_PROVIDER` is exactly `qdrant`;
- `QDRANT_COLLECTION_NAME` is a non-empty string;
- when `QDRANT_URL` is absent or blank, `QDRANT_HOST` is a non-empty string;
- when `LLM_PROVIDER` is `openai_compatible`, `OPENAI_BASE_URL` and `OPENAI_MODEL` are non-empty strings;
- when `EMBEDDING_PROVIDER` is `openai_compatible`, `OPENAI_BASE_URL` and `EMBEDDING_MODEL` are non-empty strings.

Raise `ValueError` with a clear setting-specific message for every failed invariant.

Validation must not:

- make network calls;
- instantiate provider or SDK clients;
- access Qdrant;
- contact LM Studio or Bedrock;
- read or write application data;
- mutate the supplied Settings instance.

### Tests

Create `tests/test_config.py`.

Use focused pytest tests and parameterization. Use no more than 12 test functions.

Cover:

- a valid development configuration;
- the module-level wrapper;
- all numeric and range invariants;
- query-length ordering;
- blank provider/environment values;
- rejection of Chroma and every non-Qdrant vector-store value;
- Qdrant collection and connection-field requirements;
- OpenAI-compatible LLM and embedding requirements;
- absence of network calls;
- clear ValueError messages.

Tests must use dummy local values and require no real credentials, Qdrant connection, LM Studio connection or Bedrock access.

### Prohibited Scope

Do not:

- modify `app/main.py`;
- modify requirements or environment files;
- remove legacy Chroma fields in this task;
- add provider adapters;
- add dependencies;
- redesign Settings;
- change API routes;
- perform unrelated cleanup or formatting;
- create shell-generated source files;
- commit or push;
- begin FND-002.

### Required Verification

Run:

- `.venv/bin/python --version`;
- `.venv/bin/python -m pytest tests/test_config.py -q`;
- `.venv/bin/python -m compileall -q app tests/test_config.py`;
- `git diff --check`;
- `git diff -- app/config.py tests/test_config.py`.

The Python version must be exactly 3.14.7.

If pytest is unavailable, a required field does not exist, an allowed file has conflicting user changes, or completion requires another file, stop and report the blocker. Do not install dependencies or expand scope.

### Completion Evidence

Report:

- exact files changed;
- validation rules implemented;
- exact commands executed;
- complete test results;
- diff scope;
- remaining blockers.

Stop after FND-001 evidence. Do not start another task.

## 8. CL-002 — FND-002 Platform Error Taxonomy

**Status:** ARCHITECT_APPROVED

### Objective

Implement the provider-neutral and framework-neutral platform error taxonomy without adding transport, provider-SDK, or runtime-integration behavior.

### Allowed Files

- `app/core/__init__.py`
- `app/core/errors.py`
- `tests/test_errors.py`

No other file may be created or modified.

### Required Hierarchy

- `PlatformError`
  - `ApplicationValidationError`
  - `ConfigurationError`
  - `ResourceNotFoundError`
  - `ProviderError`
    - `ProviderUnavailableError`
    - `ProviderTimeoutError`
  - `EmbeddingError`
  - `VectorStoreError`
  - `RetrievalError`
  - `IngestionError`
    - `UnsupportedDocumentError`
  - `SessionError`
  - `ToolError`
  - `OrchestrationError`
  - `InternalPlatformError`

### Required Design

- Use Python 3.14 `StrEnum` for `ErrorCode`.
- Give every exception type, including the base `PlatformError`, a unique stable provider-neutral code and a safe default message.
- Use this public constructor contract consistently: `message: str | None = None` and keyword-only `public_details: Mapping[str, object] | None = None`.
- Treat a caller-supplied message and public details as explicitly approved for public exposure; copy the supplied details so later caller mutation cannot change stored error state.
- Provide `to_public_dict()` returning only `code`, `message`, and optional `details` when public details were supplied.
- Re-export `ErrorCode` and the complete exception hierarchy from `app/core/__init__.py`.
- Keep the taxonomy framework-neutral and provider-neutral.
- Preserve raw causes only through normal Python exception chaining with `raise ... from cause`.
- Never serialize raw exceptions, chained causes, credentials, provider SDK responses, internal paths, tracebacks, or private content.
- HTTP status codes, request IDs, logging, and API error-envelope integration belong to later boundary tasks and must not be added here.

### Stable Error Codes

Define these `ErrorCode` members and string values exactly:

- `PLATFORM_ERROR = "PLATFORM_ERROR"`
- `APPLICATION_VALIDATION_ERROR = "APPLICATION_VALIDATION_ERROR"`
- `CONFIGURATION_ERROR = "CONFIGURATION_ERROR"`
- `RESOURCE_NOT_FOUND_ERROR = "RESOURCE_NOT_FOUND_ERROR"`
- `PROVIDER_ERROR = "PROVIDER_ERROR"`
- `PROVIDER_UNAVAILABLE_ERROR = "PROVIDER_UNAVAILABLE_ERROR"`
- `PROVIDER_TIMEOUT_ERROR = "PROVIDER_TIMEOUT_ERROR"`
- `EMBEDDING_ERROR = "EMBEDDING_ERROR"`
- `VECTOR_STORE_ERROR = "VECTOR_STORE_ERROR"`
- `RETRIEVAL_ERROR = "RETRIEVAL_ERROR"`
- `INGESTION_ERROR = "INGESTION_ERROR"`
- `UNSUPPORTED_DOCUMENT_ERROR = "UNSUPPORTED_DOCUMENT_ERROR"`
- `SESSION_ERROR = "SESSION_ERROR"`
- `TOOL_ERROR = "TOOL_ERROR"`
- `ORCHESTRATION_ERROR = "ORCHESTRATION_ERROR"`
- `INTERNAL_PLATFORM_ERROR = "INTERNAL_PLATFORM_ERROR"`

### Safe Default Messages

Default messages must describe the category without exposing implementation details. Tests must assert the exact defaults chosen in `app/core/errors.py` so accidental public-contract changes are detected.

### Tests

Create focused deterministic tests in `tests/test_errors.py`. Use parameterization where appropriate and no more than nine test functions.

Cover:

- the complete inheritance hierarchy;
- Python 3.14 `StrEnum` behavior and the exact stable values;
- uniqueness of all error codes;
- safe non-empty default messages;
- caller-approved message overrides;
- defensive copying and optional inclusion of public details;
- the exact public serialization shape;
- explicit re-exports from `app.core`;
- exception chaining while confirming that sensitive raw cause content never appears in public serialization.

Tests must require no credentials, provider SDKs, network access, Qdrant, LM Studio, or Bedrock.

### Prohibited Scope

Do not:

- import FastAPI or Starlette;
- add HTTP status codes or request IDs;
- import provider SDKs;
- modify `app/main.py` or `app/config.py`;
- modify provider, vector-store, retrieval, ingestion, API, or orchestration implementations;
- integrate exception handlers, logging, or transport error envelopes;
- change dependencies or environment files;
- fix async behavior;
- remove legacy Chroma paths;
- perform unrelated cleanup or formatting;
- modify governance documents or workspace rules;
- commit or push;
- begin FND-003.

### Required Verification

Run:

- `.venv/bin/python --version`;
- `.venv/bin/python -m pytest tests/test_errors.py -q`;
- `.venv/bin/python -m compileall -q app/core tests/test_errors.py`;
- `git diff --check`;
- `git diff -- app/core/__init__.py app/core/errors.py tests/test_errors.py`.

The Python version must be exactly 3.14.7.

If pytest is unavailable, an allowed file contains conflicting owner changes, a required design conflicts with the accepted architecture, or completion requires another file, stop and report the blocker. Do not install dependencies or expand scope.

### Completion Evidence

Report:

- exact files changed;
- hierarchy and stable codes implemented;
- public serialization contract;
- exact commands executed;
- complete focused-test results;
- compilation and diff-check results;
- remaining blockers or deferred issues.

Stop after FND-002 evidence. Do not stage, commit, push, or begin FND-003.
