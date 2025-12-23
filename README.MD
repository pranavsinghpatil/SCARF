# SCARF 🧣: Scientific Claim-Assumption-Rationale Framework

**Deconstruct Scientific Logic with AI.**

SCARF is an advanced reasoning engine that ingests scientific PDF documents and decomposes them into a rigorous logical graph. Isolate claims, surface hidden assumptions, and identify evidence gaps.

![SCARF UI Mockup](https://via.placeholder.com/800x400?text=SCARF+Dashboard)

## 🚀 Quick Start

### Prerequisites
*   **Python 3.9+**
*   **Node.js 18+**
*   **Novita AI API Key** (for ERNIE 4.0/4.5)

### 1. Setup
Runs backend setup, dependency checks, and starts both servers.
```bash
click launch.bat
# OR
./launch.bat
```

### 2. Manual Installation
**Backend**:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.api.main:app --reload
```

**Frontend**:
```bash
cd NewFrontend
npm install
npm run dev
```

---

## 🏗 Architecture

SCARF follows a modular **Chain-of-Reasoning** pipeline:

### 1. Perception Layer (Module 0)
*   **Grounder**: Converts raw PDF into addressable `Section` objects.
*   **Tech**: PaddleOCR (Layout Analysis) + PyMuPDF (Text Extraction).

### 2. Semantic Layer (Modules 1-2)
*   **Segmenter**: Classifies sections by rhetorical role (Method, Results, etc.).
*   **Extractor**: Normalizes text into atomic `ScientificClaim` objects.

### 3. Reasoning Layer (Modules 3-6)
*   **Evidence Linker**: Scans the document to find proof for every claim.
*   **Assumption Miner**: Infers implicit dependencies (e.g., "Assumes data linearity").
*   **Gap Analyzer**: Synthesizes conflicting signals (Claims without Evidence).
*   **Validation Synthesizer**: Generates specific research questions to test the gaps.

---

## 🛠 Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **LLM** | **ERNIE 4.0** (via Novita AI) | Core Reasoning Engine |
| **Backend** | **FastAPI** (Python) | API & Pipeline Orchestrator |
| **Vision** | **PaddleOCR** | Document Layout Analysis |
| **Frontend** | **React + Vite** | Interactive Dashboard |
| **Styling** | **Tailwind CSS** | UI Design System |

---

## 📁 Project Structure

```
SCARF/
├── backend/
│   ├── api/            # FastAPI Endpoints
│   ├── reasoning_pipeline/
│   │   ├── modules/    # Individual logic units (0-6)
│   │   └── pipeline.py # Orchestrator
│   └── ernie_pipeline/ # LLM Client
├── NewFrontend/        # React Application
├── docs/               # Technical Documentation
└── requirements.txt    # Python Dependencies
```

## 🤝 Contributing
Built for the **PaddlePaddle Hackathon**.
Team: Antigravity

License: MIT
