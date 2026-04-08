from __future__ import annotations

from datetime import datetime
from datetime import timezone

import httpx
import pandas as pd


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def _compute_weather_risk(rainfall_mm: float, temperature_c: float) -> float:
    rain_component = min(0.7, max(0.0, rainfall_mm / 20.0))
    heat_component = min(0.3, max(0.0, abs(temperature_c - 26.0) / 20.0))
    return round(min(1.0, rain_component + heat_component), 4)


def load_weather_table(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def weather_score_for(df: pd.DataFrame, date: str, time_slot: str, city: str) -> float:
    matched = df[
        (df["date"] == date)
        & (df["time_slot"] == time_slot)
        & (df["city"].str.lower() == city.lower())
    ]
    if matched.empty:
        return 0.15
    return float(matched.iloc[0]["weather_risk_score"])


def live_weather_signal(lat: float, lon: float, timeout_seconds: float = 3.0) -> dict | None:
    try:
        response = httpx.get(
            OPEN_METEO_URL,
            params={
                "latitude": float(lat),
                "longitude": float(lon),
                "current": "temperature_2m,precipitation",
            },
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
        current = payload.get("current", {})
        temperature_c = float(current.get("temperature_2m", 26.0))
        rainfall_mm = float(current.get("precipitation", 0.0))
        risk_score = _compute_weather_risk(rainfall_mm, temperature_c)
        return {
            "source": "live_open_meteo",
            "temperature_c": temperature_c,
            "rainfall_mm": rainfall_mm,
            "weather_risk_score": risk_score,
            "observed_at": str(current.get("time", "")),
        }
    except Exception:
        return None


def weather_signal_for(
    *,
    weather_df: pd.DataFrame,
    date: str,
    time_slot: str,
    city: str,
    lat: float,
    lon: float,
    enable_live: bool,
) -> dict:
    table_score = weather_score_for(weather_df, date, time_slot, city)
    table_signal = {
        "source": "historical_table",
        "temperature_c": None,
        "rainfall_mm": None,
        "weather_risk_score": float(table_score),
        "observed_at": datetime.now(timezone.utc).isoformat(),
    }
    if not enable_live:
        return table_signal

    live = live_weather_signal(lat, lon)
    if live is None:
        return table_signal
    return live
