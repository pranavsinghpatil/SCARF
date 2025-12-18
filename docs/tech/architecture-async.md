# Async Architecture: The Job Queue

**Why This Matters**
SCARF relies on two slow processes:
1.  **OCR (Perception)**: Parsing a 10-page PDF takes 5–20 seconds.
2.  **LLM Reasoning (Cognition)**: Generating claims, evidence, and gaps can take 30–60 seconds per module.

A standard HTTP request times out after 30-60 seconds. We cannot keep the user waiting on a loading spinner for 5 minutes.

## 🔄 The Pattern: Async Job Polling

We implement a **Fire-and-Forget** pattern with **State Polling**.

### 1. The Trigger (`POST /analyze`)
The user uploads a PDF. We do **not** process it immediately.
1.  Save PDF to disk (`uploads/{job_id}.pdf`).
2.  Create a `Job` record (in-memory or DB) with status `PENDING`.
3.  Spawn a `Background Task` (FastAPI `BackgroundTasks`).
4.  **Return Immediately**: `202 Accepted` with `{"job_id": "xyz"}`.

### 2. The Worker (The Background Task)
This runs in the background while the user gets their `job_id`.
```python
async def process_pipeline(job_id: str):
    try:
        update_job_status(job_id, "PROCESSING_OCR")
        doc = await run_ocr(job_id)
        
        update_job_status(job_id, "PROCESSING_REASONING")
        report = await run_reasoning(doc)
        
        save_result(job_id, report)
        update_job_status(job_id, "COMPLETED")
    except Exception as e:
        update_job_status(job_id, "FAILED", error=str(e))
```

### 3. The Poller (`GET /status/{job_id}`)
 The frontend polls this endpoint every 2 seconds.
*   **Response**:
    ```json
    {
      "status": "PROCESSING_REASONING",
      "progress": 45,
      "message": "Linking Evidence for Claim 3..."
    }
    ```

### 4. The Result (`GET /report/{job_id}`)
Once status is `COMPLETED`, the frontend requests the final JSON artifact to render the report card.

## ⚡ Concurrency in Python
We use `asyncio` to parallelize independent steps.
*   **Sequential**: OCR (Must happen first).
*   **Parallel**: Once logic is segmented, Module 2 (Claims) and Module 4 (Assumptions) *could* run in parallel if independent (though in v1 strict sequence is safer).

## 🛠 File Structure Implication
*   `backend/tasks.py`: Holds the `process_pipeline` logic.
*   `backend/store.py`: Simple Dictionary-based state store (for hackathon).
