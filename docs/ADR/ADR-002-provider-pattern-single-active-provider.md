# ADR-002 — Provider Pattern and Single-Active-Provider Selection

**Status:** ACCEPTED  
**Date:** 2026-08-07  
**Decision Owner:** Dhanush Reddy  
**Architecture:** Enterprise AI Platform for Real Estate  
**Applies To:** LLM, embedding, vector-store, and future external-capability providers

## Context

The Python AI service must support different infrastructure in development and production without allowing application behavior to depend on a concrete vendor SDK.

The currently approved provider direction intentionally differs by environment for some capabilities: development uses local Qwen 3.6 through LM Studio's OpenAI-compatible endpoint for the LLM capability, while production uses AWS Bedrock models for LLM and embedding capabilities. Qdrant is the sole V1 vector store under ADR-001. The development embedding implementation remains configuration-driven by the current development configuration.

Without an explicit provider-selection rule, the codebase could drift toward direct SDK imports, hidden fallback behavior, runtime service-location, multi-provider fan-out, or vendor-specific branches inside application services. Those patterns would increase coupling and make behavior, testing, failure handling, and operations harder to reason about.

The platform therefore needs both a stable provider abstraction and an explicit rule for how concrete implementations become active.

## Decision

**External AI and infrastructure capabilities are accessed through platform-owned provider contracts, and exactly one concrete implementation per provider capability is active in a service runtime unless a future ADR explicitly approves routing or fan-out.**

For V1:

- application services depend on platform-owned contracts/interfaces rather than concrete provider implementations;
- provider implementations adapt external SDKs/protocols to platform-owned request, result, error, and streaming semantics;
- concrete provider selection occurs only in the composition/bootstrap boundary using validated configuration;
- one configured LLM Provider implementation is active at a time;
- one configured Embedding Provider implementation is active at a time;
- Qdrant is the sole active V1 Vector Store Provider implementation, consistent with ADR-001;
- "single active" is evaluated **per provider capability** and does not require the LLM, embeddings, and vector store to come from the same vendor;
- application services must not branch on provider names, model vendors, SDK types, or environment-specific provider choices;
- provider-specific SDK objects must be translated at the provider boundary before results enter application/business logic;
- provider implementations do not own prompts, retrieval policy, response formatting, session policy, or other application decisions;
- runtime multi-provider fan-out, automatic cross-provider failover, dynamic model routing, and per-request provider switching are not V1 capabilities;
- adding another supported provider does not authorize provider selection outside the composition boundary;
- a future requirement for dynamic routing, fallback across vendors, ensembles, or simultaneous providers requires explicit architecture review and, when material, a new ADR.

Configuration determines which approved implementation is selected. Configuration does not change dependency direction or permit business logic to become vendor-aware.

## Rationale

### Stable Application Boundary

Provider contracts keep application services focused on capability semantics rather than SDK mechanics. Development and production implementations can differ without forcing provider-specific branches into the RAG service or future AI capabilities.

### Deterministic Runtime Behavior

One active implementation per capability makes it clear which external system owns a request, which configuration applies, and which failure/latency metrics are relevant. This is easier to test and operate than implicit routing or hidden fallback.

### Controlled Extensibility

Future providers can be introduced as adapters behind an existing contract when a real requirement exists. The architecture remains extensible without carrying speculative provider implementations or routing infrastructure in V1.

### Testability

Application services can be tested using fakes or mocks that satisfy platform contracts. Tests do not need a live provider SDK merely to verify application orchestration.

### Provider Leakage Prevention

Keeping concrete SDK objects and vendor branching at the infrastructure/composition boundary prevents an external provider from becoming the de facto application architecture.

## Alternatives Considered

### Direct Provider SDK Usage in Application Services — Rejected

This reduces adapter code initially but couples business/application behavior to external SDKs, complicates testing, and makes provider changes invasive.

### Runtime Service Locator — Rejected

Allowing application code to ask a global registry or factory for whichever provider it needs hides dependencies and spreads provider-selection concerns throughout the codebase. Dependencies must instead be composed explicitly at controlled boundaries.

### Multiple Active Providers with Dynamic Routing in V1 — Rejected

There is no approved V1 requirement for cost routing, model routing, ensembles, or per-request vendor selection. Adding this now would create unnecessary configuration, observability, error-handling, and testing complexity.

### Automatic Cross-Provider Failover — Rejected for V1

Transparent failover between vendors changes response behavior, operational semantics, cost, data-routing considerations, and evaluation requirements. It must not be introduced as an implementation detail. If required later, it needs an explicit reliability requirement and architecture decision.

### One Vendor for Every Capability — Rejected

The architecture selects one implementation **per capability**, not one universal vendor for the entire platform. LLM, embedding, and vector-store capabilities have different requirements and may use different approved providers while remaining behind stable contracts.

## Consequences

### Positive

- business/application logic remains provider-agnostic;
- development and production can use different approved implementations behind the same contracts;
- dependencies are explicit and testable;
- provider SDK leakage is constrained to infrastructure adapters;
- runtime behavior and operational ownership are easier to reason about;
- future provider additions have a controlled extension path;
- V1 avoids speculative multi-provider routing complexity.

### Tradeoffs

- provider contracts and adapters require deliberate maintenance;
- provider-specific capabilities cannot leak directly into application services merely because an SDK exposes them;
- changing the active provider requires configuration/composition validation and provider contract testing;
- a future multi-provider routing or failover requirement will need additional architecture rather than being enabled implicitly.

## Implementation Impact

This ADR records an architecture rule. It does **not** authorize a broad provider-layer rewrite and performs no implementation change by itself.

Subsequent scoped implementation tasks must ensure that:

1. application services consume provider contracts rather than concrete SDK classes;
2. provider selection is centralized in composition/bootstrap code;
3. configuration validates supported provider selections before runtime work begins;
4. exactly one LLM and one embedding implementation are composed for a runtime;
5. Qdrant remains the sole V1 vector-store implementation under ADR-001;
6. concrete provider response/error types are translated at the provider boundary;
7. tests verify provider-contract behavior without requiring application logic to know provider names;
8. no automatic provider fallback or routing is added without a new approved requirement/decision.

Implementation cleanup must be split into reviewable module-scoped tasks according to the project's Cline workflow.

## Verification

Architecture and code reviews should be able to answer all of the following:

- Can application services run against a test double without importing a concrete provider SDK?
- Is concrete provider selection confined to configuration/composition?
- Is there exactly one active implementation for each configured provider capability?
- Are provider-specific objects translated before crossing into application logic?
- Can development and production provider choices change without editing business/application services?
- Has any routing, fan-out, or fallback behavior been introduced without an explicit architecture decision?

Failure on any of these checks is an architecture violation unless superseded by a later accepted ADR.

## Relationship to Other Decisions

- **ADR-001 — Use Qdrant as the Sole V1 Vector Store:** narrows the V1 Vector Store Provider implementation to Qdrant while preserving the provider boundary.
- **ARCHITECTURE.md Sections 9–10:** define dependency injection/composition and provider responsibilities that this ADR formalizes.
- The approved development/production model currently uses local Qwen 3.6 through LM Studio for the development LLM and AWS Bedrock models for production LLM/embeddings. Those are configuration-selected implementations, not application-layer dependencies.

## Supersession

This ADR has no predecessor and supersedes no accepted ADR.

Any future decision that introduces multiple simultaneous implementations for one provider capability, runtime routing, or automatic cross-provider failover must explicitly reference and supersede or amend the affected parts of this ADR.
