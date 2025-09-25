
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv() 

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)