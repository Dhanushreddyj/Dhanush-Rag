"""Embedding generation — delegates to the configured provider."""

from typing import List, Any
from functools import lru_cache

from app.config import settings
from app.providers.base import EmbeddingProvider
from app.providers.openai import OpenAIEmbeddingProvider


@lru_cache(maxsize=1)
def get_embeddings() -> EmbeddingProvider:
    """Return the configured embedding provider (singleton)."""
    return OpenAIEmbeddingProvider(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        model=settings.EMBEDDING_MODEL,
    )


async def embed_text(text: str) -> List[float]:
    """Embed a single text string."""
    embeddings = get_embeddings()
    return await embeddings.embed_query(text)


async def embed_texts(texts: List[str]) -> "List[List[float]]":
    """Embed multiple text strings."""
    embeddings = get_embeddings()
    return await embeddings.embed_documents(texts)
