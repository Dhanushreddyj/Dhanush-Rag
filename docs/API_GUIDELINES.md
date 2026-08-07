# Enterprise AI Platform — API Guidelines

**Status:** ACCEPTED  
**Version:** 1.0  
**Last Updated:** 2026-08-07  
**Applies To:** REST and SSE contracts exposed by the Python AI service to the existing Next.js backend

## 1. Purpose and Boundary

The Python AI service exposes capability-oriented APIs consumed by the existing Next.js backend. Web/mobile clients do not bypass the existing backend to depend directly on Python provider details.

FastAPI is the delivery framework (ADR-003). API controllers translate HTTP and call application use cases; they do not implement retrieval, prompting, provider access, session persistence, citation assembly, or LangGraph decisions.

## 2. General Contract Rules

- JSON is the default request/response representation for non-streaming APIs;
- UTF-8/Unicode is supported end-to-end;
- external contracts use application/product concepts rather than Bedrock, LM Studio/OpenAI-compatible, Qdrant, or other provider SDK types;
- request/response models are explicit and strongly typed;
- optional fields have defined absence/default semantics;
- unknown/invalid inputs are rejected according to the endpoint's compatibility policy rather than silently repurposed;
- internal refactors do not alter API contracts accidentally.

## 3. API Versioning

Version externally consumed capability routes in the URL path using a major API prefix such as `/v1/...`.

Rules:

- backward-compatible additions remain within the same major version;
- incompatible field/semantic/removal changes require explicit migration/version review;
- internal service release version and API major version are separate concepts;
- health/operational probe routes may remain outside capability version prefixes;
- do not create `/v2` merely for internal refactoring or provider changes when the external contract is unchanged.

Migration from current unversioned baseline routes must be a scoped implementation/API-compatibility task; this document does not silently rewrite existing routes.

## 4. Resource and Operation Design

- use nouns/resource/capability semantics where natural;
- use HTTP methods according to operation semantics;
- do not expose provider-specific endpoints such as `/bedrock/query` or `/qdrant/search`;
- retrieval-only APIs expose retrieval capability, not raw Qdrant collection objects;
- ingestion/admin APIs remain clearly distinguishable from read/query APIs;
- destructive/admin operations require explicit authorization and idempotency/concurrency consideration.

## 5. Request Contracts

Every request model defines:

- required fields;
- type/range/length/count bounds;
- optional/default behavior;
- provider-neutral metadata filter shape where applicable;
- session/correlation semantics where applicable.

Do not pass arbitrary provider parameters through generic dictionaries. If the platform intentionally exposes a tunable behavior, model it as an application/API concept with validation.

## 6. Correlation and Request Identity

Every request receives a correlation/request identifier at the API boundary. If an approved caller-supplied identifier is accepted, validate its shape/size; otherwise generate one.

The identifier:

- propagates through application/provider/retrieval/logging/tracing work;
- is returned through the agreed response header/envelope/stream metadata;
- is safe to expose but is **not** an authentication credential;
- must not be used as an unbounded metric label.

Exact header naming should be consistent service-wide and documented with the API implementation.

## 7. Authentication and Authorization

The production mechanism is DEFERRED by ADR-009.

Until promoted, API design must preserve a pre-use-case authentication boundary and verified security context without inventing a production auth header/protocol.

CORS does not satisfy this requirement. Authorization failures must occur before provider/tool work where feasible.

## 8. Response Contracts and Citations

Non-streaming successful responses use stable typed models.

For RAG responses, application-owned response models may include:

- answer/result;
- validated citations/sources;
- safe operation/model metadata when part of the product contract;
- request/correlation identity;
- completion/state metadata.

Citation identifiers derive from persisted/retrieved source/chunk metadata, never solely from model-generated source names.

Provider SDK objects/raw token chunks never appear in API responses.

## 9. Error Envelope

Errors use a stable client-safe envelope conceptually equivalent to:

```json
{
  "error": {
    "code": "RETRIEVAL_FAILED",
    "message": "The request could not be completed.",
    "request_id": "...",
    "details": null
  }
}
```

Rules:

- `code` is stable/machine-readable and provider-neutral;
- `message` is safe for the caller;
- `request_id` supports diagnostics;
- `details` is optional and never contains raw exceptions/secrets/private provider bodies;
- provider exceptions are translated before the controller boundary.

Expected categories include validation, authentication/authorization once selected, configuration/unavailable, provider timeout/unavailable, embedding/vector/retrieval, ingestion, session, tool, and orchestration errors.

## 10. HTTP Status Semantics

Use status codes consistently:

- `2xx` for successful accepted/completed semantics appropriate to the operation;
- `400` for malformed/application-invalid client input when no more specific code applies;
- `401`/`403` after authentication/authorization behavior is defined;
- `404` for absent addressed resources where revealing absence is allowed;
- `409` for applicable state/version/idempotency conflicts;
- `413` for payload bounds where appropriate;
- `422` for schema/semantic validation when following FastAPI's typed validation conventions;
- `429` for enforced rate/abuse limits;
- `5xx` for server/dependency failures, mapped safely.

Do not return HTTP 200 with a hidden error object merely to simplify clients.

## 11. SSE Streaming Contract

ADR-008 selects Server-Sent Events using `Content-Type: text/event-stream`.

V1 defines these platform event categories:

| Event | Purpose |
| --- | --- |
| `start` | establishes request/stream metadata |
| `delta` | incremental generated/application content |
| `citation` | validated citation/source information when emitted incrementally |
| `metadata` | safe non-content operation/completion metadata |
| `error` | terminal client-safe failure after streaming has begun |
| `done` | explicit successful stream completion |

Each `data:` payload is JSON and includes enough version/request/sequence context to be processed deterministically. Exact field schemas are implementation-contract artifacts and must be tested/versioned consistently; provider-native event fields are prohibited.

Rules:

- failures before stream start use normal HTTP error status/envelope;
- after headers/body start, terminal failures use the `error` SSE event then close;
- success emits `done`; connection close alone is not success confirmation;
- sequence ordering must be deterministic for one stream;
- client disconnect/cancellation propagates downstream where supported;
- heartbeat/comment frames carry no application semantics;
- intermediary buffering/caching must not defeat incremental delivery;
- POST streaming is allowed and is consumed by Next.js as an HTTP response stream; browser `EventSource` is not an architectural requirement.

## 12. Idempotency and Mutating Operations

Read-only query/retrieval requests do not require idempotency keys merely because they are HTTP calls.

Ingestion/admin/mutating operations must explicitly define retry/idempotency semantics. Where caller retries could duplicate durable work, use an application-owned idempotency mechanism/key contract appropriate to the operation rather than relying on accidental duplicate tolerance.

Exact idempotency persistence technology is not selected by this standard.

## 13. Filtering, Pagination, and Bounds

- metadata filters have one provider-neutral schema; Qdrant-specific filter objects never cross the API boundary;
- all list/retrieval limits are bounded;
- pagination should use stable semantics appropriate to the resource; do not expose database cursors/SDK objects directly;
- defaults are documented and server-controlled;
- worldwide text is not destructively ASCII-sanitized.

## 14. Timeouts, Cancellation, and Retries

- server/provider timeouts are explicit and operation-appropriate;
- clients receive safe timeout/unavailable errors;
- client disconnect should cancel streaming work where supported;
- automatic retries must respect idempotency and must not duplicate mutations;
- transport retries do not become hidden multi-provider failover (ADR-002).

## 15. Health and Readiness

Operational endpoints distinguish:

- liveness: process can respond;
- readiness: dependencies/configuration required for traffic are usable.

Readiness checks are bounded and do not make expensive model generations on every probe. Responses do not expose credentials/private endpoint configuration.

## 16. Compatibility and Deprecation

Breaking API changes require explicit review, migration plan, and version impact.

Deprecations must define:

- old/new contract;
- migration guidance;
- support/removal timeline when release practices exist;
- tests covering compatibility during the supported window.

Changing LLM/embedding provider, prompt internals, Qdrant implementation, or LangGraph graph does not by itself justify an external breaking API change.

## 17. API Review Checklist

- Is the contract provider-neutral and typed?
- Is version/compatibility impact explicit?
- Are validation bounds defined?
- Are errors stable and safe?
- Are citations application-validated?
- Does SSE follow ADR-008 event/error/completion semantics?
- Is auth left compatible with ADR-009 rather than invented?
- Are provider/SDK objects absent from external contracts?
