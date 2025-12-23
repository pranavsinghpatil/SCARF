
import os
import json
import logging
from ..schemas import Document, RhetoricalMap, SectionRole
from ..utils import repair_json
from jinja2 import Template

class RhetoricalSegmenter:
    """
    Module 1: Rhetorical Segmenter (OPTIMIZED)
    Classifies document sections using BATCHING (5 sections per API call).
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        prompt_path = os.path.join(os.path.dirname(__file__), '../../prompts/module_1_segmenter.txt')
        with open(prompt_path, 'r') as f:
            self.template = Template(f.read())
        self.progress_callback = None

    def run(self, doc: Document) -> RhetoricalMap:
        roles = []
        logging.info(f"Segmenting {len(doc.sections)} sections with batching")
        
        # BATCH: Process 5 sections at a time
        BATCH_SIZE = 5
        section_batches = [doc.sections[i:i+BATCH_SIZE] for i in range(0, len(doc.sections), BATCH_SIZE)]
        
        total_batches = len(section_batches)
        for batch_idx, batch in enumerate(section_batches):
            if self.progress_callback:
                sections_range = f"{batch_idx*BATCH_SIZE+1}-{min((batch_idx+1)*BATCH_SIZE, len(doc.sections))}"
                self.progress_callback(f"Classifying Sections {sections_range}/{len(doc.sections)}...")
            
            try:
                # Build prompt for batch
                prompt = self._build_batch_prompt(batch)
                
                # Expert system prompt for rhetorical classification
                system_prompt = ("You are a scientific document structure expert. "
                                "Classify sections accurately based on their rhetorical role in academic papers. "
                                "Be consistent and precise.")
                
                response_text = self.ernie.call(
                    prompt, 
                    system=system_prompt,
                    temperature=0.1  # Low temperature for consistency
                )
                clean_json = repair_json(response_text)
                
                # Parse response - should be array of role assignments
                data = json.loads(clean_json)
                
                if isinstance(data, list):
                    for item in data:
                        try:
                            # Normalize role before validation
                            if isinstance(item, dict) and 'role' in item:
                                role_str = item['role'].lower()
                                # Map invalid roles to valid ones
                                role_mapping = {
                                    'references': 'body',
                                    'reference': 'body',
                                    'bibliography': 'body',
                                    'acknowledgments': 'body',
                                    'acknowledgement': 'body',
                                    'appendix': 'body',
                                    'introduction': 'background',
                                    'conclusion': 'discussion',
                                    'conclusions': 'discussion'
                                }
                                if role_str in role_mapping:
                                    item['role'] = role_mapping[role_str]
                            
                            role = SectionRole.model_validate(item)
                            roles.append(role)
                        except Exception as e:
                            logging.warning(f"Invalid role assignment: {e}")
                            # Fallback: assign "body" role with high confidence
                            if isinstance(item, dict) and 'section_id' in item:
                                roles.append(SectionRole(
                                    section_id=item['section_id'],
                                    role="body",  # Safe fallback
                                    confidence=item.get('confidence', 0.9)  # Default confidence
                                ))
                else:
                    # Single object returned? Try to parse
                    try:
                        role = SectionRole.model_validate(data)
                        roles.append(role)
                    except:
                        logging.warning(f"Could not parse batch response, assigning 'body' to all")
                        for sec in batch:
                            roles.append(SectionRole(
                                section_id=sec.section_id,
                                role="body",
                                confidence=0.5  # Low confidence for fallback
                            ))
                        
            except Exception as e:
                logging.warning(f"Segmentation failed for batch {batch_idx}: {e}")
                # Fallback: assign "body" to all sections in this batch
                for sec in batch:
                    roles.append(SectionRole(
                        section_id=sec.section_id,
                        role="body",
                        confidence=0.3  # Very low confidence for error fallback
                    ))
        
        return RhetoricalMap(roles=roles)
    
    def _build_batch_prompt(self, sections):
        """Build prompt for multiple sections at once"""
        
        sections_text = ""
        for sec in sections:
            # Truncate to first 300 chars for efficiency
            content_preview = sec.content[:300] + "..." if len(sec.content) > 300 else sec.content
            sections_text += f"\n[SECTION_ID: {sec.section_id}]\nTitle: {sec.title}\nContent: {content_preview}\n"
        
        prompt = f"""You are SCARF. Classify the rhetorical role of each section below.

VALID ROLES:
- background: Literature review, related work, introduction
- method: Methodology, experimental setup
- results: Findings, data, tables
- discussion: Analysis, interpretation, conclusion
- limitations: Weaknesses, future work  
- body: General content (use as fallback for references, appendix, etc.)

NOTE: Use ONLY the roles listed above. Do not create new roles.

SECTIONS TO CLASSIFY:
{sections_text}

INSTRUCTIONS:
- Return a JSON array with one object per section
- Each object: {{"section_id": "...", "role": "...", "confidence": 0.0-1.0}}
- Use the EXACT section_id values provided above
- Use ONLY the 6 roles listed above (no "references", "introduction", etc.)
- confidence: How certain you are (0.9-1.0 = very certain, 0.5-0.8 = maybe)

IMPORTANT: Output ONLY valid JSON array. No markdown.

Example:
[
  {{"section_id": "S1", "role": "background", "confidence": 0.95}},
  {{"section_id": "S2", "role": "method", "confidence": 0.90}}
]
"""
        return prompt
