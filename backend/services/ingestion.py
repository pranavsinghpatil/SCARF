import os
import shutil
from typing import List
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(upload_file: UploadFile) -> str:
    file_path = os.path.join(UPLOAD_DIR, upload_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

def load_document(file_path: str) -> List[Document]:
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
            return loader.load()
        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
            return loader.load()
        elif ext == ".txt":
            loader = TextLoader(file_path)
            return loader.load()
        elif ext == ".md":
            loader = UnstructuredMarkdownLoader(file_path)
            return loader.load()
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    except Exception as e:
        return []

def split_documents(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000, 
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_documents(documents)

async def process_file(upload_file: UploadFile, session_id: str = "default") -> List[Document]:
    file_path = await save_upload_file(upload_file)
    try:
        raw_docs = load_document(file_path)
        if not raw_docs:
            return []
            
        chunks = split_documents(raw_docs)
        
        for chunk in chunks:
            chunk.metadata["source"] = upload_file.filename
            chunk.metadata["session_id"] = session_id
            if "page" in chunk.metadata:
                 chunk.metadata["page"] = int(chunk.metadata["page"]) + 1
            else:
                 chunk.metadata["page"] = "Unknown"
                 
        return chunks
    except Exception as e:
        raise e
