# MASTER_CONTEXT.md

**Version:** 1.7  
**Status:** ACTIVE  
**Project:** Enterprise AI Platform for Real Estate  
**Owner:** Dhanush Reddy  
**Primary Architect:** ChatGPT (Principal AI Architect)  
**Implementation Engineer:** Cline (Local Qwen 3.6)  
**Repository:** https://github.com/Dhanushreddyj/Dhanush-Rag.git

## 1. Project Mission

Build a production-grade Enterprise AI Platform for a worldwide real estate platform.

The Python service is an independent AI microservice that integrates with an existing Next.js backend. The goal is not to build a chatbot or a simple RAG demo. Agentic RAG is the first production capability of a platform intended to support additional real estate AI capabilities without major architectural redesign.

## 2. Repository Responsibility

This repository owns **only the Python AI service**.

The following already exist and are outside this repository's ownership:

- Next.js backend;
- web application;
- mobile application.

The existing backend consumes the Python service through explicit APIs. The Python project must not require redesigning the existing application backend.

## 3. Version 1 Product Scope

**V1 = Production-Grade Agentic RAG.**

The V1 target includes the foundations required for:

- document ingestion;
- embeddings;
- vector storage and retrieval;
- grounded responses and verified source/citation mapping;
- streaming end to end;
- provider abstraction;
- FastAPI service delivery;
- prompt construction;
- retriever/reranker pipeline;
- session-scoped memory;
- LangGraph orchestration;
- response construction;
- typed errors and configuration;
- security and observability;
- automated testing and AI evaluation.

This list is the **target product scope**, not a claim that every item is already complete in the current repository.

## 4. Verified Repository Baseline

The August 2026 repository audit found useful architectural intent and a meaningful RAG/provider baseline, but the implementation is not yet production-ready.

| Area | Verified Current State |
| --- | --- |
| FastAPI | present; route responsibilities require hardening |
| PDF/document ingestion | baseline loaders/chunking present; async, idempotency, and failure semantics require hardening |
| Embeddings | provider abstraction started; factory/provider contract inconsistencies require correction |
| Vector stores | Qdrant adapter started; SDK semantics and embedding wiring require correction. Legacy Chroma code exists in the audited snapshot but is outside the approved V1 target and will be removed through a scoped hardening task. |
| Retrieval | baseline flow present; async contract errors require correction |
| Grounded generation | baseline retrieve/generate intent present; request path requires hardening |
| Citations | source metadata exists; application-owned citation validation/mapping is not complete |
| Streaming | provider-level streaming code exists; end-to-end API streaming is not complete |
| Provider abstraction | present and worth preserving; contracts require normalization |
| Session memory | target capability; not complete in audited snapshot |
| LangGraph Agentic RAG | target capability; LangGraph orchestration is not implemented in audited snapshot |
| Testing | minimal; insufficient for production confidence |
| Observability | not production-complete |

Earlier numeric architecture scores and percentage estimates are treated as historical/provisional review notes, not production-readiness evidence. The authoritative current-vs-target assessment is maintained in `ARCHITECTURE.md` and `REVIEW.md`.

## 5. Technology Stack

| Category | Approved Direction |
| --- | --- |
| Programming Language | CPython 3.14.7 with AsyncIO / async-first I/O |
| Framework | FastAPI for HTTP delivery; Pydantic for typed data contracts and validation |
| Agent Framework | LangGraph for agent orchestration only |
| Provider Strategy | Configuration-driven provider contracts. Development LLM: local Qwen 3.6 through LM Studio's OpenAI-compatible endpoint. Development embeddings: current development configuration. Production LLM: AWS Bedrock models. Production embeddings: AWS Bedrock Embedding Models. Exactly one implementation per provider capability is active at a time. |
| Vector Database | Qdrant is the only approved V1 vector database in development and production |
| Deployment | Independently deployable Python AI microservice behind the existing Next.js backend. Production deployment platform remains an explicit future decision. |
| Development Tooling | Mac with VS Code + Cline; PC-hosted LM Studio for the current development LLM workflow |

Streaming responses and session-scoped memory are platform capabilities, not provider/technology selections.

Technologies are not replaced or expanded without an explicit decision. Current provider selections are configuration choices behind stable contracts, not permanent architectural coupling. Future provider names do not authorize speculative SDK additions.

## 6. Development Topology

Development uses a split-machine workflow:

- **Mac:** VS Code, Cline, source development, and local project workflow;
- **PC:** LM Studio inference server using Qwen 3.6 14B A3B FableVibes Q5/Q4 on RTX 4070 Super / Ryzen 9700X / 32 GB RAM.

The PC is treated as a network LLM provider endpoint. Application source must not hard-code its LAN IP, port, API key, or model name.

The architecture does not require the Python runtime to be permanently co-located with either machine in development; endpoint configuration controls provider connectivity.

## 7. Engineering Principles

- Clean Architecture
- SOLID
- dependency injection
- Provider Pattern
- Repository Pattern where persistence semantics justify it
- Service Layer
- interface/contract first
- async-first I/O
- strong typing
- low coupling / high cohesion
- no circular dependencies
- no business logic in FastAPI controllers
- no business logic in providers
- no business logic in factories or middleware

## 8. Architectural Ownership

- Controllers remain thin.
- Services orchestrate application use cases.
- Providers communicate with external systems.
- Repositories own application persistence semantics.
- Prompt Builder owns prompt/model-request construction.
- Retriever owns retrieval policy.
- Session Manager owns conversation-scoped memory policy.
- Response Builder owns response/citation construction.
- Tool Registry owns agent-callable tool registration/resolution.
- Agent layer owns orchestration.
- LangGraph coordinates; it does not absorb application logic.

Each module has one primary reason to change.

## 9. Provider Strategy

One active implementation per provider capability is selected through validated configuration/composition. V1 does not perform multi-provider fan-out or runtime provider routing: exactly one configured LLM provider and one configured embedding provider are active at a time.

Approved current direction:

- development LLM: local Qwen via LM Studio/OpenAI-compatible endpoint;
- production LLM: AWS Bedrock models;
- development vector store: Qdrant;
- production vector store: Qdrant;
- development embeddings: current development configuration;
- production embeddings: AWS Bedrock Embedding Models.

Potential future LLM/embedding providers such as OpenAI, Azure OpenAI, Anthropic, Ollama, or Gemini remain options only if approved later. Potential future vector databases/search systems such as Milvus, Pinecone, or Azure AI Search likewise require a new architectural decision. Business/application logic must never depend on concrete provider SDKs.

## 10. Prompt, Memory, and Streaming Strategy

### Prompts

Prompt Builder owns system prompts and future recommendation, search, extraction, and summarization prompt families. Providers never own application prompt construction.

### Memory

V1 memory is session-based and conversation-scoped. Persistent long-term user memory is a later capability unless explicitly promoted.

### Streaming

Streaming is an end-to-end architectural constraint. Provider streaming alone does not count as feature completion; the application event model, Response Builder, FastAPI transport, cancellation, final citations/metadata, and Next.js integration contract must participate.

## 11. Future Capability Horizon

The architecture must be able to support future approved capabilities such as:

- property search;
- recommendation engine;
- CRM assistant;
- investment analysis;
- image search;
- scheduling;
- market analytics;
- document intelligence;
- tool calling;
- planning/orchestration capabilities;
- memory evolution.

Actual release sequencing is owned by `ROADMAP.md`.

## 12. Documentation Operating System

The engineering documentation set is intended to let a new senior engineer understand the platform and begin contributing confidently with minimal verbal handover.

Core documents:

- `MASTER_CONTEXT.md`
- `PROJECT_VISION.md`
- `ARCHITECTURE.md`
- `CODE_STYLE.md`
- `CONTRIBUTING.md`
- `API_GUIDELINES.md`
- `TESTING.md`
- `SECURITY.md`
- `OBSERVABILITY.md`
- `ROADMAP.md`
- `TASKS.md`
- `PROMPTS.md`
- `REVIEW.md`
- `docs/ADR/*`

Documentation is part of the architecture, not after-the-fact explanation.

## 13. Development Workflow

`Requirement -> Architecture Decision -> Scoped Prompt -> Cline Implementation -> Tests -> Code Review -> Merge`

Every logical module is reviewed before merge. The project is never generated or rewritten in one large AI prompt.

## 14. Cline/Qwen Rules

Cline/Qwen must:

- read the task-specified engineering documents before changes;
- never redesign the architecture;
- never introduce frameworks/providers without approval;
- never move responsibility across layers without approval;
- never bypass contracts/providers;
- never instantiate provider SDKs in application business logic;
- modify only task-authorized files;
- keep each implementation prompt to one logical scope;
- add/update tests required by the task;
- report assumptions or blockers rather than silently broadening scope.

## 15. Roles

### Principal AI Architect / Senior Engineer

Owns architecture, engineering decisions, code reviews, refactoring plans, implementation prompts, roadmap coherence, and engineering documentation quality.

### Implementation Engineer — Cline / Local Qwen

Implements/refactors scoped modules, writes tests and task-specific documentation, fixes approved defects, and does not redesign architecture.

### Project Owner — Dhanush Reddy

Owns product direction and final decision authority.

## 16. Current Status

- Repository baseline audit: complete enough to establish the accepted architecture and implementation gap map.
- `PROJECT_VISION.md`: ACCEPTED v1.2.
- `ARCHITECTURE.md`: ACCEPTED v1.3.
- Initial ADR set: complete for the currently decidable architecture. ADR-001 through ADR-008 are ACCEPTED; ADR-009 through ADR-011 explicitly defer authentication/trust mechanism, telemetry-stack selection, and deployment/runtime topology until their production decision inputs exist.
- Engineering standards: `CODE_STYLE.md`, `CONTRIBUTING.md`, `TESTING.md`, `SECURITY.md`, `API_GUIDELINES.md`, and `OBSERVABILITY.md` are ACCEPTED v1.0.
- Implementation entry: ACCEPTED by the project owner on 2026-08-07 for Phase 1 Runtime Foundation Hardening.
- Authorized first implementation scope: FND-001 configuration/startup validation only; CL-001 is the only executable Cline prompt.
- Subsequent prompts/tasks remain blocked until FND-001 implementation, tests, and senior-engineer diff review are accepted.

## 17. Long-Term Goal

Build an enterprise-grade AI Platform for Real Estate whose first production capability is Agentic RAG, whose architecture supports future AI products without significant redesign, and whose engineering quality is suitable for professional teams and worldwide production operation.
