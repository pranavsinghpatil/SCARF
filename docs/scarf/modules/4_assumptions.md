# Module 4: Assumption Miner

**Status**: v1 (Partial Implementation)
**Role**: The Deep Reader.

## 🎯 Responsibility
Surface **implicit dependencies** required for the claims to hold. These are rarely written explicitly in the paper.

## ⚙️ Inputs & Outputs

*   **Input**: `ClaimList` + `METHOD` Sections.
*   **Output**: `AssumptionLedger`.
    ```json
    [
      {
        "claim_id": "C1",
        "assumptions": [
          {
            "type": "DATA",
            "statement": "Training data is i.i.d.",
            "confidence": 0.7
          }
        ]
      }
    ]
    ```

## 🔬 Assumption Categories (v1)
1.  **Data Assumptions**: "Training set covers the inference distribution."
2.  **Model Assumptions**: "Linearity, Stationarity, Independence."
3.  **Evaluation Assumptions**: "Metric X is a valid proxy for quality Y."

## 🧠 Logic (ERNIE Prompt)
**Prompt Strategy**:
"Identify implicit assumptions required for this method to work. Rules: If unsure, return empty list. Assumptions must be plausible."

## 🔒 Constraints
*   **High Confidence Only**: Do not guess wild assumptions.
*   **Explicit Uncertainty**: Always attach a confidence score.
