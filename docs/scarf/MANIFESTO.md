# SCARF: Scientific Claim–Assumption–Rationale Framework (v1)

> **Goal**: To build a framework that acts as a lens for structured reasoning over scientific documents, producing interpretable artifacts that support human critical judgment.

---

## 1. The Core Research Statement
Modern scientific literature is evaluated through manual peer review, requiring experts to identify claims, verify supporting evidence, infer assumptions, and assess methodological gaps. This process **does not scale** and is prone to **inconsistency**.

**The Hypothesis**:
We investigate whether large language models, combined with doc-understanding pipelines, can assist this process by **structurally decomposing** scientific papers into **claims, evidence, assumptions, and gaps**, producing interpretable artifacts that support human critical judgment.

**Note**: SCARF is not an app. It is an infrastructure for scientific reasoning.

---

## 2. The Solution (SCARF v1)
We define SCARF as a **Reasoning Assembly Line** composed of 6 distinct, testable modules.

### The Reasoning Pipeline
1.  **[Module 0: Document Grounder](modules/0_grounder.md)** - Ground truth extraction.
2.  **[Module 1: Rhetorical Segmenter](modules/1_segmenter.md)** - Functional role assignment.
3.  **[Module 2: Claim Extractor](modules/2_extractor.md)** - Claim identification.
4.  **[Module 3: Evidence Linker](modules/3_evidence.md)** - Claim-Evidence alignment.
5.  **[Module 4: Assumption Miner](modules/4_assumptions.md)** - Implicit dependency inference.
6.  **[Module 5: Gap Signal Generator](modules/5_gaps.md)** - Critique signal generation.
7.  **[Module 6: Validation Synthesizer](modules/6_validation.md)** - Research question generation.

---

## 3. System Constraints (The "Defensibility" Layer)
To maintain scientific rigor, SCARF adheres to strict principles:

1.  **No Hallucination**: No reasoning step may reference information outside the grounded document (Module 0).
2.  **Alignment, Not Truth**: We check if the paper's evidence supports its claims. We do not fact-check against the entire internet.
3.  **Signals, Not Verdicts**: Output "Gap Signals", not "Rejections".
4.  **Uncertainty Flagging**: Explicitly mark low-confidence inferences.

---

## 4. Evaluation Strategy
We systematically evaluate structure, not correctness.
See [**Evaluation Strategy**](evaluation/strategy.md).

---

## 5. Technology Stack
*   **Perception**: `PaddleOCR-VL` (Layout Analysis)
*   **Reasoning**: `ERNIE 4.5/5` (Novita AI)
*   **Engineering**: `FastAPI` + `Python`

> *SCARF does not judge. It illuminates.*
