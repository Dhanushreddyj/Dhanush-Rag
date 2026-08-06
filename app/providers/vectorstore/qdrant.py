"""Qdrant vector store provider — implements VectorStoreProvider interface.

Uses qdrant-client 1.19.x API (client-level methods, not collection objects).
"""

from typing import List, Dict, Any, Optional

import qdrant_client
from langchain_core.documents import Document

from app.providers.base import VectorStoreProvider


class QdrantVectorStoreProvider(VectorStoreProvider):
    """Qdrant-backed vector store.

    Usage (via factory):
        from app.providers.factory import get_vector_store_provider
        provider = get_vector_store_provider(
            url="https://qdrant-xyz.com",
            api_key="your-key",
            collection_name="my_collection",
        )
    """

    def __init__(
        self,
        url: Optional[str] = None,
        host: str = "localhost",
        port: int = 6041,
        api_key: Optional[str] = None,
        collection_name: str = "documents",
        embedding_function=None,  # type: ignore (optional callable)
    ):
        """Initialize the Qdrant provider.

        Args:
            url: Cloud deployment URL (e.g., https://qdrant-xyz.com). Overrides host/port if set.
            host: Local Qdrant server hostname (used when url is not provided).
            port: Port to use for local connection.
            embedding_function: Callable that takes a list of texts and returns embeddings.
        """
        self.url = url
        self.host = host
        self.port = port
        self.api_key = api_key or ""
        self.collection_name = collection_name
        self.embedding_function = embedding_function

        if url:
            import qdrant_client as _qc

            self._client = _qc.QdrantClient(url=url, api_key=api_key)
        else:
            self._client = qdrant_client.QdrantClient(
                host=host, port=port, api_key=api_key
            )

    async def create_collection(self) -> None:
        """Create the collection (idempotent — no-op if exists)."""
        from app.config import settings as _settings

        if self._client.collection_exists(self.collection_name):
            return  # already exists

        dimension = getattr(_settings, "EMBEDDING_DIMENSION", None)
        if dimension is not None and isinstance(dimension, int):
            vectors_config = qdrant_client.http.models.models.VectorParams(
                size=dimension, distance_metric="Float64"
            )
        else:
            raise RuntimeError(
                "EMBEDDING_DIMENSION must be set in settings for Qdrant collection creation. "
                "Add EMBEDDING_DIMENSION = <int> to app/config.py."
            )

        self._client.create_collection(
            collection_name=self.collection_name,
            vectors_config=vectors_config,
            metadata={"created_at": "auto"},
        )

    def _ensure_collection(self):
        """Create or get the collection (synchronous — for internal use)."""
        if not self._client.collection_exists(self.collection_name):
            raise RuntimeError(
                f"Collection '{self.collection_name}' does not exist. "
                "Call create_collection() first."
            )

    async def similarity_search(
        self, query: str, k: int = 5, filters: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Search for similar documents using the Qdrant SDK directly."""
        from qdrant_client.http.models.models import Filter

        try:
            # Convert langchain-style filter dict to Qdrant Filter if provided
            query_filter = None
            if filters:
                query_filter = self._build_qdrant_filter(filters)

            response = await asyncio.to_thread_safe(self._client.query_points)(
                collection_name=self.collection_name,
                query=query,
                limit=k,
                with_payload=True,
                with_vectors=False,
                query_filter=query_filter,
            )

            docs = []
            for result in response.results:
                payload = getattr(result, "payload", {}) or {}
                content = payload.pop("_content", "")
                doc = Document(
                    page_content=content,
                    metadata={**payload, "_score": result.score},
                )
                docs.append(doc)

            return docs
        except Exception as e:
            raise RuntimeError(f"Qdrant similarity search failed: {e}")

    def _build_qdrant_filter(self, filters: Dict[str, Any]) -> "Filter":  # type: ignore (forward ref)
        """Convert a dict of filter conditions to Qdrant Filter."""
        from qdrant_client.http.models.models import Filter as QdrantFilter

        conditions = []
        for key, value in filters.items():
            if isinstance(value, dict):
                op = value.get("op", "eq")
                val = value.get("value")
                if op == "eq":
                    conditions.append(QdrantFilter(key=key, value=val))
                elif op == "neq":
                    conditions.append(
                        QdrantFilter(key=key, operator="neq", value=val)
                    )
                elif op == "in":
                    conditions.append(
                        QdrantFilter(key=key, operator="in", value=value.get("values", []))
                    )
            else:
                # Simple equality filter
                conditions.append(QdrantFilter(key=key, value=value))

        if not conditions:
            return None  # type: ignore (None means no filtering)

        return QdrantFilter(conditions=conditions, operator="and")

    async def add_documents(
        self,
        documents: List[Any],
        ids: Optional[List[str]] = None,
        batch_size: int = 100,
    ) -> None:
        """Add documents to the vector store."""
        from qdrant_client.http.models.models import PointStruct

        self._ensure_collection()

        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            batch_ids = ids[i : i + batch_size] if ids else None

            # Prepare data for Qdrant
            points = []
            for idx, doc in enumerate(batch):
                content = doc.page_content if hasattr(doc, "page_content") else str(doc)
                metadata = getattr(doc, "metadata", {}) or {}
                metadata["_content"] = content  # store content in metadata

                point_id = batch_ids[idx] if batch_ids and idx < len(batch_ids) else None

                if self.embedding_function is not None:
                    embedding = await self.embedding_function(content)
                else:
                    raise ValueError("embedding_function is required for add_documents")

                points.append(
                    PointStruct(id=point_id, vector=embedding, metadata=metadata)
                )

            self._client.upsert(collection_name=self.collection_name, points=points)

    async def reset_collection(self) -> None:
        """Reset (drop and recreate) the collection."""
        await self.delete_collection()
        await self.create_collection()

    async def delete_collection(self) -> None:
        """Delete the entire collection."""
        try:
            self._client.delete_collection(self.collection_name)
        except Exception as e:
            # Handle both old and new SDK error types
            if "not found" not in str(e).lower():
                raise

    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        self._ensure_collection()
        try:
            info = self._client.get_collection(self.collection_name)
            return {
                "count": getattr(info, "num_vectors", 0),
                "metadata": dict(getattr(info, "metadata", {}) or {}),
            }
        except Exception as e:
            if "not found" not in str(e).lower():
                raise
            return {"count": 0, "metadata": {}}

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
