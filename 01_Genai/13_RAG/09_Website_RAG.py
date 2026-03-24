import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, QueryRequest
from openai import OpenAI
import uuid

load_dotenv()

BASE_URL = "https://docs.chaicode.com"
SEED_URL = "https://docs.chaicode.com/youtube/getting-started/"
EMBEDDING_MODEL = "text-embedding-3-small"
COLLECTIONS = ["html", "git", "cpp", "django", "sql", "devops"]

# Parent route -> to collection name
SLUG_TO_COLLECTION = {
    "chai-aur-html":   "html",
    "chai-aur-git":    "git",
    "chai-aur-c":      "cpp",       
    "chai-aur-django": "django",
    "chai-aur-sql":    "sql",
    "chai-aur-devops": "devops",
}

client = OpenAI(timeout=60.0)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500, 
    chunk_overlap=200
)
qdrant = QdrantClient(url="http://localhost:6333") #  Connect to the "Database"

#Shared - Embeddings

def get_embeddings(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]

def get_embedding(text: str) -> list[float]:
    return get_embeddings([text])[0]


# STEP 1 — SCRAPE SIDEBAR → GET ALL URLS

def get_topic_url_map() -> dict[str, list[str]]:
    resp = requests.get(SEED_URL)
    soup = BeautifulSoup(resp.content, "html.parser")

    top_ul = soup.find("ul", class_=lambda c: c and "top-level" in c)

    topic_map = {}

    for li in top_ul.find_all("li", recursive=False): # recursive=false : only look at the immediate children of the tag

        # skip li that has no <details> (e.g. Getting Started)
        details = li.find("details")
        if not details:
            continue

        # get all <a> tags inside this details block
        anchors = details.find_all("a", href=True)
        if not anchors:
            continue
        urls = []
        collection_name = None

        for a in anchors:
            href = a["href"]
            if not href.startswith("/youtube/"):
                continue

            # /youtube/chai-aur-html/welcome/
            parts = urlparse(href).path.strip("/").split("/")
            # parts = ["youtube", "chai-aur-html", "welcome"]

            if collection_name is None:
                slug = parts[1] 
                collection_name = SLUG_TO_COLLECTION.get(slug)

            urls.append(BASE_URL + href)

        if collection_name and urls:
            topic_map[collection_name] = urls
            print(f"✓ {collection_name}: {len(urls)} urls")

    return topic_map



# step-2 - Create Qdrant collections

def create_collections(collection_names: list[str]): 
    existing = [c.name for c in qdrant.get_collections().collections]
    
    for name in collection_names:
        #Agar collection already bana hua hai → skip
        if name in existing:
            print(f"[skip] collection '{name} already exists")
        else:
            qdrant.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE) # Similarity measure hai , Cosine similarity → best for semantic search
            )
            print(f"[CREATED] collection '{name}'")


def ingest_collection(collection_name: str, urls: list[str]):
    print(f"\n{'='*50}")
    print(f"Processing collection: {collection_name} ({len(urls)} pages)")
    print(f"{'='*50}")

    for url in urls:
        print(f"\n  → Scraping: {url}")
        try:
            loader = WebBaseLoader([url])
            docs = loader.load()

            if not docs or not docs[0].page_content.strip():
                print(f"  [SKIP] empty content at {url}")
                continue
            
            chunks = splitter.split_documents(docs)

             # embed all chunks at once using openai embed model
            texts = [chunk.page_content for chunk in chunks]
            vectors = get_embeddings(texts)


            # Qdrant stores things as 'Points'. Each point needs an ID, the Vector, and the actual Text (Payload).
            points = [
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vectors[i],
                    payload={
                        "text": chunks[i].page_content,
                        "source": url,
                        "collection": collection_name
                    }
                )
                for i in range(len(chunks))
            ]

            # insert points into qdrant
            qdrant.upsert(
                collection_name=collection_name,
                points=points
            )
            print(f"  ✓ Upserted {len(points)} points into '{collection_name}'")
        except Exception as e:
            print(f" [Error] {url} -> {e}")
            continue




# ─────────────────────────────────────────────
# QUERY — STEP 1 : LLM ROUTER
# ─────────────────────────────────────────────

ROUTER_PROMPT = f"""
You are a router for a documentation assistant.
Read the user query and return ONLY one word from: {COLLECTIONS}
No explanation. Just the single word.

Examples:
  "how do I create a model in Django?" → django
  "what is a git branch?" → git
  "how to write a for loop in C++?" → cpp
  "what is a Docker container?" → devops
  "how to write a SELECT query?" → sql
  "what is an HTML form?" → html
"""

# generate collection name based on user query
def route_query(query: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=10,
        messages=[
            {"role": "system", "content": ROUTER_PROMPT},
            {"role": "user", "content": query}
        ]
    )

    label = response.choices[0].message.content.strip().lower()
    if label not in COLLECTIONS:
        print(f"  [ROUTER WARNING] '{label}' not valid, defaulting to 'html'")
        return "html"
    return label


# QUERY — STEP 2 : SEARCH + ANSWER

ANSWER_PROMPT = """
You are a helpful documentation assistant for ChaiCode.
Answer using ONLY the context provided.
- If found → answer clearly.
- If partial → say "I found partial information:" and answer what's available.
- If nothing → say "This topic is not covered in the provided documentation."
- Mention source URL for anything you reference.
- Do NOT use outside knowledge.
"""

def query_pipeline(query: str):
    #route 
    collection = route_query(query)
    print(f"[ROUTER] → '{collection}'")

    #embed
    query_vector = get_embedding(query)

    results = qdrant.query_points(
        collection_name=collection,
        query=query_vector,
        limit=5
    ).points
    print(f"[SEARCH] {len(results)} chunks retrieved from '{collection}'")
    print()

    if not results:
        print("No results found.")
        return

    print()
    # build context
    context = "\n\n".join(
        f"[Source: {r.payload['source']}]\n{r.payload['text']}"
        for r in results
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": ANSWER_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )

    print("Answer:")
    print(response.choices[0].message.content)



# ENTRY POINT ( kb ingestion wala code chlana hai and kav query wala : can avoid this seperation by using 2 diff file for each)

if __name__ == "__main__": # File directly run kr rha koi → execute kro else agr Import ho rha file khi → skip kro us sma 
    # sys.argv = command line arguments : if you run :  python main.py ingest, then sys.argv = ["main.py", "ingest"]
    if len(sys.argv) < 2: 
        print("Usage:")
        print("  python main.py ingest   ← populate Qdrant (run once)")
        print("  python main.py query    ← ask a question")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "ingest":
        topic_map = get_topic_url_map()
        create_collections(list(topic_map.keys()))
        for collection_name, urls in topic_map.items():
            ingest_collection(collection_name, urls)

        print("\n" + "="*50)
        print("✅ Ingestion Complete — Stats:")
        for name in topic_map.keys():
            info = qdrant.get_collection(name)
            print(f"  {name}: {info.points_count} points") # points  = chunks

    elif mode == "query":
        query = input("What is your query > ")
        print()
        query_pipeline(query)

    else:
        print(f"Unknown mode: '{mode}'")
        print("Use: python main.py ingest  OR  python main.py query")



# Notes:
# at line 217 results = Every result Qdrant returns is a ScoredPoint — one stored chunk with its similarity score.
# ScoredPoint(
#     id      → unique id of that chunk in Qdrant
#     score   → how similar it is to your query (0 to 1, higher = better)
#     payload → the actual data you stored (text, source, collection)
#     vector  → None here because we didn't ask Qdrant to return vectors back
# )