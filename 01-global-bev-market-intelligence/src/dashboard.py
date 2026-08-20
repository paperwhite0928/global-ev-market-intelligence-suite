import os
import json
import webbrowser
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. Configuration & Official Brand Color Palette (Pure BEV 6 Major Groups)
# ==============================================================================
COMPANY_COLORS = {
    "BYD": "#E11D48",                # Vivid Crimson Red (BYD Brand Identity)
    "Tesla Inc.": "#7C3AED",         # Electric Violet (Tesla Pioneer)
    "Volkswagen Group": "#00A8A8",    # Cyan / Teal (VW Electrified ID)
    "BMW Group": "#000000",          # Pure Obsidian Black (BMW Luxury)
    "Hyundai-Kia Group": "#00287A",   # Deep Indigo Blue (Hyundai-Kia E-GMP)
    "Mercedes-Benz Group": "#7F8C8D" # Silver / Metallic Slate (Mercedes-Benz EQ)
}

def apply_layout(fig, height=360, margin=None, showlegend=True, extra_xaxis=None, extra_yaxis=None):
    layout_dict = dict(
        autosize=True,
        font=dict(family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, sans-serif", size=12, color="#334155"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        showlegend=showlegend,
        margin=margin or dict(l=55, r=25, t=30, b=45),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="#e2e8f0",
            borderwidth=1,
            font=dict(size=11)
        ),
        hoverlabel=dict(
            bgcolor="#1e293b",
            font_size=12,
            font_color="#ffffff"
        )
    )
    fig.update_layout(**layout_dict)
    if extra_xaxis:
        fig.update_layout(xaxis=extra_xaxis)
    if extra_yaxis:
        fig.update_layout(yaxis=extra_yaxis)
    return fig

# ==============================================================================
# 2. Data Loading & Preprocessing
# ==============================================================================
base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(base_dir)
data_dir = os.path.join(project_dir, "data")

sales_path = os.path.join(data_dir, "ev_sales_by_company.csv")
market_path = os.path.join(data_dir, "global_bev_market.csv")
battery_path = os.path.join(data_dir, "battery_strategy.csv")

sales = pd.read_csv(sales_path)
market = pd.read_csv(market_path)
battery = pd.read_csv(battery_path)

sales.columns = sales.columns.str.strip()
market.columns = market.columns.str.strip()
battery.columns = battery.columns.str.strip()

# Global market YoY growth calculation
market = market.sort_values("year").reset_index(drop=True)
market["global_growth_rate"] = market["total_global_bev_sales"].pct_change() * 100
market["global_volume_diff"] = market["total_global_bev_sales"].diff()

# Merge sales with global market info
df = sales.merge(
    market[["year", "total_global_bev_sales", "global_passenger_car_market_share", "global_growth_rate", "global_volume_diff"]],
    on="year",
    how="left"
)

df = df.sort_values(["company", "year"]).reset_index(drop=True)

# Calculate metrics
df["market_share"] = (df["bev_sales"] / df["total_global_bev_sales"]) * 100
df["growth_rate"] = df.groupby("company")["bev_sales"].pct_change() * 100
df["volume_change"] = df.groupby("company")["bev_sales"].diff()

company_order = [
    "BYD",
    "Tesla Inc.",
    "Volkswagen Group",
    "Hyundai-Kia Group",
    "BMW Group",
    "Mercedes-Benz Group"
]

# 5-Year Cumulative Net Volume Expansion & Multiples (2020 -> 2025)
sales_2020 = df[df["year"] == 2020].set_index("company")["bev_sales"]
sales_2025 = df[df["year"] == 2025].set_index("company")["bev_sales"]

cum_growth_records = []
for comp in company_order:
    v20 = sales_2020.get(comp, 0)
    v25 = sales_2025.get(comp, 0)
    diff = v25 - v20
    mult = (v25 / v20) if v20 > 0 else 0
    rate = ((v25 - v20) / v20 * 100) if v20 > 0 else 0
    cum_growth_records.append({
        "company": comp,
        "sales_2020": v20,
        "sales_2025": v25,
        "volume_diff": diff,
        "multiple": mult,
        "cum_growth_rate": rate,
        "display_text": f" +{diff:,.0f} units ({mult:.1f}x)"
    })
cum_growth = pd.DataFrame(cum_growth_records).sort_values("volume_diff", ascending=True)

# ==============================================================================
# 3. Tab 1 - Chart 1: Global BEV Adoption Trend (Penetration %)
# ==============================================================================
fig_global = go.Figure()

fig_global.add_trace(go.Scatter(
    x=market["year"],
    y=market["global_passenger_car_market_share"],
    mode="lines+markers+text",
    name="Global BEV Penetration Rate (%)",
    line=dict(color="#2563eb", width=3.5, shape="spline"),
    marker=dict(size=9, color="#1d4ed8", symbol="circle", line=dict(color="#ffffff", width=2)),
    text=[f"<b>{val:.1f}%</b>" for val in market["global_passenger_car_market_share"]],
    textposition="top center",
    textfont=dict(size=12, color="#1e293b"),
    fill="tozeroy",
    fillcolor="rgba(37, 99, 235, 0.08)",
    hovertemplate="<b>Year %{x}</b><br>Global BEV Penetration: <b>%{y:.1f}%</b><extra></extra>"
))

apply_layout(
    fig_global,
    height=360,
    showlegend=False,
    margin=dict(l=50, r=25, t=30, b=45),
    extra_xaxis=dict(title="Year", tickmode="array", tickvals=[2020, 2021, 2022, 2023, 2024, 2025], range=[2019.6, 2025.4], gridcolor="#f1f5f9"),
    extra_yaxis=dict(title="Penetration Rate (%)", range=[0, 24], ticksuffix="%", gridcolor="#f1f5f9")
)

fig_global.add_annotation(
    x=2020, y=3.1,
    text="<b>2020: 3.1%</b> (Early Niche)",
    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.2, arrowcolor="#64748b",
    ax=45, ay=-35, font=dict(size=11, color="#475569"),
    bgcolor="#ffffff", bordercolor="#cbd5e1", borderwidth=1, borderpad=4
)
fig_global.add_annotation(
    x=2025, y=19.7,
    text="<b>2025: 19.7%</b> (1 in 5 New Cars)",
    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.2, arrowcolor="#2563eb",
    ax=-90, ay=-35, font=dict(size=11, color="#1e40af"),
    bgcolor="#eff6ff", bordercolor="#93c5fd", borderwidth=1, borderpad=4
)

# ==============================================================================
# 4. Tab 1 - Chart 2: Annual BEV Deliveries by OEM (2020–2025)
# ==============================================================================
fig_sales = px.line(
    df,
    x="year",
    y="bev_sales",
    color="company",
    markers=True,
    color_discrete_map=COMPANY_COLORS
)

fig_sales.update_traces(
    line=dict(width=2.8),
    marker=dict(size=7, line=dict(color="#ffffff", width=1.5)),
    hovertemplate="<b>%{data.name}</b><br>Year: %{x}<br>Deliveries: <b>%{y:,.0f} units</b><extra></extra>"
)

apply_layout(
    fig_sales,
    height=360,
    showlegend=True,
    margin=dict(l=65, r=25, t=35, b=45),
    extra_xaxis=dict(title="Year", tickmode="linear", dtick=1, gridcolor="#f1f5f9"),
    extra_yaxis=dict(title="Annual BEV Deliveries (Units)", tickformat=",.0f", gridcolor="#f1f5f9")
)

# ==============================================================================
# 5. Tab 1 - Chart 3: 2025 BEV Sales Volume Ranking Leaderboard
# ==============================================================================
ranking_2025 = df[df["year"] == 2025].sort_values("bev_sales", ascending=True).copy()

fig_ranking = px.bar(
    ranking_2025,
    x="bev_sales",
    y="company",
    color="company",
    color_discrete_map=COMPANY_COLORS,
    orientation="h",
    text="bev_sales"
)

fig_ranking.update_traces(
    texttemplate=" %{text:,.0f} units",
    textposition="outside",
    textfont=dict(size=11, color="#334155"),
    hovertemplate="<b>%{y}</b><br>2025 Deliveries: <b>%{x:,.0f} units</b><extra></extra>",
    marker=dict(line=dict(color="#ffffff", width=1))
)

apply_layout(
    fig_ranking,
    height=340,
    showlegend=False,
    margin=dict(l=145, r=65, t=15, b=40),
    extra_xaxis=dict(title="Annual Deliveries (Units)", tickformat=",.0f", gridcolor="#f1f5f9", range=[0, 2700000]),
    extra_yaxis=dict(title="", gridcolor="#f1f5f9")
)

# ==============================================================================
# 6. Tab 1 - Chart 4: 2025 Deliveries Share Donut Chart
# ==============================================================================
share_2025 = df[df["year"] == 2025].copy()

fig_pie = px.pie(
    share_2025,
    names="company",
    values="bev_sales",
    color="company",
    color_discrete_map=COMPANY_COLORS,
    hole=0.48
)

fig_pie.update_traces(
    textposition="inside",
    textinfo="percent+label",
    textfont=dict(size=11, color="#ffffff"),
    insidetextorientation="horizontal",
    marker=dict(line=dict(color="#ffffff", width=2)),
    hovertemplate="<b>%{label}</b><br>Deliveries: %{value:,.0f} units<br>Share of Top 6: <b>%{percent}</b><extra></extra>"
)

apply_layout(
    fig_pie,
    height=340,
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20)
)
fig_pie.update_layout(
    annotations=[dict(
        text="<b>2025</b><br>Top 6",
        x=0.5, y=0.5,
        font_size=13,
        showarrow=False,
        font=dict(color="#64748b")
    )]
)

# ==============================================================================
# 7. Tab 2 - Chart 5: Global Market Share Trajectory (2020–2025)
# ==============================================================================
fig_share = px.line(
    df,
    x="year",
    y="market_share",
    color="company",
    markers=True,
    color_discrete_map=COMPANY_COLORS
)

fig_share.update_traces(
    line=dict(width=2.8),
    marker=dict(size=7, line=dict(color="#ffffff", width=1.5)),
    hovertemplate="<b>%{data.name}</b><br>Year: %{x}<br>Global Share: <b>%{y:.2f}%</b><extra></extra>"
)

apply_layout(
    fig_share,
    height=380,
    showlegend=True,
    margin=dict(l=60, r=25, t=35, b=45),
    extra_xaxis=dict(title="Year", tickmode="linear", dtick=1, gridcolor="#f1f5f9"),
    extra_yaxis=dict(title="Global BEV Market Share (%)", ticksuffix="%", gridcolor="#f1f5f9")
)

# ==============================================================================
# 8. Tab 2 - Chart 6: YoY Deliveries Growth Rate Grouped Bar Chart
# ==============================================================================
growth_df = df.dropna(subset=["growth_rate"]).copy()

fig_growth_bar = px.bar(
    growth_df,
    x="year",
    y="growth_rate",
    color="company",
    barmode="group",
    color_discrete_map=COMPANY_COLORS
)

fig_growth_bar.update_traces(
    marker=dict(line=dict(color="#ffffff", width=0.8)),
    hovertemplate="<b>%{data.name}</b><br>Year: %{x}<br>YoY Growth: <b>%{y:+.1f}%</b><extra></extra>"
)

apply_layout(
    fig_growth_bar,
    height=380,
    showlegend=True,
    margin=dict(l=60, r=25, t=35, b=45),
    extra_xaxis=dict(title="Year", tickmode="linear", dtick=1, gridcolor="#f1f5f9"),
    extra_yaxis=dict(title="Year-over-Year Growth Rate (%)", ticksuffix="%", gridcolor="#f1f5f9", zeroline=True, zerolinewidth=1.5, zerolinecolor="#94a3b8")
)
fig_growth_bar.update_layout(bargap=0.25, bargroupgap=0.08)

# ==============================================================================
# 9. Tab 3 - Chart 7: Battery Technology Strategy Matrix (Heatmap)
# ==============================================================================
battery["company"] = battery["company"].astype(str).str.strip().replace({
    "Tesla": "Tesla Inc."
})

tech_cols = ["lfp", "ncm", "nca", "blade_battery"]
tech_labels = [
    "LFP (Lithium Iron Phosphate)",
    "NCM (Nickel Cobalt Manganese)",
    "NCA (Nickel Cobalt Aluminum)",
    "Blade Battery (BYD CTP LFP)"
]

battery_filtered = battery[battery["company"].isin(company_order)].copy()
battery_filtered["company"] = pd.Categorical(battery_filtered["company"], categories=company_order, ordered=True)
battery_filtered = battery_filtered.sort_values("company")

company_id = {company: i + 1 for i, company in enumerate(company_order)}
z_matrix = []
text_matrix = []

for _, row in battery_filtered.iterrows():
    z_row = []
    text_row = []
    for col in tech_cols:
        if str(row[col]).strip().lower() == "yes":
            z_row.append(company_id[str(row["company"])])
            text_row.append("✓ Adopted")
        else:
            z_row.append(0)
            text_row.append("- Not Adopted")
    z_matrix.append(z_row)
    text_matrix.append(text_row)

colors = ["#f8fafc"] + [COMPANY_COLORS[c] for c in company_order]
n_colors = len(colors)
custom_colorscale = []
for i, color in enumerate(colors):
    custom_colorscale.append([i / (n_colors - 1), color])
    custom_colorscale.append([i / (n_colors - 1), color])

fig_battery = go.Figure(
    data=go.Heatmap(
        z=z_matrix,
        x=tech_labels,
        y=battery_filtered["company"].astype(str),
        text=text_matrix,
        texttemplate="<b>%{text}</b>",
        textfont=dict(size=13, color="#1e293b"),
        colorscale=custom_colorscale,
        showscale=False,
        xgap=6,
        ygap=6,
        hovertemplate="<b>Automaker:</b> %{y}<br><b>Chemistry:</b> %{x}<br><b>Status:</b> %{text}<extra></extra>"
    )
)

apply_layout(
    fig_battery,
    height=360,
    showlegend=False,
    margin=dict(l=155, r=25, t=40, b=20),
    extra_xaxis=dict(title="", side="top", tickfont=dict(size=12, color="#1e293b")),
    extra_yaxis=dict(title="", tickfont=dict(size=12, color="#1e293b"), autorange="reversed")
)

# ==============================================================================
# 10. Tab 4 - Chart 8: YoY Growth Trajectory Line Chart (with Global Benchmark)
# ==============================================================================
fig_growth_line = go.Figure()

# Add Global Market Growth Benchmark
market_growth_filtered = market.dropna(subset=["global_growth_rate"])
fig_growth_line.add_trace(go.Scatter(
    x=market_growth_filtered["year"],
    y=market_growth_filtered["global_growth_rate"],
    mode="lines+markers",
    name="🌐 Global Market Benchmark",
    line=dict(color="#64748b", width=3, dash="dot", shape="spline"),
    marker=dict(size=8, symbol="diamond"),
    hovertemplate="<b>Global Market Benchmark</b><br>Year: %{x}<br>Avg Growth: <b>%{y:+.1f}%</b><extra></extra>"
))

for comp in company_order:
    comp_df = growth_df[growth_df["company"] == comp]
    fig_growth_line.add_trace(go.Scatter(
        x=comp_df["year"],
        y=comp_df["growth_rate"],
        mode="lines+markers",
        name=comp,
        line=dict(color=COMPANY_COLORS[comp], width=2.8, shape="spline"),
        marker=dict(size=7, line=dict(color="#ffffff", width=1.5)),
        hovertemplate=f"<b>{comp}</b><br>Year: %{{x}}<br>YoY Growth: <b>%{{y:+.1f}}%</b><extra></extra>"
    ))

apply_layout(
    fig_growth_line,
    height=380,
    showlegend=True,
    margin=dict(l=60, r=25, t=40, b=45),
    extra_xaxis=dict(title="Year", tickmode="linear", dtick=1, gridcolor="#f1f5f9"),
    extra_yaxis=dict(title="YoY Growth Rate (%)", ticksuffix="%", gridcolor="#f1f5f9", zeroline=True, zerolinewidth=1.5, zerolinecolor="#94a3b8", range=[-35, 205])
)

# ==============================================================================
# 11. Tab 4 - Chart 9: Annual Net Volume Added Grouped Bar Chart
# ==============================================================================
vol_change_df = df.dropna(subset=["volume_change"]).copy()

fig_volume_added = px.bar(
    vol_change_df,
    x="year",
    y="volume_change",
    color="company",
    barmode="group",
    color_discrete_map=COMPANY_COLORS
)

fig_volume_added.update_traces(
    marker=dict(line=dict(color="#ffffff", width=0.8)),
    hovertemplate="<b>%{data.name}</b><br>Year: %{x}<br>Net Deliveries Added: <b>%{y:+,.0f} units</b><extra></extra>"
)

apply_layout(
    fig_volume_added,
    height=380,
    showlegend=True,
    margin=dict(l=70, r=25, t=40, b=45),
    extra_xaxis=dict(title="Year", tickmode="linear", dtick=1, gridcolor="#f1f5f9"),
    extra_yaxis=dict(title="Annual Net Volume Added (Units)", tickformat="+,s", gridcolor="#f1f5f9", zeroline=True, zerolinewidth=1.5, zerolinecolor="#94a3b8")
)
fig_volume_added.update_layout(bargap=0.22, bargroupgap=0.06)

# ==============================================================================
# 12. Generate Pivot Growth Table HTML
# ==============================================================================
pivot_growth = df.pivot(index="company", columns="year", values="growth_rate")
pivot_sales = df.pivot(index="company", columns="year", values="bev_sales")

pivot_rows = []
for comp in company_order:
    color = COMPANY_COLORS[comp]
    s20 = int(pivot_sales.loc[comp, 2020]) if comp in pivot_sales.index and 2020 in pivot_sales.columns else 0
    row_html = f"""
    <tr>
        <td>
            <span class="company-badge" style="border-left-color: {color};">
                <span class="company-dot" style="background-color: {color};"></span>
                <b>{comp}</b>
            </span>
        </td>
        <td class="text-right font-mono">{s20:,} units</td>
    """
    for y in [2021, 2022, 2023, 2024, 2025]:
        val = pivot_growth.loc[comp, y] if comp in pivot_growth.index and y in pivot_growth.columns else 0
        sales_val = int(pivot_sales.loc[comp, y]) if comp in pivot_sales.index and y in pivot_sales.columns else 0
        row_html += f"""
        <td class="text-right font-mono">
            <div style="font-weight:600; color:{'#059669' if val>0 else '#dc2626'}">{val:+.1f}%</div>
            <div style="font-size:11px; color:#64748b;">({sales_val:,})</div>
        </td>
        """
    
    # 5-year total multiplier & volume diff
    v20 = sales_2020.get(comp, 1)
    v25 = sales_2025.get(comp, 0)
    diff = v25 - v20
    mult = v25 / v20 if v20 > 0 else 0
    row_html += f"""
        <td class="text-right font-mono" style="background:#f8fafc; font-weight:700; color:#1e40af;">
            +{diff:,} units<br>
            <span style="font-size:11.5px; color:#475569;">({mult:.1f}x Expansion)</span>
        </td>
    </tr>
    """
    pivot_rows.append(row_html)

# Add Global Market benchmark row
global_sales_2020 = market.loc[market["year"] == 2020, "total_global_bev_sales"].values[0]
global_sales_2025 = market.loc[market["year"] == 2025, "total_global_bev_sales"].values[0]
global_diff = global_sales_2025 - global_sales_2020
global_mult = global_sales_2025 / global_sales_2020

global_row_html = f"""
<tr style="background:#eff6ff; font-weight:600; border-top: 2px solid #93c5fd;">
    <td><b>🌐 Global BEV Market Total</b></td>
    <td class="text-right font-mono">{int(global_sales_2020):,} units</td>
"""
for y in [2021, 2022, 2023, 2024, 2025]:
    g_val = market.loc[market["year"] == y, "global_growth_rate"].values[0]
    g_sales = market.loc[market["year"] == y, "total_global_bev_sales"].values[0]
    global_row_html += f"""
    <td class="text-right font-mono">
        <div style="font-weight:700; color:#1d4ed8;">+{g_val:.1f}%</div>
        <div style="font-size:11px; color:#64748b;">({int(g_sales):,})</div>
    </td>
    """
global_row_html += f"""
    <td class="text-right font-mono" style="background:#dbeafe; font-weight:800; color:#1e40af;">
        +{global_diff:,} units<br>
        <span style="font-size:11.5px; color:#1e40af;">({global_mult:.1f}x Expansion)</span>
    </td>
</tr>
"""
pivot_rows.append(global_row_html)
pivot_rows_html = "\n".join(pivot_rows)

# ==============================================================================
# 13. Extract Plotly Divs
# ==============================================================================
div_global = fig_global.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})
div_sales = fig_sales.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})
div_ranking = fig_ranking.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})
div_pie = fig_pie.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})
div_share = fig_share.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})
div_growth_bar = fig_growth_bar.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})
div_battery = fig_battery.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})
div_growth_line = fig_growth_line.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})
div_volume_added = fig_volume_added.to_html(full_html=False, include_plotlyjs=False, config={"responsive": True, "displayModeBar": False})

# ==============================================================================
# 14. Build Consolidated Single Dashboard HTML
# ==============================================================================
html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global Pure BEV Market Intelligence Dashboard (2020–2025)</title>
    <!-- Plotly.js -->
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-main: #f8fafc;
            --bg-card: #ffffff;
            --border-color: #e2e8f0;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #94a3b8;
            --primary: #2563eb;
            --primary-light: #eff6ff;
            --radius-lg: 14px;
            --radius-md: 8px;
            --radius-sm: 6px;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.07);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-primary);
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }}

        .dashboard-container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px 24px 40px;
        }}

        /* Header */
        .dashboard-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .header-title-group h1 {{
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .header-badge {{
            display: inline-flex;
            align-items: center;
            padding: 3px 10px;
            background: #dbeafe;
            color: #1e40af;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
        }}

        .header-subtitle {{
            color: var(--text-secondary);
            font-size: 13.5px;
            margin-top: 4px;
        }}

        .header-meta {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .meta-pill {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 6px 12px;
            border-radius: var(--radius-sm);
            font-size: 12.5px;
            font-weight: 500;
            color: var(--text-secondary);
            box-shadow: var(--shadow-sm);
        }}

        /* KPI Cards Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}

        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 18px 20px;
            box-shadow: var(--shadow-sm);
            position: relative;
            overflow: hidden;
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3.5px;
            background: var(--primary);
        }}

        .kpi-card.byd::before {{ background: #E11D48; }}
        .kpi-card.tesla::before {{ background: #7C3AED; }}
        .kpi-card.market::before {{ background: #2563eb; }}
        .kpi-card.legacy::before {{ background: #00287A; }}

        .kpi-title {{
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }}

        .kpi-value {{
            font-size: 26px;
            font-weight: 800;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            line-height: 1.1;
        }}

        .kpi-trend {{
            margin-top: 8px;
            font-size: 12.5px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .trend-up {{
            color: #059669;
            font-weight: 600;
        }}

        .trend-desc {{
            color: var(--text-muted);
        }}

        /* Tab Navigation */
        .tabs-nav-container {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 6px;
            margin-bottom: 20px;
            box-shadow: var(--shadow-sm);
        }}

        .tabs-nav {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
        }}

        .tab-btn {{
            flex: 1;
            min-width: 180px;
            padding: 10px 16px;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            font-size: 13.5px;
            font-weight: 600;
            border-radius: var(--radius-md);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            transition: all 0.2s ease;
            white-space: nowrap;
        }}

        .tab-btn:hover {{
            background: var(--bg-main);
            color: var(--text-primary);
        }}

        .tab-btn.active {{
            background: var(--primary);
            color: #ffffff;
            box-shadow: 0 3px 8px rgba(37, 99, 235, 0.25);
        }}

        /* Tab Contents */
        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
        }}

        /* Grid Layouts */
        .dashboard-grid-2x2 {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 20px;
        }}

        .dashboard-grid-1x2 {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 20px;
        }}

        .dashboard-grid-single {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }}

        /* Dashboard Cards */
        .chart-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 18px 20px;
            box-shadow: var(--shadow-sm);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            min-width: 0;
        }}

        .chart-card-header {{
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid #f1f5f9;
        }}

        .chart-card-title {{
            font-size: 15px;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .chart-card-subtitle {{
            font-size: 12.5px;
            color: var(--text-secondary);
            margin-top: 2px;
        }}

        .chart-container {{
            width: 100%;
            position: relative;
            overflow: hidden;
            min-width: 0;
        }}

        .chart-container .plotly-graph-div {{
            width: 100% !important;
            min-width: 0 !important;
        }}

        /* Strategic Insight Callout */
        .insight-box {{
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--primary);
            padding: 16px 20px;
            border-radius: 0 var(--radius-md) var(--radius-md) 0;
            margin-top: 20px;
            box-shadow: var(--shadow-sm);
        }}

        .insight-box h4 {{
            font-size: 14px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 6px;
        }}

        .insight-box p {{
            font-size: 13.5px;
            color: var(--text-secondary);
            line-height: 1.6;
        }}

        /* Battery Chem Specs Grid */
        .chem-specs-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 16px;
            margin-top: 20px;
        }}

        .chem-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 16px 18px;
            box-shadow: var(--shadow-sm);
        }}

        .chem-badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: var(--radius-sm);
            font-size: 11.5px;
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .chem-badge.lfp {{ background: #fef3c7; color: #92400e; }}
        .chem-badge.ncm {{ background: #e0e7ff; color: #3730a3; }}
        .chem-badge.nca {{ background: #fae8ff; color: #86198f; }}
        .chem-badge.blade {{ background: #fee2e2; color: #991b1b; }}

        .chem-card h4 {{
            font-size: 14.5px;
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .chem-card ul {{
            padding-left: 18px;
            font-size: 12.5px;
            color: var(--text-secondary);
        }}

        .chem-card li {{
            margin-bottom: 4px;
        }}

        /* Pivot Growth Table */
        .table-responsive {{
            overflow-x: auto;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            background: var(--bg-card);
            box-shadow: var(--shadow-sm);
            margin-top: 20px;
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 13px;
        }}

        .data-table th {{
            background: #f1f5f9;
            color: var(--text-secondary);
            font-weight: 600;
            padding: 12px 16px;
            border-bottom: 2px solid var(--border-color);
            white-space: nowrap;
        }}

        .data-table td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
        }}

        .data-table tr:hover {{
            background: #f8fafc;
        }}

        .company-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding-left: 8px;
            border-left: 3px solid transparent;
        }}

        .company-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }}

        .font-mono {{
            font-family: 'JetBrains Mono', monospace;
        }}

        .text-right {{
            text-align: right;
        }}

        /* Responsive */
        @media (max-width: 1024px) {{
            .dashboard-grid-2x2, .dashboard-grid-1x2 {{
                grid-template-columns: 1fr;
            }}
            .kpi-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (max-width: 640px) {{
            .dashboard-container {{
                padding: 14px;
            }}
            .kpi-grid {{
                grid-template-columns: 1fr;
            }}
            .tab-btn {{
                min-width: 140px;
                padding: 8px 12px;
                font-size: 12.5px;
            }}
        }}
    </style>
</head>
<body>

<div class="dashboard-container">
    <!-- Header -->
    <header class="dashboard-header">
        <div class="header-title-group">
            <h1>
                ⚡ Global Pure BEV Market Intelligence Dashboard
                <span class="header-badge">2020 – 2025</span>
            </h1>
            <p class="header-subtitle">Empirical Market Analysis of 6 Major Automakers (BYD, Tesla, VW, Hyundai-Kia, BMW, Mercedes-Benz) & Battery Strategies</p>
        </div>
        <div class="header-meta">
            <div class="meta-pill">📊 Scope: 100% Pure BEVs</div>
            <div class="meta-pill">🔄 Data Benchmark: IEA & Official IR</div>
        </div>
    </header>

    <!-- Top KPI Cards -->
    <section class="kpi-grid">
        <div class="kpi-card market">
            <div class="kpi-title">2025 Global BEV Penetration</div>
            <div class="kpi-value">19.7%</div>
            <div class="kpi-trend">
                <span class="trend-up">▲ +16.6%p</span>
                <span class="trend-desc">Expanded from 3.1% in 2020 (7.0x)</span>
            </div>
        </div>

        <div class="kpi-card byd">
            <div class="kpi-title">2025 Global #1 Volume (BYD)</div>
            <div class="kpi-value">2,256,714 units</div>
            <div class="kpi-trend">
                <span class="trend-up">▲ +27.9% YoY</span>
                <span class="trend-desc">Surpassed Tesla with Vertical Integration</span>
            </div>
        </div>

        <div class="kpi-card tesla">
            <div class="kpi-title">2025 Global #2 Volume (Tesla)</div>
            <div class="kpi-value">1,640,000 units</div>
            <div class="kpi-trend">
                <span style="color:#64748b; font-weight:600;">Dedicated Pioneer</span>
                <span class="trend-desc">11.7% Share · Navigating Maturity</span>
            </div>
        </div>

        <div class="kpi-card legacy">
            <div class="kpi-title">Legacy Leader / Hyundai-Kia Growth</div>
            <div class="kpi-value">983k / 514k units</div>
            <div class="kpi-trend">
                <span class="trend-up">VW 983k · HMG 514k</span>
                <span class="trend-desc">E-GMP Platform Expansion</span>
            </div>
        </div>
    </section>

    <!-- Tabs Navigation Bar -->
    <nav class="tabs-nav-container">
        <div class="tabs-nav">
            <button class="tab-btn active" onclick="switchTab('tab-overview', this)">
                📊 1. Global Market Overview
            </button>
            <button class="tab-btn" onclick="switchTab('tab-dynamics', this)">
                📈 2. Market Share & Growth Dynamics
            </button>
            <button class="tab-btn" onclick="switchTab('tab-battery', this)">
                🔋 3. Battery Technology Strategy
            </button>
            <button class="tab-btn" onclick="switchTab('tab-growth-analysis', this)">
                🚀 4. YoY Growth & Net Volume Expansion
            </button>
        </div>
    </nav>

    <!-- TAB 1: Overview & Market Trends -->
    <div id="tab-overview" class="tab-content active">
        <div class="dashboard-grid-2x2">
            <div class="chart-card">
                <div class="chart-card-header">
                    <h2 class="chart-card-title">Global BEV Market Penetration Trajectory (2020–2025)</h2>
                    <p class="chart-card-subtitle">Share of Pure Electric BEVs in Global Passenger Car Deliveries (%)</p>
                </div>
                <div class="chart-container">
                    {div_global}
                </div>
            </div>

            <div class="chart-card">
                <div class="chart-card-header">
                    <h2 class="chart-card-title">Annual BEV Deliveries by Top 6 Automakers</h2>
                    <p class="chart-card-subtitle">Historical Delivery Trends Across Major OEM Groups (2020–2025)</p>
                </div>
                <div class="chart-container">
                    {div_sales}
                </div>
            </div>

            <div class="chart-card">
                <div class="chart-card-header">
                    <h2 class="chart-card-title">2025 BEV Volume Leaderboard</h2>
                    <p class="chart-card-subtitle">Final Ranked Annual Deliveries by Automaker Group (Units)</p>
                </div>
                <div class="chart-container">
                    {div_ranking}
                </div>
            </div>

            <div class="chart-card">
                <div class="chart-card-header">
                    <h2 class="chart-card-title">2025 Top-6 OEM Delivery Distribution</h2>
                    <p class="chart-card-subtitle">Proportional Share Among the 6 Major Electrified Groups (%)</p>
                </div>
                <div class="chart-container">
                    {div_pie}
                </div>
            </div>
        </div>

        <div class="insight-box">
            <h4>💡 Executive Market Takeaways (2020–2025)</h4>
            <p>
                Between 2020 and 2025, the global pure BEV market expanded **7.0x from 2.00M to 14.00M units**, driving adoption penetration from 3.1% to 19.7%.
                Propelled by 100% in-house battery vertical integration, **BYD ascended to the Global #1 position with 2.26M units (16.1% share)**.
                **Tesla maintained #2 with 1.64M units (11.7% share)** while managing product cycle maturity.
                Among legacy titans, **Volkswagen Group (983k units, 7.0% share)** and **Hyundai-Kia Group (514k units, 3.7% share)** established resilient podium positions via dedicated modular architectures (MEB and E-GMP).
            </p>
        </div>
    </div>

    <!-- TAB 2: Competitive Dynamics & Growth -->
    <div id="tab-dynamics" class="tab-content">
        <div class="dashboard-grid-1x2">
            <div class="chart-card">
                <div class="chart-card-header">
                    <h2 class="chart-card-title">Global BEV Market Share Dynamics (2020–2025)</h2>
                    <p class="chart-card-subtitle">Percentage Share of Total Global Pure BEV Market Deliveries (%)</p>
                </div>
                <div class="chart-container">
                    {div_share}
                </div>
            </div>

            <div class="chart-card">
                <div class="chart-card-header">
                    <h2 class="chart-card-title">Annual YoY Delivery Growth Rate Comparison</h2>
                    <p class="chart-card-subtitle">Year-over-Year Percentage Growth by Automaker Group (%)</p>
                </div>
                <div class="chart-container">
                    {div_growth_bar}
                </div>
            </div>
        </div>

        <div class="insight-box">
            <h4>📈 Competitive Market Share & Growth Analysis</h4>
            <p>
                <b>1. BYD's Hyper-Expansion:</b> Leveraging low-cost LFP Blade Batteries and rapid model iterations, BYD surged from 6.55% in 2020 to 16.12% in 2025 (+17.2x delivery volume).<br>
                <b>2. Tesla's Monopolistic Dilution:</b> Tesla's early market dominance (24.98% in 2020) normalized to 11.71% in 2025 as mainstream competition intensified.<br>
                <b>3. Legacy OEM Stratification:</b> Volkswagen Group held legacy leadership (7.02%), followed by Hyundai-Kia Group (3.67%) and BMW Group (3.16%), effectively scaling premium and volume segments.
            </p>
        </div>
    </div>

    <!-- TAB 3: Battery Tech Strategy -->
    <div id="tab-battery" class="tab-content">
        <div class="dashboard-grid-single">
            <div class="chart-card">
                <div class="chart-card-header">
                    <h2 class="chart-card-title">Automaker Battery Chemistry & Packaging Deployment Matrix</h2>
                    <p class="chart-card-subtitle">Strategic Adoption of LFP, NCM, NCA, and Cell-to-Pack Blade Technologies</p>
                </div>
                <div class="chart-container">
                    {div_battery}
                </div>
            </div>
        </div>

        <!-- Battery Chemical Specs Detail Cards -->
        <div class="chem-specs-grid">
            <div class="chem-card">
                <span class="chem-badge lfp">LFP (Lithium Iron Phosphate)</span>
                <h4>Low Cost & Exceptional Thermal Stability</h4>
                <ul>
                    <li><b>Strengths:</b> Lowest raw material cost, superior fire safety, long cycle life (>3,000 cycles).</li>
                    <li><b>Trade-offs:</b> Lower gravimetric energy density, cold weather performance degradation.</li>
                    <li><b>Primary OEM Mix:</b> BYD (100%), Tesla (Standard RWD), Hyundai-Kia (Entry), VW Group.</li>
                </ul>
            </div>

            <div class="chem-card">
                <span class="chem-badge blade">Blade Battery</span>
                <h4>BYD Proprietary Cell-to-Pack (CTP) LFP</h4>
                <ul>
                    <li><b>Architecture:</b> Direct structural integration boosts pack space utilization by 50%.</li>
                    <li><b>Safety:</b> Passed rigorous nail penetration tests without thermal runaway.</li>
                    <li><b>Primary OEM Mix:</b> BYD standard across entire vehicle portfolio.</li>
                </ul>
            </div>

            <div class="chem-card">
                <span class="chem-badge ncm">NCM (Nickel Cobalt Manganese)</span>
                <h4>High Energy Density & Long Highway Range</h4>
                <ul>
                    <li><b>Strengths:</b> Premium energy density (250-300 Wh/kg), fast DC charging, cold tolerance.</li>
                    <li><b>Trade-offs:</b> Vulnerability to commodity price spikes (Ni, Co), active thermal management required.</li>
                    <li><b>Primary OEM Mix:</b> Hyundai-Kia (E-GMP 800V), VW Group, BMW Group, Mercedes-Benz.</li>
                </ul>
            </div>

            <div class="chem-card">
                <span class="chem-badge nca">NCA (Nickel Cobalt Aluminum)</span>
                <h4>Maximum Specific Power & Acceleration</h4>
                <ul>
                    <li><b>Strengths:</b> Ultra-high specific power output, outstanding discharge rates for performance.</li>
                    <li><b>Trade-offs:</b> Complex manufacturing, higher degradation sensitivity under high temperatures.</li>
                    <li><b>Primary OEM Mix:</b> Tesla (Long Range & Performance trims).</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- TAB 4: Growth Rate Analysis (Graphs & Pivot Table) -->
    <div id="tab-growth-analysis" class="tab-content">
        <div class="dashboard-grid-1x2">
            <div class="chart-card">
                <div class="chart-card-header">
                    <h2 class="chart-card-title">YoY Delivery Growth Trajectory (2021–2025)</h2>
                    <p class="chart-card-subtitle">OEM Growth Profiles Benchmarked Against Global Market Growth (Dotted Line)</p>
                </div>
                <div class="chart-container">
                    {div_growth_line}
                </div>
            </div>

            <div class="chart-card">
                <div class="chart-card-header">
                    <h2 class="chart-card-title">Annual Net Incremental Deliveries Added (2021–2025)</h2>
                    <p class="chart-card-subtitle">Net Additional Vehicle Volume Delivered Over Prior Year (Units)</p>
                </div>
                <div class="chart-container">
                    {div_volume_added}
                </div>
            </div>
        </div>

        <!-- Pivot Summary Growth Table -->
        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Automaker (OEM)</th>
                        <th class="text-right">2020 Base</th>
                        <th class="text-right">2021 (YoY)</th>
                        <th class="text-right">2022 (YoY)</th>
                        <th class="text-right">2023 (YoY)</th>
                        <th class="text-right">2024 (YoY)</th>
                        <th class="text-right">2025 (YoY)</th>
                        <th class="text-right" style="background:#f1f5f9;">5-Yr Cumulative Net Volume (2020→2025)</th>
                    </tr>
                </thead>
                <tbody>
                    {pivot_rows_html}
                </tbody>
            </table>
        </div>

        <div class="insight-box">
            <h4>🚀 Strategic Insights on Pure BEV Market Dynamics</h4>
            <p>
                <b>• 2021–2022 Gold Rush:</b> BYD (+145% → +184%), Tesla (+87% → +40%), and Hyundai-Kia (+58% → +138%) outpaced global market growth during the early adoption boom.<br>
                <b>• 2023–2024 EV Chasm & Correction:</b> Subsidies expired and early adopters saturated, moderating global market growth to +15% and causing temporary delivery contractions for Tesla (-1.0%) and Volkswagen (-3.4%).<br>
                <b>• 2025 Strategic Rebound:</b> Mass-market LFP rollouts and new dedicated models enabled BYD (+27.9%), VW (+31.9%), and Hyundai-Kia (+12.4%) to lead the market recovery.
            </p>
        </div>
    </div>
</div>

<script>
    // Tab switching logic with automatic Plotly resize trigger
    function switchTab(tabId, btn) {{
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

        const targetTab = document.getElementById(tabId);
        if (targetTab) {{
            targetTab.classList.add('active');
        }}
        if (btn) {{
            btn.classList.add('active');
        }}

        // Trigger resize so newly visible tab charts scale properly
        setTimeout(() => {{
            window.dispatchEvent(new Event('resize'));
            document.querySelectorAll('.plotly-graph-div').forEach(el => {{
                if (window.Plotly && el) {{
                    Plotly.Plots.resize(el);
                }}
            }});
        }}, 50);
    }}

    // Initial resize trigger on window load
    window.addEventListener('load', () => {{
        setTimeout(() => {{
            window.dispatchEvent(new Event('resize'));
            document.querySelectorAll('.plotly-graph-div').forEach(el => {{
                if (window.Plotly && el) {{
                    Plotly.Plots.resize(el);
                }}
            }});
        }}, 100);
    }});
</script>
</body>
</html>
"""

# ==============================================================================
# 15. Save and Open Dashboard
# ==============================================================================
output_html_path = os.path.join(project_dir, "dashboard.html")
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print("\n" + "=" * 65)
print("  [SUCCESS] Global Pure BEV Market Unified Dashboard generated successfully!")
print(f"  [PATH] {output_html_path}")
print("=" * 65 + "\n")

# Open single browser window/tab
webbrowser.open(f"file://{output_html_path}")