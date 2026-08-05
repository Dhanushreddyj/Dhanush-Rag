"""
OpenAI provider implementations for LLM, embeddings, and vector stores.

This module wraps langchain_openai behind the abstract interfaces defined in
`app.providers.base`. Business logic should import from `providers/base.py`,
not directly from this module.

Future providers (e.g., Bedrock) will implement the same interfaces.
"""

from typing import List, Dict, Any, Optional
import asyncio
from functools import lru_cache

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.exceptions import LLMCallErrorException

from app.providers.base import (
    LLMProvider,
    EmbeddingProvider,
    VectorStoreProvider,
)
from app.config import settings


class OpenAILLMProvider(LLMProvider):
    """OpenAI provider for language model services."""

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.base_url = base_url or settings.OPENAI_BASE_URL
        self.model = model or settings.OPENAI_MODEL

    @lru_cache(maxsize=1)
    def _get_llm(self, temperature: float, max_tokens: int):
        """Cached LLM instance creation to avoid repeated initialization."""
        return ChatOpenAI(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def generate_answer(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        llm = self._get_llm(temperature, max_tokens)

        context_text = "\n\n".join(
            [f"[Source {i+1}]\n{doc['text']}" for i, doc in enumerate(context_docs)]
        )

        if system_prompt is None:
            system_prompt = (
                "You are a helpful real estate assistant. "
                "Answer questions based on the provided context. "
                "If the context doesn't contain enough information, say so clearly. "
                "Be concise and professional."
            )

        user_prompt = f"""Based on the following context, answer the user's question.

Context:
{context_text}

Question: {query}

Answer:"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        try:
            response = llm.invoke(messages)
            return {
                "answer": response.content.strip(),
                "model_used": self.model,
            }
        except LLMCallErrorException as e:
            raise RuntimeError(f"LLM API error: {e}") from e

    def generate_stream(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ):
        """Streaming generator — yields chunks as they arrive."""
        llm = self._get_llm(temperature, max_tokens)

        context_text = "\n\n".join(
            [f"[Source {i+1}]\n{doc['text']}" for i, doc in enumerate(context_docs)]
        )

        if system_prompt is None:
            system_prompt = (
                "You are a helpful real estate assistant. "
                "Answer questions based on the provided context. "
                "If the context doesn't contain enough information, say so clearly. "
                "Be concise and professional."
            )

        user_prompt = f"""Based on the following context, answer the user's question.

Context:
{context_text}

Question: {query}

Answer:"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        stream = llm.stream(messages)
        for chunk in stream:
            if hasattr(chunk, "content") and chunk.content:
                yield chunk.content


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI provider for embedding generation services."""

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.base_url = base_url or settings.OPENAI_BASE_URL
        self.model = model or settings.EMBEDDING_MODEL

    @lru_cache(maxsize=1)
    def _get_embeddings(self):
        """Cached embeddings instance creation."""
        return OpenAIEmbeddings(
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def embed_text(self, text: str) -> List[float]:
        try:
            return self._get_embeddings().embed_query(text)
        except LLMCallErrorException as e:
            raise RuntimeError(f"Embedding API error: {e}") from e

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        try:
            return self._get_embeddings().embed_documents(texts)
        except LLMCallErrorException as e:
            raise RuntimeError(f"Embedding API error: {e}") from e


class OpenAIVectorStoreProvider(VectorStoreProvider):
    """ChromaDB provider for vector storage (production-ready with Qdrant swap)."""

    def __init__(self, persist_directory: str = None, embedding_provider=None):
        self.persist_directory = persist_directory or str(settings.CHROMA_DIR)
        self.embedding_provider = embedding_provider  # type: EmbeddingProvider | None

    async def add_documents(
        self,
        documents: List[Any],
        ids: Optional[List[str]] = None,
        batch_size: int = 100,
    ) -> None:
        from langchain_chroma import Chroma

        embeddings = (
            self.embedding_provider._get_embeddings()
            if self.embedding_provider
            else OpenAIEmbeddingProvider()._get_embeddings()
        )
        store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=embeddings,
            client_settings=__import__("chromadb").config.Settings(
                allow_reset=True,
                anonymized_telemetry=False,
            ),
        )

        if ids is None:
            await asyncio.get_event_loop().run_in_executor(
                lambda: store.add_documents(documents, batch_size=batch_size)
            )
        else:
            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i : i + batch_size]
                batch_ids = ids[i : i + batch_size]
                await asyncio.get_event_loop().run_in_executor(
                    lambda b=batch_docs, bi=batch_ids: store.add_documents(b, ids=bi)
                )

    async def similarity_search(
        self,
        query: str,
        k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        from langchain_chroma import Chroma

        embeddings = (
            self.embedding_provider._get_embeddings()
            if self.embedding_provider
            else OpenAIEmbeddingProvider()._get_embeddings()
        )
        store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=embeddings,
            client_settings=__import__("chromadb").config.Settings(
                allow_reset=True,
                anonymized_telemetry=False,
            ),
        )

        if filters:
            return await asyncio.get_event_loop().run_in_executor(
                lambda: store.similarity_search(query, k=k, filter=filters)
            )
        else:
            return await asyncio.get_event_loop().run_in_executor(
                lambda: store.similarity_search(query, k=k)
            )

    async def delete_collection(self) -> None:
        from langchain_chroma import Chroma

        embeddings = (
            self.embedding_provider._get_embeddings()
            if self.embedding_provider
            else OpenAIEmbeddingProvider()._get_embeddings()
        )
        store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=embeddings,
            client_settings=__import__("chromadb").config.Settings(
                allow_reset=True,
                anonymized_telemetry=False,
            ),
        )

        await asyncio.get_event_loop().run_in_executor(lambda: store.delete_collection())


__all__ = [
    "OpenAILLMProvider",
    "OpenAIEmbeddingProvider",
    "OpenAIVectorStoreProvider",
]
