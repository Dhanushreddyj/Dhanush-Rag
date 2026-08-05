"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class HealthResponse(BaseModel):
    service: str
    status: str
    version: str


class QueryRequest(BaseModel):
    query: str = Field(..., description="User question")
    filters: Optional[Dict[str, Any]] = Field(
        default=None, description="Metadata filters for retrieval"
    )
    top_k: Optional[int] = Field(default=None, description="Number of chunks to retrieve")


class SourceDocument(BaseModel):
    text: str
    metadata: Dict[str, Any]
    score: Optional[float] = None


class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[SourceDocument]
    count: int
    model_used: str
    timestamp: datetime = Field(default_factory=datetime.now)
    model_config ={
        "protected_namespaces": ()
    }

class RetrieveRequest(BaseModel):
    query: str = Field(..., description="Query text")
    filters: Optional[Dict[str, Any]] = Field(
        default=None, description="Metadata filters"
    )
    top_k: Optional[int] = Field(default=None, description="Number of chunks")


class RetrieveResponse(BaseModel):
    query: str
    documents: List[SourceDocument]
    count: int


class IngestRequest(BaseModel):
    docs_dir: Optional[str] = Field(default=None, description="Documents directory")
    chunk_size: Optional[int] = Field(default=None, description="Chunk size")
    chunk_overlap: Optional[int] = Field(default=None, description="Chunk overlap")


class IngestedDocument(BaseModel):
    doc_id: str
    filename: str
    doc_type: str
    chunks_count: int
    status: str


class IngestResponse(BaseModel):
    status: str
    message: str
    documents: List[IngestedDocument]
    total_chunks: int
    timestamp: datetime = Field(default_factory=datetime.now)
