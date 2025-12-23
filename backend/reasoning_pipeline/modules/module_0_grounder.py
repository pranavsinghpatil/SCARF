
import os
import fitz  # PyMuPDF
import logging
import re
from ..schemas import Document, Section

class DocumentGrounder:
    """
    Module 0: Smart Document Grounding
    Extracts text and intelligently detects sections using heuristics.
    NO OCR - just fast PyMuPDF text extraction.
    """
    def __init__(self):
        # Common section headers in scientific papers
        self.section_keywords = [
            r'\babstract\b',
            r'\bintroduction\b',
            r'\bbackground\b',
            r'\brelated\s+work\b',
            r'\bmethods?\b',
            r'\bmethodology\b',
            r'\bexperiments?\b',
            r'\bresults?\b',
            r'\bdiscussion\b',
            r'\bconclusion\b',
            r'\breferences?\b',
            r'\backnowledgments?\b'
        ]

    def run(self, pdf_path: str, job_id: str) -> Document:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at {pdf_path}")

        doc_pdf = fitz.open(pdf_path)
        
        # Extract all text with page info
        full_text = ""
        page_breaks = []
        
        for page_num, page in enumerate(doc_pdf):
            page_text = page.get_text()
            page_breaks.append(len(full_text))
            full_text += page_text + "\n\n"
        
        doc_pdf.close()
        
        # Detect sections using heuristics
        sections = self._detect_sections(full_text, page_breaks)
        
        # Fallback: if no sections detected, create one big section
        if not sections:
            logging.warning("No sections detected, using full document as single section")
            sections = [Section(
                section_id="FULL",
                title="Full Document",
                page_range=[1, len(page_breaks)],
                content=full_text
            )]
        
        logging.info(f"Detected {len(sections)} sections: {[s.title for s in sections]}")
        
        return Document(doc_id=job_id, sections=sections)

    def _detect_sections(self, text: str, page_breaks: list) -> list:
        """
        Detect sections using line-based heuristics:
        - Short lines (< 50 chars) are potential headers
        - Match against section keywords
        - Track positions and split text
        """
        lines = text.split('\n')
        section_markers = []
        
        current_pos = 0
        for line in lines:
            line_stripped = line.strip()
            
            # Check if line is a potential section header
            if len(line_stripped) > 3 and len(line_stripped) < 100:
                # Check for numbering (e.g., "1. Introduction", "2.1 Methods")
                if re.match(r'^[\d\.\s]+[A-Z]', line):
                    section_markers.append((current_pos, line_stripped))
                else:
                    # Check for keyword match
                    for keyword_pattern in self.section_keywords:
                        if re.search(keyword_pattern, line_stripped, re.IGNORECASE):
                            section_markers.append((current_pos, line_stripped))
                            break
            
            current_pos += len(line) + 1  # +1 for newline
        
        # If we found markers, split text
        if section_markers:
            sections = []
            for idx, (pos, title) in enumerate(section_markers):
                # Determine end position
                end_pos = section_markers[idx + 1][0] if idx + 1 < len(section_markers) else len(text)
                
                # Extract content
                content = text[pos:end_pos].strip()
                
                # Determine page range
                start_page = self._get_page_num(pos, page_breaks)
                end_page = self._get_page_num(end_pos, page_breaks)
                
                # Clean title (remove numbering)
                clean_title = re.sub(r'^[\d\.\s]+', '', title).strip()
                
                sections.append(Section(
                    section_id=f"S{idx+1}",
                    title=clean_title,
                    page_range=list(range(start_page, end_page + 1)),
                    content=content[:6000]  # Limit to 6000 chars per section
                ))
            
            return sections
        
        return []

    def _get_page_num(self, char_pos: int, page_breaks: list) -> int:
        """Convert character position to page number"""
        for idx, break_pos in enumerate(page_breaks):
            if char_pos < break_pos:
                return max(1, idx)
        return len(page_breaks)
