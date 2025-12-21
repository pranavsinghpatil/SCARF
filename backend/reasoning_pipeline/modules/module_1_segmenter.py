
import os
import json
import logging
from ..schemas import Document, RhetoricalMap, SectionRole
from ..utils import repair_json
from jinja2 import Template

class RhetoricalSegmenter:
    """
    Module 1: Classifies the rhetorical role of each section.
    Uses ERNIE via a prompt template.
    Refined: Added robust parsed response handling.
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        # Load prompt template from file
        prompt_path = os.path.join(os.path.dirname(__file__), '../../prompts/module_1_segmenter.txt')
        with open(prompt_path, 'r') as f:
            self.template = Template(f.read())
        
        self.valid_roles = ["background", "method", "results", "discussion", "limitations", "body"]

    def run(self, doc: Document) -> RhetoricalMap:
        roles = []
        logging.info(f"Starting Rhetorical Segmentation for {doc.doc_id}")
        
        for section in doc.sections:
            # Skip empty sections
            if not section.content.strip():
                continue
                
            # Prepare Schema for injection
            schema_str = json.dumps(SectionRole.model_json_schema(), indent=2)
            
            # Truncate content to avoid token overflow in classification (only need beginning/end often)
            # content_snippet = section.content[:1000] + "\n...\n" + section.content[-500:] 
            # Use full content for now, assume ERNIE 4.5 32k window
            
            prompt = self.template.render(
                section=section,
                schema=schema_str
            )
            
            try:
                response_text = self.ernie.call(prompt, system="You are a scientific research assistant.")
                clean_json = repair_json(response_text)
                role_obj = SectionRole.model_validate_json(clean_json)
                
                # Normalize role
                if role_obj.role.lower() not in self.valid_roles:
                   role_obj.role = "body"
                   
                # Enforce ID consistency
                role_obj.section_id = section.section_id
                
                roles.append(role_obj)
            except Exception as e:
                logging.error(f"Module 1 Error on {section.section_id}: {e}")
                # Fallback
                roles.append(SectionRole(section_id=section.section_id, role="body", confidence=0.0))
                
        return RhetoricalMap(roles=roles)
