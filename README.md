# ChatBot - Automated Policy and FAQ Assistant

Universities have a vast amount of information scattered across different departments, from registration policies to leave-of-absence procedures. Students and staff often struggle to find specific answers, leading to a high volume of repetitive questions for administrative offices.  

This project is an LLM-based **RAG (Retrieval-Augmented Generation) ChatBot** that ingests various university documents (PDFs, CSVs) and provides concise answers to natural language queries. It significantly reduces administrative burden and gives students instant access to information.

---

## Features

- Ask questions about university policies, FAQs, and rules.
- Retrieves answers from PDFs and CSV databases.
- Returns the top source document for reference.
- Frontend interface with HTML, CSS, and JS for easy interaction.
- Built with FastAPI for backend APIs.

---

---

## Installation

1. Clone the repo:
```bash
git clone https://github.com/YourUsername/ChatBot.git
cd ChatBot
```
2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```
3. Install dependencies:
```bash
pip install -r requirement.txt
```
4.Add your API keys in .env:
```bash
GROQ_API_KEY=your_groq_api_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

## Usage
Run FastAPI backend:
```bash
uvicorn app:app --reload
```

## Access frontend:
Open frontend/index.html in your browser to interact with the ChatBot.

## Libraries Used
 - FastAPI - Backend API framework
 - Pydantic - Data validation
 - LangChain - RAG framework
 - LangChain-Groq - LLM integration
 - LangChain-Chroma - Vector database integration
 - LangChain-HuggingFace - Embeddings and models
 - LangChain-Community - Document loaders
 - Pandas - CSV processing
 - Python-Dotenv - Environment variable management
