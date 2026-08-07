# Enterprise AI Platform — Testing and AI Evaluation Standard

**Status:** ACCEPTED  
**Version:** 1.0  
**Last Updated:** 2026-08-07  
**Applies To:** Unit, contract, integration, API, streaming, end-to-end, evaluation, and performance verification

## 1. Purpose

Tests establish deterministic software correctness; evaluations establish probabilistic AI quality. Production-grade Agentic RAG requires both.

This standard defines test ownership and gates without inventing unsupported quality/SLO thresholds before representative baselines exist.

## 2. Test Layers

| Layer | Purpose | Default external dependencies |
| --- | --- | --- |
| Unit | pure/module/application behavior | none |
| Contract | prove adapters satisfy platform contracts | fake/local/controlled implementation |
| Integration | verify composed modules/infrastructure | local/ephemeral approved infrastructure |
| API | HTTP schemas/status/errors/SSE/dependency overrides | no production providers required |
| End-to-end | validate representative full capability flow | controlled environment |
| AI Evaluation | retrieval/grounding/citation/quality regression | controlled dataset/providers as configured |
| Performance/load | latency/concurrency/stream behavior | representative dedicated environment |

The default fast suite must not require AWS credentials, a live production Bedrock endpoint, or other production secrets.

## 3. Unit Tests

Unit tests cover deterministic behavior such as:

- configuration validation;
- application/use-case orchestration with fakes;
- prompt construction/version selection;
- response/citation mapping;
- retrieval/context-selection policy;
- metadata-filter validation;
- session policy/context-window selection;
- cache-key composition;
- error translation;
- stream-event mapping;
- LangGraph routing/state rules when deterministic;
- embedding/index compatibility checks.

Tests target public/contract behavior and avoid coupling to incidental private implementation details.

## 4. Provider Contract Tests

Every provider implementation must prove the semantics required by its platform contract.

### LLM Provider

Verify generation result shape, streaming event normalization, timeout/error translation, cancellation where supported, and model metadata semantics.

### Embedding Provider

Verify query/document embedding shape, numeric output, deterministic dimension for configured model, batching semantics, async behavior, and safe error translation.

### Vector Store Provider

V1 contract tests target Qdrant only. Verify collection/index setup as owned by the provider/repository boundary, add/upsert semantics, retrieval/top-k/filter behavior, score mapping, deletion/reset semantics where approved, and error translation.

Do not maintain Chroma contract tests merely to demonstrate abstraction.

## 5. Integration Tests

Integration tests verify boundaries between real modules and approved local/ephemeral dependencies.

Priority integrations include:

- embedding -> Qdrant ingestion/retrieval compatibility;
- ingestion -> chunk metadata -> retrieval -> citation identity;
- Retriever -> provider contracts;
- RAG service -> Prompt/Response/Session boundaries;
- FastAPI composition/dependency lifecycle;
- SSE application events -> FastAPI transport;
- LangGraph -> already-tested application operations when the graph is introduced.

Production provider integration suites may run separately with explicit credentials/environment and must never be a hidden requirement of local unit tests.

## 6. API Tests

API tests must verify:

- request/response schema and validation bounds;
- stable error envelope/status mapping;
- Unicode/international query handling;
- dependency override/injection behavior;
- authentication boundary behavior once ADR-009 is promoted;
- liveness versus readiness semantics;
- SSE content type and incremental event parsing;
- stream start/delta/metadata-or-citation/error/done behavior;
- disconnect/cancellation where testable;
- raw provider exceptions/data are not leaked.

An HTTP 500 response is never an acceptable success-path assertion.

## 7. Async and Concurrency Tests

Tests must detect:

- missing `await`/returned coroutine objects;
- event-loop blocking by synchronous I/O where practical;
- cancellation propagation for streaming/provider work;
- unsafe shared mutable state;
- duplicate/non-idempotent background work;
- concurrency behavior of session/cache/provider lifecycle where relevant.

Do not use event-loop ownership tricks in production code merely to satisfy tests.

## 8. Qdrant and Embedding Compatibility

ADR-006 is a mandatory test boundary.

Tests must prove that:

- configured query embeddings match the active index compatibility identity;
- dimension mismatch fails clearly;
- model/provider change is not considered compatible based on dimension alone;
- incompatible changes require a new index revision/re-ingestion path;
- metadata/payload needed for source/citation identity survives ingestion/retrieval;
- development data is not assumed production-compatible merely because both use Qdrant.

## 9. AI Evaluation Dataset

Maintain a curated, versioned real-estate evaluation dataset with stable case IDs. It should include:

- answerable questions with expected evidence;
- unanswerable/insufficient-context questions;
- ambiguous questions;
- metadata-filter scenarios;
- citation expectations;
- multilingual/international text representative of approved product behavior;
- adversarial/prompt-injection-oriented retrieved content;
- regression cases from real defects when safe/appropriate.

Evaluation data must not contain uncontrolled production personal/sensitive data.

## 10. AI Evaluation Metrics

Track, as applicable:

- retrieval recall/relevance;
- context precision;
- groundedness;
- faithfulness;
- citation accuracy;
- citation coverage;
- answer relevance;
- insufficient-context behavior;
- hallucination/unsupported-material-claim rate;
- retrieval/time-to-first-event/end-to-end latency.

No global quality threshold is invented in this version. Baseline first; then record release gates with dataset/model/prompt/index versions so thresholds are meaningful.

## 11. Regression and Release Gating

Changes affecting prompts, model configuration, embeddings, chunking, retrieval policy, reranking, citations, session context, or agent routing must run the relevant evaluation/regression suite.

A change is not accepted merely because aggregate quality improves if it materially regresses citation correctness, insufficient-context behavior, security behavior, or latency without explicit review.

## 12. Performance Verification

Measure the initial architecture performance targets under representative conditions; do not treat local Qwen/LM Studio latency as production SLO evidence.

Track distributions (P50/P95/P99 where sample size supports them), not averages alone, for:

- API overhead;
- embedding latency;
- Qdrant retrieval;
- pre-generation pipeline;
- time to first streamed model event;
- total generation duration/output size;
- stream forwarding overhead;
- error/timeout rate under load.

## 13. Test Data and Isolation

- tests own/clean their data and collections;
- do not point destructive tests at shared production Qdrant collections;
- use explicit test collection/index identities;
- no real credentials in fixtures/snapshots;
- freeze/mock time only when it improves deterministic behavior;
- avoid order-dependent tests;
- random tests require reproducible seeds when failures must be replayed.

## 14. Coverage and Quality

Coverage is a diagnostic, not proof of correctness. Changed critical behavior must be meaningfully tested even before a repository-wide numeric threshold is established.

Do not write assertion-free tests, snapshot huge opaque provider objects, or mock the exact implementation under test until the test only proves its own mocks.

Flaky tests are defects: fix/isolate the cause rather than normalizing retries as success.

## 15. Minimum Change Gate

Before review/merge:

1. relevant deterministic tests pass;
2. provider/API/integration tests required by the changed boundary pass;
3. relevant AI evaluations run for probabilistic changes;
4. failures are explained/fixed rather than ignored;
5. test commands/results are reported in the implementation handoff;
6. production credentials/services are not required by the default fast suite.
