# SCARF Glossary

Strict definitions for the terms used in the framework.

## 🏛 Structure
*   **Document Grounder**: The module that converts PDF bytes into addressable Sections.
*   **Rhetorical Segment**: A section of text classified by its functional role (e.g., "Results").

## 💎 Artifacts
*   **Claim**: A normalized declarative statement asserting scientific contribution (Novelty, Superiority, Generalization).
*   **Evidence**: A specific pointer to text, table, or figure that substantiates a Claim.
*   **Assumption**: A condition that must hold for a Claim or Method to be valid, but is not the explicit focus of the paper.
*   **Gap Signal**: A pattern indicating a potential weakness in the Claim-Evidence link (e.g., "Missing Ablation").

## ⚠️ Concepts
*   **Alignment**: The consistency between what is claimed and what is shown. SCARF judges Alignment, not Truth.
*   **Hallucination Guard**: The principle that no reasoning step may reference knowledge outside the provided document text.
*   **Decomposition**: The process of breaking a linear narrative into structured assertions (Claims) and supports (Evidence).
