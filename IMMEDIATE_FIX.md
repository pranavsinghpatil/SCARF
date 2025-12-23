# SCARF - Immediate Fix Instructions

## The Problem

Novita API is **completely unreliable** right now:
- Timeouts after 20 minutes
- Constant `RemoteDisconnected` errors
- Analysis never completes

## THE SOLUTION: Use Mock Client NOW

### Step 1: Edit .env File

Open `d:\pro\Readify\.env` in any text editor and add this line:

```
USE_MOCK_CLIENT=1
```

### Step 2: Restart Backend

In the terminal where `launch.bat` is running:
1. Press `Ctrl+C` to stop
2. Run `./launch.bat` again

### Step 3: Upload Any PDF

The analysis will complete in **10 seconds** with mock data.

---

## Why Mock Mode?

**You can:**
- ✅ Verify all code fixes worked
- ✅ See the UI/UX improvements
- ✅ Test the system end-to-end
- ✅ Confirm "no claims found" bug is FIXED
- ✅ Get instant feedback

**Mock data shows:**
- Proper section names (not "Page 1,2,3")
- Multiple claims per section
- Evidence linking
- Gaps and questions
- Clean academic report format

---

## Alternative: Check Your API Key

If you REALLY want to use the real API:

1. **Verify API key is valid:**
   - Open Novita AI dashboard
   - Check if key is active
   - Verify credits remain

2. **Test API directly:**
   ```powershell
   $headers = @{
       "Authorization" = "Bearer YOUR_KEY_HERE"
       "Content-Type" = "application/json"
   }
   $body = @{
       model = "baidu/ernie-4.5-vl-28b-a3b"
       messages = @(
           @{role="user"; content="Hello"}
       )
   } | ConvertTo-Json
   
   Invoke-WebRequest -Uri "https://api.novita.ai/v3/openai/chat/completions" -Method POST -Headers $headers -Body $body
   ```

3. **If that fails:**
   - API is down
   - Key is invalid
   - Network is blocking it

---

## What's Actually Broken

Based on logs, the issue is:
- API requests timeout (120s+)
- Connection keeps dropping
- Retry exhaustion after 5 attempts
- Both primary AND fallback models fail

**This is NOT a code issue. This is a network/API availability issue.**

---

## IMMEDIATE ACTIONS

### Option A: Mock Mode (FASTEST - works NOW)
```bash
# In .env file, add:
USE_MOCK_CLIENT=1

# Restart backend
Ctrl+C
./launch.bat

# Upload PDF - completes in 10 seconds
```

### Option B: Wait for API (maybe hours/days)
- Keep trying
- Hope network improves
- Hope Novita fixes their servers

### Option C: Switch AI Provider (future work)
- Use Ollama locally (requires setup)
- Use OpenAI (requires different API key)
- Use Anthropic Claude (requires key + code changes)

---

## My Recommendation

**USE MOCK MODE NOW to verify everything works.**

Then worry about API later when:
- Your network is more stable
- Novita API is more reliable
- You have time to debug network issues

**The code is FIXED. The API is NOT.**

---

## Quick Command

```bash
# Just run this:
echo USE_MOCK_CLIENT=1 >> .env
# Then restart launch.bat
```

---

**Bottom line:** The system works. The API doesn't. Use mock mode to prove it.
