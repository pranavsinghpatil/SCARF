# ERNIE API Integration in SCARF

**Role**: The Reasoning Engine.
SCARF uses **ERNIE 4.5/5** (via Novita AI) not to "chat", but to perform specific **cognitive tasks** within our pipeline.

## 🔌 API Strategy: Constrained Generation

For SCARF, we do not want creative essays. We want **JSON** or **Structured Text**.
We enforce this via the system prompt:

```python
SYSTEM_PROMPT = """
You are SCARF, a scientific reasoning engine.
Your goal is to extract structural logic from text.
You do not judge correctness. You check alignment.
Return output in strictly valid JSON format.
"""
```

### Basic Call Structure (Synchronous)

```python
import requests
import os

def call_ernie_json(prompt: str, schema: dict):
    """
    Calls ERNIE and enforces JSON output via prompting strategies.
    """
    url = "https://api.novita.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('NOVITA_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    # We inject the schema into the prompt to guide the model
    full_prompt = f"{prompt}\n\nReturn JSON adhering to: {schema}"
    
    data = {
        "model": "ernie-4.5",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.1, # Low temperature for deterministic logic
        "response_format": {"type": "json_object"} # If supported, or simulated via prompt
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()['choices'][0]['message']['content']
```

## 🧠 Decomposition Prompts (The "New" Prompt Engineering)

We replaced "Summarize" with "Decompose".

### 1. Claim Extraction Prompt
```text
Extract primary scientific claims from the text below.
A claim is a declarative statement asserting novelty, effectiveness, or generalization.
Rules:
- Ignore background info.
- Normalize to atomic statements.
- Return JSON: [{"claim": "...", "confidence": 0.9}]
```

### 2. Evidence Linking Prompt
```text
Given Claim C and Section S:
Does Section S provide specific evidence for Claim C?
If yes, classify type: [Quantitative, Qualitative, Theoretical].
Rule: Do not hallucinate. If no evidence, return "None".
```

## 🛡 Robustness
1.  **JSON Validation**: We parse the output with `Pydantic`. If it fails, we retry (up to 3 times).
2.  **Context Management**: We process per-section, not the whole paper at once, to stay well within the context window.
