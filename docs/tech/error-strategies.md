# Resilience & Error Strategies

**Why This Matters**
AI Systems are non-deterministic. They fail in creative ways.
*   "I cannot answer this."
*   Returns Invalid JSON.
*   Hallucinates data not in the source.

SCARF must be **Robust**, not Fragile.

## 🛡 The Defense Layers

### Layer 1: The OCR Guard (Module 0)
*   **Risk**: OCR produces garbage text for complex math/diagrams.
*   **Strategy**:
    *   **Confidence Filtering**: Drop text blocks with average OCR confidence < 60%.
    *   **Layout Preservation**: Keep "Tables" as separate HTML/Markdown blocks, do not squash them into plain text.

### Layer 2: The Hallucination Guard (Prompting)
*   **Risk**: Model invents claims.
*   **Strategy**: "Grounding Prompts".
    *   Every extraction must cite a `source_section_id`.
    *   If the model extracts a claim but points to a non-existent section, we **discard** it.

### Layer 3: The Format Guard (Pydantic)
*   **Risk**: Model returns Markdown-wrapped JSON (```json ... ```).
*   **Strategy**:
    *   **Preprocessor**: Regex strip `^```json` and ````$`.
    *   **Validator**: Use Pydantic's strict mode.

### Layer 4: The Fallback
*   If a Module fails (e.g., Evidence Linker crashes):
    *   **Do not crash the job.**
    *   Mark that specific module as `SKIPPED` in the report.
    *   Return the partial report (Claims without Evidence are better than nothing).

## 🚨 HTTP Error Mapping
*   **400 Bad Request**: Invalid PDF (password protected, corrupted).
*   **429 Too Many Requests**: Novita API rate limit hit. (Handled via Exponential Backoff).
*   **500 Internal Error**: Code bug (logs sent to stderr).
