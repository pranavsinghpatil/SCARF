# Readify - Document Q&A Assistant

Readify is an intelligent RAG (Retrieval-Augmented Generation) pipeline that allows users to upload documents (PDF, DOCX, TXT, MD) and ask context-aware questions. It leverages a modern Next.js frontend and a robust FastAPI backend with MongoDB Atlas Vector Search.

## 🚀 Features

- **Multi-Format Ingestion**: Supports PDF, DOCX, TXT, and Markdown files.
- **Advanced RAG Pipeline**: Uses similarity search with metadata filtering for precise answers.
- **Session Management**: Isolated user sessions to prevent data leakage.
- **Modern UI**: Polished, dark-themed Chat Interface with real-time feedback.
- **Provider Agnostic**: Configurable to use **OpenAI** or **Gemini** (currently set to Generic/Gemini for assignment).

> [!NOTE]
> For a detailed technical breakdown, see our [Full Architecture Guide](ARCHITECTURE.md).

## 🏗️ Architecture Overview

```mermaid
graph TD
    User[User] -->|Uploads File| FE[Frontend (Next.js)]
    User -->|Asks Question| FE
    
    FE -->|API Request| BE[Backend API (FastAPI)]
    
    subgraph Ingestion Pipeline
        BE -->|Extract Text| Loader[Document Loader]
        Loader -->|Split| Chunker[Text Splitter]
        Chunker -->|Generate| Embed[Embedding Model]
        Embed -->|Store Vectors| DB[(MongoDB Atlas)]
    end
    
    subgraph RAG Query Pipeline
        BE -->|Query| DB
        DB -->|Top-k Chunks| BE
        BE -->|Context + Prompt| LLM[LLM Service]
        LLM -->|Answer| BE
    end
```

## 🛠️ Technology Stack

- **Frontend**: Next.js 14, Tailwind CSS, Lucide Icons, Framer Motion
- **Backend**: FastAPI, LangChain, PyMongo
- **Database**: MongoDB Atlas (Vector Search)
- **AI**: LangChain (OpenAI/Gemini integrations)

## 📦 Installation & Setup

### Prerequisites
- Node.js 18+
- Python 3.10+
- MongoDB Atlas Cluster (Vector Search enabled)

### 1. Clone & Configure
```bash
git clone https://github.com/pranavsinghpatil/Readify.git
cd Readify
```

### 2. Backend Setup
```bash
# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Configure Environment
# Copy .env.example to backend/.env and fill in your keys
copy backend\.env.example backend\.env
```

### 3. Frontend Setup
```bash
cd frontend
npm install
cd ..
```

### 4. Run Application
Simply double-click `launch.bat` or run:
```bash
.\launch.bat
```
The app will open at `http://localhost:3000`.

## 📄 License
MIT License. Created by Pranav Patil.
