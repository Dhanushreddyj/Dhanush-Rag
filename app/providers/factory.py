"""
Provider factory — selects implementations based on environment configuration.

Business logic should import from this module (or use the convenience functions in
`llm_service.py`, `vector_store.py`, and `embeddings.py`) rather than importing
provider implementations directly. This enables:
- Swapping providers without changing business code
- Testing with mock implementations
- Future provider additions (Bedrock, Azure AI, etc.)

Usage:
    from app.providers.factory import get_llm_provider, get_vector_store, get_embeddings
"""

from typing import Dict, Any, Optional
import os


def _get_env_bool(key: str, default: bool = False) -> bool:
    """Read a boolean environment variable."""
    val = os.environ.get(key, str(default)).lower()
    return val in ("true", "1", "yes")


# Provider selection — override via environment variables or config
from app.config import settings as _settings

LLM_PROVIDER_NAME = os.environ.get("LLM_PROVIDER", _settings.LLM_PROVIDER).lower()
EMBEDDING_PROVIDER_NAME = os.environ.get("EMBEDDING_PROVIDER", _settings.EMBEDDING_PROVIDER).lower()
VECTOR_STORE_PROVIDER_NAME = os.environ.get("VECTOR_STORE_PROVIDER", _settings.VECTOR_STORE_PROVIDER).lower()


def get_llm_provider(**kwargs) -> Any:
    """Return the configured LLM provider."""
    if LLM_PROVIDER_NAME == "bedrock":
        from app.providers.bedrock import BedrockLLMProvider

        return BedrockLLMProvider(
            region_name=kwargs.get("region_name", os.environ.get("AWS_REGION", "us-east-1")),
            model_id=kwargs.get("model_id", os.environ.get("BEDROCK_MODEL_ID", "")),
            credentials=kwargs.get("credentials"),
        )
    elif LLM_PROVIDER_NAME in ("openai", "openai_compatible"):
        from app.providers.openai import OpenAILLMProvider

        return OpenAILLMProvider(
            api_key=kwargs.get("api_key", os.environ.get("OPENAI_API_KEY", "")),
            base_url=kwargs.get("base_url", os.environ.get("OPENAI_BASE_URL")),
            model=kwargs.get("model", os.environ.get("OPENAI_MODEL", "gpt-4o-mini")),
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER_NAME}")


def get_embeddings_provider(**kwargs) -> Any:
    """Return the configured embedding provider."""
    if EMBEDDING_PROVIDER_NAME == "bedrock":
        from app.providers.bedrock import BedrockEmbeddingProvider

        return BedrockEmbeddingProvider(
            region_name=kwargs.get("region_name", os.environ.get("AWS_REGION", "us-east-1")),
            model_id=kwargs.get("model_id", os.environ.get("BEDROCK_EMBEDDING_MODEL_ID", "")),
            credentials=kwargs.get("credentials"),
        )
    elif EMBEDDING_PROVIDER_NAME == "openai":
        from app.providers.openai import OpenAIEmbeddingProvider

        return OpenAIEmbeddingProvider(
            api_key=kwargs.get("api_key", os.environ.get("OPENAI_API_KEY", "")),
            base_url=kwargs.get("base_url", os.environ.get("OPENAI_BASE_URL")),
            model=kwargs.get("model", os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")),
        )
    else:
        raise ValueError(f"Unsupported embedding provider: {EMBEDDING_PROVIDER_NAME}")


def get_vector_store_provider(**kwargs) -> Any:
    """Return the configured vector store provider."""
    if VECTOR_STORE_PROVIDER_NAME == "qdrant":
        from app.providers.vectorstore.qdrant import QdrantVectorStoreProvider

        return QdrantVectorStoreProvider(
            url=kwargs.get("url") or os.environ.get("QDRANT_URL"),
            host=kwargs.get("host") or os.environ.get("QDRANT_HOST", ""),
            api_key=kwargs.get("api_key", os.environ.get("QDRANT_API_KEY", "")),
            collection_name=kwargs.get("collection_name", os.environ.get("QDRANT_COLLECTION_NAME", "default")),
            embedding_function=kwargs.get("embedding_function"),
        )
    elif VECTOR_STORE_PROVIDER_NAME == "chroma":
        from app.providers.chroma import ChromaVectorStoreProvider

        return ChromaVectorStoreProvider(
            persist_directory=kwargs.get("persist_directory", os.environ.get("CHROMA_DIR", "./data/chroma")),
        )
    else:
        raise ValueError(f"Unsupported vector store provider: {VECTOR_STORE_PROVIDER_NAME}")


__all__ = [
    "get_llm_provider",
    "get_embeddings_provider",
    "get_vector_store_provider",
]
