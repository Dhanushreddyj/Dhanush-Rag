"""Qdrant Cloud smoke test — reads QDRANT_URL / QDRANT_API_KEY from app.config."""

import asyncio, sys
sys.path.insert(0, ".")

from app.config import settings
from app.providers.vectorstore.qdrant import QdrantVectorStoreProvider
from langchain_core.documents import Document


async def main():
    url = settings.QDRANT_URL
    api_key = settings.QDRANT_API_KEY or ""
    collection_name = "test_qdrant_sanity"

    if not url:
        print("SKIP — QDRANT_URL is not set in environment.")
        return

    provider = QdrantVectorStoreProvider(
        url=url,
        api_key=api_key,
        collection_name=collection_name,
    )

    # 1. Create collection (idempotent)
    await provider.create_collection()
    print("✓ Collection created")

    # 2. Add documents
    docs = [
        Document(
            page_content="Qdrant is a powerful vector database for AI applications.",
            metadata={"source": "sanity_test"},
        ),
        Document(
            page_content="The NoFeeZ platform helps manage property listings and sale agreements.",
            metadata={"source": "sanity_test"},
        ),
    ]
    await provider.add_documents(docs)
    print("✓ Documents added")

    # 3. Search
    results = await provider.similarity_search("vector database", k=1)
    assert len(results) == 1, f"Expected 1 result, got {len(results)}"
    assert "Qdrant" in results[0].page_content, f"Unexpected content: {results[0].page_content}"
    print(f"✓ Search OK — found: {results[0].page_content[:80]}")

    # 4. Cleanup
    await provider.delete_collection()
    print("✓ Collection deleted")


if __name__ == "__main__":
    asyncio.run(main())