"""Verify that importing settings does not trigger validation."""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("OPENAI_BASE_URL", "https://test.com")

try:
    from app.config import settings
    print("SUCCESS: Import OK — no validation ran")
    print(f"LLM provider: {repr(settings.LLM_PROVIDER)}")
except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
