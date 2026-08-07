# ADR-011 — Production Deployment and Runtime Topology

**Status:** DEFERRED  
**Date:** 2026-08-07  
**Decision Owner:** Dhanush Reddy  
**Architecture:** Enterprise AI Platform for Real Estate  
**Applies To:** Production hosting, process/runtime topology, scaling, networking, and regional deployment

## Context

The Python AI service is an independently deployable microservice consumed by the existing Next.js backend. It uses production AWS Bedrock LLM/embedding providers and Qdrant, but those provider choices do not by themselves determine where or how the Python service must run.

Production hosting requirements such as traffic volume, concurrency, regions, availability targets, disaster recovery, network topology, latency, cost, organizational cloud standards, and operational ownership are not yet approved. Selecting containers, serverless, Kubernetes, a particular AWS compute service, or another platform now would be speculative.

The application architecture nevertheless must avoid implementation choices that would prevent safe multi-worker/multi-instance deployment later.

## Decision

**The concrete production deployment/runtime platform and topology are deferred until operational requirements are known. The service must remain deployable as an independently scalable Python backend without correctness depending on one process or developer machine.**

Until the platform is selected:

- the Python AI service remains independently deployable behind the existing Next.js backend;
- application correctness must not depend on mutable module-level state that exists only inside one process;
- production session/cache/rate-limit state requiring shared semantics must use explicitly selected shared designs rather than accidental process globals;
- provider endpoints/credentials/configuration are externally configured;
- production execution must not depend on the development Mac or PC/LM Studio topology;
- startup/shutdown must support owned resource lifecycle and graceful termination;
- liveness/readiness must be distinguishable for deployment health management;
- the runtime must preserve async I/O and SSE streaming behavior through the chosen ingress/proxy path;
- horizontal scaling must remain possible where operational requirements justify it;
- local filesystem state must not become an undeclared production source of truth;
- deployment-specific SDKs or environment assumptions must not leak into application services;
- a concrete hosting/orchestration platform must not be added to architecture merely because the repository contains a container file or a provider runs on AWS.

## Decision Trigger

Promote this ADR when the following are known:

1. expected request volume, concurrency, and streaming connection profile;
2. availability/SLO and disaster-recovery objectives;
3. target regions and data-residency constraints;
4. Next.js backend deployment/network topology;
5. Qdrant production hosting/network topology;
6. AWS Bedrock region/model availability requirements;
7. organizational cloud/runtime standards and operational ownership;
8. autoscaling, cost, observability, secrets, and deployment-pipeline requirements.

## Options to Evaluate Later

Container orchestration, managed container services, serverless/container runtimes, or other approved compute platforms may be evaluated when requirements are known. Their presence in this list is not approval.

## Consequences

### Positive

- avoids locking production hosting before operational requirements exist;
- keeps application architecture portable across plausible runtime topologies;
- prevents local-development topology from becoming a production dependency;
- makes auth, telemetry, persistence, and streaming infrastructure decisions depend on real deployment facts.

### Tradeoffs

- final production capacity/scaling design remains open;
- authentication and telemetry ADRs cannot be fully promoted until topology is clearer;
- production runbooks and infrastructure-as-code are intentionally deferred.

## Implementation Impact

This ADR authorizes **no production deployment-platform implementation**. Development tooling/container files may exist, but they must not be presented as the accepted production topology.

Application hardening may still enforce platform-independent invariants such as graceful lifecycle, async correctness, provider configuration, health/readiness separation, and avoidance of correctness-sensitive process globals.

## Relationship to Other Decisions

- **ADR-005:** production provider selection does not determine the Python compute platform.
- **ADR-007:** production session persistence selection depends on required cross-instance/durability semantics.
- **ADR-008:** the selected topology must preserve SSE streaming behavior.
- **ADR-009:** production service-to-service trust depends on network/runtime topology.
- **ADR-010:** telemetry-stack selection should align with the production runtime/operations environment.
- **ARCHITECTURE.md Section 32:** defines deployment/scaling invariants constrained here.

## Supersession

When production operational requirements are known, this ADR must be promoted/replaced with an ACCEPTED topology decision including compute/runtime, ingress/networking, scaling, regional strategy, health/lifecycle, secrets/configuration, and failure-domain consequences.
