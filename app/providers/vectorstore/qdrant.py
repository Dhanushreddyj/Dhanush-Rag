"""Qdrant vector store provider — implements VectorStoreProvider interface."""

from typing import List, Dict, Any, Optional

import qdrant_client
from langchain.document import Document

from app.providers.base import VectorStoreProvider


class QdrantVectorStoreProvider(VectorStoreProvider):
    """Qdrant-backed vector store.

    Usage (via factory):
        from app.providers.factory import get_vector_store_provider
        provider = get_vector_store_provider(
            host="http://localhost",
            api_key="your-key",
            collection_name="my_collection",
        )
    """

    def __init__(
        self,
        host: str,
        api_key: str,
        collection_name: str = "documents",
        embedding_function=None,  # type: ignore (optional callable)
    ):
        self._client = qdrant_client.QdrantClient(host=host, api_key=api_key)
        self.collection_name = collection_name
        self.embedding_function = embedding_function

    async def create_collection(self) -> None:
        """Create the collection (idempotent — no-op if exists)."""
        self._ensure_collection()  # creates if missing, returns existing

    def _ensure_collection(self):
        """Create or get the collection (synchronous — for internal use)."""
        try:
            return self._client.get_collection(self.collection_name)
        except qdrant_client.CollectionNotFoundError:
            return self._client.create_collection(
                name=self.collection_name,
                metadata={"created_at": "auto"},
            )

    async def similarity_search(
        self, query: str, k: int = 5, filters: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Search for similar documents."""
        collection = self._ensure_collection()

        # Embed the query using the configured embedding function
        if self.embedding_function is not None:
            query_embedding = await self.embedding_function(query)
        else:
            raise ValueError("embedding_function is required for similarity search")

        results = collection.query(
            vectors=[query_embedding],
            n=k,
            filter=filters or {},
        )

        # Convert Qdrant results to Document objects
        documents = []
        for result in results:
            doc_id = result.get("id", "")
            metadata = result.get("metadata", {})
            content = metadata.pop("_content", "")  # remove internal field
            doc = Document(page_content=content, metadata=metadata)
            doc.metadata["_score"] = result.get("distance")
            documents.append(doc)

        return documents

    async def add_documents(
        self,
        documents: List[Any],
        ids: Optional[List[str]] = None,
        batch_size: int = 100,
    ) -> None:
        """Add documents to the vector store."""
        collection = self._ensure_collection()

        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            batch_ids = ids[i : i + batch_size] if ids else None

            # Prepare data for Qdrant
            vectors = []
            metadatas = []
            for doc in batch:
                content = doc.page_content if hasattr(doc, "page_content") else str(doc)
                metadata = getattr(doc, "metadata", {}) or {}
                metadata["_content"] = content  # store content in metadata

                if self.embedding_function is not None:
                    embedding = await self.embedding_function(content)
                else:
                    raise ValueError("embedding_function is required for add_documents")

                vectors.append(embedding)
                metadatas.append(metadata)

            collection.add(
                ids=batch_ids,
                vectors=vectors,
                metadatas=metadatas,
            )

    async def reset_collection(self) -> None:
        """Reset (drop and recreate) the collection."""
        await self.delete_collection()
        await self.create_collection()

    async def delete_collection(self) -> None:
        """Delete the entire collection."""
        try:
            self._client.delete_collection(self.collection_name)
        except qdrant_client.CollectionNotFoundError:
            pass  # already deleted

    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        collection = self._ensure_collection()
        stats = collection.stats()
        return {
            "count": stats.get("num_vectors", 0),
            "metadata": collection.metadata,
        }

    async def similarity_search_with_score(
        self, query: str, k: int = 5, filters: Optional[Dict[str, Any]] = None
    ) -> List[tuple]:
        """Search for similar documents with scores. Returns list of (Document, score)."""
        docs = await self.similarity_search(query=query, k=k, filters=filters)
        results = []
        for doc in docs:
            score = doc.metadata.pop("_score", None)  # type: ignore
            results.append((doc, score))
        return results

