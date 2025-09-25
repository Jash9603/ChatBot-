from fastapi import APIRouter
from pydantic import BaseModel
from Backend.RAG.chain import get_answer, get_top_source

router = APIRouter()

class Question(BaseModel):
    question: str

@router.post("/ask")
def ask_question(data: Question):
    answer = get_answer(data.question)
    source = get_top_source(data.question)
    return {"answer": answer, "source": source}
