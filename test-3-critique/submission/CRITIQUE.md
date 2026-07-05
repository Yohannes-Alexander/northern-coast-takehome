# RFC Critique — Mary Scoring v5: Confidence-Calibrated Unified Scoring

As a Senior AI Platform Engineer, I have reviewed the proposed RFC for Mary Scoring v5. Below is my detailed evaluation, scoring, and recommendation.

---

## 1. Score the RFC

*   **Problem Framing: 3/5**
    *   *Rationale*: Identifying "missed whales" (tail opportunities like L009) is commercially critical, but framing a text-generated "confidence interval" (e.g., `± 12`) as a statistically valid calibration mechanism is conceptually flawed.
*   **Evidence Quality: 1/5**
    *   *Rationale*: A dataset of only 14 historical conversations is statistically insignificant; the claimed 71% to 79% accuracy shift represents a difference of exactly *one* conversation, which is pure noise.
*   **Architectural Fit: 2/5**
    *   *Rationale*: Collapsing structured gates into a single black-box LLM call increases opacity, completely eliminates explainability, and makes regression testing nearly impossible.
*   **Migration Risk: 2/5**
    *   *Rationale*: Determining "shadow accuracy" within a 14-day parallel run is operationally impossible because B2B wholesale deals take weeks or months to close, leaving us with no real ground truth to evaluate.
*   **Recommendation Supportability: 1/5**
    *   *Rationale*: Dismissing evaluation drift with the claim that "we don't need to A/B test because the LLM contextualizes signals" is a dangerous operational stance that leaves us with no debugging pathway when scoring breaks.

---

## 2. Load-Bearing Claims

### Claim 1: "Confidence calibration enables tail detection."
*   **Evaluation**: **Not Supported**. 
*   **Defense**: LLMs are notoriously poor at self-calibration and frequently output arbitrary numbers with high confidence. The "confidence interval" generated as text (e.g. `85±2`) is not a statistical calculation derived from probability theory; it is merely next-token prediction. Relying on an LLM to state its own uncertainty is highly unsafe for routing $30K-$100K deals.

### Claim 2: "The pilot results prove a 3.6x improvement in tail detection."
*   **Evaluation**: **Not Supported**.
*   **Defense**: The sample size of 14 is far too small. A change in tail detection from 14% (2 leads) to 50% (7 leads) on a sample of 14 is statistically meaningless. Furthermore, the RFC cites a Brier score of `0.18` but fails to explain how this was calculated. To compute a Brier score, one needs binary outcomes (deal closed vs. not) and predicted probabilities. A textual interval `75 ± 12` cannot be directly mapped to a Brier score without arbitrary statistical assumptions that the author does not document.

### Claim 3: "Removing gates reduces system complexity and maintenance burden."
*   **Evaluation**: **Partially Supported, but misleading**.
*   **Defense**: While it does delete ~400 lines of deterministic Python code, it shifts the complexity into a prompt-engineering black box. Instead of debugging predictable Python code, engineers will spend time trying to adjust system instructions to fix edge cases, which frequently introduces regressions in other leads. Net system complexity and debugging time will increase.

### Claim 4: "We can cut over once shadow accuracy &ge; production accuracy during a 14-day parallel run."
*   **Evaluation**: **Not Supported**.
*   **Defense**: The definition of "accuracy" here is undefined. How do we establish the ground truth of a lead's value within 14 days? If a lead is routed to the nurture pool (Warm), we won't know if it was a "missed whale" (like L009) until months later when they either close elsewhere or re-engage. A 14-day window is mathematically insufficient to calculate true B2B lead conversion accuracy.

---

## 3. What's Missing

1.  **A Predictable Hybrid Architecture (LLM Extraction + Rule Engine)**:
    *   The author did not consider using the LLM solely as a structured entity extractor (extracting volume, presence of license, years of experience, product brand) while keeping the score calculation in deterministic Python. This hybrid approach gives the benefit of LLM context parsing while maintaining 100% predictability, observability, and easy A/B testing of business weights.
2.  **A Robust Regression Testing Suite (Evals)**:
    *   There is no mention of how we will test prompt changes. If we change the system prompt to fix a bug, how do we guarantee we don't break scoring for hot leads? The RFC lacks an automated eval framework (like Promptfoo or custom assertion tests) running against a large dataset (e.g., 500+ historical leads).
3.  **Explainability / Audit Trails for Sales**:
    *   When a KAM asks, *"Why was this lead archived?"*, we cannot tell them. In the 5-gate model, we could point to the specific failed gate (e.g., "Company has no import license"). In the proposed model, we only have a natural-language rationale which may hallucinate or contradict the score.

---

## 4. Decision

**Decision**: **send-back-to-author**

### Defense:
While the candidate correctly identifies a crucial commercial problem—the current system under-scores high-value tail leads like L009—the proposed solution is a regression in software engineering best practices. It trades structured, debuggable code for an uncalibrated, black-box LLM call backed by mathematically invalid statistics and a statistically noisy 14-sample pilot. 

To get this approved, the author must:
1.  **Revise the architecture**: Propose a hybrid model where the LLM extracts structured features (validated via Pydantic) and a Python service computes the score and confidence.
2.  **Increase evaluation scale**: Test the proposed changes against at least 200+ historical leads, showing statistically significant improvements.
3.  **Define real metrics**: Replace the hand-waved Brier score and "shadow accuracy" with a concrete definition of ground truth (e.g., historical sales closure data) and a longer shadow observation period (e.g., 60 days) to match our B2B sales cycle.

---

## 5. Debrief Questions

1.  *"How did you mathematically calculate the Brier score of 0.18 using a textual output format like '75 ± 12' against a sample size of 14, and what was the binary ground truth used?"*
    *   *Why it matters*: Tests if the candidate actually understands the statistics they cited or if they are throwing buzzwords into the RFC to sound authoritative.
2.  *"If we deploy this and a KAM complains that a specific high-value client was scored a 30 (Cold) and archived, what is the exact engineering workflow to debug, fix, and verify that the fix doesn't break other leads?"*
    *   *Why it matters*: Exposes the candidate's operational maturity. A junior will say "we adjust the prompt," whereas a senior will realize that prompt adjustment without a regression suite is a game of whack-a-mole.
3.  *"Why did you choose a 14-day shadow migration period, and how do you plan to establish the 'ground truth' conversion of the shadow leads in that time frame when our sales cycle is historically 45+ days?"*
    *   *Why it matters*: Probes their understanding of the underlying business domain (B2B wholesale sales cycle) versus blindly applying a standard web SaaS rollout playbook.
4.  *"Why did you decide to let the LLM calculate the final score contextually rather than using the LLM to extract structured attributes (e.g. volume, license status) and calculating the score deterministically in code?"*
    *   *Why it matters*: Tests if the candidate can weigh architectural trade-offs (flexibility vs. predictability/observability) or if they simply default to "let the LLM do everything."
