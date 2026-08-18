# ADR-018 — AI Evaluation and Release Gates

**Status:** PROPOSED
**Date:** 2026-08-18

## Context

A system can produce a plausible answer while retrieving the wrong source, routing a dynamic question to RAG or leaking restricted information. Endpoint success is not evidence of AI correctness.

## Decision

Create a versioned evaluation dataset that grows to 300–500 representative questions before V1 release.

Cases cover basic product knowledge, cross-module questions, ambiguity, multilingual/country scenarios, dynamic-state routing, permissions/privacy, hallucination traps, negative/zero-answer behavior, conflicts and citations.

Each golden case may define expected route, required/forbidden sources, must-include and must-not-include concepts, allowed fallback and authorization context.

Track retrieval precision/recall, reranking quality, route accuracy, groundedness, hallucination rate, citation accuracy, permission leakage and latency.

Critical release gates:

- permission leakage = 0;
- fabricated inventory = 0;
- fabricated payment state = 0;
- fabricated current legal/compliance state = 0;
- dynamic-state questions do not use static RAG as current truth.

Other numeric thresholds are ratified after a trustworthy baseline and cannot be weakened merely to pass a release.

## Consequences

- evaluation fixtures begin during parser/retrieval development rather than at the end;
- routing and authorization regressions block releases;
- model/provider changes require evaluation comparison;
- performance targets cannot override security and grounding correctness.
