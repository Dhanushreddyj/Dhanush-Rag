"""
Embedding generation using OpenAI-compatible API (LM Studio)
"""

from langchain_openai import OpenAIEmbeddings

from app.config import settings


def get_embeddings() -> OpenAIEmbeddings:
    """
    Create embeddings instance using LM Studio OpenAI-compatible API
    """
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
    )


def embed_text(text: str) -> list:
    """
    Embed a single text string
    """
    embeddings = get_embeddings()
    return embeddings.embed_query(text)


def embed_texts(texts: list) -> list:
    """
    Embed multiple text strings
    """
    embeddings = get_embeddings()
    return embeddings.embed_documents(texts)
