#!/usr/bin/env python3
"""
SCARF System Health Check
Validates all modules, dependencies, and connections.
"""

import sys
import os
from pathlib import Path

# Results tracker
results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

def check(name, func):
    """Run a check and track results"""
    try:
        result = func()
        if result is True or result is None:
            results["passed"].append(name)
            print(f"✓ {name}")
        else:
            results["warnings"].append(f"{name}: {result}")
            print(f"⚠ {name}: {result}")
    except Exception as e:
        results["failed"].append(f"{name}: {str(e)}")
        print(f"✗ {name}: {str(e)}")

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

# ============================================================================
# 1. PYTHON ENVIRONMENT
# ============================================================================
print_section("Python Environment")

check("Python Version (>=3.9)", lambda: sys.version_info >= (3, 9))

# ============================================================================
# 2. CORE DEPENDENCIES
# ============================================================================
print_section("Core Dependencies")

check("FastAPI", lambda: __import__("fastapi") and True)
check("Uvicorn", lambda: __import__("uvicorn") and True)
check("Pydantic", lambda: __import__("pydantic") and True)
check("Jinja2", lambda: __import__("jinja2") and True)
check("Python-dotenv", lambda: __import__("dotenv") and True)
check("Requests", lambda: __import__("requests") and True)

# ============================================================================
# 3. OCR & PDF PROCESSING
# ============================================================================
print_section("OCR & PDF Processing")

check("PyMuPDF (fitz)", lambda: __import__("fitz") and True)
check("Pillow (PIL)", lambda: __import__("PIL") and True)
check("NumPy", lambda: __import__("numpy") and True)

def check_paddleocr():
    from paddleocr import PPStructure
    # Don't initialize here (heavy), just import
    return True

check("PaddleOCR (PPStructure)", check_paddleocr)

# ============================================================================
# 4. REASONING MODULES
# ============================================================================
print_section("Reasoning Pipeline Modules")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def check_module_import(mod_name):
    try:
        module = __import__(f"reasoning_pipeline.modules.{mod_name}", fromlist=[''])
        return True
    except Exception as e:
        return str(e)

check("Module 0: Grounder", lambda: check_module_import("module_0_grounder"))
check("Module 1: Segmenter", lambda: check_module_import("module_1_segmenter"))
check("Module 2: Extractor", lambda: check_module_import("module_2_extractor"))
check("Module 3: Evidence Linker", lambda: check_module_import("module_3_evidence"))
check("Module 4: Assumption Miner", lambda: check_module_import("module_4_assumptions"))
check("Module 5: Gap Analyzer", lambda: check_module_import("module_5_gaps"))
check("Module 6: Validation Synthesizer", lambda: check_module_import("module_6_validation"))

# ============================================================================
# 5. PYDANTIC SCHEMAS
# ============================================================================
print_section("Pydantic Schemas")

def check_schemas():
    from reasoning_pipeline.schemas import (
        Document, Section, RhetoricalMap, SectionRole,
        ClaimList, Claim, EvidenceGraph, EvidenceLink,
        AssumptionLedger, Assumption, GapAnalysis, ValidationReport
    )
    # Try creating a dummy object
    Section(section_id="test", title="Test", page_range=[1], content="test")
    return True

check("Schema Validation", check_schemas)

# ============================================================================
# 6. PROMPT TEMPLATES
# ============================================================================
print_section("Prompt Templates")

prompt_dir = Path("backend/prompts")
required_prompts = [
    "module_1_segmenter.txt",
    "module_2_extractor.txt",
    "module_3_evidence.txt",
    "module_4_assumptions.txt",
    "module_5_gaps.txt",
    "module_6_validation.txt"
]

for prompt in required_prompts:
    path = prompt_dir / prompt
    check(f"Prompt: {prompt}", lambda p=path: p.exists())

# ============================================================================
# 7. ERNIE CLIENT
# ============================================================================
print_section("AI Client (Ernie)")

def check_ernie_client():
    from ernie_pipeline.client import ErnieClient
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("NOVITA_API_KEY")
    if not api_key:
        return "NOVITA_API_KEY not set (will use mock)"
    
    client = ErnieClient()
    # Check session is initialized
    if not hasattr(client, 'session'):
        return "Session not initialized"
    return True

check("Ernie Client Initialization", check_ernie_client)

# ============================================================================
# 8. PIPELINE INTEGRATION
# ============================================================================
print_section("Pipeline Integration")

def check_pipeline():
    from reasoning_pipeline.pipeline import SCARFPipeline
    from ernie_pipeline.client import ErnieClient
    
    # Mock client for test
    class MockClient:
        def call(self, prompt, system=None):
            return '{"test": "data"}'
            
    pipeline = SCARFPipeline(MockClient())
    
    # Check all modules initialized
    assert pipeline.grounder is not None
    assert pipeline.segmenter is not None
    assert pipeline.extractor is not None
    assert pipeline.linker is not None
    assert pipeline.miner is not None
    assert pipeline.analyzer is not None
    assert pipeline.synthesizer is not None
    return True

check("Pipeline Assembly", check_pipeline)

# ============================================================================
# 9. API ENDPOINTS
# ============================================================================
print_section("FastAPI Backend")

def check_api():
    from api.main import app
    routes = [r.path for r in app.routes]
    required = ["/upload", "/status/{job_id}", "/report/{job_id}"]
    for route in required:
        if not any(route in r for r in routes):
            return f"Missing route: {route}"
    return True

check("API Routes", check_api)

# ============================================================================
# 10. FRONTEND BUILD
# ============================================================================
print_section("Frontend")

frontend_dist = Path("NewFrontend/dist")
check("Frontend Build Exists", lambda: frontend_dist.exists() or "Run 'npm run build'")

# ============================================================================
# FINAL REPORT
# ============================================================================
print("\n" + "="*60)
print("  SYSTEM HEALTH REPORT")
print("="*60)

print(f"\n✓ PASSED: {len(results['passed'])}")
for item in results['passed'][:5]:  # Show first 5
    print(f"  • {item}")
if len(results['passed']) > 5:
    print(f"  ... and {len(results['passed']) - 5} more")

if results['warnings']:
    print(f"\n⚠ WARNINGS: {len(results['warnings'])}")
    for item in results['warnings']:
        print(f"  • {item}")

if results['failed']:
    print(f"\n✗ FAILED: {len(results['failed'])}")
    for item in results['failed']:
        print(f"  • {item}")
    print("\n❌ SYSTEM NOT READY")
    sys.exit(1)
else:
    print("\n✅ ALL SYSTEMS OPERATIONAL")
    sys.exit(0)
