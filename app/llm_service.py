"""
LLM service wrapper for OpenAI
"""

from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import settings


def get_llm() -> ChatOpenAI:
    """
    Create OpenAI LLM instance
    """
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=0.2,
        max_tokens=1024,
    )


def generate_answer(
    query: str,
    context_docs: List[Dict[str, Any]],
    system_prompt: str = None,
) -> str:
    """
    Generate answer using retrieved context
    """
    llm = get_llm()

    # Build context string
    context_text = "\n\n".join(
        [f"[Source {i+1}]\n{doc['text']}" for i, doc in enumerate(context_docs)]
    )

    # Default system prompt if not provided
    if system_prompt is None:
        system_prompt = (
            "You are a helpful real estate assistant. "
            "Answer questions based on the provided context. "
            "If the context doesn't contain enough information, say so clearly. "
            "Be concise and professional."
        )

    # Build prompt
    user_prompt = f"""Based on the following context, answer the user's question.

Context:
{context_text}

Question: {query}

Answer:"""

    # Call LLM
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)
    return response.content.strip()


def generate_answer_with_sources(
    query: str,
    context_docs: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Generate answer and return with sources
    """
    answer = generate_answer(query, context_docs)

    return {
        "query": query,
        "answer": answer,
        "sources": context_docs,
        "model_used": settings.OPENAI_MODEL,
    }