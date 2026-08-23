import os
import json
import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pdf_generator import generate_board_briefing_pdf


# ==============================================================================
# Page Configuration & Terminal Theme (Sidebar Completely Removed)
# ==============================================================================
st.set_page_config(
    page_title="The German Auto Triad's China Trap: Asymmetric IDAR Absorption & Phased De-risking (2019–2035)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Custom High-Contrast CSS (Completely hide Streamlit sidebar)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Completely hide Streamlit sidebar and collapse button */
    [data-testid="stSidebar"], section[data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #0F172A;
        color: #F43F5E;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        border: 1px solid #881337;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #F43F5E;
        border-radius: 50%;
        box-shadow: 0 0 0 rgba(244, 63, 94, 0.4);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(244, 63, 94, 0); }
        100% { box-shadow: 0 0 0 0 rgba(244, 63, 94, 0); }
    }
    
    .hero-title {
        font-size: 1.95rem;
        font-weight: 800;
        color: #F8FAFC !important;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
        line-height: 1.25;
    }
    .hero-subtitle {
        font-size: 0.98rem;
        color: #94A3B8 !important;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    
    .metric-container {
        background: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 14px;
        padding: 1.2rem 1.3rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #94A3B8 !important;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8FAFC !important;
        line-height: 1.1;
        margin-bottom: 0.3rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-tag {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load centralized JSON datasets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)

# Load verified datasets
audited_facts = load_json("audited_financial_facts.json")
historical_deliveries = load_json("historical_deliveries.json")
triad_oems = load_json("triad_oems.json")
idar_data = load_json("idar_asymmetric_strategy.json")
technology_flow_data = load_json("technology_flow_matrix.json")
bifurcation_data = load_json("bifurcation_scenarios.json")
capital_defense_data = load_json("capital_defense.json")
cross_sector_data = load_json("cross_sector_safeguards.json")

df_chart = pd.DataFrame([
    {
        "year": r["year"],
        "Volkswagen Group": r["vwChinaK"],
        "Mercedes-Benz": r["mercedesChinaK"],
        "BMW Group": r["bmwChinaK"],
        "Total Triad Sales": r["totalTriadChinaK"],
        "Total Local Prod": r["totalTriadLocalProdK"],
        "Market Share (%)": r["triadChinaMarketSharePct"],
        "NEV Penetration (%)": r["chineseEvPenetrationPct"],
        # Disaggregated 6 Dependency Metrics
        "vwEbitShare": r.get("vwEbitShare", 38.0),
        "mercedesEbitShare": r.get("mercedesEbitShare", 31.5),
        "bmwEbitShare": r.get("bmwEbitShare", 28.5),
        "triadEbitShare": r.get("chinaEbitSharePct", 32.7),
        
        "vwComponentsCost": r.get("vwComponentsCost", 58.5),
        "mercedesComponentsCost": r.get("mercedesComponentsCost", 42.0),
        "bmwComponentsCost": r.get("bmwComponentsCost", 48.0),
        "triadComponentsCost": r.get("chineseComponentsCostPct", 49.5),
        
        "vwSupplierConcentration": r.get("vwSupplierConcentration", 76.5),
        "mercedesSupplierConcentration": r.get("mercedesSupplierConcentration", 68.0),
        "bmwSupplierConcentration": r.get("bmwSupplierConcentration", 82.0),
        "triadSupplierConcentration": r.get("supplierConcentrationCr3Pct", 75.5),
        
        "vwDataStorage": r.get("vwDataStorage", 100.0),
        "mercedesDataStorage": r.get("mercedesDataStorage", 100.0),
        "bmwDataStorage": r.get("bmwDataStorage", 100.0),
        "triadDataStorage": r.get("dataStorageIsolationPct", 100.0),
        
        "vwVotingPower": r.get("vwVotingPower", 0.0),
        "mercedesVotingPower": r.get("mercedesVotingPower", 37.5),
        "bmwVotingPower": r.get("bmwVotingPower", 0.0),
        "triadVotingPower": r.get("votingPowerPct", 37.5),
        
        "vwSubstitutability": r.get("vwSubstitutability", 4.8),
        "mercedesSubstitutability": r.get("mercedesSubstitutability", 3.7),
        "bmwSubstitutability": r.get("bmwSubstitutability", 4.2),
        "triadSubstitutability": r.get("substitutabilityYears", 4.2)
    }
    for r in historical_deliveries["timeSeries"]
])

df_forecast = pd.DataFrame(bifurcation_data["forecastTimeSeries2026_2035"])

# Main Terminal Header
st.markdown("""
<div>
    <div class="status-badge"><span class="pulse-dot"></span> Institutional Strategic Intelligence Suite | 2019–2025 &amp; 2026–2035 Forecast</div>
    <div class="hero-title">The German Auto Triad's China Trap</div>
    <div class="hero-subtitle">Asymmetric IDAR Absorption, Governance Vulnerabilities (AktG §179) &amp; The Phased De-risking Playbook (2019–2035)</div>
</div>
""", unsafe_allow_html=True)


# 4 Key Macro Ribbon Metrics
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown("""
    <div class="metric-container" style="border: 1.5px solid #881337;">
        <div class="metric-label" style="color: #FDA4AF;">Triad Sales Collapse</div>
        <div class="metric-value" style="color: #F43F5E;">-1.59M <span style="font-size: 0.9rem; color:#FDA4AF;">Units</span></div>
        <div class="metric-tag" style="background:#4C0519; color:#FDA4AF; border: 1px solid #881337;">-28.1% (2019: 5.65M Units ➔ 2025: 4.06M Units)</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="metric-container" style="border: 1.5px solid #881337;">
        <div class="metric-label" style="color: #FDA4AF;">Triad Market Share Halved</div>
        <div class="metric-value" style="color: #F43F5E;">12.8%</div>
        <div class="metric-tag" style="background:#4C0519; color:#FDA4AF; border: 1px solid #881337;">-12.3%p (2019: 25.1% ➔ 2025: 12.8%)</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="metric-container" style="border: 1.5px solid #881337;">
        <div class="metric-label" style="color: #FDA4AF;">China EBIT Contribution Plunge</div>
        <div class="metric-value" style="color: #F43F5E;">-€7.3B</div>
        <div class="metric-tag" style="background:#4C0519; color:#FDA4AF; border: 1px solid #881337;">-48.0% (2019: €15.2B ➔ 2025: €7.9B)</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="metric-container" style="border: 1.5px solid #9A3412;">
        <div class="metric-label" style="color: #FDBA74;">Local Production Ratio</div>
        <div class="metric-value" style="color: #F97316;">89.2%</div>
        <div class="metric-tag" style="background:#431407; color:#FDBA74; border: 1px solid #9A3412;">90% of Sales Volume Sunk in Domestic Fabs</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 8 Revised Executive Tabs (100% Pure English)
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 1. 2019–2025 Market Collapse & Dependency",
    "🏢 2. Triad Encroachment & Hostage Dilemmas",
    "🏛️ 3. IDAR Strategy & Asymmetric Openness",
    "🔄 4. Technology Exfiltration & Reverse Flow",
    "🔀 5. 3 Scenarios & 2035 Future Forecast",
    "🔒 6. €45B Sunk Capital & Dual-Track Air-Gap",
    "💡 7. 5 Strategic Truths & Policy Actions",
    "🛡️ 8. Cross-Sector Safeguards & Board Checklist"
])

# ==============================================================================
# TAB 1: 2019–2025 MARKET COLLAPSE & QUANTITATIVE DEPENDENCY
# ==============================================================================
with tab1:
    st.markdown("### 📊 2019–2025 Continuous Time-Series & 3-OEM Quantitative Dependency Charts")
    
    main_view_type = st.radio(
        "Select Analysis Dimension:",
        [
            "📊 1. Basic Market Performance (Deliveries / Production / Share)",
            "📐 2. 6 Measurable Dependency Time-Series (3-OEM Comparative Lines)",
            "🕸️ 3. Triad 6-Dimension High-Contrast Radar Diagrams"
        ],
        horizontal=True
    )
    
    # --------------------------------------------------------------------------
    # LEVEL 1: BASIC MARKET PERFORMANCE
    # --------------------------------------------------------------------------
    if "1. Basic Market Performance" in main_view_type:
        perf_sub = st.selectbox(
            "Select Performance Metric:",
            [
                "3-OEM Individual Deliveries (VW Deep Blue / Mercedes Slate / BMW White)",
                "Local Production (Yellow) vs. Total Deliveries (Red)",
                "Triad Market Share (Dark Russet) vs. China NEV Penetration (Red)"
            ]
        )
        
        if "3-OEM Individual Deliveries" in perf_sub:
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=df_chart["year"], y=df_chart["Volkswagen Group"],
                name="Volkswagen Group (VW Deep Blue: #002D72)",
                marker_color="#002D72"
            ))
            fig_bar.add_trace(go.Bar(
                x=df_chart["year"], y=df_chart["Mercedes-Benz"],
                name="Mercedes-Benz (Mercedes Slate: #94A3B8)",
                marker_color="#94A3B8"
            ))
            fig_bar.add_trace(go.Bar(
                x=df_chart["year"], y=df_chart["BMW Group"],
                name="BMW Group (BMW White: #FFFFFF)",
                marker_color="#FFFFFF",
                marker_line_color="#CBD5E1",
                marker_line_width=1.5
            ))
            fig_bar.add_trace(go.Scatter(
                x=df_chart["year"], y=df_chart["Total Triad Sales"],
                name="Total Triad Deliveries",
                line=dict(color="#FCD34D", width=3)
            ))
            fig_bar.update_layout(
                barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=380, margin=dict(l=40, r=20, t=20, b=40),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(gridcolor="#1e293b", dtick=1), yaxis=dict(title="Deliveries (k units)", gridcolor="#1e293b")
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        elif "Local Production" in perf_sub:
            fig_prod = go.Figure()
            fig_prod.add_trace(go.Bar(
                x=df_chart["year"], y=df_chart["Total Local Prod"],
                name="China Local Production (Yellow)",
                marker_color="#EAB308"
            ))
            fig_prod.add_trace(go.Bar(
                x=df_chart["year"], y=df_chart["Total Triad Sales"],
                name="Total Deliveries in China (Red)",
                marker_color="#DC2626"
            ))
            fig_prod.update_layout(
                barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=380, margin=dict(l=40, r=20, t=20, b=40),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(gridcolor="#1e293b", dtick=1), yaxis=dict(title="Volume (k units)", gridcolor="#1e293b")
            )
            st.plotly_chart(fig_prod, use_container_width=True)

        else:
            fig_share = go.Figure()
            fig_share.add_trace(go.Scatter(
                x=df_chart["year"], y=df_chart["Market Share (%)"],
                name="Triad Market Share (%) [Dark Russet / #8B4513]",
                line=dict(color="#8B4513", width=3.5)
            ))
            fig_share.add_trace(go.Scatter(
                x=df_chart["year"], y=df_chart["NEV Penetration (%)"],
                name="China NEV Penetration (%) [Crimson Red / #DC2626]",
                line=dict(color="#DC2626", width=3.5)
            ))
            fig_share.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=380, margin=dict(l=40, r=20, t=20, b=40),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(gridcolor="#1e293b", dtick=1), yaxis=dict(title="Ratio (%)", gridcolor="#1e293b")
            )
            st.plotly_chart(fig_share, use_container_width=True)

    # --------------------------------------------------------------------------
    # LEVEL 2: DISAGGREGATED 6 DEPENDENCY METRICS (3 OEM COMPARISON)
    # --------------------------------------------------------------------------
    elif "2. 6 Measurable Dependency" in main_view_type:
        dep_metric_choice = st.selectbox(
            "Select Quantitative Dependency Dimension (2019–2025):",
            [
                "1. China EBIT Contribution Share (%) [VW vs Mercedes vs BMW vs Avg]",
                "2. Chinese Component Cost Share (BOM %) [VW vs Mercedes vs BMW vs Avg]",
                "3. Chinese Supplier Concentration (CR3 %) [VW vs Mercedes vs BMW vs Avg]",
                "4. Local Data Storage & Isolation Ratio (%) [VW vs Mercedes vs BMW vs Avg]",
                "5. Chinese Equity & Effective Voting Power (%) [VW vs Mercedes vs BMW vs Avg]",
                "6. Non-China Replacement Lead Time (Years) [VW vs Mercedes vs BMW vs Avg]"
            ]
        )
        
        is_voting_metric = "5. Chinese Equity & Effective Voting Power" in dep_metric_choice
        
        if "1. China EBIT Contribution" in dep_metric_choice:
            vw_col, mb_col, bmw_col, avg_col = "vwEbitShare", "mercedesEbitShare", "bmwEbitShare", "triadEbitShare"
            y_title = "China EBIT Contribution Share (%)"
        elif "2. Chinese Component Cost" in dep_metric_choice:
            vw_col, mb_col, bmw_col, avg_col = "vwComponentsCost", "mercedesComponentsCost", "bmwComponentsCost", "triadComponentsCost"
            y_title = "Chinese Component Cost Share (BOM %)"
        elif "3. Chinese Supplier Concentration" in dep_metric_choice:
            vw_col, mb_col, bmw_col, avg_col = "vwSupplierConcentration", "mercedesSupplierConcentration", "bmwSupplierConcentration", "triadSupplierConcentration"
            y_title = "Top-3 Supplier Concentration CR3 (%)"
        elif "4. Local Data Storage" in dep_metric_choice:
            vw_col, mb_col, bmw_col, avg_col = "vwDataStorage", "mercedesDataStorage", "bmwDataStorage", "triadDataStorage"
            y_title = "Local Data Isolation Ratio (%)"
        elif is_voting_metric:
            vw_col, mb_col, bmw_col, avg_col = "vwVotingPower", "mercedesVotingPower", "bmwVotingPower", "triadVotingPower"
            y_title = "Effective Chinese Voting Power (%)"
        else:
            vw_col, mb_col, bmw_col, avg_col = "vwSubstitutability", "mercedesSubstitutability", "bmwSubstitutability", "triadSubstitutability"
            y_title = "Replacement Lead Time (Years)"

        fig_dep = go.Figure()
        
        # 1. Volkswagen: VW Deep Blue (#00439C)
        fig_dep.add_trace(go.Scatter(
            x=df_chart["year"], y=df_chart[vw_col],
            name="Volkswagen Group (VW Deep Blue: #00439C)",
            line=dict(color="#00439C", width=3.5),
            marker=dict(size=8, symbol="square")
        ))
        
        # 2. Mercedes-Benz: Silver / Slate (#94A3B8)
        fig_dep.add_trace(go.Scatter(
            x=df_chart["year"], y=df_chart[mb_col],
            name="Mercedes-Benz (Silver Slate: #94A3B8)",
            line=dict(color="#94A3B8", width=3.5),
            marker=dict(size=8, symbol="circle")
        ))
        
        # 3. BMW Group: Pure White (#FFFFFF)
        fig_dep.add_trace(go.Scatter(
            x=df_chart["year"], y=df_chart[bmw_col],
            name="BMW Group (BMW White: #FFFFFF)",
            line=dict(color="#FFFFFF", width=3.5, dash="solid"),
            marker=dict(size=8, symbol="triangle-up", color="#FFFFFF")
        ))
        
        # 4. Triad Composite Average: Red (#F43F5E)
        fig_dep.add_trace(go.Scatter(
            x=df_chart["year"], y=df_chart[avg_col],
            name="Triad Composite Average (Red: #F43F5E)",
            line=dict(color="#F43F5E", width=4, dash="solid"),
            marker=dict(size=9, symbol="diamond")
        ))
        
        # Special 25% Veto Threshold line for Voting Power metric
        if is_voting_metric:
            fig_dep.add_hline(
                y=25.0, line_dash="dash", line_color="#EF4444", line_width=2.5,
                annotation_text="⚠️ AktG §179 25% Supermajority Blocking Veto Threshold (25.0%)",
                annotation_position="top left",
                annotation_font=dict(color="#FDA4AF", size=11)
            )
            fig_dep.update_layout(yaxis=dict(range=[-2, 45]))
            
            st.info("""
            💡 **Chinese Equity & Voting Power Analytical Guide:**
            * **Mercedes-Benz (Top 35.8% ➔ 37.5%)**: Geely (9.69%) + BAIC (9.98%) combined 19.67% stake yields **37.5% effective voting power at 52–55% AGM turnout, exceeding the 25% blocking minority threshold (above red dashed line)**.
            * **Volkswagen & BMW (Bottom 0.0%)**: Direct parent equity is 0%, but local joint ventures (SAIC/FAW 50:50, BBA Shenyang 75:25) create operational asset lock-in.
            * **Triad Composite Average (Middle 11.9% ➔ 12.5%)**: Aggregate parent weighting across the 3 German OEMs.
            """)
        
        fig_dep.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=420, margin=dict(l=40, r=20, t=20, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor="#1e293b", dtick=1), yaxis=dict(title=y_title, gridcolor="#1e293b")
        )
        st.plotly_chart(fig_dep, use_container_width=True)

    # --------------------------------------------------------------------------
    # LEVEL 3: 6-DIMENSION HIGH-CONTRAST RADAR
    # --------------------------------------------------------------------------
    else:
        st.markdown("#### 🕸️ 2025 German Auto Triad 6-Dimension Dependency Radar (High-Contrast Radar)")
        
        radar_display_mode = st.radio(
            "Select Radar Display Mode:",
            [
                "1. Integrated Overlay View (Mercedes Slate / VW Blue / BMW White / Avg Red)",
                "2. 3-Split Side-by-Side Cards (VW Black / Mercedes Red / BMW Yellow)"
            ],
            horizontal=True
        )
        
        radar_info = historical_deliveries.get("radarSummary2025", {})
        categories = radar_info.get("dimensions", [])
        
        if "1. Integrated Overlay View" in radar_display_mode:
            fig_radar = go.Figure()
            
            # Volkswagen: VW Deep Blue (#00439C)
            fig_radar.add_trace(go.Scatterpolar(
                r=radar_info.get("volkswagen", []),
                theta=categories,
                fill='toself',
                name='Volkswagen Group (VW Deep Blue: #00439C)',
                line=dict(color='#00439C', width=3),
                fillcolor='rgba(0, 67, 156, 0.45)'
            ))
            
            # Mercedes-Benz: Silver / Slate (#94A3B8)
            fig_radar.add_trace(go.Scatterpolar(
                r=radar_info.get("mercedes", []),
                theta=categories,
                fill='toself',
                name='Mercedes-Benz (Silver Slate: #94A3B8)',
                line=dict(color='#94A3B8', width=3),
                fillcolor='rgba(148, 163, 184, 0.35)'
            ))
            
            # BMW Group: BMW White (#FFFFFF)
            fig_radar.add_trace(go.Scatterpolar(
                r=radar_info.get("bmw", []),
                theta=categories,
                fill='toself',
                name='BMW Group (BMW White: #FFFFFF)',
                line=dict(color='#FFFFFF', width=3),
                fillcolor='rgba(255, 255, 255, 0.35)'
            ))
            
            # Triad Benchmark: Vivid Crimson Red (#F43F5E, dashed)
            fig_radar.add_trace(go.Scatterpolar(
                r=radar_info.get("triadAvg", []),
                theta=categories,
                name='Triad Composite Benchmark (Red Dash: #F43F5E)',
                line=dict(color='#F43F5E', width=3.5, dash='dash')
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    bgcolor='rgba(170, 68, 0, 0.40)',  # Dark Russet / Maroon
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255, 255, 255, 0.25)", color="#F1F5F9"),
                    angularaxis=dict(gridcolor="rgba(255, 255, 255, 0.25)", color="#FFFFFF")
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                height=460,
                margin=dict(l=50, r=50, t=30, b=40),
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        else:
            st.caption("Compares each OEM's 6-dimension profile against the Triad composite benchmark (VW: Black BG | Mercedes: Red BG | BMW: Yellow BG).")
            r_col1, r_col2, r_col3 = st.columns(3)
            
            # Subplot 1: Volkswagen (Black Background)
            with r_col1:
                st.markdown("<h5 style='text-align:center; color:#38BDF8; background:#000000; padding:6px; border-radius:6px; border:1px solid #1E3A8A;'>🏢 Volkswagen Group (Black Background)</h5>", unsafe_allow_html=True)
                fig_vw = go.Figure()
                fig_vw.add_trace(go.Scatterpolar(
                    r=radar_info.get("volkswagen", []),
                    theta=categories,
                    fill='toself',
                    name='Volkswagen Group',
                    line=dict(color='#00439C', width=3),
                    fillcolor='rgba(0, 67, 156, 0.45)'
                ))
                fig_vw.add_trace(go.Scatterpolar(
                    r=radar_info.get("triadAvg", []),
                    theta=categories,
                    name='Triad Benchmark (Red)',
                    line=dict(color='#F43F5E', width=2, dash='dash')
                ))
                fig_vw.update_layout(
                    polar=dict(bgcolor='#000000', radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(gridcolor="#334155", color="#94A3B8", tickfont=dict(size=9))),
                    paper_bgcolor="rgba(0,0,0,0)", height=320, margin=dict(l=30, r=30, t=20, b=20), showlegend=False
                )
                st.plotly_chart(fig_vw, use_container_width=True)

            # Subplot 2: Mercedes-Benz (Red Background)
            with r_col2:
                st.markdown("<h5 style='text-align:center; color:#FDA4AF; background:#4C0519; padding:6px; border-radius:6px; border:1px solid #881337;'>🏢 Mercedes-Benz Group (Red Background)</h5>", unsafe_allow_html=True)
                fig_mb = go.Figure()
                fig_mb.add_trace(go.Scatterpolar(
                    r=radar_info.get("mercedes", []),
                    theta=categories,
                    fill='toself',
                    name='Mercedes-Benz',
                    line=dict(color='#94A3B8', width=3),
                    fillcolor='rgba(148, 163, 184, 0.35)'
                ))
                fig_mb.add_trace(go.Scatterpolar(
                    r=radar_info.get("triadAvg", []),
                    theta=categories,
                    name='Triad Benchmark (White)',
                    line=dict(color='#FFFFFF', width=2, dash='dash')
                ))
                fig_mb.update_layout(
                    polar=dict(bgcolor='rgba(185, 28, 28, 0.35)', radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(gridcolor="#881337", color="#FDA4AF", tickfont=dict(size=9))),
                    paper_bgcolor="rgba(0,0,0,0)", height=320, margin=dict(l=30, r=30, t=20, b=20), showlegend=False
                )
                st.plotly_chart(fig_mb, use_container_width=True)

            # Subplot 3: BMW Group (Yellow Background)
            with r_col3:
                st.markdown("<h5 style='text-align:center; color:#FDE047; background:#422006; padding:6px; border-radius:6px; border:1px solid #A16207;'>🏢 BMW Group (Yellow Background)</h5>", unsafe_allow_html=True)
                fig_bmw_r = go.Figure()
                fig_bmw_r.add_trace(go.Scatterpolar(
                    r=radar_info.get("bmw", []),
                    theta=categories,
                    fill='toself',
                    name='BMW Group',
                    line=dict(color='#FFFFFF', width=3),
                    fillcolor='rgba(255, 255, 255, 0.35)'
                ))
                fig_bmw_r.add_trace(go.Scatterpolar(
                    r=radar_info.get("triadAvg", []),
                    theta=categories,
                    name='Triad Benchmark (Red)',
                    line=dict(color='#F43F5E', width=2, dash='dash')
                ))
                fig_bmw_r.update_layout(
                    polar=dict(bgcolor='rgba(202, 138, 4, 0.35)', radialaxis=dict(visible=False, range=[0, 100]), angularaxis=dict(gridcolor="#A16207", color="#FDE047", tickfont=dict(size=9))),
                    paper_bgcolor="rgba(0,0,0,0)", height=320, margin=dict(l=30, r=30, t=20, b=20), showlegend=False
                )
                st.plotly_chart(fig_bmw_r, use_container_width=True)

    # 3 Red Threat Metric Alerts
    c1, c2, c3 = st.columns(3)
    with c1:
        st.error("📉 **Delivery Collapse (Critical)**: 2019: 5.65M units ➔ 2025: 4.06M units (**-1.59M units / -28.1% plunge**)")
    with c2:
        st.error("📉 **Market Share Halved (Critical)**: 2019: 25.1% ➔ 2025: 12.8% (**-12.3%p share erosion**)")
    with c3:
        st.error("📉 **China EBIT Collapse (Critical)**: 2019: €15.2B ➔ 2025: €7.9B (**-48.0% profit halved**)")

    # ==========================================================================
    # COMPREHENSIVE 2019-2025 FULL TIME-SERIES AUDIT DATA TABLE (VALUE-BASED DYNAMIC HEATMAP)
    # ==========================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 2019–2025 Continuous Time-Series Comprehensive Audit Matrix")
    st.caption("🎨 **Value-Based Dynamic Diverging Heatmap**: Cells dynamically map values relative to the metric 7-year mean. Safe/peak historical levels render in **🟦 Blue**, midpoint means render in **⬜ White**, and severe risk metrics transition continuously into **🟥 Deep Crimson Red**.")

    def compute_cell_color(val, val_list, higher_is_better=True):
        avg = sum(val_list) / len(val_list)
        min_v = min(val_list)
        max_v = max(val_list)
        if max_v == min_v:
            return "background: #FFFFFF; color: #0F172A; font-weight: bold; border: 1.5px solid #CBD5E1;"

        if higher_is_better:
            if val >= avg:
                t = (val - avg) / (max_v - avg) if max_v > avg else 0.0
            else:
                t = -(avg - val) / (avg - min_v) if avg > min_v else 0.0
        else:
            if val <= avg:
                t = (avg - val) / (avg - min_v) if avg > min_v else 0.0
            else:
                t = -(val - avg) / (max_v - avg) if max_v > avg else 0.0

        if t > 0: # White -> Blue
            r = int(255 - t * (255 - 30))
            g = int(255 - t * (255 - 64))
            b = int(255 - t * (255 - 175))
            text_color = "#FFFFFF" if t > 0.45 else "#0F172A"
            font_weight = "900" if t > 0.6 else "bold"
        elif t < 0: # White -> Red
            s = abs(t)
            r = int(255 - s * (255 - 190))
            g = int(255 - s * (255 - 18))
            b = int(255 - s * (255 - 60))
            text_color = "#FFFFFF" if s > 0.45 else "#881337"
            font_weight = "900" if s > 0.6 else "bold"
        else: # Exactly Mean / Midpoint
            r, g, b = 255, 255, 255
            text_color = "#0F172A"
            font_weight = "900"

        border = "border: 2px solid #94A3B8;" if abs(t) < 0.15 else "border: 1px solid rgba(0,0,0,0.12);"
        return f"background: rgb({r}, {g}, {b}); color: {text_color}; font-weight: {font_weight}; {border}"

    table_metrics_data = [
        # SECTION 1
        {"type": "header", "title": "📈 1. Basic Market Performance Time-Series (2019–2025)"},
        {
            "name": "• Volkswagen China Deliveries (k units)",
            "values": [4233, 3850, 3300, 3180, 3236, 2980, 2780],
            "display": ["4,233", "3,850", "3,300", "3,180", "3,236", "2,980", "2,780"],
            "higher_is_better": True,
            "delta": "-1,453 (-34.3%)",
            "badge": "🔴 Severe Plunge",
            "badge_style": "background: #4C0519; color: #FDA4AF; border: 1px solid #881337;"
        },
        {
            "name": "• Mercedes-Benz China Deliveries (k units)",
            "values": [693, 774, 758, 751, 737, 675, 630],
            "display": ["693", "774", "758", "751", "737", "675", "630"],
            "higher_is_better": True,
            "delta": "-63 (-9.1%)",
            "badge": "🟠 Margin Hostage",
            "badge_style": "background: #431407; color: #FDBA74; border: 1px solid #9A3412;"
        },
        {
            "name": "• BMW Group China Deliveries (k units)",
            "values": [724, 777, 846, 792, 825, 705, 650],
            "display": ["724", "777", "846", "792", "825", "705", "650"],
            "higher_is_better": True,
            "delta": "-74 (-10.2%)",
            "badge": "🟠 Share Encroached",
            "badge_style": "background: #431407; color: #FDBA74; border: 1px solid #9A3412;"
        },
        {
            "name": "• Triad Composite Deliveries (k units)",
            "values": [5650, 5401, 4904, 4723, 4798, 4360, 4060],
            "display": ["5,650", "5,401", "4,904", "4,723", "4,798", "4,360", "4,060"],
            "higher_is_better": True,
            "delta": "-1,590 (-28.1%)",
            "badge": "🔴 Severe Plunge",
            "badge_style": "background: #4C0519; color: #FDA4AF; border: 1px solid #881337;"
        },
        {
            "name": "• Triad China Local Production (k units)",
            "values": [5055, 4824, 4370, 4260, 4323, 3915, 3620],
            "display": ["5,055", "4,824", "4,370", "4,260", "4,323", "3,915", "3,620"],
            "higher_is_better": True,
            "delta": "-1,435 (-28.4%)",
            "badge": "🔴 Asset Sunk",
            "badge_style": "background: #4C0519; color: #FDA4AF; border: 1px solid #881337;"
        },
        {
            "name": "• Local Production Share (%)",
            "values": [89.5, 89.3, 89.1, 90.2, 90.1, 89.8, 89.2],
            "display": ["89.5%", "89.3%", "89.1%", "90.2%", "90.1%", "89.8%", "89.2%"],
            "higher_is_better": False,
            "delta": "-0.3%p (90% Lock-in)",
            "badge": "🔴 Exit Constrained",
            "badge_style": "background: #4C0519; color: #FDA4AF; border: 1px solid #881337;"
        },
        {
            "name": "• Triad China Market Share (%)",
            "values": [25.1, 24.5, 21.5, 19.8, 18.2, 15.1, 12.8],
            "display": ["25.1%", "24.5%", "21.5%", "19.8%", "18.2%", "15.1%", "12.8%"],
            "higher_is_better": True,
            "delta": "-12.3%p (Halved)",
            "badge": "🔴 Share Collapse",
            "badge_style": "background: #4C0519; color: #FDA4AF; border: 1px solid #881337;"
        },
        {
            "name": "• China NEV Penetration Rate (%)",
            "values": [4.9, 5.8, 15.5, 27.8, 35.7, 47.5, 53.5],
            "display": ["4.9%", "5.8%", "15.5%", "27.8%", "35.7%", "47.5%", "53.5%"],
            "higher_is_better": False,
            "delta": "+48.6%p (Surge)",
            "badge": "🔴 ICE Displaced",
            "badge_style": "background: #4C0519; color: #FDA4AF; border: 1px solid #881337;"
        },
        # SECTION 2
        {"type": "header", "title": "📐 2. 6 Measurable Dependency Time-Series (2019–2025)"},
        {
            "name": "1. China EBIT Contribution Share (%)",
            "values": [37.8, 39.2, 40.8, 37.6, 35.2, 33.5, 32.7],
            "display": ["37.8%", "39.2%", "40.8%", "37.6%", "35.2%", "33.5%", "32.7%"],
            "higher_is_better": False,
            "delta": "-5.1%p (-€7.3B Halved)",
            "badge": "🔴 Margin Hostage",
            "badge_style": "background: #4C0519; color: #FDA4AF; border: 1px solid #881337;"
        },
        {
            "name": "2. Chinese Component Cost Share (BOM %)",
            "values": [32.0, 36.5, 40.2, 44.5, 47.0, 48.8, 49.5],
            "display": ["32.0%", "36.5%", "40.2%", "44.5%", "47.0%", "48.8%", "49.5%"],
            "higher_is_better": False,
            "delta": "+17.5%p (Surge)",
            "badge": "🔴 BOM Dependent",
            "badge_style": "background: #4C0519; color: #FDA4AF; border: 1px solid #881337;"
        },
        {
            "name": "3. Chinese Supplier Concentration (CR3 %)",
            "values": [45.0, 52.0, 61.5, 68.0, 72.0, 74.2, 75.5],
            "display": ["45.0%", "52.0%", "61.5%", "68.0%", "72.0%", "74.2%", "75.5%"],
            "higher_is_better": False,
            "delta": "+30.5%p (Monopoly)",
            "badge": "🔴 Supply Captive",
            "badge_style": "background: #4C0519; color: #FDA4AF; border: 1px solid #881337;"
        },
        {
            "name": "4. Local Data Isolation Ratio (%)",
            "values": [25.0, 45.0, 85.0, 95.0, 100.0, 100.0, 100.0],
            "display": ["25.0%", "45.0%", "85.0%", "95.0%", "100.0%", "100.0%", "100.0%"],
            "higher_is_better": False,
            "delta": "+75.0%p (0% Exfil)",
            "badge": "🔴 Data Blockade",
            "badge_style": "background: #4C0519; color: #FDA4AF; border: 1px solid #881337;"
        },
        {
            "name": "5. Chinese Equity & Effective Voting Power (%)",
            "values": [11.9, 12.1, 12.2, 12.3, 12.4, 12.5, 12.5],
            "display": ["11.9%", "12.1%", "12.2%", "12.3%", "12.4%", "12.5%", "12.5%"],
            "higher_is_better": False,
            "delta": "+0.6%p (MB 37.5%)",
            "badge": "🔴 Veto Captured",
            "badge_style": "background: #4C0519; color: #FDA4AF; border: 1px solid #881337;"
        },
        {
            "name": "6. Non-China Replacement Lead Time (Years)",
            "values": [1.5, 2.0, 2.7, 3.2, 3.7, 4.0, 4.2],
            "display": ["1.5 yrs", "2.0 yrs", "2.7 yrs", "3.2 yrs", "3.7 yrs", "4.0 yrs", "4.2 yrs"],
            "higher_is_better": False,
            "delta": "+2.7 yrs (50 mos)",
            "badge": "🔴 Irreplaceable",
            "badge_style": "background: #4C0519; color: #FDA4AF; border: 1px solid #881337;"
        }
    ]

    table_rows_html = []
    for item in table_metrics_data:
        if item.get("type") == "header":
            table_rows_html.append(f"""<tr style="background: #0B1329; border-top: 2px solid #475569; border-bottom: 1px solid #1E293B;">
<td colspan="10" style="padding: 8px 14px; text-align: left; font-weight: 800; color: #38BDF8; font-family: 'Plus Jakarta Sans', sans-serif;">{item['title']}</td>
</tr>""")
        else:
            cells = []
            vals = item["values"]
            disp = item["display"]
            hib = item["higher_is_better"]
            for v, d in zip(vals, disp):
                style = compute_cell_color(v, vals, hib)
                cells.append(f'<td style="padding: 8px; {style}">{d}</td>')
            cells_str = "\n".join(cells)
            badge = item["badge"]
            b_style = item["badge_style"]
            delta = item["delta"]
            table_rows_html.append(f"""<tr style="border-bottom: 1px solid #334155;">
<td style="padding: 10px 14px; text-align: left; font-weight: bold; color: #F8FAFC; font-family: 'Plus Jakarta Sans', sans-serif;">{item['name']}</td>
{cells_str}
<td style="padding: 8px; color: #FDA4AF; text-align: center; font-weight: bold; background: #0F172A;">{delta}</td>
<td style="padding: 8px; text-align: center; background: #0F172A;"><span style="{b_style} padding: 3px 8px; border-radius: 4px; font-weight: bold;">{badge}</span></td>
</tr>""")

    full_table_html = f"""<div style="overflow-x: auto; margin-bottom: 2rem; border-radius: 12px; border: 1px solid #475569;">
<table style="width: 100%; border-collapse: collapse; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; text-align: right;">
<thead>
<tr style="border-bottom: 2px solid #64748B; text-align: center; background: #020617; color: #94A3B8;">
<th style="padding: 12px 14px; text-align: left; font-family: 'Plus Jakarta Sans', sans-serif; min-width: 210px; color: #F8FAFC;">Metric Description</th>
<th style="padding: 10px 8px; color: #CBD5E1;">2019</th>
<th style="padding: 10px 8px; color: #CBD5E1;">2020</th>
<th style="padding: 10px 8px; color: #CBD5E1;">2021</th>
<th style="padding: 10px 8px; color: #CBD5E1;">2022</th>
<th style="padding: 10px 8px; color: #CBD5E1;">2023</th>
<th style="padding: 10px 8px; color: #CBD5E1;">2024</th>
<th style="padding: 10px 8px; color: #CBD5E1;">2025</th>
<th style="padding: 10px 12px; background: #0F172A; color: #F8FAFC; text-align: center;">2019–2025 Delta</th>
<th style="padding: 10px 12px; background: #0F172A; color: #F8FAFC; text-align: center;">Risk Status</th>
</tr>
</thead>
<tbody>
{"".join(table_rows_html)}
</tbody>
</table>
</div>"""
    st.markdown(full_table_html, unsafe_allow_html=True)

    # 6 MEASURABLE DEPENDENCY DIMENSIONS MATRIX TABLE (RED HIGH-SEVERITY THEME)
    st.markdown("### 📐 Triad 6-Dimension Quantitative Dependency Matrix (2025 Audit Baseline)")
    st.caption("💡 Formal audit matrix parameterizing 'Dependency' into **6 measurable statutory dimensions (EBIT Share, BOM Cost, Supplier CR3, Data Isolation, Voting Power, and Replacement Lead Time)**.")

    dep_matrix_html = """<div style="overflow-x: auto; margin-bottom: 1.5rem; border-radius: 12px; border: 1px solid #881337;">
<table style="width: 100%; border-collapse: collapse; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.82rem; text-align: left;">
<thead>
<tr style="background: #020617; color: #94A3B8; border-bottom: 2px solid #881337;">
<th style="padding: 12px 14px; width: 22%;">Dimension</th>
<th style="padding: 12px 14px; width: 20%; color: #CBD5E1;">Mercedes-Benz Group</th>
<th style="padding: 12px 14px; width: 20%; color: #38BDF8;">Volkswagen Group</th>
<th style="padding: 12px 14px; width: 20%; color: #FFFFFF;">BMW Group</th>
<th style="padding: 12px 14px; width: 18%; color: #FDA4AF;">Triad Composite Avg</th>
</tr>
</thead>
<tbody>
<tr style="border-bottom: 1px solid #1E293B; background: #0F172A;">
<td style="padding: 12px 14px; font-weight: bold; color: #F8FAFC;">1. China EBIT Share</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.4);">31.5% (€2.40B S-Class Concentration)</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.6);">38.0% (JV Equity Method Concentration)</td>
<td style="padding: 12px 14px; color: #FED7AA; background: rgba(67, 20, 7, 0.4);">28.5% (Shenyang BBA Operating Concentration)</td>
<td style="padding: 12px 14px; font-weight: bold; color: #FDA4AF; background: rgba(76, 5, 25, 0.8);">32.7% (Persistent Lock-in)</td>
</tr>
<tr style="border-bottom: 1px solid #1E293B; background: #0F172A;">
<td style="padding: 12px 14px; font-weight: bold; color: #F8FAFC;">2. Chinese Component BOM Cost</td>
<td style="padding: 12px 14px; color: #FED7AA; background: rgba(67, 20, 7, 0.4);">42.0% (CATL Cells + Local Electrics)</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.8); font-weight: bold;">58.5% (92.8% Domestic Sourced in Fabs)</td>
<td style="padding: 12px 14px; color: #FED7AA; background: rgba(67, 20, 7, 0.5);">48.0% (Shenyang iX3 & CATL Battery Packs)</td>
<td style="padding: 12px 14px; font-weight: bold; color: #FDA4AF; background: rgba(76, 5, 25, 0.8);">49.5% (Surged from 32% in 2019)</td>
</tr>
<tr style="border-bottom: 1px solid #1E293B; background: #0F172A;">
<td style="padding: 12px 14px; font-weight: bold; color: #F8FAFC;">3. Chinese Supplier Concentration (CR3)</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.5);">68.0% (CATL, Momenta, BAIC Electronics)</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.7);">76.5% (CATL, Gotion, XPENG, SAIC)</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.9); font-weight: bold;">82.0% (CATL & EVE Energy Duopoly)</td>
<td style="padding: 12px 14px; font-weight: bold; color: #FDA4AF; background: rgba(76, 5, 25, 0.8);">75.5% (Upstream Monopolization)</td>
</tr>
<tr style="border-bottom: 1px solid #1E293B; background: #0F172A;">
<td style="padding: 12px 14px; font-weight: bold; color: #F8FAFC;">4. Local Data Isolation Ratio</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.8);">100.0% (DSL Statutory Local Air-gap)</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.8);">100.0% (Hefei VCTC Cloud Isolation)</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.8);">100.0% (Shenyang Server 100% Retained)</td>
<td style="padding: 12px 14px; font-weight: bold; color: #FDA4AF; background: rgba(76, 5, 25, 0.9);">100.0% (0% Outbound Telemetry Allowed)</td>
</tr>
<tr style="border-bottom: 1px solid #1E293B; background: #0F172A;">
<td style="padding: 12px 14px; font-weight: bold; color: #F8FAFC;">5. Chinese Equity & Voting Power</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.9); font-weight: bold;">19.67% Stake / 37.5% AGM Effective Veto</td>
<td style="padding: 12px 14px; color: #CBD5E1; background: rgba(15, 23, 42, 0.6);">0% Parent Equity / JV Operational Lock-in</td>
<td style="padding: 12px 14px; color: #FED7AA; background: rgba(67, 20, 7, 0.4);">0% Parent Equity / €3.73B Sunk BBA Stake</td>
<td style="padding: 12px 14px; font-weight: bold; color: #FDA4AF; background: rgba(76, 5, 25, 0.8);">12.5% Parent Avg (MB >25% Veto Held)</td>
</tr>
<tr style="background: #0F172A;">
<td style="padding: 12px 14px; font-weight: bold; color: #F8FAFC;">6. Non-China Replacement Lead Time</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.6);">36 to 48 Months (3–4 Years)</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.8); font-weight: bold;">48 to 60 Months (4–5 Years)</td>
<td style="padding: 12px 14px; color: #FDA4AF; background: rgba(76, 5, 25, 0.7);">42 to 54 Months (3.5–4.5 Years)</td>
<td style="padding: 12px 14px; font-weight: bold; color: #FDA4AF; background: rgba(76, 5, 25, 0.9);">4.2 Years (Protracted Rebalancing)</td>
</tr>
</tbody>
</table>
</div>"""
    st.markdown(dep_matrix_html, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: TRIAD ENCROACHMENT & HOSTAGE DILEMMAS
# ==============================================================================
with tab2:
    st.markdown("### 🏢 Triad Asymmetric Encroachment Mechanisms & Corporate Hostage Dilemmas (2025 Baseline)")
    st.caption("🔴 All structural vulnerabilities (Equity Collar Capture, Software Subcontracting, Battery Captive Supply) represent **Critical Operational Threats**.")
    
    for oem in triad_oems:
        st.markdown(f"""
        <div style="background: #0F172A; border: 1.5px solid #881337; border-radius: 14px; padding: 1.3rem; margin-bottom: 1.3rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1E293B; padding-bottom: 0.6rem; margin-bottom: 0.8rem;">
                <span style="font-size: 1.15rem; font-weight: 800; color: #F8FAFC;">{oem['name']} — {oem['trapType']}</span>
                <span style="font-size: 0.75rem; background: #4C0519; color: #FDA4AF; padding: 4px 10px; border-radius: 6px; font-weight: 800; border: 1px solid #881337; font-family: monospace;">
                    🔴 CRITICAL THREAT: {oem['trapTag']}
                </span>
            </div>
            <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.6; margin-bottom: 0.8rem;">
                <strong>• Local Production vs. Deliveries:</strong> <span style="color:#FCD34D;">{oem['localProductionVsSales']}</span><br>
                <strong>• Shareholder &amp; Equity Structure:</strong> <span style="color:#F43F5E; font-weight:bold;">{oem['shareholderStructure']}</span><br>
                <strong>• Vulnerability Summary:</strong> {oem['encroachmentSummary']}
            </div>
            <div style="font-size: 0.83rem; color: #FDA4AF; background: #4C0519; padding: 12px 14px; border-radius: 8px; margin-bottom: 0.6rem; border: 1px solid #881337; line-height: 1.5;">
                🔴 <strong>Corporate Hostage &amp; Compliance Dilemma:</strong> {oem['appeasementBehavior']}
            </div>
            <div style="font-size: 0.72rem; color: #94A3B8; border-top: 1px solid #1E293B; padding-top: 6px; font-family: monospace;">
                📑 <strong>Regulatory Source:</strong> {oem['metadata']['source']} [{oem['metadata']['confidenceScore']}] • <strong>Base Date:</strong> {oem['metadata']['baseDate']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 3: IDAR STRATEGY & ASYMMETRIC OPENNESS
# ==============================================================================
with tab3:
    st.markdown("### 🏛️ China's 'Asymmetric Openness & IDAR (Introduce, Digest, Absorb, Re-innovate)' Strategy Framework")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown(f"""
        <div style="background: #0F172A; border: 1px solid #881337; border-radius: 12px; padding: 1.2rem; height: 100%;">
            <h4 style="color: #FDA4AF; margin: 0 0 0.5rem 0;">1. {idar_data['coreConcepts']['stateLedMercantilism']['name']}</h4>
            <p style="font-size: 0.83rem; color: #CBD5E1; line-height: 1.5;">
                {idar_data['coreConcepts']['stateLedMercantilism']['definition']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_c2:
        st.markdown(f"""
        <div style="background: #0F172A; border: 1px solid #D97706; border-radius: 12px; padding: 1.2rem; height: 100%;">
            <h4 style="color: #FCD34D; margin: 0 0 0.5rem 0;">2. {idar_data['coreConcepts']['asymmetricOpenness']['name']}</h4>
            <div style="font-size: 0.8rem; font-mono; font-weight: bold; color: #F59E0B; margin-bottom: 0.4rem;">
                "{idar_data['coreConcepts']['asymmetricOpenness']['slogan']}"
            </div>
            <p style="font-size: 0.8rem; color: #CBD5E1; line-height: 1.5;">
                {idar_data['coreConcepts']['asymmetricOpenness']['mechanism']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 🔄 IDAR 3-Phase Process")
    id_c1, id_c2, id_c3 = st.columns(3)
    for idx, (col, phase) in enumerate(zip([id_c1, id_c2, id_c3], idar_data['coreConcepts']['idarStrategy']['phases'])):
        with col:
            st.markdown(f"""
            <div style="background: #070B12; border: 1px solid #1E293B; border-radius: 10px; padding: 1rem;">
                <span style="font-size: 0.72rem; font-mono; background: #0F172A; color: #38BDF8; padding: 2px 6px; border-radius: 4px; font-weight: 700;">{phase['step']}</span>
                <h4 style="color: #F8FAFC; margin: 0.4rem 0 0.3rem 0;">{phase['name']}</h4>
                <p style="font-size: 0.8rem; color: #94A3B8; line-height: 1.4;">{phase['detail']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("#### 📥 Inbound Absorption: 3 Core Mechanisms & Landmark Case Studies")
    for mech in idar_data['inboundMechanisms']:
        with st.expander(f"📌 {mech['mechanism']}", expanded=True):
            st.markdown(f"**Strategic Method:** {mech['method']}")
            st.markdown("**Landmark Case Studies:**")
            for c in mech['cases']:
                if 'sector' in c:
                    st.markdown(f"- **[{c['sector']}] {c['example']}**: {c['result']}")
                elif 'company' in c:
                    st.markdown(f"- **[M&A] {c['company']} (Acquirer: {c['buyer']})**: {c['impact']}")
                elif 'policy' in c:
                    st.markdown(f"- **[Subsidy] {c['policy']} (Target: {c['target']})**: {c['impact']}")

    st.markdown("#### 🔒 Outbound Lockdown: 4 Legal Statutes Blocking Critical IP & Asset Repatriation")
    out_c1, out_c2 = st.columns(2)
    for idx, stat in enumerate(idar_data['outboundLegalStatutes']):
        target_col = out_c1 if idx % 2 == 0 else out_c2
        with target_col:
            with st.expander(f"⚖️ {stat['name']} — [{stat['enactment']}]", expanded=True):
                st.markdown(f"**Statutory Mandate:** {stat['coreContent']}")
                st.markdown("**Controlled Categories:**")
                for item in stat['restrictedTech']:
                    st.markdown(f"- **{item['item']}**: {item['detail']}")

    st.markdown("#### 💡 Systemic Weaponization & De-risking Takeaways")
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.markdown(f"""
        <div style="background: #0F172A; border: 1px solid #881337; border-radius: 12px; padding: 1.2rem; height: 100%;">
            <h4 style="color: #FDA4AF; margin: 0 0 0.5rem 0;">{idar_data['executiveTakeaways']['systemicWeaponization']['title']}</h4>
            <p style="font-size: 0.83rem; color: #CBD5E1; line-height: 1.6;">
                {idar_data['executiveTakeaways']['systemicWeaponization']['explanation']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with t_col2:
        st.markdown(f"""
        <div style="background: #0F172A; border: 1px solid #065F46; border-radius: 12px; padding: 1.2rem; height: 100%;">
            <h4 style="color: #6EE7B7; margin: 0 0 0.5rem 0;">{idar_data['executiveTakeaways']['deriskingRootCause']['title']}</h4>
            <p style="font-size: 0.83rem; color: #CBD5E1; line-height: 1.6;">
                {idar_data['executiveTakeaways']['deriskingRootCause']['explanation']}
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: TECHNOLOGY EXFILTRATION & REVERSE FLOW DYNAMICS
# ==============================================================================
with tab4:
    st.markdown("### 🔄 Technology Exfiltration & Reverse Flow Dynamics: Historical Transfer (1984–2020) vs. Present Competition (2025)")
    
    dims = technology_flow_data["historicalVsPresent"]["dimensions"]
    df_dims = pd.DataFrame([
        {
            "Domain": d["dimension"],
            "Severity": d.get("severityTag", "🔴 Critical"),
            "Historical Cooperation (1984–2020)": d["pastCooperation"],
            "Present Competition (2025)": d["presentCompetition"]
        }
        for d in dims
    ])
    st.table(df_dims)
    
    st.markdown("#### 🔬 5 Core Technological Domains: Empirical Evidence Breakdown")
    doms = technology_flow_data["domainSpecificEvidence"]
    for d in doms:
        sev = d.get("severity", "critical")
        card_border = "#881337" if sev == "critical" else "#9A3412" if sev == "moderate" else "#713F12"
        card_bg = "#4C0519" if sev == "critical" else "#431407" if sev == "moderate" else "#422006"
        tag_text_color = "#FDA4AF" if sev == "critical" else "#FDBA74" if sev == "moderate" else "#FDE047"
        
        with st.expander(f"📌 {d['domain']} — [{d.get('severityTag', '🔴 Critical')}]", expanded=True):
            col_eu, col_cn = st.columns(2)
            with col_eu:
                st.markdown(f"**🇪🇺 European Status & Residual Competitiveness:**\n\n{d['europeStatus']}")
            with col_cn:
                st.markdown(f"**🇨🇳 Chinese Dominance & Supply Chain Capture:**\n\n{d['chinaStatus']}")
            
            st.markdown(f"""
            <div style="background: {card_bg}; border: 1px solid {card_border}; border-radius: 8px; padding: 10px 14px; margin-top: 8px;">
                <strong style="color: {tag_text_color}; font-size: 0.85rem;">Strategic Flow Reversal Conclusion:</strong>
                <span style="color: #F8FAFC; font-size: 0.83rem; margin-left: 6px;">{d['flowDirection']}</span>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# TAB 5: 3 SCENARIOS & 2026–2035 10-YEAR FORECAST ENGINE
# ==============================================================================
with tab5:
    st.markdown("### 🔀 3 Strategic Bifurcation Scenarios & 2026–2035 10-Year Simulation Engine")
    st.caption("💡 Toggle preset buttons or adjust the 6 active policy levers below to recalculate real-time EBIT margins, AktG §179 blocking veto status, and 10-year dynamic trajectories.")
    
    preset_col1, preset_col2, preset_col3 = st.columns(3)
    
    if 'dilution_val' not in st.session_state:
        st.session_state.dilution_val = 15
        st.session_state.turnout_val = 85
        st.session_state.shock_val = 15
        st.session_state.mineral_val = 20
        st.session_state.bev_val = 120
        st.session_state.tariff_val = 21

    with preset_col1:
        if st.button("🔴 Scenario A: Status Quo Preset (2035 Subcontractor Decline)", use_container_width=True):
            st.session_state.dilution_val = 0
            st.session_state.turnout_val = 52
            st.session_state.shock_val = 5
            st.session_state.mineral_val = 5
            st.session_state.bev_val = 80
            st.session_state.tariff_val = 10
            st.rerun()

    with preset_col2:
        if st.button("🟢 Scenario B: Phased De-risking Preset (2035 Sovereignty Recovery: Recommended)", use_container_width=True):
            st.session_state.dilution_val = 15
            st.session_state.turnout_val = 85
            st.session_state.shock_val = 15
            st.session_state.mineral_val = 20
            st.session_state.bev_val = 120
            st.session_state.tariff_val = 21
            st.rerun()

    with preset_col3:
        if st.button("🔵 Scenario C: Abrupt Decoupling Preset (2026-28 Liquidity Crisis)", use_container_width=True):
            st.session_state.dilution_val = 30
            st.session_state.turnout_val = 90
            st.session_state.shock_val = 40
            st.session_state.mineral_val = 35
            st.session_state.bev_val = 200
            st.session_state.tariff_val = 35
            st.rerun()

    st.markdown("#### 🎛️ Real-Time Policy Simulation Levers (6 Active Controls)")
    calc_c1, calc_c2, calc_c3 = st.columns(3)
    with calc_c1:
        in_dilution = st.slider("1. Strategic Capital Dilution (% New Shares Issued)", min_value=0, max_value=45, value=st.session_state.dilution_val, step=5)
        in_turnout = st.slider("2. Allied Proxy Turnout (85%+ Mobilization Drives Total 69%+) (%)", min_value=50, max_value=95, value=st.session_state.turnout_val, step=1)
    with calc_c2:
        in_china_shock = st.slider("3. China Sales Volume Shock (%)", min_value=5, max_value=50, value=st.session_state.shock_val, step=5)
        in_mineral_prem = st.slider("4. Non-China Mineral Cost Premium (%)", min_value=5, max_value=40, value=st.session_state.mineral_val, step=5)
    with calc_c3:
        in_bev_vol = st.slider("5. Triad BEV Annual Production (10k Units)", min_value=50, max_value=250, value=st.session_state.bev_val, step=10)
        in_tariff = st.slider("6. EU Countervailing Tariff Rate (%)", min_value=10, max_value=40, value=st.session_state.tariff_val, step=1)

    # Exact Real-time Calculations
    S_cn_dyn = 19.67 / (1.0 + (in_dilution / 100.0))
    S_allied_dyn = (35.0 + in_dilution) / (1.0 + (in_dilution / 100.0))
    S_float_dyn = 45.33 / (1.0 + (in_dilution / 100.0))
    
    tot_turnout = (S_cn_dyn * 1.0) + (S_allied_dyn * (in_turnout / 100.0)) + (S_float_dyn * 0.38)
    eff_cn_power = (S_cn_dyn * 1.0 / tot_turnout) * 100.0
    veto_held = eff_cn_power >= 25.00000

    unit_pack_cost = (82.0 * 128.0 * (in_mineral_prem / 100.0)) / 1.08
    tot_battery_cost_b = ((in_bev_vol * 10000) * unit_pack_cost) / 1e9
    cn_ebit_loss_b = 12.8 * (in_china_shock / 100.0) * 1.25
    tariff_hit_b = (32000 * 42500 * (in_tariff / 100.0) * 0.7) / 1e9
    
    tot_deduct_b = tot_battery_cost_b + cn_ebit_loss_b + tariff_hit_b
    adj_ebit_b = max(5.0, round(36.5 - tot_deduct_b, 2))
    adj_margin = round((adj_ebit_b / 380.0) * 100.0, 2)

    # Dynamic Path Evaluation & Severity Colors
    if adj_margin >= 7.8 and not veto_held:
        current_path_name = "Scenario B: Phased De-risking (2035 Sovereignty Recovery: Recommended)"
        current_path_tag = "🟢 STRATEGIC SWEET SPOT (OPTIMAL ROBUSTNESS)"
        current_path_color = "#10B981"
        current_path_border = "#059669"
        current_path_bg = "#064E3B"
        current_path_desc = "Controls outbound technology transfer, scales allied supply alliances, eliminates 25% blocking vetoes under AktG §179, and expands operating margins to 10.2% by 2035."
    elif adj_margin < 5.0 or in_china_shock >= 35:
        current_path_name = "Scenario C: Abrupt Decoupling (2026-2028 Liquidity Cliff)"
        current_path_tag = "🔴 HIGH-RISK CLIFF-EDGE (CRITICAL CRISIS)"
        current_path_color = "#F43F5E"
        current_path_border = "#881337"
        current_path_bg = "#4C0519"
        current_path_desc = "Abrupt volume exit and write-downs trigger a collapse in operating margins to 1.8% between 2026 and 2028, causing severe cash-flow deficits."
    else:
        current_path_name = "Scenario A: Status Quo (2035 Subcontractor Decline)"
        current_path_tag = "🔴 STATUS QUO DEPENDENCY (SEVERE CAPTURE)"
        current_path_color = "#F43F5E"
        current_path_border = "#881337"
        current_path_bg = "#4C0519"
        current_path_desc = "Persistent 25% supermajority veto entrenches corporate dependency; loss of software and battery leadership halves operating margins to 4.2% by 2035."

    # Dynamic Combined Scenario Card
    st.markdown(f"""
    <div style="background: #0F172A; border: 2px solid {current_path_color}; border-radius: 14px; padding: 1.3rem; margin-top: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1E293B; padding-bottom: 0.5rem; margin-bottom: 0.8rem;">
            <div>
                <span style="font-size: 0.75rem; font-family: monospace; color: {current_path_color}; font-weight: 800; background: {current_path_bg}; padding: 4px 10px; border-radius: 6px; border: 1px solid {current_path_border};">
                    {current_path_tag}
                </span>
                <h3 style="color: #FFFFFF; margin: 0.4rem 0 0 0; font-size: 1.2rem;">{current_path_name}</h3>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 0.75rem; color: #E2E8F0;">Simulated EBIT &amp; Margin:</span>
                <div style="font-size: 1.45rem; font-weight: 800; color: {'#34D399' if adj_margin>=7.8 else '#F43F5E'}; font-family: monospace;">
                    €{adj_ebit_b:.1f}B <span style="font-size: 0.95rem; color: #FFFFFF;">({adj_margin:.2f}%)</span>
                </div>
            </div>
        </div>
        <p style="font-size: 0.85rem; color: #E2E8F0; line-height: 1.5; margin-bottom: 1rem;">
            {current_path_desc}
        </p>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; text-align: center;">
            <div style="background: #070B12; padding: 12px; border-radius: 8px; border: 1px solid #1E293B;">
                <div style="font-size: 0.72rem; color: #FFFFFF; font-weight: bold;">1. Adjusted Total EBIT</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: {'#34D399' if adj_margin>=7.8 else '#F43F5E'}; font-family: monospace; margin-top: 2px;">
                    €{adj_ebit_b:.1f}B
                </div>
                <div style="font-size: 0.68rem; color: {'#FDA4AF' if tot_deduct_b>5 else '#FFFFFF'};">Deductions: -€{tot_deduct_b:.2f}B</div>
            </div>
            <div style="background: #070B12; padding: 12px; border-radius: 8px; border: 1px solid #1E293B;">
                <div style="font-size: 0.72rem; color: #FFFFFF; font-weight: bold;">2. Chinese Effective Voting Power</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: {'#F43F5E' if veto_held else '#34D399'}; font-family: monospace; margin-top: 2px;">
                    {eff_cn_power:.2f}%
                </div>
                <div style="font-size: 0.68rem; color: {'#FDA4AF' if veto_held else '#6EE7B7'};">Total Turnout: {tot_turnout:.1f}% (Stake {S_cn_dyn:.2f}%)</div>
            </div>
            <div style="background: #070B12; padding: 12px; border-radius: 8px; border: 1px solid #1E293B;">
                <div style="font-size: 0.72rem; color: #FFFFFF; font-weight: bold;">3. Battery Cost Surcharge</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: {'#F97316' if unit_pack_cost>1500 else '#FFFFFF'}; font-family: monospace; margin-top: 2px;">
                    +€{unit_pack_cost:.0f}
                </div>
                <div style="font-size: 0.68rem; color: #FFFFFF;">Total: -€{tot_battery_cost_b:.2f}B</div>
            </div>
            <div style="background: #070B12; padding: 12px; border-radius: 8px; border: 1px solid #1E293B;">
                <div style="font-size: 0.72rem; color: #FFFFFF; font-weight: bold;">4. AktG §179 Veto Status</div>
                <div style="font-size: 1.05rem; font-weight: 800; color: {'#F43F5E' if veto_held else '#34D399'}; margin-top: 4px;">
                    {'🔴 25% Veto Active (High Risk)' if veto_held else '🟢 25% Veto Eliminated (Safe)'}
                </div>
                <div style="font-size: 0.68rem; color: #FFFFFF;">Threshold: &lt;25.00% Required</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # ONE-CLICK EXECUTIVE BOARD BRIEFING PDF GENERATOR MODULE
    # ==========================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    pdf_c1, pdf_c2 = st.columns([3, 2])
    with pdf_c1:
        st.markdown("""
        <div style="background: #0F172A; border: 1px solid #334155; border-radius: 10px; padding: 12px 16px;">
            <div style="font-size: 0.88rem; font-weight: bold; color: #F8FAFC; display: flex; align-items: center; gap: 8px;">
                <span>📄 One-Click Executive Board Briefing Dossier (PDF Export)</span>
            </div>
            <div style="font-size: 0.76rem; color: #94A3B8; margin-top: 3px; line-height: 1.4;">
                Instant multi-page vector PDF export reflecting your current 6 active slider parameters, AktG §179 voting thresholds, 2019–2025 audited tables, and 6-point board supervisory checklist.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with pdf_c2:
        try:
            pdf_bytes = generate_board_briefing_pdf({
                'adjusted_ebit': adj_ebit_b,
                'margin_pct': adj_margin,
                'effective_cn_power': eff_cn_power,
                'blocking_veto': veto_held,
                'dilution_pct': in_dilution,
                'allied_turnout': in_turnout,
                'china_volume_shock': in_china_shock,
                'mineral_premium': in_mineral_prem,
                'bev_volume': in_bev_vol * 10000,
                'tariff_rate': in_tariff,
                'unit_pack_penalty': unit_pack_cost,
                'total_battery_penalty_b': tot_battery_cost_b,
                'china_ebit_loss_b': cn_ebit_loss_b,
                'tariff_loss_b': tariff_hit_b,
                'total_turnout': tot_turnout,
                's_cn': S_cn_dyn
            })
            st.download_button(
                label="📥 Download Executive Briefing (PDF)",
                data=pdf_bytes,
                file_name=f"Executive_Board_Briefing_Dossier_2026_2035_{'SweetSpot' if not veto_held and adj_margin>=7.8 else 'HighRisk'}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF Export Error: {e}")

    # 2026–2035 10-Year Dynamic Forecast Trajectory Chart
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📈 2026–2035 10-Year Forecast Bifurcation Trajectories")

    
    forecast_mode = st.radio(
        "Select Forecast Metric:",
        [
            "1. Global Operating EBIT Margin (%) 2026–2035",
            "2. China Market Share (%) 2026–2035",
            "3. Allied Battery Supply Chain Autonomy (%) 2026–2035"
        ],
        horizontal=True
    )

    years = list(range(2025, 2036))
    custom_traj = []
    for yr in years:
        idx = yr - 2025
        if idx == 0:
            custom_traj.append(adj_margin)
        else:
            if not veto_held and adj_margin >= 7.8:
                val = adj_margin + (10.2 - adj_margin) * (idx / 10.0)
            elif adj_margin < 5.0 or in_china_shock >= 35:
                val = max(1.5, adj_margin - 2.0 * np.exp(-idx/2.0) + 0.45 * idx)
            else:
                val = max(3.5, adj_margin - 0.42 * idx)
            custom_traj.append(round(val, 2))

    fig_future = go.Figure()
    
    if "1. Global Operating EBIT Margin" in forecast_mode:
        fig_future.add_trace(go.Scatter(
            x=df_forecast["year"], y=df_forecast["scenA_margin"],
            name="Scenario A: Status Quo (Margin Halved to 4.2%)",
            line=dict(color="#F43F5E", width=3, dash="dot")
        ))
        fig_future.add_trace(go.Scatter(
            x=df_forecast["year"], y=df_forecast["scenB_margin"],
            name="Scenario B: Phased De-risking (Margin Expands to 10.2%)",
            line=dict(color="#10B981", width=3.5)
        ))
        fig_future.add_trace(go.Scatter(
            x=df_forecast["year"], y=df_forecast["scenC_margin"],
            name="Scenario C: Abrupt Decoupling (2026-28 Cliff at 1.8%)",
            line=dict(color="#6366F1", width=2.5, dash="dash")
        ))
        fig_future.add_trace(go.Scatter(
            x=years, y=custom_traj,
            name="🎛️ Live Slider Simulated Path",
            line=dict(color="#FCD34D", width=4),
            marker=dict(size=6)
        ))
        fig_future.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=400, margin=dict(l=40, r=20, t=20, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor="#1e293b", dtick=1), yaxis=dict(title="EBIT Margin (%)", gridcolor="#1e293b")
        )

    elif "2. China Market Share" in forecast_mode:
        fig_future.add_trace(go.Scatter(
            x=df_forecast["year"], y=df_forecast["scenA_share"],
            name="Scenario A: Status Quo (Share Drops to 2.8%)",
            line=dict(color="#F43F5E", width=3, dash="dot")
        ))
        fig_future.add_trace(go.Scatter(
            x=df_forecast["year"], y=df_forecast["scenB_share"],
            name="Scenario B: Phased De-risking (Luxury Niche Defended at 8.0%)",
            line=dict(color="#10B981", width=3.5)
        ))
        fig_future.add_trace(go.Scatter(
            x=df_forecast["year"], y=df_forecast["scenC_share"],
            name="Scenario C: Abrupt Decoupling (2027 Immediate Exit 0.3%)",
            line=dict(color="#6366F1", width=2.5, dash="dash")
        ))
        fig_future.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=400, margin=dict(l=40, r=20, t=20, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor="#1e293b", dtick=1), yaxis=dict(title="China Market Share (%)", gridcolor="#1e293b")
        )

    else:
        fig_future.add_trace(go.Scatter(
            x=df_forecast["year"], y=df_forecast["scenA_batteryAutonomy"],
            name="Scenario A: Status Quo (100% CATL Lock-in: 35%)",
            line=dict(color="#F43F5E", width=3, dash="dot")
        ))
        fig_future.add_trace(go.Scatter(
            x=df_forecast["year"], y=df_forecast["scenB_batteryAutonomy"],
            name="Scenario B: Phased De-risking (Allied Supply Reaches 95%)",
            line=dict(color="#10B981", width=3.5)
        ))
        fig_future.add_trace(go.Scatter(
            x=df_forecast["year"], y=df_forecast["scenC_batteryAutonomy"],
            name="Scenario C: Abrupt Decoupling (Forced 100% Autonomy)",
            line=dict(color="#6366F1", width=2.5, dash="dash")
        ))
        fig_future.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=400, margin=dict(l=40, r=20, t=20, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor="#1e293b", dtick=1), yaxis=dict(title="Allied Battery Autonomy (%)", gridcolor="#1e293b")
        )

    st.plotly_chart(fig_future, use_container_width=True)

    st.markdown("""
    <div style="background: #0F172A; border: 1px solid #334155; border-radius: 12px; padding: 1.2rem; margin-top: 1rem;">
        <h4 style="color: #F8FAFC; margin: 0 0 0.5rem 0;">🔮 2026–2035 10-Year Trajectory Insights:</h4>
        <div style="font-size: 0.83rem; color: #CBD5E1; line-height: 1.6;">
            • <strong>2026–2028 Transition Threshold:</strong> Scenario B incurs temporary cost premiums during initial cell scaling and capital dilution, but successfully dismantles 25% blocking minorities and restores technological sovereignty.<br>
            • <strong>2030–2035 Long-Term Expansion:</strong> As solid-state battery alliances (Korean &amp; Western Tier-1s) and proprietary software architectures (MB.OS, Rivian-VW) mature post-2032, <strong>operating margins rebound to 10.2%</strong>, permanently diverging from the status-quo decline curve (4.2%).
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 6: €45B SUNK CAPITAL & DUAL-TRACK AIR-GAP
# ==============================================================================
with tab6:
    st.markdown("### 🔒 Structural Lock-In (€45B Sunk CapEx) & The 'In China for China' Dual-Track")
    
    st.markdown("""
    <div style="background: #0F172A; border: 1px solid #334155; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;">
        <h4 style="color: #38BDF8; margin-bottom: 0.5rem;">The 3 Economic Realities Preventing Decoupling:</h4>
        <ul style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.6;">
            <li><strong>1. Sunk CapEx in Mega-Fabs (<span style="color:#F43F5E; font-weight:bold;">€45.0B OEM Footprint</span>):</strong> Shenyang Tiexi/Dadong (€10.5B), Anting/Hefei MEB (€18.2B), and Beijing Benz (€16.3B) from 2003 to 2023.</li>
            <li><strong>2. Cash-Flow Dependency:</strong> Chinese JV dividends (<span style="color:#FCD34D;">€10B–€14B/yr</span>) fund global transition CapEx and software R&D.</li>
            <li><strong>3. Supply Chain Cost Parity (<span style="color:#F43F5E; font-weight:bold;">+25% Gap</span>):</strong> Western EV manufacturing is structurally 20–30% more expensive without Chinese LFP scale.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div style="background: #0F172A; border: 1px solid #881337; border-radius: 12px; padding: 1.2rem; height: 100%;">
            <div style="font-size: 0.8rem; font-mono; color: #FDA4AF; font-weight: 700;">TRACK A: DOMESTIC CHINESE FLEET</div>
            <h4 style="color: #F8FAFC; margin: 0.3rem 0 0.6rem 0;">100% Localized Ecosystem (Regulatory & Supply Chain Compliance)</h4>
            <ul style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5;">
                <li>• XPENG CEA zonal E/E (VW) & Momenta AD (Mercedes)</li>
                <li>• Horizon Robotics & Huawei silicon interfaces</li>
                <li>• CATL & EVE Energy domestic LFP battery cells</li>
                <li>• Domestic cloud servers complying with PRC Intelligence Law Art. 7</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_b:
        st.markdown("""
        <div style="background: #0F172A; border: 1px solid #065F46; border-radius: 12px; padding: 1.2rem; height: 100%;">
            <div style="font-size: 0.8rem; font-mono; color: #6EE7B7; font-weight: 700;">TRACK B: WESTERN & ALLIED GLOBAL FLEET</div>
            <h4 style="color: #F8FAFC; margin: 0.3rem 0 0.6rem 0;">Sovereign Cloud & Allied Stack (Data Sovereignty & Defense Compliance)</h4>
            <ul style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5;">
                <li>• Rivian Open SDV (VW), MB.OS (Mercedes), Google AAOS</li>
                <li>• Qualcomm Snapdragon & NVIDIA DRIVE compute platforms</li>
                <li>• CRMA/IRA-compliant allied cell suppliers (PowerCo, Panasonic, LG/Samsung/SK)</li>
                <li>• NATO-certified sovereign data air-gap (zero foreign peering)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 7: 5 STRATEGIC TRUTHS & POLICY ACTIONS
# ==============================================================================
with tab7:
    st.markdown("### 💡 5 Executive Strategic Truths & Policy Action Framework")
    
    insights = [
        {
            "num": "1",
            "title_en": "Re-evaluating Tariff Efficacy: Beyond Unilateral Border Adjustments",
            "finding": "Unilateral countervailing duties (e.g., EU's 20.7% tariff) directly compress operating margins for European OEMs re-exporting from China (such as BMW Shenyang with the iX3). Meanwhile, non-EU competitors circumvent tariffs through greenfield assembly plants in Eastern Europe (e.g., Hungary, Poland).",
            "action": "Standalone tariffs fail to defend industrial competitiveness; policy must combine trade measures with localized manufacturing incentives to avoid penalizing European OEMs.",
            "border": "#881337", "tag_color": "#FDA4AF"
        },
        {
            "num": "2",
            "title_en": "The Imperative of Phased De-risking Over Abrupt Decoupling",
            "finding": "An abrupt operational exit jeopardizes €45.0B in cumulative sunk CapEx and eliminates €12.8B in annual JV dividend inflows needed to fund global software and EV R&D. Western EV manufacturing remains structurally 20–30% more expensive without Chinese scale.",
            "action": "A phased, managed rebalancing—using current joint venture cash flows to finance the transition of Western manufacturing footprints—is the only economically viable path.",
            "border": "#D97706", "tag_color": "#FCD34D"
        },
        {
            "num": "3",
            "title_en": "Defending Corporate Governance (AktG §179) Against Asymmetric IDAR Mechanisms",
            "finding": "A 19.67% non-EU equity stake can functionally command a 35.8% voting share during low AGM attendance (~55%), securing a blocking minority (Sperrminorität, >25%) under German Corporate Law (§179 AktG).",
            "action": "Safeguard board independence and restructuring autonomy by executing authorized capital issuances (diluting concentrated stakes to ~17.1%) and mobilizing proxy turnout to achieve total AGM turnout >= 70.0% (or allied-only turnout >= 85.0%).",
            "border": "#0284C7", "tag_color": "#38BDF8"
        },
        {
            "num": "4",
            "title_en": "Mitigating EV Unit Cost Disparities (+€1,944/unit) via Diversified Global Supply Alliances",
            "finding": "Upstream raw material concentration (65% Lithium refining, 90% Graphite) and LFP manufacturing scale create a structural unit cost penalty of +€1,944 per vehicle that individual OEM balance sheets cannot absorb alone.",
            "action": "Rather than relying on short-term subsidies, OEMs and policymakers must scale CRMA and IRA-compliant multi-regional procurement alliances (integrating European in-house cell initiatives, Japanese, and global Tier-1 suppliers) to establish non-monopolistic scale parity and hedge upstream processing risks.",
            "border": "#7C3AED", "tag_color": "#C084FC"
        },
        {
            "num": "5",
            "title_en": "Operationalizing 'In China for China' as a Survival Strategy for Technological Sovereignty and Data Air-Gapping",
            "finding": "Mandatory compliance with PRC Intelligence Law (Art. 7) prevents a single unified software stack from serving both mainland and Western defense-aligned markets.",
            "action": "Formally bifurcate system architectures: deploy 100% localized digital ecosystems for the mainland domestic market, while mandating hardware-level and NATO-certified sovereign data air-gapping (zero foreign peering) for global vehicle fleets.",
            "border": "#059669", "tag_color": "#6EE7B7"
        }
    ]

    for item in insights:
        st.markdown(f"""
        <div style="background: #0F172A; border: 1px solid {item['border']}; border-radius: 14px; padding: 1.3rem; margin-bottom: 1.1rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; border-bottom: 1px solid #1E293B; padding-bottom: 0.5rem;">
                <div>
                    <h4 style="color: #F8FAFC; margin: 0; font-size: 1.05rem;">{item['num']}. {item['title_en']}</h4>
                </div>
                <span style="font-size: 0.72rem; font-mono; font-weight: bold; background: #070B12; color: {item['tag_color']}; padding: 3px 10px; border-radius: 6px; border: 1px solid {item['border']}; flex-shrink: 0; margin-left: 10px;">
                    TRUTH 0{item['num']}
                </span>
            </div>
            <div style="font-size: 0.84rem; color: #FCD34D; line-height: 1.55; margin-bottom: 0.6rem; background: #070B12; padding: 10px 12px; border-radius: 8px; border-left: 3px solid {item['tag_color']};">
                <strong>🎯 Finding:</strong> {item['finding']}
            </div>
            <div style="font-size: 0.84rem; color: #E2E8F0; line-height: 1.55; background: rgba(30, 41, 59, 0.4); padding: 10px 12px; border-radius: 8px; border-left: 3px solid #38BDF8;">
                <strong style="color: #38BDF8;">⚡ Action:</strong> {item['action']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 8: CROSS-SECTOR SAFEGUARDS & BOARD CHECKLIST
# ==============================================================================
with tab8:
    st.markdown("### 🛡️ Universal Cross-Industry Defense Protocol (4 Critical Sectors) & Supervisory Board Verdict")
    st.caption("🌐 **Universal Cross-Industry Defense Protocol**: Structural vulnerability diagnostics and 4-pillar safeguard rules (Quotas, IP Black-Boxing, Data Air-Gap, Governance) spanning Automotive SDVs, Advanced Semiconductors & EDA, Battery Materials, and Biopharma.")

    # 4-Sector Selector (Distinct Radios)
    sectors = cross_sector_data["sectors"]
    sector_names = [f"{s['icon']} {s['sector']}" for s in sectors]
    
    col_sel, col_score = st.columns([3, 2])
    with col_sel:
        chosen_idx = st.radio(
            "Select Strategic Technology Sector:",
            options=range(len(sectors)),
            format_func=lambda i: sector_names[i],
            horizontal=True
        )
    
    selected_sec = sectors[chosen_idx]
    
    with col_score:
        score_box_html = f"""<div style="background: #070B12; border: 1px solid {selected_sec['border']}; border-radius: 12px; padding: 10px 14px; margin-top: 10px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
<span style="font-size: 0.78rem; font-weight: bold; color: {selected_sec['color']}; font-mono;">{selected_sec['riskLevel']}</span>
<span style="font-size: 0.85rem; font-weight: 900; color: #FFFFFF; font-mono;">{selected_sec['riskScore']} / 100</span>
</div>
<div style="width: 100%; background: #1E293B; height: 7px; border-radius: 4px; overflow: hidden;">
<div style="width: {selected_sec['riskScore']}%; background: {selected_sec['color']}; height: 100%;"></div>
</div>
</div>"""
        st.markdown(score_box_html, unsafe_allow_html=True)

    # Sector Deep-Dive Card (Zero Indent to prevent codeblock escaping)
    sector_card_html = f"""<div style="background: #0F172A; border: 1.5px solid {selected_sec['border']}; border-radius: 16px; padding: 1.4rem; margin-top: 0.8rem; margin-bottom: 1.4rem; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1E293B; padding-bottom: 0.7rem; margin-bottom: 0.9rem;">
<div style="display: flex; align-items: center; gap: 10px;">
<span style="font-size: 1.6rem;">{selected_sec['icon']}</span>
<div>
<h3 style="color: #F8FAFC; margin: 0; font-size: 1.2rem;">{selected_sec['sector']}</h3>
<div style="font-size: 0.8rem; color: {selected_sec['color']}; font-mono; font-weight: bold;">Sector Code: {selected_sec['id'].upper()} • Institutional Safeguard Matrix</div>
</div>
</div>
<span style="font-size: 0.75rem; background: #070B12; color: {selected_sec['color']}; padding: 4px 10px; border-radius: 6px; border: 1px solid {selected_sec['border']}; font-mono; font-weight: 700;">
{selected_sec['riskLevel']}
</span>
</div>
<div style="background: rgba(76, 5, 25, 0.4); border: 1px solid #881337; border-radius: 10px; padding: 10px 14px; margin-bottom: 1.2rem;">
<div style="font-size: 0.8rem; font-mono; font-weight: bold; color: #FDA4AF; margin-bottom: 2px;">🔴 Identified Structural Vulnerability:</div>
<div style="font-size: 0.86rem; color: #FEE2E2; line-height: 1.5;">{selected_sec['vulnerability']}</div>
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
<div style="background: #070B12; padding: 14px; border-radius: 10px; border: 1px solid #1E293B; border-top: 3px solid #34D399;">
<div style="font-size: 0.82rem; font-weight: bold; color: #34D399; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
<span>🌐</span> {selected_sec.get('chinaPlusOneTitle', '1. China+1 Sourcing Quotas')}
</div>
<div style="font-size: 0.83rem; color: #CBD5E1; line-height: 1.55;">
{selected_sec['chinaPlusOne']}
</div>
</div>
<div style="background: #070B12; padding: 14px; border-radius: 10px; border: 1px solid #1E293B; border-top: 3px solid #38BDF8;">
<div style="font-size: 0.82rem; font-weight: bold; color: #38BDF8; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
<span>🔒</span> {selected_sec.get('ipBlackBoxingTitle', '2. Intellectual Property (IP) Black-Boxing')}
</div>
<div style="font-size: 0.83rem; color: #CBD5E1; line-height: 1.55;">
{selected_sec['ipBlackBoxing']}
</div>
</div>
<div style="background: #070B12; padding: 14px; border-radius: 10px; border: 1px solid #1E293B; border-top: 3px solid #C084FC;">
<div style="font-size: 0.82rem; font-weight: bold; color: #C084FC; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
<span>🛡️</span> {selected_sec.get('dataAirGapTitle', '3. Sovereign Data Air-Gapping')}
</div>
<div style="font-size: 0.83rem; color: #CBD5E1; line-height: 1.55;">
{selected_sec['dataAirGap']}
</div>
</div>
<div style="background: #070B12; padding: 14px; border-radius: 10px; border: 1px solid #1E293B; border-top: 3px solid #FCD34D;">
<div style="font-size: 0.82rem; font-weight: bold; color: #FCD34D; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
<span>⚖️</span> {selected_sec.get('governanceTitle', '4. Board Geopolitical Risk Committee')}
</div>
<div style="font-size: 0.83rem; color: #CBD5E1; line-height: 1.55;">
{selected_sec['governance']}
</div>
</div>
</div>
</div>"""
    st.markdown(sector_card_html, unsafe_allow_html=True)

    # 4-Sector Cross-Industry Comparative Matrix Table
    st.markdown("#### 📊 Cross-Sector Institutional Defense Matrix")
    
    matrix_rows = []
    for s in sectors:
        matrix_rows.append(f"""<tr style="border-bottom: 1px solid #1E293B;">
<td style="padding: 10px 12px; font-weight: bold; color: {s['color']}; text-align: left; background: #070B12;">
{s['icon']} {s['sector']}
</td>
<td style="padding: 10px 12px; color: #CBD5E1; font-size: 0.8rem; line-height: 1.4;">
<strong style="color: #34D399;">{s.get('chinaPlusOneTitle', '1. Quota')}</strong><br>{s['chinaPlusOne']}
</td>
<td style="padding: 10px 12px; color: #CBD5E1; font-size: 0.8rem; line-height: 1.4;">
<strong style="color: #38BDF8;">{s.get('ipBlackBoxingTitle', '2. IP')}</strong><br>{s['ipBlackBoxing']}
</td>
<td style="padding: 10px 12px; color: #CBD5E1; font-size: 0.8rem; line-height: 1.4;">
<strong style="color: #C084FC;">{s.get('dataAirGapTitle', '3. Data')}</strong><br>{s['dataAirGap']}
</td>
<td style="padding: 10px 12px; color: #FCD34D;">
<strong style="color: #FCD34D;">{s.get('governanceTitle', '4. Governance')}</strong><br>{s['governance']}
</td>
</tr>""")
        
    matrix_html = f"""<div style="overflow-x: auto; margin-bottom: 1.8rem; border-radius: 12px; border: 1px solid #334155;">
<table style="width: 100%; border-collapse: collapse; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.82rem; text-align: left;">
<thead>
<tr style="background: #0B1329; border-bottom: 2px solid #334155; color: #94A3B8;">
<th style="padding: 12px 10px; width: 18%;">Strategic Sector</th>
<th style="padding: 12px 10px; width: 21%; color: #34D399;">1. Supply Quotas</th>
<th style="padding: 12px 10px; width: 21%; color: #38BDF8;">2. IP Black-Boxing</th>
<th style="padding: 12px 10px; width: 20%; color: #C084FC;">3. Data Air-Gap</th>
<th style="padding: 12px 10px; width: 20%; color: #FCD34D;">4. Board Committee</th>
</tr>
</thead>
<tbody>
{"".join(matrix_rows)}
</tbody>
</table>
</div>"""
    st.markdown(matrix_html, unsafe_allow_html=True)

    # Concrete Executive Board Supervisory Checklist
    st.markdown("#### 📋 C-Level & Supervisory Board 6-Point Oversight Checklist")
    
    board_checks = [
        ("1. Shareholder Governance Oversight", "Are non-EU voting rights strictly controlled below 25% under German AktG §179? (Execute 15% strategic dilution and mobilize proxy turnout to achieve total AGM turnout >= 70.0% / allied-only turnout >= 85.0%)."),
        ("2. Software Source Code Black-Boxing", "Is firmware supplied to Chinese JVs exclusively in compiled binary format, with root algorithm source code isolated in hardware security modules (HSM)?"),
        ("3. Outbound Data Air-Gapping", "Is complete physical and cryptographic air-gapping operational between mainland vehicle telemetry servers and Western headquarters infrastructure?"),
        ("4. 30% Battery Supply Concentration Cap", "Is single-country battery cell and refined material dependency capped below 30% of total platform BOM value?"),
        ("5. Unilateral JV Exit & IP Revocation Clause", "Do joint venture contracts contain explicit covenants permitting unilateral asset disposal and license termination upon state technology transfer mandates?"),
        ("6. Board Geopolitical Risk Committee", "Are all new non-EU capital projects and technology licensing agreements subject to prior unanimous approval by a board-level Geopolitical Risk Committee?")
    ]
    
    for title, desc in board_checks:
        chk_html = f"""<div style="background: #070B12; border: 1px solid #1E293B; border-radius: 8px; padding: 10px 14px; margin-bottom: 6px;">
<strong style="color: #38BDF8; font-size: 0.85rem;">{title}:</strong>
<span style="color: #CBD5E1; font-size: 0.82rem; margin-left: 6px;">{desc}</span>
</div>"""
        st.markdown(chk_html, unsafe_allow_html=True)

    st.markdown("---")
    verdict_html = """<div style="background: #0F172A; border: 1px solid #065F46; border-radius: 12px; padding: 1.2rem; text-align: center;">
<h4 style="color: #6EE7B7; margin: 0 0 0.5rem 0;">Executive Strategic Verdict</h4>
<p style="color: #F8FAFC; font-size: 0.9rem; max-width: 900px; margin: 0 auto; line-height: 1.6;">
"China is no longer merely an assembly hub or a high-margin consumer market; it is a formidable state-backed technological competitor. European and Western industry must avoid the trap of abrupt cliff-edge exits, harness current cash flows to fund Western rebalancing, and execute a resolute <strong>'Phased De-risking (Scenario B)'</strong> to regain capital and technological sovereignty."
</p>
</div>"""
    st.markdown(verdict_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab8_pdf_c1, tab8_pdf_c2 = st.columns([3, 2])
    with tab8_pdf_c1:
        st.markdown("""
        <div style="background: #0F172A; border: 1px solid #334155; border-radius: 10px; padding: 12px 16px;">
            <div style="font-size: 0.88rem; font-weight: bold; color: #F8FAFC;">
                📥 Export Complete Supervisory Board Briefing Dossier (PDF)
            </div>
            <div style="font-size: 0.76rem; color: #94A3B8; margin-top: 3px;">
                Download the complete multi-page statutory governance report, historical delivery tables, and board oversight checklist.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with tab8_pdf_c2:
        try:
            tab8_pdf_bytes = generate_board_briefing_pdf({
                'adjusted_ebit': 31.2,
                'margin_pct': 8.21,
                'effective_cn_power': 24.43,
                'blocking_veto': False,
                'dilution_pct': 15,
                'allied_turnout': 85,
                'china_volume_shock': 15,
                'mineral_premium': 20,
                'bev_volume': 1200000,
                'tariff_rate': 21,
                'unit_pack_penalty': 1944,
                'total_battery_penalty_b': 2.33,
                'china_ebit_loss_b': 2.4,
                'tariff_loss_b': 0.2,
                'total_turnout': 69.04,
                's_cn': 17.10
            })
            st.download_button(
                label="📄 Download Complete Board Dossier (PDF)",
                data=tab8_pdf_bytes,
                file_name="Executive_Supervisory_Board_Dossier_2026_2035.pdf",
                mime="application/pdf",
                key="tab8_pdf_download",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF Export Error: {e}")


st.markdown("<p style='text-align: center; color: #64748B; font-size: 0.75rem; margin-top: 2rem;'>Stage 05 Strategic Decision Engine • China Tech-Absorption (IDAR) &amp; German Auto Triad Dependency (2019–2025) &amp; 2026–2035 10-Year Forecast • Audited Institutional Baseline</p>", unsafe_allow_html=True)
