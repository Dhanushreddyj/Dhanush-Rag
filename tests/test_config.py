import pytest
import app.config as config_module
from app.config import Settings, validate_settings


def _valid_settings(**overrides):
    """Return a fully valid Settings instance with explicit defaults for every field."""
    base = {
        "ENV": "production",
        "LLM_PROVIDER": "bedrock",
        "EMBEDDING_PROVIDER": "bedrock",
        "VECTOR_STORE_PROVIDER": "qdrant",
        "QDRANT_HOST": "localhost",
        "TOP_K": 5,
        "MAX_CHUNK_SIZE": 1000,
        "CHUNK_OVERLAP": 150,
        "EMBEDDING_DIMENSION": 1536,
        "MIN_QUERY_LENGTH": 3,
        "MAX_QUERY_LENGTH": 2048,
        "MAX_CONTEXT_DOCS": 10,
        "RATE_LIMIT_PER_MINUTE": 60,
        "RATE_LIMIT_WINDOW_SECONDS": 60.0,
        "CACHE_TTL_SECONDS": 300,
        "MAX_CACHE_SIZE": 1000,
        "QDRANT_URL": None,
        "QDRANT_COLLECTION_NAME": "default",
        "OPENAI_API_KEY": None,
        "OPENAI_MODEL": "",
        "OPENAI_BASE_URL": None,
        "CHROMA_PERSISTENCE": True,
        "LOG_LEVEL": "INFO",
        "LOG_FORMAT": "json",
    }
    base.update(overrides)
    return Settings(**base)


def test_valid_candidate():
    """A fully valid Settings candidate should pass validation."""
    # Local Qdrant: URL absent and host nonblank.
    s = _valid_settings(
        ENV="production",
        LLM_PROVIDER="bedrock",
        EMBEDDING_PROVIDER="bedrock",
        VECTOR_STORE_PROVIDER="qdrant",
        QDRANT_HOST="localhost",
        TOP_K=5,
        MAX_CHUNK_SIZE=1000,
        CHUNK_OVERLAP=150,
    )
    validate_settings(s)

    # Cloud Qdrant: URL nonblank and host blank.
    s = _valid_settings(
        ENV="production",
        LLM_PROVIDER="bedrock",
        EMBEDDING_PROVIDER="bedrock",
        VECTOR_STORE_PROVIDER="qdrant",
        QDRANT_URL="https://cloud.qdrant.com",
        QDRANT_HOST="",
        TOP_K=5,
        MAX_CHUNK_SIZE=1000,
        CHUNK_OVERLAP=150,
    )
    validate_settings(s)


def test_global_settings_wrapper(monkeypatch):
    """validate_settings() should use the module-level settings instance."""

    monkeypatch.setattr(config_module, "settings", _valid_settings())
    config_module.validate_settings()
    validate_settings()


@pytest.mark.parametrize(
    "field_name,invalid_value",
    [
        ("TOP_K", -1),
        ("TOP_K", 0),
        ("MAX_CHUNK_SIZE", -1),
        ("MAX_CHUNK_SIZE", 0),
        ("EMBEDDING_DIMENSION", -1),
        ("EMBEDDING_DIMENSION", 0),
        ("MIN_QUERY_LENGTH", -1),
        ("MIN_QUERY_LENGTH", 0),
        ("MAX_QUERY_LENGTH", -1),
        ("MAX_QUERY_LENGTH", 0),
        ("MAX_CONTEXT_DOCS", -1),
        ("MAX_CONTEXT_DOCS", 0),
        ("RATE_LIMIT_PER_MINUTE", -1),
        ("RATE_LIMIT_PER_MINUTE", 0),
        ("RATE_LIMIT_WINDOW_SECONDS", -1),
        ("RATE_LIMIT_WINDOW_SECONDS", 0),
        ("CACHE_TTL_SECONDS", -1),
        ("CACHE_TTL_SECONDS", 0),
        ("MAX_CACHE_SIZE", -1),
        ("MAX_CACHE_SIZE", 0),
    ],
)
def test_nonpositive_numeric_invariants(field_name, invalid_value):
    """Numeric invariants: all positive-integer fields must reject non-positive values."""
    s = _valid_settings(
        ENV="production",
        LLM_PROVIDER="bedrock",
        EMBEDDING_PROVIDER="bedrock",
        VECTOR_STORE_PROVIDER="qdrant",
        QDRANT_HOST="localhost",
        **{field_name: invalid_value},
    )
    with pytest.raises(ValueError) as exc:
        validate_settings(s)
    assert field_name in str(exc.value)


@pytest.mark.parametrize(
    "chunk_overlap,max_chunk_size,error_msg",
    [
        (-1, 1000, "CHUNK_OVERLAP must be greater than or equal to zero and less than MAX_CHUNK_SIZE"),
        (1000, 1000, "CHUNK_OVERLAP must be greater than or equal to zero and less than MAX_CHUNK_SIZE"),
        (1500, 1000, "CHUNK_OVERLAP must be greater than or equal to zero and less than MAX_CHUNK_SIZE"),
    ],
)
def test_invalid_chunk_overlap(chunk_overlap, max_chunk_size, error_msg):
    s = _valid_settings(
        ENV="production",
        LLM_PROVIDER="bedrock",
        EMBEDDING_PROVIDER="bedrock",
        VECTOR_STORE_PROVIDER="qdrant",
        QDRANT_HOST="localhost",
        MAX_CHUNK_SIZE=max_chunk_size,
        CHUNK_OVERLAP=chunk_overlap,
    )
    with pytest.raises(ValueError) as exc:
        validate_settings(s)
    assert error_msg in str(exc.value)


def test_invalid_query_length_order():
    s = _valid_settings(
        ENV="production",
        LLM_PROVIDER="bedrock",
        EMBEDDING_PROVIDER="bedrock",
        VECTOR_STORE_PROVIDER="qdrant",
        QDRANT_HOST="localhost",
        MIN_QUERY_LENGTH=10,
        MAX_QUERY_LENGTH=5,
    )
    with pytest.raises(ValueError) as exc:
        validate_settings(s)
    assert "MIN_QUERY_LENGTH must be less than or equal to MAX_QUERY_LENGTH" in str(
        exc.value
    )


@pytest.mark.parametrize(
    "field,invalid_value",
    [
        ("ENV", ""),
        ("ENV", "  "),
        ("LLM_PROVIDER", ""),
        ("LLM_PROVIDER", "\t"),
        ("EMBEDDING_PROVIDER", ""),
        ("EMBEDDING_PROVIDER", "   "),
        ("QDRANT_COLLECTION_NAME", ""),
        ("QDRANT_COLLECTION_NAME", " \n "),
    ],
)
def test_blank_required_strings(field, invalid_value):
    s = _valid_settings(**{field: invalid_value})
    with pytest.raises(ValueError) as exc:
        validate_settings(s)
    assert f"{field} must be a non-empty string" in str(exc.value)


@pytest.mark.parametrize(
    "vector_store_provider,error_msg",
    [
        ("chroma", "VECTOR_STORE_PROVIDER must be exactly 'qdrant'"),
        ("pinecone", "VECTOR_STORE_PROVIDER must be exactly 'qdrant'"),
        ("weavemetric", "VECTOR_STORE_PROVIDER must be exactly 'qdrant'"),
    ],
)
def test_non_qdrant_vector_store_rejected(vector_store_provider, error_msg):
    s = _valid_settings(
        ENV="production",
        LLM_PROVIDER="bedrock",
        EMBEDDING_PROVIDER="bedrock",
        VECTOR_STORE_PROVIDER=vector_store_provider,
        QDRANT_HOST="localhost",
    )
    with pytest.raises(ValueError) as exc:
        validate_settings(s)
    assert error_msg in str(exc.value)


def test_qdrant_connection_configuration_required():
    s = _valid_settings(
        ENV="production",
        LLM_PROVIDER="bedrock",
        EMBEDDING_PROVIDER="bedrock",
        VECTOR_STORE_PROVIDER="qdrant",
        QDRANT_URL=None,
        QDRANT_HOST="",
    )
    with pytest.raises(ValueError) as exc:
        validate_settings(s)
    assert "QDRANT_URL must be set or QDRANT_HOST must be a non-empty string" in str(
        exc.value
    )


@pytest.mark.parametrize(
    "base_url,model,error_msg",
    [
        (None, "gpt-4o-mini", "OPENAI_BASE_URL must be set"),
        ("", "gpt-4o-mini", "OPENAI_BASE_URL must be set"),
        ("http://lm-studio:6001", "", "OPENAI_MODEL must be a non-empty string"),
        ("http://lm-studio:6001", "  ", "OPENAI_MODEL must be a non-empty string"),
    ],
)
def test_openai_compatible_llm_requirements(base_url, model, error_msg):
    s = _valid_settings(
        ENV="production",
        LLM_PROVIDER="openai_compatible",
        EMBEDDING_PROVIDER="bedrock",
        VECTOR_STORE_PROVIDER="qdrant",
        QDRANT_HOST="localhost",
        OPENAI_BASE_URL=base_url,
        OPENAI_MODEL=model,
    )
    with pytest.raises(ValueError) as exc:
        validate_settings(s)
    assert error_msg in str(exc.value)


@pytest.mark.parametrize(
    "base_url,model,error_msg",
    [
        (None, "text-embedding-3-small", "OPENAI_BASE_URL must be set"),
        ("", "text-embedding-3-small", "OPENAI_BASE_URL must be set"),
        ("http://lm-studio:6001", "", "EMBEDDING_MODEL must be a non-empty string"),
        ("http://lm-studio:6001", "  ", "EMBEDDING_MODEL must be a non-empty string"),
    ],
)
def test_openai_compatible_embedding_requirements(base_url, model, error_msg):
    s = _valid_settings(
        ENV="production",
        LLM_PROVIDER="bedrock",
        EMBEDDING_PROVIDER="openai_compatible",
        VECTOR_STORE_PROVIDER="qdrant",
        QDRANT_HOST="localhost",
        OPENAI_BASE_URL=base_url,
        EMBEDDING_MODEL=model,
    )
    with pytest.raises(ValueError) as exc:
        validate_settings(s)
    assert error_msg in str(exc.value)


def test_non_openai_compatible_configuration_succeeds():
    s = _valid_settings(
        ENV="production",
        LLM_PROVIDER="bedrock",
        EMBEDDING_PROVIDER="bedrock",
        VECTOR_STORE_PROVIDER="qdrant",
        QDRANT_HOST="localhost",
        OPENAI_BASE_URL=None,
        OPENAI_MODEL="",
    )
    validate_settings(s)