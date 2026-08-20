"""Toyota Multi-Pathway vs BEV Strategy: Executive Strategic Intelligence Suite.

An institutional-grade interactive dashboard demonstrating the empirical validation
of Toyota's hybrid-centric multi-pathway strategy and 2026-2030 predictive forecasts.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Setup Root Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.clean_data import run_pipeline
from src.forecast import SCENARIOS, simulate_toyota_forecast
from src.load_data import load_all_processed, load_raw

# ---------------------------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Toyota Multi-Pathway Strategy Intelligence",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Institutional / Consulting-Grade Look
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #111827;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    .kpi-card {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 1.1rem 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #6B7280;
        margin-bottom: 0.35rem;
    }
    .kpi-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #111827;
        letter-spacing: -0.02em;
    }
    .kpi-delta {
        font-size: 0.85rem;
        font-weight: 500;
        color: #059669;
        margin-top: 0.2rem;
    }
    .strategy-callout {
        background-color: #F0FDF4;
        border-left: 4px solid #16A34A;
        padding: 1rem 1.2rem;
        border-radius: 4px;
        margin: 1rem 0;
        font-size: 0.95rem;
        color: #166534;
        line-height: 1.5;
    }
    .quote-box {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 1rem 1.2rem;
        border-radius: 4px;
        margin: 1rem 0;
        font-size: 0.95rem;
        color: #1E3A8A;
        line-height: 1.5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Data Loading & Initialization
# ---------------------------------------------------------------------------

processed_dir = ROOT / "data" / "processed"
if not (processed_dir / "toyota_mix_clean.csv").exists():
    with st.spinner("Initializing verified official data pipeline..."):
        run_pipeline()

data = load_all_processed()
raw_investments = load_raw("ev_investments")
raw_materials = load_raw("battery_material_prices")
raw_tariffs = load_raw("tariff_events")

# Color Palettes
COLOR_MAP = {
    "HEV": "#2563EB",       # Royal Blue
    "PHEV": "#0D9488",      # Teal
    "BEV": "#DC2626",       # Crimson Red
    "FCEV": "#D97706",      # Amber
    "ICE": "#9CA3AF",       # Slate Gray
}

# ---------------------------------------------------------------------------
# Header & Executive Summary Cards
# ---------------------------------------------------------------------------

st.markdown('<div class="main-title">🚘 Toyota Multi-Pathway Strategy Intelligence</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">'
    'Empirical validation of Toyota’s hybrid-first electrification strategy, battery resource economics, '
    'and dedicated 2026–2030 predictive scenarios based on official corporate & IEA datasets.'
    '</div>',
    unsafe_allow_html=True,
)

# Top KPI Summary Row
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-label">2024 Global HEV Volume</div>
            <div class="kpi-value">4.16M <span style="font-size:1.1rem; color:#6B7280;">units</span></div>
            <div class="kpi-delta">▲ +21.6% YoY (91.8% of Electrified Mix)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-label">FY2024 Operating Margin</div>
            <div class="kpi-value">11.9%</div>
            <div class="kpi-delta">▲ Record ¥5.35T Operating Profit</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-label">Battery Resource Efficiency</div>
            <div class="kpi-value">1 : 6 : 90</div>
            <div class="kpi-delta">1 BEV = 6 PHEVs = 90 HEVs in Critical Minerals</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Navigation Tabs
# ---------------------------------------------------------------------------

tab_proof, tab_macro, tab_battery, tab_forecast, tab_takeaways = st.tabs([
    "🏆 1. Strategic Proof (Toyota Playbook)",
    "🌐 2. Macro Reality & Infrastructure",
    "🔋 3. Battery Economics (1:6:90 Rule)",
    "🔮 4. Toyota 2026–2030 Forecast Simulator",
    "📜 5. Executive Strategic Takeaways",
])

# ===========================================================================
# TAB 1: Strategic Proof
# ===========================================================================

with tab_proof:
    st.header("Empirical Proof: Toyota's Pragmatic Triumph")
    st.markdown(
        """
        While competitors and capital markets aggressively pivoted all-in on dedicated Battery Electric Vehicles (BEV) between 2021 and 2023, 
        Toyota remained committed to its **"Multi-Pathway" principle aligned with customer choice and real-world regional infrastructure maturity**.
        Consequently, Toyota achieved **4.16 million HEV deliveries and record automotive operating profit (¥5.35T / 11.9% margin)**, 
        empirically validating the commercial wisdom of its strategic pragmatism.
        """
    )

    mix = data["toyota_mix"]

    # Region selection with Global as the clear default
    region_order = ["Global", "North America", "Europe", "Asia"]
    region_labels = {
        "Global": "🌍 Global Total",
        "North America": "🇺🇸 North America",
        "Europe": "🇪🇺 Europe",
        "Asia": "🌏 Asia",
    }

    selected_region = st.radio(
        "📍 Select Geographic Region:",
        options=region_order,
        index=0,  # Default to Global
        format_func=lambda r: region_labels.get(r, r),
        horizontal=True,
    )

    c1, c2 = st.columns([2, 1])

    with c1:
        subset = mix[mix["region"] == selected_region]

        fig_mix = px.bar(
            subset,
            x="year",
            y="units",
            color="powertrain",
            color_discrete_map=COLOR_MAP,
            title=f"Toyota & Lexus Electrified Sales Breakdown — {region_labels.get(selected_region, selected_region)} (2019–2025)",
            labels={"units": "Units (Thousands)", "year": "Year", "powertrain": "Powertrain"},
            barmode="stack",
            text="units",
        )
        fig_mix.update_traces(texttemplate="%{text:,.0f}k", textposition="inside")
        fig_mix.update_layout(
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#F3F4F6", title="Electrified Sales Volume (Thousands)"),
        )
        st.plotly_chart(fig_mix, width="stretch")

    with c2:
        st.subheader("Powertrain Share Matrix (%)")
        pivot_share = subset.pivot_table(
            index="year", columns="powertrain", values="share_within_region", fill_value=0
        )
        st.dataframe(
            pivot_share.style.format("{:.1f}%").background_gradient(cmap="Blues", subset=["HEV"]),
            width="stretch",
            height=280,
        )

        hev_2024_share = pivot_share.loc[2024, "HEV"] if 2024 in pivot_share.index and "HEV" in pivot_share.columns else 0.0
        st.markdown(
            f"""
            <div class="strategy-callout">
            <b>{region_labels.get(selected_region, selected_region)} Strategic Analysis:</b><br>
            In 2024, Full Hybrids (HEV) accounted for <b>{hev_2024_share:.1f}%</b> of Toyota's total electrified sales in <b>{selected_region}</b>.
            Even amidst infrastructure deficits and mineral price spikes, HEVs delivered immediate carbon abatement while generating superior corporate profitability.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Multi-Region 2024 Comparison Overview
    with st.expander("🌐 2024 Global vs Regional Electrified Portfolio Breakdown", expanded=False):
        mix_2024 = mix[mix["year"] == 2024].copy()
        fig_comp = px.bar(
            mix_2024,
            x="region",
            y="units",
            color="powertrain",
            color_discrete_map=COLOR_MAP,
            barmode="group",
            title="2024 Toyota Electrified Sales by Region & Powertrain (Thousands)",
            labels={"units": "Sales Units (k)", "region": "Region", "powertrain": "Powertrain"},
            text="units",
        )
        fig_comp.update_traces(texttemplate="%{text:,.0f}k", textposition="outside")
        fig_comp.update_layout(plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(showgrid=True, gridcolor="#F3F4F6"))
        st.plotly_chart(fig_comp, width="stretch")

    # Financial Correlation
    st.subheader("Financial Strength & R&D Self-Funding Ability")
    fin = data["financials"]
    
    col_fin1, col_fin2 = st.columns(2)
    
    with col_fin1:
        fig_fin = go.Figure()
        fig_fin.add_trace(
            go.Bar(
                x=fin["year"],
                y=fin["revenue_usd_b"],
                name="Revenue (USD B)",
                marker_color="#94A3B8",
                opacity=0.7,
            )
        )
        fig_fin.add_trace(
            go.Scatter(
                x=fin["year"],
                y=fin["operating_margin_pct"],
                name="Operating Margin (%)",
                yaxis="y2",
                line=dict(color="#16A34A", width=3),
                mode="lines+markers",
            )
        )
        fig_fin.update_layout(
            title="Toyota Revenue vs Operating Margin (%)",
            yaxis=dict(title="Revenue (USD Billion)", showgrid=False),
            yaxis2=dict(
                title="Operating Margin (%)",
                overlaying="y",
                side="right",
                showgrid=False,
                ticksuffix="%",
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_fin, width="stretch")

    with col_fin2:
        fig_rd = go.Figure()
        fig_rd.add_trace(
            go.Scatter(
                x=fin["year"],
                y=fin["rd_spend_usd_b"],
                name="R&D Spend (USD B)",
                line=dict(color="#2563EB", width=2.5),
                mode="lines+markers",
            )
        )
        fig_rd.add_trace(
            go.Scatter(
                x=fin["year"],
                y=fin["ev_capex_usd_b"],
                name="EV/Battery CAPEX (USD B)",
                line=dict(color="#DC2626", width=2.5, dash="dash"),
                mode="lines+markers",
            )
        )
        fig_rd.update_layout(
            title="Toyota Annual R&D & EV CAPEX Scaling (USD Billion)",
            yaxis=dict(title="USD Billion", showgrid=True, gridcolor="#F3F4F6"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_rd, width="stretch")


# ===========================================================================
# TAB 2: Macro Environment & Infrastructure
# ===========================================================================

with tab_macro:
    st.header("Macro Constraints: Battery Mineral Volatility & Charging Gaps")
    st.markdown(
        """
        The aggressive global transition to pure electric vehicles collided with two structural macro bottlenecks: **extreme battery commodity supply chain volatility** and **severe regional charging infrastructure deficits**.
        Toyota's hybrid-centric strategy served as an effective macroeconomic shock absorber.
        """
    )

    c_m1, c_m2 = st.columns(2)

    with c_m1:
        st.subheader("Battery Critical Mineral Price Volatility (2020–2025)")
        mat_df = raw_materials.copy()
        fig_mat = px.line(
            mat_df,
            x="year",
            y="price_usd_per_unit",
            color="material",
            markers=True,
            title="Material Spot Prices (USD / Metric Ton)",
            labels={"price_usd_per_unit": "USD / Ton", "year": "Year", "material": "Mineral"},
        )
        fig_mat.update_layout(
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(showgrid=True, gridcolor="#F3F4F6"),
        )
        st.plotly_chart(fig_mat, width="stretch")

        st.caption("Source: London Metal Exchange (LME) & Fastmarkets Benchmark Assessments.")

    with c_m2:
        st.subheader("IEA Official Charging Infrastructure Density")
        risk_df = data["risk_summary"].sort_values("chargers_per_million", ascending=False)
        fig_infra = px.bar(
            risk_df,
            x="region",
            y="chargers_per_million",
            color="region",
            color_discrete_sequence=["#3B82F6", "#10B981", "#F59E0B"],
            title="Public Chargers per Million Inhabitants (2024/2025 IEA)",
            labels={"chargers_per_million": "Public Chargers / Million Pop", "region": "Region"},
            text="chargers_per_million",
        )
        fig_infra.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig_infra.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            yaxis=dict(showgrid=True, gridcolor="#F3F4F6"),
        )
        st.plotly_chart(fig_infra, width="stretch")

        st.caption("Source: IEA Global EV Outlook 2024 (China 3.5M+, Europe 1M+, North America 220k+ public chargers).")

    st.markdown(
        """
        <div class="quote-box">
        <b>Strategic Macro Insight:</b><br>
        When battery-grade Lithium Carbonate spiked to $78,000/ton in 2022, large 75 kWh BEV packs imposed immense bill-of-materials inflation, 
        triggering severe division losses and price hikes across pure EV makers. In contrast, Toyota's small 1.3 kWh HEV packs insulated operating margins 
        from raw material price shocks while preserving robust consumer affordability.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===========================================================================
# TAB 3: Battery Economics (1:6:90 Principle)
# ===========================================================================

with tab_battery:
    st.header("The 1:6:90 Principle: Battery Resource Optimization")
    st.markdown(
        """
        A cornerstone of Toyota's engineering philosophy is **"maximizing global fleet carbon abatement under constrained battery mineral resources."**
        The raw battery minerals required for a single 75 kWh pure electric vehicle (BEV) can manufacture **6 Plug-in Hybrids (PHEV)** or **90 Full Hybrids (HEV)**.
        """
    )

    c_b1, c_b2 = st.columns([1, 1])

    with c_b1:
        st.subheader("Vehicle Production per 75 kWh Battery Pack")
        equiv_data = pd.DataFrame({
            "Vehicle Type": ["BEV (Pure Electric)", "PHEV (Plug-in Hybrid)", "HEV (Full Hybrid)"],
            "Battery Capacity (kWh)": [75.0, 15.0, 1.3],
            "Units Produced per 75kWh": [1, 6, 90],
            "Fleet CO2 Reduction Effect (kg/yr)": [3200, 13200, 43200],
        })

        fig_equiv = px.bar(
            equiv_data,
            x="Vehicle Type",
            y="Units Produced per 75kWh",
            color="Vehicle Type",
            color_discrete_map={"BEV (Pure Electric)": "#DC2626", "PHEV (Plug-in Hybrid)": "#0D9488", "HEV (Full Hybrid)": "#2563EB"},
            text="Units Produced per 75kWh",
            title="Number of Vehicles Built from Single 75 kWh Battery Resource",
        )
        fig_equiv.update_traces(texttemplate="%{text} Units", textposition="outside")
        fig_equiv.update_layout(plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig_equiv, width="stretch")

    with c_b2:
        st.subheader("Total Fleet CO2 Emission Reduction (Relative)")
        fig_co2 = px.bar(
            equiv_data,
            x="Vehicle Type",
            y="Fleet CO2 Reduction Effect (kg/yr)",
            color="Vehicle Type",
            color_discrete_map={"BEV (Pure Electric)": "#DC2626", "PHEV (Plug-in Hybrid)": "#0D9488", "HEV (Full Hybrid)": "#2563EB"},
            text="Fleet CO2 Reduction Effect (kg/yr)",
            title="Annual Fleet-wide CO2 Abatement from Same Mineral Resource",
        )
        fig_co2.update_traces(texttemplate="%{text:,.0f} kg", textposition="outside")
        fig_co2.update_layout(plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig_co2, width="stretch")

    st.markdown(
        """
        <div class="strategy-callout">
        <b>Mathematical Proof:</b> While a single 75 kWh BEV reduces ~3.2 tons of CO2 per year, 
        90 Full Hybrids (HEVs) built from the exact same battery mineral resource achieve over 43.2 tons of cumulative annual CO2 abatement (a <b>13.5x higher carbon efficiency multiplier</b>).
        Under real-world supply chain and infrastructure bottlenecks, hybrid deployment offers the fastest, most scalable carbon reduction impact.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===========================================================================
# TAB 4: Toyota 2026-2030 Forecast Simulator
# ===========================================================================

with tab_forecast:
    st.header("🔮 Toyota Dedicated 2026–2030 Strategic Forecast Simulator")
    st.markdown(
        """
        This predictive simulation engine models **Toyota Motor Corporation's** powertrain mix trajectory, 
        profitability resilience, and next-generation battery/software roadmap (Solid-State Batteries & Arene OS).
        Select strategic scenario presets and fine-tune macro variables to simulate performance through 2030.
        """
    )

    # Simulator Controls Sidebar/Column
    with st.expander("⚙️ Simulation Settings & Scenario Assumptions", expanded=True):
        sc_col1, sc_col2 = st.columns([1.5, 2.5])
        
        with sc_col1:
            selected_scenario = st.selectbox(
                "Select Toyota Strategic Scenario",
                list(SCENARIOS.keys()),
                index=0,
            )
            st.info(SCENARIOS[selected_scenario]["description"])

        with sc_col2:
            st.markdown("<b>Fine-Tune Toyota Strategic Parameters:</b>", unsafe_allow_html=True)
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                custom_hev = st.slider(
                    "2030 Toyota HEV Target Volume (k units)",
                    min_value=3500,
                    max_value=7000,
                    value=5200 if "Base" in selected_scenario else (6200 if "Bull" in selected_scenario else 4400),
                    step=100,
                )
                battery_cost = st.slider(
                    "2030 Battery Pack Cost ($ / kWh)",
                    min_value=50.0,
                    max_value=140.0,
                    value=float(SCENARIOS[selected_scenario]["battery_cost_2030"]),
                    step=5.0,
                )
            with p_col2:
                custom_bev = st.slider(
                    "2030 Toyota BEV Target Volume (k units)",
                    min_value=500,
                    max_value=3500,
                    value=int(SCENARIOS[selected_scenario]["bev_target_2030_k"]),
                    step=100,
                )
                hev_margin = st.slider(
                    "HEV Operating Margin Premium (%)",
                    min_value=0.0,
                    max_value=5.0,
                    value=2.5,
                    step=0.5,
                )

    # Run Simulation
    sim_df, kpi_summary = simulate_toyota_forecast(
        scenario_name=selected_scenario,
        custom_hev_2030_k=custom_hev,
        custom_bev_2030_k=custom_bev,
        battery_pack_cost_usd_kwh=battery_cost,
        hev_margin_premium_pct=hev_margin,
    )

    # Display 2030 Result Cards
    st.subheader("2030 Projected Milestone KPIs")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("2030 Electrified Mix", kpi_summary["2030_electrified_volume"])
    with k2:
        st.metric("2030 Projected Margin", kpi_summary["2030_operating_margin"], f"{kpi_summary['2030_operating_profit']} Op. Profit")
    with k3:
        st.metric("2024-2030 Cum. Profit", kpi_summary["2024_2030_cumulative_profit"], "R&D Self-Funded")
    with k4:
        st.metric("2030 Battery Demand", kpi_summary["2030_total_battery_demand_gwh"])

    # Forecast Visualizations
    col_sim1, col_sim2 = st.columns(2)

    with col_sim1:
        st.subheader("Toyota Projected Powertrain Mix (2024–2030)")
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Bar(x=sim_df["year"], y=sim_df["ice_units_k"], name="ICE (Gasoline)", marker_color=COLOR_MAP["ICE"]))
        fig_vol.add_trace(go.Bar(x=sim_df["year"], y=sim_df["hev_units_k"], name="HEV (Hybrid)", marker_color=COLOR_MAP["HEV"]))
        fig_vol.add_trace(go.Bar(x=sim_df["year"], y=sim_df["phev_units_k"], name="PHEV", marker_color=COLOR_MAP["PHEV"]))
        fig_vol.add_trace(go.Bar(x=sim_df["year"], y=sim_df["bev_units_k"], name="BEV (Electric)", marker_color=COLOR_MAP["BEV"]))
        fig_vol.update_layout(
            barmode="stack",
            yaxis=dict(title="Global Sales Volume (Thousands)", showgrid=True, gridcolor="#F3F4F6"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_vol, width="stretch")

    with col_sim2:
        st.subheader("Toyota Projected Revenue & Operating Profit (USD B)")
        fig_prof = go.Figure()
        fig_prof.add_trace(go.Bar(x=sim_df["year"], y=sim_df["revenue_usd_b"], name="Revenue ($B)", marker_color="#CBD5E1"))
        fig_prof.add_trace(go.Scatter(x=sim_df["year"], y=sim_df["operating_profit_usd_b"], name="Operating Profit ($B)", yaxis="y2", line=dict(color="#059669", width=3), mode="lines+markers"))
        fig_prof.update_layout(
            yaxis=dict(title="Revenue (USD B)", showgrid=False),
            yaxis2=dict(title="Operating Profit (USD B)", overlaying="y", side="right", showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_prof, width="stretch")

    # Battery Demand vs Carbon Index
    st.subheader("Battery Capacity Demand (GWh) vs Cumulative Carbon Abatement Index")
    fig_bat = go.Figure()
    fig_bat.add_trace(go.Bar(x=sim_df["year"], y=sim_df["battery_gwh_bev"], name="BEV Battery Demand (GWh)", marker_color="#DC2626"))
    fig_bat.add_trace(go.Bar(x=sim_df["year"], y=sim_df["battery_gwh_hev"], name="HEV Battery Demand (GWh)", marker_color="#2563EB"))
    fig_bat.add_trace(go.Scatter(x=sim_df["year"], y=sim_df["co2_abatement_index"], name="CO2 Abatement Index (2024=100)", yaxis="y2", line=dict(color="#10B981", width=3, dash="dot"), mode="lines+markers"))
    fig_bat.update_layout(
        barmode="stack",
        yaxis=dict(title="Annual Battery Demand (GWh)", showgrid=True, gridcolor="#F3F4F6"),
        yaxis2=dict(title="Carbon Abatement Index", overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_bat, width="stretch")

    # Detailed Projections Table
    with st.expander("📋 View Detailed Simulation Projection Data"):
        display_df = sim_df[[
            "year", "total_volume_k", "hev_units_k", "bev_units_k", "electrified_share_pct",
            "revenue_usd_b", "operating_margin_pct", "operating_profit_usd_b", "total_battery_gwh"
        ]].copy()
        display_df.columns = [
            "Year", "Total Volume (k)", "HEV (k)", "BEV (k)", "Electrified Share (%)",
            "Revenue ($B)", "Margin (%)", "Op. Profit ($B)", "Battery (GWh)"
        ]
        st.dataframe(display_df.style.format({
            "Total Volume (k)": "{:,.0f}",
            "HEV (k)": "{:,.0f}",
            "BEV (k)": "{:,.0f}",
            "Electrified Share (%)": "{:.1f}%",
            "Revenue ($B)": "${:,.1f}",
            "Margin (%)": "{:.1f}%",
            "Op. Profit ($B)": "${:,.1f}",
            "Battery (GWh)": "{:,.1f}",
        }), width="stretch")


# ===========================================================================
# TAB 5: Executive Takeaways
# ===========================================================================

with tab_takeaways:
    st.header("Executive Summary: Strategic Lessons & Strategic Takeaways")
    
    st.markdown(
        """
        ### 📌 4 Decisive Strategic Takeaways (Toyota Electrification Thesis)
        
        1. **Validation of the Pragmatic Multi-Pathway Bridge**
           - During the global "EV Chasm", Toyota's hybrid-centric strategy avoided destructive price wars, 
             delivering **4.16M electrified vehicles and an all-time record 11.9% operating margin (¥5.35T Operating Profit)** in FY2024.
           
        2. **Capital Efficiency & Self-Funded R&D**
           - While pure-play and aggressive legacy EV divisions suffered multi-billion-dollar operating losses, 
             Toyota utilized its **massive annual operating cash flows (>¥5 Trillion)** to fully self-fund its North Carolina battery complex ($13.9B) and solid-state gigafactories without debt dilution.

        3. **Fleet Carbon Abatement Maximization (1:6:90 Principle)**
           - In a mineral-constrained environment, utilizing a single 75 kWh battery allocation to deploy 90 HEVs achieves 
             **13.5x greater fleet-wide annual CO2 abatement (~43.2 tons vs 3.2 tons)** compared to a single large-pack BEV.

        4. **Orderly High-Margin Leap to Solid-State Tech (2026–2030)**
           - With modular EV gigacasting rolling out in 2026 and commercial **Solid-State Battery commercialization slated for 2027–2028**, 
             Toyota has preserved balance sheet resilience to execute an orderly, profitable scale-up to 1.8M–2.8M dedicated BEVs by 2030.
        """
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #6B7280; font-size: 0.85rem;">
        <b>Toyota Hybrid vs BEV Strategy Intelligence Project</b> | Data-driven Portfolio for Strategic Analysis & Predictive Modeling<br>
        Verified Data Sources: Toyota Motor Corporation Global Newsroom, IEA Global EV Outlook, LME / Fastmarkets.
        </div>
        """,
        unsafe_allow_html=True,
    )