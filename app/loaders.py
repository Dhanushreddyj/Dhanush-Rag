"""
Document loaders for PDF, TXT, DOCX, and other formats
"""

import os
from pathlib import Path
from typing import List, Dict, Any
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    DirectoryLoader,
)
from langchain_core.documents import Document


def load_document(file_path: str) -> List[Document]:
    """
    Load a single document based on file extension
    """
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".pdf":
        loader = PyPDFLoader(str(path))
    elif ext == ".txt":
        loader = TextLoader(str(path), encoding="utf-8")
    elif ext == ".docx":
        loader = Docx2txtLoader(str(path))
    else:
        # Fallback: try text loader
        loader = TextLoader(str(path), encoding="utf-8", errors="ignore")

    return loader.load()


def load_directory(
    docs_dir: str,
    glob_pattern: str = "**/*",
    show_progress: bool = True,
) -> List[Document]:
    """
    Load all documents from a directory
    """
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        raise FileNotFoundError(f"Documents directory not found: {docs_dir}")

    all_documents = []
    files_processed = 0

    for file_path in docs_path.glob(glob_pattern):
        if file_path.is_file() and not file_path.name.startswith("."):
            try:
                docs = load_document(str(file_path))

                # Add metadata
                for doc in docs:
                    doc.metadata["filename"] = file_path.name
                    doc.metadata["filepath"] = str(file_path)
                    doc.metadata["doc_type"] = infer_doc_type(file_path.name)

                all_documents.extend(docs)
                files_processed += 1

                if show_progress:
                    print(f"Loaded: {file_path.name} ({len(docs)} chunks)")

            except Exception as e:
                print(f"Error loading {file_path.name}: {e}")

    print(f"Total files loaded: {files_processed}")
    print(f"Total documents: {len(all_documents)}")

    return all_documents


def infer_doc_type(filename: str) -> str:
    """
    Infer document type from filename
    """
    filename_lower = filename.lower()

    if any(word in filename_lower for word in ["sale", "agreement", "contract"]):
        return "sale_agreement"
    elif any(word in filename_lower for word in ["lease", "rental", "tenant"]):
        return "lease_agreement"
    elif any(word in filename_lower for word in ["title", "deed", "ownership"]):
        return "title_deed"
    elif any(word in filename_lower for word in ["faq", "guide", "help"]):
        return "faq"
    elif any(word in filename_lower for word in ["property", "listing", "details"]):
        return "property_details"
    elif any(word in filename_lower for word in ["legal", "law", "regulation"]):
        return "legal"
    else:
        return "general"