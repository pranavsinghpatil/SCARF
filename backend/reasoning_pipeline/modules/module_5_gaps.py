
import os
import json
from ..schemas import EvidenceGraph, AssumptionLedger, GapAnalysis, ClaimGaps, GapSignal
from ..utils import repair_json
from jinja2 import Template

class GapAnalyzer:
    """
    Module 5: Analyzes Claims vs Evidence vs Assumptions to find gaps.
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        with open(os.path.join(os.path.dirname(__file__), '../../prompts/module_5_gaps.txt'), 'r') as f:
            self.template = Template(f.read())

    def run(self, claims, evidence: EvidenceGraph, assumptions: AssumptionLedger) -> GapAnalysis:
        analysis_entries = []
        
        # We process per-Claim.
        # We need to look up Evidence and Assumptions for each Claim ID.
        ev_lookup = {link.claim_id: link.evidence for link in evidence.links}
        ass_lookup = {entry.claim_id: entry.assumptions for entry in assumptions.ledger}
        
        for claim in claims.claims:
            ev_list = ev_lookup.get(claim.claim_id, [])
            ass_list = ass_lookup.get(claim.claim_id, [])
            
            # Prepare summary strings for the prompt
            ev_summary = "\n".join([f"- {e.type}: {e.snippet}" for e in ev_list]) or "No evidence found."
            ass_summary = "\n".join([f"- {a.type}: {a.statement}" for a in ass_list]) or "No assumptions inferred."
            
            schema_str = json.dumps(GapSignal.model_json_schema(), indent=2)
            
            prompt = self.template.render(
                claim=claim,
                evidence_summary=ev_summary,
                assumptions_summary=ass_summary,
                schema=schema_str
            )

            try:
                response_text = self.ernie.call(prompt)
                clean_json = repair_json(response_text)
                
                # Expecting list of strings or objects? 
                # Prompt says "Return JSON adhering to schema".
                # Let's assume the LLM returns a list of GapSignal objects directly or strings.
                # If prompt returns pure strings, we wrap them.
                
                # For v1 robustness:
                data = json.loads(clean_json)
                signals = []
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, str):
                            signals.append(GapSignal(signal=item))
                        elif isinstance(item, dict):
                            signals.append(GapSignal(**item))
                            
                analysis_entries.append(ClaimGaps(claim_id=claim.claim_id, signals=signals))
            except Exception as e:
                pass

        return GapAnalysis(analysis=analysis_entries)
