# This system is a hybrid Retrieval-Augmented Generation (RAG) pipeline that processes PDF documents to enable intelligent question answering. It combines semantic search using a vector database (Qdrant) with structured reasoning using a knowledge graph (Neo4j).

# During ingestion, the PDF is split into chunks, embedded for semantic retrieval, and analyzed by an LLM to extract entities and relationships, which are stored in Neo4j.

# During querying, the system retrieves relevant document chunks and graph relationships, combines both contexts, and uses an LLM to generate accurate, context-aware answers.

import os
from pathlib import Path
import json
from dotenv import load_dotenv
from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from neo4j import GraphDatabase

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URL"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")),
)

embedder = OpenAIEmbeddings(model="text-embedding-3-small")

COLLECTION_NAME = "pdf_knowledgeGraph"
QDRANT_URL = "http://localhost:6333"


# ── Qdrant ───────────────────────────────────────────────
def store_to_qdrant(docs: list):
    QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embedder,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
    )
    print(f"[✓] {len(docs)} chunks stored in Qdrant")


def search_qdrant(query: str) -> str:
    retriever = QdrantVectorStore.from_existing_collection(
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
        embedding=embedder
    )
    results = retriever.similarity_search(query, k=4)
    context = "\n\n".join(
        f"Source: {chunk.metadata.get('source', 'N/A')} | Page: {chunk.metadata.get('page_label', 'N/A')}\nContent: {chunk.page_content}"
        for chunk in results
    )
    return context



# ── Neo4j ───────────────────────────────────────────────
# Step : Neo4j me graph(entities & relationships) store karna
# code is from docs of neo4j python driver
def store_to_neo4j(graph_data: dict):
     # Neo4j session start (connection context)
    with driver.session() as session:

        # create nodes for entities
        for entity in graph_data.get("entities", []):
            name = entity["name"]
            # Neo4j label me space allowed nahi hota → replace with _
            label = entity["type"].strip().replace(" ", "_") 
            session.run(
                f"MERGE (n: `{label}` {{name: $name}})",
                name=name
            )

        # create relationships between entities
        for rel in graph_data.get("relationships", []):
            from_node = rel["source"].strip()
            to_node = rel["target"].strip()
            rel_type = rel["type"].strip().replace(" ", "_") 

            session.run(
                f"""
                MATCH (a {{name: $from_node}}), (b {{name: $to_node}})
                MERGE (a)-[r: `{rel_type}`]->(b)
                """,
                from_node=from_node,
                to_node=to_node
            )



def search_neo4j(query: str) -> str:
    # Query ke words se matching nodes dhundo
    keywords = query.lower().split()

    with driver.session() as session:
        result = session.run("""
            MATCH (a)-[r]->(b)
            WHERE any(keyword IN $keywords 
                  WHERE toLower(a.name) CONTAINS keyword 
                  OR toLower(b.name) CONTAINS keyword)
            RETURN a.name AS from, type(r) AS rel, b.name AS to
            LIMIT 20
        """, keywords=keywords)

        rows = result.data()

    if not rows:
        return "No related graph data found."

    graph_context = "\n".join(
        f"{row['from']} -[{row['rel']}]-> {row['to']}"
        for row in rows
    )

    print(f"[✓] Found {len(rows)} relevant graph relationships in Neo4j :", graph_context)
    return graph_context




#Step : LLM se entities aur relationships extract kar rha hu ak chunk sa
def extract_graph_from_chunk(chunk: str) -> dict:
    prompt = f"""
You are a knowledge graph extractor.
From the text below, extract.
1. Entities — each with a name and type (e.g. Person, Organization, Technology, Concept, Place)
2. Relationships — directed edges between entities with a relationship type (e.g. WORKS_AT, USES, LIKES, PART_OF)

Return ONLY valid JSON in this exact format, nothing else:
{{
    "entities": [
        {{"name": "entity_name", "type": "entity_type"}},
        ...
    ],
    "relationships": [
        {{"source": "entity_name", "target": "entity_name", "type": "relationship_type"}},
        ...
    ]
}}

Text:
{chunk}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0, # deterministic output ke liye temperature 0 rakhte hain : no creativity needed here
    )

    raw = response.choices[0].message.content.strip() # remove any spaces

    # format the json (bec llm can sometime return like this : ```json {....} ``` ) and in this case json.loads() will fail, so we need to clean it
    if raw.startswith("```"):
        raw = raw.split("```")[1] # ```json {....} ``` ko clean krke sirf {....} bacha do
        if raw.startswith("json"):
            raw = raw[4:].strip()
    
    try:
        return json.loads(raw) # json string ko python dict me convert kar do
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        print("Raw LLM Output:", raw)
        return {"entities": [], "relationships": []}




# Main execution flow
def pdf_to_knowledge_graph(pdf_path: str):
    print(f"\n🚀 Starting pipeline for: {pdf_path}\n")

    # Step 1: Extract & chunk
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(pages)
    chunks = [doc.page_content for doc in docs]
    print(f"[✓] {len(chunks)} chunks extracted")

    # Step 2: Store to Qdrant
    store_to_qdrant(docs)


    # Step 3: Har chunk se graph data(entities & relationships) extract karo
    for i, chunk in enumerate(chunks):
        print(f"\nProcessing chunk {i+1}/{len(chunks)}...")
        graph_data = extract_graph_from_chunk(chunk)
        print(f"Extracted {len(graph_data['entities'])} entities and {len(graph_data['relationships'])} relationships.")

        # Step 4: Extracted graph data Neo4j me store karo
        store_to_neo4j(graph_data)
        print("Stored to Neo4j successfully.")

    print("\n✅ Pipeline execution completed.")
    print(f"\n🔍 Open Neo4j Browser: http://localhost:7474")
    print(f"   Run: MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50")




# ── Chat Function ───────────────────────────────────────────────
def chat(query: str, history: list) -> str:
    print("\n[→] Searching Qdrant...")
    qdrant_context = search_qdrant(query)

    print("[→] Searching Neo4j...")
    neo4j_context = search_neo4j(query)

    system_prompt = f"""
You are a helpful assistant. Answer the user's question using the context below.
If you don't know the answer, say you don't know.

## Relevant Document Chunks (Semantic Search):
{qdrant_context}

## Related Entities & Relationships (Knowledge Graph):
{neo4j_context}
"""

    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": query}]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=600,
        messages=messages,
        timeout=60.0
    )

    return response.choices[0].message.content



# ── Entry Point ─────────────────────────────────────────────
if __name__ == "__main__":

    #── Run 1: PDF ingest karo (sirf pehli baar) ──
    # pdf_path = Path(__file__).parent / "the_last_lesson.pdf"
    # pdf_to_knowledge_graph(pdf_path)


    # ---- Run 2: Chat with RAG (Qdrant + Neo4j) ──
    print("🚀 Hybrid RAG Chat (Qdrant + Neo4j)")
    print("Type 'exit' to quit\n")

    history = []  # multi-turn memory

    while True:
        query = input("You: ").strip()
        if query.lower() == "exit":
            driver.close()
            break

        answer = chat(query, history)
        print(f"\nAssistant: {answer}\n")

        # history update karo — multi-turn ke liye
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": answer})




# Full flow recap:
#
# INGEST PIPELINE
# PDF
#  └─ PyPDFLoader              → pages (Document objects)
#  └─ RecursiveTextSplitter    → smart chunks (1000 chars, 200 overlap)
#       ├─ Qdrant              → embeddings stored (semantic search ke liye)
#       └─ GPT-4o-mini         → JSON {entities, relationships} per chunk
#               └─ Neo4j MERGE → nodes + edges stored (no duplicates)
#
# CHAT PIPELINE
# User Query
#  ├─ Qdrant similarity_search → top 4 relevant chunks
#  ├─ Neo4j keyword match      → related entities & relationships
#  └─ GPT-4o-mini              → final answer (both contexts combined)