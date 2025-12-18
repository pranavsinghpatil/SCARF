
import os
import json
from ..schemas import Document, RhetoricalMap, SectionRole
from ..utils import repair_json
from jinja2 import Template

class RhetoricalSegmenter:
    """
    Module 1: Classifies the rhetorical role of each section.
    Uses ERNIE via a prompt template.
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        # Load prompt template from file
        with open(os.path.join(os.path.dirname(__file__), '../../prompts/module_1_segmenter.txt'), 'r') as f:
            self.template = Template(f.read())

    def run(self, doc: Document) -> RhetoricalMap:
        roles = []
        for section in doc.sections:
            # Prepare Schema for injection
            schema_str = json.dumps(SectionRole.model_json_schema(), indent=2)
            
            # Render Prompt
            prompt = self.template.render(
                section=section,
                schema=schema_str
            )
            
            # Call AI
            try:
                response_text = self.ernie.call(prompt)
                clean_json = repair_json(response_text)
                role_obj = SectionRole.model_validate_json(clean_json)
                roles.append(role_obj)
            except Exception as e:
                # Fallback: Assume Body if AI fails
                print(f"Module 1 Error on {section.section_id}: {e}")
                pass
                
        return RhetoricalMap(roles=roles)
