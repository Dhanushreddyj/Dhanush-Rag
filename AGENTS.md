# Codex Repository Governance

## Authority Order

Follow this hierarchy when instructions conflict:

1. Explicit owner decisions.
2. Accepted ADRs.
3. `docs/ARCHITECTURE.md`.
4. `docs/MASTER_CONTEXT.md`.
5. `docs/PROJECT_VISION.md`.
6. `docs/TASKS.md`.
7. `docs/PROMPTS.md`.
8. `docs/REVIEW.md`.
9. Engineering standards.
10. Workspace rules.
11. Active-task restrictions.

Stop and report any material conflict. Do not silently choose, reconcile, redesign, or broaden the architecture.

## Operating Rules

- Inspect the repository and make a bounded plan before editing.
- Work on exactly one approved task at a time and modify only its exact allowed files.
- Use CPython 3.14.7 strictly.
- Qdrant is the only approved V1 vector store. Do not introduce or retain a Chroma runtime path.
- Do not introduce LangChain casually or use it as a shortcut. It requires explicit architecture authorization.
- LangGraph is for orchestration only; it does not own business logic, provider access, retrieval, prompts, persistence, or HTTP delivery.
- Business logic remains provider-neutral. Provider selection is configuration-driven, with exactly one active implementation per capability.
- Never expose credentials, tokens, raw provider responses, tracebacks, internal paths, private content, or other raw internal data.
- Dependency installation, live external calls, destructive actions, staging, commits, and pushes require explicit owner approval.
- Mocked, deterministic, network-isolated tests are the default.
- Live LM Studio, Qdrant, or Bedrock tests require explicit owner authorization for that execution.
- Never begin the next task automatically.

## Active Implementation Task

### Authorization

- Task: DEV-RAG-001
- Prompt: CX-DEV-RAG-001
- Status: ARCHITECT_APPROVED
- Name: Working Development RAG Vertical Slice
- Python: CPython 3.14.7 only

### Objective

Deliver one verified development RAG vertical slice that:

1. imports and starts the FastAPI application under CPython 3.14.7;
2. loads typed configuration from the supported environment source;
3. composes exactly one development LLM adapter, one development embedding adapter, and Qdrant;
4. loads a safe synthetic Markdown or text test document;
5. splits it using application-owned code;
6. generates document embeddings through an OpenAI-compatible development adapter;
7. creates or validates an isolated Qdrant collection with the matching dimension;
8. stores vectors and provider-neutral payloads;
9. embeds a query;
10. retrieves relevant chunks;
11. builds grounded context;
12. generates an answer through LM Studio;
13. returns a validated FastAPI response containing safe source information; and
14. returns safe platform errors without raw exception leakage.

This is an explicit sequencing exception for a working development path. It does not redesign or simplify the approved architecture, authorize the full enterprise backlog, or establish production readiness.

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
- Qdrant is the only vector store; support both Qdrant Cloud and self-hosted Qdrant configuration.
- Use direct approved SDK or protocol clients.
- Remove all Chroma runtime paths.
- Remove all LangChain runtime imports and assumptions. Do not add LangChain packages.
- LangGraph remains orchestration-only and need not be introduced merely to prove this vertical slice.
- Provider selection remains configuration-driven, with exactly one active implementation per capability.
- Business logic must not depend on provider SDK types.
- Use async contracts consistently and await every coroutine.
- Provider adapters must not own prompt construction.
- Send actual query vectors to Qdrant, never natural-language text as a point query.
- Match the Qdrant collection dimension to the active embedding model.
- Use valid SDK vector, payload, filter, point, and response models.
- Disable application answer caching unless a safe complete cache identity is implemented and tested.
- API routes must not expose `str(exception)`, credentials, SDK responses, tracebacks, or internal paths.
- Tests must not treat HTTP 500 as success.
- Do not claim production readiness.
- Do not implement the complete authorization, canonical-corpus, reranking, agent-tool, streaming, production telemetry, or Bedrock-live scope.

### Offline Test Policy

Default tests must:

- be deterministic and network-isolated;
- use fakes or mocks for LM Studio and external Qdrant;
- test startup, configuration, provider composition, embeddings, Qdrant mapping, ingestion, retrieval, grounded generation, safe errors, and API responses;
- run under CPython 3.14.7; and
- leave existing external services untouched.

### Owner-Authorized Live Development Gate

Do not run the live gate until offline tests pass and the owner explicitly authorizes that execution.

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

If LM Studio lacks a usable embedding model, Qdrant credentials are unavailable, the configured embedding dimension is incompatible, or a live service cannot be reached, stop and report the exact blocker. Never fabricate a successful live result.

### Dependency Boundary

- Modify `requirements.txt` or `requirements-dev.txt` only when required by the approved direct-SDK architecture.
- Do not install packages automatically.
- If installation is required after manifest review, stop and request explicit owner approval with the exact package and command.

### Prohibited Scope

Do not:

- redesign or simplify approved architecture;
- stage, commit, push, merge, or delete branches;
- begin improvements beyond the working vertical slice;
- mark FND-002 through FND-009 DONE before review evidence is accepted;
- begin another task automatically.

### Evidence Requirements

Report exact files changed, implementation and contract mappings, exact commands and complete results, CPython version evidence, offline test evidence, compilation and diff-check results, dependency-manifest changes and any requested install command, live-gate authorization/status, the unique collection name if the live gate runs, and all remaining blockers or deferred scope. Include complete scoped diffs. Do not expose credentials or raw private data.

### Stop Condition

Stop after implementation and offline verification, then either complete an explicitly owner-authorized live gate or report the exact live-gate blocker/authorization requirement. Do not stage, commit, push, merge, delete branches, claim production readiness, begin later improvements, or begin another task.
