# ADR-008 — Use Server-Sent Events for External Response Streaming

**Status:** ACCEPTED  
**Date:** 2026-08-07  
**Decision Owner:** Dhanush Reddy  
**Architecture:** Enterprise AI Platform for Real Estate  
**Applies To:** Streaming responses from the Python AI service to the existing Next.js backend

## Context

Streaming is a Day-1 platform requirement. The internal stream is provider-neutral and may include generated text deltas, completion metadata, citations/source information, typed failures, and lifecycle events. The existing Next.js backend—not the browser/mobile client directly—is the approved consumer of the Python AI microservice.

The external transport therefore needs a simple unidirectional HTTP streaming protocol that works with FastAPI and server-to-server HTTP clients, supports typed events beyond raw text tokens, preserves correlation/error/completion semantics, and does not require a bidirectional connection when V1 has no bidirectional streaming requirement.

## Decision

**The Python AI service uses Server-Sent Events (SSE) over HTTP for V1 streaming responses to the Next.js backend.**

The transport uses `Content-Type: text/event-stream`. Event payloads carry platform-owned JSON data; raw provider SDK chunks are never emitted directly.

For V1:

- the request is made through the normal authenticated HTTP API boundary;
- the response is an SSE stream consumed by the Next.js backend as an HTTP streaming response;
- use of SSE does not require the browser `EventSource` API, so streaming endpoints may retain the HTTP method appropriate to the API contract, including POST where the request body contains query/session/filter input;
- the application/provider layers emit provider-neutral stream events and the delivery layer maps them to SSE;
- the event model must distinguish at least stream lifecycle/start, content delta, final metadata/citation information, terminal error, and completion semantics;
- exact event names and JSON payload schemas are versioned in `API_GUIDELINES.md`; transport code must not invent provider-specific event shapes;
- correlation/request identity is preserved for the entire stream;
- failures detected before streaming begins use the normal HTTP status/error contract;
- after streaming headers/body have begun, a recoverable-to-transport terminal failure is represented by a typed SSE error event followed by stream termination rather than pretending the HTTP status can be changed;
- successful streams end with an explicit completion event rather than relying only on TCP connection close;
- client disconnect/cancellation propagates toward application/provider work where supported so abandoned generation does not continue unnecessarily;
- intermediary buffering/caching must be configured so it does not defeat streaming semantics;
- heartbeat/comment frames may be used when operationally required but are not application data;
- sensitive prompts, retrieved text, and generated content are not logged merely because they pass through the stream;
- streaming remains compatible with citations and final metadata rather than exposing text-only token chunks.

This ADR selects the wire protocol. It does not define the exact API route, event JSON schema, authentication mechanism, proxy product, timeout values, or deployment topology.

## Rationale

### Matches the Communication Direction

V1 streaming is primarily server-to-client along one response path. SSE fits that model without introducing bidirectional socket semantics that the requirement does not need.

### Works with Existing HTTP Boundary

SSE remains ordinary HTTP and fits FastAPI plus the existing Next.js-to-Python service boundary. The Next.js backend can consume the response stream without exposing Python-provider details to web/mobile clients.

### Structured Events

Named/typed SSE events with JSON payloads can represent deltas, citations, metadata, errors, and completion more safely than an unstructured text byte stream.

### Operational Simplicity

SSE uses the existing HTTP authentication, correlation, proxy, observability, and connection-management boundary. No separate WebSocket protocol stack is required for V1.

## Alternatives Considered

### Raw Chunked Text Response — Rejected

Raw text chunks are simple but do not provide a strong typed envelope for citations, completion metadata, lifecycle state, or mid-stream errors.

### WebSockets — Rejected for V1

V1 does not require bidirectional real-time messaging between the Next.js backend and Python service during one generation stream. WebSockets would introduce extra connection/session/proxy operational complexity without an approved requirement.

### NDJSON Streaming — Rejected

NDJSON can carry structured events, but SSE provides explicit event-stream semantics, event typing, and heartbeat conventions while remaining an HTTP response stream. There is no V1 requirement that favors NDJSON instead.

### Provider-Native Streaming Format — Rejected

Bedrock, LM Studio/OpenAI-compatible, or future provider event formats must not become the external API contract. Provider chunks are normalized before reaching the transport boundary.

## Consequences

### Positive

- one explicit external streaming protocol;
- structured lifecycle/data/error/completion events;
- compatible with provider-neutral application streaming;
- works within the FastAPI/HTTP service boundary;
- avoids unnecessary WebSocket infrastructure;
- supports citations and final metadata alongside generated text;
- cleanly separates pre-stream HTTP errors from mid-stream terminal errors.

### Tradeoffs

- proxies/load balancers must be configured to preserve long-lived streaming and avoid buffering;
- once the response has started, HTTP status cannot communicate later generation failure;
- the Next.js integration must implement SSE parsing for an HTTP response stream;
- bidirectional workflows would require a later protocol decision if future requirements genuinely need them.

## Implementation Impact

This ADR performs **no streaming implementation change**.

Later scoped tasks and `API_GUIDELINES.md` must define:

1. the versioned stream-event envelope;
2. exact event names and payload schemas;
3. terminal completion/error behavior;
4. correlation propagation;
5. disconnect/cancellation behavior;
6. FastAPI transport mapping from provider-neutral application events;
7. API/integration tests that consume the stream incrementally;
8. proxy/deployment requirements needed to prevent buffering and enforce appropriate timeouts.

No implementation task may expose raw provider streaming objects directly to the Next.js backend.

## Verification

- Is the response `text/event-stream` and parseable incrementally?
- Are stream events platform-owned rather than provider-owned?
- Can citations/metadata/errors be represented without corrupting generated text?
- Is completion explicit?
- Are pre-stream and mid-stream failures handled according to different transport realities?
- Does client cancellation stop downstream work where supported?
- Can the Next.js backend consume the stream without knowing which LLM provider is active?

## Relationship to Other Decisions

- **ADR-003:** FastAPI owns the external HTTP delivery boundary used for SSE.
- **ADR-004:** LangGraph may participate in internal orchestration but does not own the external streaming protocol.
- **ADR-005:** development and production provider streams are normalized behind provider/application contracts before SSE mapping.
- **ARCHITECTURE.md Section 19:** defines the end-to-end streaming requirements formalized by this ADR.

## Supersession

This ADR has no predecessor and supersedes no accepted ADR.

A future requirement for bidirectional streaming, persistent duplex connections, or a non-HTTP streaming transport requires explicit architecture review and an amending/superseding ADR.
