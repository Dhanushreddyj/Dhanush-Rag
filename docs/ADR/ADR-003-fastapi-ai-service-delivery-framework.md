# ADR-003 — FastAPI as the Python AI Service Delivery Framework

**Status:** ACCEPTED  
**Date:** 2026-08-07  
**Decision Owner:** Dhanush Reddy  
**Architecture:** Enterprise AI Platform for Real Estate  
**Applies To:** HTTP/API delivery boundary of the Python AI microservice

## Context

The worldwide real estate platform already has an existing Next.js backend, web application, and mobile application. This repository owns only the independently deployable Python AI service. The existing Next.js backend consumes the Python service through an API boundary; the Python service does not replace or absorb the existing backend.

The AI platform needs an HTTP delivery framework that supports typed request/response contracts, asynchronous I/O, streaming, dependency injection integration, lifecycle management, middleware, health endpoints, and generated API documentation without becoming the location of application or AI business logic.

FastAPI is already the approved framework in the project architecture and current repository baseline. This ADR formalizes its responsibility boundary so future contributors do not gradually turn FastAPI controllers, dependencies, middleware, or lifecycle hooks into application services.

## Decision

**FastAPI is the approved HTTP/API delivery framework for the Python AI service.**

FastAPI is an outer delivery-layer dependency. It owns HTTP concerns and translates between transport contracts and application operations.

For V1:

- FastAPI exposes the Python AI service's REST/API surface consumed by the existing Next.js backend;
- controllers/routes remain thin and delegate use-case execution to application services;
- FastAPI/Pydantic performs transport-level request parsing, shape/type validation, and response serialization;
- application-specific validation and use-case decisions remain outside controllers;
- dependency injection exposes already-composed application dependencies to routes rather than constructing provider SDK clients inside controllers;
- authentication/trust enforcement occurs at the API boundary once the concrete Next.js-to-Python mechanism is accepted by its dedicated ADR;
- middleware owns cross-cutting HTTP behavior only, such as correlation propagation and approved request-level concerns;
- FastAPI lifecycle hooks may start/stop composed infrastructure resources but do not own business workflows;
- streaming transport is exposed through the FastAPI delivery boundary while generation/orchestration remains owned by application/provider abstractions;
- controllers may translate typed application errors into safe HTTP responses but must not expose raw provider exceptions, SDK objects, credentials, or stack traces;
- FastAPI-specific request/response objects do not propagate into provider, repository, retrieval, prompt, session, response-building, or domain/capability logic;
- provider SDKs, Qdrant SDK calls, prompt construction, retrieval policy, session policy, response/citation assembly, and LangGraph decision logic are forbidden inside API routes;
- the application core must remain testable without requiring an HTTP server.

The exact endpoint schemas, API versioning rules, streaming wire protocol, error-envelope format, authentication mechanism, and public compatibility policy are governed by `API_GUIDELINES.md` and/or dedicated ADRs as those decisions are accepted. Selecting FastAPI does not pre-decide those mechanisms.

## Rationale

### Clear Service Boundary

FastAPI provides a well-defined delivery layer for the independently deployable Python service while preserving the existing Next.js backend as the product-facing backend boundary.

### Async and Streaming Compatibility

The platform is async-first and requires streaming compatibility from V1. FastAPI supports asynchronous request handling and streaming delivery without requiring the application core to depend on transport primitives.

### Typed Transport Contracts

FastAPI and Pydantic provide explicit validation and serialization at the HTTP boundary. Internal application contracts remain platform-owned and are not defined by vendor SDK response objects.

### Thin-Controller Enforcement

Treating FastAPI strictly as a delivery framework keeps retrieval, prompting, provider access, orchestration, and persistence responsibilities in their approved modules.

### Operational Fit

FastAPI provides standard lifecycle, middleware, health-route, and API-documentation mechanisms suitable for the Python service while leaving production deployment topology and infrastructure choices to separate decisions.

## Alternatives Considered

### Flask — Rejected

Flask could expose the required HTTP endpoints, but the project already has an accepted FastAPI architecture and no requirement justifies changing frameworks. Introducing another delivery framework would create unnecessary migration and consistency cost.

### Django / Django REST Framework — Rejected

The Python AI service does not require Django's broader web-application stack. Adding it would expand the framework surface without an approved capability need and would conflict with the established microservice architecture.

### Expose LangGraph Directly as the Service Boundary — Rejected

LangGraph is approved for agent orchestration only. Making it the external API architecture would blur transport and orchestration responsibilities and violate the platform's layering rules.

### Provider-Specific HTTP Endpoints — Rejected

Exposing Bedrock-, LM-Studio-, OpenAI-compatible-, or Qdrant-shaped routes would leak infrastructure choices into the service contract. External consumers interact with platform capabilities, not provider APIs.

### Move AI API Responsibilities into the Existing Next.js Backend — Rejected

The approved project boundary assigns AI capability implementation to the independent Python service. The Next.js backend remains the consumer/integration boundary and is outside this repository's implementation scope.

## Consequences

### Positive

- one consistent Python HTTP delivery framework;
- clear separation between transport and application logic;
- strong typed request/response handling at the boundary;
- async-first and streaming-compatible delivery;
- application services remain independently testable;
- provider and vector-store SDKs remain outside controllers;
- the existing Next.js backend can integrate through a stable service API rather than provider-specific interfaces.

### Tradeoffs

- contributors must maintain explicit mapping between transport schemas and application contracts where their responsibilities differ;
- FastAPI convenience features must not be used as justification for placing application state or business logic in dependencies/routes;
- framework-specific middleware and lifecycle behavior require their own tests;
- changing the delivery framework later would require an explicit architecture decision and migration plan.

## Implementation Impact

This ADR records the delivery-framework decision and performs **no implementation refactor by itself**.

Subsequent scoped implementation tasks must ensure that:

1. routes/controllers remain thin and call application services;
2. controllers do not call LLM, embedding, vector-store, or other provider SDKs directly;
3. controllers do not perform retrieval, prompt construction, response/citation assembly, or session policy;
4. FastAPI dependencies receive or expose composed application dependencies rather than acting as service locators;
5. HTTP validation is separated from application/business validation;
6. application errors are mapped to safe transport errors at the delivery boundary;
7. streaming remains end-to-end compatible without coupling application services to FastAPI response objects;
8. framework lifecycle code manages resource lifecycle only at the approved composition boundary;
9. API behavior has transport-level tests in addition to application-service tests.

Existing controller/provider leakage identified in the repository audit must be corrected later through bounded implementation tasks, not through this ADR.

## Verification

Architecture and code reviews should be able to answer all of the following:

- Can the application use case be tested without FastAPI or an HTTP server?
- Does each route primarily translate HTTP input/output and delegate application work?
- Are provider SDK imports absent from controllers?
- Are retrieval, prompts, sessions, citations, and agent decisions owned outside FastAPI?
- Are errors translated safely rather than leaking raw infrastructure exceptions?
- Can streaming implementation evolve without moving model-generation logic into the controller?
- Does the service boundary remain Python AI service ↔ existing Next.js backend rather than bypassing that integration model?

Failure on these checks is an architecture violation unless superseded by a later accepted ADR.

## Relationship to Other Decisions

- **ADR-001 — Use Qdrant as the Sole V1 Vector Store:** Qdrant remains behind the provider/infrastructure boundary and must never be accessed directly from FastAPI routes.
- **ADR-002 — Provider Pattern and Single-Active-Provider Selection:** provider selection/composition remains outside controllers; FastAPI consumes application-facing dependencies.
- **ARCHITECTURE.md Sections 7–9 and 22:** define layer responsibilities, dependency direction, composition, and FastAPI controller rules formalized by this ADR.
- The future authentication/trust ADR will define the concrete Next.js-to-Python trust mechanism without changing FastAPI's delivery-layer responsibility.
- The future streaming ADR/API standard will define the external streaming wire protocol without moving generation ownership into FastAPI.

## Supersession

This ADR has no predecessor and supersedes no accepted ADR.

Replacing FastAPI, adding a second Python delivery framework, or materially changing the Python service boundary requires explicit architecture review and a superseding ADR.
