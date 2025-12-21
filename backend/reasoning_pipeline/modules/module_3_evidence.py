
import os
import json
import logging
from ..schemas import Document, ClaimList, EvidenceGraph, ClaimEvidencePair, EvidenceLink
from ..utils import repair_json
from jinja2 import Template

class EvidenceLinker:
    """
    Module 3: Links Claims to Evidence in Results/Experiments sections.
    Refined: Robust JSON parsing and fallback.
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        prompt_path = os.path.join(os.path.dirname(__file__), '../../prompts/module_3_evidence.txt')
        with open(prompt_path, 'r') as f:
            self.template = Template(f.read())

    def run(self, doc: Document, claims: ClaimList) -> EvidenceGraph:
        links = []
        logging.info(f"Starting Evidence Linking for {len(claims.claims)} claims")

        # Optimization: In a real system we'd check only relevant sections.
        # For valid demo, we check sections labeled 'results' or just all if small doc.
        # Let's check first 5 non-empty sections to be safe.
        target_sections = [s for s in doc.sections if len(s.content) > 50][:5]

        for claim in claims.claims:
            evidence_for_claim = []
            
            for section in target_sections:
                schema_str = json.dumps(EvidenceLink.model_json_schema(), indent=2)
                
                prompt = self.template.render(
                    claim=claim,
                    section=section,
                    schema=schema_str
                )

                try:
                    # System instruction to be strict
                    response_text = self.ernie.call(prompt, system="You are a strict evidence verifier. Return 'none' if no direct proof exists.")
                    clean_json = repair_json(response_text)
                    
                    # Robust Parsing
                    if "none" in clean_json.lower() and len(clean_json) < 20:
                        continue
                        
                    data = json.loads(clean_json)
                    
                    # Handle if LLM returns a list or single object
                    if isinstance(data, list):
                        items = data
                    else:
                        items = [data]
                        
                    for item in items:
                        # Skip if TYPE is NONE (sometimes model returns object with type='none')
                        if item.get("type", "").lower() == "none":
                            continue
                            
                        # Validate
                        ev_obj = EvidenceLink.model_validate(item)
                        # Enforce section_id correctness
                        ev_obj.section_id = section.section_id
                        evidence_for_claim.append(ev_obj)

                except Exception as e:
                    # logging.warning(f"Evidence check failed for C:{claim.claim_id} S:{section.section_id}: {e}")
                    pass
            
            if evidence_for_claim:
                links.append(ClaimEvidencePair(claim_id=claim.claim_id, evidence=evidence_for_claim))

        return EvidenceGraph(links=links)
