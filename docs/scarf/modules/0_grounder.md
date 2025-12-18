# Module 0: Document Grounder

**Status**: v1 (Full Implementation)
**Role**: The Foundation.

## 🎯 Responsibility
Convert a raw PDF into a **grounded, addressable document representation**.
This module is the single source of truth for all downstream reasoning. If it's not in Module 0's output, it doesn't exist.

## ⚙️ Inputs & Outputs

*   **Input**: Raw PDF File.
*   **Output**: `Document` JSON object.
    ```json
    {
      "pages": [
        {
          "page_num": 1,
          "image_path": "visuals/page_1.jpg",
          "sections": ["S1", "S2"]
        }
      ],
      "sections": [
        {
          "section_id": "S1",
          "title": "1. Introduction",
          "content": "Deep learning models...",
          "bbox": [x1, y1, x2, y2],
          "page_num": 1
        }
      ]
    }
    ```

## 🧠 Logic (No AI Reasoning)
This module uses **OCR** and **Layout Parsing**, not LLMs.
1.  **PDF -> Images**: Using `pdf2image`.
2.  **Layout Parsing**: Using `PaddleOCR-VL` (PP-Structure).
    *   Detect Header/Footer (filter out).
    *   Detect Text Blocks.
    *   Detect Tables/Figures.
3.  **Sectioning**: Heuristic grouping of blocks based on font size and numbering (e.g., "1. Introduction" vs body text).

## 🔒 Constraints
*   **Full Coverage**: Every character in the PDF must be mapped.
*   **Immutability**: Once generated, the `Document` object is read-only.
