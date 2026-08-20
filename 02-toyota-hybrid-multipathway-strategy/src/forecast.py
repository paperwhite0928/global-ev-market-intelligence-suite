"""Toyota-Dedicated 2026-2030 Electrification Forecast and Simulation Engine.

This module models Toyota Motor Corporation's multi-pathway strategy,
projecting sales mix, financial profitability, battery capacity requirements,
and carbon abatement efficiency under customizable macro and internal scenarios.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Predefined Strategic Scenarios (Toyota Only)
# ---------------------------------------------------------------------------

SCENARIOS: Dict[str, Dict[str, Any]] = {
    "Base: Pragmatic Multi-Pathway": {
        "description": (
            "Baseline scenario aligned with Toyota's official electrification roadmap. "
            "Hybrids (HEV) sustain strong cash flow generation (4.8M–5.2M units/yr), "
            "while next-gen dedicated BEV platforms and gigacasting gradually scale BEVs to 1.8M units by 2030."
        ),
        "hev_growth_rate": 0.04,  # ~4% annual volume stabilization
        "bev_target_2030_k": 1800,  # 1.8M BEVs in 2030
        "phev_target_2030_k": 350,
        "avg_operating_margin": 10.2,  # 10.2% Operating Margin
        "battery_cost_2030": 85.0,  # $/kWh
        "solid_state_commercialized": 2027,
    },
    "Bull: Extended Chasm & Hybrid Supercycle": {
        "description": (
            "Public charging infrastructure bottlenecks and EV subsidy rollbacks prolong the global 'Hybrid Supercycle'. "
            "Global HEV demand surges past 6.0M units, generating industry-leading operating margins (11.5%–12.5%). "
            "BEV capex pacing is moderated (1.2M units by 2030) while solid-state battery R&D matures."
        ),
        "hev_growth_rate": 0.08,
        "bev_target_2030_k": 1200,
        "phev_target_2030_k": 450,
        "avg_operating_margin": 11.8,
        "battery_cost_2030": 95.0,
        "solid_state_commercialized": 2028,
    },
    "Accelerated: Solid-State & Tech Leapfrog": {
        "description": (
            "Early commercial mass-production of Solid-State Batteries in 2027 paired with Arene OS software "
            "accelerates BEV volume to 2.8M units by 2030. Accumulated hybrid cash flows fully self-fund "
            "massive capital expenditures and gigafactories without debt dilution."
        ),
        "hev_growth_rate": 0.01,
        "bev_target_2030_k": 2800,
        "phev_target_2030_k": 300,
        "avg_operating_margin": 9.4,
        "battery_cost_2030": 70.0,
        "solid_state_commercialized": 2026,
    },
}


def simulate_toyota_forecast(
    scenario_name: str = "Base: Pragmatic Multi-Pathway",
    custom_hev_2030_k: int | None = None,
    custom_bev_2030_k: int | None = None,
    battery_pack_cost_usd_kwh: float = 85.0,
    hev_margin_premium_pct: float = 2.5,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Simulate Toyota's 2024-2030 sales volume, powertrain mix, and financials.

    Returns:
        yearly_df: DataFrame containing yearly projections (2024-2030).
        summary_kpis: Dictionary containing high-level 2030 milestone KPIs.
    """
    preset = SCENARIOS.get(scenario_name, SCENARIOS["Base: Pragmatic Multi-Pathway"])
    years = np.arange(2024, 2031)

    # 2024 Base Figures (Toyota Official Actuals in thousands)
    base_hev = 4160
    base_phev = 158
    base_bev = 141
    base_fcev = 2
    base_revenue = 318.0  # USD Billion
    base_op_profit = 37.8  # USD Billion (approx ~¥5.35T at 142 JPY/USD)

    target_hev = custom_hev_2030_k if custom_hev_2030_k else (
        5200 if "Base" in scenario_name else (6200 if "Bull" in scenario_name else 4400)
    )
    target_bev = custom_bev_2030_k if custom_bev_2030_k else preset["bev_target_2030_k"]
    target_phev = preset["phev_target_2030_k"]

    # Smooth S-curve / linear interpolation
    hev_series = np.linspace(base_hev, target_hev, len(years))
    bev_series = np.geomspace(max(base_bev, 50), target_bev, len(years))
    phev_series = np.linspace(base_phev, target_phev, len(years))
    fcev_series = np.linspace(base_fcev, 5, len(years))

    records = []
    for i, yr in enumerate(years):
        hev_vol = int(round(hev_series[i]))
        bev_vol = int(round(bev_series[i]))
        phev_vol = int(round(phev_series[i]))
        fcev_vol = int(round(fcev_series[i]))
        electrified_total = hev_vol + bev_vol + phev_vol + fcev_vol

        # Assumed total Toyota global volume moves from 10.3M in 2024 to ~11.0M in 2030
        total_vehicle_volume = int(10300 + (yr - 2024) * 116)
        ice_volume = max(0, total_vehicle_volume - electrified_total)

        # Revenue and Profit Dynamics
        # ASP estimated at $31,500 base, with BEVs higher but margins driven by HEV
        revenue_usd_b = round(base_revenue * (1 + 0.03 * (yr - 2024)), 1)
        
        # Margin formula: Base margin + HEV contribution - BEV margin dilution (buffered by battery cost decline)
        bev_share = bev_vol / total_vehicle_volume
        hev_share = hev_vol / total_vehicle_volume
        
        cost_savings_factor = max(0.0, (120.0 - battery_pack_cost_usd_kwh) / 100.0)
        margin_pct = round(
            preset["avg_operating_margin"]
            + (hev_share * hev_margin_premium_pct)
            - (bev_share * (4.0 - cost_savings_factor * 3.0)),
            2
        )
        op_profit_usd_b = round(revenue_usd_b * (margin_pct / 100), 1)

        # Battery Resource Consumption (GWh)
        # Average battery capacity: HEV = 1.3 kWh, PHEV = 15 kWh, BEV = 75 kWh
        battery_gwh_hev = round(hev_vol * 1.3 / 1000, 2)
        battery_gwh_bev = round(bev_vol * 75.0 / 1000, 2)
        battery_gwh_phev = round(phev_vol * 15.0 / 1000, 2)
        total_battery_gwh = round(battery_gwh_hev + battery_gwh_bev + battery_gwh_phev, 2)

        # Cumulative CO2 fleet emission reduction efficiency (Index relative to 2024 = 100)
        # HEV reduces ~30% CO2 vs ICE, BEV reduces ~70% on grid mix
        co2_avoided_index = round(
            100 + (hev_vol * 0.3 + phev_vol * 0.5 + bev_vol * 0.7) / (base_hev * 0.3 + base_bev * 0.7) * 20,
            1
        )

        records.append({
            "year": int(yr),
            "total_volume_k": total_vehicle_volume,
            "hev_units_k": hev_vol,
            "bev_units_k": bev_vol,
            "phev_units_k": phev_vol,
            "fcev_units_k": fcev_vol,
            "ice_units_k": ice_volume,
            "electrified_total_k": electrified_total,
            "electrified_share_pct": round(electrified_total / total_vehicle_volume * 100, 1),
            "bev_share_pct": round(bev_vol / total_vehicle_volume * 100, 1),
            "hev_share_pct": round(hev_vol / total_vehicle_volume * 100, 1),
            "revenue_usd_b": revenue_usd_b,
            "operating_margin_pct": margin_pct,
            "operating_profit_usd_b": op_profit_usd_b,
            "total_battery_gwh": total_battery_gwh,
            "battery_gwh_bev": battery_gwh_bev,
            "battery_gwh_hev": battery_gwh_hev,
            "co2_abatement_index": co2_avoided_index,
        })

    df = pd.DataFrame(records)

    last_row = df.iloc[-1]
    cumulative_profit = df["operating_profit_usd_b"].sum()

    summary_kpis = {
        "scenario_name": scenario_name,
        "2030_electrified_volume": f"{last_row['electrified_total_k']:,}k ({last_row['electrified_share_pct']}%)",
        "2030_hev_volume": f"{last_row['hev_units_k']:,}k units",
        "2030_bev_volume": f"{last_row['bev_units_k']:,}k units",
        "2030_operating_margin": f"{last_row['operating_margin_pct']:.1f}%",
        "2030_operating_profit": f"${last_row['operating_profit_usd_b']}B",
        "2024_2030_cumulative_profit": f"${cumulative_profit:.1f}B",
        "2030_total_battery_demand_gwh": f"{last_row['total_battery_gwh']} GWh",
    }

    return df, summary_kpis
