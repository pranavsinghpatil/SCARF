from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum

# --- Module 0: Document Grounder ---
class Section(BaseModel):
    section_id: str = Field(..., description="Unique ID for the section (S1, S2, etc.)")
    title: str = Field(..., description="Section title found in the text")
    page_range: List[int] = Field(..., description="Pages where this section appears")
    content: str = Field(..., description="Full text content of the section")

class Document(BaseModel):
    doc_id: str
    sections: List[Section]

# --- Module 1: Rhetorical Segmenter ---
class RhetoricalRole(str, Enum):
    BACKGROUND = "background"
    METHOD = "method"
    RESULTS = "results"
    DISCUSSION = "discussion"
    LIMITATIONS = "limitations"
    BODY = "body"  # Fallback

class SectionRole(BaseModel):
    section_id: str
    role: RhetoricalRole
    confidence: float = Field(..., ge=0.0, le=1.0)

class RhetoricalMap(BaseModel):
    roles: List[SectionRole]

# --- Module 2: Claim Extractor ---
class ScientificClaim(BaseModel):
    claim_id: str = Field(..., description="Unique ID (C1, C2...)")
    statement: str = Field(..., description="Normalized declarative statement")
    source_section_id: str = Field(..., description="Where the claim was found")
    confidence: float = Field(..., ge=0.0, le=1.0)
    
class ClaimList(BaseModel):
    claims: List[ScientificClaim]

# --- Module 3: Evidence Linker ---
class EvidenceType(str, Enum):
    QUANTITATIVE = "quantitative"
    QUALITATIVE = "qualitative"
    THEORETICAL = "theoretical"
    NONE = "none"

class EvidenceLink(BaseModel):
    section_id: str = Field(..., description="Section containing the evidence")
    type: EvidenceType
    snippet: str = Field(..., description="Specific text or figure reference")
    notes: Optional[str] = Field(None, description="Contextual notes")

class ClaimEvidencePair(BaseModel):
    claim_id: str
    evidence: List[EvidenceLink]

class EvidenceGraph(BaseModel):
    links: List[ClaimEvidencePair]

# --- Module 4: Assumption Miner ---
class AssumptionType(str, Enum):
    DATA = "data"
    MODEL = "model"
    EVALUATION = "evaluation"

class Assumption(BaseModel):
    type: AssumptionType
    statement: str
    confidence: float

class ClaimAssumptions(BaseModel):
    claim_id: str
    assumptions: List[Assumption]

class AssumptionLedger(BaseModel):
    ledger: List[ClaimAssumptions]

# --- Module 5: Gap Analyzer ---
class GapSignal(BaseModel):
    signal: str = Field(..., description="Non-judgmental critique signal")

class ClaimGaps(BaseModel):
    claim_id: str
    signals: List[GapSignal]

class GapAnalysis(BaseModel):
    analysis: List[ClaimGaps]

# --- Module 6: Validation Synthesizer ---
class ValidationQuestion(BaseModel):
    question: str

class ClaimValidation(BaseModel):
    claim_id: str
    questions: List[ValidationQuestion]

class ValidationReport(BaseModel):
    report: List[ClaimValidation]
