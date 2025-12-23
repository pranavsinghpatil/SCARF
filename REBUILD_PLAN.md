# SCARF Performance Optimization Strategy

## Critical Issues Identified

### 1. Too Many AI Calls
**Current:**
- Module 1: 1 call per section (~50 calls for 50-page paper)
- Module 3: 1 call per claim per section (~500 calls worst case)
- **Total: 600+ API calls for large paper**

**Optimized:**
- Module 1: Batch sections into groups of 5 (~10 calls)
- Module 3: Single call with all claims + relevant sections (~20 calls)
- **Target: <50 API calls**

### 2. Slow OCR
**Current:** PaddleOCR processes each page individually (10 sec/page = 8 min for 50 pages)
**Optimized:** PyMuPDF text extraction (instant for text PDFs)

### 3. Sequential Processing
**Current:** Modules run one after another
**Optimized:** Parallelize where possible (Modules 3 & 4 can run simultaneously)

---

## Implementation Plan

### Phase 1: Quick Wins (Immediate) ✅
1. ✅ Replace OCR with PyMuPDF text extraction
2. ✅ Smart section detection (heuristics)
3. ✅ Remove "Page 1,2,3" nonsense

### Phase 2: Batching (Next)
**Module 1 (Segmenter):**
```python
# Instead of:
for section in sections:
    role = call_ai(section)

# Do:
for batch in chunks(sections, 5):
    roles = call_ai_batch(batch)  # Single prompt with 5 sections
```

**Module 3 (Evidence):**
```python
# Instead of:
for claim in claims:
    for section in sections:
        evidence = call_ai(claim, section)

# Do:
for claim in claims:
    evidence = call_ai(claim, all_relevant_sections)  # Single call
```

### Phase 3: Caching
- Save OCR results per PDF hash
- Reuse if same document uploaded again

### Phase 4: Parallel Processing
```python
import concurrent.futures

with ThreadPoolExecutor() as executor:
    evidence_future = executor.submit(linker.run, doc, claims)
    assumptions_future = executor.submit(miner.run, doc, claims)
    
    evidence = evidence_future.result()
    assumptions = assumptions_future.result()
```

---

## Expected Performance

### Before Optimization
- 50-page paper: 15-20 minutes
- API calls: 600+
- User sees: "Page 1", "Page 2" 🤦

### After Optimization
- 50-page paper: **3-5 minutes**
- API calls: **~40**
- User sees: "Introduction", "Methods" ✅

---

## Files to Modify

1. ✅ `module_0_grounder.py` - DONE (PyMuPDF + section detection)
2. ⏳ `module_1_segmenter.py` - Batch processing
3. ⏳ `module_3_evidence.py` - Smart batching
4. ✅ `ReportDashboard.tsx` - DONE (clean UI)
5. ⏳ `tasks.py` - Parallel execution

---

## Priority Actions

**RIGHT NOW:**
- Module 0 is fixed (smart sections)
- UI is fixed (claim-focused)
- Next: Implement batching in Module 1 and 3

**Estimated Total Time:**
- Batching implementation: 2 hours
- Testing & iteration: 1 hour
- **Total rebuild: 3 hours**

---

## Validation Checklist

After rebuild, test with:
1. Small paper (5 pages) - Should complete in <1 minute
2. Medium paper (20 pages) - Should complete in ~2 minutes
3. Large paper (50 pages) - Should complete in <5 minutes

Success criteria:
- ✅ Shows "Introduction", "Methods", not "Page 1"
- ✅ Claims appear within 60 seconds
- ✅ No "linking failed" errors
- ✅ UI is clean and usable
- ✅ Results make sense
