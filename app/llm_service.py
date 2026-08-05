"""
LLM service — delegates to the configured provider.

The default provider is OpenAI (for development). In production this should
be swapped via environment variables or a config flag.
"""

from typing import List, Dict, Any, Optional
from functools import lru_cache

from app.config import settings
from app.providers.base import LLMProvider


@lru_cache(maxsize=1)
def get_llm_provider() -> LLMProvider:
    """Return the configured LLM provider (singleton)."""
    from app.providers.factory import get_llm_provider as _factory

    return _factory(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        model=settings.OPENAI_MODEL,
    )


def generate_answer_with_sources(
    query: str,
    context_docs: List[Dict[str, Any]],
    system_prompt: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> Dict[str, Any]:
    """Generate answer and return with sources via the configured provider."""
    llm_provider = get_llm_provider()

    result = llm_provider.generate_answer(
        query=query,
        context_docs=context_docs,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return {
        "query": query,
        "answer": result["answer"],
        "sources": context_docs,
        "model_used": result["model_used"],
    }


def generate_stream(
    query: str,
    context_docs: List[Dict[str, Any]],
    system_prompt: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
):
    """Streaming generator — yields chunks as they arrive."""
    llm_provider = get_llm_provider()

    for chunk in llm_provider.generate_stream(
        query=query,
        context_docs=context_docs,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    ):
        yield chunk


__all__ = [
    "get_llm_provider",
    "generate_answer_with_sources",
    "generate_stream",
]
