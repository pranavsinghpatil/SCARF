
import os
import json
from ..schemas import Document, ClaimList, AssumptionLedger, ClaimAssumptions, Assumption
from ..utils import repair_json
from jinja2 import Template

class AssumptionMiner:
    """
    Module 4: Infers implicit assumptions.
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        with open(os.path.join(os.path.dirname(__file__), '../../prompts/module_4_assumptions.txt'), 'r') as f:
            self.template = Template(f.read())

    def run(self, doc: Document, claims: ClaimList) -> AssumptionLedger:
        ledger_entries = []
        
        # Concat Method + Evaluation sections for context
        # In v1, we just take the whole doc text (careful with token limits!)
        # or just the first 3 sections.
        context_text = "\n".join([s.content for s in doc.sections[:3]])
        
        for claim in claims.claims:
            schema_str = json.dumps(Assumption.model_json_schema(), indent=2)
            
            prompt = self.template.render(
                claim=claim,
                context=context_text,
                schema=schema_str
            )

            try:
                response_text = self.ernie.call(prompt)
                clean_json = repair_json(response_text)
                
                # Prompt usually returns list of Assumptions
                # We need to wrap it into ClaimAssumptions
                # Let's assume prompt returns [Assumption, Assumption]
                
                # Manual hack for list parsing since Pydantic validates single object usually
                data = json.loads(clean_json)
                assumptions_list = [Assumption(**item) for item in data]
                
                ledger_entries.append(ClaimAssumptions(claim_id=claim.claim_id, assumptions=assumptions_list))
            except Exception as e:
                pass

        return AssumptionLedger(ledger=ledger_entries)
