"""
evidence_engine.py — Steps 2-4 of the pipeline: GATHER CONTEXT,
TEST HYPOTHESES, EXPLAIN EVIDENCE.

Deterministic weighted rule scoring. Each hypothesis carries a list of
signals; each signal either supports or contradicts it. The score is a
simple normalized weighted sum — intentionally transparent over
"clever": a business stakeholder should be able to see exactly why a
hypothesis ranked where it did.

Confidence is then derived from the score distribution AND the
support/contradiction balance — a hypothesis can score highest and
still yield only Medium or Insufficient confidence if evidence is thin
or contradictory. This file has no LLM dependency.
"""

from dataclasses import dataclass, field


@dataclass
class Signal:
    description: str
    supports: bool
    weight: float = 1.0


@dataclass
class Hypothesis:
    name: str
    signals: list[Signal] = field(default_factory=list)

    @property
    def support_count(self) -> int:
        return sum(1 for s in self.signals if s.supports)

    @property
    def contra_count(self) -> int:
        return sum(1 for s in self.signals if not s.supports)

    @property
    def raw_score(self) -> float:
        return sum(s.weight if s.supports else -s.weight for s in self.signals)


def rank_hypotheses(hypotheses: list[Hypothesis]) -> list[dict]:
    """Normalize raw scores to a 0-100 scale across all hypotheses."""
    scores = [max(h.raw_score, 0) for h in hypotheses]
    total = sum(scores) or 1
    ranked = []
    for h, s in zip(hypotheses, scores):
        ranked.append({
            "name": h.name,
            "score_pct": round(100 * s / total, 1),
            "support": h.support_count,
            "contradict": h.contra_count,
        })
    return sorted(ranked, key=lambda r: -r["score_pct"])


def confidence_from(ranked: list[dict], contradictory_signal_gap: bool = False) -> str:
    """
    High: top hypothesis clearly separated, no contradiction, 3+ support.
    Medium: top hypothesis leads but with thinner or mixed evidence.
    Insufficient: leading hypotheses are within a few points of each
    other, or the same evidence set contradicts itself across cohorts
    (contradictory_signal_gap=True) — the engine abstains rather than
    guessing.
    """
    if contradictory_signal_gap:
        return "insufficient"
    if not ranked:
        return "insufficient"
    top = ranked[0]
    gap = top["score_pct"] - (ranked[1]["score_pct"] if len(ranked) > 1 else 0)
    if top["support"] >= 3 and top["contradict"] == 0 and gap >= 15:
        return "high"
    if top["support"] >= 1 and gap >= 5:
        return "medium"
    return "insufficient"


if __name__ == "__main__":
    # Regional Revenue case — mirrors prototype/index.html CASE A1
    inventory_shortage = Hypothesis("Inventory shortage", [
        Signal("Stockout flag = 1 for 4 consecutive weeks", True),
        Signal("Fulfillment delay tickets up 3x", True),
        Signal("Sell-through drop concentrated in 2 SKUs", True),
        Signal("No matching drop in web traffic (demand-side)", True),
    ])
    competitor_promo = Hypothesis("Competitor promotion", [
        Signal("Competitor price-tracking flagged a promo in Region A", True),
        Signal("Feedback mentions of competitor pricing up", True),
        Signal("Our own price held flat (would expect discounting if true)", False),
    ])
    campaign_issue = Hypothesis("Campaign under-delivery", [
        Signal("Campaign spend was on-plan", False),
        Signal("Click-through rate in line with baseline", False),
        Signal("Minor delivery delay on 1 channel", True),
    ])

    ranked = rank_hypotheses([inventory_shortage, competitor_promo, campaign_issue])
    for r in ranked:
        print(r)
    print("Confidence:", confidence_from(ranked))

    # Churn case — contradictory across cohorts -> abstain
    print("\nChurn case confidence:", confidence_from(ranked=[
        {"name": "Pricing change (SMB)", "score_pct": 38, "support": 2, "contradict": 2},
        {"name": "Onboarding friction", "score_pct": 34, "support": 2, "contradict": 1},
    ], contradictory_signal_gap=True))
