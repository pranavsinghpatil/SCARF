# Module 2: Claim Extractor

**Status**: v1 (Full Implementation)
**Role**: The Mining Engine.
**Criticality**: This is the core intellectual value of SCARF.

## 🎯 Responsibility
Identify, normalize, and index **primary scientific claims**.
A claim is not just a sentence; it is a scoped assertion.

## ⚙️ Inputs & Outputs

*   **Input**: Sections labeled `BACKGROUND`, `METHOD`, `RESULTS` (from M1).
*   **Output**: `ClaimList`.
    ```json
    [
      {
        "claim_id": "C1",
        "statement": "The proposed method improves accuracy by 5% over SOTA.",
        "type": "NOVELTY",
        "source_section": "S2",
        "confidence": 0.9
      }
    ]
    ```

## 🔬 Definition: What is a Claim?
A declarative statement asserting:
*   **Novelty**: "We propose a new mechanism..."
*   **Superiority**: "Our model outperforms X..."
*   **Effectiveness**: "The method creates stable embeddings..."
*   **Generalization**: "This approach works across domains..."

## 🧠 Logic (ERNIE Prompt)
**Prompt Strategy**:
"Extract primary scientific claims from the text. A claim is a declarative statement asserting novelty, effectiveness, generalization, or superiority. Rules: Do not extract background. Rewrite concisely."

## 🔒 Constraints
*   **Atomic**: One claim per object.
*   **Normalized**: Rewrite "We observed that X happens" to "X happens under condition Y".
