# Parallel Query (Fan Out) Retrival Augment generation

#Parallel Query Fanout Retrieval (PQFR) mein hum ek single user query ko directly search nahi karte. 
#Usko pehle 2–3 meaningful sub-queries mein tod dete hain, jahan har sub-query original question ke alag angle ko represent karti hai. 
#Phir in sab queries par parallel vector search chalaate hain taaki har query apne relevant documents retrieve kare.
#Kyunki har query different aspect cover karti hai, humein zyada complete aur diverse information milti hai. 
#Iske baad hum sab results ko merge karke duplicate chunks hata dete hain aur ek clean context bana kar LLM ko dete hain final answer generate karne ke liye. 
#Is approach ka main benefit ye hai ki single query se jo information miss ho sakti thi, wo multiple queries ki wajah se cover ho jaati hai, aur answer zyada accurate aur complete banta hai.                                                                                                                                                                                                                                                 user Query

# rating : 6/10

from pathlib import Path
import json
import asyncio
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

text_spliter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200
)
split_docs = text_spliter.split_documents(docs)
print(len(split_docs))

embedder = OpenAIEmbeddings(
    model="text-embedding-3-small",
)

# vector_Store = QdrantVectorStore.from_documents(
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


query = input('What your query > ')

SystemPrompt_multiquery = """
You are an intelligent multi-query generation assistant.

Your task is to take a single user query and generate exactly 3 diverse and meaningful sub-queries.

Guidelines:
    - Break the user query into different aspects, intents, or perspectives.
    - Each query should focus on a unique angle of the original query.
    - Avoid repetition or rephrasing the same query.
    - Keep each query clear, concise, and specific.

Return output in JSON format:
{
  "queries": ["query1", "query2", "query3"]
}

Example:
    User Query:
    "Explain Kubernetes autoscaling, its types, and limitations"

    Output: 
    {
        "queries": [
            "What is Kubernetes autoscaling and how does it work?",
            "What are the different types of autoscaling in Kubernetes (HPA, VPA, Cluster Autoscaler)?",
            "What are the limitations and challenges of Kubernetes autoscaling?"
        ]
    }
    
"""
client = OpenAI(timeout=60.0)

Multi_query = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=600,
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SystemPrompt_multiquery},
        {"role": "user", "content": query},
    ]
)


content = Multi_query.choices[0].message.content
data = json.loads(content) # convert in dict
queries = data["queries"] # list of queries

print("Generated Queries:")
for i, q in enumerate(queries, 1):
    print(f"  {i}. {q}")
print()

# Perform Similarity Search
# `similarity_search` is a **regular blocking function**, not a coroutine so await dont works on blocking func
# asyncio.to_thread wraps the blocking function into a new thread, making it awaitable, and now all 3 search is being performed on diff-diff thread 
async def search():
    tasks = [asyncio.to_thread(retriever.similarity_search, q, k=4) for q in queries]
    results = await asyncio.gather(*tasks) # runs all of them concurrently
    return results

search_results = asyncio.run(search())
print(f"Raw results: {[len(sz) for sz in search_results]} query results retrieved")
print()

# we are getting list of lists(per query gives 1 list containing multiple docs) : [[{1}, {2}], [{2}, {3}}], [{4}, {3}]]
# duplicates aa rahe hain (same _id repeat) so we need to filter out unique docs    

all_docs = [doc for sublist in search_results for doc in sublist] # nested comprehension (we got all docs in a list) here, docs = {metaata: , page_content: } = a chunk

# Remove duplicates (_id based)
unique_docs = {}
for doc in all_docs:
    doc_id = doc.metadata['_id']
    if(doc_id not in unique_docs):
        unique_docs[doc_id] = doc
    
final_docs = list(unique_docs.values())[:6] # take max 6 uniq docs so that LLM dont get confuse 


context = "\n\n".join(
    f"[Document: {chunk.metadata['source']} | Page: {chunk.metadata['page_label']}]\n{chunk.page_content}"
    for chunk in final_docs
)


final_prompt = f"""
You are a helpful assistant.

Answer the user's question using the context below.
- Answer whatever parts you can find in the context.
- If some parts are missing, say "I found partial information:" and answer what's available.
- If nothing relevant exists, say "This topic is not covered in the provided document."
- Mention source and page number for anything you reference.
- Do NOT use outside knowledge.

Context:
{context}
"""

result = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=1024,
    messages=[
        {"role": "system", "content": final_prompt},
        {"role": "user", "content": query},
    ]
)

print("Answer:")
print(result.choices[0].message.content)