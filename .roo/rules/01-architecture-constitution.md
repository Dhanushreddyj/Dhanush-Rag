# Architecture Constitution

These rules are non-negotiable.

## Runtime and Frameworks

- CPython 3.14.7 only.
- FastAPI owns HTTP delivery only.
- Pydantic owns typed validation and settings models.
- LangGraph owns agent orchestration only.
- Async-first for I/O and provider boundaries.
- Do not introduce LangChain unless an accepted architecture decision explicitly authorizes it.

## Layer Ownership

- Controllers translate HTTP requests and responses.
- Controllers remain thin.
- Application services orchestrate use cases.
- Contracts define provider-neutral interfaces and typed models.
- Providers adapt external systems and SDKs.
- Repositories own persistence semantics.
- Prompt Builder owns prompt construction.
- Retriever owns retrieval, filtering, ranking, and reranking policy.
- Response Builder owns response formatting and citations.
- Session Manager owns conversation-scoped state.
- Tool Registry owns approved tool registration.
- LangGraph coordinates approved application operations and tools.
- Composition/bootstrap owns dependency construction and provider selection.

## Provider Strategy

- Business logic must remain provider-agnostic.
- Exactly one provider implementation is active for each capability.
- Provider selection is configuration-driven.
- Production LLM provider: AWS Bedrock models.
- Production embedding provider: AWS Bedrock embedding models.
- Development LLM: Qwen through LM Studio’s OpenAI-compatible endpoint.
- Development embeddings remain configuration-driven.
- OpenAI-compatible is a protocol boundary, not a permanent vendor dependency.
- Providers must not construct prompts or make business decisions.
- SDK request and response objects must not escape provider boundaries.

## Vector Store

- Qdrant is the only approved V1 vector database.
- Qdrant Cloud is the current development deployment.
- Self-hosted Qdrant must remain supported through configuration.
- Chroma is not an approved V1 runtime path.
- Do not introduce OpenSearch, Pinecone, Milvus, or another vector database without an accepted ADR.

## Prohibitions

- No business logic in controllers.
- No business logic in providers.
- No provider SDK use inside application services.
- No direct Qdrant access from API routes.
- No prompts inside providers or controllers.
- No hard-coded API keys, credentials, LAN addresses, ports, or model identifiers.
- No global mutable request state.
- No circular dependencies.
- No framework-wide redesign during an implementation task.