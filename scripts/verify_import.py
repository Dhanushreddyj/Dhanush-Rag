"""Verify that importing settings does not trigger validation."""
import sys
sys.path.insert(0, "/Users/dhanushreddyjanagama/Developer/NOFEEZ RAG/app")

try:
    from config import settings
    print("SUCCESS: Import OK — no validation ran")
    print(f"LLM provider: {repr(settings.LLM_PROVIDER)}")
except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)