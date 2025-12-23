
import os
import json
import logging
from ..schemas import Document, ClaimList, AssumptionLedger, ClaimAssumptions, Assumption
from ..utils import repair_json
from jinja2 import Template

class AssumptionMiner:
    """
    Module 4: Infers implicit assumptions.
    Refined: Context gathering and List parsing.
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        prompt_path = os.path.join(os.path.dirname(__file__), '../../prompts/module_4_assumptions.txt')
        with open(prompt_path, 'r') as f:
            self.template = Template(f.read())

    def run(self, doc: Document, claims: ClaimList) -> AssumptionLedger:
        ledger_entries = []
        logging.info("Starting Assumption Mining")
        
        # Context Strategy: Concat first 2 pages (Method/Intro usually here)
        # to give broad context for assumptions.
        context_sections = doc.sections[:2]
        context_text = "\n---\n".join([s.content for s in context_sections])
        
        # Truncate to safe length (approx 1000 words)
        if len(context_text) > 6000:
            context_text = context_text[:6000]
        
        total_c = len(claims.claims)
        for idx_c, claim in enumerate(claims.claims):
            if hasattr(self, 'progress_callback') and self.progress_callback:
                self.progress_callback(f"Mining Assumptions for Claim {idx_c+1}/{total_c}...")
            schema_str = json.dumps(Assumption.model_json_schema(), indent=2)
            
            prompt = self.template.render(
                claim=claim,
                context=context_text,
                schema=schema_str
            )

            try:
                response_text = self.ernie.call(
                    prompt,
                    system="Infer implicit scientific assumptions. Be critical.",
                    temperature=0.3  # Balanced for assumptions
                )
                clean_json = repair_json(response_text)
                
                data = json.loads(clean_json)
                
                # Check for "assumptions" key wrapper or direct list
                if isinstance(data, dict) and "assumptions" in data:
                    item_list = data["assumptions"]
                elif isinstance(data, list):
                    item_list = data
                else:
                    item_list = []
                    
                valid_assumptions = []
                for item in item_list:
                    try:
                        valid_assumptions.append(Assumption.model_validate(item))
                    except:
                        continue
                
                if valid_assumptions:
                    ledger_entries.append(ClaimAssumptions(claim_id=claim.claim_id, assumptions=valid_assumptions))
                    
            except Exception as e:
                logging.warning(f"Assumption mining failed for {claim.claim_id}: {e}")
                pass

        return AssumptionLedger(ledger=ledger_entries)
