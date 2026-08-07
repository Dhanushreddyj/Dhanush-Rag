# Enterprise AI Platform — Engineering Roadmap

**Status:** ACCEPTED  
**Version:** 1.0  
**Last Updated:** 2026-08-07  
**Scope:** Python AI microservice; V1 production-grade Agentic RAG foundation

## 1. Purpose

This roadmap sequences engineering work without redesigning the accepted architecture. It is capability/dependency driven, not date driven. `TASKS.md` owns executable task detail; this document owns phase order and exit gates.

## 2. Roadmap Rules

- architecture/ADRs precede material implementation decisions;
- each implementation task has one logical scope and required tests;
- stabilize lower-level contracts before building higher-level orchestration;
- do not introduce future capabilities/providers/infrastructure speculatively;
- production readiness requires tests, security, observability, evaluation, and operational evidence—not a local demo;
- deferred ADRs block only work that requires those specific decisions, not unrelated foundation hardening.

## 3. Phase 0 — Architecture and Governance Foundation

**Status: COMPLETE**

Delivered:

- repository baseline audit and implementation gap map;
- `MASTER_CONTEXT.md`, `PROJECT_VISION.md`, `ARCHITECTURE.md`;
- ADR-001 through ADR-008 accepted;
- ADR-009 through ADR-011 explicitly deferred with decision triggers;
- `CODE_STYLE.md`, `CONTRIBUTING.md`, `TESTING.md`, `SECURITY.md`, `API_GUIDELINES.md`, `OBSERVABILITY.md`;
- execution planning documents and implementation-entry review package.

Exit condition: a senior engineer can identify service boundary, dependency direction, provider strategy, Qdrant/index strategy, streaming/session semantics, testing/security/observability expectations, and deferred production decisions without verbal handover.

## 4. Phase 1 — Runtime Foundation Hardening

**Goal:** create a correct, testable foundation before adding/expanding Agentic RAG components.

Sequence:

1. configuration/startup validation;
2. platform error taxonomy/translation contracts;
3. LLM/embedding/vector-store provider contract normalization, async-first;
4. controlled provider composition/single-active-provider selection;
5. remove legacy Chroma runtime/dependency/configuration paths;
6. harden Qdrant adapter and collection/index compatibility behavior;
7. harden development embedding path behind the contract;
8. harden local Qwen/LM Studio LLM adapter path;
9. establish provider/unit/contract/integration test baseline.

### Phase 1 Exit Gate

- application imports/startup configuration validate predictably;
- no approved runtime Chroma path remains;
- Qdrant is the sole V1 vector-store adapter;
- provider contracts are async-safe/provider-neutral;
- configuration/composition selects one implementation per capability;
- application code does not require provider SDK types;
- deterministic foundation tests pass without production credentials;
- local provider/Qdrant integrations have explicit integration-test paths.

## 5. Phase 2 — Owned RAG Application Components

**Goal:** establish the modular RAG capabilities that LangGraph will later orchestrate.

Sequence:

1. Prompt Builder and prompt ownership/version semantics;
2. Retriever pipeline and provider-neutral retrieval result/context selection;
3. Response Builder and citation validation/assembly;
4. Session Manager contract and V1 conversation-scoped policy (persistence backend still deferred);
5. ingestion service hardening with async Qdrant/embedding integration and source/chunk identity;
6. RAG application service orchestration over these components;
7. deterministic unit/integration tests and controlled RAG evaluation cases.

### Phase 2 Exit Gate

- Prompt Builder owns prompts;
- Retriever owns retrieval/context policy;
- Response Builder owns citations/response construction;
- Session Manager owns session policy;
- RAG service orchestrates instead of implementing all internals;
- provider SDK/Qdrant/FastAPI/LangGraph types do not leak into application contracts;
- ingestion/retrieval/citation identity is end-to-end testable;
- insufficient-context behavior has regression coverage.

## 6. Phase 3 — Delivery, Streaming, and Agentic RAG

**Goal:** expose stable application capabilities and introduce orchestration only after their contracts are reliable.

Sequence:

1. thin FastAPI controllers and dependency injection/composition boundary;
2. stable API error envelope and `/v1` capability contract migration plan;
3. provider-neutral application stream-event model;
4. SSE transport per ADR-008/API guidelines;
5. minimal controlled Tool Registry required by V1 orchestration;
6. LangGraph Agentic RAG graph over already-tested application operations;
7. API/SSE/graph routing tests.

### Phase 3 Exit Gate

- controllers contain transport logic only;
- SSE uses `start/delta/citation/metadata/error/done` platform events;
- cancellation/error/completion behavior is testable;
- LangGraph nodes are thin orchestration adapters;
- graph state contains platform-owned types, not provider SDK objects;
- RAG capabilities remain usable/testable without LangGraph.

## 7. Phase 4 — Production Hardening and Evaluation

**Goal:** establish operational confidence for a production candidate without prematurely selecting deferred infrastructure.

Work includes:

- structured logging/correlation/redaction;
- liveness/readiness and bounded dependency checks;
- timeout/retry/cancellation hardening;
- concurrency/multi-worker correctness review;
- cache/rate-state review (no accidental process-local production semantics);
- Bedrock production provider contract/integration validation once exact approved model configuration is available;
- Qdrant production index/compatibility/migration validation;
- security verification and prompt-injection/tool boundary tests;
- curated AI evaluation baseline for retrieval, groundedness, faithfulness, citations, insufficient-context behavior, hallucination, and latency;
- representative load/performance measurements against architecture budgets.

### Phase 4 Exit Gate

- no raw provider errors/secrets/sensitive content leak through APIs/logging;
- production provider/index configurations are validated;
- evaluation baseline/report exists;
- performance distributions are measured under representative conditions;
- readiness reflects actual dependencies;
- known production blockers are explicit.

## 8. Phase 5 — Production Deployment Readiness

**Goal:** promote infrastructure-dependent decisions only when real production inputs exist.

Required before production release:

- ADR-009 promoted: Next.js-to-Python authentication/trust mechanism;
- ADR-010 promoted: production telemetry/export/alerting stack;
- ADR-011 promoted: deployment/runtime topology;
- session persistence ADR promoted if production continuity semantics require it;
- secrets/network/ingress/scaling/runbook decisions aligned with topology;
- release/API compatibility and rollback plan;
- production smoke/readiness/evaluation gates.

This phase is intentionally blocked on operational requirements rather than guessed today.

## 9. Post-V1 Capability Expansion

After V1 is production-proven, roadmap candidates include property search, recommendations, CRM assistance, investment analysis, image search, scheduling, market analytics, and document intelligence.

Each enters through typed application capabilities/tools and only receives LangGraph routing/provider adapters when the requirement needs them. Roadmap presence does not authorize implementation.

## 10. Explicit Non-Goals

The roadmap does not authorize:

- ChromaDB;
- multi-provider runtime routing/fan-out;
- persistent long-term user memory in V1;
- a telemetry/deployment/auth technology before its deferred ADR is promoted;
- repository-wide cosmetic rewrites;
- building future real-estate AI products before the V1 foundation is stable.
