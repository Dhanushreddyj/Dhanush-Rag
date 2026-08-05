"""
Abstract base classes for all service providers.

Business logic should only import from this module, never directly from
provider implementations (e.g., langchain_openai). This enables:
- Swapping providers without changing business code
- Testing with mock implementations
- Future provider additions (Bedrock, Azure AI, etc.)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class LLMProvider(ABC):
    """Interface for language model services."""

    @abstractmethod
    def generate_answer(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """Generate an answer from retrieved context."""

    @abstractmethod
    def generate_stream(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ):
        """Generate a streaming response (async generator)."""


class EmbeddingProvider(ABC):
    """Interface for embedding generation services."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string. Returns a list of floats."""

    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple text strings. Returns list of float lists."""

    # New methods for async document embedding (preferred in production)
    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string. Returns a list of floats."""

    @abstractmethod
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple document strings asynchronously. Returns list of float lists."""


class VectorStoreProvider(ABC):
    """Interface for vector database services."""

    @abstractmethod
    async def add_documents(
        self,
        documents: List[Any],
        ids: Optional[List[str]] = None,
        batch_size: int = 100,
    ) -> None:
        """Add documents to the vector store."""

    @abstractmethod
    async def similarity_search(
        self,
        query: str,
        k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """Search for similar documents. Returns list of Document objects."""

    @abstractmethod
    async def delete_collection(self) -> None:
        """Delete the entire collection (use with caution)."""


class CacheProvider(ABC):
    """Interface for caching services."""

    @abstractmethod
    async def get(self, key: str) -> Any:
        """Get a cached value. Returns None if not found or expired."""

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: float = 60.0) -> bool:
        """Set a cached value with TTL in seconds."""

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete a cached value."""


class HealthCheckProvider(ABC):
    """Interface for health check services."""

    @abstractmethod
    async def check_llm_connectivity(self) -> Dict[str, Any]:
        """Check if the LLM service is reachable and functional."""

    @abstractmethod
    async def check_vector_store_connectivity(self) -> Dict[str, Any]:
        """Check if the vector store is reachable and functional."""


__all__ = [
    "LLMProvider",
    "EmbeddingProvider",
    "VectorStoreProvider",
    "CacheProvider",
    "HealthCheckProvider",
]
