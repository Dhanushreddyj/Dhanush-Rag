"""
Script to ingest documents from the command line
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ingest import ingest_documents_from_directory, clear_and_reingest
from app.config import settings


def main():
    parser = argparse.ArgumentParser(
        description="Ingest documents into the RAG vector store"
    )

    parser.add_argument(
        "--docs-dir",
        type=str,
        default=str(settings.DOCS_DIR),
        help=f"Documents directory (default: {settings.DOCS_DIR})",
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=settings.MAX_CHUNK_SIZE,
        help=f"Chunk size (default: {settings.MAX_CHUNK_SIZE})",
    )

    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=settings.CHUNK_OVERLAP,
        help=f"Chunk overlap (default: {settings.CHUNK_OVERLAP})",
    )

    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear vector store before ingestion",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Real Estate RAG - Document Ingestion")
    print("=" * 60)
    print(f"Documents directory: {args.docs_dir}")
    print(f"Chunk size: {args.chunk_size}")
    print(f"Chunk overlap: {args.chunk_overlap}")
    print(f"Clear before ingest: {args.clear}")
    print("=" * 60)

    if args.clear:
        print("\nClearing vector store and re-ingesting...\n")
        result = clear_and_reingest(
            docs_dir=args.docs_dir,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
        )
    else:
        print("\nStarting ingestion...\n")
        result = ingest_documents_from_directory(
            docs_dir=args.docs_dir,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
        )

    print("\n" + "=" * 60)
    print("Ingestion Complete")
    print("=" * 60)
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    print(f"Documents ingested: {len(result['documents'])}")
    print(f"Total chunks: {result['total_chunks']}")
    if "total_in_collection" in result:
        print(f"Total in collection: {result['total_in_collection']}")
    print("=" * 60)


if __name__ == "__main__":
    main()