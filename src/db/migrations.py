from __future__ import annotations

from src.db.database import get_connection

MIGRATIONS: list[tuple[int, str]] = [
    (
        1,
        """
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            failure_probability REAL NOT NULL,
            risk_label TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ),
    (
        2,
        """
        CREATE INDEX IF NOT EXISTS idx_predictions_order_id ON predictions(order_id);
        """,
    ),
    (
        3,
        """
        CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at);
        """,
    ),
]


def apply_migrations() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                applied_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        existing = {
            int(row[0])
            for row in conn.execute("SELECT version FROM schema_migrations").fetchall()
        }

        for version, sql in MIGRATIONS:
            if version in existing:
                continue
            conn.executescript(sql)
            conn.execute("INSERT INTO schema_migrations (version) VALUES (?)", (version,))

        conn.commit()
