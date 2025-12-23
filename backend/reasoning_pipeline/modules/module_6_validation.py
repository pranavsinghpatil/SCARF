
import os
import json
import logging
from ..schemas import GapAnalysis, ValidationReport, ClaimValidation, ValidationQuestion
from ..utils import repair_json
from jinja2 import Template

class ValidationSynthesizer:
    """
    Module 6: Generates validation questions based on gaps.
    Refined: Full Implementation.
    """
    def __init__(self, ernie_client):
        self.ernie = ernie_client
        prompt_path = os.path.join(os.path.dirname(__file__), '../../prompts/module_6_validation.txt')
        with open(prompt_path, 'r') as f:
            self.template = Template(f.read())

    def run(self, gap_analysis: GapAnalysis) -> ValidationReport:
        report_entries = []
        logging.info("Starting Validation Synthesis")
        
        total = len(gap_analysis.analysis)
        for idx, gap_entry in enumerate(gap_analysis.analysis):
            if hasattr(self, 'progress_callback') and self.progress_callback:
                self.progress_callback(f"Generating Questions for Claim {idx+1}/{total}...")

            if not gap_entry.signals:
                continue
                
            gaps_list = [g.signal for g in gap_entry.signals]
            schema_str = json.dumps(ValidationQuestion.model_json_schema(), indent=2)
            
            prompt = self.template.render(
                gaps_list=gaps_list,
                schema=schema_str
            )

            try:
                response_text = self.ernie.call(
                    prompt,
                    system="Generate constructive research questions.",
                    temperature=0.5  # Higher for creative questions
                )
                clean_json = repair_json(response_text)
                
                data = json.loads(clean_json)
                
                questions = []
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, str):
                            questions.append(ValidationQuestion(question=item))
                        elif isinstance(item, dict):
                            try:
                                questions.append(ValidationQuestion.model_validate(item))
                            except:
                                if item.values():
                                    questions.append(ValidationQuestion(question=str(list(item.values())[0])))
                            
                if questions:
                    report_entries.append(ClaimValidation(claim_id=gap_entry.claim_id, questions=questions))
            except Exception as e:
                logging.warning(f"Validation gen failed for {gap_entry.claim_id}: {e}")
                pass

        return ValidationReport(report=report_entries)
