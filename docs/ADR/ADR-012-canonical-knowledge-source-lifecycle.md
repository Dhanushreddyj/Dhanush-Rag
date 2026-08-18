# ADR-012 — Canonical Knowledge Source and Lifecycle

**Status:** PROPOSED
**Date:** 2026-08-18

## Context

Nofeez supplied 110 approved Markdown modules containing stable product and business semantics. They are source records, not disposable upload files. The prior architecture described generic document ingestion and deferred exact identity/version policy.

## Decision

The 110 Markdown modules are the canonical global Nofeez knowledge source.

Each document must provide validated YAML metadata including document ID, title, category, version, language, canonical flag, priority and update/effective dates where applicable. The body is parsed separately by Markdown hierarchy and numbered sections.

Canonical files may be read, validated, indexed, versioned and archived. Automated ingestion must never silently rewrite them.

Every derived chunk retains document ID/version, section identity, source path, status, content hash, parser/chunker/embedding compatibility metadata, indexed timestamp and provenance. Chunk IDs are deterministic for a document version and semantic section.

Normal retrieval includes only canonical ACTIVE versions. Superseded and archived versions remain available only through explicit historical retrieval.

Invalid documents enter a validation queue and are not indexed.

## Consequences

- the repository needs a canonical knowledge directory and document/version registry;
- ingestion becomes semantic and version-aware;
- source changes require controlled Git or approved source updates;
- historical policy questions can be supported later without contaminating normal retrieval;
- PDF/developer extraction remains a separate provenance workflow.

## Alternatives Rejected

- treating vector storage as the source of truth;
- random IDs on every ingestion;
- silently replacing old versions;
- learning global policy from conversations.
