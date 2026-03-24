# Query Decomposition - Chain of Thought (Less Abstract)

# In Chain of Thought RAG, the original query is first sent to an LLM which breaks it down into 3 smaller sequential sub-questions — where each question logically builds on the previous one.
# Then the process runs step by step. Sub-query 1 searches the vector DB, gets relevant docs, and the LLM answers it — this becomes **answer1**. 
# Now sub-query 2 goes to the vector DB, gets its own docs, but this time the LLM also gets **answer1 as extra context** — so it already knows what was found in step 1 before answering step 2. Same thing happens for sub-query 3 — it gets its own docs from vector DB, but the LLM now has **both answer1 and answer2 as context**, making it the most informed step.
# Finally, all 3 answers are combined with the original query and sent to the LLM one last time — which synthesizes everything into a single complete, accurate final answer. The key idea is **each step makes the next step smarter**, unlike Fan Out where all queries run independently and don't know about each other.

# rating final answer : 8.5/10

from pathlib import Path
import json
import asyncio
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from collections import defaultdict

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

# ── STEP 1 — decompose into sequential sub-questions ──────────────────────────
decompose_prompt = """
You are an expert query decomposition assistant.

Break the user query into exactly 3 sequential sub-questions.
Each sub-question should build on the previous one — like steps in a chain.
Sub-question 2 assumes sub-question 1 is already answered.
Sub-question 3 assumes sub-question 1 and 2 are already answered.

Return ONLY this JSON:
{
  "queries": ["sub-question1", "sub-question2", "sub-question3"]
}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=600,
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": decompose_prompt},
        {"role": "user", "content": query},
    ]
)

queries = json.loads(response.choices[0].message.content)["queries"]

print("Decomposed Sub-questions:")
for i, q in enumerate(queries, 1):
    print(f"  {i}. {q}")
print()

# ── STEP 2 — sequential CoT loop ──────────────────────────────────────────────
previous_answers = []  # accumulates answers from each step

for i, sub_query in enumerate(queries):
    print(f"Processing step {i+1}: {sub_query}")

    # retrieve relevant docs for this sub-query
    docs_retrieved = retriever.similarity_search(sub_query, k=4)

    context = "\n\n".join(
        f"[Page: {doc.metadata['page_label']}]\n{doc.page_content}"
        for doc in docs_retrieved
    )

    # build context from previous answers
    previous_context = ""
    if previous_answers:
        previous_context = "\n\n".join(
            f"Step {j+1} Q: {queries[j]}\nStep {j+1} A: {ans}"
            for j, ans in enumerate(previous_answers)
        )

    step_prompt = f"""
You are a helpful assistant. Answer the sub-question using ONLY the context below.
Be concise — this answer will be used as context for the next step.
{"Previous steps for context:\n" + previous_context if previous_context else ""}

Context:
{context}
"""

    step_response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=512,
        messages=[
            {"role": "system", "content": step_prompt},
            {"role": "user", "content": sub_query},
        ]
    )

    answer = step_response.choices[0].message.content
    previous_answers.append(answer)

    print(f"  Step {i+1} Answer: {answer[:100]}...")  # preview
    print()

# ── STEP 3 — final answer using all steps ─────────────────────────────────────
all_steps_context = "\n\n".join(
    f"Step {i+1} Q: {queries[i]}\nStep {i+1} A: {previous_answers[i]}"
    for i in range(len(queries))
)

final_prompt = f"""
You are a helpful assistant.
You have already answered 3 sequential sub-questions to build up knowledge.
Now use all of those answers to give a final, complete, well-structured answer.
Do NOT use outside knowledge — only what is in the step answers below.

Sub-questions and their answers:
{all_steps_context}

Original question: {query}
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


## Flow Visualized

# Original Query
#       ↓
# LLM breaks it into 3 sub-questions (sequential, dependent)
#       ↓
# sub-query 1 → vector DB → docs → LLM → answer1
#                                            ↓
# sub-query 2 → vector DB → docs → LLM (answer1 as context) → answer2
#                                                                   ↓
# sub-query 3 → vector DB → docs → LLM (answer1+answer2 as context) → answer3
#                                                                           ↓
# original query + answer1 + answer2 + answer3 → final LLM call → final answer