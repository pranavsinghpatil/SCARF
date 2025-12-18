
from .modules.module_0_grounder import DocumentGrounder
from .modules.module_1_segmenter import RhetoricalSegmenter
from .modules.module_2_extractor import ClaimExtractor
from .modules.module_3_evidence import EvidenceLinker
from .modules.module_4_assumptions import AssumptionMiner
from .modules.module_5_gaps import GapAnalyzer
from .modules.module_6_validation import ValidationSynthesizer
from .schemas import Document

class SCARFPipeline:
    def __init__(self, ernie_client):
        self.grounder = DocumentGrounder()
        self.segmenter = RhetoricalSegmenter(ernie_client)
        self.extractor = ClaimExtractor(ernie_client)
        self.linker = EvidenceLinker(ernie_client)
        self.miner = AssumptionMiner(ernie_client)
        self.analyzer = GapAnalyzer(ernie_client)
        self.synthesizer = ValidationSynthesizer(ernie_client)
        
    def run(self, pdf_path: str, job_id: str):
        # 1. Grounding
        doc = self.grounder.run(pdf_path, job_id)
        
        # 2. Segmentation
        rhetoric = self.segmenter.run(doc)
        
        # 3. Claims
        claims = self.extractor.run(doc, rhetoric)
        
        # 4. Evidence
        evidence = self.linker.run(doc, claims)
        
        # 5. Assumptions
        assumptions = self.miner.run(doc, claims)
        
        # 6. Gaps
        gaps = self.analyzer.run(claims, evidence, assumptions)
        
        # 7. Validation
        validation = self.synthesizer.run(gaps)
        
        return {
            "doc": doc.dict(),
            "rhetoric": rhetoric.dict(),
            "claims": claims.dict(),
            "evidence": evidence.dict(),
            "assumptions": assumptions.dict(),
            "gaps": gaps.dict(),
            "validation": validation.dict()
        }
