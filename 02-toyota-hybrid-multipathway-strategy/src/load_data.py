"""Load raw and processed datasets."""

from pathlib import Path

import pandas as pd

from src.utils import PROCESSED_DIR, RAW_DIR

RAW_FILES = {
    "toyota_electrified_sales": "toyota_electrified_sales.csv",
    "company_bev_sales": "company_bev_sales.csv",
    "ev_investments": "ev_investments.csv",
    "financials": "financials.csv",
    "battery_material_prices": "battery_material_prices.csv",
    "charging_infrastructure": "charging_infrastructure.csv",
    "tariff_events": "tariff_events.csv",
}

PROCESSED_FILES = {
    "toyota_mix": "toyota_mix_clean.csv",
    "bev_sales": "bev_sales_clean.csv",
    "financials": "financials_clean.csv",
    "battery_index": "battery_index_clean.csv",
    "risk_summary": "risk_summary.csv",
}


def load_raw(name: str) -> pd.DataFrame:
    """Load a named raw CSV."""
    if name not in RAW_FILES:
        raise KeyError(f"Unknown raw dataset: {name}. Choose from {list(RAW_FILES)}")
    path = RAW_DIR / RAW_FILES[name]
    return pd.read_csv(path, parse_dates=["date"] if name == "tariff_events" else False)


def load_processed(name: str) -> pd.DataFrame:
    """Load a named processed CSV."""
    if name not in PROCESSED_FILES:
        raise KeyError(
            f"Unknown processed dataset: {name}. Choose from {list(PROCESSED_FILES)}"
        )
    path = PROCESSED_DIR / PROCESSED_FILES[name]
    return pd.read_csv(path)


def load_all_raw() -> dict[str, pd.DataFrame]:
    """Load every raw dataset."""
    return {name: load_raw(name) for name in RAW_FILES}


def load_all_processed() -> dict[str, pd.DataFrame]:
    """Load every processed dataset."""
    return {name: load_processed(name) for name in PROCESSED_FILES}
