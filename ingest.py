import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Load documents from data/
docs = []
for file in os.listdir("data"):
    path = os.path.join("data", file)
    if file.endswith(".pdf"):
        docs.extend(PyPDFLoader(path).load())
    elif file.endswith(".txt"):
        docs.extend(TextLoader(path).load())

# Use an embeddings-capable model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Store vectors in Chroma
db = Chroma.from_documents(docs, embeddings, persist_directory="chroma_db")
db.persist()

print("Knowledge base created and stored in chroma_db/")
