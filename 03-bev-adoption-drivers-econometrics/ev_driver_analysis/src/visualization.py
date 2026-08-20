"""
visualization.py - Plotly Visualizers for Dashboard (Dark Theme)
Contains functions for correlation heatmaps, panel trend charts, IRF curves, and SHAP plots.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

COLOR_PALETTE = {
    "primary": "#3B82F6",
    "secondary": "#10B981",
    "accent": "#F59E0B",
    "danger": "#EF4444",
    "purple": "#8B5CF6",
    "cyan": "#06B6D4",
    "dark_bg": "#0F172A",
    "paper_bg": "#1E293B"
}

# OEM Designated Brand Color Palette
OEM_COLORS = {
    "BYD": "#E11D48",                 # Vivid Red (Global #1 BEV Volume)
    "Tesla": "#7C3AED",               # Electric Violet (Global #2 Dedicated Platform)
    "Volkswagen Group": "#00A8A8",     # Teal / Cyan (Legacy Leader ID/Audi/Porsche)
    "Hyundai-Kia Group": "#1D4ED8",   # Deep Blue (E-GMP 800V Ultra-Fast Charging)
    "BMW Group": "#475569",           # Dark Slate / Black (Premium Luxury Leader)
    "Mercedes-Benz Group": "#94A3B8", # Metallic Silver (Flagship Luxury EQ)
    "Toyota": "#FB923C"               # Light Orange (Hybrid Leader / Gradual Shift)
}

OEM_LABELS = {
    "BYD": "BYD",
    "Tesla": "Tesla Inc.",
    "Volkswagen Group": "Volkswagen Group",
    "Hyundai-Kia Group": "Hyundai-Kia Group",
    "BMW Group": "BMW Group",
    "Mercedes-Benz Group": "Mercedes-Benz Group",
    "Toyota": "Toyota"
}

# Region Designated Colors: CN=Red, EU=Green, US=Blue
REGION_COLORS = {
    "CN": "#EF4444",  # China (Vivid Red)
    "EU": "#10B981",  # Europe (Vivid Green)
    "US": "#3B82F6"   # United States (Vivid Blue)
}

REGION_LABELS = {
    "CN": "China (CN)",
    "EU": "Europe (EU)",
    "US": "United States (US)"
}

# Professional Business English Variable Labels (Zero Underscores)
DRIVER_LABELS = {
    "battery_pack_price_usd_kwh": "Battery Pack Price (USD/kWh)",
    "lithium_carbonate_price_usd_ton": "Lithium Carbonate Price (USD/ton)",
    "lithium_carbonate_usd_ton": "Lithium Carbonate Price (USD/ton)",
    "nickel_price_usd_ton": "Nickel Commodity Price (USD/ton)",
    "cobalt_price_usd_ton": "Cobalt Commodity Price (USD/ton)",
    "wti_oil_price_usd": "WTI Crude Oil Price (USD/bbl)",
    "residential_electricity_price_usd_kwh": "Residential Electricity Price (USD/kWh)",
    "interest_rate_pct": "Central Bank Policy Rate (%)",
    "used_ev_depreciation_rate_pct": "Used EV Annual Depreciation Rate (%)",
    "semiconductor_lead_time_weeks": "Semiconductor Lead Time (Weeks)",
    "public_chargers_per_million_capita": "Public Chargers Density (Units/M Capita)",
    "log_public_chargers": "Public Chargers Density (Natural Log)",
    "fast_chargers_ratio": "DC Fast Charger Share (%)",
    "applied_tariff_rate_pct": "Applied Tariff Rate on Imports (%)",
    "subsidy_intensity_ratio": "EV Purchase Subsidy Intensity Ratio",
    "cpi_index": "Consumer Price Index (CPI)",
    "gdp_growth_index": "Real GDP Growth Index",
    "average_msrp_usd": "Average Vehicle MSRP (USD)",
    "bev_lineup_count": "Dedicated BEV Lineup Count",
    "lfp_battery_mix_pct": "LFP Battery Adoption Mix (%)",
    "us_ira_feoc_dummy": "US IRA FEOC Exclusion Policy Dummy",
    "eu_co2_target_tightening_dummy": "EU Fleet CO2 Target Tightening Dummy",
    "cn_trade_in_scheme_dummy": "China Trade-In Incentive Policy Dummy",
    "company_Tesla": "OEM Fixed Effect: Tesla",
    "company_BYD": "OEM Fixed Effect: BYD",
    "company_Volkswagen Group": "OEM Fixed Effect: Volkswagen Group",
    "company_Hyundai-Kia Group": "OEM Fixed Effect: Hyundai-Kia Group",
    "company_BMW Group": "OEM Fixed Effect: BMW Group",
    "company_Mercedes-Benz Group": "OEM Fixed Effect: Mercedes-Benz Group",
    "company_Toyota": "OEM Fixed Effect: Toyota",
    "region_US": "Regional Fixed Effect: United States (US)",
    "region_EU": "Regional Fixed Effect: Europe (EU)",
    "region_CN": "Regional Fixed Effect: China (CN)"
}

def clean_label(key: str) -> str:
    """Returns elegant English label without any underscores."""
    if key in DRIVER_LABELS:
        return DRIVER_LABELS[key]
    return key.replace("_", " ").title()

def plot_bev_sales_trends(df: pd.DataFrame, group_by: str = "region") -> go.Figure:
    agg = df.groupby(["date", group_by])["bev_sales"].sum().reset_index()
    group_name = "Region" if group_by == "region" else "Automaker (OEM)"
    
    if group_by == "company":
        fig = px.line(
            agg, x="date", y="bev_sales", color="company",
            color_discrete_map=OEM_COLORS,
            title=f"<b>Monthly BEV Sales Trends by {group_name} (2020–2025)</b>",
            labels={"date": "Date", "bev_sales": "Monthly BEV Sales (Units)", "company": "Company"},
            template="plotly_dark"
        )
    else:
        fig = px.line(
            agg, x="date", y="bev_sales", color="region",
            color_discrete_map=REGION_COLORS,
            title=f"<b>Monthly BEV Sales Trends by {group_name} (2020–2025)</b>",
            labels={"date": "Date", "bev_sales": "Monthly BEV Sales (Units)", "region": "Region"},
            template="plotly_dark"
        )
        
    fig.update_layout(
        paper_bgcolor=COLOR_PALETTE["paper_bg"],
        plot_bgcolor=COLOR_PALETTE["dark_bg"],
        height=450,
        hovermode="x unified",
        margin=dict(l=50, r=40, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig
        
    fig.update_layout(
        paper_bgcolor=COLOR_PALETTE["paper_bg"],
        plot_bgcolor=COLOR_PALETTE["dark_bg"],
        height=450,
        hovermode="x unified",
        margin=dict(l=50, r=40, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def plot_lag_heatmap(corr_df: pd.DataFrame) -> go.Figure:
    """
    Renders correlation heatmap where:
    - Positive (+) is Blue (Darker blue = higher positive)
    - Zero (0.0) is Dark Charcoal Neutral
    - Negative (-) is Red (Darker red = stronger negative)
    """
    cols = ["lag_0", "lag_1", "lag_3", "lag_6"]
    x_labels = ["Lag 0 (Same Month)", "Lag 1 (1M Lag)", "Lag 3 (3M Lag)", "Lag 6 (6M Lag)"]
    
    y_labels = [DRIVER_LABELS.get(d, d) for d in corr_df["driver"]]
    z_values = corr_df[cols].values
    
    text_values = []
    for row in z_values:
        row_text = []
        for val in row:
            if np.isnan(val):
                row_text.append("-")
            else:
                prefix = "+" if val > 0 else ""
                row_text.append(f"{prefix}{val:.2f}")
        text_values.append(row_text)

    custom_colorscale = [
        [0.0, "#DC2626"],   # -0.8 Strong Negative (Vivid Red)
        [0.25, "#881337"],  # -0.4 Weak Negative (Dark Rose)
        [0.5, "#0F172A"],   #  0.0 Neutral Zero (Dark Charcoal)
        [0.75, "#1E40AF"],  # +0.4 Weak Positive (Soft Blue)
        [1.0, "#2563EB"]    # +0.8 Strong Positive (Vivid Blue)
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=z_values,
            x=x_labels,
            y=y_labels,
            text=text_values,
            texttemplate="<b>%{text}</b>",
            textfont=dict(size=14, color="#FFFFFF", family="Arial Black, sans-serif"),
            colorscale=custom_colorscale,
            zmin=-0.8,
            zmax=0.8,
            xgap=3,
            ygap=3,
            colorbar=dict(
                title=dict(text="Correlation (r)", side="right"),
                tickvals=[-0.8, -0.4, 0, 0.4, 0.8],
                ticktext=["-0.8 (Strong Negative: Red)", "-0.4", "0.0 (Neutral)", "+0.4", "+0.8 (Strong Positive: Blue)"]
            )
        )
    )
    
    fig.update_layout(
        title="<b>Lag Cross-Correlation Matrix with Monthly BEV Sales</b>",
        template="plotly_dark",
        paper_bgcolor=COLOR_PALETTE["paper_bg"],
        plot_bgcolor=COLOR_PALETTE["dark_bg"],
        height=520,
        margin=dict(l=240, r=40, t=60, b=50),
        xaxis=dict(tickfont=dict(size=12, color="#F8FAFC"), side="bottom"),
        yaxis=dict(tickfont=dict(size=12, color="#F8FAFC"), autorange="reversed")
    )
    return fig

def plot_dual_axis_trend(df: pd.DataFrame, selected_driver: str) -> go.Figure:
    """
    Renders dual-axis time-series: BEV Sales (Left) vs. Selected Driver Metric (Right).
    """
    agg = df.groupby("date").agg({
        "bev_sales": "sum",
        selected_driver: "mean"
    }).reset_index()

    driver_name = DRIVER_LABELS.get(selected_driver, selected_driver)

    fig = go.Figure()

    # Trace 1: Monthly BEV Sales (Bar)
    fig.add_trace(go.Bar(
        x=agg["date"],
        y=agg["bev_sales"],
        name="Monthly BEV Sales (Left Axis)",
        marker_color="rgba(59, 130, 246, 0.75)",
        yaxis="y"
    ))

    # Trace 2: Selected Driver Variable (Line)
    fig.add_trace(go.Scatter(
        x=agg["date"],
        y=agg[selected_driver],
        name=f"{driver_name} (Right Axis)",
        line=dict(color="#F59E0B", width=3.5),
        mode="lines+markers",
        marker=dict(size=6, color="#F59E0B"),
        yaxis="y2"
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLOR_PALETTE["paper_bg"],
        plot_bgcolor=COLOR_PALETTE["dark_bg"],
        height=450,
        hovermode="x unified",
        margin=dict(l=60, r=60, t=40, b=40),
        yaxis=dict(
            title=dict(text="BEV Sales (Units)", font=dict(color="#3B82F6")),
            tickfont=dict(color="#3B82F6"),
            side="left"
        ),
        yaxis2=dict(
            title=dict(text=driver_name, font=dict(color="#F59E0B")),
            tickfont=dict(color="#F59E0B"),
            overlaying="y",
            side="right"
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def plot_driver_scatter(df: pd.DataFrame, selected_driver: str) -> go.Figure:
    """
    Renders scatter plot cleanly colored by Region (CN=Red, EU=Green, US=Blue)
    without any overlapping titles or messy legends.
    """
    driver_name = DRIVER_LABELS.get(selected_driver, selected_driver)
    clean_df = df.dropna(subset=[selected_driver, "bev_sales"]).copy()
    clean_df["region_label"] = clean_df["region"].map(lambda r: REGION_LABELS.get(r, r))
    
    fig = px.scatter(
        clean_df,
        x=selected_driver,
        y="bev_sales",
        color="region",
        color_discrete_map=REGION_COLORS,
        hover_data=["date", "company", "region"],
        labels={
            selected_driver: driver_name,
            "bev_sales": "Monthly BEV Sales (Units)",
            "region": "Region"
        },
        template="plotly_dark"
    )

    fig.update_traces(
        marker=dict(size=7.5, opacity=0.8, line=dict(width=0.5, color="#FFFFFF"))
    )

    # Add OLS regression trendline
    if len(clean_df) > 2:
        x_vals = clean_df[selected_driver].values
        y_vals = clean_df["bev_sales"].values
        slope, intercept = np.polyfit(x_vals, y_vals, 1)
        x_trend = np.linspace(x_vals.min(), x_vals.max(), 100)
        y_trend = slope * x_trend + intercept
        
        fig.add_trace(go.Scatter(
            x=x_trend,
            y=y_trend,
            mode="lines",
            name="OLS Linear Trendline",
            line=dict(color="#FBBF24", width=3, dash="dash")
        ))

    fig.update_layout(
        paper_bgcolor=COLOR_PALETTE["paper_bg"],
        plot_bgcolor=COLOR_PALETTE["dark_bg"],
        height=450,
        margin=dict(l=60, r=40, t=40, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(15, 23, 42, 0.9)",
            bordercolor="#334155",
            borderwidth=1,
            font=dict(size=12, color="#F8FAFC")
        )
    )
    return fig

def plot_driver_distribution(df: pd.DataFrame, selected_driver: str) -> go.Figure:
    """
    Renders boxplot distribution colored by region (CN=Red, EU=Green, US=Blue).
    """
    df_box = df.copy()
    df_box["year"] = pd.to_datetime(df_box["date"]).dt.year.astype(str)
    driver_name = DRIVER_LABELS.get(selected_driver, selected_driver)
    
    fig = px.box(
        df_box,
        x="year",
        y=selected_driver,
        color="region",
        color_discrete_map=REGION_COLORS,
        labels={
            "year": "Year",
            selected_driver: driver_name,
            "region": "Region"
        },
        template="plotly_dark"
    )
    fig.update_layout(
        paper_bgcolor=COLOR_PALETTE["paper_bg"],
        plot_bgcolor=COLOR_PALETTE["dark_bg"],
        height=450,
        margin=dict(l=50, r=50, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def plot_irf_curves(irf_df: pd.DataFrame) -> go.Figure:
    irf_renamed = irf_df.copy()
    irf_renamed["impulse_name"] = irf_renamed["impulse_variable"].map(clean_label)
    fig = px.line(
        irf_renamed, x="month", y="response_bev_sales", color="impulse_name",
        title="<b>Vector Autoregression (VAR): 12-Month Impulse Response Functions</b>",
        labels={"month": "Months Elapsed Since Shock", "response_bev_sales": "BEV Sales Response (Std Shock)", "impulse_name": "Shock Driver Variable"},
        template="plotly_dark"
    )
    fig.update_layout(
        paper_bgcolor=COLOR_PALETTE["paper_bg"],
        plot_bgcolor=COLOR_PALETTE["dark_bg"],
        height=450,
        margin=dict(l=50, r=50, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def plot_shap_importance(importance_df: pd.DataFrame) -> go.Figure:
    top_15 = importance_df.head(15).sort_values(by="importance", ascending=True).copy()
    top_15["feature_label"] = top_15["feature"].map(clean_label)
    fig = px.bar(
        top_15, x="importance", y="feature_label", orientation="h",
        title="<b>XGBoost SHAP Global Feature Importance (|Mean SHAP Value|)</b>",
        labels={"importance": "Mean Absolute SHAP Value", "feature_label": "Key Adoption Driver"},
        template="plotly_dark",
        color="importance",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(
        paper_bgcolor=COLOR_PALETTE["paper_bg"],
        plot_bgcolor=COLOR_PALETTE["dark_bg"],
        height=480,
        margin=dict(l=260, r=40, t=60, b=40)
    )
    return fig

