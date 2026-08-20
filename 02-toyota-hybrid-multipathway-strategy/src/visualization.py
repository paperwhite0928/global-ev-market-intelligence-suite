"""Chart helpers for notebooks and dashboard."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.utils import OUTPUT_CHARTS, ensure_dirs

PALETTE = {
    "HEV": "#2ecc71",
    "PHEV": "#3498db",
    "BEV": "#e74c3c",
    "FCEV": "#9b59b6",
}


def setup_style() -> None:
    """Apply consistent plot styling."""
    sns.set_theme(style="whitegrid", context="talk")
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["figure.dpi"] = 120


def save_fig(name: str) -> Path:
    """Save current figure to outputs/charts."""
    ensure_dirs()
    path = OUTPUT_CHARTS / f"{name}.png"
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    return path


def plot_toyota_mix_stacked(df: pd.DataFrame, region: str = "Global") -> Path:
    """Stacked area chart of Toyota powertrain mix."""
    setup_style()
    subset = df[df["region"] == region].pivot_table(
        index="year", columns="powertrain", values="units", aggfunc="sum", fill_value=0
    )
    colors = [PALETTE.get(c, "#95a5a6") for c in subset.columns]
    ax = subset.plot(kind="area", stacked=True, color=colors, alpha=0.85)
    ax.set_title(f"Toyota Electrified Sales Mix — {region}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Units (thousands)")
    ax.legend(title="Powertrain", bbox_to_anchor=(1.02, 1), loc="upper left")
    return save_fig(f"toyota_mix_{region.lower()}")


def plot_bev_market_share(df: pd.DataFrame, year: int | None = None) -> Path:
    """Bar chart of BEV market share by company."""
    setup_style()
    target_year = year or int(df["year"].max())
    subset = df[df["year"] == target_year].sort_values("market_share_pct", ascending=True)
    ax = sns.barplot(
        data=subset,
        y="company",
        x="market_share_pct",
        hue="company",
        palette="rocket",
        legend=False,
    )
    ax.set_title(f"BEV Market Share by OEM ({target_year})")
    ax.set_xlabel("Market Share (%)")
    ax.set_ylabel("")
    return save_fig(f"bev_share_{target_year}")


def plot_battery_index(df: pd.DataFrame) -> Path:
    """Line chart of composite battery material index."""
    setup_style()
    ax = sns.lineplot(data=df, x="year", y="composite_index", marker="o", linewidth=2.5)
    ax.axhline(100, color="gray", linestyle="--", alpha=0.6, label="2020 baseline")
    ax.set_title("Battery Material Cost Index (2020 = 100)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Index")
    ax.legend()
    return save_fig("battery_cost_index")


def plot_risk_heatmap(df: pd.DataFrame) -> Path:
    """Heatmap of regional BEV transition risk factors."""
    setup_style()
    metrics = df.set_index("region")[
        ["avg_tariff_impact", "battery_cost_index", "bev_transition_risk_score"]
    ]
    ax = sns.heatmap(metrics, annot=True, fmt=".1f", cmap="YlOrRd")
    ax.set_title("Regional BEV Transition Risk")
    return save_fig("regional_risk_heatmap")
