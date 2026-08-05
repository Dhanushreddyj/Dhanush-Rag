"""
Real Estate RAG - FastAPI Main Entry Point
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.schemas import (
    HealthResponse,
    QueryRequest,
    QueryResponse,
    IngestRequest,
    IngestResponse,
    RetrieveRequest,
    RetrieveResponse,
)
from app.rag_service import ask_rag
from app.ingest import ingest_documents_from_directory
from app.vector_store import get_vector_store
from app.middleware import create_rate_limit_middleware
from app.validators import validate_query, validate_filters

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Python RAG backend for real-estate documents",
    version="1.0.0",
)

# Add CORS middleware for JavaScript integration
app.add_middleware(
    FastAPICORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
app.add_middleware(create_rate_limit_middleware(app))

# ============================================================
# Lifespan events
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.config import validate_settings

    # Startup — validate configuration before starting services
    validate_settings()
    print(f"Starting {settings.APP_NAME}...")
    vector_store = get_vector_store()
    print("Vector store initialized.")
    yield
    # Shutdown
    print("Shutting down...")

app.router.lifespan_context = lifespan

# ============================================================
# API Endpoints
# ============================================================

@app.get("/", response_model=HealthResponse)
async def root():
    """
    Health check endpoint
    """
    return {
        "service": settings.APP_NAME,
        "status": "healthy",
        "version": "1.0.0",
    }

@app.get("/health", response_model=HealthResponse)
async def health():
    """
    Health check endpoint
    """
    return {
        "service": settings.APP_NAME,
        "status": "healthy",
        "version": "1.0.0",
    }

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Ask a RAG question and get a grounded answer with sources
    """
    # Validate the query
    validation_result = validate_query(request.query)
    if not validation_result.is_valid:
        raise HTTPException(
            status_code=400,
            detail="Invalid query",
            headers={"X-Validation-Errors": ",".join(validation_result.errors)},
        )

    # Validate filters if provided
    if request.filters:
        filter_validation = validate_filters(request.filters)
        if not filter_validation.is_valid:
            raise HTTPException(
                status_code=400,
                detail="Invalid filters",
                headers={"X-Validation-Errors": ",".join(filter_validation.errors)},
            )

    try:
        result = await ask_rag(
            query=request.query,
            filters=request.filters,
            top_k=request.top_k or settings.TOP_K,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_endpoint(request: RetrieveRequest):
    """
    Retrieve relevant chunks without generating an answer
    """
    try:
        vector_store = get_vector_store()
        results = vector_store.similarity_search(
            query=request.query,
            k=request.top_k or settings.TOP_K,
            filters=request.filters,
        )

        documents = [
            {
                "text": doc.page_content,
                "metadata": doc.metadata,
                "score": getattr(doc, "score", None),
            }
            for doc in results
        ]

        return {
            "query": request.query,
            "documents": documents,
            "count": len(documents),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest", response_model=IngestResponse)
async def ingest_endpoint(
    request: IngestRequest, background_tasks: BackgroundTasks
):
    """
    Ingest documents from the configured documents directory
    """
    try:
        result = await ingest_documents_from_directory(
            docs_dir=request.docs_dir or settings.DOCS_DIR,
            chunk_size=request.chunk_size or settings.MAX_CHUNK_SIZE,
            chunk_overlap=request.chunk_overlap or settings.CHUNK_OVERLAP,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sources")
async def list_sources():
    """
    List all ingested document sources
    """
    try:
        vector_store = get_vector_store()
        collection = vector_store.get_collection()
        all_metadata = collection.get(include=["metadatas"])

        sources = []
        seen_ids = set()

        for meta in all_metadata["metadatas"]:
            doc_id = meta.get("doc_id")
            if doc_id and doc_id not in seen_ids:
                seen_ids.add(doc_id)
                sources.append(
                    {
                        "doc_id": doc_id,
                        "filename": meta.get("filename"),
                        "doc_type": meta.get("doc_type"),
                        "ingested_at": meta.get("ingested_at"),
                    }
                )

        return {"sources": sources, "count": len(sources)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sources/{doc_id}")
async def get_source(doc_id: str):
    """
    Get metadata for a specific document
    """
    try:
        vector_store = get_vector_store()
        collection = vector_store.get_collection()
        all_metadata = collection.get(include=["metadatas"])

        for meta in all_metadata["metadatas"]:
            if meta.get("doc_id") == doc_id:
                return {
                    "doc_id": doc_id,
                    "filename": meta.get("filename"),
                    "doc_type": meta.get("doc_type"),
                    "total_chunks": meta.get("total_chunks"),
                    "ingested_at": meta.get("ingested_at"),
                }

        raise HTTPException(status_code=404, detail="Document not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================
# Run server
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )