from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

# pdf file ka path extract kr rha hai  :  __file__ = current python file ka path | .parent = uska folder
pdf_path = Path(__file__).parent / "sliceCC.pdf"


#PyPDFLoader pdf ko directly text me convert karke LIST of Documents return karta hai , har Document object = 1 page
# isliye agar pdf 33 pages ki hai to docs list me 33 elements honge
loader = PyPDFLoader(pdf_path)
docs = loader.load()

# print(docs[0]) # print 0th chunk(i.e 0th page)
# print(len(docs)) # 33

# RecursiveCharacterTextSplitter then splits smartly — it tries to break at \n\n first, then \n, then space, then character
# LLM ek baar me bahut bada text process nahi karta efficiently isliye documents ko chote chunks me todte hain
# chunk_size = max characters in one chunk
# chunk_overlap = previous chunk ka thoda part next chunk me repeat krta hai taki context break na ho, agar overlap nahi hota to important sentence cut ho sakta tha
text_Splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

split_docs = text_Splitter.split_documents(docs)
# print(len(split_docs)) 

embedder = OpenAIEmbeddings(
    model="text-embedding-3-small",
)

# injection = embeddings ko vector DB(we are using Qdrant vector db) me store karna, isko RAG pipeline me "indexing phase" bolte hain

# vector_store = QdrantVectorStore.from_documents(
#     documents=[], # create new collection form krka usma ak empty document bnadega in qdrant db
#     url="http://localhost:6333",
#     collection_name="learning-langchain",
#     embedding=embedder, # ya code btarha hai ki : openai ka ya model ko use krka embedding krna hai 
# )

# vector_store.add_documents(split_docs) # split_docs me jo chote chunks hain unhe vector store(qdrant db) me add kar do
# print("Injection Done")


# yaha hum existing vector collection sa connect kar rahe hain
# matlab embeddings already DB me store hain ab hum bas unhe search karenge
retriver = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333", # qdrant server is url pa hosted hai
    collection_name="learning-langchain",
    embedding=embedder
)

query = "What is the Late payment charges?"

# search_result = list of objects, where each entry contains a metadata dictionary (holding file details) and a page_content string (containing the extracted text).
# Ex : [{"metadata": .... , "page_content": "....."}, {"metadata": .... , "page_content": "....."}]
# similarity_search query ko bhi embedding me convert karta hai fir vector DB me nearest vectors dhundta hai so, result = most relevant chunks from document
search_result = retriver.similarity_search(query, k=4) # k = top 4 most relevant chunks return karo

context = "\n\n".join(
    f" Source: {chunk.metadata['source']} | Page: {chunk.metadata['page_label']} \n Content: {chunk.page_content}"
    for chunk in search_result
)
print(context)
system_prompt = f"""
You are a helpful assistant for answering questions based on the provided context. Use the following context to answer the question. If you don't know the answer, say you don't know.

context: {context}
"""

client = OpenAI(timeout=60.0) # upr ka kam hona mai time lgega so , openai ko btado ki timout error 60sec tk kmsakum wait kkrna ka baad de

chat_result = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query }
    ]
)

print("Answer: ", chat_result.choices[0].message.content)


