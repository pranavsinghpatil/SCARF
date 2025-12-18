# PaddleOCR-VL & Layout Analysis

**The Problem**: Standard OCR gives you a stream of text. It doesn't tell you "this is a title," "this is a table," or "this is a caption."
**The Solution**: **PaddleOCR-VL** (Vision-Language) and **PP-Structure**.

## 🏗 What is Layout Analysis?

It's the process of segmenting a document image into regions:
*   Text
*   Title
*   Figure
*   Figure Caption
*   Table
*   Header/Footer
*   Reference

For SCARF, this is **critical**. We don't just want to dump text; we want to recreate the *structure* of the paper.

## 🛠 How we use PP-Structure

PP-Structure is a pipeline within PaddleOCR that uses object detection (usually PicoDet or YOLO-based) to find these regions.

```python
from paddleocr import PPStructure

# Initialize layout engine
table_engine = PPStructure(show_log=True, image_orientation=True)

# Run on image
result = table_engine(img_path)
```

### The Result Object
The result is a list of regions. Each region has:
*   `type`: "text", "title", "table", "figure"
*   `bbox`: [x1, y1, x2, y2]
*   `res`: The content (OCR text or HTML for tables)

## 📊 Table Recognition (The Magic Part)

One of the hardest parts of OCR is tables. PP-Structure detects a table, then uses a separate model (TableMaster or SLANet) to:
1.  Detect rows and columns.
2.  Recognize text in each cell.
3.  **Output HTML**: It actually gives us `<table><tr><td>...` code!

**In SCARF:**
We take this HTML and inject it directly into our Jinja2 templates. This means tables in the PDF become responsive HTML tables on the website.

## 🧠 Vision-Language Models (ERNIE-Layout / LayoutXLM)

For even smarter understanding, we can use **ERNIE-Layout**.
*   **Input**: Image + OCR Text + Bounding Boxes.
*   **Task**: "Key Information Extraction" (KIE).
*   **Example**: Finding the "Authors" or "Affiliations" specifically, even if they aren't labeled explicitly.

We use this to extract metadata (Title, Author, Date) accurately from the first page.

## 🚀 Implementation Strategy for SCARF

1.  **Page 1**: Run KIE (Key Information Extraction) to get metadata.
2.  **All Pages**: Run Layout Analysis to split into blocks.
3.  **Filtering**: Remove Headers/Footers (noise).
4.  **Ordering**: Sort blocks by column (XY-cut algorithm).
5.  **Reconstruction**: Stitch text blocks into Markdown sections.
