# Module 5: Gap Signal Generator

**Status**: v1 (Basic Implementation)
**Role**: The Consultant.

## 🎯 Responsibility
Emit **non-judgmental critique signals**.
We do not say "The paper is wrong." We say "Here is a pattern that usually indicates weakness."

## ⚙️ Inputs & Outputs

*   **Input**: `EvidenceGraph` (M3) + `AssumptionLedger` (M4).
*   **Output**: `GapAnalysis`.
    ```json
    {
      "claim_id": "C1",
      "signals": [
        "Claim claims generalization but evidence is limited to one dataset.",
        "No ablation study for the added attention module."
      ]
    }
    ```

## 🔬 Signal Types
*   **Unsupported Claim**: Claim exists, Evidence list is empty.
*   **Narrow Evaluation**: Evidence exists, but is limited to a specific setting (e.g., synthetic data).
*   **Missing Ablation**: Multi-part method, but no component-wise testing.

## 🧠 Logic (ERNIE Prompt)
**Prompt Strategy**:
"Given the claim and linked evidence, identify potential gaps. Phrase as signals, not conclusions."

## 🔒 Constraints
*   **Tone**: Neutral, objective, assistive.
*   **Traceability**: Every signal must point to a specific Claim/Evidence mismatch.
