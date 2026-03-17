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