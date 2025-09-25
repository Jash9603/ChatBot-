from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Backend.RAG.chain import get_answer, get_top_source  
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_question(data: Question):
    answer = get_answer(data.question)
    source = get_top_source(data.question)
    return {"answer": answer, "source": source}
