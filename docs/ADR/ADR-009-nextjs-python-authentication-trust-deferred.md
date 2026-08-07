# ADR-009 — Next.js-to-Python Authentication and Trust Mechanism

**Status:** DEFERRED  
**Date:** 2026-08-07  
**Decision Owner:** Dhanush Reddy  
**Architecture:** Enterprise AI Platform for Real Estate  
**Applies To:** Service-to-service trust between the existing Next.js backend and Python AI service

## Context

The Python AI service is a protected backend service consumed by the existing Next.js backend. Its AI, retrieval, ingestion, session, and future tool endpoints must not become implicitly public simply because they are exposed through HTTP.

The correct concrete trust mechanism depends materially on the final deployment/runtime topology, network boundary, identity platform, secret-management model, tenant/user delegation requirements, and operational ownership. Those decisions are not yet selected.

Choosing a static API key, JWT issuer, mTLS design, AWS-native request signing/identity, gateway authentication, or another mechanism before that topology exists would hard-code infrastructure assumptions into the service architecture.

## Decision

**Concrete Next.js-to-Python authentication technology is deferred until production deployment and identity requirements are known. The security boundary itself is not deferred.**

Until the mechanism is selected:

- protected AI endpoints are architected to require authenticated/authorized service access in production;
- authentication/trust validation occurs at the FastAPI/API boundary before expensive AI work begins;
- business/application services consume verified caller/security context rather than parsing transport credentials;
- CORS is never treated as authentication or authorization;
- client-supplied identity, tenant, role, or permission claims are not trusted unless verified by the approved trust mechanism;
- secrets, tokens, signing keys, and credentials are never hard-coded or logged;
- authentication failure must not fall through to anonymous AI/provider execution;
- authorization remains capability-aware, especially for ingestion, admin operations, session access, and future tools;
- end-user/tenant delegation from Next.js, if required, must be distinguished from service identity rather than inferred implicitly;
- implementation tasks must not choose a concrete authentication library/protocol until this ADR is promoted with the required production context.

## Decision Trigger

Promote this ADR from DEFERRED when the following are known:

1. production deployment platform and service network topology;
2. Next.js backend hosting/runtime and its supported workload identity mechanism;
3. whether the Python service is private-network-only, gateway-fronted, or otherwise reachable;
4. whether end-user/tenant identity must be delegated to Python or only service identity is required;
5. key/credential lifecycle and secrets-management ownership;
6. required authorization granularity and audit requirements.

## Options to Evaluate Later

The future decision may evaluate workload identity/IAM, signed short-lived service tokens, mTLS, gateway-issued identity, or another requirements-compatible mechanism. Listing an option here does not approve it.

Static long-lived shared secrets should require strong justification because rotation, leakage, and caller identity are weaker operationally than workload-aware mechanisms.

## Consequences

### Positive

- avoids coupling authentication to an unknown deployment platform;
- preserves a mandatory protected-service boundary;
- prevents Cline or framework defaults from inventing production security;
- leaves room for workload-native identity once topology is known.

### Tradeoffs

- production deployment cannot be declared security-complete until this ADR is promoted;
- integration tests for the final trust mechanism remain blocked on the concrete decision;
- local development must clearly distinguish development bypass/test identities from production trust behavior.

## Implementation Impact

This ADR authorizes **no production authentication implementation**. Architecture may define verified security-context interfaces and authorization boundaries, but a concrete production mechanism must wait for this ADR's decision trigger.

## Relationship to Other Decisions

- **ADR-003:** FastAPI is the API boundary where the approved trust mechanism will be enforced.
- **ADR-011:** deployment/runtime topology is a prerequisite input to the final trust decision.
- **ARCHITECTURE.md Section 26:** defines the security requirements constrained here.

## Supersession

When the production trust mechanism is selected, this ADR must be promoted/replaced with an ACCEPTED decision that records the mechanism, alternatives, credential lifecycle, verification boundary, and operational consequences.
