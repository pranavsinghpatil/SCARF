
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
        prompt_path = os.path.join(os.path.dirname(__file__), '../../prompts/module_2_extractor.txt')
        with open(prompt_path, 'r') as f:
            self.template = Template(f.read())

    def run(self, doc: Document, rhetorical_map: RhetoricalMap) -> ClaimList:
        all_claims = []
        
        # Build role lookup with proper enum value access
        role_lookup = {r.section_id: r.role.value for r in rhetorical_map.roles}
        
        logging.info(f"Extracting claims from {len(doc.sections)} sections")

        total = len(doc.sections)
        for idx, section in enumerate(doc.sections):
            if hasattr(self, 'progress_callback') and self.progress_callback:
                self.progress_callback(f"Extracting Claims from Section {idx+1}/{total}...")
                
            role = role_lookup.get(section.section_id, "body")
            
            # Skip only clearly irrelevant sections
            skip_roles = ["limitations"]  # Very restrictive - almost all sections are checked
            if role in skip_roles:
                logging.info(f"Skipping section {section.section_id} (role: {role})")
                continue

            schema_str = json.dumps(ClaimList.model_json_schema(), indent=2)
            
            prompt = self.template.render(
                section=section,
                schema=schema_str
            )

            try:
                # Expert system prompt for claims extraction
                system_prompt = ("You are a scientific claims extraction expert. "
                                "Extract ONLY falsifiable, testable claims from scientific papers. "
                                "Ignore background statements and citations. Be precise and evidence-focused.")
                
                response_text = self.ernie.call(
                    prompt,
                    system=system_prompt,
                    temperature=0.2  # Low temperature for precision
                )
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

        logging.info(f"Module 2 complete: Extracted {len(all_claims)} total claims from {len(doc.sections)} sections")
        return ClaimList(claims=all_claims)
