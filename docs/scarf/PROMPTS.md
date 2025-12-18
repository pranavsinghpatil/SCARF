# SCARF Prompt Engineering Strategy

**"Low temperature. No creativity. Surgical precision."**

This document maps the SCARF Reasoning Pipeline modules to specific ERNIE Prompts.

## 🎨 Design Principles
1.  **System Prompt**: Always enforce the SCARF persona.
2.  **JSON Enforcement**: Always request JSON output with a specific schema.
3.  **Ambiguity Handling**: Instruct the model to return "None" or empty lists instead of hallucinating.

---

## 🤖 System Prompt
```text
You are SCARF, a scientific reasoning engine.
Your goal is to extract structural logic from text.
You do not judge correctness. You check alignment.
Return output in strictly valid JSON format.
```

---

## 🧱 Module 1: Rhetorical Segmenter

**Goal**: Classify section roles.

**Prompt**:
```text
You are given a section of a scientific paper.
Classify its rhetorical role as one of:
[Background, Method, Results, Discussion, Limitations].

Return JSON:
{
  "role": "...",
  "confidence": 0-1
}

Section text:
{SECTION_TEXT}
```

---

## 🔍 Module 2: Claim Extractor

**Goal**: Identify atomic claims.

**Prompt**:
```text
Extract primary scientific claims from the text below.
A claim is a declarative statement asserting novelty, effectiveness, generalization, or superiority.

Rules:
- Do not extract background statements.
- Rewrite each claim concisely.
- Return JSON only.

Output format:
[
  {
    "claim_id": "C_N",
    "statement": "...",
    "confidence": 0-1
  }
]

Text:
{METHOD + RESULTS + DISCUSSION}
```

---

## 🔗 Module 3: Evidence Linker

**Goal**: Verify existence of proof.

**Prompt**:
```text
Given a claim and a paper section, identify whether this section provides evidence supporting the claim.

If yes, describe the evidence type [Quantitative, Qualitative, Theoretical].

Return JSON:
{
  "supports": true/false,
  "evidence_type": "...",
  "snippet": "...",
  "notes": "..."
}

Claim:
{CLAIM_STATEMENT}

Section:
{RESULTS_SECTION_TEXT}
```

---

## 🧠 Module 4: Assumption Miner

**Goal**: Surface implicit dependencies.

**Prompt**:
```text
Identify implicit assumptions required for the claim to hold, based only on the provided method and evaluation.

Rules:
- If unsure, return an empty list.
- Each assumption must be plausible and grounded.

Return JSON:
[
  {
    "type": "data|evaluation",
    "statement": "...",
    "confidence": 0-1
  }
]
```

---

## ⚠️ Module 5: Gap Analyzer

**Goal**: Generate signals, not verdicts.

**Prompt**:
```text
Given a claim and its linked evidence, identify potential gaps that may warrant further scrutiny.

Rules:
- Do not judge correctness.
- Phrase as signals, not conclusions.

Return JSON:
[
  "Evidence is limited to...",
  "No ablation study for..."
]
```

---

## ❓ Module 6: Validation Questions

**Goal**: Suggest next steps.

**Prompt**:
```text
Based on the identified gaps, generate up to 2 validation questions that could increase confidence in the claim.

Return a list of questions only.
```
