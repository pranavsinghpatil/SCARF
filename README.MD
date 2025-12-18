# SCARF: Scientific Claim–Assumption–Rationale Framework

> **A framework for structured reasoning over scientific documents.**

---

## 🔬 The Mission
**SCARF** investigates whether automated systems can assist peer review by structurally decomposing scientific papers.
It is **not** a "Chat with PDF" tool. It is a **Decomposition Engine**.

## 🔴 The Problem
Manual peer review is slow, inconsistent, and biased. Even experts struggle to critically read papers outside their niche because:
*   Claims are not explicitly labeled.
*   Evidence is distributed across sections.
*   Assumptions are often unstated.

## ✅ The Solution
SCARF decomposes a paper into four interpretable artifacts:

1.  **Claim–Evidence Table**: Mapping declarative statements to their supporting data.
2.  **Assumption Ledger**: Surfacing implicit dependencies (Data, Model, Evaluation).
3.  **Gap Signals**: Identifying unsupported claims or missing validations.
4.  **Validation Questions**: Suggesting questions that would test the paper's rigor.

---

## 🛠 Tech Stack
*   **Perception**: `PaddleOCR-VL` (PP-Structure) for layout-aware parsing.
*   **Reasoning**: `ERNIE 4.5/5` (via Novita AI) for logic extraction.
*   **Orchestration**: Python / FastAPI.

---

## 📂 Documentation

*   [**The SCARF Manifesto**](docs/scarf/MANIFESTO.md) (Read this first)
*   [**System Workflow**](docs/WORKFLOW.md)
*   [**Tech Handbook**](docs/tech/README.md)

---

> *SCARF does not judge "Truth". It judges "Consistency".*
