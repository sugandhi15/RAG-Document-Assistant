# 📄 DocuMind-AI

An AI-powered Document Question Answering System built using **Retrieval-Augmented Generation (RAG)**. Upload one or more PDF documents and ask questions in natural language. The application retrieves the most relevant document chunks using semantic search and generates accurate answers using Google's Gemini model.

---

## 🚀 Features

- 📂 Upload multiple PDF documents
- 🔍 Semantic search using Sentence Transformers
- 🗂️ FAISS vector database for fast retrieval
- 🤖 Gemini-powered answer generation
- 💬 ChatGPT-style Streamlit interface
- 📑 Displays retrieved document context
- ⚡ Dynamic vector index creation
- 🧠 Retrieval-Augmented Generation (RAG)

---

## 🏗️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- Sentence Transformers
- FAISS
- PyPDF2
- NumPy

---

## 📁 Project Structure

```
DocuMind-AI/
│
├── app.py                 # Streamlit Application
├── rag.py                 # Retrieval Pipeline
├── ingest.py              # PDF Processing
├── config.py              # Gemini Configuration
├── requirements.txt
├── README.md
├── data/
└── vector_store/
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/sugandhi15/RAG-Document-Assistant.git
```

Move into the project

```bash
cd RAG-Document-Assistant
```

Create virtual environment

```bash
python -m venv myenv
```

Activate environment

Windows

```bash
myenv\Scripts\activate
```

Linux / Mac

```bash
source myenv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure API Key

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run

```bash
streamlit run app.py
```

---

## 🧠 How It Works

```
PDF Upload
      │
      ▼
Extract Text
      │
      ▼
Chunking
      │
      ▼
Sentence Embeddings
      │
      ▼
FAISS Vector Search
      │
      ▼
Top-K Retrieval
      │
      ▼
Gemini
      │
      ▼
Final Answer
```

---

## 📸 Screenshots

### Upload Documents

(Add Screenshot Here)

---

### Chat Interface

(Add Screenshot Here)

---

### Retrieved Context

(Add Screenshot Here)

---

## 💡 Future Improvements

- Conversation memory
- Hybrid Search (BM25 + Dense Retrieval)
- OCR support for scanned PDFs
- Citation highlighting
- Support for Word and PowerPoint documents
- Vector database using ChromaDB or Pinecone
- User authentication
- Cloud deployment

---

## 🎯 Learning Outcomes

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- Prompt Engineering
- Large Language Models
- Streamlit Development
- Information Retrieval
- AI Application Development

---

## 👩‍💻 Author

**Sugandhi Bansal**

GitHub: https://github.com/sugandhi15/RAG-Document-Assistant

---

## ⭐ If you like this project

Please consider giving it a ⭐ on GitHub.
