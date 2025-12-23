
import os
import json
import logging
from ..schemas import Document, ClaimList, EvidenceGraph, ClaimEvidencePair, EvidenceLink
from ..utils import repair_json
from jinja2 import Template

class EvidenceLinker:
    """
    Module 3: Evidence Linker (OPTIMIZED)
    Links claims to supporting evidence using SMART BATCHING.
    Instead of claim×section API calls, does ONE call per claim with ALL relevant sections.
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        prompt_path = os.path.join(os.path.dirname(__file__), '../../prompts/module_3_evidence.txt')
        with open(prompt_path, 'r') as f:
            self.template = Template(f.read())
        self.progress_callback = None

    def run(self, doc: Document, claims: ClaimList) -> EvidenceGraph:
        links = []
        logging.info(f"Linking evidence for {len(claims.claims)} claims")
        
        # Filter to only relevant sections (skip references, acknowledgments)
        relevant_sections = [
            s for s in doc.sections 
            if not any(keyword in s.title.lower() for keyword in ['reference', 'acknowledgment', 'bibliography'])
        ]
        
        total = len(claims.claims)
        for idx, claim in enumerate(claims.claims):
            if self.progress_callback:
                self.progress_callback(f"Linking Evidence for Claim {idx+1}/{total}...")
            
            try:
                # BATCH: Send ALL relevant sections in ONE API call
                prompt = self._build_batch_prompt(claim, relevant_sections)
                
                # Expert system prompt for evidence linking
                system_prompt = ("You are an evidence evaluation specialist. "
                                "Link scientific claims to supporting evidence with precision. "
                                "Extract exact citations and classify evidence type accurately.")
                
                response_text = self.ernie.call(
                    prompt,
                    system=system_prompt,
                    temperature=0.2  # Low-medium temperature for accuracy
                )
                clean_json = repair_json(response_text)
                
                # Parse response - should be a list of evidence objects
                data = json.loads(clean_json)
                
                evidence_list = []
                if isinstance(data, list):
                    for item in data:
                        try:
                            # Validate and add
                            ev = EvidenceLink.model_validate(item)
                            evidence_list.append(ev)
                        except Exception as e:
                            logging.warning(f"Invalid evidence item: {e}")
                            # Try to salvage partial data
                            if isinstance(item, dict) and 'snippet' in item:
                                evidence_list.append(EvidenceLink(
                                    section_id=item.get('section_id', 'UNKNOWN'),
                                    type=item.get('type', 'qualitative'),
                                    snippet=item['snippet']
                                ))
                
                if evidence_list:
                    links.append(ClaimEvidencePair(claim_id=claim.claim_id, evidence=evidence_list))
                else:
                    logging.warning(f"No evidence found for claim {claim.claim_id}")
                    
            except Exception as e:
                logging.warning(f"Evidence linking failed for {claim.claim_id}: {e}")
                pass
        
        return EvidenceGraph(links=links)
    
    def _build_batch_prompt(self, claim, sections):
        """Build a prompt that includes ALL sections at once"""
        
        # Create a compact representation of all sections
        sections_text = ""
        for sec in sections:
            # Truncate each section to 500 chars to keep prompt manageable
            content_preview = sec.content[:500] + "..." if len(sec.content) > 500 else sec.content
            sections_text += f"\n[SECTION: {sec.title} | ID: {sec.section_id}]\n{content_preview}\n"
        
        prompt = f"""You are SCARF. Find evidence for the following claim in the provided document sections.

CLAIM:
{claim.statement}

DOCUMENT SECTIONS:
{sections_text}

INSTRUCTIONS:
- Search ALL sections above for evidence supporting or refuting the claim
- Return a JSON array of evidence objects
- Each evidence object must have:
  - section_id: The ID of the section (e.g., "S1", "S2")
  - type: "quantitative", "qualitative", or "theoretical"
  - snippet: The exact text snippet (1-2 sentences)
- If no evidence found, return empty array: []

IMPORTANT: Output ONLY valid JSON array. No markdown, no explanation.

Example output:
[
  {{"section_id": "S3", "type": "quantitative", "snippet": "Table 1 shows accuracy of 95%"}},
  {{"section_id": "S5", "type": "qualitative", "snippet": "The results demonstrate effectiveness"}}
]
"""
        return prompt
