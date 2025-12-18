# Prompt Management Strategy

**Why This Matters**
Prompts are code. They should not be hardcoded strings inside Python functions.
They need versioning, variable interpolation, and separation of concerns.

## 🛠 Jinja2 for Prompts
We use **Jinja2** (the same template engine for HTML) to manage our AI Prompts.

### Directory Structure
```
backend/
  reasoning_pipeline/
    prompts/
      system_persona.txt
      module_1_segmenter.txt
      module_2_claims.txt
      module_3_evidence.txt
```

### Example Template (`module_2_claims.txt`)
```text
You are analyzing the section: "{{ section_title }}"

Extract primary claims from the following text.
Strictly adhere to this JSON Schema:
{{ schema_json }}

Text Content:
{{ section_content }}
```

## 🚀 Benefits
1.  **Readability**: Prompts are edited in plain text files, not Python string concatenation.
2.  **Dynamic Context**: We can inject large variables (Schemas, Text Chunks) cleanly.
3.  **A/B Testing**: We can easily swap `module_2_claims_v1.txt` with `module_2_claims_v2.txt` to test performance.

## 📦 Implementation
We will build a simple `PromptLoader` class:
```python
class PromptLoader:
    def render(self, template_name, **kwargs):
        # loads template, fills variables, returns string
```
