# BusinessIntelligence.ai — The AI Business Investigator

**Accenture Innovation Challenge 2026 — Round 2 · Problem Track 3**

Dashboards report *what* changed. BusinessIntelligence.ai automatically investigates
*why*, tests competing explanations against evidence, states its confidence
(including "I don't know yet"), and hands managers a persona-specific action brief.

▶ **Demo video:** `[add your unlisted YouTube / Loom link here]`
▶ **Live interactive prototype:** open `prototype/index.html` in a browser (see note below)

---

## What's in this repo

```
├── prototype/
│   └── index.html            # Interactive investigation console (the working prototype)
├── engine/
│   ├── detection.py           # Step 1: deterministic signal detection (control chart / z-score)
│   └── evidence_engine.py     # Steps 2-4: deterministic hypothesis scoring + confidence
├── data/
│   ├── sales_daily.csv        # Simulated Sales source (daily grain)
│   ├── inventory_daily.csv    # Simulated Ops/Inventory source (daily grain)
│   ├── crm_weekly.csv         # Simulated CRM source (weekly grain, different cadence)
│   └── kpi_semantic_contract.yaml   # Governed KPI definitions, lineage, access roles
└── README.md
```

## The five-stage pipeline

| Stage | Method | LLM? |
|---|---|---|
| 1. Detect signal | Rolling mean/std control chart | No |
| 2. Gather context | Deterministic source join + reconciliation | No |
| 3. Test hypotheses | Weighted rule-based evidence scoring | No |
| 4. Explain with evidence | Deterministic confidence scoring → **LLM narrates the result** | Narration only |
| 5. Recommend action | Deterministic action-brief assembly | No |

**The LLM is never the source of quantitative truth.** It receives an already-computed
evidence bundle (JSON) and is instructed not to introduce any figure that isn't in it.
Every other stage is plain statistics, rules, and joins — auditable by a non-technical
stakeholder.

## What the prototype demonstrates (Round 2 minimum expectations)

- **5 KPIs across 4 source systems at different grains/cadences** — Sales (daily),
  Ops/Inventory (daily), CRM (weekly), Finance (weekly)
- **A governed KPI semantic contract** — `data/kpi_semantic_contract.yaml`
- **2 personas with different narratives/actions** — Regional Sales Manager vs. CFO,
  switchable live in the console
- **One multi-factor movement** — Case A1, Regional Revenue (inventory shortage vs.
  competitor promotion vs. campaign issue)
- **One abstention scenario** — Case A2, Churn Rate; evidence contradicts itself across
  cohorts, so the engine asks a clarifying question instead of guessing
- **One sparse-history KPI** — Case A3, a product launched 18 days ago; falls back to a
  category-proxy baseline and caps confidence at Medium
- **One role-based security scenario** — Case A4, Gross Margin; locked unless the CFO
  persona is selected
- **A case shown with no investigation at all** — Case A5, Inventory Availability;
  included deliberately to show the engine stays quiet on normal variation
- **Runtime telemetry** — live panel tracking model calls, latency, estimated tokens,
  and estimated cost per investigation

## Running it

**Interactive console (`prototype/index.html`):** this file calls the Anthropic API
directly from the browser for the narrative-synthesis step. It runs out of the box
inside a Claude.ai artifact (which proxies that call automatically). To run it as a
fully standalone static file outside that environment, either:
- point the `fetch()` call at your own backend endpoint that holds an API key, or
- run it in "deterministic-only" mode by skipping the "Generate narrative" button —
  every other stage works with no API access at all.

**Reference Python engine** (shows the same detection/scoring logic outside the browser):

```bash
cd engine
python3 detection.py        # z-score control-chart detection on the Sales CSV
python3 evidence_engine.py  # weighted hypothesis scoring + confidence derivation
```

No dependencies beyond the Python standard library.

## Design principle

> Separate meaningful movement from noise. Connect a hypothesis to evidence. Consider
> alternatives. State uncertainty plainly. Never let a fluent narrative substitute for
> evidence — a correlation should never quietly become a confident, wrong cause.

## Roadmap (see full Business Proposal for detail)

1. **MVP** — wire the pipeline to 1-2 real KPIs for one business unit, human-approval
   gate on every recommendation
2. **Pilot** — full KPI set for one business unit, feedback capture, weight
   recalibration
3. **Scale** — multi-business-unit rollout, more personas/entitlements, tiered
   agentic follow-up actions

## Team

- Vishaka Singh — Team Leader — IIT Delhi, Chemical Engineering
- [Team Member 2] — [College] — [Stream]
- [Team Member 3] — [College] — [Stream]
