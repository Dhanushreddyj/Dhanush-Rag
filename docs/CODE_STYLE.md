# Enterprise AI Platform — Code Style Standard

**Status:** ACCEPTED  
**Version:** 1.0  
**Last Updated:** 2026-08-07  
**Applies To:** Python application code, tests, scripts, and implementation-focused examples

## 1. Purpose and Authority

This document defines how Python code is written so architectural boundaries remain visible in the code itself. It operationalizes `MASTER_CONTEXT.md`, `PROJECT_VISION.md`, `ARCHITECTURE.md`, and accepted ADRs; it may not silently override them.

If a style preference conflicts with architecture, correctness, security, or an accepted ADR, the higher-level engineering decision wins.

## 2. Core Principles

Code must optimize for readability, explicit dependencies, strong typing, testability, safe async behavior, and narrow responsibility.

- prefer boring, explicit code over clever indirection;
- keep one primary responsibility per module/type;
- make dependencies visible through constructors/function parameters/composition;
- use platform-owned types at application boundaries;
- isolate framework/vendor SDK types at their approved boundaries;
- fail clearly on invalid configuration/state;
- do not hide architectural violations behind helper functions.

## 3. Python Baseline

- CPython 3.14.7 is the required language runtime.
- Source is UTF-8.
- Use four spaces for indentation; tabs are prohibited in Python source.
- Keep lines readable; target at most 100 characters unless readability is materially worse after wrapping.
- Use trailing commas in multiline literals/calls/signatures where they improve stable formatting/diffs.
- Use one logical statement per line.
- Formatting/lint/type-check tool selection may be automated later; no implementation task may introduce a new repository-wide tool merely to enforce this document without task authorization.

## 4. Naming

| Construct | Convention | Example |
| --- | --- | --- |
| Module/function/local | `snake_case` | `build_response`, `retrieval_result` |
| Class/type | `PascalCase` | `RAGService`, `Citation` |
| Constant | `UPPER_SNAKE_CASE` | `DEFAULT_TOP_K` |
| Application service | `*Service` | `RAGService` |
| Repository | `*Repository` | `SessionRepository`, `QdrantDocumentRepository` |
| External provider | `*Provider` | `BedrockLLMProvider` |
| Builder | `*Builder` | `PromptBuilder`, `ResponseBuilder` |
| State/lifecycle owner | `*Manager` | `SessionManager` |
| Registry | `*Registry` | `ToolRegistry` |
| Transport DTO | `*Request`, `*Response` | `QueryRequest`, `QueryResponse` |
| Internal operation output | semantic `*Result` | `RetrievalResult` |
| Application exception | `*Error` | `RetrievalError` |

Python protocols/ABCs do **not** use an `I` prefix. Use `LLMProvider`, not `ILLMProvider`.

Async functions are named for the operation (`retrieve`, `generate`, `save`), not `async_retrieve`. The signature communicates async behavior.

Avoid vague production names such as `Manager`, `Helper`, `Utils`, `Common`, or `Processor` unless the name communicates a real owned responsibility.

## 5. Imports and Dependencies

Group imports in this order with a blank line between groups:

1. Python standard library;
2. third-party packages;
3. application-local imports.

Rules:

- no wildcard imports;
- no imports added solely for side effects unless framework registration explicitly requires them and the reason is documented;
- application/domain modules must not import FastAPI, LangGraph, Qdrant, Bedrock, LM Studio/OpenAI-compatible SDK clients, or other concrete infrastructure types;
- provider modules may import their concrete SDKs but translate results/errors before returning to application code;
- avoid circular-import workarounds; fix the dependency direction instead;
- local imports used only to hide an import cycle are a design smell and require review.

## 6. Type Discipline

- public functions, methods, constructors, provider contracts, repository contracts, and application-service boundaries require explicit parameter and return types;
- avoid `Any` at architectural boundaries; confine unavoidable vendor/dynamic values to adapters and translate promptly;
- use precise optionality (`T | None`) instead of sentinel ambiguity;
- use application-owned Pydantic models/dataclasses/value objects where stable typed data crosses module boundaries;
- do not expose raw dictionaries when a stable named contract materially improves correctness;
- do not pass provider SDK response objects through application layers;
- collections should be typed to their element/key/value semantics.

Type suppression (`# type: ignore`) must be narrow and include a reason when it hides more than a known third-party typing defect.

## 7. Functions, Classes, and Modules

- functions should do one coherent thing and expose explicit inputs/outputs;
- avoid Boolean-flag-heavy functions that represent several behaviors; prefer clearer operations/contracts;
- constructors establish valid dependencies but should not perform expensive network work unless lifecycle semantics explicitly require it;
- application services orchestrate use cases; they do not construct providers;
- providers adapt external systems; they do not own business policy, prompts, retrieval policy, or response formatting;
- controllers translate transport and call one application use case;
- factories/composition select and construct dependencies; they do not become global service locators.

## 8. Async and Concurrency

- I/O request paths are async-first;
- every coroutine must be awaited or deliberately scheduled through an owned background-work mechanism;
- never call `asyncio.run()` inside FastAPI/application request paths;
- synchronous network/SDK work must not block the event loop; isolate it behind an appropriate thread/executor boundary if no async API exists;
- cancellation should propagate through streaming/provider work where supported;
- shared mutable state requires explicit concurrency ownership;
- do not assume an `async def` function is non-blocking merely because of its signature.

## 9. Errors

- raise platform/application errors for expected boundary failures;
- use exception chaining (`raise ... from exc`) when translating infrastructure errors and retaining internal diagnostic context is useful;
- never return raw provider exception strings to API clients;
- do not catch `Exception` merely to return success or hide a failure;
- catch broadly only at an intentional boundary that translates/logs/re-raises safely;
- error messages must not contain credentials, raw provider bodies, private document contents, internal filesystem paths, or stack traces intended for clients.

## 10. Logging

- production code uses structured logging primitives defined by `OBSERVABILITY.md`;
- do not use `print()` for application runtime logging;
- log events/outcomes, not prose dumps of entire objects;
- never indiscriminately log prompts, queries, retrieved text, model output, tokens/credentials, or session contents;
- use correlation/request context where available.

## 11. Configuration and Constants

- runtime provider/model/endpoints/credentials are configuration, not source constants;
- never hard-code the development PC IP/hostname, LM Studio port, API keys, AWS credentials, Bedrock model IDs, or deployment-specific hostnames in application code;
- validate configuration at startup/composition before serving dependent traffic;
- do not read environment variables ad hoc throughout application services; settings/composition owns configuration access.

## 12. Prompts, Retrieval, Responses, and Agents

- prompts/templates belong to Prompt Builder/prompt assets, not providers/controllers;
- retrieval policy belongs to Retriever, not Qdrant/provider adapters;
- citations and response construction belong to Response Builder;
- Session Manager owns conversation-state policy;
- LangGraph nodes coordinate application capabilities and remain thin;
- retrieved documents/tool output are untrusted data and never gain authority over system/application instructions.

## 13. Comments and Documentation

Use comments to explain **why**, constraints, invariants, or non-obvious risks—not to restate the code.

Public architectural contracts and non-obvious behavior require docstrings. Small obvious private helpers do not need ceremonial docstrings.

TODO/FIXME comments must name the missing requirement/task/decision where possible. Do not leave vague permanent TODOs such as `# fix later`.

## 14. Tests

- test names describe behavior (`test_retrieve_rejects_invalid_top_k`);
- use Arrange/Act/Assert structure when it improves clarity without comment clutter;
- test through public behavior unless internal invariants require a focused unit test;
- do not accept HTTP 500 as a valid success-path outcome;
- tests must follow `TESTING.md` and must not require real production credentials in the default suite.

## 15. Prohibited Shortcuts

Do not:

- call provider/Qdrant SDKs from controllers/application business logic;
- hide dependencies behind mutable globals/service locators;
- silence type/runtime errors to make tests pass;
- create sync wrappers that take ownership of an already-running event loop;
- introduce speculative abstractions/providers/frameworks;
- perform unrelated refactors in a scoped task;
- encode provider-specific response fields into platform contracts without architecture review.

## 16. Review Checklist

Before approval, confirm:

- naming communicates architectural responsibility;
- types are explicit at public boundaries;
- dependency direction is correct;
- async work does not block or drop coroutines;
- errors are safely translated;
- logs are structured and redacted;
- configuration is externalized;
- tests cover changed behavior;
- no provider/framework leakage or speculative dependency was introduced.
