# SCARF Evaluation Strategy

**"We do not evaluate truth. We evaluate structural alignment."**

This document defines how we prove SCARF works. We cannot rely on standard "Accuracy" metrics because scientific truth is debated. Instead, we use proxy metrics for **reasoning quality**.

---

## 1. Claim Extraction: Precision
*   **Metric**: `Claim Precision`.
*   **Test**: Take 3-5 seminal papers. Manually annotate the "Main Claims". Run Module 2.
*   **Success**: Did SCARF find the main claims? Did it avoid extracting background noise?

## 2. Evidence Linking: Coverage
*   **Metric**: `Evidence Link Rate`.
*   **Test**: For every extracted claim, does SCARF find a link?
*   **Constraint**: We do not check if the experiment was done *correctly* (that's hard). We check if the *pointer* to the experiment is valid.

## 3. Assumption Mining: Plausibility
*   **Metric**: `Human Plausibility Score (1-5)`.
*   **Test**: Show extracted assumptions to a human.
*   **Question**: "Is this a reasonable thing to infer?" vs "Is this a hallucination?".
*   **Target**: >50% plausibility is a success for v1.

## 4. Gap Analysis: Reviewer Alignment
*   **Metric**: `Reviewer Utility`.
*   **Test**: "Would a peer reviewer find this signal useful?"
*   **Goal**: The signal doesn't need to be fatal, just **worth checking**.

## 5. End-to-End: The "Aha!" Test
For each processed paper, we ask:
*   "Did SCARF surface a structural detail I would have missed in a 5-minute skim?"

If **Yes** -> The system adds value.
