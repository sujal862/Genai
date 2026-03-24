
# Basic: RAG

                ┌──────────────────────────┐
                │       DATA SOURCE        │
                │  PDFs / Docs / Website   │
                └─────────────┬────────────┘
                              │
                              ▼
                    ┌──────────────────────────┐
                    │    CHUNKING              │
                    │ Split text into          │
                    │ small pieces(indexing)   │
                    └────────┬─────────────────┘
                             │
                             ▼
                     ┌──────────────┐
                     │  EMBEDDINGS  │
                     │ text → vector│
                     └───────┬──────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │     VECTOR STORE     │
                 │ Pinecone / FAISS /   │
                 │ Chroma / Weaviate    │
                 └─────────┬────────────┘
                           │
                           │ (similarity search)
                           ▼
        USER QUESTION → EMBEDDING → SEARCH VECTOR DB
                           │
                           ▼
                ┌──────────────────────┐
                │   RELEVANT CHUNKS    │
                │   top-k documents    │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │        LLM           │
                │  (GPT / Llama etc)   │
                └─────────┬────────────┘
                          │
                          ▼
                       RESPONSE


---------------------------------------------------------------------------------------------------------------------------------

# Qdrant : manual way vs high level way

high level way :using langchain see in 02_rag_1/py

manual way :

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid

# 1. Connect to the "Database"
# This tells our script where the Qdrant engine is running 
client = QdrantClient(url="http://localhost:6333")
collection_name = "kubernetes-official-docs"

# 2. Create a "Bucket" (Collection) for our data
# recreate_collection deletes any old version and starts fresh.
# We set 'size=1536' because that's the specific "length" of OpenAI's embedding vectors ('text-embedding-3-small').
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# 3. Turn text into Math (Embeddings)
# We pull just the text from our split documents and send them to OpenAI.
# This gives us a list of vecotr Embeddings for all chunks at once
texts = [doc.page_content for doc in split_docs]
vectors = embedder.embed_documents(texts)

# 4. Prepare "Points" for Qdrant
# Qdrant stores things as 'Points'. Each point needs an ID, the Vector, and the actual Text (Payload).
points = []
# We 'zip' them so the 1st text chunk matches the 1st vector, the 2nd with the 2nd, etc.
for i, (doc, vector) in enumerate(zip(split_docs, vectors)):
    points.append(
        PointStruct(
            id=str(uuid.uuid4()), # Generates a unique ID for every chunk
            vector=vector,
            payload={
                "page_content": doc.page_content, # The actual text chunk
                "metadata": doc.metadata, # This keeps your PDF page numbers!
            }
        )
    )

# 5. Upload to Qdrant
# We send the entire list of 'points' at once. This is much faster than sending one by one.
client.upsert(
    collection_name=collection_name,
    points=points
)

print(f"Successfully uploaded {len(points)} chunks to Qdrant!")


-----------------------------------------------------------------------------------------------------------------------------------

# LLM Router: (after 09_)
An LLM Router is a system that automatically directs incoming queries to the most appropriate LLM (or model variant) based on some criteria — instead of always using one fixed model.
Why it exists: Not every query needs GPT-4o or Claude Opus. Simple questions can be handled by cheaper/faster models, while complex ones need the heavy hitters. A router optimizes for cost, speed, and quality.