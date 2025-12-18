# SCARF Documentation Index

**Scientific Claim–Assumption–Rationale Framework**

## 📚 Core Research Documents
*   [**Manifesto**](scarf/MANIFESTO.md): The core research statement and vision. "We do not judge truth; we judge alignment."
*   [**System Workflow**](WORKFLOW.md): The high-level data flow.
*   [**Evaluation Strategy**](scarf/evaluation/strategy.md): How we measure success without "truth" labels.

## ⚙️ System Modules (The Reasoning Pipeline)
The SCARF pipeline is composed of 6 isolated modules:
1.  [**Module 0: Document Grounder**](scarf/modules/0_grounder.md) (The Foundation)
2.  [**Module 1: Rhetorical Segmenter**](scarf/modules/1_segmenter.md) (The Map)
3.  [**Module 2: Claim Extractor**](scarf/modules/2_extractor.md) (The Miner)
4.  [**Module 3: Evidence Linker**](scarf/modules/3_evidence.md) (The Forensic)
5.  [**Module 4: Assumption Miner**](scarf/modules/4_assumptions.md) (The Deep Reader)
6.  [**Module 5 & 6: Gap Analyzer & Validation**](scarf/modules/5_gaps.md) (The Critique)

## 🛠 Technical Implementation
*   [**Architecture**](ARCHITECTURE.md): System-level diagram and stack.
*   [**Schemas**](../backend/reasoning_pipeline/schemas.py): Pydantic models defining the data contract.
*   [**Tech Stack Handbook**](tech/README.md): Detailed guides on Python, FastAPI, PaddleOCR, etc.

## 🚀 Guides
*   [**Setup Guide**](SETUP.md): Installation and local dev setup.
*   [**Hackathon Context**](HACKATHON.md): Original challenge requirements.
