import os
import pandas as pd
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv() 
# Hugging Face API key
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Directories
DATA_DIR = "./data"
VECTOR_DB_DIR = "./chroma_db"

# Load CSVs from data folder
df = pd.read_csv(os.path.join(DATA_DIR, "faqs.csv"))
df_rules = pd.read_csv(os.path.join(DATA_DIR, "rules.csv"))

qa_documents = []
rules_documents = []

for _, row in df.iterrows():
    content = f"Q: {row['question']}\nA: {row['answer']}"
    metadata = {"source": row.get("metadata", "faqs.csv")}
    qa_documents.append(Document(page_content=content, metadata=metadata))

for _, row in df_rules.iterrows():
    content = f"Rules: {row['rule']}"
    metadata = {"source": "rules.csv"}
    rules_documents.append(Document(page_content=content, metadata=metadata))

# Load PDF from data folder
loader = UnstructuredPDFLoader(os.path.join(DATA_DIR, "handbook.pdf"), strategy="fast")
pdf_docs = loader.load()

# Split PDF into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
pdf_chunks = text_splitter.split_documents(pdf_docs)

# Combine all docs
documents = qa_documents + rules_documents + pdf_chunks

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/msmarco-MiniLM-L-12-v3")

def get_vectorstore():
    if os.path.exists(VECTOR_DB_DIR) and os.listdir(VECTOR_DB_DIR):
        vectorstore = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=embeddings
        )
        print("✅ Loaded existing Chroma DB!")
    else:
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=VECTOR_DB_DIR
        )
        print("✅ Created new Chroma DB!")
    return vectorstore.as_retriever(search_kwargs={"k": 5})

retriever = get_vectorstore()
