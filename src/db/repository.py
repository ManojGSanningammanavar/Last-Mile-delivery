from __future__ import annotations

from src.db.database import get_connection


def save_prediction(order_id: str, failure_probability: float, risk_label: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO predictions (order_id, failure_probability, risk_label) VALUES (?, ?, ?)",
            (order_id, failure_probability, risk_label),
        )
        conn.commit()


def prediction_monitoring_summary(window_hours: int = 24) -> dict:
    safe_window = max(1, int(window_hours))
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT
                COUNT(*) AS total,
                AVG(failure_probability) AS avg_probability,
                SUM(CASE WHEN risk_label = 'HIGH' THEN 1 ELSE 0 END) AS high_count,
                SUM(CASE WHEN risk_label = 'MEDIUM' THEN 1 ELSE 0 END) AS medium_count,
                SUM(CASE WHEN risk_label = 'LOW' THEN 1 ELSE 0 END) AS low_count
            FROM predictions
            WHERE created_at >= datetime('now', ?)
            """,
            (f"-{safe_window} hours",),
        ).fetchone()

    total = int(row[0] or 0)
    avg_probability = float(row[1] or 0.0)
    high = int(row[2] or 0)
    medium = int(row[3] or 0)
    low = int(row[4] or 0)
    return {
        "window_hours": safe_window,
        "total_predictions": total,
        "avg_failure_probability": round(avg_probability, 4),
        "risk_mix": {
            "HIGH": high,
            "MEDIUM": medium,
            "LOW": low,
        },
    }
