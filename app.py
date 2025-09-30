from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma

# Reload vector DB with same embedding function used in ingest.py
embeddings = OllamaEmbeddings(model="nomic-embed-text")
db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
retriever = db.as_retriever()

# Use a chat model for responses
llm = OllamaLLM(model="gemma3:12b")

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)

def chat(query: str):
    return qa.invoke(query)

if __name__ == "__main__":
    print("RAG chatbot ready. Type 'exit' to quit.")
    while True:
        q = input("You: ")
        if q.lower() in ["exit", "quit"]:
            break
        print("Bot:", chat(q))
