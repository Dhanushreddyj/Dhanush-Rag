# Enterprise AI Platform — Observability Standard

**Status:** ACCEPTED  
**Version:** 1.0  
**Last Updated:** 2026-08-07  
**Applies To:** Structured logging, metrics, traces/correlation, streaming telemetry, health/readiness, and operational diagnostics

## 1. Purpose

Production AI behavior must be diagnosable across API, retrieval, embeddings, Qdrant, model generation, sessions, ingestion, streaming, and agent orchestration without leaking sensitive content.

ADR-010 deliberately defers the telemetry vendor/stack. This standard defines vendor-neutral telemetry semantics that any future exporter/backend must preserve.

## 2. Operational Questions

Telemetry must make it possible to answer:

- Which request failed and at which stage?
- Which configured provider/model/index revision handled it?
- How long did validation, session load, embedding, retrieval, reranking, prompt construction, generation, and streaming take?
- How many chunks were retrieved/selected?
- Was a cache used?
- Did a provider timeout/retry/failure occur?
- What was time to first streamed event?
- Did a stream complete, fail, or disconnect?
- Which ingestion document/chunks succeeded/failed?
- Is the process alive and are required dependencies ready?

## 3. Correlation Model

Assign a request/correlation identifier at the API boundary and propagate it through application operations, provider calls, Qdrant/retrieval work, LangGraph/tool execution, logs, and trace context.

Rules:

- request IDs are not authentication secrets;
- preserve caller trace/correlation context only after validating supported shape/size;
- background work creates/propagates owned correlation context explicitly;
- one request can contain multiple spans/events but remains traceable as one operation;
- never use request/session/document IDs as unbounded metric labels.

## 4. Structured Logging

Runtime logs are structured records, not `print()` statements or multiline object dumps.

Recommended common fields where relevant:

- timestamp;
- severity;
- service/version/environment;
- request/correlation ID;
- operation/stage;
- outcome/error category;
- duration;
- provider capability/provider-model safe identifier where approved;
- index/corpus revision safe identifier;
- retry count;
- stream state;
- counts such as retrieved/selected chunks.

Do not log entire request/provider/session objects merely for convenience.

## 5. Sensitive Data and Redaction

By default, do **not** log:

- system/application prompts;
- user query text;
- retrieved document text;
- generated model output;
- full citation/document metadata if sensitive;
- full session conversation state;
- authorization headers/tokens/API keys/AWS credentials/Qdrant keys;
- raw provider request/response bodies;
- arbitrary tool output.

Prefer safe identifiers, lengths/counts, hashes/pseudonymous values where justified, and typed outcome/error categories.

Any future content sampling/debug logging requires explicit security/privacy policy, access control, retention, and redaction; it is never enabled casually in production.

## 6. Metrics

Metrics are low-cardinality and stage-oriented. Names may be mapped to the selected telemetry backend later, but the semantics remain stable.

Required metric families should cover:

- request count by operation/outcome;
- request duration;
- validation failures;
- embedding request duration/failure;
- Qdrant/retrieval duration/failure;
- retrieved/selected chunk distributions;
- reranker duration when enabled;
- provider generation duration/failure/timeout/retry;
- time to first streamed event;
- stream duration/completion/error/disconnect;
- ingestion documents/chunks success/failure/duration;
- cache hit/miss/eviction where caching is enabled;
- readiness/dependency-state transitions where appropriate.

Never label metrics with query text, request ID, session ID, document path, raw model output, or another unbounded/high-cardinality value.

## 7. Tracing and Spans

Trace structure should mirror architecture stages, for example:

- API request;
- application use case;
- session load/update;
- query embedding;
- retrieval/Qdrant;
- reranking;
- prompt build;
- LLM/provider generation;
- response/citation build;
- SSE streaming lifecycle;
- tool execution;
- ingestion/load/chunk/embed/upsert stages.

Provider/repository adapters create infrastructure spans without exposing SDK objects to application logic. Trace attributes follow the same sensitive-data rules as logs.

Exact tracing SDK/exporter is deferred by ADR-010.

## 8. Streaming Observability

For ADR-008 SSE streams track at minimum:

- request accepted/start time;
- model/application stream start;
- time to first emitted application/SSE event;
- event count/bytes only where useful and safe;
- completion versus terminal error;
- client disconnect/cancellation;
- provider timeout/retry during stream;
- total duration.

Do not log every generated delta by default. Observability must not turn streaming into a content-exfiltration path.

## 9. Retrieval and AI Quality Context

Operational telemetry and AI evaluation are complementary.

Telemetry may record safe version/identity metadata needed to correlate regressions, such as:

- prompt version;
- retrieval policy version;
- model/provider configuration identity safe for operations;
- embedding/index revision;
- chunking/corpus revision;
- reranker version when used.

Groundedness/faithfulness/citation quality are evaluation metrics governed by `TESTING.md`, not inferred solely from production latency/logs.

## 10. Error Telemetry

Errors use stable categories aligned with platform error boundaries: validation, configuration, provider timeout/unavailable, embedding, vector store, retrieval, ingestion, session, tool, orchestration, streaming, and unknown/internal.

Internal logs/traces may retain safe exception type/stack diagnostics according to access policy, but client responses remain redacted/provider-neutral.

Repeated failures must be diagnosable without recording raw sensitive provider responses.

## 11. Liveness and Readiness

Expose separate semantics:

- **Liveness:** process/runtime can respond;
- **Readiness:** dependencies/configuration needed for traffic are usable.

Readiness covers configured dependencies appropriate to the running capability without performing expensive model generation on every probe.

Health telemetry records state/outcome and latency without credentials/endpoints/private error dumps.

## 12. Performance Budgets

Track architecture's initial engineering targets separately from accepted SLOs. At minimum preserve measurement boundaries for:

- Python API overhead;
- query embedding;
- vector retrieval;
- optional reranking;
- pre-generation RAG pipeline;
- time to first streamed model event;
- Python stream forwarding overhead;
- end-to-end duration/output size.

Development Qwen/LM Studio measurements are reported separately from production Bedrock performance. Local workstation latency is not production SLO evidence.

## 13. Sampling, Retention, and Alerting

Exact sampling rates, retention periods, alert thresholds, dashboards, on-call integration, and telemetry backend are deferred until ADR-010 is promoted.

Principles now:

- never sample away all errors;
- avoid high-volume debug events by default;
- alerts should be based on actionable service health/quality signals, not noisy single events;
- telemetry retention must respect future privacy/data-residency policy;
- initial performance budgets are not automatically paging SLOs.

## 14. Tests and Review

Tests should verify instrumentation behavior where correctness/security depends on it:

- correlation propagation;
- sensitive-field redaction/absence;
- stable error categories;
- readiness behavior;
- SSE completion/error/disconnect metrics/events;
- no raw provider content in normal logs.

Review telemetry changes for cardinality, sensitive data, performance overhead, and architecture ownership.

## 15. Deferred Technology Choice

This standard selects **no telemetry vendor, exporter, agent, collector, or SaaS product**. Introducing one requires ADR-010's decision inputs/approval and a scoped integration task.

## 16. Review Checklist

- Can one request be traced across architectural stages?
- Are latency/failure metrics available for the important dependencies?
- Are logs structured rather than `print()` based?
- Is sensitive AI/session/provider content excluded by default?
- Are metric labels bounded?
- Are streaming completion/failure/disconnect observable?
- Are liveness/readiness distinct?
- Did the change accidentally select the deferred telemetry stack?
