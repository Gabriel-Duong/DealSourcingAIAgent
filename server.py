from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma

# --- Define models explicitly ---
EMBED_MODEL = "nomic-embed-text:latest"   # embeddings only
CHAT_MODEL = "gemma3:12b"                 # LLM for answers

# --- Load vector DB ---
embeddings = OllamaEmbeddings(model=EMBED_MODEL)
db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
retriever = db.as_retriever()

# --- Set up chat LLM ---
llm = OllamaLLM(model=CHAT_MODEL)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)

# --- FastAPI app ---
app = FastAPI(title="RAG Advisory Bot", version="0.1.0")

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    raw = qa.invoke(query.question)

    # normalize to a plain string for frontends
    if isinstance(raw, dict):
        # common keys: "result", "answer", "text"
        answer_text = raw.get("result") or raw.get("answer") or raw.get("text") or str(raw)
    else:
        answer_text = str(raw)

    return {
        "model": CHAT_MODEL,
        "embedding_model": EMBED_MODEL,
        "answer_text": answer_text,
        "raw": raw  # keep for debugging if needed
    }

