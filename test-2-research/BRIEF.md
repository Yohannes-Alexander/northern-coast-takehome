# Test 2 — WhatsApp messaging at scale: design the path

You have **1 hour**. Use Claude + any research tools. Output: a written recommendation we'll read carefully and discuss in the debrief.

We're testing **judgment under research pressure** — can you navigate an open problem efficiently, identify the load-bearing constraints, verify your facts against real sources, and commit to a defended recommendation?

---

## The situation

We're a B2B beverage distributor. Wholesale leads flow inbound from 60+ countries. Most contact us via WhatsApp; some via email. Container-load orders ($30K-$100K each).

Operationally today:

- **The main BSD WhatsApp number** runs on ManyChat — a generic chatbot tool. It's how we capture inbound first-touch. **We've decided to move off ManyChat.** It can't do what we need (we'll get to what we need below).
- **Each of our 4 KAMs has their own WhatsApp Business App (WAB) on a VOIP number** — one number per KAM, on a phone they actually use to message customers. These are their working phones. The KAMs *talk* to customers on these numbers. They don't want to move to a desktop tool — they need WAB on a phone.
- We've been **considering consolidating to one BSD number for everything**, but the routing problem is unsolved — how does inbound to that single number get to the right KAM without a human triaging?

## What we need

Programmatic, high-volume, two-way WhatsApp at scale. Specifically:

- **~2K outbound messages/day, scaling to ~10K/day** within 6 months
- **Inbound from these messages** routed back to the right KAM (or to an AI agent that drafts a reply for KAM approval)
- **All conversation data captured into our customer data platform** — we OWN the conversations. Not "data we rent from a SaaS inbox." Owned, queryable, in our database.
- **Each KAM keeps WAB on their phone.** This is a hard constraint. The KAMs run the customer relationships; their phones are how they do that. Anything that requires them to "log into a desktop app" is wrong.
- Cost-sensitive but not cheap-at-all-costs. We'll pay for the right architecture.

## What we suspect (but haven't confirmed)

- WhatsApp Business API (the API behind WAB) is going to come up. Read its docs.
- The WhatsApp ecosystem has middlemen between you and Meta. They might matter; they might be a tax. Figure it out.
- The "consolidate to one number" path and the "keep KAM numbers" path are fundamentally different architectures. They have different vendors, different costs, different operational shape. We're not telling you which we've picked because we want your view.
- Vendors in this space are categorized in ways that aren't obvious from a single comparison sheet. Don't trust feature checklists alone.

## What we're NOT looking for

- A vendor-comparison spreadsheet (Twilio vs Vonage vs Wati...). That's the obvious output. We've already done that mentally. We want the architectural call.
- A "depends on your needs" hedge. Commit to a recommendation.
- A 12-month roadmap. We want the next 30 days.

## What to submit

A single document (markdown, no length cap but **shorter is better if you can defend it**). Include:

1. **Your recommendation** — specifically what to build / buy / integrate, in one paragraph at the top.

2. **The load-bearing constraints you identified.** Which ones eliminate options? Which ones are softer? Why did you prioritize them in this order?

3. **The vendor / architecture path you'd take.** Name the specific product(s). Cite real URLs (vendor docs / pricing pages / API references) that we can open and verify.

4. **A defensive pilot plan** — the actual concrete steps to PROVE this works before committing. What do you test, in what order, with what cost cap? What would make you abandon this path and switch? Pilots are designed to fail fast, not to succeed.

5. **What Phase 1 looks like AFTER the pilot succeeds.** First 30 days of real rollout. What ships, what stays manual, what stays sequential, what runs in parallel. Specific milestones with acceptance criteria.

6. **What you'd verify before signing a contract.** Three specific things you couldn't confirm in 1 hour but would need to before committing.

7. **What you considered and rejected.** At least 2 alternative paths, with the specific reason each fails.

8. **Where you used AI vs overrode it.** If your initial Claude-generated answer changed during the hour, tell us where and why. If it didn't change, tell us why you trusted it.

## Time

**1 hour, hard cap.** If you go significantly over (~90+ min), report that honestly. We'd rather see a 1-hour-shaped output than a 3-hour overworked one.

## Note on AI use

You're expected to use Claude / Codex / browse / search throughout. The signal is **not** "did you use AI." The signal is "**did you verify what AI told you, and where did you push back on it?**"

A common failure pattern in this space: Claude is high-confidence-wrong on specific vendor products. Vendor categorization, coexistence rules, pricing structures, post-2024 product changes — these are training-cutoff territory. We've seen Claude confidently mislead on respond.io, Chakra, BSP categories, WABA-specific features. The truth lives in vendor docs and recent forum posts.

We don't penalize being initially wrong. We penalize *staying* wrong.

---

Good luck. We read for taste, not output volume.
