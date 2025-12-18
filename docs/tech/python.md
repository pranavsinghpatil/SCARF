# Python in SCARF

**Why Python?**
Python is the undisputed king of AI and Data Science. For SCARF, it is the glue that binds OCR (PaddlePaddle), LLMs (API calls), and Web Serving (FastAPI) together.

## 🚀 Advanced Techniques Used

### 1. Type Hinting & Pydantic
We don't just write Python; we write **typed** Python. This prevents runtime errors and enables auto-documentation.

```python
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class PaperMetadata(BaseModel):
    title: str
    authors: List[str]
    url: Optional[HttpUrl] = None
    page_count: int
```

**Why?**
*   **Validation**: `PaperMetadata(page_count="ten")` will fail instantly, saving us from weird bugs later.
*   **IDE Support**: VS Code knows exactly what fields exist.

### 2. Asynchronous Programming (`async`/`await`)
SCARF is I/O bound. We wait for:
*   OCR to finish (CPU/GPU bound, but often offloaded)
*   ERNIE API to respond (Network bound)
*   File writes

Blocking code kills performance. We use `async` everywhere possible.

```python
import asyncio

async def process_paper(pdf_path: str):
    # Run OCR and AI in parallel if possible
    ocr_task = asyncio.create_task(run_ocr(pdf_path))
    ai_task = asyncio.create_task(prepare_prompts(pdf_path))
    
    await ocr_task
    await ai_task
```

### 3. Generators for Large Files
PDFs can be huge. We never load everything into RAM if we can avoid it.

```python
def read_large_file(file_path):
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            yield chunk
```

### 4. Decorators for Retry Logic
APIs fail. Network glitches happen. We use decorators to handle this cleanly.

```python
import time
from functools import wraps

def retry(max_retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    time.sleep(delay)
            raise Exception("Max retries exceeded")
        return wrapper
    return decorator

@retry()
def call_ernie_api(prompt):
    # ...
```

### 5. Pathlib for File Management
Strings are for text, not paths. We use `pathlib`.

```python
from pathlib import Path

BASE_DIR = Path(__file__).parent
PDF_DIR = BASE_DIR / "uploads" / "pdfs"
PDF_DIR.mkdir(parents=True, exist_ok=True)
```

## 🧠 DSA & Problem Solving in SCARF

*   **Tree Traversal**: A research paper is a tree (Title -> Sections -> Subsections -> Paragraphs). We parse this hierarchy to generate the Table of Contents.
*   **String Matching**: Fuzzy matching is used to link citations `[1]` to the bibliography.
*   **Queueing**: When multiple users upload files, we use a background task queue (via `FastAPI BackgroundTasks` or Celery) to process them without freezing the server.

## 🛠 Best Practices
1.  **Docstrings**: Every function must have a docstring explaining inputs and outputs.
2.  **Black Formatter**: We use `black` to enforce code style. No arguments about formatting.
3.  **Virtual Environments**: Never install global packages. Always use `.venv`.
