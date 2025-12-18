# Module 1: Rhetorical Segmenter

**Status**: v1 (Basic Implementation)
**Role**: The Map Maker.

## 🎯 Responsibility
Assign **functional roles** to the sections identified by Module 0.
We need to know *where* to look. Claims are usually in the Intro/Conclusion; Evidence is in Results.

## ⚙️ Inputs & Outputs

*   **Input**: `Document` (Sections).
*   **Output**: `RhetoricalMap`.
    ```json
    [
      {"section_id": "S1", "role": "BACKGROUND", "confidence": 0.95},
      {"section_id": "S4", "role": "METHOD", "confidence": 0.88},
      {"section_id": "S6", "role": "RESULTS", "confidence": 0.92}
    ]
    ```

## 🔬 Taxonomy (v1)
We limit roles to broad categories:
1.  `BACKGROUND`: Prior work, problem definition.
2.  `METHOD`: Proposed approach, architecture, algorithm.
3.  `RESULTS`: Experiments, datasets, tables, quantitative analysis.
4.  `DISCUSSION`: Interpretation, limitations, future work.

## 🧠 Logic (ERNIE Prompt)
**Task**: Classification.
**Prompt Strategy**:
"You are given a section of a scientific paper. Classify its rhetorical role as one of: [Background, Method, Results, Discussion]. Return JSON."

## 🔒 Constraints
*   **One Role per Section**: Simplify the model.
*   **Low Ambiguity**: If uncertain, default to `BODY`.
