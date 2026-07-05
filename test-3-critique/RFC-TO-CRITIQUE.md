# RFC — Mary scoring v5: Confidence-calibrated unified scoring

**Author:** [previous candidate, anonymized]
**Date:** 2026-05-08
**Status:** Proposed
**Reviewer:** YOU

---

## Background

Mary's current scoring uses a 5-gate model (Importer / Product / Volume / Company / Portal), with each gate evaluated separately and a deterministic sum producing the final 0-100 score. The model has been in production since March 2026.

**The problem we're solving:** the gate-based model under-counts business impact on tail opportunities. The L009 incident (Andean Distribuciones, Brazil) is the canonical example — scored Warm (67) at first touch, ultimately closed for $500K (would have been Hot if the system understood deal size). This pattern recurs: ~3-5 leads per quarter that look "Warm" by gate-sum but represent significant commercial opportunities.

## Proposal

Replace the 5-gate model with a single LLM call that produces:
- A 0-100 score
- A confidence interval (e.g., "75 ± 12")
- A natural-language rationale

The LLM call uses Claude Sonnet 4.5 with a structured prompt incorporating the same five signal categories the current gates evaluate, but allows the model to weigh signals contextually rather than via fixed arithmetic.

### Why this works

- **Confidence calibration enables tail detection** — when the model is highly confident a lead is Warm, it's a routine Warm. When it's confident a lead is in the tail (e.g., scoring 85±2), that confidence signal can route to KAM-with-review rather than direct nurture.
- **Contextual weighting captures L009-shaped leads** — the 5-gate model gives equal weight to each gate; a single LLM call can recognize that "12-year importer + $300K revenue + clear commitment" should outweigh a missed Portal gate.
- **Reduces system complexity** — removing the per-gate evaluation removes ~400 lines of scoring code and eliminates the gate-by-gate eval surface, which has been a maintenance burden.

### Evidence

We piloted the new approach against 14 historical conversations from the staging dataset. Results:

| Metric | Old (gates) | New (calibrated LLM) |
|--------|-------------|----------------------|
| Tier accuracy | 71% | 79% |
| Tail detection (Warm with score >70) | 14% | 50% |
| Confidence calibration (Brier score) | n/a | 0.18 |

Tail detection improved 3.6× in the sample — sufficient to expect this would have caught L009-shaped opportunities in the wild.

## Migration plan

1. Ship the new scoring as a shadow service (week 1)
2. Run both systems in parallel for 14 days
3. Cut over once shadow accuracy ≥ production accuracy
4. Remove the gate-based scoring code (week 4)

Total estimated effort: 3-4 weeks of engineering. One backend engineer + half-time of an eval engineer.

## Risk assessment

- **LLM variance** — sample-to-sample variance on the same input. Mitigation: temperature 0, retry-on-shape-fail.
- **Cost** — per-call Sonnet inference ~$0.003 vs current $0 (deterministic). At ~50 conversations/day, ~$0.15/day. Acceptable.
- **Eval drift** — without per-gate scoring, we can no longer A/B individual signal weights. Mitigation: we don't need to, because the LLM contextualizes them.

## Recommendation

Approve. Ship to production within 6 weeks. Decommission gate scoring at month 3.

---

*Signed off internally by tech lead.*
