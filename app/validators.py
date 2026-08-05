"""
Query validators for input sanitization and validation.
Ensures queries meet quality requirements before processing.
"""

import re
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ValidationError


class QueryValidationError(Exception):
    """Raised when a query fails validation."""

    def __init__(self, message: str, errors: Optional[List[str]] = None):
        self.message = message
        self.errors = errors or []
        super().__init__(message)


class QueryValidationResult(BaseModel):
    """Result of query validation."""
    is_valid: bool
    cleaned_query: str
    original_query: str
    filters: Optional[Dict[str, Any]] = None
    top_k: int = 5
    errors: list[str] = []


class QueryValidator:
    """Validates and sanitizes RAG queries."""

    # Characters that indicate low-quality queries
    LOW_QUALITY_PATTERNS = [
        r"^[\s]+$",  # Whitespace only
        r"^[?]+$",   # Question marks only
        r"^hi$|^hello$|^hey$",  # Greetings without query
        r"what is this?$",  # Vague "this" reference
    ]

    # Stop words that make a query low quality when used alone
    STOP_WORDS = {"is", "that", "this", "it", "me", "you"}

    def __init__(self, min_length: int = 3, max_length: int = 2048):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, query: str) -> QueryValidationResult:
        """Validate and clean a query string."""
        errors = []

        # Check length
        if len(query.strip()) < self.min_length:
            errors.append(f"Query too short. Minimum {self.min_length} characters.")
        elif len(query.strip()) > self.max_length:
            errors.append(f"Query too long. Maximum {self.max_length} characters.")

        # Check for low quality patterns
        cleaned = query.strip().lower()
        for pattern in self.LOW_QUALITY_PATTERNS:
            if re.match(pattern, cleaned):
                errors.append("Query appears to be low quality or incomplete.")
                break

        # Check for stop words dominating the query
        words = cleaned.split()
        stop_word_count = sum(1 for w in words if w in self.STOP_WORDS)
        if len(words) > 0 and stop_word_count / len(words) > 0.5:
            errors.append("Query is dominated by generic words.")

        # Clean the query
        cleaned_query = (
            re.sub(r"[^a-zA-Z0-9\s!?.,;:'\"-]", "", query.strip())
            .strip()
        )

        if errors:
            return QueryValidationResult(
                is_valid=False,
                cleaned_query=cleaned_query,
                original_query=query,
                errors=errors,
            )

        return QueryValidationResult(
            is_valid=True,
            cleaned_query=cleaned_query,
            original_query=query,
        )


class MetadataFilterValidator:
    """Validates metadata filters for vector store queries."""

    VALID_FILTER_TYPES = {
        "eq": str,
        "in": list,
        "gte": (int, float),
        "lte": (int, float),
        "gt": (int, float),
        "lt": (int, float),
        "contains": str,
    }

    def validate(self, filters: Dict[str, Any]) -> QueryValidationResult:
        """Validate metadata filter structure."""
        errors = []

        for key, value in filters.items():
            if not isinstance(key, str):
                errors.append(f"Filter keys must be strings. Got {type(key).__name__}.")
                continue

            # Check for reserved characters
            if any(c in key for c in [" ", ".", "/"]):
                errors.append(
                    f"Filter key '{key}' contains invalid characters."
                )
                continue

            # Validate filter value type
            if isinstance(value, dict):
                for op, val in value.items():
                    if op not in self.VALID_FILTER_TYPES:
                        errors.append(f"Invalid operator '{op}'.")
                    elif not isinstance(val, self.VALID_FILTER_TYPES.get(op)):
                        expected = self.VALID_FILTER_TYPES[op]
                        errors.append(
                            f"Filter '{key}' operator '{op}' expects {expected}, "
                            f"got {type(val).__name__}."
                        )

        return QueryValidationResult(
            is_valid=len(errors) == 0,
            cleaned_query="",
            original_query=str(filters),
            filters=filters if errors else None,
            errors=errors,
        )


# Module-level singleton instances
query_validator = QueryValidator(min_length=3, max_length=2048)
filter_validator = MetadataFilterValidator()


def validate_query(query: str) -> QueryValidationResult:
    """Validate a RAG query."""
    return query_validator.validate(query)


def validate_filters(filters: Dict[str, Any]) -> QueryValidationResult:
    """Validate metadata filters."""
    return filter_validator.validate(filters)