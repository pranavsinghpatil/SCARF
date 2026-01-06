from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from backend.services.ingestion import process_file
from backend.database import get_collection
from backend.services.llm_provider import LLMProvider
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
import os

router = APIRouter()

@router.post("/upload")
async def upload_document(files: list[UploadFile] = File(...), session_id: str = Form("default")):
    provider = LLMProvider()
    if not provider.is_configured():
         raise HTTPException(status_code=500, detail="LLM API Key not configured.")
         
    results = []
    total_chunks = 0
    errors = []
    
    # Process files in parallel to reduce latency
    import asyncio
    
    # 1. Validate files before processing
    valid_files = []
    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".pdf", ".docx", ".txt", ".md"]:
             errors.append(f"{file.filename}: Unsupported file type {ext}")
             continue
             
        # Check size (rough check since we rely on file.file which is spooled)
        # We'll rely on loader to fail if empty, but good to catch obvious ones.
        valid_files.append(file)

    if not valid_files and errors:
         raise HTTPException(status_code=400, detail=f"Validation failed: {'; '.join(errors)}")

    try:
        # Create tasks for all file processing
        tasks = [process_file(file, session_id) for file in valid_files]
        all_chunks_lists = await asyncio.gather(*tasks, return_exceptions=True)

        collection = get_collection()
        if collection is None:
             raise HTTPException(status_code=500, detail="Database not configured.")

        embeddings = provider.get_embeddings()
        vector_store = MongoDBAtlasVectorSearch(
            collection=collection,
            embedding=embeddings,
            index_name="vector_index",
            text_key="text",
            embedding_key="embedding",
        )

        for i, chunks in enumerate(all_chunks_lists):
            file = valid_files[i]
            if isinstance(chunks, Exception):
                print(f"Error processing {file.filename}: {chunks}")
                errors.append(f"{file.filename}: {str(chunks)}")
                continue
            
            if not chunks:
                 print(f"Warning: No content extracted from {file.filename}")
                 errors.append(f"{file.filename}: No content extracted (empty or scannable-only PDF?).")
                 continue

            vector_store.add_documents(chunks)
            total_chunks += len(chunks)
            results.append(file.filename)
        
        if not results:
             # All failed
             detail_msg = "; ".join(errors) if errors else "Processing failed."
             raise HTTPException(status_code=400, detail=f"Failed to process files: {detail_msg}")

        return {
            "status": "success",
            "filenames": results,
            "chunks_processed": total_chunks,
            "errors": errors,
            "message": f"Successfully indexed {len(results)} files. {len(errors)} errors ignored."
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.delete("/reset/{session_id}")
async def delete_session_docs(session_id: str):
    collection = get_collection()
    if collection is None:
         raise HTTPException(status_code=500, detail="Database not configured.")
         
    try:
        result = collection.delete_many({"session_id": session_id})
        return {"status": "success", "deleted_count": result.deleted_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/files/{session_id}/{filename}")
async def delete_specific_file(session_id: str, filename: str):
    collection = get_collection()
    if collection is None:
         raise HTTPException(status_code=500, detail="Database not configured.")
         
    try:
        # Delete documents matching session_id AND source filename
        result = collection.delete_many({
            "session_id": session_id,
            "source": filename
        })
        
        if result.deleted_count == 0:
            # Not strict error, just info
            return {"status": "not_found", "message": "No vectors found for this file."}
            
        return {"status": "success", "deleted_count": result.deleted_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
