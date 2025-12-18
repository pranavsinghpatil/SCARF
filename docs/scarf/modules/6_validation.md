# Module 6: Validation Synthesizer

**Status**: v1 (Minimal Implementation)
**Role**: The Thinking Partner.

## 🎯 Responsibility
Generate **research-relevant validation questions**.
Instead of judging the paper, we ask questions that would help a human judge it.

## ⚙️ Inputs & Outputs

*   **Input**: `GapAnalysis` (M5).
*   **Output**: `ValidationQuestions`.
    ```json
    {
      "claim_id": "C1",
      "questions": [
        "How does performance change under domain shift?"
      ]
    }
    ```

## 🧠 Logic (ERNIE Prompt)
**Prompt Strategy**:
"Based on the identified gaps, generate up to 2 validation questions that could increase confidence in the claim."

## 🔒 Constraints
*   **Surgical**: Short, specific questions.
*   **Actionable**: Questions should imply a possible experiment.
