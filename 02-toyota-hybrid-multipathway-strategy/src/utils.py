"""Shared utilities for paths and formatting."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_CHARTS = PROJECT_ROOT / "outputs" / "charts"
OUTPUT_TABLES = PROJECT_ROOT / "outputs" / "tables"


def ensure_dirs() -> None:
    """Create output directories if missing."""
    for path in (PROCESSED_DIR, OUTPUT_CHARTS, OUTPUT_TABLES):
        path.mkdir(parents=True, exist_ok=True)


def fmt_billions(value: float) -> str:
    """Format a USD value in billions."""
    return f"${value:,.1f}B"


def fmt_pct(value: float) -> str:
    """Format a percentage with one decimal."""
    return f"{value:.1f}%"
