"""Clean raw datasets and write processed tables."""

from __future__ import annotations

import pandas as pd

from src.load_data import load_all_raw
from src.utils import PROCESSED_DIR, ensure_dirs


def clean_toyota_mix(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate Toyota electrified sales by year and powertrain."""
    out = df.copy()
    out["year"] = out["year"].astype(int)
    out["units"] = out["units"].astype(int)
    out = out.groupby(["year", "region", "powertrain"], as_index=False)["units"].sum()
    out["share_within_region"] = out.groupby(["year", "region"])["units"].transform(
        lambda s: s / s.sum() * 100
    )
    return out.sort_values(["year", "region", "powertrain"]).reset_index(drop=True)


def clean_bev_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize peer BEV sales."""
    out = df.copy()
    out["year"] = out["year"].astype(int)
    out["bev_units"] = out["bev_units"].astype(int)
    out["market_share_pct"] = out["market_share_pct"].astype(float)
    total_by_year = out.groupby("year")["bev_units"].transform("sum")
    out["share_of_sample_pct"] = out["bev_units"] / total_by_year * 100
    return out.sort_values(["year", "company"]).reset_index(drop=True)


def clean_financials(df: pd.DataFrame) -> pd.DataFrame:
    """Clean Toyota financial metrics."""
    out = df.copy()
    out["year"] = out["year"].astype(int)
    numeric_cols = [
        "revenue_usd_b",
        "operating_margin_pct",
        "rd_spend_usd_b",
        "ev_capex_usd_b",
    ]
    for col in numeric_cols:
        out[col] = out[col].astype(float)
    out["rd_intensity_pct"] = out["rd_spend_usd_b"] / out["revenue_usd_b"] * 100
    return out.sort_values("year").reset_index(drop=True)


def clean_battery_index(df: pd.DataFrame) -> pd.DataFrame:
    """Build a normalized battery material price index (2020 = 100)."""
    out = df.copy()
    out["year"] = out["year"].astype(int)
    out["price_usd_per_unit"] = out["price_usd_per_unit"].astype(float)
    base = out[out["year"] == 2020].set_index("material")["price_usd_per_unit"]
    out["index_2020_base"] = out.apply(
        lambda row: row["price_usd_per_unit"] / base[row["material"]] * 100,
        axis=1,
    )
    composite = (
        out.groupby("year")["index_2020_base"].mean().reset_index(name="composite_index")
    )
    return composite.sort_values("year").reset_index(drop=True)


def build_risk_summary(
    tariffs: pd.DataFrame,
    charging: pd.DataFrame,
    battery: pd.DataFrame,
) -> pd.DataFrame:
    """Combine policy, infrastructure, and cost signals into a risk table."""
    tariff_score = (
        tariffs.groupby("region")["impact_score"]
        .mean()
        .reset_index(name="avg_tariff_impact")
    )
    infra = (
        charging[charging["year"] == charging["year"].max()]
        .groupby("region", as_index=False)
        .agg({"public_chargers": "sum", "population_millions": "sum"})
    )
    infra["infra_per_million_pop"] = (
        infra["public_chargers"] / infra["population_millions"]
    )
    latest_battery = battery[battery["year"] == battery["year"].max()][
        "composite_index"
    ].iloc[0]

    rows = []
    for _, row in tariff_score.iterrows():
        region = row["region"]
        infra_row = infra[infra["region"] == region]
        chargers = infra_row["infra_per_million_pop"].iloc[0] if len(infra_row) else 0
        risk = row["avg_tariff_impact"] * 0.4 + (latest_battery / 100) * 0.35
        if chargers < 500:
            risk += 0.25
        rows.append(
            {
                "region": region,
                "avg_tariff_impact": round(row["avg_tariff_impact"], 2),
                "battery_cost_index": round(latest_battery, 1),
                "chargers_per_million": round(chargers, 1),
                "bev_transition_risk_score": round(min(risk, 5.0), 2),
            }
        )
    return pd.DataFrame(rows).sort_values("bev_transition_risk_score", ascending=False)


def run_pipeline() -> dict[str, pd.DataFrame]:
    """Run full cleaning pipeline and persist outputs."""
    ensure_dirs()
    raw = load_all_raw()

    cleaned = {
        "toyota_mix": clean_toyota_mix(raw["toyota_electrified_sales"]),
        "bev_sales": clean_bev_sales(raw["company_bev_sales"]),
        "financials": clean_financials(raw["financials"]),
        "battery_index": clean_battery_index(raw["battery_material_prices"]),
    }
    cleaned["risk_summary"] = build_risk_summary(
        raw["tariff_events"],
        raw["charging_infrastructure"],
        cleaned["battery_index"],
    )

    cleaned["toyota_mix"].to_csv(PROCESSED_DIR / "toyota_mix_clean.csv", index=False)
    cleaned["bev_sales"].to_csv(PROCESSED_DIR / "bev_sales_clean.csv", index=False)
    cleaned["financials"].to_csv(PROCESSED_DIR / "financials_clean.csv", index=False)
    cleaned["battery_index"].to_csv(PROCESSED_DIR / "battery_index_clean.csv", index=False)
    cleaned["risk_summary"].to_csv(PROCESSED_DIR / "risk_summary.csv", index=False)

    return cleaned


if __name__ == "__main__":
    results = run_pipeline()
    print("Processed datasets written:")
    for name, df in results.items():
        print(f"  {name}: {len(df)} rows")
