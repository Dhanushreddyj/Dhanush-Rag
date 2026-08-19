# Nofeez AI Platform — Engineering Roadmap

**Status:** ACTIVE
**Version:** 2.0
**Last Updated:** 2026-08-19
**Scope:** Python AI microservice and Nofeez knowledge/orchestration layer

## 1. Purpose

This roadmap aligns the accepted clean architecture with the authoritative Nofeez RAG implementation requirements for 110 canonical Markdown modules. It is dependency-driven, not date-driven. TASKS.md owns executable detail.

## 2. Roadmap Rules

- no implementation runs until its governing ADRs and task are accepted;
- canonical sources are never silently rewritten by ingestion;
- route selection precedes retrieval or tool execution;
- permission filtering precedes LLM context exposure;
- RAG describes stable meaning, live services provide current truth, model services produce labeled estimates, and tools perform authorized changes;
- Qdrant remains the sole V1 vector database and must support the approved hybrid retrieval contract;
- every phase includes deterministic tests and traceability;
- implementation proceeds through small reviewed tasks.

## 3. Phase 0A — Requirements and Governance Alignment

**Status: COMPLETE**

Deliver:

- authoritative Markdown copy of the 66-part Nofeez instruction;
- requirements traceability matrix;
- updated master context, vision, architecture, roadmap, tasks, prompts and review record;
- ADR-012 through ADR-018;
- explicit suspension of old implementation authorization.

Exit gate:

- no contradiction remains about canonical sources, routing, hybrid retrieval, permissions, incremental indexing, reconciliation or evaluation;
- Qdrant/OpenSearch interpretation is explicit;
- revised task dependencies are accepted;
- one implementation prompt is promoted explicitly.

## 4. Phase 1 — Runtime Foundation

Sequence:

1. typed configuration/startup validation;
2. platform error taxonomy;
3. async provider contracts;
4. controlled provider composition;
5. legacy Chroma removal;
6. Qdrant dense/sparse index compatibility foundation;
7. development embedding adapter;
8. LM Studio/Qwen development LLM adapter;
9. deterministic foundation test harness.

Exit gate: startup is deterministic, provider SDKs do not leak, Qdrant is the only runtime vector store, and foundation tests need no production credentials.

## 5. Phase 2 — Canonical Knowledge Foundation

Sequence:

1. canonical repository and source discovery contract;
2. YAML metadata parser and schema validator;
3. Markdown heading/numbered-section parser;
4. forbidden-content and duplicate-ID validation queue;
5. semantic chunker with parent context;
6. deterministic document/chunk IDs and SHA-256 hashes;
7. document/version registry with ACTIVE, SUPERSEDED, ARCHIVED and DRAFT states;
8. changed-section detection and incremental embedding;
9. Qdrant payload/index schema and version filters.

Exit gate: all 110 supplied canonical modules parse successfully; invalid files do not index; unchanged chunks do not re-embed; changed sections replace only affected active chunks.

## 6. Phase 3 — Retrieval, Routing and Authorization

Sequence:

1. Nofeez intent registry;
2. entity resolver and hierarchy models;
3. stable/live/model/action query classifier;
4. domain route contract;
5. dense + sparse/keyword retrieval;
6. metadata filters;
7. reranker;
8. confidence gate and controlled query expansion;
9. role, market, tenant and namespace filters;
10. context deduplication/compression and source precedence.

Exit gate: route accuracy, retrieval quality and permission isolation meet approved evaluation gates; dynamic-state questions never rely on static RAG alone.

## 7. Phase 4 — Nofi Context and Response

Sequence:

1. Prompt Builder and trusted/untrusted context separation;
2. Nofi structured Context Builder;
3. Response Builder and citation validation;
4. UNKNOWN and CURRENT_STATE_UNAVAILABLE fallbacks;
5. fact/estimate/prediction/recommendation labeling;
6. conflict detection;
7. live domain/model/tool contracts;
8. LangGraph orchestration over tested application capabilities;
9. SSE delivery and session-scoped context where approved.

Exit gate: every material claim is traceable; unsupported property, price, payment, inventory and legal data is never fabricated; live-service failure does not fall back to stale RAG.

## 8. Phase 5 — Synchronization and Operations

Sequence:

1. Git/CI or approved source-change trigger;
2. parse/validate/diff/rechunk/re-embed/upsert pipeline;
3. superseded-chunk cleanup;
4. event-driven cache invalidation contracts;
5. scheduled reconciliation;
6. ingestion status and index-health APIs;
7. conflict and failed-validation queues;
8. structured retrieval and routing telemetry;
9. admin diagnostics APIs for the existing backend/UI.

Exit gate: changed knowledge becomes active automatically, deleted/superseded content is not retrievable, and reconciliation detects and repairs safe derived-state drift.

## 9. Phase 6 — Evaluation and Production Readiness

Deliver:

- 300–500 golden questions across product, cross-module, dynamic-state, privacy, ambiguity, multilingual and hallucination-trap categories;
- route, retrieval, reranking, groundedness, citation and permission tests;
- zero fabricated inventory, payment state and legal rules;
- zero permission leakage;
- representative latency and failure measurements;
- authentication, telemetry, deployment and secrets decisions required by production.

## 10. Post-V1

Future work may include verified translations, project/developer document namespaces, media extraction workflows, knowledge-graph enrichment, recommendations and other AI capabilities. None may bypass canonical-source, authorization, provenance or live-state boundaries.
