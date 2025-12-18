# SCARF Tech Stack Handbook

Welcome to the technical deep-dive of SCARF. This folder contains detailed documentation for every core technology used in the project.

These guides are written to be **practical, advanced, and specific to SCARF**. They go beyond "Hello World" to explain *why* we use these tools and *how* they solve our specific problems (PDF parsing, AI enrichment, static site generation).

## 📚 Documentation Index

### Core Language & Backend
*   **[Python (python.md)](./python.md)**: Advanced Python patterns, type hinting, and performance optimization.
*   **[FastAPI (fastapi.md)](./fastapi.md)**: Building high-performance async APIs.
*   **[Async Architecture (architecture-async.md)](./architecture-async.md)**: How we handle long-running OCR jobs via polling.
*   **[Pydantic Contracts (pydantic-schemas.md)](./pydantic-schemas.md)**: Enforcing strict JSON schemas on LLM outputs.
*   **[Error Strategy (error-strategies.md)](./error-strategies.md)**: Resilience against hallucinations and OCR failures.
*   **[Requests (requests.md)](./requests.md)**: Robust HTTP client usage for external APIs.
*   **[Dotenv (dotenv.md)](./dotenv.md)**: Security best practices.

### OCR & Document Understanding
*   **[PaddleOCR (paddleocr.md)](./paddleocr.md)**: The engine behind text extraction. How it works and how we tune it.
*   **[PaddleOCR-VL (paddleocr-vl.md)](./paddleocr-vl.md)**: Layout-aware document understanding. Preserving tables, headers, and structure.
*   **[PDF2Image (pdf2image.md)](./pdf2image.md)**: The critical pre-processing step converting PDFs to high-res images for OCR.

### AI & Intelligence
*   **[ERNIE API (ernie-api.md)](./ernie-api.md)**: Integrating Baidu's ERNIE model.
*   **[Prompt Management (prompt-management.md)](./prompt-management.md)**: Using Jinja2 to version and manage prompt templates.

### Frontend & Static Site Generation
*   **[Frontend Integration (frontend-integration.md)](./frontend-integration.md)**: Visualizing the Critique Report.
*   **[Jinja2 (jinja2.md)](./jinja2.md)**: Used for prompt templates and static site generation.
*   **[CSS (css.md)](./css.md)**: Styling strategy.
*   **[JavaScript (javascript.md)](./javascript.md)**: Interactivity.

### Deployment
*   **[GitHub Pages (github-pages.md)](./github-pages.md)**: Automating the publishing of generated sites directly to the web.

---

## 🧭 How to use this handbook

1.  **New to the project?** Start with `python.md` and `fastapi.md` to understand the codebase foundation.
2.  **Working on the core pipeline?** Read `pdf2image.md` -> `paddleocr.md` -> `paddleocr-vl.md`.
3.  **Improving the output?** Focus on `jinja2.md`, `css.md`, and `javascript.md`.
4.  **Debugging AI?** Check `ernie-api.md`.

*This documentation is a living part of the project. Update it as you learn new tricks or change architectural decisions.*
