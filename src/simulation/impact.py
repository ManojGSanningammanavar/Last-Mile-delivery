from __future__ import annotations

import pandas as pd


def simulate_improvement(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "estimated_prevented_failures": 0,
            "high_risk_orders": 0,
            "prevented_ratio": 0.0,
        }

    high_risk = df[df["failure_probability"].astype(float) > 0.7]
    prevented = int(round(len(high_risk) * 0.5, 0))
    return {
        "estimated_prevented_failures": prevented,
        "high_risk_orders": int(len(high_risk)),
        "prevented_ratio": 0.5,
    }
