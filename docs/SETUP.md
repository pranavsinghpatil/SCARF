# SCARF Setup Guide

This document explains how to set up the SCARF (Scientific Claim–Assumption–Rationale Framework) system locally.

Tone: **developer-friendly, practical, copy-paste ready.**

---

## ✅ Prerequisites

* **OS:** Linux / macOS / Windows
* **Python:** 3.10+ recommended
* **Git:** installed
* **Node.js (optional):** only if you later add a richer frontend
* **GitHub account:** for GitHub Pages deployment
* **Novita AI account:** for access to ERNIE models via API

---

## 1️⃣ Clone the Repository

```bash
# Clone your fork or main repo
git clone https://github.com/<your-username>/readify.git
cd readify
```

---

## 2️⃣ Create and Activate a Virtual Environment

```bash
# Create venv
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1
```

To deactivate later:

```bash
deactivate
```

---

## 3️⃣ Install Python Dependencies

> Note: exact dependencies will be maintained in `requirements.txt`.

Example `requirements.txt` (draft):

```txt
fastapi
uvicorn[standard]
python-multipart
jinja2
pydantic
requests
python-dotenv

# Paddle / OCR
paddlepaddle
paddleocr

# Utilities
numpy
Pillow
```

Install them:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> If PaddlePaddle fails to install, check their official install docs for platform-specific wheels.

---

## 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env  # if provided
# or create it manually
```

Inside `.env`, add:

```env
# Novita AI for ERNIE models
NOVITA_API_KEY="your_novita_api_key_here"
NOVITA_BASE_URL="https://api.novita.ai/v1"  # example placeholder

# GitHub deployment
GITHUB_TOKEN="your_github_personal_access_token"
GITHUB_USERNAME="your_github_username"
GITHUB_REPO_BASE="readify-sites"  # repo to host generated sites

# General
READIFY_ENV="development"
PORT=8000
```

> ⚠️ Never commit `.env` with real keys to Git.

---

## 5️⃣ Setting up Novita AI (ERNIE Integration)

1. Sign up / log in to **Novita AI**.
2. Create an API key from your dashboard.
3. Note the model name for ERNIE (e.g., `ernie-4.5` or similar hosted model).
4. Store your key in `.env` as `NOVITA_API_KEY`.

A minimal Python client snippet (to be used inside `ernie_pipeline/`):

```python
import os
import requests

NOVITA_API_KEY = os.getenv("NOVITA_API_KEY")
BASE_URL = os.getenv("NOVITA_BASE_URL", "https://api.novita.ai/v1")


def call_ernie(prompt: str, model: str = "ernie-4.5") -> str:
    headers = {
        "Authorization": f"Bearer {NOVITA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt},
        ],
    }
    resp = requests.post(f"{BASE_URL}/chat/completions", json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()
```

This function will be wrapped by higher-level helpers (e.g. `summarize_paper`, `generate_tldr`, etc.).

---

## 6️⃣ Setting up PaddleOCR-VL

SCARF uses **PaddleOCR / PaddleOCR-VL** for document layout-aware extraction.

Basic steps:

1. Install PaddlePaddle & PaddleOCR (already in `requirements.txt`).
2. Verify installation with a small OCR test.

Example minimal OCR snippet (to place inside `ocr_pipeline/` later):

```python
from paddleocr import PaddleOCR

def get_ocr_engine():
    # lang='en' for English; can extend later
    return PaddleOCR(use_angle_cls=True, lang='en')


def run_ocr_on_pdf(pdf_path: str):
    ocr = get_ocr_engine()
    # For multi-page PDF, first convert pages to images (e.g. using pdf2image)
    # Then run ocr. This is a simplified placeholder.
    # TODO: Replace with VL/document-layout specific pipeline.
    result = ocr.ocr(pdf_path, cls=True)
    return result
```

Later, this will be replaced or enhanced by PaddleOCR-VL’s **layout-aware** models.

---

## 7️⃣ Running the FastAPI Backend

Entry point (planned): `backend/api/main.py`.

Run locally:

```bash
uvicorn backend.api.main:app --reload --port 8000
```

After starting, open:

* **API docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Redoc docs:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

These will show available endpoints:

* `POST /upload` – upload a PDF
* `GET /status/{job_id}` – processing status (optional)
* `GET /result/{job_id}` – link to generated site or ZIP download

---

## 8️⃣ Frontend Setup (Basic Version)

Initially, SCARF can use:

* A simple HTML form (in `frontend/templates/index.html`)
* Served directly by FastAPI using Jinja2

Example route (to be implemented later):

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

---

## 9️⃣ GitHub Pages Deployment (High-Level)

Requirements:

* A GitHub repo (e.g., `readify-sites`)
* Personal Access Token with `repo` permissions

SCARF will:

* Generate a static site folder for each paper
* Commit & push it under a specific branch (`gh-pages` or `main` depending on your setup)
* Construct the final URL in the format:

  * `https://<username>.github.io/<site-folder>/`

Deployment logic will live in `backend/deploy/` and use the `GITHUB_TOKEN` from `.env`.

---

## 🔍 Verifying Your Setup

You’re good if:

* `uvicorn` starts without errors
* `/docs` endpoint loads in the browser
* A dummy OCR test runs without crashing
* A sample `call_ernie()` request returns a response

---

## 🧯 Troubleshooting (Common Issues)

* **PaddlePaddle install fails**

  * Check Python + CUDA compatibility
  * Try CPU-only wheel if GPU is not needed for the hackathon

* **Novita API 401/403**

  * Double-check `NOVITA_API_KEY`
  * Make sure the header uses `Bearer <key>`

* **CORS issues when adding a frontend later**

  * Enable CORS in FastAPI using `fastapi.middleware.cors.CORSMiddleware`.

---

You are now ready to start wiring the **PDF → OCR → Reasoning → Critique** pipeline. 🚀
