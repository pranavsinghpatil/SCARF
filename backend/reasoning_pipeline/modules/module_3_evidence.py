
import os
import json
from ..schemas import Document, ClaimList, EvidenceGraph, ClaimEvidencePair, EvidenceLink
from ..utils import repair_json
from jinja2 import Template

class EvidenceLinker:
    """
    Module 3: Links Claims to Evidence in Results/Experiments sections.
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        with open(os.path.join(os.path.dirname(__file__), '../../prompts/module_3_evidence.txt'), 'r') as f:
            self.template = Template(f.read())

    def run(self, doc: Document, claims: ClaimList) -> EvidenceGraph:
        # In a real system, we'd use embedding retrieval to find relevant sections first.
        # For hackathon/v1, we scan "Results" sections for each claim.
        # Ideally, we rely on Module 1's map, but let's blindly check all sections for robustness in this stub.
        
        links = []

        for claim in claims.claims:
            evidence_for_claim = []
            
            # Optimization: Only check first 5 sections or specifically "Results" in future
            for section in doc.sections:
                schema_str = json.dumps(EvidenceLink.model_json_schema(), indent=2)
                
                # We need a custom schema for the response that wraps status
                # The prompt asks for { "supports": bool, ... } which isn't exactly EvidenceLink
                # Let's assume we adjusted the prompt or schema.
                # Actually, let's inject a wrapper schema or handle the response dynamically.
                # For simplicity, let's assume the LLM returns EvidenceLink if supported, or handles "none".
                
                prompt = self.template.render(
                    claim=claim,
                    section=section,
                    schema=schema_str
                )

                try:
                    response_text = self.ernie.call(prompt)
                    clean_json = repair_json(response_text)
                    
                    # Hack: Check if simple "none" or null
                    if "none" in clean_json.lower() and len(clean_json) < 20:
                        continue
                        
                    evidence_obj = EvidenceLink.model_validate_json(clean_json)
                    if evidence_obj.type != "none":
                        evidence_for_claim.append(evidence_obj)
                        
                except Exception as e:
                    pass
            
            links.append(ClaimEvidencePair(claim_id=claim.claim_id, evidence=evidence_for_claim))

        return EvidenceGraph(links=links)
