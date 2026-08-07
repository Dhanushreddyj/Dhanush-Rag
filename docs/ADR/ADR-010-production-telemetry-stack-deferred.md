# ADR-010 — Production Telemetry Stack Selection

**Status:** DEFERRED  
**Date:** 2026-08-07  
**Decision Owner:** Dhanush Reddy  
**Architecture:** Enterprise AI Platform for Real Estate  
**Applies To:** Production logging, metrics, tracing, alerting, and telemetry export

## Context

The platform requires production-grade observability: structured logs, metrics, trace/correlation context, health/readiness signals, provider/retrieval latency, streaming outcomes, ingestion outcomes, and sufficient failure diagnostics to operate the AI service safely.

The production deployment platform and organizational telemetry/alerting environment have not been selected. Choosing a telemetry vendor, collector, backend, retention policy, or alerting product before that context is known would create an unnecessary infrastructure commitment.

Observability requirements are architectural; the telemetry vendor is not yet architectural fact.

## Decision

**The production telemetry vendor/stack is deferred. Vendor-neutral observability semantics and privacy requirements are mandatory now.**

Until the stack is selected, the platform must preserve the ability to observe at least:

- request/correlation identity across the Python request lifecycle;
- request count, success/failure, and latency;
- retrieval latency and retrieved/selected chunk counts;
- embedding and vector-store operation latency/failure;
- configured provider/model identity safe for telemetry;
- time to first streamed output and total generation duration;
- provider timeout/retry/failure outcomes;
- streaming completion, failure, and client disconnect;
- ingestion document/chunk success/failure;
- liveness/readiness state and dependency health;
- cache behavior where caching is enabled.

Additional invariants:

- telemetry APIs must not leak a vendor SDK into application/business logic;
- prompts, user queries, retrieved document text, generated content, credentials, and secrets are sensitive and must not be indiscriminately logged;
- correlation identifiers must not be treated as authorization credentials;
- production sampling, retention, redaction, data residency, and alert thresholds require explicit operational policy;
- an implementation task must not select a telemetry vendor merely because an SDK is convenient.

## Decision Trigger

Promote this ADR when the following are known:

1. deployment/runtime platform;
2. organization's existing logging/metrics/tracing standards, if any;
3. incident-response and alerting ownership;
4. telemetry retention and cost constraints;
5. security/privacy/data-residency constraints;
6. required distributed-trace propagation across Next.js and Python.

## Options to Evaluate Later

Managed cloud telemetry, OpenTelemetry-compatible pipelines, dedicated observability vendors, or a combination may be evaluated when requirements are known. Mentioning them here does not approve a product or SDK.

## Consequences

### Positive

- observability semantics can be designed without vendor lock-in;
- sensitive AI data handling rules are explicit early;
- final telemetry selection can align with deployment/organization operations;
- speculative monitoring dependencies are avoided.

### Tradeoffs

- vendor-specific dashboards/alerts cannot be finalized yet;
- production readiness remains incomplete until telemetry export/alerting are selected and tested;
- standards must later map platform metrics/events to the chosen backend.

## Implementation Impact

This ADR authorizes **no production telemetry-vendor integration**. `OBSERVABILITY.md` may define vendor-neutral logging, metric names/semantics, correlation, redaction, and health standards before the final backend is selected.

## Relationship to Other Decisions

- **ADR-008:** streaming telemetry must observe SSE lifecycle without logging sensitive content by default.
- **ADR-011:** production deployment topology is a key input to telemetry-stack selection.
- **ARCHITECTURE.md Section 27:** defines the observability requirements constrained here.

## Supersession

When the production telemetry stack is selected, this ADR must be promoted/replaced with an ACCEPTED decision recording exporters/backends, trace propagation, retention/sampling, redaction, alerting ownership, and operational consequences.
