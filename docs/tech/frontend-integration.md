# Frontend Integration: The Report Card

**Why This Matters**
The output of SCARF is not a chat stream. It is a **Structured Report**.
The Frontend must verify and visualize this structure effectively.

## 🏗 Interaction Model (Client-Side Polling)
Since we are keeping the frontend simple (HTML + Vanilla JS):

1.  **Upload Page**: Simple Form `multipart/form-data`.
2.  **Loading Page**:
    *   Receives `job_id`.
    *   `setInterval()` every 2s to fetch `/status/{job_id}`.
    *   Update Progress Bar text: "Identifying Claims...", "Checking Assumptions...".
3.  **Report Page**:
    *   Fetched via `/report/{job_id}`.
    *   Renders the JSON data.

## 🎨 Visualization Stategy

### 1. The Claim–Evidence Table
*   **Layout**: A Data Grid or Card Layout.
*   **Column 1**: The Claim (Bold).
*   **Column 2**: Evidence Type (Badge: Green for Quant, Blue for Qual, Red for None).
*   **Column 3**: Snippet (Click to expand).

### 2. The Gap Signals
*   **Visual**: Warning cards or "Admonitions" (Yellow background).
*   **Interaction**: Hovering a Gap Signal highlights the related Claim.

### 3. The Source Viewer (Stretch Goal)
*   **Left Pane**: The Rendered Report.
*   **Right Pane**: The PDF (rendered as images).
*   **Interaction**: Clicking a citation `[S3]` scrolls the Right Pane to Section 3.

## 🔗 The Data Link
The Frontend expects the exact JSON structure defined in `backend.reasoning_pipeline.schemas`.
Any change in `schemas.py` must be reflected in the JS rendering logic.
