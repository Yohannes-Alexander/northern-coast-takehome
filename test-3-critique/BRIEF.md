# Test 3 — Critique an RFC

You're a senior AI Platform Engineer at Northern Coast Beverages. A candidate at your role wrote an RFC for changes to our lead-qualification scoring system (Mary). The RFC has been signed off internally by their tech lead.

**Your job:** read the RFC at `RFC-TO-CRITIQUE.md`, evaluate it, and decide whether you'd approve it as-is, send it back for revision, or block it. Defend your call.

## What to submit

A single markdown file at `submission/CRITIQUE.md`. It must include all five sections below.

### 1. Score the RFC

Out of 5, on these dimensions:
- **Problem framing** (1-5)
- **Evidence quality** (1-5)
- **Architectural fit** (1-5)
- **Migration risk** (1-5)
- **Recommendation supportability** (1-5)

Brief 1-line rationale per dimension.

### 2. Load-bearing claims

Identify the 3-5 claims this RFC most depends on. For each, defend whether the evidence supports it. If it doesn't, say so explicitly.

### 3. What's missing

What did the author NOT consider? List 2-3 alternative approaches or considerations they should have addressed. Defend why each matters.

### 4. Decision

One of: **approve / approve-with-revisions / block / send-back-to-author**. Defend in 200 words.

If you'd block or send back: what specifically needs to change before this could be approved?

### 5. Debrief questions

3-5 questions you'd ask the author in a follow-up conversation. The questions should reveal whether they're a strong senior or someone going through the motions.

---

## What we're testing

This is **critical thinking** — your ability to read someone else's confident-sounding work and find what's wrong with it. Specifically:
- Can you identify which claims are load-bearing vs decorative?
- Can you spot when evidence is thinner than the conclusion it supports?
- Can you recognize missing alternatives the author should have addressed?
- Can you push back on a proposal that's been signed off by leadership?

We're NOT testing:
- Whether you agree with the proposal (well-reasoned approve and well-reasoned block are equally strong)
- Whether you would have written a better RFC (this is critique, not redesign)
- Whether you find every possible issue (we'd rather see 3 specific defended critiques than 10 vague ones)

## Time

60-90 min. Use AI tools freely. The signal is what you direct AI to check, not whether you used it.

## Note on context

Northern Coast is a fictional B2B beverage distributor. The L009 incident referenced in the RFC is an actual incident in our system (a "missed whale" — a lead scored Warm at first touch that converted to a $500K deal). Treat it as real for the purpose of evaluating the RFC's logic.
