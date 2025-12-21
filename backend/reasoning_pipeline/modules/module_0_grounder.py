
import os
import fitz  # PyMuPDF
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR
from ..schemas import Document, Section
import logging

# Initialize PaddleOCR once (it loads heavy models)
# We use English and structure analysis
try:
    OCR_ENGINE = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
except Exception as e:
    logging.warning(f"PaddleOCR failed to load: {e}. Module 0 will allow purely text-based extraction fallback.")
    OCR_ENGINE = None

class DocumentGrounder:
    """
    Module 0: Converts a specific PDF file into a Grounded Document object.
    Uses PaddleOCR for layout analysis AND text extraction.
    """
    def __init__(self):
        self.ocr = OCR_ENGINE

    def run(self, pdf_path: str, job_id: str) -> Document:
        """
        Extracts content from PDF.
        Strategy:
        1. Render PDF pages to images.
        2. Run PaddleOCR on each page to get text blocks.
        3. (Simplification for v1) Group blocks into 'Sections' based on heuristics or just pages.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at {pdf_path}")

        extracted_sections = []
        
        # Open PDF
        doc_pdf = fitz.open(pdf_path)
        
        for page_num, page in enumerate(doc_pdf):
            # 1. Render page to image for OCR
            pix = page.get_pixmap(dpi=300)
            img_data = pix.tobytes("png")
            
            # Convert bytes to numpy array for Paddle
            # Or save to temp file (safer for Paddle)
            temp_img_path = f"{pdf_path}_p{page_num}.png"
            with open(temp_img_path, "wb") as f:
                f.write(img_data)
            
            try:
                # 2. Run OCR
                # result = [[[[x1,y1],[x2,y2]..], "text", confidence], ...]
                if self.ocr:
                    result = self.ocr.ocr(temp_img_path, cls=True)
                else:
                    # Fallback if Paddle failed to load: use PyMuPDF text
                    text = page.get_text()
                    # Fake structure matching Paddle: List of [Msg] where Msg is [Coords, (Text, Conf)]
                    # Coords=None, Text=text, Conf=1.0
                    result = [[ [None, (text, 1.0)] ]]

                # 3. Process Result
                # In v1, we treat each Page as a "Section" if we can't detect headers easily
                # Improved: Concatenate all text on page
                
                page_text_lines = []
                if result and result[0]:
                    for line in result[0]:
                        # Handle potential None result from Paddle
                        if line:
                            text_content = line[1][0]
                            page_text_lines.append(text_content)
                
                full_page_text = "\n".join(page_text_lines)
                
                # Basic Sectioning: Just create a section per page for now
                # In Step 2 (Segmenter), the LLM will assign roles to these chunks.
                section_id = f"P{page_num+1}"
                extracted_sections.append(
                    Section(
                        section_id=section_id,
                        title=f"Page {page_num+1}",
                        page_range=[page_num+1],
                        content=full_page_text
                    )
                )

            finally:
                # Cleanup temp image
                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)

        doc_pdf.close()

        return Document(
            doc_id=job_id,
            sections=extracted_sections
        )
