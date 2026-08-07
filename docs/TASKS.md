# Enterprise AI Platform — Engineering Task Backlog

**Status:** ACCEPTED PLANNING BASELINE  
**Version:** 1.0  
**Last Updated:** 2026-08-07  
**Implementation State:** AUTHORIZED — FND-001 only

## 1. Purpose

This file converts `ROADMAP.md` into bounded engineering tasks. It does not authorize execution. A task becomes executable only when promoted into an approved Cline prompt after dependency/review checks.

## 2. Status and Priority

Statuses:

- `PLANNED` — sequenced but not executable yet;
- `READY_AFTER_ENTRY` — no known architecture blocker once implementation entry is accepted;
- `READY` — explicitly authorized for implementation;
- `BLOCKED_DECISION` — requires a deferred decision/input;
- `IN_PROGRESS`, `REVIEW`, `DONE` — execution lifecycle after implementation begins.

Priorities: `P0` foundation/blocker, `P1` V1 capability, `P2` production hardening, `P3` future/optional.

## 3. Phase 1 — Runtime Foundation

| ID | Priority | Task | Depends On | Status |
| --- | --- | --- | --- | --- |
| FND-001 | P0 | Configuration/startup validation boundary | governance complete | READY |
| FND-002 | P0 | Platform error taxonomy and safe boundary errors | FND-001 | PLANNED |
| FND-003 | P0 | Normalize async LLM/Embedding/VectorStore provider contracts | FND-002 | PLANNED |
| FND-004 | P0 | Provider composition/single-active-provider selection | FND-003 | PLANNED |
| FND-005 | P0 | Remove legacy Chroma runtime/dependencies/config paths | FND-004 | PLANNED |
| FND-006 | P0 | Correct/harden Qdrant V1 provider behavior | FND-003, FND-005 | PLANNED |
| FND-007 | P0 | Development embedding adapter + ADR-006 compatibility integration | FND-003, FND-006 | PLANNED |
| FND-008 | P0 | Qwen/LM Studio OpenAI-compatible LLM adapter correctness | FND-003, FND-004 | PLANNED |
| FND-009 | P1 | Foundation integration/composition test harness | FND-006–FND-008 | PLANNED |

### FND-001 — Configuration/Startup Validation

Objective: make configuration deterministic, typed, validated before dependent traffic, and aligned with accepted provider/Qdrant architecture.

Known evidence: live baseline `app.main` imports `validate_settings`, while current `app.config` does not define it. Legacy Chroma configuration also exists but Chroma cleanup itself remains FND-005 to preserve one-task scope.

Allowed logical scope when promoted: configuration module + its focused tests only. Do not fix factory/Qdrant/RAG defects inside this task.

Acceptance direction:

- startup validation function exists and is testable;
- invalid numeric/required configuration fails clearly;
- provider selection values are validated without instantiating SDK clients;
- secrets/endpoints/model values remain externally configured;
- tests need no live provider/Qdrant/AWS access.

### FND-002 — Platform Error Taxonomy

Objective: define platform-owned error categories/translation contracts used by later provider/application/API work. No HTTP/provider SDK logic belongs in the core error model.

### FND-003 — Provider Contract Normalization

Objective: make required provider operations strongly typed and async-first with no vendor objects. Align implementation method names/signatures only through scoped adapter follow-ups.

### FND-004 — Provider Composition

Objective: select exactly one LLM and one embedding implementation at controlled composition/bootstrap; Qdrant is the sole vector-store implementation. Remove hidden environment reads/service-location from business paths as scoped.

### FND-005 — Chroma Removal

Objective: remove Chroma packages/config/provider runtime paths under ADR-001 without replacing architecture or touching unrelated application behavior.

### FND-006 — Qdrant Provider

Objective: correct client APIs, async blocking boundaries, embedding/query-vector handling, filter mapping, payload/source metadata, collection creation/dimension/distance compatibility, and error translation per provider contract/ADR-006.

### FND-007 — Development Embeddings

Objective: make the configured development embedding implementation satisfy the normalized provider contract and carry explicit index compatibility identity. Do not invent a permanent development vendor/model in architecture.

### FND-008 — Development LLM

Objective: make Qwen 3.6 via LM Studio's OpenAI-compatible endpoint satisfy LLM generation/streaming contracts without hard-coded LAN/model configuration or prompt ownership inside the provider.

## 4. Phase 2 — RAG Application Components

| ID | Priority | Task | Depends On | Status |
| --- | --- | --- | --- | --- |
| RAG-001 | P1 | Prompt Builder + prompt ownership/versioning | Phase 1 contracts | PLANNED |
| RAG-002 | P1 | Retriever pipeline/context selection contract | FND-006, FND-007 | PLANNED |
| RAG-003 | P1 | Response Builder + citation assembly/validation | RAG-002 | PLANNED |
| RAG-004 | P1 | Session Manager V1 contract/policy | FND-002 | PLANNED |
| RAG-005 | P1 | Ingestion service async/source/chunk/index hardening | FND-006, FND-007 | PLANNED |
| RAG-006 | P1 | RAG application service orchestration | RAG-001–RAG-005, FND-008 | PLANNED |
| RAG-007 | P1 | Controlled RAG integration/evaluation baseline | RAG-006 | PLANNED |

Rules:

- RAG-004 selects no production persistence backend (ADR-007);
- RAG-006 does not embed prompts/retrieval/citation policy back into one god service;
- citations derive from stored/retrieved source/chunk identity;
- retrieved content remains untrusted model context.

## 5. Phase 3 — API, Streaming, Agent

| ID | Priority | Task | Depends On | Status |
| --- | --- | --- | --- | --- |
| API-001 | P1 | Thin FastAPI controller/dependency boundary | RAG-006 | PLANNED |
| API-002 | P1 | `/v1` contract + stable error envelope migration | API-001 | PLANNED |
| STR-001 | P1 | Provider-neutral application stream-event model | RAG-003, FND-008 | PLANNED |
| STR-002 | P1 | SSE FastAPI transport per ADR-008 | STR-001, API-001 | PLANNED |
| AGT-001 | P1 | Minimal Tool Registry contracts/approved tools | RAG-006 | PLANNED |
| AGT-002 | P1 | LangGraph V1 Agentic RAG orchestration | RAG-006, STR-001, AGT-001 | PLANNED |
| AGT-003 | P1 | Graph/SSE/API integration tests | STR-002, AGT-002 | PLANNED |

LangGraph implementation cannot be promoted before underlying components are independently stable/tested.

## 6. Phase 4 — Production Hardening

| ID | Priority | Task | Depends On | Status |
| --- | --- | --- | --- | --- |
| OPS-001 | P2 | Structured logging/correlation/redaction primitives | foundation errors/API context | PLANNED |
| OPS-002 | P2 | Liveness/readiness dependency checks | provider composition | PLANNED |
| OPS-003 | P2 | Timeout/retry/cancellation/concurrency audit | Phase 1–3 | PLANNED |
| EVAL-001 | P2 | Curated real-estate evaluation dataset + harness | RAG-007 | PLANNED |
| PERF-001 | P2 | Representative performance/load baseline | Phase 3 | PLANNED |
| SEC-001 | P2 | Production Next.js-to-Python authentication | ADR-009 promoted | BLOCKED_DECISION |
| TEL-001 | P2 | Production telemetry exporter/backend integration | ADR-010 promoted | BLOCKED_DECISION |
| DEP-001 | P2 | Production deployment/runtime implementation | ADR-011 promoted | BLOCKED_DECISION |
| MEM-001 | P2 | Production session persistence | production persistence requirements/ADR | BLOCKED_DECISION |

Bedrock production provider integration/validation is promoted when exact production model/configuration is selected. The provider family is accepted; model/index compatibility still requires concrete configuration evidence.

## 7. Task Promotion Checklist

Before changing a task from `PLANNED` to executable:

1. dependencies are reviewed/complete enough;
2. no deferred ADR is being bypassed;
3. allowed files are explicit;
4. acceptance criteria/tests are explicit;
5. one logical module/concern is affected;
6. prompt references current governance versions;
7. architecture review confirms the task does not cause a second refactor immediately afterward.

## 8. Out-of-Scope Backlog

Do not implement until separately promoted: hybrid search, reranking technology selection, conversation summaries/compression, long-term memory, dynamic multi-provider routing/failover, future recommendation/property/CRM/investment/image/scheduling/analytics capabilities.
