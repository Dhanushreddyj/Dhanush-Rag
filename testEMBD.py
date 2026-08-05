from app.embeddings import get_embeddings

embeddings = get_embeddings()

result = embeddings.embed_query(
    "A residential property in Hyderabad"
)

print("Embedding dimensions:", len(result))
print(result[:5])
