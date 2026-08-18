# ADR-015 — Permission-Aware Knowledge Namespaces and Context Assembly

**Status:** PROPOSED
**Date:** 2026-08-18
**Related:** ADR-009

## Context

Global platform knowledge, developer/project documents and private user/domain data have different visibility. Relying on an LLM instruction not to disclose retrieved secrets is not an authorization control.

## Decision

Knowledge is separated into explicit namespaces, including:

- GLOBAL_NOFEEZ;
- DEVELOPER:{developer_id};
- PROJECT:{project_id};
- USER_PRIVATE:{user_id} or equivalent private service context.

Role, market, tenant, ownership and resource filters are applied before restricted content reaches the LLM.

Private profiles, contact data, search history, saved items, payments, consent, fraud signals, lead data and internal notes are not placed in global RAG. They are retrieved from authorized live/private services and assembled at request time.

The Context Builder keeps canonical RAG, live domain context, model output and private context structurally separate.

ADR-009 still determines the concrete Next.js-to-Python authentication mechanism. This ADR defines application authorization semantics independently.

## Consequences

- Next.js must supply a trusted authorization-context contract;
- retrieval tests require cross-role and cross-tenant negative cases;
- permission leakage is a zero-tolerance release metric;
- project/developer uploads never join global knowledge automatically.
