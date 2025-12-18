
from .reasoning_pipeline.pipeline import SCARFPipeline
from .ernie_pipeline.client import ErnieClient
import asyncio
import os

# Initialize Client
# Check if key exists to decide whether to mock or not for dev convenience
if os.getenv("NOVITA_API_KEY"):
    PIPELINE = SCARFPipeline(ErnieClient())
else:
    print("WARNING: No NOVITA_API_KEY found. Using Mock ERNIE.")
    class MockErnie:
        def call(self, prompt, system=None):
            return "{}"
    PIPELINE = SCARFPipeline(MockErnie())

async def run_pipeline_task(job_id: str, file_path: str, job_store: dict):
    """
    The main background worker.
    """
    try:
        job_store[job_id]["status"] = "PROCESSING_OCR"
        job_store[job_id]["progress"] = 10
        
        # 1. Pipeline Run
        # Note: pipeline.run is synchronous in our v1 code, so we run it directly
        # In prod, we might offload to a thread if it blocks too much.
        result = PIPELINE.run(file_path, job_id)
        
        job_store[job_id]["status"] = "COMPLETED"
        job_store[job_id]["progress"] = 100
        job_store[job_id]["result"] = result
        
    except Exception as e:
        job_store[job_id]["status"] = "FAILED"
        job_store[job_id]["error"] = str(e)
