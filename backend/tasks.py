
from .reasoning_pipeline.pipeline import SCARFPipeline
from .ernie_pipeline.client import ErnieClient
from .ernie_pipeline.mock_client import MockErnieClient
import asyncio
import os

# Initialize Client
# Set USE_MOCK_CLIENT=1 in .env or environment to test without API
use_mock = os.getenv("USE_MOCK_CLIENT", "0") == "1"

if use_mock:
    print("⚠️  WARNING: Using MockErnieClient - NO actual API calls will be made!")
    print("⚠️  Set USE_MOCK_CLIENT=0 or remove it from .env to use real API")
    PIPELINE = SCARFPipeline(MockErnieClient())
elif os.getenv("NOVITA_API_KEY"):
    print("✓ Using Novita AI API")
    PIPELINE = SCARFPipeline(ErnieClient())
else:
    print("❌ ERROR: No NOVITA_API_KEY found and USE_MOCK_CLIENT not set.")
    print("   Either set NOVITA_API_KEY in .env or set USE_MOCK_CLIENT=1 for testing")
    raise RuntimeError("No API key and mock mode not enabled")


def run_pipeline_task(job_id: str, file_path: str, job_store: dict):
    """
    The main background worker.
    """
    try:
        def update_progress(msg: str):
            job_store[job_id]["message"] = msg 
            # Note: We do not await here because it's called from synchronous module code.
            # This relies on the polling endpoint seeing the change in shared memory.

        # Inject callback into modules
        PIPELINE.segmenter.progress_callback = update_progress

        PIPELINE.extractor.progress_callback = update_progress
        PIPELINE.linker.progress_callback = update_progress
        PIPELINE.miner.progress_callback = update_progress
        PIPELINE.analyzer.progress_callback = update_progress
        PIPELINE.synthesizer.progress_callback = update_progress

        job_store[job_id]["status"] = "PROCESSING_OCR"
        job_store[job_id]["progress"] = 10
        job_store[job_id]["message"] = "Grounding PDF (OCR)..."
        
        if not os.path.exists("debug_output"):
            os.makedirs("debug_output")
        
        # Helper to dump debug
        def dump_step(name, data):
            with open(f"debug_output/{job_id}_{name}.json", "w", encoding="utf-8") as f:
                if hasattr(data, "model_dump_json"):
                    f.write(data.model_dump_json(indent=2))
                else:
                    import json
                    json.dump(data, f, indent=2, default=str)

        # 1. Grounding
        doc = PIPELINE.grounder.run(file_path, job_id)
        dump_step("1_doc", doc)
        
        # Validation checks
        has_content = any(len(s.content.strip()) > 50 for s in doc.sections)
        sec_count = len(doc.sections)
        
        if not has_content:
             job_store[job_id]["message"] = "WARNING: PDF seems empty or scanned image. OCR might have failed."
             update_progress("WARNING: PDF text extraction failed or empty.")
             # We effectively stop here or continue knowing it will fail
        else:
             job_store[job_id]["time_grounding"] = str(sec_count)
             
        job_store[job_id]["progress"] = 25
        job_store[job_id]["message"] = f"OCR Complete. Analyzing {sec_count} sections..."

        # 2. Segmentation
        rhetoric = PIPELINE.segmenter.run(doc)
        dump_step("2_rhetoric", rhetoric)
        job_store[job_id]["progress"] = 40
        job_store[job_id]["message"] = f"Structure mapped. Extracting claims..."
        
        # Store partial results
        job_store[job_id]["partial_results"] = {
            "doc": doc.dict(),
            "rhetoric": rhetoric.dict(),
            "stage": "segmentation_complete"
        }

        # 3. Claims
        claims = PIPELINE.extractor.run(doc, rhetoric)
        dump_step("3_claims", claims)
        claim_count = len(claims.claims)
        job_store[job_id]["progress"] = 55
        job_store[job_id]["message"] = f"Found {claim_count} claims. Linking evidence..."
        
        # Update partial results with claims
        job_store[job_id]["partial_results"] = {
            "doc": doc.dict(),
            "rhetoric": rhetoric.dict(),
            "claims": claims.dict(),
            "stage": "extraction_complete"
        }

        # 4 & 5: Evidence + Assumptions (RUN IN PARALLEL)
        from concurrent.futures import ThreadPoolExecutor
        import logging
        
        logging.info("Running Evidence Linking and Assumption Mining in parallel...")
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            evidence_future = executor.submit(PIPELINE.linker.run, doc, claims)
            assumptions_future = executor.submit(PIPELINE.miner.run, doc, claims)
            
            # Wait for both to complete
            evidence = evidence_future.result()
            assumptions = assumptions_future.result()
        
        dump_step("4_evidence", evidence)
        job_store[job_id]["progress"] = 70
        job_store[job_id]["message"] = f"Evidence linked. Analyzing logic & gaps..."
        
        # Update partial results with both evidence and assumptions
        job_store[job_id]["partial_results"] = {
            "doc": doc.dict(),
            "rhetoric": rhetoric.dict(),
            "claims": claims.dict(),
            "evidence": evidence.dict(),
            "assumptions": assumptions.dict(),
            "stage": "parallel_complete"
        }
        
        dump_step("5_assumptions", assumptions)
        job_store[job_id]["progress"] = 85
        job_store[job_id]["message"] = "Generating validation questions..."
        
        # 6. Gaps
        gaps = PIPELINE.analyzer.run(claims, evidence, assumptions)
        dump_step("6_gaps", gaps)
        
        # Update partial results with gaps
        job_store[job_id]["partial_results"] = {
            "doc": doc.dict(),
            "rhetoric": rhetoric.dict(),
            "claims": claims.dict(),
            "evidence": evidence.dict(),
            "assumptions": assumptions.dict(),
            "gaps": gaps.dict(),
            "stage": "gaps_complete"
        }
        
        # 7. Validation
        validation = PIPELINE.synthesizer.run(gaps)
        dump_step("7_validation", validation)
        
        result = {
            "doc": doc.dict(),
            "rhetoric": rhetoric.dict(),
            "claims": claims.dict(),
            "evidence": evidence.dict(),
            "assumptions": assumptions.dict(),
            "gaps": gaps.dict(),
            "validation": validation.dict()
        }
        
        job_store[job_id]["status"] = "COMPLETED"
        job_store[job_id]["progress"] = 100
        job_store[job_id]["message"] = "Analysis Complete."
        job_store[job_id]["result"] = result
        
    except Exception as e:
        job_store[job_id]["status"] = "FAILED"
        job_store[job_id]["error"] = str(e)
        job_store[job_id]["message"] = f"Error: {str(e)}"
