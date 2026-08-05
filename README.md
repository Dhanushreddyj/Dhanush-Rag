# Real Estate RAG - Python Backend

A production-ready Python RAG backend for real-estate buying and selling activities, designed to integrate with your existing JavaScript chatbot.

## Features

- FastAPI REST API with OpenAPI docs
- Document ingestion (PDF, TXT, DOCX)
- ChromaDB vector database
- OpenAI embeddings and LLM
- Retrieval + grounded answer generation
- Metadata filtering for real-estate documents
- Docker support

## Quick Start

### 1. Clone and Setup

```bash
cd python-rag-project
cp env_example.txt .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-...
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create Sample Data (Optional)

```bash
python scripts/build_sample_data.py
```

### 4. Ingest Documents

```bash
python scripts/ingest_documents.py
```

### 5. Start the Server

```bash
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

## API Endpoints

### Health Check

```bash
GET http://localhost:8000/health
```

### Query (RAG)

```bash
POST http://localhost:8000/query
Content-Type: application/json

{
  "query": "What documents do I need to buy a property?",
  "top_k": 5
}
```

### Retrieve Only

```bash
POST http://localhost:8000/retrieve
Content-Type: application/json

{
  "query": "property registration process",
  "top_k": 3
}
```

### Ingest Documents

```bash
POST http://localhost:8000/ingest
Content-Type: application/json

{
  "docs_dir": "./data/documents",
  "chunk_size": 1000,
  "chunk_overlap": 150
}
```

### List Sources

```bash
GET http://localhost:8000/sources
```

## JavaScript Integration

```javascript
// Query the RAG service
const response = await fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'What should I check before buying land?',
    top_k: 5
  })
});

const data = await response.json();
console.log(data.answer);
console.log(data.sources);
```

## Docker Deployment

```bash
# Build and run
docker-compose up --build

# Or run individually
docker build -t real-estate-rag .
docker run -p 8000:8000 --env-file .env real-estate-rag
```

## Project Structure

```
python-rag-project/
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── config.py        # Configuration
│   ├── schemas.py       # Pydantic models
│   ├── loaders.py       # Document loaders
│   ├── embeddings.py    # OpenAI embeddings
│   ├── vector_store.py  # ChromaDB management
│   ├── llm_service.py   # LLM wrapper
│   ├── rag_service.py   # RAG pipeline
│   ├── ingest.py        # Ingestion logic
│   └── utils.py         # Utilities
├── data/
│   ├── documents/       # Source documents
│   └── chroma/          # Vector index
├── scripts/
│   ├── ingest_documents.py
│   └── build_sample_data.py
├── requirements.txt
├── .env
├── Dockerfile
└── docker-compose.yml
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | LLM model | `gpt-4o-mini` |
| `EMBEDDING_MODEL` | Embedding model | `text-embedding-3-small` |
| `TOP_K` | Chunks to retrieve | `5` |
| `MAX_CHUNK_SIZE` | Chunk size | `1000` |
| `CHUNK_OVERLAP` | Chunk overlap | `150` |

## Next Steps

1. Add your real estate documents to `data/documents/`
2. Run ingestion script
3. Test queries via API or Swagger UI
4. Integrate with your JavaScript chatbot

## License

MIT