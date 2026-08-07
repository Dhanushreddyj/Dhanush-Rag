# ADR-005 — Development and Production LLM/Embedding Provider Strategy

**Status:** ACCEPTED  
**Date:** 2026-08-07  
**Decision Owner:** Dhanush Reddy  
**Architecture:** Enterprise AI Platform for Real Estate  
**Applies To:** LLM and embedding provider selection across development and production

## Context

Development and production have different operational requirements. Development must remain practical with the owner's current local inference environment, while production needs an approved managed provider strategy. These environment-specific choices must not change application architecture or introduce vendor branches into business logic.

The current development topology uses a Mac for VS Code/Cline and project workflow, with a PC hosting LM Studio. The PC runs Qwen 3.6 14B A3B FableVibes Q5/Q4 and exposes an OpenAI-compatible network endpoint. Production LLM and embedding capabilities are approved on AWS Bedrock. The development embedding implementation remains whatever is selected by the current development configuration; this ADR intentionally does not invent a permanent development embedding vendor/model.

Provider selection remains governed by ADR-002: configuration/composition selects exactly one implementation per provider capability at a time.

## Decision

**Development and production may use different concrete LLM/embedding providers behind the same platform-owned provider contracts.**

The approved current strategy is:

| Capability | Development | Production |
| --- | --- | --- |
| LLM | Local Qwen 3.6 through LM Studio's OpenAI-compatible endpoint | AWS Bedrock models |
| Embeddings | Current development configuration behind the Embedding Provider contract | AWS Bedrock Embedding Models |
| Vector store | Qdrant under ADR-001 | Qdrant under ADR-001 |

Additional rules:

- provider choice is configuration-driven and composition-owned;
- exactly one LLM implementation and one embedding implementation are active per runtime, consistent with ADR-002;
- application/business logic must not branch on development versus production provider names;
- "OpenAI-compatible" describes the protocol used by the current LM Studio development endpoint; it does **not** make OpenAI the production provider or a permanent architecture dependency;
- application source must not hard-code the LM Studio LAN IP, port, workstation hostname, API key, or local model identifier;
- production AWS region, concrete Bedrock model IDs, credentials/IAM mechanics, and inference parameters are configuration/operational choices unless they materially change an architectural contract;
- production AWS credentials must come from an approved AWS credential/identity mechanism, not application-source constants;
- changing an embedding model must obey ADR-006 embedding/index compatibility rules;
- introducing an additional provider implementation requires a real requirement, contract tests, and controlled configuration; a roadmap mention alone is insufficient;
- this strategy does not authorize dynamic provider routing, fan-out, automatic vendor fallback, or per-request provider switching.

## Rationale

### Practical Local Development

The existing Qwen/LM Studio workstation provides a usable local development path without requiring development requests to consume production LLM capacity.

### Production Provider Approval

AWS Bedrock is the currently approved production provider family for both LLM and embedding capabilities. Application code accesses those capabilities through provider contracts rather than Bedrock-specific business logic.

### Environment Independence

The same application use cases operate against either environment because provider differences are resolved at composition. Environment selection is deployment/configuration, not a separate application architecture.

### No Premature Development Embedding Decision

The architecture does not yet need a permanent development embedding vendor/model. Keeping this configuration-driven avoids creating a false architectural commitment while ADR-006 protects index compatibility.

## Alternatives Considered

### OpenAI as the Permanent Production LLM/Embedding Provider — Rejected

This was present in earlier project assumptions but is no longer the approved production strategy. Production uses AWS Bedrock provider implementations.

### Require AWS Bedrock for All Development — Rejected

This would remove the approved local Qwen/LM Studio development path and unnecessarily couple day-to-day development to production infrastructure.

### Make LM Studio a Production Dependency — Rejected

LM Studio is current development tooling/provider infrastructure. It is not part of the approved production runtime architecture.

### Hard-Code One Development Embedding Model in Architecture — Rejected for Now

No accepted requirement currently justifies making a permanent development embedding model an architectural invariant. The active configuration must still be explicit and compatible with its Qdrant index.

### Multi-Provider Runtime Routing — Rejected for V1

ADR-002 defines single-active-provider selection per capability. Runtime routing/failover requires a separate future decision if a concrete requirement emerges.

## Consequences

### Positive

- local development remains practical on the current hardware;
- production provider direction is explicit;
- business logic remains provider-agnostic;
- OpenAI-compatible protocol use is not confused with OpenAI production coupling;
- provider/model configuration can evolve within controlled contracts;
- environment parity is enforced at application contracts rather than requiring identical vendors.

### Tradeoffs

- development and production provider adapters require contract-parity testing;
- model behavior and quality may differ across environments;
- production validation must include Bedrock-specific integration/evaluation testing;
- development embedding configuration must be explicitly tracked with its Qdrant index compatibility metadata.

## Implementation Impact

This ADR performs **no provider implementation work**.

Later scoped tasks must ensure that:

1. development LLM endpoint/model settings are environment-configured;
2. production LLM/embedding adapters use AWS Bedrock behind platform contracts;
3. provider selection is validated at composition/startup;
4. application services contain no OpenAI-, Bedrock-, LM-Studio-, or Qwen-specific branches;
5. only one implementation per provider capability is composed at a time;
6. provider contract tests cover the semantics required by application services;
7. embedding changes follow ADR-006;
8. secrets and credentials are never hard-coded.

## Verification

- Can the development LLM endpoint change without editing application services?
- Can production use Bedrock without application code importing Bedrock SDK types?
- Does OpenAI-compatible wording appear only as a protocol/provider-adapter detail where applicable?
- Is the development embedding choice configuration-driven rather than treated as a permanent vendor invariant?
- Is one implementation active per capability?
- Are model/provider changes evaluated against contract and index-compatibility requirements?

## Relationship to Other Decisions

- **ADR-001:** Qdrant is the sole V1 vector store in development and production.
- **ADR-002:** provider selection is configuration/composition-owned with one active implementation per capability.
- **ADR-006:** embedding/index compatibility governs model changes and Qdrant re-indexing.
- **ARCHITECTURE.md Sections 6 and 10:** define the environment topology and provider architecture formalized here.

## Supersession

This ADR replaces earlier informal assumptions that OpenAI is the permanent production LLM/embedding provider. It does not supersede ADR-001 or ADR-002.

A future change to the approved production provider family or the single-active-provider strategy requires explicit architecture review and an ADR update/supersession as appropriate.
