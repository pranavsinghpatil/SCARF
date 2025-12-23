# Mock Ernie Client for Testing
# Use this when Novita API is down or too slow

import logging
import json

class MockErnieClient:
    """
    Mock AI client that returns plausible responses WITHOUT calling the API.
    Use for testing when network/API is unavailable.
    """
    
    def __init__(self):
        self.model = "mock-ernie"
        self.call_count = 0
        logging.info("[MOCK] Using MockErnieClient - NO actual API calls")
    
    def call(self, prompt: str, system: str = None, temperature: float = 0.3) -> str:
        """Return mock responses based on prompt content"""
        self.call_count += 1
        logging.info(f"[MOCK] Call #{self.call_count} (temp={temperature}, system='{system[:50] if system else 'None'}')")
        
        # Detect which module is calling based on system prompt
        if "classify" in prompt.lower() or "rhetorical" in prompt.lower():
            # Module 1: Segmentation
            return self._mock_segmentation(prompt)
        
        elif "claim" in prompt.lower():
            # Module 2: Claims
            return self._mock_claims(prompt)
        
        elif "evidence" in prompt.lower():
            # Module 3: Evidence
            return self._mock_evidence(prompt)
        
        elif "assumption" in prompt.lower():
            # Module 4: Assumptions
            return self._mock_assumptions(prompt)
        
        elif "gap" in prompt.lower():
            # Module 5: Gaps
            return self._mock_gaps(prompt)
        
        elif "question" in prompt.lower():
            # Module 6: Questions
            return self._mock_questions(prompt)
        
        else:
            logging.warning(f"[MOCK] Unknown prompt type, returning empty array")
            return "[]"
    
    def _mock_segmentation(self, prompt: str) -> str:
        """Mock response for Module 1"""
        # Extract section IDs from prompt
        import re
        section_ids = re.findall(r'SECTION_ID:\s*(\S+)', prompt)
        
        roles = []
        for sid in section_ids:
            # Simple heuristic
            if "intro" in sid.lower() or sid == "S1":
                role = "background"
            elif "method" in sid.lower() or sid == "S2":
                role = "method"
            elif "result" in sid.lower() or sid == "S3":
                role = "results"
            elif "discuss" in sid.lower() or sid == "S4":
                role = "discussion"
            else:
                role = "body"
            
            roles.append({
                "section_id": sid,
                "role": role,
                "confidence": 0.85
            })
        
        return json.dumps(roles)
    
    def _mock_claims(self, prompt: str) -> str:
        """Mock response for Module 2"""
        # Extract section ID
        import re
        match = re.search(r'SECTION ID:\s*(\S+)', prompt)
        section_id = match.group(1) if match else "S1"
        
        # Return 2-3 mock claims
        claims = {
            "claims": [
                {
                    "claim_id": f"C{self.call_count}",
                    "statement": "The proposed model achieves 95% accuracy on the test dataset",
                    "source_section_id": section_id,
                    "confidence": 0.90
                },
                {
                    "claim_id": f"C{self.call_count + 100}",
                    "statement": "Our approach outperforms baseline methods by 15%",
                    "source_section_id": section_id,
                    "confidence": 0.85
                }
            ]
        }
        return json.dumps(claims)
    
    def _mock_evidence(self, prompt: str) -> str:
        """Mock response for Module 3"""
        evidence = [
            {
                "section_id": "S3",
                "type": "quantitative",
                "snippet": "Table 1 shows accuracy of 95.2% on benchmark dataset",
                "notes": "Primary experimental result"
            },
            {
                "section_id": "S2",
                "type": "qualitative",
                "snippet": "The methodology ensures robust evaluation",
                "notes": "Supporting context"
            }
        ]
        return json.dumps(evidence)
    
    def _mock_assumptions(self, prompt: str) -> str:
        """Mock response for Module 4"""
        assumptions = {
            "assumptions": [
                {
                    "type": "data",
                    "statement": "Test data is representative of real-world scenarios",
                    "confidence": 0.7
                },
                {
                    "type": "model",
                    "statement": "Architecture generalizes beyond training distribution",
                    "confidence": 0.6
                }
            ]
        }
        return json.dumps(assumptions)
    
    def _mock_gaps(self, prompt: str) -> str:
        """Mock response for Module 5"""
        gaps = [
            {"signal": "No comparison with recent state-of-the-art methods"},
            {"signal": "Limited discussion of failure cases"}
        ]
        return json.dumps(gaps)
    
    def _mock_questions(self, prompt: str) -> str:
        """Mock response for Module 6"""
        questions = [
            {"question": "How does the model perform on out-of-distribution data?"},
            {"question": "What are the computational requirements for deployment?"}
        ]
        return json.dumps(questions)
