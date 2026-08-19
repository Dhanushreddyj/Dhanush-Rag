# Active Task

## Authorization

- Task: FND-002
- Prompt: CL-002
- Status: ARCHITECT_APPROVED
- Python: CPython 3.14.7 only

## Objective

Implement the provider-neutral and framework-neutral platform error taxonomy.

## Execution Role

Roo Code mode may generate and edit only the implementation and test code listed below. All governance documents and workspace rules are read-only.

## Allowed Files

- `app/core/__init__.py`
- `app/core/errors.py`
- `tests/test_errors.py`

## Required Design

- Use Python 3.14 `StrEnum` for `ErrorCode`.
- Define `PlatformError` as the base exception.
- Implement the complete CL-002 exception hierarchy.
- Give every exception type a unique stable code and safe default message.
- Public serialization contains only code, message, and optional approved public details.
- Preserve raw causes only through Python exception chaining.

## Prohibited Scope

Do not modify:

- `README.md`
- `docs/`
- `.clinerules/`
- `.roo/`
- `.rooignore`
- `app/main.py`
- `app/config.py`
- `app/providers/`
- `requirements.txt`
- environment files
- API handlers
- provider composition
- Qdrant integration
- Chroma paths
- async contracts

Do not:

- import FastAPI or Starlette into core errors;
- add HTTP status codes or request IDs;
- import provider SDKs;
- add dependencies;
- begin FND-003;
- stage, commit, or push.

## Verification

Run only:

- `.venv/bin/python --version`
- `.venv/bin/python -m pytest tests/test_errors.py -q`
- `.venv/bin/python -m compileall -q app/core tests/test_errors.py`
- `git diff --check`
- `git diff -- app/core/__init__.py app/core/errors.py tests/test_errors.py`

## Stop Condition

Stop after FND-002 implementation, focused tests, and evidence reporting. Never automatically begin the next task.
