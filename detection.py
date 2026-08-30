"""
detection.py — Step 1 of the investigation pipeline: DETECT SIGNAL.

Deterministic only. No LLM calls happen here or in evidence_engine.py —
the LLM is used exclusively for narrative synthesis in the console
prototype (prototype/index.html), never for computing whether a
movement is meaningful.

Method: rolling mean / standard deviation control chart. A point is
flagged when it falls outside `z_threshold` standard deviations of the
trailing window. This is intentionally simple and auditable — a
stakeholder can recompute it by hand from the same numbers.
"""

import csv
import statistics as stats
from dataclasses import dataclass


@dataclass
class DetectionResult:
    kpi: str
    window_mean: float
    window_std: float
    actual: float
    z_score: float
    flagged: bool
    note: str


def load_series(csv_path: str, value_col: str, group_filter: dict | None = None):
    """Load a single numeric series from a CSV, optionally filtered to one group."""
    values = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            if group_filter and any(row.get(k) != v for k, v in group_filter.items()):
                continue
            values.append(float(row[value_col]))
    return values


def detect(series: list[float], kpi_name: str, z_threshold: float = 2.0,
           min_history: int = 6) -> DetectionResult:
    """
    Compare the latest point in `series` against the trailing window
    (everything before it). Falls back to a widened threshold note if
    history is too short to trust the baseline — this is the sparse-
    history path (see ADOPT_NEWPROD in the semantic contract).
    """
    if len(series) < 2:
        raise ValueError("Need at least 2 points to detect anything.")

    *window, actual = series
    sparse = len(window) < min_history

    mean = stats.mean(window)
    std = stats.pstdev(window) if len(window) > 1 else 0.0
    z = (actual - mean) / std if std > 0 else 0.0
    flagged = abs(z) >= z_threshold

    note = (
        f"Only {len(window)} historical points available (< {min_history}); "
        "baseline is unreliable. In production this falls back to a "
        "category/proxy baseline and caps downstream confidence at Medium."
        if sparse else
        f"Rolling window of {len(window)} points, mean={mean:.1f}, std={std:.2f}."
    )

    return DetectionResult(
        kpi=kpi_name, window_mean=round(mean, 2), window_std=round(std, 2),
        actual=actual, z_score=round(z, 2), flagged=flagged, note=note,
    )


if __name__ == "__main__":
    # Regional Revenue — Region A, Product X (multi-factor movement case)
    revenue = load_series(
        "../data/sales_daily.csv", "revenue_index",
        group_filter={"region": "Region A", "product": "Product X"},
    )
    result = detect(revenue, "Regional Revenue — Region A")
    print(result)

    # New Product Adoption has no equivalent CSV baseline in this sample —
    # see engine/evidence_engine.py and the prototype for the sparse-history
    # path, which is illustrated with hard-coded proxy data for the demo.
