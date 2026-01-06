from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.llm_provider import LLMProvider
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from backend.database import get_collection
from langchain_core.prompts import PromptTemplate

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    filenames: list[str] = []
    session_id: str = "default"

@router.post("/query")
async def chat(request: ChatRequest):
    collection = get_collection()
    if collection is None:
        raise HTTPException(status_code=500, detail="Database not configured.")

    provider = LLMProvider()
    embeddings = provider.get_embeddings()
    
    vector_store = MongoDBAtlasVectorSearch(
        collection=collection, 
        embedding=embeddings, 
        index_name="vector_index", 
        text_key="text", 
        embedding_key="embedding"
    )
    
    # 1. Retrieve a small pool of candidates to be fast (k=30)
    #    We need slightly more than k=5 initially to allow for filtering out other session data,
    #    but we keep it small to ensure low latency.
    print(f"--- Query: {request.question} ---")
    print(f"--- Session: {request.session_id} | Filtering for files: {request.filenames} ---")
    raw_docs = vector_store.similarity_search(request.question, k=30)
    
    # 2. Filter by session_id for strict isolation
    docs = [
        doc for doc in raw_docs 
        if doc.metadata.get("session_id") == request.session_id 
        and (not request.filenames or doc.metadata.get("source") in request.filenames)
    ]

    # 3. Strict limit to top 7
    docs = docs[:7]

    print(f"--- Retrieved {len(docs)} chunks after filtering. ---")
    
    if not docs:
        return {
            "answer": "I couldn't find this information in the uploaded document(s).",
            "citations": []
        }

    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Generate
    llm = provider.get_chat_model()
    
    prompt_template = """You are an intelligent document research assistant. Your goal is to answer the user's question accurately using ONLY the provided context.

    Context:
    {context}
    
    Question: {question}
    
    Instructions:
    - Look for specific details, titles, definitions, and affiliations in the text.
    - If the user asks for the "name" or "title" of the paper, look for the main heading at the beginning.
    - If the user asks about an entity (like "CeADAR") that appears in headers, footers, or affiliations, describe what the text says about it (e.g., "It appears to be an affiliation...").
    - If the answer is not explicitly stated but is clearly implied by the context, you may infer it.
    - If the answer is definitely not in the text, say: "I couldn't find this information in the uploaded document."
    
    Answer:"""
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    files_chain = prompt | llm
    
    try:
        response = files_chain.invoke({"context": context, "question": request.question})
    except Exception as e:
        error_msg = str(e)
        if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg:
             raise HTTPException(status_code=429, detail="Free tier rate limit exceeded. Please wait ~30 seconds before trying again.")
        print(f"LLM Generation Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response from AI provider.")
    
    # Deduplicate citations with Page Numbers
    # Format: "Filename (Page X, Y)"
    source_map = {}
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        # Metadata 'page' should be 1-indexed int from ingestion
        page = doc.metadata.get("page", "?")
        if source not in source_map:
            source_map[source] = set()
        source_map[source].add(str(page))
    
    citations = []
    for source, pages in source_map.items():
        # Filter out '?' and sort numerical pages
        valid_pages = [p for p in pages if p != '?' and p.isdigit()]
        sorted_pages = sorted(valid_pages, key=lambda x: int(x))
        
        if sorted_pages:
             page_str = ", ".join(sorted_pages)
             citations.append(f"{source} (Page {page_str})")
        else:
             citations.append(f"{source}")
    
    return {
        "answer": response.content,
        "citations": citations
    }
