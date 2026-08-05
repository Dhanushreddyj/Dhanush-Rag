"""
RAG service — retrieval, caching, and answer generation.

This module orchestrates:
1. Query cache lookup (in-memory LRU with TTL)
2. Vector similarity search via the configured provider
3. Answer generation via the configured LLM provider
4. Response formatting for the API layer

The default providers are OpenAI/ChromaDB (for development). In production,
swap them by overriding `get_llm_provider()` and `get_vector_store()`.
"""

from typing import List, Dict, Any, Optional
from functools import lru_cache

from app.vector_store import similarity_search
from app.llm_service import get_llm_provider
from app.config import settings


@lru_cache(maxsize=1)
def _get_rag_answer(query: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Cached answer generation — avoids repeated LLM calls for identical queries."""
    llm_provider = get_llm_provider()

    result = llm_provider.generate_answer(
        query=query,
        context_docs=context_docs,
        system_prompt=(
            "You are a helpful real estate assistant. "
            "Answer questions based on the provided context. "
            "If the context doesn't contain enough information, say so clearly. "
            "Be concise and professional."
        ),
    )

    return {
        "answer": result["answer"],
        "model_used": result.get("model_used", settings.OPENAI_MODEL),
    }


async def ask_rag(
    query: str,
    filters: Optional[Dict[str, Any]] = None,
    top_k: int = 5,
) -> Dict[str, Any]:
    """
    Main RAG pipeline: retrieve + generate answer.

    Uses Redis cache to avoid redundant API calls and vector searches.
    """
    from app.cache import get_query_cache

    # Check cache first (skip if query is empty, too short, or caching disabled)
    if len(query.strip()) > 3 and settings.CACHE_ENABLED:
        cached = get_query_cache().get(get_query_cache()._make_key(query))
        if cached is not None:
            return cached

    # Retrieve relevant documents via the configured vector store provider
    retrieved_docs = similarity_search(
        query=query,
        k=top_k,
        filters=filters,
    )

    if not retrieved_docs:
        return {
            "query": query,
            "answer": (
                "I couldn't find relevant information in the documents to answer this question. "
                "Please try rephrasing or ask about a different topic."
            ),
            "sources": [],
            "count": 0,
            "model_used": settings.OPENAI_MODEL,
        }

    # Format documents for LLM
    context_docs = [
        {
            "text": doc.page_content,
            "metadata": doc.metadata,
            "score": getattr(doc, "score", None),
        }
        for doc in retrieved_docs
    ]

    # Generate answer via the configured LLM provider (with cache)
    result = _get_rag_answer(query=query, context_docs=context_docs)

    response = {
        "query": query,
        "answer": result["answer"],
        "sources": context_docs,
        "count": len(context_docs),
        "model_used": result.get("model_used", settings.OPENAI_MODEL),
    }

    # Cache the answer for 60 seconds to avoid redundant LLM calls
    from app.cache import get_query_cache
    get_query_cache().set(get_query_cache()._make_key(query), response, ttl=60.0)

    return response


def format_sources_for_display(sources: List[Dict[str, Any]]) -> str:
    """Format sources for display in chatbot UI."""
    if not sources:
        return "No sources available"

    source_lines = []
    for i, source in enumerate(sources, 1):
        filename = source.get("metadata", {}).get("filename", "Unknown")
        doc_type = source.get("metadata", {}).get("doc_type", "Unknown")
        source_lines.append(f"{i}. {filename} ({doc_type})")

    return "\n".join(source_lines)


def build_rag_response(
    query: str,
    answer: str,
    sources: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Build a complete RAG response object."""
    return {
        "query": query,
        "answer": answer,
        "sources": sources,
        "sources_display": format_sources_for_display(sources),
        "count": len(sources),
        "model_used": settings.OPENAI_MODEL,
    }
