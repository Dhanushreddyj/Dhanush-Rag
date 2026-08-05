"""
ChromaDB vector store management
"""

from typing import List, Dict, Any, Optional

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import settings
from app.embeddings import get_embeddings


# Global vector store instance
_vector_store: Optional[Chroma] = None


def get_vector_store() -> Chroma:
    """
    Get or create ChromaDB vector store instance
    """
    global _vector_store

    if _vector_store is None:
        embeddings = get_embeddings()

        _vector_store = Chroma(
            persist_directory=str(settings.CHROMA_DIR),
            embedding_function=embeddings,
            client_settings=chromadb.config.Settings(
                allow_reset=True,
                anonymized_telemetry=False,
            ),
        )

    return _vector_store


def add_documents(
    documents: List[Document],
    ids: Optional[List[str]] = None,
    batch_size: int = 100,
) -> None:
    """
    Add documents to the vector store
    """
    vector_store = get_vector_store()

    if ids is None:
        # Auto-generate IDs
        vector_store.add_documents(documents, batch_size=batch_size)
    else:
        # Use provided IDs
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i : i + batch_size]
            batch_ids = ids[i : i + batch_size]
            vector_store.add_documents(batch_docs, ids=batch_ids)


def similarity_search(
    query: str,
    k: int = 5,
    filters: Optional[Dict[str, Any]] = None,
) -> List[Document]:
    """
    Search for similar documents
    """
    vector_store = get_vector_store()

    if filters:
        return vector_store.similarity_search(query, k=k, filter=filters)
    else:
        return vector_store.similarity_search(query, k=k)


def similarity_search_with_score(
    query: str,
    k: int = 5,
    filters: Optional[Dict[str, Any]] = None,
) -> List[tuple]:
    """
    Search with similarity scores
    """
    vector_store = get_vector_store()

    if filters:
        return vector_store.similarity_search_with_score(query, k=k, filter=filters)
    else:
        return vector_store.similarity_search_with_score(query, k=k)


def delete_collection() -> None:
    """
    Delete the entire ChromaDB collection (use with caution)
    """
    global _vector_store
    _vector_store = None

    # Recreate empty store
    embeddings = get_embeddings()
    _vector_store = Chroma(
        persist_directory=str(settings.CHROMA_DIR),
        embedding_function=embeddings,
        client_settings=chromadb.config.Settings(
            allow_reset=True,
            anonymized_telemetry=False,
        ),
    )


def get_collection_stats() -> Dict[str, Any]:
    """
    Get collection statistics
    """
    vector_store = get_vector_store()
    collection = vector_store.get_collection()

    return {
        "count": collection.count(),
        "name": collection.name,
    }
