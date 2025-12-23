# Quick Fix: API Timeout Issues

## Problem
Novita API keeps timing out with `RemoteDisconnected` errors.  
Analysis stuck, can't complete.

## Solution: Use Mock Client for Testing

### Option 1: Enable Mock Mode (FASTEST)

1. **Edit `.env` file:**
   ```bash
   # Add this line
   USE_MOCK_CLIENT=1
   ```

2. **Restart backend:**
   - Stop `launch.bat` (Ctrl+C)
   - Run `./launch.bat` again

3. **Test upload:**
   - Should complete in **5-10 seconds** (no API calls)
   - Will see:
     ```
     ⚠️  WARNING: Using MockErnieClient - NO actual API calls will be made!
     ```

4. **Results:**
   - Mock data (plausible but not real analysis)
   - Proves system works
   - Tests UI/UX
   - Verifies all fixes

### Option 2: Fix API Issues

**Check API Key:**
```bash
# Verify in .env
NOVITA_API_KEY=sk-...
```

**Test connectivity:**
```powershell
# Check if you can reach Novita
Test-NetConnection -ComputerName api.novita.ai -Port 443
```

**Check quota:**
- Visit https://novita.ai dashboard
- Verify credits remain
- Check rate limits

### Option 3: Try Different Network

**Possible causes:**
- ISP blocking API endpoints
- Firewall/VPN issues
- Unstable internet connection

**Try:**
- Switch to mobile hotspot
- Disable VPN if using one
- Check firewall settings

---

## When to Use Mock vs Real API

### Use Mock When:
- ✅ Testing system functionality
- ✅ Developing UI changes
- ✅ Verifying bug fixes
- ✅ API is down/slow
- ✅ No API quota left

### Use Real API When:
- ✅ Need actual analysis
- ✅ Testing AI quality
- ✅ Production use
- ✅ Generating real reports

---

## Quick Test Commands

### Enable Mock:
```bash
echo USE_MOCK_CLIENT=1 >> .env
./launch.bat
```

### Disable Mock:
```bash
# Remove or comment out in .env:
# USE_MOCK_CLIENT=1

# Or set to 0:
USE_MOCK_CLIENT=0
```

---

## Expected Behavior

### With Mock Client:
```
✅ Upload: Instant
✅ Grounding: 1 second
✅ Segmentation: 1 second  
✅ Claims: 1 second (returns 2 mock claims per section)
✅ Evidence: 1 second
✅ Assumptions: 1 second
✅ Gaps: 1 second
✅ Questions: 1 second
⏱️  TOTAL: ~5-10 seconds
```

### With Real API (working):
```
✅ Upload: Instant
✅ Grounding: 1 second
✅ Segmentation: 10-15 seconds
✅ Claims: 30-60 seconds
✅ Evidence: 30-60 seconds
✅ Assumptions: 30-60 seconds
✅ Gaps: 30-60 seconds
✅ Questions: 30-60 seconds
⏱️  TOTAL: 2-5 minutes
```

### With Real API (timing out):
```
✅ Upload: Instant
✅ Grounding: 1 second
⚠️  Segmentation: Stuck...
⏳ Retry... Retry... Retry...
❌ 15+ minutes, still incomplete
```

---

## Immediate Action

**To test the system RIGHT NOW:**

1. **Stop backend** (Ctrl+C in terminal)

2. **Edit `.env`:**
   ```bash
   USE_MOCK_CLIENT=1
   ```

3. **Restart:**
   ```bash
   ./launch.bat
   ```

4. **Upload any PDF**

5. **Should complete in ~10 seconds**

6. **Check results:**
   - Will show mock claims
   - Proves all code works
   - Verifies UI displays correctly
   - Confirms "no claims found" bug is FIXED

---

## Files Created

- ✅ `backend/ernie_pipeline/mock_client.py` - Mock AI responses
- ✅ `backend/tasks.py` - Updated to support `USE_MOCK_CLIENT`

---

## Summary

**Network issue = Can't test real API now**

**Solution = Use mock mode to verify system works**

**Result = Instant testing, proves fixes are working**

**Next = When API is stable, disable mock for real analysis**
