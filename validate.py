"""Quick System Validation for SCARF"""
import sys
import os

print("="*60)
print("SCARF SYSTEM VALIDATION")
print("="*60)

# Test 1: Core Dependencies
print("\n[1/5] Core Dependencies...")
try:
    import fastapi, uvicorn, pydantic, jinja2, requests
    print("✓ FastAPI, Uvicorn, Pydantic, Jinja2, Requests")
except Exception as e:
    print(f"✗ Missing: {e}")
    sys.exit(1)

# Test 2: OCR & PDF  
print("\n[2/5] PDF & OCR Libraries...")
try:
    import fitz, PIL, numpy
    print("✓ PyMuPDF, Pillow, NumPy")
except Exception as e:
    print(f"✗ Missing: {e}")
    sys.exit(1)

try:
    from paddleocr import PaddleOCR
    print("✓ PaddleOCR (Standard)")
except Exception as e:
    print(f"⚠ PaddleOCR: {e}")

# Test 3: Check module files exist
print("\n[3/5] Module Files...")
backend_path = "backend/reasoning_pipeline/modules"
modules = ["module_0_grounder.py", "module_1_segmenter.py", 
           "module_2_extractor.py", "module_3_evidence.py",
           "module_4_assumptions.py", "module_5_gaps.py",
           "module_6_validation.py"]

for mod in modules:
    path = os.path.join(backend_path, mod)
    if os.path.exists(path):
        print(f"✓ {mod}")
    else:
        print(f"✗ Missing: {mod}")
        sys.exit(1)

# Test 4: Prompt Files
print("\n[4/5] Prompt Templates...")
prompt_path = "backend/prompts"
prompts = ["module_1_segmenter.txt", "module_2_extractor.txt",
           "module_3_evidence.txt", "module_4_assumptions.txt",
           "module_5_gaps.txt", "module_6_validation.txt"]

for p in prompts:
    path = os.path.join(prompt_path, p)
    if os.path.exists(path):
        print(f"✓ {p}")
    else:
        print(f"✗ Missing: {p}")

# Test 5: Environment
print("\n[5/5] Environment Configuration...")
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("NOVITA_API_KEY")
if api_key:
    print(f"✓ NOVITA_API_KEY configured ({api_key[:8]}...)")
else:
    print("⚠ NOVITA_API_KEY not set (Mock mode)")

print("\n" + "="*60)
print("✅ SYSTEM VALIDATED - READY TO RUN")
print("="*60)
print("\nLaunch with: ./launch.bat")
print("Frontend: http://localhost:5555")
print("Backend API: http://127.0.0.1:9999/docs")
