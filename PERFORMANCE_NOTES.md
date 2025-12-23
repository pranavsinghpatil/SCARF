# Analysis Performance Investigation

## Issue
After uploading a PDF, analysis takes 15+ minutes and then redirects to home page.

## Likely Causes

### 1. PaddleOCR Initialization (First Run Only)
- **Time**: 30-60 seconds
- **Reason**: Downloads models on first use
- **Fix**: Models are now cached, subsequent runs should be faster

### 2. OCR Processing Time
- **Per Page**: 3-10 seconds (depending on DPI and content)
- **Large Document (50 pages)**: 2.5-8 minutes just for OCR
- **Action**: Check document page count in debug output

### 3. AI API Calls (Ernie)
Each module makes multiple API calls:
- Module 1 (Segmenter): 1 call per section (~50 calls for 50 sections)
- Module 2 (Extractor): 1 call per relevant section (~10-20 calls)
- Module 3 (Evidence): 1 call per claim per section (~50-200 calls)
- Module 4 (Assumptions): 1 call per claim (~10-20 calls)
- Module 5 (Gaps): 1 call per claim (~10-20 calls)
- Module 6 (Validation): 1 call per claim with gaps (~5-10 calls)

**Total**: 150-400 API calls
**Per Call**: 2-5 seconds (with retry logic)
**Total Time**: 5-30 minutes

### 4. Network Issues
- Retry logic (3 attempts per call)
- Timeout: 60 seconds per attempt
- If network is unstable: Each call could take 3 minutes

## Debug Steps

1. **Check Debug Output**:
   ```
   backend/debug_output/{job_id}_1_doc.json
   ```
   - Count number of sections
   - Check if content is populated

2. **Monitor Backend Logs**:
   - Look for "Segmenting Section X/Y..."
   - Look for retry messages
   - Look for timeout errors

3. **Check API Key**:
   - Verify Novita API key is valid
   - Check rate limits

## Solutions

### Short Term
1. **Reduce Sections**: Process only first 20 pages for testing
2. **Batch API Calls**: Combine multiple sections in one prompt (risky for accuracy)
3. **Increase Timeout Limit**: Frontend now has 20-minute timeout

### Long Term
1. **Caching**: Save intermediate results, resume on failure
2. **Parallel Processing**: Run modules concurrently where possible
3. **Streaming Updates**: Send partial results as they complete
4. **Server-Side Events (SSE)**: Replace polling with real-time updates

## Quick Fix Applied
1. ✓ Added 20-minute timeout to frontend polling
2. ✓ Added error state display
3. ✓ Added retry counter for 404 responses
4. ✓ Progress messages now show which section/claim is being processed

## Expected Behavior Now
- Analysis completes within 20 minutes OR shows timeout error
- Progress bar updates smoothly
- If backend restarts, shows "job not found" error instead of infinite loading
- Clear error message if something fails
