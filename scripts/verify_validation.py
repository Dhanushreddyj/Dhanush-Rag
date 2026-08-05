"""Verify validate_settings() works correctly."""

import os
import sys
from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_test(env_vars: dict, expect_error: bool):
    """Run a validation test in an isolated Python process.

    Args:
        env_vars: environment variables to set for the child process.
        expect_error: True if we expect validate_settings() to raise ValueError.
    """
    cmd = [sys.executable, "-c", "from app.config import settings, validate_settings; validate_settings()"]
    env = os.environ.copy()
    env.update(env_vars)

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT), env=env)
    passed = (result.returncode != 0) == expect_error
    status = "PASS" if passed else "FAIL"
    print(f"{status}: {result.stderr.strip()[:120] or '(no output)'}")


if __name__ == "__main__":
    # Test 1: Current env should pass (LM STUDIO + openai_compatible)
    print("Test 1 — current env (should PASS):", end=" ")
    run_test(
        {
            "OPENAI_API_KEY": "test-key",
            "OPENAI_BASE_URL": "https://test.com",
            "LLM_PROVIDER": "openai_compatible",
            "EMBEDDING_PROVIDER": "openai_compatible",
            "VECTOR_STORE_PROVIDER": "qdrant",
        },
        expect_error=False,
    )

    # Test 2: Missing API key should fail
    print("Test 2 — missing key (should FAIL):", end=" ")
    run_test(
        {
            "OPENAI_API_KEY": "",
            "OPENAI_BASE_URL": "https://test.com",
            "LLM_PROVIDER": "openai_compatible",
            "EMBEDDING_PROVIDER": "openai_compatible",
            "VECTOR_STORE_PROVIDER": "qdrant",
        },
        expect_error=True,
    )

    # Test 3: Bedrock provider should require AWS creds
    print("Test 3 — no AWS creds (should FAIL):", end=" ")
    run_test(
        {
            "OPENAI_API_KEY": "",
            "OPENAI_BASE_URL": "https://test.com",
            "LLM_PROVIDER": "bedrock",
            "EMBEDDING_PROVIDER": "openai_compatible",
            "VECTOR_STORE_PROVIDER": "qdrant",
        },
        expect_error=True,
    )

    print("\nAll tests completed.")
