# SCARF Documentation

This directory contains the core research and design documents for the **Scientific Claim–Assumption–Rationale Framework**.

## 📂 Structure

### 📜 [Manifesto](MANIFESTO.md)
The core philosophy, research statement, and high-level vision. "We do not judge truth; we judge alignment."

### ⚙️ [Modules](modules/)
Detailed specifications for the 6-step reasoning pipeline.
*   **Module 0**: Grounding (PDF -> Text)
*   **Module 1**: Segmentation (Text -> Roles)
*   **Module 2**: Claim Extraction (Text -> Claims)
*   **Module 3**: Evidence Linking (Claims -> Evidence)
*   **Module 4**: Assumption Mining (Logic -> Assumptions)
*   **Module 5/6**: Critique & Validation (Graph -> Signals)

### 📏 [Evaluation](evaluation/)
Strategy for validating the system without ground-truth labels.
*   **Strategy**: Precision, Coverage, Plausibility tests.

---

> This folder is the "Brain" of the project. The `tech/` folder is the "Body".
