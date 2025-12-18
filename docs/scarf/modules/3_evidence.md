# Module 3: Evidence Linker

**Status**: v1 (Full Implementation)
**Role**: The Forensic Analyst.

## 🎯 Responsibility
Link each extracted extracted Claim (from M2) to explicit supporting **Evidence** in the text.
This answers: "Where is the proof?"

## ⚙️ Inputs & Outputs

*   **Input**: `ClaimList` (from M2) + Sections labeled `RESULTS` (from M1).
*   **Output**: `EvidenceGraph`.
    ```json
    [
      {
        "claim_id": "C1",
        "evidence_links": [
          {
            "section_id": "S6",
            "type": "QUANTITATIVE",
            "snippet": "Table 2 shows a 5% improvement.",
            "notes": "Compared on ImageNet only."
          }
        ]
      }
    ]
    ```

## 🔬 Evidence Taxonomy
1.  **Quantitative**: Tables, charts, metrics (e.g., "Accuracy = 95%").
2.  **Qualitative**: Visual inspection, case studies (e.g., "Figure 4 shows sharper edges").
3.  **Theoretical**: Mathematical proof, derivation.
4.  **None**: No evidence found (Flag this!).

## 🧠 Logic (ERNIE Prompt)
**Prompt Strategy**:
"Given Claim C1 and Section S6, does this section provide specific evidence supporting the claim? If yes, describe the type."

## 🔒 Constraints
*   **No Interpretation**: Do not judge if the evidence is *good*. Just check if it *exists* and is *relevant*.
*   **Strict Linking**: Evidence must be cited or present in the text.
