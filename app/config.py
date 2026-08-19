"""
Configuration settings for the RAG service
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "RealEstateRAG"
    ENV: str = "development"

    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    CHROMA_DIR: Path = BASE_DIR / "data" / "chroma"
    DOCS_DIR: Path = BASE_DIR / "data" / "documents"

    # Embeddings
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSION: int = 1536

    # Providers (override via environment variables)
    LLM_PROVIDER: str = "openai_compatible"
    EMBEDDING_PROVIDER: str = "openai_compatible"
    VECTOR_STORE_PROVIDER: str = "qdrant"

    # OpenAI-compatible API (e.g., LM Studio, Bedrock endpoint)
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_BASE_URL: Optional[str] = None

    # RAG parameters
    TOP_K: int = 5
    MAX_CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 150
    MIN_QUERY_LENGTH: int = 3
    MAX_QUERY_LENGTH: int = 2048
    MAX_CONTEXT_DOCS: int = 10

    # ChromaDB
    CHROMA_PERSISTENCE: bool = True

    # Rate limiting (requests per minute)
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_WINDOW_SECONDS: float = 60.0

    # Caching
    CACHE_ENABLED: bool = True
    CACHE_TTL_SECONDS: int = 300  # 5 minutes
    MAX_CACHE_SIZE: int = 1000

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Qdrant (local or cloud)
    QDRANT_URL: Optional[str] = None  # Cloud deployment URL; overrides host/port if set
    QDRANT_HOST: str = "localhost"
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION_NAME: str = "default"




settings = Settings()



def validate_settings(candidate: Settings | None = None) -> None:
    """Validate configuration settings at application startup.

    When *candidate* is ``None``, validates the module-level ``settings`` instance.
    Raises ``ValueError`` with a clear setting-specific message for every failed invariant.
    Does not make network calls, instantiate providers or SDK clients, access Qdrant,
    contact LM Studio or Bedrock, read/write application data, or mutate the supplied Settings.
    """

    s = candidate if candidate is not None else settings

    # Numeric and range invariants ---------------------------------------------------------
    if s.TOP_K <= 0:
        raise ValueError("TOP_K must be greater than zero")
    if s.MAX_CHUNK_SIZE <= 0:
        raise ValueError("MAX_CHUNK_SIZE must be greater than zero")
    if not (0 <= s.CHUNK_OVERLAP < s.MAX_CHUNK_SIZE):
        raise ValueError(
            "CHUNK_OVERLAP must be greater than or equal to zero and less than MAX_CHUNK_SIZE"
        )
    if s.EMBEDDING_DIMENSION <= 0:
        raise ValueError("EMBEDDING_DIMENSION must be greater than zero")
    if s.MIN_QUERY_LENGTH <= 0:
        raise ValueError("MIN_QUERY_LENGTH must be greater than zero")
    if s.MAX_QUERY_LENGTH <= 0:
        raise ValueError("MAX_QUERY_LENGTH must be greater than zero")
    if s.MIN_QUERY_LENGTH > s.MAX_QUERY_LENGTH:
        raise ValueError(
            "MIN_QUERY_LENGTH must be less than or equal to MAX_QUERY_LENGTH"
        )
    if s.MAX_CONTEXT_DOCS <= 0:
        raise ValueError("MAX_CONTEXT_DOCS must be greater than zero")
    if s.RATE_LIMIT_PER_MINUTE <= 0:
        raise ValueError("RATE_LIMIT_PER_MINUTE must be greater than zero")
    if s.RATE_LIMIT_WINDOW_SECONDS <= 0:
        raise ValueError("RATE_LIMIT_WINDOW_SECONDS must be greater than zero")
    if s.CACHE_TTL_SECONDS <= 0:
        raise ValueError("CACHE_TTL_SECONDS must be greater than zero")
    if s.MAX_CACHE_SIZE <= 0:
        raise ValueError("MAX_CACHE_SIZE must be greater than zero")

    # Provider and environment ---------------------------------------------------------
    for field in ("ENV", "LLM_PROVIDER", "EMBEDDING_PROVIDER"):
        value = getattr(s, field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")

    # Vector store ---------------------------------------------------------
    if s.VECTOR_STORE_PROVIDER != "qdrant":
        raise ValueError(
            f"VECTOR_STORE_PROVIDER must be exactly 'qdrant', got '{s.VECTOR_STORE_PROVIDER}'"
        )

    if not isinstance(s.QDRANT_COLLECTION_NAME, str) or not s.QDRANT_COLLECTION_NAME.strip():
        raise ValueError("QDRANT_COLLECTION_NAME must be a non-empty string")

    # Qdrant connection ---------------------------------------------------------
    qdrant_url = getattr(s, "QDRANT_URL", None)
    if (qdrant_url is None) or not str(qdrant_url).strip():
        qdrant_host = getattr(s, "QDRANT_HOST", "")
        if not isinstance(qdrant_host, str) or not qdrant_host.strip():
            raise ValueError(
                "QDRANT_URL must be set or QDRANT_HOST must be a non-empty string"
            )

    # OpenAI-compatible LLM ---------------------------------------------------------
    if s.LLM_PROVIDER == "openai_compatible":
        base_url = getattr(s, "OPENAI_BASE_URL", None)
        model = getattr(s, "OPENAI_MODEL", "")
        if (base_url is None) or not str(base_url).strip():
            raise ValueError("OPENAI_BASE_URL must be set when LLM_PROVIDER is openai_compatible")
        if not isinstance(model, str) or not model.strip():
            raise ValueError("OPENAI_MODEL must be a non-empty string when LLM_PROVIDER is openai_compatible")

    # OpenAI-compatible embeddings ---------------------------------------------------------
    if s.EMBEDDING_PROVIDER == "openai_compatible":
        base_url = getattr(s, "OPENAI_BASE_URL", None)
        model = getattr(s, "EMBEDDING_MODEL", "")
        if (base_url is None) or not str(base_url).strip():
            raise ValueError(
                "OPENAI_BASE_URL must be set when EMBEDDING_PROVIDER is openai_compatible"
            )
        if not isinstance(model, str) or not model.strip():
            raise ValueError(
                "EMBEDDING_MODEL must be a non-empty string when EMBEDDING_PROVIDER is openai_compatible"
            )
