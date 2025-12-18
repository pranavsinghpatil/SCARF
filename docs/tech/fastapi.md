# FastAPI in SCARF

**Why FastAPI?**
FastAPI is modern, fast (high performance), and easy to use. It's built on top of Starlette for the web parts and Pydantic for the data parts.

## ⚡ Core Concepts

### 1. Dependency Injection
We use this to manage database connections, settings, and shared logic.

```python
from fastapi import Depends, FastAPI

def get_settings():
    return config.Settings()

@app.post("/upload")
async def upload_pdf(settings: config.Settings = Depends(get_settings)):
    print(settings.upload_dir)
```

**Why?**
*   Makes testing easy (we can override `get_settings` with a mock).
*   Keeps code clean and modular.

### 2. Background Tasks
Processing a PDF takes time (OCR + AI). We can't make the user wait 2 minutes for a response.

```python
from fastapi import BackgroundTasks

@app.post("/process/{job_id}")
async def start_processing(job_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(pipeline.run_full_pipeline, job_id)
    return {"message": "Processing started", "job_id": job_id}
```

The user gets a "Processing started" response instantly, while the server works in the background.

### 3. Pydantic Models for Validation
Input validation is automatic.

```python
class QuestionRequest(BaseModel):
    context: str
    question: str
    max_length: int = 500

@app.post("/ask")
async def ask_question(req: QuestionRequest):
    # req.context is guaranteed to be a string
    # req.max_length defaults to 500 if missing
    return ernie.answer(req.context, req.question)
```

### 4. Automatic Documentation
FastAPI generates Swagger UI (`/docs`) and ReDoc (`/redoc`) automatically.
*   **Swagger UI**: Interactive. We use it to test our API endpoints manually.
*   **ReDoc**: Clean documentation for sharing.

## 🏗 Structure in SCARF

## 🏗 Structure in SCARF

*   `backend/api/main.py`: The entry point. Defines the `app`.
*   `backend/api/routers/`: Splits routes into modules (e.g., `upload.py`, `query.py`).
*   `backend/reasoning_pipeline/`: Core logic modules.
*   `backend/reasoning_pipeline/schemas.py`: The Pydantic Contracts.

## 🚀 Performance Tips
*   **Uvicorn**: We run FastAPI with Uvicorn, an ASGI server.
*   **Workers**: In production, we run multiple workers (`uvicorn main:app --workers 4`) to handle concurrent requests.
