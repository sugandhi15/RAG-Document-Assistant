from ingest import load_documents
from ingest import create_chunks

from rag import (
    create_embeddings,
    build_faiss_index,
    save_index,
    save_chunks
)

docs = load_documents("data")

chunks = create_chunks(docs)

embeddings = create_embeddings(chunks)

index = build_faiss_index(embeddings)

save_index(index)

save_chunks(chunks)

print("Database Created Successfully!")