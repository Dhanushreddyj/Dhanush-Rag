# Nofeez AI Platform — Controlled Implementation Prompt Registry

**Status:** ACTIVE
**Version:** 2.0
**Last Updated:** 2026-08-20
**Implementation State:** CX-DEV-RAG-001 ARCHITECT_APPROVED — DEV-RAG-001 ONLY

## 1. Purpose

This tool-neutral registry controls implementation prompts. The authoritative Nofeez requirements materially changed the V1 scope after CL-001 was prepared.

The project owner and principal architect maintain this registry. Implementation tools may read it but must not edit governance documents, task status, prompt authorization, review records, ADRs, or workspace rules. An implementation tool may generate code and tests only under an already ARCHITECT_APPROVED prompt assigned to that tool.

## 2. Current Authorization

CL-001 remains suspended as a historical prompt prepared before the accepted Nofeez requirements alignment.

CL-001-R1 is ACCEPTED after successful FND-001 implementation and review.

CL-002 and CX-002 are SUPERSEDED and non-executable.

CX-DEV-RAG-001 is the only ARCHITECT_APPROVED and executable implementation prompt. It authorizes only DEV-RAG-001. Every later prompt is NOT GENERATED and remains non-executable.

## 3. Prompt Lifecycle

DRAFT -> ARCHITECT_APPROVED -> EXECUTED -> REVIEW -> ACCEPTED or REWORK

Only ARCHITECT_APPROVED prompts are executable.

## 4. Registry

| Prompt | Task | Status | Notes |
| --- | --- | --- | --- |
| CL-001 | Former FND-001 prompt | SUSPENDED | Superseded by CL-001-R1 |
| CL-001-R1 | FND-001 configuration/startup validation | ACCEPTED | Implemented and accepted through PR #7 |
| CL-002 | FND-002 platform error taxonomy | SUPERSEDED | Non-executable; implementation ownership moved to Codex |
| CX-002 | FND-002 platform error taxonomy | SUPERSEDED | Non-executable; replaced by the owner-prioritized vertical-slice sequence |
| CX-DEV-RAG-001 | DEV-RAG-001 working development RAG vertical slice | ARCHITECT_APPROVED | Only executable implementation prompt |
| All later prompts | Later tasks and improvements | NOT GENERATED | Gated until DEV-RAG-001 evidence is reviewed |

## 5. Mandatory Prompt Controls

Every prompt must name one objective, allowed files, prohibited scope, governing ADRs, deterministic tests, required evidence and stop conditions. The assigned implementation tool must use editor-native changes rather than shell-generated source files and must stop after repeated tool or syntax failure.

Implementation prompts authorize code and test generation only. They never authorize the implementation tool to edit this registry, other governance documents, ADRs, review records, or workspace rules.

## 6. Current Rule

Only CX-DEV-RAG-001 may execute. It authorizes Codex to implement only DEV-RAG-001 and requires a stop after implementation, offline verification, and an explicitly owner-authorized live gate or exact live-gate blocker. Codex must not stage, commit, push, merge, or begin later improvements.

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

## 8. CX-002 — FND-002 Platform Error Taxonomy

**Status:** SUPERSEDED — NON-EXECUTABLE

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

Stop after FND-002 evidence. Codex must not stage, commit, push, or begin FND-003.

## 9. CX-DEV-RAG-001 — Working Development RAG Vertical Slice

**Status:** ARCHITECT_APPROVED

### Sequencing Authority

The owner authorizes Codex to complete the repairs necessary for one working development RAG vertical slice before later code improvements. This is an explicit sequencing exception. It does not redesign or simplify the approved architecture, authorize completion claims for the enterprise backlog, or establish production readiness.

DEV-RAG-001 is the only READY implementation task. FND-002 through FND-009 remain PLANNED and are not independently executable while it is active. Their applicable runtime-foundation requirements may be satisfied and mapped during DEV-RAG-001 review, but none may be marked DONE before evidence review.

### Objective

Deliver this verified development flow:

1. Import and start the FastAPI application under CPython 3.14.7.
2. Load typed configuration from the supported environment source.
3. Compose exactly one development LLM adapter, one development embedding adapter, and Qdrant.
4. Load a safe synthetic Markdown or text test document.
5. Split it using application-owned code.
6. Generate document embeddings through an OpenAI-compatible development adapter.
7. Create or validate an isolated Qdrant collection with the matching dimension.
8. Store vectors and provider-neutral payloads.
9. Embed a query.
10. Retrieve relevant chunks.
11. Build grounded context.
12. Generate an answer through LM Studio.
13. Return a validated FastAPI response containing safe source information.
14. Return safe platform errors without raw exception leakage.

### Allowed Implementation Paths

- `app/**`
- `tests/**`
- `scripts/**`
- `.env.example`
- `requirements.txt`
- `requirements-dev.txt`

No other path may be created or modified during implementation.

### Prohibited Paths

Do not modify:

- `AGENTS.md` during implementation;
- `README.md` or `docs/**`;
- `.clinerules/**`;
- `.roo/**`;
- `.rooignore`;
- `.env` or any secret file;
- `knowledge/canonical/**`;
- existing canonical source material;
- unrelated repository files.

### Required Implementation Constraints

- Use CPython 3.14.7 strictly.
- FastAPI remains the delivery framework.
- Qdrant is the only vector store.
- Support Qdrant Cloud and self-hosted Qdrant configuration.
- Use direct approved SDK or protocol clients.
- Remove all Chroma runtime paths.
- Remove all LangChain runtime imports and assumptions.
- Do not add LangChain packages.
- LangGraph remains orchestration-only and need not be introduced merely to prove the development vertical slice.
- Provider selection remains configuration-driven.
- Exactly one provider implementation is active per capability.
- Business logic must not depend on provider SDK types.
- Use async contracts consistently and await every coroutine.
- Prompt construction must not be owned by the provider adapter.
- Qdrant must receive actual vectors, not natural-language text as a point query.
- Qdrant collection dimension must match the active embedding model.
- Use valid SDK vector, payload, filter, point, and response models.
- Disable application answer caching unless a safe complete cache identity is implemented and tested.
- API routes must not expose `str(exception)`, credentials, SDK responses, tracebacks, or internal paths.
- Do not accept HTTP 500 as test success.
- Do not claim production readiness.
- Do not implement the complete authorization, canonical-corpus, reranking, agent-tool, streaming, production telemetry, or Bedrock-live scope.

### Offline Test Policy

Default tests must:

- be deterministic;
- be network-isolated;
- use fakes or mocks for LM Studio and external Qdrant;
- test startup, configuration, provider composition, embeddings, Qdrant mapping, ingestion, retrieval, grounded generation, safe errors, and API responses;
- run under CPython 3.14.7; and
- leave existing external services untouched.

Offline verification must include:

- `.venv/bin/python --version`;
- `.venv/bin/python -m pytest -q`;
- `.venv/bin/python -m compileall -q app tests scripts`;
- `git diff --check`;
- `git status --short --untracked-files=all`; and
- a complete diff limited to the allowed implementation paths.

The Python version must be exactly 3.14.7. If a required package is unavailable, follow the dependency boundary below rather than installing it automatically.

### Owner-Authorized Live Development Gate

The final live development gate may run only after offline tests pass and the owner explicitly authorizes that execution.

The live gate may:

- contact only the configured LM Studio endpoint;
- contact only the configured Qdrant endpoint;
- use existing configured credentials without printing, copying, or documenting them;
- discover configured model identifiers without exposing tokens;
- create one uniquely named development collection;
- ingest only a safe synthetic test document; and
- perform one retrieval and grounded-answer query.

The live gate must not:

- contact AWS Bedrock;
- use production customer or transactional data;
- import the 110-file canonical corpus;
- modify or delete an existing Qdrant collection;
- reset Qdrant;
- overwrite existing vectors;
- expose credentials; or
- claim success unless the real response is verified.

Leave the unique live-gate collection in place and report its name. Deletion requires separate owner approval.

If LM Studio does not expose a usable embedding model, Qdrant credentials are unavailable, the configured embedding dimension is incompatible, or a live service cannot be reached, stop and report the exact blocker. Never fabricate a successful live result.

### Dependency Boundary

Codex may modify `requirements.txt` or `requirements-dev.txt` only when required by the approved direct-SDK architecture. Codex must not install packages automatically. If installation is required after manifest review, stop and request explicit owner approval with the exact package and command.

### Evidence Requirements

Report:

- exact files changed;
- the implemented startup, configuration, composition, ingestion, embedding, Qdrant, retrieval, grounding, generation, API, and safe-error flow;
- mappings to any applicable FND-002 through FND-009 runtime-foundation requirements, without marking those tasks DONE;
- exact commands executed and complete results;
- CPython 3.14.7 evidence;
- complete offline test, compilation, diff-check, status, and scoped-diff evidence;
- dependency-manifest changes and any exact installation approval request;
- live-gate authorization and execution status;
- the unique Qdrant collection name if the live gate runs; and
- exact blockers and deferred scope.

Do not expose credentials, local `.env` contents, SDK responses containing private data, internal paths, or raw private data.

### Stop Condition

Stop after implementation and offline verification, then either complete an explicitly owner-authorized live gate or report its exact blocker or authorization requirement. Do not stage, commit, push, merge, delete branches, begin improvements beyond the working vertical slice, mark FND-002 through FND-009 DONE, claim production readiness, or begin another task automatically.
