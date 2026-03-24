# Query Decomposition - Step Back Prompting (More Abstract)

# rating : 9/10

from pathlib import Path
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

pdf_path = Path(__file__).parent / "Kubernetes.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200
)
split_docs = text_splitter.split_documents(docs)

embedder = OpenAIEmbeddings(model="text-embedding-3-small")

# vector_store = QdrantVectorStore.from_documents(
#     documents=split_docs,
#     url="http://localhost:6333",
#     collection_name="kubernetes-official-docs",
#     embedding=embedder,
# )
# print("Injection Done")

retriever = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="kubernetes-official-docs",
    embedding=embedder,
)

client = OpenAI(timeout=60.0)
query = input("What is your query? > ")
print()

# ── STEP 1 — generate step back (abstract) question ───────────────────────────
step_back_prompt = """
You are an expert at abstraction.

Your task is to take a specific user question and generate a more abstract 
"step back" version of it that zooms out to the broader concept or principle.

Rules:
- Make it broader and more general than the original
- It should retrieve wider context that helps answer the specific question
- Return ONLY this JSON:
{
  "original": "original question here",
  "stepback": "broader abstract version here"
}

Example:
    Original:  "when was the last time a team from canada won the stanley cup as of 2002?"
    Step Back: "which years did a team from canada win the stanley cup?"

Example:
    Original:  "How does the kubelet restart a failed container?"
    Step Back: "How does Kubernetes manage container lifecycle on a node?"
"""

stepback_response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=300,
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": step_back_prompt},
        {"role": "user", "content": query},
    ]
)

stepback_data = json.loads(stepback_response.choices[0].message.content)
stepback_question = stepback_data["stepback"]

print(f"Original  :  {query}")
print(f"Step Back :  {stepback_question}")
print()

# ── STEP 2 — retrieve docs for BOTH questions ─────────────────────────────────
original_docs = retriever.similarity_search(query, k=3)
stepback_docs = retriever.similarity_search(stepback_question, k=3)

print(f"Docs from original query  : {len(original_docs)}")
print(f"Docs from stepback query  : {len(stepback_docs)}")
print()

# ── STEP 3 — deduplicate and merge both contexts ──────────────────────────────
seen = set()
final_docs = []

for doc in original_docs + stepback_docs:
    doc_id = doc.metadata["_id"]
    if doc_id not in seen:
        seen.add(doc_id)
        final_docs.append(doc)

print(f"Unique docs after merge: {len(final_docs)}")
print()

# build context — stepback docs labeled separately so LLM knows what's broader
original_context = "\n\n".join(
    f"[Page: {doc.metadata['page_label']}]\n{doc.page_content}"
    for doc in original_docs
)

stepback_context = "\n\n".join(
    f"[Page: {doc.metadata['page_label']}]\n{doc.page_content}"
    for doc in stepback_docs
)

# ── STEP 4 — final answer using both contexts ─────────────────────────────────
final_prompt = f"""
You are a helpful assistant.

You have been given two types of context:
1. Broader context (from step back question) — gives the big picture
2. Specific context (from original question) — gives direct details

Use BOTH contexts together to give a complete and accurate answer.
Do NOT use outside knowledge.
Mention page numbers where relevant.

--- Broader Context (Step Back) ---
{stepback_context}

--- Specific Context (Original) ---
{original_context}

Original Question: {query}
"""

final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=1024,
    messages=[
        {"role": "system", "content": final_prompt},
        {"role": "user", "content": query},
    ]
)

print("=" * 60)
print("Final Answer:")
print(final_response.choices[0].message.content)


## Flow

# original query (specific)
#         ↓
# LLM generates step back (broader version)
#         ↓
# retrieve docs for BOTH questions separately
#         ↓
# original_docs  →  specific details
# stepback_docs  →  broader context
#         ↓
# merge both into final prompt (labeled separately)
#         ↓
# LLM answers using big picture + specific details together