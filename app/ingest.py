"""
Document ingestion pipeline
"""

import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings
from app.loaders import load_directory
from app.vector_store import add_documents, get_vector_store
from app.schemas import IngestedDocument


def split_documents(
    documents: List,
    chunk_size: int = None,
    chunk_overlap: int = None,
) -> List:
    """
    Split documents into chunks
    """
    chunk_size = chunk_size or settings.MAX_CHUNK_SIZE
    chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    return text_splitter.split_documents(documents)


def generate_chunk_ids(documents: List, doc_id: str) -> List[str]:
    """
    Generate unique chunk IDs
    """
    return [f"{doc_id}_chunk_{i}" for i in range(len(documents))]


def ingest_documents_from_directory(
    docs_dir: str = None,
    chunk_size: int = None,
    chunk_overlap: int = None,
) -> Dict[str, Any]:
    """
    Ingest all documents from a directory
    """
    docs_dir = docs_dir or str(settings.DOCS_DIR)

    print(f"Starting ingestion from: {docs_dir}")

    # Load documents
    raw_documents = load_directory(docs_dir)

    if not raw_documents:
        return {
            "status": "no_documents",
            "message": "No documents found to ingest",
            "documents": [],
            "total_chunks": 0,
            "timestamp": datetime.now(),
        }

    # Group by source file
    docs_by_file = {}
    for doc in raw_documents:
        filepath = doc.metadata.get("filepath", "unknown")
        if filepath not in docs_by_file:
            docs_by_file[filepath] = []
        docs_by_file[filepath].append(doc)

    # Process each file
    ingested_docs = []
    total_chunks = 0

    for filepath, file_docs in docs_by_file.items():
        doc_id = str(uuid.uuid4())
        filename = Path(filepath).name
        doc_type = file_docs[0].metadata.get("doc_type", "general")

        # Add ingestion metadata
        for doc in file_docs:
            doc.metadata["doc_id"] = doc_id
            doc.metadata["filename"] = filename
            doc.metadata["doc_type"] = doc_type
            doc.metadata["ingested_at"] = datetime.now().isoformat()

        # Split into chunks
        chunked_docs = split_documents(file_docs, chunk_size, chunk_overlap)

        # Generate IDs
        chunk_ids = generate_chunk_ids(chunked_docs, doc_id)

        # Add to vector store
        add_documents(chunked_docs, ids=chunk_ids)

        # Track ingestion
        ingested_docs.append(
            IngestedDocument(
                doc_id=doc_id,
                filename=filename,
                doc_type=doc_type,
                chunks_count=len(chunked_docs),
                status="success",
            )
        )

        total_chunks += len(chunked_docs)

        print(f"Ingested: {filename} ({len(chunked_docs)} chunks)")

    # Get collection stats
    vector_store = get_vector_store()
    collection = vector_store.get_collection()
    final_count = collection.count()

    return {
        "status": "success",
        "message": f"Successfully ingested {len(ingested_docs)} documents",
        "documents": ingested_docs,
        "total_chunks": total_chunks,
        "total_in_collection": final_count,
        "timestamp": datetime.now(),
    }


def clear_and_reingest(
    docs_dir: str = None,
    chunk_size: int = None,
    chunk_overlap: int = None,
) -> Dict[str, Any]:
    """
    Clear vector store and re-ingest all documents
    """
    from app.vector_store import delete_collection

    print("Clearing vector store...")
    delete_collection()

    print("Re-ingesting documents...")
    return ingest_documents_from_directory(docs_dir, chunk_size, chunk_overlap)