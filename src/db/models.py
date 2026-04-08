from __future__ import annotations

from src.db.migrations import apply_migrations


def initialize_tables() -> None:
    apply_migrations()
