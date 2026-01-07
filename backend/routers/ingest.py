from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from backend.services.ingestion import process_file
from backend.database import get_collection
from backend.services.llm_provider import LLMProvider
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
import os
import asyncio

router = APIRouter()

@router.post("/upload")
async def upload_document(files: list[UploadFile] = File(...), session_id: str = Form("default")):
    provider = LLMProvider()
    if not provider.is_configured():
         raise HTTPException(status_code=500, detail="LLM API Key not configured.")
         
    results = []
    total_chunks = 0
    errors = []
    
    valid_files = []
    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".pdf", ".docx", ".txt", ".md"]:
             errors.append(f"{file.filename}: Unsupported file type {ext}")
             continue
        valid_files.append(file)

    if not valid_files and errors:
         raise HTTPException(status_code=400, detail=f"Validation failed: {'; '.join(errors)}")

    try:
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
                errors.append(f"{file.filename}: {str(chunks)}")
                continue
            
            if not chunks:
                 errors.append(f"{file.filename}: No content extracted.")
                 continue

            success = False
            for attempt in range(3):
                try:
                    vector_store.add_documents(chunks)
                    success = True
                    break
                except Exception as e:
                    if attempt < 2:
                        await asyncio.sleep(2)
                    else:
                        errors.append(f"{file.filename}: Vector storage failed.")
            
            if success:
                total_chunks += len(chunks)
                results.append(file.filename)
        
        if not results:
             detail_msg = "; ".join(errors) if errors else "Processing failed."
             raise HTTPException(status_code=400, detail=f"Failed to process files: {detail_msg}")

        return {
            "status": "success",
            "filenames": results,
            "chunks_processed": total_chunks,
            "errors": errors,
            "message": f"Successfully indexed {len(results)} files."
        }
    except HTTPException:
        raise
    except Exception as e:
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
        result = collection.delete_many({
            "session_id": session_id,
            "source": filename
        })
        return {"status": "success", "deleted_count": result.deleted_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
