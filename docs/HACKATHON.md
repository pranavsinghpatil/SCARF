# ERNIE AI Developer Challenge – Context for SCARF

This document maps the SCARF project to the specific requirements of the ERNIE AI Developer Challenge.

---

## 🏆 Project Fit
SCARF targets the **"Model-Building"** and **"Application-Building"** tracks concurrently.
*   **Model Building**: We are building a "Scientific Reasoning Protocol" (fine-tuning prompt chains).
*   **Application**: We are building a "Scientific Critique System" for researchers.

## 🛠 Required Technologies (How we use them)

### 1. ERNIE 4.5/5 (The Brain)
*   **Usage**: We do NOT use ERNIE as a chat bot.
*   **Innovation**: We use ERNIE as a **Reasoning Engine** for specific sub-tasks:
    *   `Claim Extraction`
    *   `Evidence Linking`
    *   `Assumption Inference`
*   **Why ERNIE?**: Its large context window enables processing dense scientific sections without losing coherence.

### 2. PaddleOCR-VL (The Eyes)
*   **Usage**: Document Layout Analysis (PP-Structure).
*   **Innovation**: We use it to **ground** the reasoning. We don't just dump text; we know that "Text Block A" is inside "Section 3.2 (Results)". This prevents hallucination.

### 3. Novita AI (The Infrastructure)
*   **Usage**: API Gateway for ERNIE models.
*   **Integration**: Standard `requests` implementation in `backend/ernie_pipeline`.

---

## 🎯 Hackathon Goals (Checklist)

### 1. Warm-Up Task (Completed)
*   [x] Extract text with PaddleOCR.
*   [x] Generate web page (SCARF generates a Critique Report as a static site).

### 2. Main Submission
*   **Differentiation**: Most teams will build "Chat with PDF" or "Summarizers". SCARF builds **"Critique with Structure"**.
*   **Impact**: Directly useful for the academic/research community.
*   **Technical Depth**: We are not just wrapping an API; we are implementing a multi-step **Reasoning Pipeline**.

---

## 📅 Timeline
1.  **Phase 1**: Architecture & Docs (Done).
2.  **Phase 2**: Core Pipeline (Claims -> Evidence) (In Progress).
3.  **Phase 3**: UI & Report Generation.
4.  **Submission**: Demo Video + Repo.
