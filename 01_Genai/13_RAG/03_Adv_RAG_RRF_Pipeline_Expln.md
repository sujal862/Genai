(1) Enrich              (2) Retrieve              (3) RRF rank          (4) Answer
      +------------+        +------------------+        +-------------+      +------------+
      | User query |------->|       LLM        |        |             |      |            |
      +------------+        |genrat 3 morquery |        |             |      |            |
            |               +---------+--------+        |             |      |            |
            |                         |                 |             |      |            |
            |               +---------v--------+        |             |      |            |
            |               |  Original query  |------> |             |      |            |
            |               +------------------+        |             |      |            |
            |               +------------------+        |  Vector DB  |      |            |
            |               |    AI query 1    |------> |  similarity |      | RRF ranking|
            |               +------------------+        |  search on  |----->| (top ranked|
            |               +------------------+        |  4 queries  |      |   chunks)  |
            |               |    AI query 2    |------> |             |      +-----+------+
            |               +------------------+        |             |            |
            |               +------------------+        |             |            |
            |               |    AI query 3    |------> |             |            |
            |               +------------------+        +-------------+            |
            |                                                                      |
            |                                                           +----------v----------+
            |                                                           | Merged context doc  |
            |                                                           | (joined top ranked chunks) | 
            |                                                           +----------+----------+
            |                                                                      |
            |                  original query also sent to final LLM               |
            +-------------------------------------------------------------------->-v----------+
                                                                        |  LLM (final ans)    |
                                                                        |  query + context = response    |
                                                                        +---------------------+






 ╔══════════════════════════════════════════════════════════════╗
 ║          ADVANCED RAG — Multi-Query + RRF Pipeline           ║
 ╚══════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│  STEP 1 — Query Enrichment (Enrichment Node)                 │
├──────────────────────────────────────────────────────────────┤
│  • User sends 1 query                                        │
│  • Pass it to an LLM (e.g. Gemini / GPT)                     │
│  • LLM generates 3 MORE versions of the query                │
│  • Now you have 4 queries total                              │
│                                                              │
│  WHY? A single query might miss chunks that use different    │
│  wording. More queries = wider semantic coverage.            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  STEP 2 — Parallel Similarity Search (Vector DB)             │
├──────────────────────────────────────────────────────────────┤
│  • Run similarity search in vector DB for ALL 4 queries      │
│  • Each query returns its own list of chunks (e.g. top-5)    │
│  • You now have 4 ranked lists of chunks                     │
│                                                              │
│  Result:                                                     │
│    Query 1 → [chunkA, chunkC, chunkF, ...]                   │
│    Query 2 → [chunkA, chunkB, chunkD, ...]                   │
│    Query 3 → [chunkC, chunkA, chunkE, ...]                   │
│    Query 4 → [chunkB, chunkA, chunkG, ...]                   │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  STEP 3 — Reciprocal Rank Fusion (RRF)                       │
├──────────────────────────────────────────────────────────────┤
│  • Merge all 4 lists into one                                │
│  • Chunks that appear in MULTIPLE lists get boosted          │
│  • Chunk appearing most frequently → ranked #1               │
│                                                              │
│                                                              │
│  Example from above:                                         │
│    chunkA appeared in all 4 lists  → score: highest          │
│    chunkB appeared in 2 lists      → score: medium           │
│    chunkG appeared in 1 list       → score: lowest           │
│                                                              │
│  WHY? Chunks consistently retrieved across multiple          │
│  queries are very likely to be relevant.                     │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  STEP 4 — Arbitrary Document (Context Assembly)              │
├──────────────────────────────────────────────────────────────┤
│  • Take top-N ranked chunks from RRF                         │
│  • Join them into one big context string                     │
│  • This is your "arbitrary document" / merged context        │
│                                                              │
│  context = "\n\n".join(top_chunks)                          │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  STEP 5 — Final LLM Call (Answer Generation)                 │
├──────────────────────────────────────────────────────────────┤
│  • Send to LLM:                                              │
│      - Original user query                                   │
│      - Merged context (top chunks from RRF)                  │
│  • LLM generates the final answer                            │
│                                                              │
│  Prompt template:                                            │
│    "Answer the question using only the context below.        │
│     Question: {user_query}                                   │
│     Context: {merged_chunks}"                                │
└──────────────────────────────────────────────────────────────┘

KEY CONCEPTS SUMMARY:
━━━━━━━━━━━━━━━━━━━━
  Multi-Query   → LLM expands 1 query into 4
  Similarity    → Vector DB finds relevant chunks per query
  RRF           → Ranks chunks by how often they appear
  Arbitrary doc → Top chunks merged into one context
  Final call    → LLM answers using that merged context