# Enterprise AI Platform — Security Standard

**Status:** ACCEPTED  
**Version:** 1.0  
**Last Updated:** 2026-08-07  
**Applies To:** Python AI service APIs, ingestion, retrieval, sessions, providers, tools, configuration, logs, and deployment-facing behavior

## 1. Purpose

The Python AI service is a protected backend service handling untrusted requests, documents, retrieved content, model outputs, provider credentials, and future tool capabilities. Security is a cross-cutting architecture constraint, not middleware added at the end.

This standard defines mandatory controls while respecting ADR-009: the concrete Next.js-to-Python production authentication technology remains DEFERRED until deployment/identity requirements are known.

## 2. Trust Boundaries

Primary trust boundaries are:

1. existing Next.js backend -> Python AI API;
2. Python API -> application services;
3. application services -> LLM/embedding/Qdrant/external providers;
4. ingestion boundary -> untrusted document bytes/content/metadata;
5. retrieval/tool output -> prompt/model context;
6. session state -> caller/session authorization boundary;
7. future agent -> tool authorization boundary.

Data crossing a boundary is validated/normalized at the boundary that owns it. Being retrieved from an internal vector store does not make content trusted instruction.

## 3. Service Authentication and Authorization

ADR-009 defers the concrete mechanism, not the requirement.

- protected production AI endpoints require verified service access;
- authentication occurs before expensive AI/provider execution;
- verified identity/security context is passed inward using platform-owned models, not raw transport credential objects;
- authorization is enforced for the requested capability/resource/session;
- CORS is not authentication;
- client-supplied tenant/user/role values are untrusted until bound to verified identity;
- development test/bypass modes must be explicit, configuration-controlled, and impossible to mistake for accepted production behavior;
- do not implement a production auth protocol/library until ADR-009 is promoted.

## 4. Secrets and Credentials

Never place secrets in:

- source code;
- committed `.env` files;
- tests/fixtures/snapshots;
- prompts/document metadata;
- API responses;
- logs/traces/metric labels;
- Cline/AI prompts or review artifacts.

Provider/API/AWS/Qdrant credentials are supplied through the approved runtime secret/configuration mechanism. Production secret-manager technology remains coupled to the future deployment decision.

Credential errors exposed to clients must be generic; internal telemetry may record safe error categories, never secret values.

## 5. Input Validation

Transport validation uses bounded typed schemas; application validation applies capability rules.

Requirements:

- enforce size/count/range limits for query text, `top_k`, filters, uploads, chunk settings, session identifiers, and future tool inputs;
- reject malformed/unsupported structures early;
- preserve legitimate Unicode/international text—ASCII-only sanitization is prohibited without a product requirement;
- do not confuse destructive character stripping with security validation;
- metadata filters use one provider-neutral allowlisted schema;
- validation failures do not expose internal implementation details.

## 6. Document Ingestion Security

Documents are untrusted input.

- validate supported file types using content-aware checks where practical, not extension alone;
- enforce configurable file/document/page/size/resource bounds before expensive processing;
- reject or isolate malformed parser inputs safely;
- ingestion paths must prevent path traversal and unintended arbitrary filesystem access;
- never execute macros/scripts/embedded code as part of document extraction;
- parser failures must be visible and must not silently report successful ingestion;
- document/source metadata must be normalized before persistence;
- future remote-URL ingestion requires a dedicated SSRF/network-egress design before implementation.

## 7. Prompt Injection and Retrieved Content

Retrieved documents, document metadata, user input, tool output, and external data are **data**, not authority.

- retrieved text cannot override system/application policy merely by containing instructions;
- Prompt Builder clearly separates trusted instructions from untrusted context;
- do not place credentials/secrets in model context;
- source/citation identity comes from stored/retrieved metadata, not model claims;
- suspicious/adversarial context is covered by AI/security evaluation cases;
- model output is untrusted when used as input to tools, persistence, or downstream actions and must be validated.

## 8. Agent and Tool Security

Future tools use least privilege.

- Tool Registry exposes only explicitly approved tools;
- no uncontrolled plugin/tool auto-discovery in production;
- authorization applies per tool/action/resource;
- destructive or externally consequential actions require explicit product/security design;
- tool input is validated independently of LLM intent;
- model-generated parameters never bypass authorization;
- provider/tool credentials remain outside graph state/prompts where possible;
- tool output is treated as untrusted data when returned to the model.

## 9. Session and Data Isolation

Session Manager owns conversation memory policy.

- session identity is validated before reads/updates;
- caller authorization must prevent cross-session/cross-tenant access;
- session data is retained only as long as approved policy requires;
- long-term persistent user memory is not a V1 feature;
- process-local memory must not be presented as secure shared production persistence;
- production persistence technology selection follows ADR-007 when required.

## 10. Provider and Network Security

- provider endpoints are configuration-controlled; never accept arbitrary provider URLs from request payloads;
- TLS/transport verification must not be disabled in production merely to make integration pass;
- restrict outbound network access to approved dependencies where deployment controls allow it;
- timeouts/bounds limit resource exhaustion from unavailable dependencies;
- provider error bodies are not forwarded raw to clients;
- AWS Bedrock/Qdrant access uses least-privilege credentials appropriate to the eventual runtime topology.

## 11. API and Error Security

Follow `API_GUIDELINES.md`.

- raw stack traces/exceptions/provider bodies/internal paths never appear in client responses;
- return stable error codes/messages appropriate to the caller;
- do not encode secrets or sensitive content in URLs;
- enforce content types and request bounds;
- streaming errors use the approved SSE error contract after a stream begins;
- health/readiness responses expose enough state for operations without leaking secrets/configuration details.

## 12. CORS, Abuse, and Rate Controls

- production CORS reflects the real caller topology; wildcard origins with credentials are prohibited;
- because Next.js is the service consumer, browser-oriented CORS must not be treated as the primary service security boundary;
- rate/abuse controls must be compatible with the production multi-instance topology;
- correctness-sensitive production rate state must not rely on an uncoordinated module global when shared semantics are required;
- exact rate limits are operational settings, not hard-coded architecture constants.

## 13. Logging, Telemetry, and Privacy

Follow `OBSERVABILITY.md`.

Never indiscriminately log:

- prompts/system instructions;
- user queries;
- retrieved document content;
- generated output;
- full session state;
- authorization headers/tokens/API keys;
- credentials/provider raw responses.

Prefer identifiers, counts, safe categories, hashes/pseudonymous identifiers where justified, and timing/outcome metadata. Data retention/redaction must match future production policy.

## 14. Dependency and Supply-Chain Security

- dependencies must be intentional and required by approved implementation scope;
- pin/constraint strategy must support reproducible builds and controlled upgrades;
- security/deprecation advisories must be reviewed as dependencies evolve;
- do not add duplicate frameworks/providers/SDKs for convenience;
- production container/runtime images, when selected, should minimize unnecessary packages/privileges;
- dependency upgrades that alter provider/index/API semantics require relevant tests/evaluations.

## 15. Security Verification

Tests/reviews must cover, where applicable:

- validation bounds and malformed payloads;
- Unicode preservation;
- unauthorized/forbidden access after ADR-009 promotion;
- session/tenant isolation;
- safe error envelopes/redaction;
- ingestion/path/file handling;
- prompt-injection-oriented retrieved context;
- tool authorization/validation;
- secret/log leakage checks;
- rate/resource bounds;
- dependency readiness failure behavior.

Security findings are not converted into silent fallbacks merely to keep a demo working.

## 16. Deferred Decisions

This standard intentionally does not choose:

- Next.js-to-Python auth mechanism (ADR-009);
- telemetry vendor (ADR-010);
- deployment/secrets/network platform (ADR-011);
- production session store (ADR-007 trigger).

Implementation prompts must not fill these gaps without the corresponding architecture decision.

## 17. Review Checklist

- Is every external/untrusted boundary explicit?
- Are inputs bounded/validated without destroying international text?
- Are secrets absent from code/logs/errors/prompts?
- Is retrieved/tool/model content treated as untrusted data?
- Are sessions/tools protected by authorization boundaries?
- Are provider/network errors safely translated?
- Did the change accidentally select a DEFERRED security/infrastructure technology?
