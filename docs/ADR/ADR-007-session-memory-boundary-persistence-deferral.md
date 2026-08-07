# ADR-007 — Session Memory Boundary and Persistence Deferral

**Status:** ACCEPTED  
**Date:** 2026-08-07  
**Decision Owner:** Dhanush Reddy  
**Architecture:** Enterprise AI Platform for Real Estate  
**Applies To:** V1 conversation/session memory semantics and future persistence selection

## Context

V1 requires conversation-scoped session memory while the platform must remain horizontally scalable and independent of any particular storage SDK. The architecture already assigns memory ownership to Session Manager and explicitly excludes persistent long-term user memory from the initial requirement.

The production persistence technology has not been selected. Choosing Redis, a relational database, a LangGraph checkpoint store, or another technology now would be speculative because required durability, cross-instance continuity, retention, recovery, regional, privacy, and latency requirements are not yet approved.

At the same time, leaving ownership undefined would allow controllers, LangGraph state, module globals, or provider implementations to become accidental memory systems.

## Decision

**V1 memory is session-based and conversation-scoped, owned by Session Manager. The persistence technology is intentionally deferred until production persistence semantics are explicitly required.**

For V1:

- Session Manager owns session identity validation, permitted conversation-state retrieval, update policy, context selection, expiry/cleanup policy, and future summary/compression integration;
- application services interact with Session Manager through platform-owned contracts rather than storage SDKs;
- persistent long-term user/profile memory is not part of the V1 requirement;
- LangGraph graph state/checkpointing does not define the platform's memory semantics;
- FastAPI request state and controllers do not own conversation memory;
- LLM/provider implementations do not own or persist conversation state;
- module-level mutable globals must not be treated as a production session store;
- a development-only in-process implementation may exist only when its non-durable, single-process semantics are explicit and do not masquerade as production behavior;
- production multi-worker/multi-instance continuity must not depend on process-local memory;
- no persistent session technology is approved by this ADR;
- before production requires continuity across workers, instances, restarts, regions, or deployment replacements, persistence requirements and the concrete repository/storage strategy must be promoted to a dedicated ADR;
- retention, deletion, privacy, and authorization rules apply to stored conversation state regardless of persistence technology;
- future summarization/compression changes context policy but does not change Session Manager ownership.

This is a deliberate deferral, not permission to select a storage backend inside an implementation task.

## Rationale

### Stable Memory Semantics Before Storage Selection

The application contract can define what session memory means without prematurely coupling the platform to a persistence product.

### Horizontal-Scaling Safety

Explicitly rejecting process-local state as a production assumption prevents behavior that works with one worker but silently loses sessions when multiple instances are introduced.

### LangGraph Containment

Session semantics remain an application concern even if LangGraph later uses checkpointing as an infrastructure mechanism. Framework storage does not automatically become the source of truth.

### Avoid Speculative Infrastructure

Durability and topology requirements determine the appropriate store. Selecting technology before those requirements exist would violate the project's decision discipline.

## Alternatives Considered

### Choose a Production Session Store Immediately — Rejected for Now

No approved durability/topology requirements justify locking a technology today. The choice is deferred until its operational requirements are known.

### Use Module-Level In-Memory State in Production — Rejected

Process-local state is inconsistent across workers/instances and is lost on restart/replacement. It cannot satisfy shared production session semantics.

### Let LangGraph Checkpointing Own Memory — Rejected

Checkpointing is an orchestration/framework mechanism. Session identity, allowed state, retention, and context policy remain application concerns owned by Session Manager.

### Put Conversation State in FastAPI Controllers — Rejected

Transport code must remain stateless with respect to application memory policy and must not become a persistence layer.

### Introduce Persistent Long-Term User Memory in V1 — Rejected

Long-term user memory introduces separate privacy, retention, authorization, deletion, and product semantics that are not part of the approved V1 requirement.

## Consequences

### Positive

- session-memory ownership is unambiguous;
- application code remains independent of persistence technology;
- production scaling cannot silently rely on module globals;
- long-term memory scope remains controlled;
- future storage can be selected from actual durability/topology requirements;
- LangGraph remains orchestration-only.

### Tradeoffs

- production persistence implementation cannot begin until its required semantics are approved;
- development memory may have weaker durability than eventual production memory;
- a later persistence ADR and migration/integration work are expected if production continuity is required.

## Implementation Impact

This ADR performs **no memory implementation and selects no persistence technology**.

Future scoped tasks may define the Session Manager contract and policy without choosing a production store. A production persistence task must not be promoted until the required durability, consistency, retention, topology, and recovery semantics are explicit.

When a persistence implementation is selected, tests must cover session isolation, expiry, concurrency, authorization boundaries, failure behavior, and any cross-instance semantics promised by that implementation.

## Verification

- Does Session Manager remain the sole owner of conversation-memory policy?
- Can application services use session memory without importing a storage SDK?
- Is process-local state clearly excluded from shared production semantics?
- Is LangGraph checkpoint state prevented from silently redefining session policy?
- Is persistent long-term user memory still outside V1 unless separately approved?
- Has any production persistence technology been introduced without a requirements-backed ADR?

## Relationship to Other Decisions

- **ADR-004:** LangGraph is orchestration-only and does not own session-memory semantics.
- **ADR-003:** FastAPI remains a delivery boundary and does not persist conversation state.
- **ARCHITECTURE.md Section 18:** defines the Session Manager ownership formalized here.

## Supersession

This ADR does not select a production persistence backend. A later requirements-backed session-persistence ADR will extend this decision by choosing implementation semantics/technology while preserving Session Manager ownership unless it explicitly supersedes that boundary.
