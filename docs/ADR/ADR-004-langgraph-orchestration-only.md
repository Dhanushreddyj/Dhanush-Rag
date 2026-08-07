# ADR-004 — Limit LangGraph to Agent Orchestration

**Status:** ACCEPTED  
**Date:** 2026-08-07  
**Decision Owner:** Dhanush Reddy  
**Architecture:** Enterprise AI Platform for Real Estate  
**Applies To:** V1 Agentic RAG and future agent workflows

## Context

The platform needs agent orchestration for workflows that require explicit state transitions, tool invocation, conditional routing, and future planning behavior. LangGraph is the approved agent framework, but the platform is not architected around LangGraph itself.

Without a strict boundary, graph nodes can easily become containers for retrieval algorithms, prompts, provider SDK calls, persistence, response formatting, and business decisions. That would make LangGraph the de facto application layer and couple otherwise reusable capabilities to one orchestration framework.

The architecture instead treats agent orchestration as a consumer/coordinator of application capabilities that are independently defined, tested, and usable without LangGraph.

## Decision

**LangGraph is used for agent orchestration only. It does not own application/business logic or infrastructure integration.**

For V1 and future agent workflows:

- graph nodes coordinate approved application operations, services, or registered tools;
- retrieval policy remains owned by the Retriever pipeline;
- prompt construction remains owned by Prompt Builder;
- response and citation assembly remain owned by Response Builder;
- session/memory policy remains owned by Session Manager;
- provider SDK calls remain inside provider adapters;
- persistence behavior remains behind repositories/provider boundaries;
- HTTP/FastAPI concerns remain outside LangGraph;
- graph state uses platform-owned typed state/contracts and must not expose vendor SDK response objects;
- graph nodes do not construct LLM, embedding, Qdrant, or other infrastructure clients;
- LangGraph does not become a service locator or dependency-injection container;
- application capabilities must be independently testable without executing a LangGraph graph;
- graph-level routing/retry behavior coordinates operations but must not duplicate provider-level resilience policy;
- LangGraph checkpointing mechanisms, if introduced, do not automatically become the platform's session-memory policy or persistence contract;
- the exact V1 graph shape is introduced only after the underlying retrieval, prompt, response, provider, and session contracts are reliable.

Material changes to graph state semantics, planning architecture, long-running workflow durability, or cross-capability orchestration may require a later ADR when those requirements are promoted.

## Rationale

### Framework Containment

Limiting LangGraph to orchestration prevents framework-specific concepts from spreading through application services and future real-estate AI capabilities.

### Independent Capability Testing

Retriever, Prompt Builder, Response Builder, Session Manager, tools, and application services can be tested directly. Agent tests then focus on routing and state-transition correctness rather than re-testing every underlying capability through a graph.

### Replaceable Orchestration Boundary

LangGraph is an approved technology, but core application behavior should not require a graph runtime to exist. This keeps the architecture stable if orchestration requirements evolve.

### Clear Failure Ownership

Provider failures, retrieval failures, validation failures, and orchestration decisions remain distinguishable. A graph does not hide every failure behind a generic node exception.

## Alternatives Considered

### Put the Entire RAG Pipeline Inside LangGraph Nodes — Rejected

This would make orchestration own prompts, retrieval, provider access, and response construction, violating the approved module ownership model and reducing independent testability.

### Use LangGraph as Dependency Container or Service Locator — Rejected

Dependency construction belongs to composition/bootstrap. Graph state and runtime context are not substitutes for explicit dependency injection.

### Let LangGraph Own Session Memory — Rejected

Conversation/session policy is an application concern owned by Session Manager. Framework checkpointing may later support persistence mechanics, but it cannot define memory semantics implicitly.

### No Agent Framework — Rejected

LangGraph is already approved for orchestration and provides a controlled basis for V1 Agentic RAG and future workflow complexity. The decision is to constrain its responsibility, not remove it.

## Consequences

### Positive

- orchestration remains separated from application logic;
- capabilities are independently reusable and testable;
- provider/framework leakage is reduced;
- graph tests can focus on routing and state behavior;
- future tools and capabilities have clear ownership before graph exposure;
- LangGraph cannot silently become the platform architecture.

### Tradeoffs

- orchestration nodes may be intentionally thin and delegate most work;
- explicit application contracts are required before graph integration;
- some convenience state/checkpoint features cannot be adopted without checking ownership boundaries;
- graph introduction happens later than the underlying capability implementations.

## Implementation Impact

This ADR performs **no implementation change** and does not authorize creation of the V1 graph yet.

When LangGraph implementation is promoted, scoped tasks must ensure that:

1. underlying application capabilities are stable and tested first;
2. graph nodes delegate to application operations/tools;
3. graph state is typed and platform-owned;
4. provider SDKs and FastAPI objects are absent from graph state/nodes;
5. Prompt Builder, Retriever, Response Builder, and Session Manager retain their ownership;
6. graph routing has dedicated tests;
7. retry/failure behavior does not duplicate or bypass provider/application resilience policy;
8. graph structure is recorded in an additional ADR if it becomes an architectural contract.

## Verification

- Can each application capability run and be tested without LangGraph?
- Are graph nodes coordinating rather than implementing capability internals?
- Is graph state free of concrete provider SDK types?
- Does Session Manager still own memory semantics?
- Does composition/bootstrap still own dependency construction?
- Are provider retries and application errors distinguishable from orchestration routing?

Failure on these checks is an architecture violation unless superseded by a later accepted ADR.

## Relationship to Other Decisions

- **ADR-002:** provider selection remains composition-owned and provider access remains behind contracts.
- **ADR-003:** FastAPI remains the external delivery boundary; LangGraph does not expose transport concerns directly.
- **ARCHITECTURE.md Section 20:** defines the LangGraph/agent boundary formalized here.

## Supersession

This ADR has no predecessor and supersedes no accepted ADR. A decision to move application ownership into an orchestration framework requires a superseding architecture review.
