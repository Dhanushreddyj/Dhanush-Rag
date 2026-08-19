# ADR-017 — Source Precedence, Grounding and Conflict Handling

**Status:** ACCEPTED
**Date:** 2026-08-18

## Context

Multiple sources may disagree. Combining them into an invented compromise or allowing marketing text to outrank authoritative live services creates unsafe answers.

## Decision

Each domain defines explicit source precedence. Representative orderings include authoritative inventory/payment/property/compliance services before verified partner/manual sources, brochures, screenshots, marketing text or user claims.

Canonical RAG explains stable semantics. Live services override RAG for current state. Active canonical versions outrank superseded/archived knowledge.

The Context Builder detects conflicts using source class, canonical status, version, effective time and priority. Unresolved conflicts produce KNOWLEDGE_CONFLICT_DETECTED and are not merged into a synthetic claim.

The Response Builder preserves internal document/chunk citations. Retrieved content is treated as data, not executable instructions. Unsupported answers return UNKNOWN; missing live state returns CURRENT_STATE_UNAVAILABLE. UNKNOWN must never be converted to zero.

## Consequences

- source precedence becomes domain configuration with tests;
- citation traceability is mandatory even when user-facing citations are optional;
- prompt injection from documents/listings cannot override system policy;
- fabricated property, price, inventory, developer, payment, ROI, legal or scarcity claims are release-blocking defects.
