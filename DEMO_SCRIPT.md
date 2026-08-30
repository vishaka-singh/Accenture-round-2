# Demo Video Script — BusinessIntelligence.ai (target: 3 minutes)

Recorded directly from `prototype/index.html`. Matches the narration style of your
Round 1 deck. Time budget assumes screen-recording with voiceover, no editing tricks
required.

---

### 0:00–0:20 — Hook (mirrors Round 1 slide 1)
**Screen:** open on the case list, Case A1 selected, Step 1 "Detect signal."
**Say:** "Your dashboard already told you regional revenue is down. It won't tell you
why, or what to do about it. That gap — between what happened and what to do — is what
we built BusinessIntelligence.ai to close."

### 0:20–0:45 — Step 1: Detect
**Screen:** point at the expected range (95-105) vs. actual (88), z-score.
**Say:** "This isn't a threshold alert. It's a rolling statistical control chart —
fully deterministic, no model involved — so a stakeholder can recompute this by hand
and trust the trigger."

### 0:45–1:05 — Step 2: Gather
**Screen:** click to Step 2, show the four source cards with different cadences.
**Say:** "Before any explanation is attempted, the engine reconciles Sales, Inventory,
CRM and market feedback onto a common grain — Product by Region by Time — even though
they refresh on different schedules."

### 1:05–1:35 — Step 3: Test hypotheses
**Screen:** Step 3, three hypothesis bars (Inventory 55%, Competitor 30%, Campaign 15%).
**Say:** "Instead of picking the first plausible story, it scores multiple competing
explanations against supporting and contradicting evidence. Inventory shortage wins —
not because it's first, but because four independent signals corroborate it and
nothing contradicts it."

### 1:35–2:00 — Step 4: Explain (the LLM moment)
**Screen:** Step 4, click "Generate investigator narrative," let it stream, point to
the "LLM — narrative synthesis only" tag and the confidence stamp.
**Say:** "Only here does a language model get involved — and only to turn this
already-scored evidence into plain language for the person reading it. It cannot
invent a number that isn't in the bundle above."

### 2:00–2:20 — The abstention case (differentiator)
**Screen:** switch to Case A2, Churn Rate. Show the "Insufficient evidence" stamp and
the clarifying question.
**Say:** "And when the evidence contradicts itself — like it does here, across customer
segments — the system doesn't guess. It says so, and asks the question a human analyst
would ask next."

### 2:20–2:40 — Persona + security
**Screen:** switch persona to CFO, open Case A4 (Gross Margin) — show it unlocking;
switch back to Regional Manager — show it lock.
**Say:** "The same case reads differently depending on who's asking, and sensitive
financial evidence stays restricted to the right role — enforced before it ever
reaches the narrative layer."

### 2:40–3:00 — Close
**Screen:** telemetry panel — calls, latency, tokens, cost; legend "4/5 stages
deterministic, 1/5 LLM."
**Say:** "Four of five stages are plain statistics and rules. One is a language model,
used only to narrate. That's the whole idea: an AI that investigates the business
before it recommends action — not one that guesses and sounds confident about it."

---

## Recording checklist
- [ ] Record at 1080p+, prototype window maximized
- [ ] Have the "Generate narrative" call succeed at least once before recording (first
      call can be slower — the telemetry latency number is more impressive on a warm run)
- [ ] Caption or verbally state the repo URL and README at the very end
- [ ] Keep total runtime ≤ 3:00 for judge attention span
