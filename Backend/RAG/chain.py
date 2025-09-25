from Backend.RAG.llm import llm
from Backend.RAG.document import retriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
You are an expert university policy and FAQ assistant. Your task is to provide a concise and accurate answer to the user's question using ONLY the provided context.

Context:
{context}

Question:
{question}

Answer:""",
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)

def get_answer(question: str) -> str:
    """Return answer from the RAG system"""
    try:
        result = qa_chain.invoke({"query": question})
        return result.get("result") if isinstance(result, dict) else str(result)
    except Exception as e:
        return f" Error fetching answer: {e}"

def get_top_source(question: str) -> str:
    """Return the source of the top document"""
    try:
        docs = retriever.invoke(question)
        if docs:
            return docs[0].metadata.get("source", "unknown")
        return "No source found"
    except:
        return "Error fetching source"
