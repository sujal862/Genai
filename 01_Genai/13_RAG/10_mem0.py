# Mem0 = retrieve + understand + structure + decide + store

from mem0 import Memory
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
QUADRANT_HOST = "localhost"

NEO4J_URL="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="reform-william-center-vibrate-press-5829"

# ============================================================
# CONFIG — Mem0 ko batao kaunse tools use karne hain
# ============================================================
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {"api_key": OPENAI_API_KEY, "model": "text-embedding-3-small"},
    },
    # LLM → decisions leta hai after each query: - kya extract karna hai (entities, relations) - purani memory update/delete karni hai ya nahi
    "llm": {"provider": "openai", "config": {"api_key": OPENAI_API_KEY, "model": "gpt-4o-mini"}},
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": QUADRANT_HOST,
            "port": 6333,
        },
    },
    # GRAPH STORE (Neo4j) → entities aur unke beech relationships store karta hai ("Sujal" -[:LIKES]-> "Python")
    "graph_store": {
        "provider": "neo4j",
        "config": {"url": NEO4J_URL, "username": NEO4J_USERNAME, "password": NEO4J_PASSWORD},
    },
}


mem_client = Memory.from_config(config)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def chat(message):
    # ============================================================
    # STEP 1 — Purani relevant memories fetch karo (Qdrant se)
    # ============================================================
    # user ka naya message vector mein convert hota hai
    # phir Qdrant mein similar vectors dhundhe jaate hain
    # user_id filter lagta hai — sirf is user ki memories
    # ============================================================
    mem_result  = mem_client.search(query=message, user_id="user_1")
    print("Memory Search Result:", mem_result)

    memories ="\n".join(
        f" Memory : {m["memory"]} | Score : {m["score"]}" 
        for m in mem_result.get("results"))
    print("Memories to LLM:", memories)

     # ============================================================
    # STEP 2 — System prompt mein purani memories inject karo
    # ============================================================
    # GPT ko context dete hain ki user ke baare mein pehle se
    # kya pata hai — taaki relevant jawab de sake
    # ============================================================
    SYSTEM_PROMPT = f"""
        You are a Memory-Aware Fact Extraction Agent, an advanced AI designed to
        systematically analyze input content, extract structured knowledge, and maintain an
        optimized memory store. Your primary function is information distillation
        and knowledge preservation with contextual awareness.

        Tone: Professional analytical, precision-focused, with clear uncertainty signaling
        
        Memory and Score:
        {memories}
    """

    messages = [
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": message }
    ]

    # STEP 3 — GPT se response lo
    result = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    response = result.choices[0].message.content
    messages.append(
        {"role": "assistant", "content": response}
    )

    # ============================================================
    # STEP 4 — Naya conversation memory mein save karo
    # ============================================================
    # mem_client.add() ke andar ye sab automatically hota hai:
    #
    #   a) Qdrant mein search — koi related memory pehle se hai?
    #
    #   b) LLM ko bheja jaata hai:
    #      "Existing memory: Sujal DISLIKES onion"
    #      "New message: I like onion"
    #      → LLM decide karta hai: DELETE old + CREATE new
    #
    #   c) Neo4j mein:
    #      LLM entities + relations extract karta hai
    #      Mem0 Cypher generate karta hai:
    #      MATCH (s)-[:DISLIKES]->(o {name:"onion"}) DELETE r
    #      CREATE (s)-[:LIKES]->(o)
    #
    #   d) Qdrant mein:
    #      Naya memory vector store hota hai with payload:
    #      { memory: "Sujal likes onion", user_id: "user_1" }
    #
    # ============================================================
    mem_client.add(messages, user_id="user_1")


    return response


# Har iteration mein:
#   1. User input lo
#   2. Purani memories fetch karo (Qdrant)
#   3. GPT se response lo (memory-aware)
#   4. Naya conversation save karo (Qdrant + Neo4j)
while True:
    query = input(">> ")
    print("BOT:" , chat(query))





## Visual Flow

# User Input
#     │
#     ▼
# mem_client.search()          ← Qdrant se purani memories fetch
#     │
#     ▼
# System Prompt + Memories     ← GPT ko context do
#     │
#     ▼
# GPT Response                 ← memory-aware jawab
#     │
#     ▼
# mem_client.add()
#     ├── Qdrant update        ← vector store mein save
#     └── Neo4j update         ← relations add/update/delete


# graph.refresh_schema()
# Neo4j ka current structure (nodes, relations, properties) fetch karke memory mein update karta hai
# LLM ko latest schema pata rehta hai → sahi Cypher generate hoti hai
# Jab bhi naye nodes/relations add hon, tab call karo