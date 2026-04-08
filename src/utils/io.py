from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def read_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def write_csv(df: pd.DataFrame, path: str | Path) -> None:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)


def read_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(payload: Any, path: str | Path) -> None:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)
