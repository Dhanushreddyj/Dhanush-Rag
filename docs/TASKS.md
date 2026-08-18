# Nofeez AI Platform — Engineering Task Backlog

**Status:** PROPOSED REQUIREMENTS ALIGNMENT
**Version:** 2.0
**Last Updated:** 2026-08-18
**Implementation State:** SUSPENDED — NO EXECUTABLE CLINE PROMPT

## 1. Purpose

This backlog converts ROADMAP.md into bounded tasks. A task is executable only when its dependencies are accepted and PROMPTS.md marks its prompt ARCHITECT_APPROVED.

## 2. Statuses

- PROPOSED — awaiting architecture/owner acceptance;
- PLANNED — accepted sequencing, not executable;
- READY — explicitly executable;
- BLOCKED_INPUT — required source/API/schema input is missing;
- IN_PROGRESS, REVIEW, DONE — implementation lifecycle;
- SUSPENDED — previous authorization withdrawn pending governance alignment.

## 3. Governance Alignment

| ID | Priority | Task | Depends On | Status |
| --- | --- | --- | --- | --- |
| GOV-001 | P0 | Commit authoritative Nofeez implementation requirement | instruction document | PROPOSED |
| GOV-002 | P0 | Requirements traceability and contradiction resolution | GOV-001 | PROPOSED |
| ADR-012–018 | P0 | Accept knowledge, routing, retrieval, permission, lifecycle and evaluation decisions | GOV-002 | PROPOSED |
| GOV-003 | P0 | Promote revised first implementation prompt | ADR acceptance | PLANNED |

## 4. Runtime Foundation

| ID | Priority | Task | Depends On | Status |
| --- | --- | --- | --- | --- |
| FND-001 | P0 | Configuration/startup validation boundary | GOV-003 | SUSPENDED |
| FND-002 | P0 | Platform error taxonomy | FND-001 | PLANNED |
| FND-003 | P0 | Async provider contract normalization | FND-002 | PLANNED |
| FND-004 | P0 | Provider composition and one-active-provider selection | FND-003 | PLANNED |
| FND-005 | P0 | Remove all legacy Chroma runtime/config/dependency paths | FND-004 | PLANNED |
| FND-006 | P0 | Qdrant dense/sparse index and payload compatibility foundation | FND-003, FND-005, ADR-014 | PLANNED |
| FND-007 | P0 | Development embedding adapter | FND-003, FND-006 | PLANNED |
| FND-008 | P0 | LM Studio/Qwen LLM adapter | FND-003, FND-004 | PLANNED |
| FND-009 | P0 | Foundation contract/integration test harness | FND-006–008 | PLANNED |

## 5. Canonical Knowledge Foundation

| ID | Priority | Task | Depends On | Status |
| --- | --- | --- | --- | --- |
| KB-001 | P0 | Canonical source repository/discovery contract | ADR-012, 110 files supplied | BLOCKED_INPUT |
| KB-002 | P0 | YAML metadata schema and parser | KB-001 | PLANNED |
| KB-003 | P0 | Markdown hierarchy/numbered-section parser | KB-002 | PLANNED |
| KB-004 | P0 | Document validator and validation queue | KB-002, KB-003 | PLANNED |
| KB-005 | P0 | Semantic chunker and parent-context enrichment | KB-003, KB-004 | PLANNED |
| KB-006 | P0 | Stable IDs and SHA-256 document/chunk hashing | KB-005 | PLANNED |
| KB-007 | P0 | Document/version registry and status transitions | KB-006, ADR-016 | PLANNED |
| KB-008 | P0 | Incremental changed-section embedding pipeline | KB-007, FND-007 | PLANNED |
| KB-009 | P0 | Qdrant chunk/document/version payload schemas | KB-007, FND-006 | PLANNED |

Acceptance: all supplied canonical files validate; failed files do not index; chunks preserve metadata, provenance and parent context; unchanged content skips embedding.

## 6. Retrieval, Routing and Permissions

| ID | Priority | Task | Depends On | Status |
| --- | --- | --- | --- | --- |
| RET-001 | P0 | Dense + sparse candidate retrieval | KB-009, ADR-014 | PLANNED |
| RET-002 | P0 | Provider-neutral metadata filters | RET-001 | PLANNED |
| RET-003 | P0 | Reranker contract and implementation | RET-001 | PLANNED |
| RET-004 | P0 | Confidence gate and context selection | RET-002, RET-003 | PLANNED |
| RTR-001 | P0 | Static/live/model/action classification models | ADR-013 | PLANNED |
| RTR-002 | P0 | Nofeez intent registry | RTR-001, 110 files supplied | BLOCKED_INPUT |
| RTR-003 | P0 | Entity resolver and hierarchy | RTR-001 | PLANNED |
| RTR-004 | P0 | Knowledge/domain router | RTR-002, RTR-003 | PLANNED |
| AUTH-001 | P0 | Role/market/tenant authorization context contract | ADR-015, backend schema | BLOCKED_INPUT |
| AUTH-002 | P0 | Namespace and pre-LLM permission filters | AUTH-001, RET-002 | PLANNED |
| CTX-001 | P0 | Source precedence, deduplication and conflict detection | ADR-017, RET-004 | PLANNED |

## 7. Nofi Integration

| ID | Priority | Task | Depends On | Status |
| --- | --- | --- | --- | --- |
| RAG-001 | P1 | Prompt Builder and prompt-injection boundary | RET-004, RTR-004, AUTH-002 | PLANNED |
| RAG-002 | P1 | Structured Nofi Context Builder | RAG-001, CTX-001 | PLANNED |
| RAG-003 | P1 | Response Builder, citation trace and knowledge contract | RAG-002 | PLANNED |
| RAG-004 | P1 | UNKNOWN/current-state-unavailable fallback behavior | RAG-003 | PLANNED |
| TOOL-001 | P1 | Live domain/model/action tool contracts | RTR-004, external API schemas | BLOCKED_INPUT |
| AGT-001 | P1 | Tool Registry | TOOL-001 | PLANNED |
| AGT-002 | P1 | LangGraph orchestration over tested capabilities | RAG-004, AGT-001 | PLANNED |
| API-001 | P1 | Thin /v1 APIs and stable error envelopes | RAG-004 | PLANNED |
| STR-001 | P1 | Provider-neutral stream events and SSE | API-001, AGT-002 | PLANNED |

## 8. Synchronization and Operations

| ID | Priority | Task | Depends On | Status |
| --- | --- | --- | --- | --- |
| SYNC-001 | P1 | Source-change trigger and validation pipeline | KB-008 | PLANNED |
| SYNC-002 | P1 | Incremental upsert and superseded-chunk removal | SYNC-001 | PLANNED |
| REC-001 | P1 | Document/chunk/Qdrant reconciliation checks | SYNC-002 | PLANNED |
| REC-002 | P1 | Safe derived-state auto-repair | REC-001 | PLANNED |
| OPS-001 | P1 | Ingestion status and index-health APIs | KB-009, REC-001 | PLANNED |
| OPS-002 | P1 | Structured routing/retrieval/ingestion telemetry | RTR-004, RET-004 | PLANNED |
| OPS-003 | P2 | Admin diagnostic APIs | OPS-001, OPS-002 | PLANNED |

## 9. Evaluation and Release Gates

| ID | Priority | Task | Depends On | Status |
| --- | --- | --- | --- | --- |
| EVAL-001 | P0 | Golden-question schema and initial fixtures | ADR-018, 110 files supplied | BLOCKED_INPUT |
| EVAL-002 | P1 | Route/retrieval/reranking tests | RTR-004, RET-004, EVAL-001 | PLANNED |
| EVAL-003 | P1 | Groundedness/citation/conflict tests | RAG-004, EVAL-001 | PLANNED |
| EVAL-004 | P0 | Permission/privacy leakage tests | AUTH-002, EVAL-001 | PLANNED |
| EVAL-005 | P0 | 300–500 question release suite | EVAL-002–004 | PLANNED |
| PROD-001 | P1 | Security, observability, deployment and rollback gates | Phase dependencies + deferred production ADRs | PLANNED |

Critical release criteria: zero permission leakage, zero fabricated inventory, zero fabricated payment state, zero fabricated legal/current compliance claims.

## 10. Promotion Rule

No task is READY. After this governance change is reviewed, accept or revise ADR-012 through ADR-018, supply the required canonical/API/authorization inputs, then promote exactly one bounded prompt.
