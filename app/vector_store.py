"""
Vector store — delegates to the configured provider.

The default provider is ChromaDB (for development). In production this should
be swapped via environment variables or a config flag.
"""

from typing import List, Dict, Any, Optional
from functools import lru_cache

from app.config import settings


@lru_cache(maxsize=1)
def get_vector_store() -> Any:
    """Return the configured vector store provider (singleton)."""
    from app.providers.factory import get_vector_store_provider as _factory

    return _factory(
        persist_directory=str(settings.CHROMA_DIR),
    )


async def similarity_search(
    query: str,
    k: int = 5,
    filters: Optional[Dict[str, Any]] = None,
) -> List[Any]:
    """Search for similar documents via the configured provider."""
    vector_store = get_vector_store()
    return await vector_store.similarity_search(query=query, k=k, filters=filters)


async def add_documents(
    documents: List[Any],
    ids: Optional[List[str]] = None,
    batch_size: int = 100,
) -> None:
    """Add documents to the vector store via the configured provider."""
    vector_store = get_vector_store()
    await vector_store.add_documents(documents=documents, ids=ids, batch_size=batch_size)


async def delete_collection() -> None:
    """Delete the entire collection (use with caution)."""
    global _vector_store
    _vector_store = None

    from app.embeddings import get_embeddings  # avoid circular import at module level
    embeddings = get_embeddings()
    vector_store = get_vector_store()
    await vector_store.delete_collection()


async def get_collection_stats() -> Dict[str, Any]:
    """Get collection statistics."""
    vector_store = get_vector_store()
    return await vector_store.get_collection_stats()
