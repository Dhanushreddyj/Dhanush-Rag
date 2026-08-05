"""Quick sanity check — does the provider layer load without errors."""

import os
import sys
from pathlib import Path

# Ensure the repository root is on sys.path so `import app` works.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("OPENAI_BASE_URL", "https://test.com")

from app.providers.base import LLMProvider, EmbeddingProvider, VectorStoreProvider  # noqa: E402 — intentional side-free import for testing
print("✓ Base interfaces loaded")

from app.providers.factory import get_llm_provider, get_embeddings_provider, get_vector_store_provider
print("✓ Factory loaded")

from app.embeddings import get_embeddings
print("✓ embeddings module loaded")

from app.vector_store import get_vector_store
print("✓ vector_store module loaded")

from app.llm_service import get_llm_provider
print("✓ llm_service module loaded")

print("\nAll imports OK.")
