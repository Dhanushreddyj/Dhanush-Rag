# ADR-013 — Knowledge Classification and Query Routing

**Status:** ACCEPTED
**Date:** 2026-08-18

## Context

Static product semantics and current domain state have different authorities. Sending every question directly to vector retrieval can produce stale or fabricated property, price, payment, compliance or user-state answers.

## Decision

Every request is classified before retrieval or tool execution into one source class:

- STATIC_KNOWLEDGE;
- DYNAMIC_DOMAIN_DATA;
- MODEL_OUTPUT;
- TRANSACTIONAL_STATE.

The application owns provider-neutral route and intent models. Routes identify RAG or a live/model/action domain such as property, inventory, pricing, Rate AI, market intelligence, lead, booking, payment, compliance, location, FX, user profile, recommendation or transaction tool.

RAG may explain what a state means. Only an authoritative live service may state what is true now. Model output is labeled as estimate/prediction/recommendation. Actions require an authorized transactional tool.

If a required live source is unavailable, return CURRENT_STATE_UNAVAILABLE. If grounding is insufficient, return UNKNOWN/insufficient context. Static RAG must not substitute.

Routing policy is independently testable. LangGraph may orchestrate routes later but does not own classification rules.

## Consequences

- router evaluation is as important as answer evaluation;
- intent/entity registries become V1 application capabilities;
- live API contracts are required inputs for full integration;
- prompt and response contracts must preserve fact/estimate/prediction/recommendation distinctions.
