"""Verify validate_settings() works correctly."""
import sys, os
sys.path.insert(0, "/Users/dhanushreddyjanagama/Developer/NOFEEZ RAG/app")

from config import settings, validate_settings

# Test 1: Current env should pass (LM STUDIO + openai_compatible)
print("Test 1 — current env (should PASS):", end=" ")
try:
    validate_settings()
    print("PASS")
except Exception as e:
    print(f"FAIL: {e}")

# Test 2: Missing API key should fail
os.environ["OPENAI_API_KEY"] = ""
print("Test 2 — missing key (should FAIL):", end=" ")
try:
    validate_settings()
    print("FAIL — no exception raised")
except ValueError as e:
    if "API_KEY" in str(e):
        print("PASS")
    else:
        print(f"FAIL: wrong error: {e}")

# Test 3: Bedrock provider should require AWS creds
os.environ["LLM_PROVIDER"] = "bedrock"
print("Test 3 — no AWS creds (should FAIL):", end=" ")
try:
    validate_settings()
    print("FAIL — no exception raised")
except ValueError as e:
    if "AWS credentials" in str(e):
        print("PASS")
    else:
        print(f"FAIL: wrong error: {e}")

print("\nAll tests completed.")