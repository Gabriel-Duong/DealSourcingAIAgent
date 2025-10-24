# server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import time

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA

PERSIST_DIR = str(Path(__file__).parent / "chroma_db")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Question(BaseModel):
    question: str

# --- load once, same as app.py ---
emb = OllamaEmbeddings(model="nomic-embed-text")
db  = Chroma(persist_directory=PERSIST_DIR, embedding_function=emb)
retriever = db.as_retriever(search_kwargs={"k":4})
llm = OllamaLLM(model="gemma3:12b")
qa  = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

@app.post("/ask")
def ask(payload: Question):
    t0 = time.time()
    res = qa.invoke(payload.question)
    return {"answer": res["result"], "latency": round(time.time()-t0, 3)}
