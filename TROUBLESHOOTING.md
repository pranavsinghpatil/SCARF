# Results Not Showing - Debugging Guide

## Symptoms
- Analysis completes (100% progress)
- Screen goes blank or redirects to home
- No error message displayed
- Results dashboard doesn't appear

## Immediate Debugging Steps

### 1. Open Browser DevTools (F12)
**Console Tab:**
Look for messages starting with `[SCARF]`:
```
[SCARF] Fetching report for job: {uuid}
[SCARF] Backend data received: {...}
[SCARF] Mapped data: {...}
[SCARF] Report state set to complete
```

**What to check:**
- Are there any red errors?
- Does "Backend data received" show an empty object `{}`?
- Does "Mapped data" have claims: `{claims: [], sections: []}`?

### 2. Check Backend Debug Output
Navigate to: `backend/debug_output/`

Find files named: `{job_id}_*.json`

**Check in order:**
1. `1_doc.json` - Did OCR extract text?
   ```json
   {
     "sections": [
       {"content": "Lorem ipsum..."} // Should have text, not empty
     ]
   }
   ```

2. `3_claims.json` - Were claims extracted?
   ```json
   {
     "claims": [
       {"statement": "..."} // Should have claims
     ]
   }
   ```

### 3. Check Backend Logs
In the terminal running `./launch.bat`:

**Look for:**
- ✓ `[INFO] Starting Claim Extraction...`
- ✗ `[ERROR] Module 2 Error: ...`
- ⚠ `[WARNING] No text found in PDF!`

### 4. Test API Endpoints Directly

**Get Job Status:**
```
http://127.0.0.1:9999/status/{job_id}
```
Should return:
```json
{
  "status": "COMPLETED",
  "progress": 100,
  "message": "Analysis Complete."
}
```

**Get Report:**
```
http://127.0.0.1:9999/report/{job_id}
```
Should return large JSON with `claims`, `evidence`, etc.

## Common Issues & Fixes

### Issue 1: Empty Claims Array
**Symptom:** `3_claims.json` shows `{"claims": []}`

**Causes:**
1. Document is not a scientific paper (no claims to extract)
2. OCR failed (check `1_doc.json` for empty content)
3. AI model hallucinated or returned invalid JSON

**Fix:**
- Use a known scientific PDF (e.g., from arXiv)
- Check if text extraction worked
- Review backend logs for JSON parsing errors

### Issue 2: Frontend Shows Blank Screen
**Symptom:** Progress reaches 100%, then nothing

**Causes:**
1. React render error (check Console for errors)
2. State not updating to "complete"
3. Data mapping failed

**Fix:**
- Check Console for `[SCARF] Report state set to complete`
- Look for React errors in Console
- Verify `reportData` is not null

### Issue 3: Results Take Forever
**Symptom:** Stuck at high progress (e.g., 85%)

**Causes:**
1. Module 6 (Validation) is slow
2. Network timeout
3. API rate limiting

**Fix:**
- Wait up to 20 minutes (now has timeout)
- Check backend logs for retry messages
- Verify internet connection stable

## Updated Behavior (After Fixes)

### Success Case:
1. Progress bar reaches 100%
2. "Analysis Complete" message
3. Dashboard shows with:
   - Claims count
   - Gap ratio
   - Executive summary
   - Claim cards

### Empty Results Case:
1. Progress bar reaches 100%
2. "Analysis Complete - No Claims Found" warning
3. Explanation of why (OCR failed, not a scientific paper, etc.)
4. Button to view debug output

### Error Case:
1. Red error screen
2. Clear error message
3. "Try Another Document" button

## Still Not Working?

### Last Resort Checks:

1. **Backend Running?**
   ```
   http://127.0.0.1:9999/
   ```
   Should show: `{"message": "SCARF Reasoning Engine API is Online..."}`

2. **CORS Issue?**
   Console shows: `Access-Control-Allow-Origin`
   - Restart backend
   - Clear browser cache

3. **State Corruption?**
   - Hard refresh browser (Ctrl+F5)
   - Clear localStorage
   - Restart both frontend and backend

4. **Check Job Store:**
   In `backend/tasks.py`, jobs are stored in memory.
   If backend restarts, job is lost.
   - Keep backend running during analysis
   - Check "job not found" error

## Quick Test

**Minimal valid test:**
1. Use a 2-page scientific PDF
2. Upload
3. Should complete in ~2 minutes
4. Should show at least 1-2 claims

If this fails, something is fundamentally broken.
Check all steps above systematically.
