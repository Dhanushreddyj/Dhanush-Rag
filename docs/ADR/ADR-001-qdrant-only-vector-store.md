# ADR-001 — Use Qdrant as the Sole V1 Vector Store

**Status:** ACCEPTED  
**Date:** 2026-08-06  
**Decision Owner:** Dhanush Reddy  
**Architecture:** Enterprise AI Platform for Real Estate  
**Applies To:** V1 development and production environments

## Context

The initial architecture allowed ChromaDB for development and Qdrant for production. The project owner has decided to start with Qdrant and not use ChromaDB.

Maintaining different vector-store technologies across development and production creates additional configuration paths, adapter code, contract-parity testing, debugging differences, and opportunities for behavior to diverge between environments.

The platform still requires a vector-store abstraction because application/retrieval logic must not depend directly on Qdrant SDK types or persistence mechanics. Provider independence and dependency inversion remain architectural principles even when only one concrete vector-store implementation is active.

## Decision

**Qdrant is the only approved V1 vector store for both development and production.**

For V1:

- development uses Qdrant;
- production uses Qdrant;
- ChromaDB is not an approved runtime dependency;
- no ChromaDB adapter is maintained for development parity;
- application and retrieval layers continue to depend on platform-defined vector-store/repository contracts;
- Qdrant SDK usage remains confined to the infrastructure/provider boundary;
- vector-store selection is not broadened to additional implementations without a new accepted architectural decision.

Existing Chroma-related code in the audited repository is legacy relative to this decision. It should be removed through a scoped implementation-hardening task with appropriate tests rather than through an unrelated bulk rewrite.

## Rationale

### Development/Production Parity

Using Qdrant in both environments reduces the risk that retrieval, filtering, payload, scoring, collection, or indexing behavior works differently during development than it does in production.

### Lower Maintenance Surface

The team does not need to maintain two vector-store SDK integrations, two sets of configuration, two adapter contract suites, and two operational debugging paths for V1.

### Better Focus

V1 engineering effort can be spent making one Qdrant integration correct, observable, tested, and production-ready instead of maintaining an unused development alternative.

### Architecture Remains Decoupled

Choosing one implementation does not justify coupling business logic to Qdrant. The abstraction remains because it defines responsibility, improves testability, prevents SDK leakage, and preserves a controlled migration boundary if future requirements genuinely demand a different store.

## Alternatives Considered

### ChromaDB for Development, Qdrant for Production — Rejected

This was the previously documented strategy. It provides simple local setup but introduces environment drift and a second implementation that the project owner does not intend to use.

### Direct Qdrant Usage Without a Platform Abstraction — Rejected

This would reduce a small amount of adapter code but violate the project's dependency rules, make application tests more infrastructure-dependent, leak persistence semantics into higher layers, and make a future migration significantly more invasive.

### Support Multiple Vector Stores in V1 — Rejected

There is no approved V1 product requirement that justifies the complexity. Future vector stores may be evaluated through a new ADR when a concrete need exists.

## Consequences

### Positive

- closer development/production parity;
- smaller dependency and configuration surface;
- fewer provider contract variants to test;
- clearer operational knowledge;
- more focused Qdrant performance and reliability work;
- reduced architectural drift between local and production retrieval behavior.

### Tradeoffs

- local development requires access to a Qdrant instance;
- Qdrant-specific operational knowledge is required earlier;
- a future vector-store change still requires a new adapter, migration plan, compatibility testing, and an ADR.

## Implementation Impact

This ADR does not itself perform application-code cleanup. The implementation backlog must include a scoped task to:

1. remove ChromaDB dependencies from the approved V1 dependency set;
2. remove Chroma-specific provider/configuration paths;
3. make Qdrant the validated development and production configuration;
4. correct and harden the existing Qdrant provider implementation;
5. establish Qdrant contract/integration tests;
6. document local Qdrant setup without hard-coding a developer machine topology;
7. verify ingestion, filtering, retrieval, collection compatibility, and deletion semantics against the approved provider contract.

## Compatibility and Migration

Embedding model, vector dimension, distance metric, payload schema, chunking policy, and collection/index version remain compatibility-sensitive. Moving from legacy development data to the accepted Qdrant path may require re-ingestion/re-indexing; no automatic compatibility with a Chroma index is assumed.

## Enforcement

Future Cline/Qwen prompts must not add or preserve ChromaDB as an active V1 implementation path. Any proposal to introduce ChromaDB or another vector-store implementation requires an explicit new requirement and architecture review.

## Related Documents

- MASTER_CONTEXT.md
- PROJECT_VISION.md
- ARCHITECTURE.md
- future TESTING.md
- future CONTRIBUTING.md

