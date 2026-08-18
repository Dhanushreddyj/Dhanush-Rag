# ADR-016 — Incremental Indexing and Reconciliation

**Status:** PROPOSED
**Date:** 2026-08-18

## Context

Manual full-corpus reindexing wastes embedding work and allows stale, deleted or superseded chunks to remain searchable. Canonical updates must propagate predictably.

## Decision

The ingestion lifecycle is:

source change -> hash check -> parse -> validate -> semantic diff -> rechunk affected sections -> embed changed chunks -> upsert -> deactivate/remove superseded active chunks.

Use SHA-256 or equivalent hashes for documents, sections and chunks. Unchanged content skips embedding.

Maintain document/version/chunk registry state with ACTIVE, SUPERSEDED, ARCHIVED and DRAFT statuses plus parser, chunker and embedding versions.

A scheduled reconciliation compares canonical sources, registry records and Qdrant indexes. It detects active documents missing from the index, superseded content still retrievable, hash/version mismatches, duplicate IDs, missing metadata, invalid parent references, orphan chunks and deleted sources still indexed.

Safe derived-state discrepancies may be repaired automatically. Source or semantic conflicts require review.

## Consequences

- ingestion needs transactional/idempotent boundaries and explicit failure queues;
- deleted/superseded content is removed from active retrieval without silently deleting history;
- operators need ingestion and reconciliation visibility;
- complexity is O(changed content) for normal updates rather than O(entire corpus).
