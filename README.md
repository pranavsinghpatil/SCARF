# Readify - Intelligent Document Question Answering

Readify is a modern, RAG-based (Retrieval Augmented Generation) application that allows users to chat with their documents (PDF, DOCX, TXT, MD). Powered by **Gemini 2.5 Flash** and **MongoDB Atlas Vector Search**, it delivers precise, context-aware answers with accurate citations.

![Readify UI](https://via.placeholder.com/800x450.png?text=Readify+Dashboard+Preview)

## 🚀 Features

*   **📄 Multi-Format Ingestion**: Drag & drop support for PDF, Word, Markdown, and Text files.
*   **🧠 Advanced RAG Pipeline**:
    *   **Hybrid Retrieval**: uses Vector Search (MongoDB) + Metadata filtering `k=30` -> `top 7`.
    *   **Smart Parsing**: Recursive chunking with overlap to preserve context.
    *   **Session Isolation**: Data is separated by user session IDs.
*   **💬 Premium Chat Interface**:
    *   Streaming-like experience.
    *   Rich Markdown rendering (Code blocks, Tables, Lists).
    *   Precise **Citations** with Page Numbers.
    *   Dark Mode aesthetics.
*   **⚡ Performance**:
    *   Parallel file processing.
    *   Optimized verification depth.
    *   Graceful error handling (e.g., API Rate Limits).

## 🛠️ Tech Stack

*   **Frontend**: Next.js 14, TailwindCSS, TypeScript, Framer Motion, Lucide React.
*   **Backend**: FastAPI (Python), LangChain, Uvicorn.
*   **AI/LLM**: Google Gemini 2.5 Flash (`generative-ai` SDK).
*   **Database**: MongoDB Atlas (Vector Search).

## 📦 Setup & Installation

### 1. Prerequisites
*   Node.js (v18+)
*   Python (3.10+)
*   MongoDB Atlas Account (Free Tier is sufficient)
*   Google Gemini API Key

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```
*Edit `.env` and add your keys:*
```ini
GOOGLE_API_KEY=AIzaSy...
MONGODB_URI=mongodb+srv://...
DB_NAME=readify_db
COLLECTION_NAME=documents
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Running the App
We have provided a convenient launcher script for Windows:
```bash
.\launch.bat
```
*   **Frontend**: `http://localhost:3000`
*   **Backend Docs**: `http://localhost:8000/docs`

## 🧪 Testing
The system includes validation logic for file types and API health.
To test manually:
1.  Upload a PDF.
2.  Ask: *"What is the summary of this document?"*
3.  Verify the answer and check the generic citations (e.g., `doc.pdf (Page 1)`).

---
*Built for Advanced Full Stack Assignment.*
