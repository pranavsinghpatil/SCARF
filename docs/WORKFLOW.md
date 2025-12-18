# System Workflow: The SCARF Pipeline

This document details the **Reasoning Assembly Line** for SCARF.

## 🔄 High-Level Data Flow

The system processes a paper in sequential modules. Each module enriches the structural representation.

### 1. Ingestion Phase
*   **User Upload**: Drag & Drop PDF.
*   **Validation**: Check file size (<10MB) and type.

### 2. Perception Phase (Module 0)
*   **Tool**: `PaddleOCR-VL`.
*   **Action**: Convert PDF images into a "Grounded Document" object.
*   **Output**: Sections (S1, S2...) with bounding boxes.

### 3. Reasoning Phase (Modules 1-6)
*   **Orchestrator**: Python `async` loop.
*   **Step 1**: Classify Rhetoric (Intro? Method?).
*   **Step 2**: Extract Claims (Novelty?).
*   **Step 3**: Link Evidence (Tables? Figures?).
*   **Step 4**: Infer Assumptions (Metrics? Data?).
*   **Step 5**: Detect Gaps (Missing links?).
*   **Step 6**: Synthesize Questions.

### 4. Presentation Phase
*   **UI**: Validation Report Card.
*   **Interactive**: Click a "Gap Signal" -> Highlight the specific text in the PDF that is missing context.

---

## 🧠 Mental Model
We do not ask the LLM to "Read the paper".
We ask it to **perform specific cognitive tasks** on specific data chunks.
`Page -> Section -> Rhetoric -> Claim -> Proof -> Critique`.
