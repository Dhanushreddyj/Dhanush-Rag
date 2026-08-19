# Nofeez AI Platform — Controlled Cline Prompt Registry

**Status:** ACTIVE
**Version:** 2.0
**Last Updated:** 2026-08-19
**Implementation State:** CL-001-R1 AUTHORIZED — FND-001 ONLY

## 1. Purpose

This registry controls implementation prompts sent to Cline/local models. The authoritative Nofeez requirements materially changed the V1 scope after CL-001 was prepared.

## 2. Current Authorization

CL-001 remains suspended as a historical prompt prepared before the accepted Nofeez requirements alignment.

CL-001-R1 is the only ARCHITECT_APPROVED implementation prompt. It authorizes only FND-001. CL-002 and every later prompt remain unavailable until FND-001 tests and senior-engineer review are accepted.

## 3. Prompt Lifecycle

DRAFT -> ARCHITECT_APPROVED -> EXECUTED -> REVIEW -> ACCEPTED or REWORK

Only ARCHITECT_APPROVED prompts are executable.

## 4. Registry

| Prompt | Task | Status | Notes |
| --- | --- | --- | --- |
| CL-001 | Former FND-001 prompt | SUSPENDED | Superseded by CL-001-R1 |
| CL-001-R1 | FND-001 configuration/startup validation | ARCHITECT_APPROVED | Only executable implementation prompt |
| CL-002+ | Later tasks | NOT GENERATED | Blocked until FND-001 is accepted |

## 5. Mandatory Prompt Controls

Every prompt must name one objective, allowed files, prohibited scope, governing ADRs, deterministic tests, required evidence and stop conditions. Cline must use editor-native changes rather than shell-generated source files and must stop after repeated tool or syntax failure.

## 6. Current Rule

Only CL-001-R1 may execute. It must stop after FND-001 implementation, focused testing and evidence collection. It must not commit, push or begin another task.

## 7. CL-001-R1 — FND-001 Configuration and Startup Validation

**Status:** ARCHITECT_APPROVED

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
