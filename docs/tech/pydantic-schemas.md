# Pydantic: The Data Contract

**Why This Matters**
In traditional software, functions return predictable types.
In AI Engineering, LLMs return **text**. This is chaotic.

SCARF uses **Pydantic** to force the LLM into a specific "Contract". If the LLM breaks the contract, the system refuses to proceed.

## 📜 The Schema as the Source of Truth
We define our "mental model" in `backend/reasoning_pipeline/schemas.py`.

```python
class ScientificClaim(BaseModel):
    claim_id: str
    statement: str
    confidence: float
```

This class is used for:
1.  **Prompt Construction**: We inject `ScientificClaim.model_json_schema()` into the system prompt.
2.  **Output Parsing**: We parse the LLM's JSON response directly into this object.
3.  **API Response**: We verify the API output matches this structure before sending it to the frontend.

## 🛡 Strategies for "Strict JSON"
Since we are using `requests` (no fancy frameworks), we use a **Retry-Repair Loop**:

1.  **Generate**: Call ERNIE with schema instructions.
2.  **Parse**: Try `ScientificClaim.model_validate_json(response)`.
3.  **Fail?**:
    *   Catch `ValidationError`.
    *   **Repair**: If it's a small JSON error (missing quotes), try a JSON repair utility.
    *   **Retry**: If deep semantic error, call ERNIE again with the error message: *"You failed to provide field 'confidence'. Retry."*

## 🚀 Why this is "Research Grade"
By defining strict schemas, we decouple the **Model** from the **System**.
*   We can swap ERNIE for GPT-4 or Claude without changing application logic.
*   We can upgrade the schema (add `citation_index`) without rewriting the prompt logic manually (dynamic prompt generation).
