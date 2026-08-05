"""
Utility functions for the RAG service
"""

import re
import hashlib
from typing import List, Dict, Any
from datetime import datetime


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    """
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove special characters but keep basic punctuation
    text = re.sub(r"[^\w\s.,!?;:()\-]", "", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def truncate_text(text: str, max_length: int = 500) -> str:
    """
    Truncate text to max length with ellipsis
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - 3] + "..."


def extract_metadata_from_text(text: str) -> Dict[str, Any]:
    """
    Extract basic metadata from text
    """
    return {
        "char_count": len(text),
        "word_count": len(text.split()),
        "sentence_count": text.count(".") + text.count("!") + text.count("?"),
        "processed_at": datetime.now().isoformat(),
    }


def generate_text_hash(text: str) -> str:
    """
    Generate a hash for text deduplication
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def format_chunk_for_display(
    chunk_text: str,
    metadata: Dict[str, Any],
    show_metadata: bool = True,
) -> str:
    """
    Format a chunk for display in logs or UI
    """
    lines = []

    if show_metadata:
        lines.append(f"File: {metadata.get('filename', 'Unknown')}")
        lines.append(f"Type: {metadata.get('doc_type', 'Unknown')}")
        lines.append(f"Length: {len(chunk_text)} chars")
        lines.append("-" * 40)

    lines.append(chunk_text)

    return "\n".join(lines)


def batch_items(items: List[Any], batch_size: int) -> List[List[Any]]:
    """
    Split items into batches
    """
    return [
        items[i : i + batch_size] for i in range(0, len(items), batch_size)
    ]


def safe_get(d: Dict, key: str, default: Any = None) -> Any:
    """
    Safely get a value from a nested dictionary
    """
    keys = key.split(".")
    value = d

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default

    return value


def merge_metadata(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two metadata dictionaries
    """
    merged = base.copy()
    merged.update(override)
    return merged