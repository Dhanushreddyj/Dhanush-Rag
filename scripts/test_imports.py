"""Quick sanity check — does the provider layer load without errors."""

from pathlib import Path
import sys, os
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("OPENAI_BASE_URL", "https://test.com")

from app.providers.base import LLMProvider, EmbeddingProvider, VectorStoreProvider
print("✓ Base interfaces loaded")

from app.providers.factory import get_llm_provider, get_embeddings_provider, get_vector_store_provider
print("✓ Factory loaded")

from app.embeddings import get_embeddings
print("✓ embeddings module loaded")

from app.vector_store import get_vector_store
print("✓ vector_store module loaded")

from app.llm_service import get_llm
print("✓ llm_service module loaded")

print("\nAll imports OK.")
