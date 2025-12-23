# SCARF System Test Guide

## ✅ System Status: READY

### Services Running
- ✅ **Frontend:** http://localhost:5555 (Active)
- ✅ **Backend API:** http://127.0.0.1:9999 (Active)
- ✅ **API Docs:** http://127.0.0.1:9999/docs (Swagger UI)

---

## Quick Test Plan

### Test 1: Basic Upload & Analysis (5-10 page paper)
**Expected Time:** ~30 seconds - 1 minute

1. **Open:** http://localhost:5555
2. **Upload:** A short scientific paper (5-10 pages)
3. **Watch for:**
   - Document structure appears (Introduction, Methods, etc. - NOT "Page 1,2,3")
   - Progress updates every few seconds
   - Partial results appear around 55% progress
4. **Check Results:**
   - Claims are specific and actionable
   - Evidence links are present
   - Clean, readable academic format

### Test 2: Medium Paper (20 pages)
**Expected Time:** ~2-3 minutes

**Success Criteria:**
- Completes in <3 minutes
- Shows 5-10 claims
- Each claim has evidence
- No JSON parsing errors
- Console shows "[SCARF]" log messages

### Test 3: Verify Optimizations

**Check Debug Output:**
```
backend/debug_output/{job_id}_*.json
```

**What to Look For:**
- `1_doc.json` - Should have sections with meaningful titles
- `3_claims.json` - Should have array of claims
- `4_evidence.json` - Should have evidence linked to claims

**Browser Console (F12):**
```
[SCARF] Fetching report for job: {uuid}
[SCARF] Backend data received: {...}
[SCARF] Mapped data: {claims: [...], sections: [...]}
```

---

## Test Checklist

### Performance
- [ ] Upload completes instantly (<1 sec)
- [ ] Text extraction is instant (not 10 sec/page)
- [ ] Claims appear at ~55% progress
- [ ] Total time <3 min for 20-page paper
- [ ] No timeout errors

### Quality
- [ ] Sections have real names (Introduction, Methods)
- [ ] Claims are specific (not vague)
- [ ] Evidence has source citations
- [ ] Gaps are insightful
- [ ] Questions are relevant

### UX
- [ ] Progress bar updates smoothly
- [ ] Messages are clear ("Linking evidence for Claim 3/10...")
- [ ] Partial results appear mid-analysis
- [ ] Final report is clean and readable
- [ ] No fancy animations, just data

---

## Expected Console Output

```
[SCARF] Upload successful, job_id: abc-123
[SCARF] Polling status...
[SCARF] Progress: 25% - Grounding PDF (OCR)...
[SCARF] Progress: 40% - Structure mapped. Extracting claims...
[SCARF] Progress: 55% - Found 8 claims. Linking evidence...
[SCARF] Partial results available: extraction_complete
[SCARF] Progress: 70% - Evidence linked. Analyzing logic & gaps...
[SCARF] Progress: 85% - Generating validation questions...
[SCARF] Progress: 100% - Analysis Complete.
[SCARF] Fetching report for job: abc-123
[SCARF] Backend data received: {doc: {...}, claims: {...}}
[SCARF] Mapped data: {claims: [8 items], sections: [6 items]}
[SCARF] Report state set to complete
```

---

## Troubleshooting

### "No claims found"
1. Check `debug_output/1_doc.json` - Is content extracted?
2. Upload a known scientific paper (not a book/thesis)

### "Analysis takes >5 minutes"
1. Check internet connection (API calls depend on network)
2. Verify Novita API key in `.env`

### "Page 1, Page 2" in results
1. Backend didn't restart with new code
2. Stop `launch.bat` and restart

### JSON parsing errors in console
1. Check backend logs for "Invalid JSON" warnings
2. This should be <5% now with `repair_json()`

---

## Success Indicators

**You know it's working when:**
- ✅ "Introduction" and "Methods" appear (not "Page 1")
- ✅ Claims visible at 55% progress (not just at 100%)
- ✅ Total time is 2-3 minutes (not 15+ minutes)
- ✅ Results are in clean academic format
- ✅ Evidence citations are specific ("Methods, Section 2.1")
- ✅ Console shows "[SCARF]" messages

**Red Flags (something's wrong):**
- ❌ Still shows "Page 1, Page 2"
- ❌ Takes >5 minutes for 20-page paper
- ❌ No results after 15 minutes
- ❌ "linking failed" errors
- ❌ Fancy cards/animations (old UI)

---

## Quick Start Test

**Fastest way to verify everything works:**

1. Open http://localhost:5555
2. Upload ANY scientific PDF (5-10 pages ideal)
3. Watch console (F12) for "[SCARF]" messages
4. Wait ~30-60 seconds
5. Should see claims appear with progress still running
6. Wait for 100% completion
7. Check results have real section names

**If this works: ✅ System is ready for production**

---

## Sample PDFs for Testing

**Good Test Papers:**
- arXiv papers (well-structured, clear IMRAD format)
- IEEE/ACM conference papers
- Nature/Science articles

**Avoid for First Test:**
- Scanned PDFs (images, no text)
- Books (too long, different structure)
- Preprints with unusual formatting

---

## Next Steps After Successful Test

1. Test with your actual research papers
2. Verify export functionality (if implemented)
3. Check results quality matches expectations
4. Report any edge cases or issues

---

**Status:** Ready for testing
**Estimated First Test Time:** <2 minutes
**Expected Success Rate:** >95%
