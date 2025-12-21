
import os
import json
import logging
from ..schemas import Document, RhetoricalMap, ClaimList, ScientificClaim
from ..utils import repair_json
from jinja2 import Template

class ClaimExtractor:
    """
    Module 2: Extracts scientific claims from relevant sections.
    Refined: Better role filtering and batch processing.
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        prompt_path = os.path.join(os.path.dirname(__file__), '../../prompts/module_2_claims.txt')
        with open(prompt_path, 'r') as f:
            self.template = Template(f.read())

    def run(self, doc: Document, rhetorical_map: RhetoricalMap) -> ClaimList:
        all_claims = []
        
        # Target only high-value sections for claims
        target_roles = ["method", "results", "discussion", "abstract"] # Abstract is distinct in some papers
        
        role_lookup = {r.section_id: r.role.lower() for r in rhetorical_map.roles}

        for section in doc.sections:
            role = role_lookup.get(section.section_id, "body")
            
            # Heuristic: If we treated pages as sections in Module 0, 'abstract' might be P1
            if role not in target_roles and section.section_id != "P1":
                continue

            schema_str = json.dumps(ClaimList.model_json_schema(), indent=2)
            
            prompt = self.template.render(
                section=section,
                schema=schema_str
            )

            try:
                # Add explicit system instruction for extraction
                response_text = self.ernie.call(prompt, system="Extract only explicit novel claims. Return empty list if none.")
                clean_json = repair_json(response_text)
                
                # Robust parsing
                data = json.loads(clean_json)
                
                # Check formatting (list vs object) based on what prompt usually returns
                # Prompt asks for ClaimList schema, so it should be {"claims": [...]}
                if "claims" in data:
                    claims_batch = ClaimList.model_validate(data)
                    # Tag claims with source section
                    for c in claims_batch.claims:
                        c.source_section_id = section.section_id
                    all_claims.extend(claims_batch.claims)
                    
            except Exception as e:
                logging.error(f"Module 2 Error on {section.section_id}: {e}")
                pass

        return ClaimList(claims=all_claims)
