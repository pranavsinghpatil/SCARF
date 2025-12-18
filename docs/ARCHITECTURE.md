# SCARF System Architecture

**Status**: v1 Design

## 🏗 High-Level Diagram

```mermaid
graph TD
    User[User Upload PDF] --> API[FastAPI Backend]
    API --> M0[Module 0: Grounder]
    
    subgraph "Reasoning Pipeline (Sequential)"
        M0 -->|Document| M1[Module 1: Segmenter]
        M1 -->|Rhetorical Map| M2[Module 2: Claim Extractor]
        M2 -->|Claims| M3[Module 3: Evidence Linker]
        M1 -->|Sections| M3
        M2 -->|Claims| M4[Module 4: Assumption Miner]
        M3 -->|Evidence Graph| M5[Module 5: Gap Analyzer]
        M4 -->|Assumptions| M5
        M5 -->|Signals| M6[Module 6: Validation Questions]
    end
    
    M6 -->|Report| API
    API --> Frontend[Web UI (Critique View)]
```

## 🧩 Component Breakdown

### 1. Document Grounder (Perception Layer)
*   **Tech**: `pdf2image`, `PaddleOCR-VL` (PP-Structure).
*   **Role**: Non-AI parsing.
*   **Data**: `backend.reasoning_pipeline.schemas.Document`.

### 2. The Reasoning Engine (Intelligence Layer)
*   **Tech**: `ERNIE 4.5/5` (via Novita AI).
*   **Role**: Stateless transformation of text -> structured insights.
*   **Orchestration**: Python `modules/` (to be implemented).
*   **Data**: `ClimateEvidenceTable`, `AssumptionLedger`.

### 3. The API (Service Layer)
*   **Tech**: `FastAPI`, `Uvicorn`.
*   **Endpoints**:
    *   `POST /analyze`: Triggers the pipeline (Async Background Task).
    *   `GET /analyze/{job_id}`: Polls status.
    *   `GET /report/{job_id}`: Returns final JSON artifact.

## 💾 Data Persistence
*   **v1**: In-memory / Filesystem (`output/{job_id}/*.json`).
*   **No Database** required for v1 prototype.

## 🛡 Security & Config
*   **Env Vars**: `NOVITA_API_KEY` (managed by `python-dotenv`).
*   **GitIgnore**: All `output/` and `.env` files.
