# Nofeez RAG Requirements Traceability

**Status:** PROPOSED
**Version:** 1.0
**Last Updated:** 2026-08-18
**Source:** NOFEEZ_RAG_IMPLEMENTATION_REQUIREMENTS.md

## 1. Purpose

This document maps the 66 source requirements into architectural decisions, roadmap capabilities, tasks and release gates. It prevents requirements from disappearing into prose or being implemented in the wrong layer.

## 2. Requirement Groups

| Source sections | Requirement group | Architecture owner | ADR / task family | V1 |
| --- | --- | --- | --- | --- |
| 1–2, 35–36, 66 | Canonical source authority and controlled updates | Knowledge ingestion/application | ADR-012, KB-* | Mandatory |
| 3, 22–27 | YAML metadata, validation, stable identity, hashing and versions | Parser/version registry | ADR-012, ADR-016, KB-* | Mandatory |
| 4–5, 51–52 | Semantic chunking, parent context and compression | Chunker/Retriever | KB-005, CTX-001 | Mandatory |
| 6–7, 17–19, 60–62 | Static/live/model/action separation and fallbacks | Knowledge Router/application | ADR-013, RTR-*, RAG-004 | Mandatory |
| 8–10, 30–32 | Hybrid retrieval, filters, reranking and confidence | Retriever | ADR-014, RET-* | Mandatory |
| 11–12 | Intent dictionary and entity hierarchy | Router/domain | RTR-002, RTR-003 | Mandatory |
| 13 | Vector/index design and namespaces | Qdrant provider/repository | ADR-014, ADR-015, KB-009 | Mandatory |
| 14–16, 45–47 | Permission-aware retrieval and context separation | Authorization/Context Builder | ADR-015, AUTH-*, RAG-002 | Mandatory |
| 18, 20, 53, 62 | No fabrication, source precedence, conflicts and zero-answer behavior | Context/Response Builder | ADR-017, CTX-001, RAG-003/004 | Mandatory |
| 21–25, 37–39 | Incremental indexing, invalidation and reconciliation | Synchronization/registry | ADR-016, SYNC-*, REC-* | Mandatory |
| 28–29, 54, 59 | Logging, traceability, diagnostics and admin visibility | Observability/admin API | OPS-* | Mandatory |
| 33–34 | Multilingual retrieval and session correction | Router/Session Context | RTR-*, session policy | Mandatory foundation |
| 40–44 | Evaluation set, route tests and golden answers | Evaluation | ADR-018, EVAL-* | Mandatory |
| 48–50 | Media candidates and knowledge-graph/dependency expansion | Document intelligence/graph | Future controlled capability | Deferred unless source corpus requires |
| 55–57 | Delivery phases, Git workflow and environment isolation | Governance/CI | ROADMAP, CONTRIBUTING | Mandatory workflow |
| 58, 63–65 | Secrets, performance and definition of done | Security/observability/release | Standards + PROD-001 | Mandatory |

## 3. Key Resolutions

### Qdrant versus OpenSearch

The source instruction says “if the team is already using OpenSearch.” This is conditional. ADR-001 remains authoritative: Qdrant is the sole V1 vector database. ADR-014 requires Qdrant dense/sparse hybrid retrieval. Adding OpenSearch requires an explicit superseding ADR.

### Admin dashboard ownership

This repository owns Python admin/diagnostic APIs and data contracts. A user-facing dashboard belongs to the existing Next.js product boundary unless separately assigned.

### PDF and developer documents

The 110 canonical Markdown files are the primary global knowledge source. PDFs, brochures and developer uploads use separate namespaces and provenance states; extracted content is not automatically canonical.

### Authentication versus retrieval authorization

ADR-009 still defers the concrete service-to-service authentication mechanism. That does not defer application authorization contracts for role, market, tenant and namespace filtering. The Next.js authorization-context schema remains a required input.

## 4. Critical Release Gates

- permission leakage = 0;
- fabricated inventory = 0;
- fabricated payment state = 0;
- fabricated current legal/compliance rule = 0;
- dynamic-state routing never falls back to static RAG;
- every grounded answer retains internal source/chunk traceability;
- failed canonical validation never reaches the active index;
- superseded/deleted chunks are absent from normal active retrieval;
- reconciliation detects missing, duplicate, stale and orphaned derived state;
- 300–500 approved evaluation questions pass the ratified thresholds.

## 5. Remaining External Inputs

- complete set of 110 canonical Markdown modules;
- role/market/tenant authorization-context contract;
- live domain API and tool schemas;
- production authentication, telemetry and deployment requirements;
- final embedding/index compatibility selections for each environment.
