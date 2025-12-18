# PaddleOCR in SCARF

**Why PaddleOCR?**
PaddleOCR (by Baidu) is currently one of the best open-source OCR tools, especially for:
1.  **Multilingual support** (80+ languages).
2.  **Lightweight models** (PP-OCR series) that run fast even on CPU.
3.  **Layout Analysis** (critical for research papers).

## 🔍 How it Works

PaddleOCR isn't just one model; it's a pipeline of three:
1.  **Text Detection (DBNet)**: Finds *where* the text is (bounding boxes).
2.  **Text Direction Classifier**: Checks if text is rotated (0°, 90°, 180°).
3.  **Text Recognition (CRNN)**: Reads the actual characters in the box.

## 🛠 Implementation in SCARF

We use the `paddleocr` Python package.

```python
from paddleocr import PaddleOCR

# Initialize once (it loads models into memory)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Run on an image path
result = ocr.ocr(img_path, cls=True)
```

### The Output Format
The output is a list of lists:
```python
[
  [
    [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],  # Bounding Box
    ('Text Content', 0.98)                     # Text and Confidence
  ],
  ...
]
```

## 🧩 Challenges & Solutions

### 1. Two-Column Layouts
Research papers often have two columns. Standard OCR reads left-to-right across the whole page, mixing up columns.
**Solution**: We use **Layout Analysis** (PaddleOCR-VL) or simple coordinate sorting.
*   Sort boxes by Y-coordinate first (lines).
*   If a box is on the left half (X < width/2), it belongs to Column 1.
*   If on the right, Column 2.

### 2. Math Equations
Standard OCR fails at complex math ($E=mc^2$).
**Solution**: We detect equations as "images" or "regions" and pass them to a specialized multimodal model (ERNIE-VL) to transcribe into LaTeX.

### 3. Performance
OCR is slow.
*   **Optimization**: Resize images to a standard width (e.g., 2000px) before processing. Too large = slow; too small = inaccurate.
*   **Batching**: Process pages in parallel if GPU is available.

## 🚀 Next Level: PP-Structure
For SCARF, we specifically look into **PP-Structure**, a module of PaddleOCR designed for:
*   Table Recognition (rebuilding Excel/CSV from image tables).
*   Layout Recovery (identifying Header, Footer, Figure, Text).

*See `paddleocr-vl.md` for more on this.*
