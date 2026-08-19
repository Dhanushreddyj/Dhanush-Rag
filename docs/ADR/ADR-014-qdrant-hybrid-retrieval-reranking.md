# ADR-014 — Qdrant Hybrid Retrieval and Reranking

**Status:** ACCEPTED
**Date:** 2026-08-18
**Related:** ADR-001, ADR-006

## Context

Nofeez contains exact product terms and semantic concepts. Dense-only retrieval is insufficient. The source instruction includes OpenSearch examples conditionally, while ADR-001 already selects Qdrant as the sole V1 vector database.

## Decision

Qdrant remains the sole V1 vector database. V1 retrieval combines:

- dense semantic retrieval;
- sparse/keyword retrieval supported through the Qdrant adapter;
- provider-neutral metadata filtering;
- reranking;
- context selection and confidence gating.

The Retriever—not the Qdrant provider—owns candidate counts, fusion, reranking, thresholds, query expansion and final context selection.

The normal target is 20–30 bounded candidates and 5–10 reranked context chunks, configurable and tuned from evaluation data. Thresholds are not permanent guessed constants.

Index compatibility includes dense/sparse model identity, dimensions, distance/fusion configuration, payload schema, chunker/parser versions and collection version.

## Consequences

- FND-006 and retrieval contracts must support dense and sparse semantics;
- a reranker implementation is mandatory before V1 completion;
- changing embedding or sparse models may require a new collection version;
- OpenSearch is not added without an explicit superseding ADR.
