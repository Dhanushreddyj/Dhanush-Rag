"""ChromaDB vector store provider — implements VectorStoreProvider interface."""

from typing import List, Dict, Any, Optional
import chromadb
from langchain.vectorstores.chroma import Chroma as LangChainChroma
from langchain.document import Document

from app.providers.base import VectorStoreProvider


class ChromaVectorStoreProvider(VectorStoreProvider):
    """ChromaDB-backed vector store."""

    def __init__(self, persist_directory: str = "./chroma_data", embedding_function=None):
        self._client = chromadb.Client(path=persist_directory)
        self._collection_name = "documents"
        self._collection = None  # lazy init
        self.embedding_function = embedding_function  # type: EmbeddingFunction | None

    @property
    def _ensure_collection(self):
        if self._collection is None:
            try:
                self._collection = self._client.get_or_create_collection(
                    name=self._collection_name,
                    metadata={"created_at": "auto"},
                )
            except Exception as e:
                raise RuntimeError(f"Failed to initialize ChromaDB collection: {e}")
        return self._collection

    async def similarity_search(
        self, query: str, k: int = 5, filters: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        chroma = LangChainChroma(
            client=self._client,
            collection_name=self._collection_name,
            embedding_function=self.embedding_function,
        )
        results = await chroma.asimilarity(query, k=k)
        return results

    async def add_documents(
        self,
        documents: List[Any],
        ids: Optional[List[str]] = None,
        batch_size: int = 100,
    ) -> None:
        chroma = LangChainChroma(
            client=self._client,
            collection_name=self._collection_name,
            embedding_function=self.embedding_function,
        )
        await chroma.aadd_documents(documents=documents, ids=ids)

    async def delete_collection(self) -> None:
        self._client.delete_collection(name=self._collection_name)
        self._collection = None

    async def get_collection_stats(self) -> Dict[str, Any]:
        collection = self._ensure_collection
        return {
            "count": len(collection),
            "metadata": collection.metadata,
        }
