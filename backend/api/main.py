
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
import shutil
import os
import uuid
# from ..reasoning_pipeline.pipeline import SCARFPipeline
# from ..ernie_pipeline.client import ErnieClient

app = FastAPI(title="SCARF API", description="Scientific Claim-Assumption-Rationale Framework")

# In-memory job store for hackathon (use Redis in prod)
JOBS = {}

from ..tasks import run_pipeline_task

@app.post("/upload")
async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    file_location = f"uploads/{job_id}.pdf"
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    JOBS[job_id] = {"status": "PENDING", "progress": 0, "message": "Queued"}
    
    background_tasks.add_task(run_pipeline_task, job_id, file_location, JOBS)
    
    return {"job_id": job_id, "message": "Upload successful. Processing started."}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"message": "Job not found"})
    return job

@app.get("/report/{job_id}")
async def get_report(job_id: str):
    # Retrieve result from disk/memory
    job = JOBS.get(job_id)
    if not job or "result" not in job:
        return JSONResponse(status_code=404, content={"message": "Report not ready"})
    return job["result"]

# Mount Frontend
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount Static Assets (CSS, JS)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Serve Index.html
@app.get("/")
async def read_index():
    return FileResponse('frontend/templates/index.html')
