from __future__ import annotations

from datetime import datetime


def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def date_only(value: str) -> str:
    return parse_datetime(value).strftime("%Y-%m-%d")
