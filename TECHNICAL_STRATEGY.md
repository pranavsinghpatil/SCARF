# Technical Strategy & RAG Optimization

This document outlines the core technical decisions and RAG (Retrieval-Augmented Generation) strategies implemented in Readify to ensure high accuracy, performance, and security.

## 1. The Pre-Filtering Strategy
One of the most critical challenges in a multi-user RAG system is **Session Pollution**. 

### The Problem
If multiple users upload similar documents (e.g., different versions of the same research paper), a standard vector search for "Limitations of Transformers" might return chunks from *all* sessions. Even if the backend filters these out in Python, the top results for the current user might be "crowded out" by better matches from other sessions.

### The Solution: Database-Level Pre-Filtering
Readify implements **MongoDB Atlas Search Pre-Filtering**. 
- **Mechanism**: The `session_id` and `source` metadata are indexed as `filter` types in Atlas Search.
- **Benefit**: MongoDB restricts the vector search to *only* the documents belonging to the current session.
- **Result**: Even with a small retrieval count (`k=5` or `k=10`), the user is guaranteed to get the most relevant information strictly from their uploaded documents.

---

## 2. Retrieval Depth (K-Selection)
Selecting the right `k` value is a balancing act between **Recall** and **Noise**.

- **Early Phase (k=100 with Post-Filtering)**: Before pre-filtering was stable, we used a very high recall (`k=100`) and manually filtered in Python. This ensured we found the session chunks but introduced latency and high token usage.
- **Current Phase (Optimized k=5 to 10)**: With pre-filtering enabled, we now use `k=5` or `k=10`. 
    - **k=5**: Provides extremely high-focus responses, perfect for quick fact-lookup.
    - **k=10**: Better for exploratory queries where synthesized perspective is needed.

---

## 3. High-Fidelity Prompting
To prevent the LLM from simply outputting raw data fragments, Readify uses a **Synthesis Prompt**:

1. **Identity**: The LLM is given the role of "Readify AI - Expert Research Assistant".
2. **Analysis Guidelines**: It is explicitly told to *synthesize* rather than *copy*.
3. **Markdown Enforcement**: The system prompts for bolding, list-making, and headers to ensure the UI remains premium and readable.

---

## 4. Handling Transient Provider Errors
Production RAG systems often face rate limits or internal server errors from AI providers. 

**Implemented Solution**:
- **Ingestion Retries**: A 3-attempt exponential backoff retry loop was added to the ingestion pipeline. If the AI provider's embedding service has a transient 500 error, the system waits and retries automatically.
- **API Status Handling**: Graceful error messages and 429 status codes are returned to the frontend if rate limits are hit, maintaining a stable user experience.

---

## 5. Security & Cleanup
- **Keepalive Unload**: Readify uses the browser's `keepalive` flag to ensure that when a user closes their tab, a "kill signal" is sent to the backend to purge vectors from MongoDB.
- **Zero Persistence Policy**: No document data is stored longer than necessary, satisfying strict data privacy requirements.

---
*These strategies combined make Readify a production-grade RAG implementation capable of handling complex document intelligence tasks with high precision.*
