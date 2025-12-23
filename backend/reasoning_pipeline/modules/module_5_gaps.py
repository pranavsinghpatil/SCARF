
import os
import json
import logging
from ..schemas import EvidenceGraph, AssumptionLedger, GapAnalysis, ClaimGaps, GapSignal
from ..utils import repair_json
from jinja2 import Template

class GapAnalyzer:
    """
    Module 5: Analyzes Claims vs Evidence vs Assumptions to find gaps.
    Refined: Full Implementation.
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        prompt_path = os.path.join(os.path.dirname(__file__), '../../prompts/module_5_gaps.txt')
        with open(prompt_path, 'r') as f:
            self.template = Template(f.read())

    def run(self, claims, evidence: EvidenceGraph, assumptions: AssumptionLedger) -> GapAnalysis:
        analysis_entries = []
        logging.info("Starting Gap Analysis")
        
        # Lookups
        ev_lookup = {link.claim_id: link.evidence for link in evidence.links}
        ass_lookup = {entry.claim_id: entry.assumptions for entry in assumptions.ledger}
        
        total_c = len(claims.claims)
        for idx, claim in enumerate(claims.claims):
            if hasattr(self, 'progress_callback') and self.progress_callback:
                self.progress_callback(f"Analyzing Gaps for Claim {idx+1}/{total_c}...")
            
            ev_list = ev_lookup.get(claim.claim_id, [])
            ass_list = ass_lookup.get(claim.claim_id, [])
            
            # Prepare summary strings for the prompt
            ev_summary = "\n".join([f"- {e.type} (Section {e.section_id}): {e.snippet}" for e in ev_list]) or "No evidence found."
            ass_summary = "\n".join([f"- {a.type}: {a.statement}" for a in ass_list]) or "No explicit assumptions identified."
            
            schema_str = json.dumps(GapSignal.model_json_schema(), indent=2)
            
            prompt = self.template.render(
                claim=claim,
                evidence_summary=ev_summary,
                assumptions_summary=ass_summary,
                schema=schema_str
            )

            try:
                response_text = self.ernie.call(
                    prompt,
                    system="Identify logical gaps. Be objective.",
                    temperature=0.4  # Higher for insightful analysis
                )
                clean_json = repair_json(response_text)
                
                data = json.loads(clean_json)
                
                # Logic to handle List[GapSignal] or List[str]
                signals = []
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, str):
                            signals.append(GapSignal(signal=item))
                        elif isinstance(item, dict):
                            # Try validation
                            try:
                                signals.append(GapSignal.model_validate(item))
                            except:
                                # Fallback if specific field missing, map first string field
                                if item.values():
                                    signals.append(GapSignal(signal=str(list(item.values())[0])))
                
                if signals:            
                    analysis_entries.append(ClaimGaps(claim_id=claim.claim_id, signals=signals))
            except Exception as e:
                logging.warning(f"Gap Analysis failed for {claim.claim_id}: {e}")
                pass

        return GapAnalysis(analysis=analysis_entries)
