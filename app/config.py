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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create settings instance
settings = Settings()


def validate_settings():
    """Validate configuration based on selected providers."""
    if settings.LLM_PROVIDER == "openai_compatible" and not settings.OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY is required for openai_compatible LLM provider. "
            "Set it in your .env file or export OPENAI_API_KEY."
        )

    if settings.LLM_PROVIDER == "bedrock":
        import boto3
        try:
            boto3.client("bedrock-runtime")
        except Exception as e:
            raise ValueError(
                "AWS credentials are required for Bedrock provider. "
                "Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY or configure via aws configure."
            ) from e

    if settings.EMBEDDING_PROVIDER == "openai_compatible" and not settings.OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY is required for openai_compatible embedding provider. "
            "Set it in your .env file or export OPENAI_API_KEY."
        )

    if settings.EMBEDDING_PROVIDER == "bedrock":
        import boto3
        try:
            boto3.client("bedrock-runtime")
        except Exception as e:
            raise ValueError(
                "AWS credentials are required for Bedrock embedding provider. "
                "Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY or configure via aws configure."
            ) from e

    # Ensure directories exist
    settings.CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    settings.DOCS_DIR.mkdir(parents=True, exist_ok=True)

# NOTE: validate_settings() is called explicitly from app/main.py during application startup.
# Importing this module should never make network calls or raise exceptions.
