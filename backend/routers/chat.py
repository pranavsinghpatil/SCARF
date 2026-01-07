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
    
    pre_filter = {
        "session_id": {"$eq": request.session_id}
    }
    if request.filenames:
        pre_filter["source"] = {"$in": request.filenames}

    raw_docs = vector_store.similarity_search(
        request.question, 
        k=5,
        pre_filter=pre_filter
    )
    
    docs = raw_docs

    if not docs:
        return {
            "answer": "I couldn't find this information in the uploaded document(s).",
            "citations": []
        }

    context = "\n\n".join([doc.page_content for doc in docs])
    
    llm = provider.get_chat_model()
    
    prompt_template = """You are Readify AI, an expert research assistant. Your mission is to provide a comprehensive, well-structured, and professional answer based strictly on the provided context.

    ### Context:
    {context}
    
    ### User Question:
    {question}
    
    ### Response Guidelines:
    1. **Synthesize & Structure**: Don't just copy chunks. Synthesize the information into a cohesive, logical response.
    2. **Markdown Excellence**: Use bold text for key terms, bullet points for lists, and headers if the response is long.
    3. **Professional Tone**: Maintain a helpful, objective, and expert tone.
    4. **Precision**: Use specific details, data points, or definitions found in the context.
    5. **Groundedness**: If the answer isn't in the context, strictly adhere to the provided documents and clearly state: "Based on the provided documents, I couldn't find specific information regarding this."
    
    ### Answer:"""
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    files_chain = prompt | llm
    
    try:
        response = files_chain.invoke({"context": context, "question": request.question})
    except Exception as e:
        error_msg = str(e)
        if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg:
             raise HTTPException(status_code=429, detail="Free tier rate limit exceeded. Please wait ~30 seconds before trying again.")
        raise HTTPException(status_code=500, detail="Failed to generate response from AI provider.")
    
    source_map = {}
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "?")
        if source not in source_map:
            source_map[source] = set()
        source_map[source].add(str(page))
    
    citations = []
    for source, pages in source_map.items():
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
