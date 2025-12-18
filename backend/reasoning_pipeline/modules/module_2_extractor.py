
import os
import json
from ..schemas import Document, RhetoricalMap, ClaimList, ScientificClaim
from ..utils import repair_json
from jinja2 import Template

class ClaimExtractor:
    """
    Module 2: Extracts scientific claims from relevant sections.
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        with open(os.path.join(os.path.dirname(__file__), '../../prompts/module_2_claims.txt'), 'r') as f:
            self.template = Template(f.read())

    def run(self, doc: Document, rhetorical_map: RhetoricalMap) -> ClaimList:
        all_claims = []
        
        # Identify relevant sections (ignore Background/Limitations for extraction?)
        # For now, let's extract from Method, Results, Discussion
        target_roles = ["method", "results", "discussion"]
        
        # Create a lookup for quick access
        role_lookup = {r.section_id: r.role for r in rhetorical_map.roles}

        for section in doc.sections:
            role = role_lookup.get(section.section_id, "body")
            if role not in target_roles:
                continue

            schema_str = json.dumps(ClaimList.model_json_schema(), indent=2)
            
            prompt = self.template.render(
                section=section,
                schema=schema_str
            )

            try:
                response_text = self.ernie.call(prompt)
                clean_json = repair_json(response_text)
                # The prompt returns a ClaimList object
                claims_batch = ClaimList.model_validate_json(clean_json)
                all_claims.extend(claims_batch.claims)
            except Exception as e:
                print(f"Module 2 Error on {section.section_id}: {e}")
                pass

        return ClaimList(claims=all_claims)
