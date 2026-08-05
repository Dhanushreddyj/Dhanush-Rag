"""
RAG service - retrieval and answer generation
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from app.vector_store import similarity_search
from app.llm_service import generate_answer_with_sources
from app.config import settings
from app.cache import cache_result, get_query_cache


async def ask_rag(
    query: str,
    filters: Optional[Dict[str, Any]] = None,
    top_k: int = 5,
) -> Dict[str, Any]:
    """
    Main RAG pipeline: retrieve + generate answer.

    Uses the in-memory cache to avoid redundant API calls and vector searches.
    """
    # Check cache first (skip if query is empty or too short)
    if len(query.strip()) > 3:
        cached = get_query_cache().get(get_query_cache()._make_key(query))
        if cached is not None:
            return cached

    # Retrieve relevant documents
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
            "timestamp": datetime.now(),
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

    # Generate answer
    result = generate_answer_with_sources(
        query=query,
        context_docs=context_docs,
    )

    result["count"] = len(context_docs)
    result["timestamp"] = datetime.now()

    return result


@cache_result(ttl=60.0)  # Cache answers for 1 minute
async def get_cached_answer(query: str, filters: Optional[Dict[str, Any]] = None, top_k: int = 5):
    """Cached wrapper around ask_rag."""
    return await ask_rag(query=query, filters=filters, top_k=top_k)


def format_sources_for_display(sources: List[Dict[str, Any]]) -> str:
    """
    Format sources for display in chatbot UI
    """
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
    """
    Build a complete RAG response object
    """
    return {
        "query": query,
        "answer": answer,
        "sources": sources,
        "sources_display": format_sources_for_display(sources),
        "count": len(sources),
        "model_used": settings.OPENAI_MODEL,
        "timestamp": datetime.now(),
    }