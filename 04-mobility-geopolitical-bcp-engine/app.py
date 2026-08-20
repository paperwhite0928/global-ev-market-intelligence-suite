import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# Page Configuration & Executive Theme
# ==============================================================================
st.set_page_config(
    page_title="Global Mobility Geopolitical Pre-emptive BCP Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# Brand Color Palette Definition (Strictly User-Defined)
# ==============================================================================
COLOR_BYD = "#E11D48"        # Vivid Red
COLOR_TESLA = "#7C3AED"      # Electric Violet
COLOR_VW = "#00A8A8"         # Cyan / Teal
COLOR_HYUNDAI = "#00287A"    # Deep Blue
COLOR_HYUNDAI_LIGHT = "#1D4ED8" # High-Contrast Blue
COLOR_BMW = "#1E293B"        # Dark Graphite / Black
COLOR_BMW_ACCENT = "#64748B" # Slate Accent
COLOR_BENZ = "#7F8C8D"       # Silver / Metallic Grey
COLOR_TOYOTA = "#F59E0B"     # Amber / Soft Orange

# Helper function to convert HEX to RGBA string for Plotly
def hex_to_rgba(hex_code, alpha=0.25):
    hex_clean = hex_code.lstrip('#')
    if len(hex_clean) == 6:
        r = int(hex_clean[0:2], 16)
        g = int(hex_clean[2:4], 16)
        b = int(hex_clean[4:6], 16)
        return f"rgba({r}, {g}, {b}, {alpha})"
    return f"rgba(56, 189, 248, {alpha})"

# High-Contrast CSS for 100% Text Visibility in Both Dark & Light Themes
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #0F172A;
        color: #38BDF8;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        border: 1px solid #334155;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #38BDF8;
        border-radius: 50%;
        box-shadow: 0 0 0 rgba(56, 189, 248, 0.4);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(56, 189, 248, 0); }
        100% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }
    }
    
    .hero-title {
        font-size: 2.15rem;
        font-weight: 800;
        color: #F8FAFC !important;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #94A3B8 !important;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    
    /* High-Contrast Universal Cards */
    .metric-container {
        background: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 14px;
        padding: 1.2rem 1.3rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        position: relative;
        overflow: hidden;
    }
    .metric-label {
        font-size: 0.8rem;
        font-weight: 700;
        color: #94A3B8 !important;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #F8FAFC !important;
        line-height: 1.1;
        margin-bottom: 0.3rem;
    }
    .metric-tag {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
    }
    
    /* Emergency Guard Cards */
    .emergency-card {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 12px;
        padding: 1.3rem 1.4rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .emergency-card h4 {
        font-size: 1.15rem;
        font-weight: 800;
        margin: 0 0 0.6rem 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .emergency-section {
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .emergency-section b {
        color: #FFFFFF !important;
        font-weight: 700;
    }
    .crisis-tag {
        background: #450A0A;
        color: #FCA5A5;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .action-tag {
        background: #172554;
        color: #93C5FD;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .defense-tag {
        background: #064E3B;
        color: #6EE7B7;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    
    .insight-box {
        background: #0F172A !important;
        border: 1px solid #334155 !important;
        border-left: 4px solid #00A8A8 !important;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        color: #E2E8F0 !important;
    }
    .insight-box h4 {
        color: #38BDF8 !important;
        font-size: 0.95rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
    }
    .insight-box p {
        color: #CBD5E1 !important;
        font-size: 0.84rem;
        line-height: 1.5;
        margin: 0;
    }
    .insight-box b {
        color: #FFFFFF !important;
    }
    
    .prescribe-card {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.9rem;
    }
    .prescribe-card h4 {
        font-size: 1.08rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
    }
    .prescribe-card p {
        color: #E2E8F0 !important;
        font-size: 0.88rem;
        line-height: 1.55;
        margin: 0;
    }
    .prescribe-card b {
        color: #FFFFFF !important;
    }
    
    .condition-banner {
        background: #0F172A !important;
        border: 1px solid #334155 !important;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 1.2rem;
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        align-items: center;
    }
    .condition-tag {
        background: #1E293B;
        border: 1px solid #475569;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        color: #F8FAFC;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# Sidebar: Geopolitical Engine Controls (English)
# ==============================================================================
st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
    <div style="background: #0F172A; padding: 8px; border-radius: 8px; color: #38BDF8; font-size: 1.4rem;">🎛️</div>
    <div>
        <div style="font-weight: 800; font-size: 1.05rem; color: #F8FAFC;">GEOPOLITICAL ENGINE</div>
        <div style="font-size: 0.7rem; color: #94A3B8; font-weight: 600;">2026-2035 SCENARIO SIMULATOR</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size: 0.85rem; color: #94A3B8; font-weight: 600; margin-bottom: 0.6rem;'>Exogenous Variable Calibration</p>", unsafe_allow_html=True)

eu_relaxation = st.sidebar.slider(
    "1. 🇪🇺 EU 2035 Mandate Delay Intensity (%)",
    min_value=0, max_value=100, value=85, step=5,
    help="Higher values expand legal recognition for PHEV, EREV, and carbon-neutral e-Fuels."
)

tariff_level = st.sidebar.slider(
    "2. 🇺🇸 Western Tariff & Connected Car Embargo (%)",
    min_value=0, max_value=100, value=80, step=5,
    help="Severity of US 100% tariffs and cybersecurity bans on foreign HW/SW."
)

mineral_inflation = st.sidebar.slider(
    "3. ⛏️ Non-China Arctic/Greenland Mineral Premium ($/kWh)",
    min_value=0, max_value=50, value=25, step=5,
    help="Battery pack cost inflation from domesticating supply chains in high-cost regions."
)

v2g_regulation = st.sidebar.slider(
    "4. ⚡ AI Grid Crisis & V2G Mandate Ratio (%)",
    min_value=0, max_value=100, value=70, step=5,
    help="Regulatory mandate for bi-directional vehicle-to-grid (V2G) power integration to alleviate AI data center grid shortages."
)

st.sidebar.markdown("---")

# Comprehensive Geopolitical Stress Index
geo_stress_index = int((tariff_level * 0.35) + (mineral_inflation * 1.1) + (v2g_regulation * 0.30) - (eu_relaxation * 0.15))
geo_stress_index = max(10, min(98, geo_stress_index))

st.sidebar.markdown(f"""
<div style="background: #0F172A; border: 1px solid #334155; border-radius: 10px; padding: 1rem; color: white;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.75rem; font-weight: 700; color: #94A3B8;">GEOPOLITICAL STRESS</span>
        <span style="font-size: 0.7rem; background: {'#DC2626' if geo_stress_index > 70 else '#2563EB'}; padding: 2px 6px; border-radius: 4px; font-weight: 700;">
            {'CRITICAL' if geo_stress_index > 70 else 'ELEVATED'}
        </span>
    </div>
    <div style="font-size: 1.7rem; font-weight: 800; color: #38BDF8; margin: 0.2rem 0;">{geo_stress_index} / 100</div>
    <div style="font-size: 0.7rem; color: #94A3B8; line-height: 1.4;">
        ⚠️ Combined tariff, mineral inflation, and AI grid mandate stress index.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# Header Section (Updated to Recommended Title Option 1)
# ==============================================================================
st.markdown("""
<div>
    <div class="status-badge"><span class="pulse-dot"></span> Executive Briefing Room | Pre-emptive BCP Engine</div>
    <div class="hero-title">2026~2035 Global Mobility Geopolitical Risk & Pre-emptive BCP Engine</div>
    <div class="hero-subtitle">A Dynamic Scenario Simulator & Survival Playbook for German Automotive Leadership</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# Dynamic Econometric Modeling Logic
# ==============================================================================
total_demand = 90.0  # Million units

phev_share = max(15.0, min(60.0, 24.0 + (eu_relaxation * 0.22) - (v2g_regulation * 0.05)))
bev_share = max(12.0, min(55.0, 42.0 - (eu_relaxation * 0.16) - (mineral_inflation * 0.20) + (v2g_regulation * 0.08)))
ice_share = max(5.0, 100.0 - phev_share - bev_share)

v2g_hw_cost_premium = (v2g_regulation * 0.12)
battery_cost = 110 + mineral_inflation + v2g_hw_cost_premium

# 4 Key Metrics Cards (English)
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Global New Vehicle Demand (TIV)</div>
        <div class="metric-value">{total_demand:.0f}M <span style="font-size: 1rem; color:#94A3B8;">Units</span></div>
        <div class="metric-tag" style="background:#451A03; color:#F59E0B;">⚠️ 10-Yr Zero-Sum Stagnation</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">2030 Proj. PHEV / EREV Share</div>
        <div class="metric-value" style="color: #38BDF8;">{phev_share:.1f}%</div>
        <div class="metric-tag" style="background:#172554; color:#60A5FA;">📈 Dominant Powertrain</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">2030 Proj. Pure BEV Share</div>
        <div class="metric-value" style="color: #34D399;">{bev_share:.1f}%</div>
        <div class="metric-tag" style="background:#064E3B; color:#6EE7B7;">⚡ V2G Grid Capacity: {v2g_regulation}%</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Avg. Battery Pack Cost</div>
        <div class="metric-value" style="color: #F87171;">${battery_cost:.0f}<span style="font-size: 1rem;">/kWh</span></div>
        <div class="metric-tag" style="background:#450A0A; color:#FCA5A5;">🔺 Mineral +${mineral_inflation} | V2G +${v2g_hw_cost_premium:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# Dynamic Action Generation Engine Function
# ==============================================================================
def get_dynamic_oem_playbook_en(eu, tariff, mineral, v2g):
    is_eu_high = eu >= 65
    is_tariff_high = tariff >= 65
    is_mineral_high = mineral >= 20
    is_v2g_high = v2g >= 60
    
    playbooks = {}
    
    # 1. 🇩🇪 Volkswagen Group
    if is_v2g_high and is_eu_high:
        vw_prevent = "Producing non-V2G legacy EVs subject to European grid penalties, while burning capital on proprietary CARIAD software."
        vw_push = "Standardize <b>V2G bi-directional charging on 100km+ Gen-2 PHEVs and MEB+ platforms</b>; monetize European virtual power plant (VPP) fleet contracts with Rivian Open SDV."
        vw_badge = "V2G Grid Integrated PHEV Fleet"
    elif is_eu_high and is_tariff_high:
        vw_prevent = "Halt aggressive BEV capacity expansion in Europe and cease proprietary CARIAD OS capital burn."
        vw_push = "Downsize to 7.5M units; monopolize European cash flow with <b>100km+ Gen-2 PHEVs (Golf/Tiguan)</b> and fast-track Rivian JV Open SDV architecture."
        vw_badge = "PHEV Home Turf Monopolization"
    elif not is_eu_high and is_mineral_high:
        vw_prevent = "Avoid high-cost NCM cell concentration on luxury BEVs as raw mineral inflation spikes unit losses."
        vw_push = "Accelerate LFP/Sodium-ion battery JVs and maximize MPGe energy efficiency across entry ID.2 platforms."
        vw_badge = "Affordability Cost Defense"
    else:
        vw_prevent = "Discard the historical 10M volume illusion and unoptimized German fixed cost structures."
        vw_push = "Consolidate assembly modules to cut fixed overhead by 20%; deploy Bosch/Google-backed open architecture."
        vw_badge = "Restructuring & Optimization"
    playbooks["VW"] = {"prevent": vw_prevent, "push": vw_push, "badge": vw_badge}
    
    # 2. 🇩🇪 BMW Group
    if is_v2g_high:
        bmw_prevent = "Delaying bidirectional energy management integration into Neue Klasse architecture."
        bmw_push = "Deploy <b>'BMW Connected Home & Grid Energy Service'</b> across 5/7-Series PHEVs/BEVs; capture premium grid stabilization utility tariffs."
        bmw_badge = "Premium V2G Energy Ecosystem"
    elif is_tariff_high and is_mineral_high:
        bmw_prevent = "Avoid predatory discounting wars against Chinese players that dilute brand equity."
        bmw_push = "Leverage <b>'Power of Choice' modular lines</b> to pivot PHEV/BEV production ratios within 2 weeks; protect 10%+ EBIT margin on 5/7-Series."
        bmw_badge = "Flexible Line & Margin Defense"
    elif is_eu_high:
        bmw_prevent = "Do not mandate premature sunset dates for high-efficiency inline-6 and PHEV powertrains."
        bmw_push = "Extend life of next-gen PHEVs into the late 2030s to harvest global high-margin premium volume."
        bmw_badge = "Premium Multi-Powertrain"
    else:
        bmw_prevent = "Excessive proprietary OS spending."
        bmw_push = "Deploy lightweight proprietary UI layers atop standardized Android Automotive foundations."
        bmw_badge = "Digital R&D Efficiency"
    playbooks["BMW"] = {"prevent": bmw_prevent, "push": bmw_push, "badge": bmw_badge}
    
    # 3. 🇩🇪 Mercedes-Benz Group
    if is_v2g_high or is_eu_high:
        benz_prevent = "Abandon the rigid '2030 100% BEV' timeline and scale back heavy depreciation on entry EQ models lacking smart grid integration."
        benz_push = "Roll back MMA platform to multi-powertrain (PHEV/ICE) and double down on <b>Maybach, G-Class, and AMG Performance Hybrids with bi-directional high-voltage charging</b>."
        benz_badge = "Top-End Luxury & V2G Power Hub"
    else:
        benz_prevent = "Sustaining low-margin A/B-Class entry volume."
        benz_push = "Electrify S-Class flagship VIP lines and monetize Level-3 Drive Pilot autonomy subscriptions."
        benz_badge = "Ultra-Luxury VIP Monetization"
    playbooks["BENZ"] = {"prevent": benz_prevent, "push": benz_push, "badge": benz_badge}
    
    # 4. 🇺🇸 Tesla Inc.
    if is_v2g_high:
        tesla_prevent = "Treating vehicle manufacturing as a standalone automotive hardware business."
        tesla_push = "<b>Scale Megapack utility ESS to 35%+ of total corporate revenue</b>; turn 5 million customer vehicles into a nationwide Virtual Power Plant (Tesla Electric VPP)."
        tesla_badge = "⚡ AI Power Grid Monopoly & VPP"
    elif is_tariff_high and not is_mineral_high:
        tesla_prevent = "Relying purely on vehicle export volumes into heavily tariffed foreign jurisdictions."
        tesla_push = "<b>Accelerate Unboxed manufacturing to slash build costs by 50%</b>; scale NACS charging network subscriptions and commercialize North American FSD Robotaxis."
        tesla_badge = "Cost Disruption & NACS Monopoly"
    elif is_mineral_high:
        tesla_prevent = "Single-stream automotive hardware margin vulnerability."
        tesla_push = "<b>Scale Megapack utility ESS to 30%+ of revenue</b> and monetize V2G Virtual Power Plants (VPP) via Tesla Electric."
        tesla_badge = "Utility ESS & Grid Dominance"
    else:
        tesla_prevent = "Volume stagnation without a sub-$25k platform."
        tesla_push = "Aggressive Model Y global line optimization and early ramp-up of next-gen mass platform."
        tesla_badge = "Global Volume Scaling"
    playbooks["TESLA"] = {"prevent": tesla_prevent, "push": tesla_push, "badge": tesla_badge}
    
    # 5. 🇨🇳 BYD
    if is_tariff_high:
        byd_prevent = "Direct vehicle export illusions against Western 100% tariffs and countervailing duties."
        byd_push = "Accelerate CKD/SKD assembly plants in Hungary, Brazil, and Turkey; <b>monopolize Global South markets with $15k 5th-Gen DM-i PHEVs</b>."
        byd_badge = "Global South & Ultra-Low PHEV Monopoly"
    else:
        byd_prevent = "Capital depletion through price wars as domestic subsidies phase out."
        byd_push = "Monetize Blade battery and vertically integrated component supply as a global Tier-1 provider."
        byd_badge = "Global Component Penetration"
    playbooks["BYD"] = {"prevent": byd_prevent, "push": byd_push, "badge": byd_badge}
    
    # 6. 🇰🇷 Hyundai-Kia Group
    if is_v2g_high:
        h_prevent = "Treating E-GMP 800V V2L features as marketing gimmicks rather than standardizing grid V2G utility software."
        h_push = "Commercialize <b>'Hyundai Grid-Flex V2G Fleet Software'</b> in North America/Europe; pivot Georgia HMGMA lines to hybrid mix with EREV launch."
        h_badge = "800V V2G Grid Agility"
    elif is_tariff_high or is_eu_high:
        h_prevent = "Exposing dedicated US EV lines to 10-25% tariffs and low cell JV utilization."
        h_push = "Instantly configure Georgia HMGMA plant for <b>flexible hybrid production (securing 85%+ utilization)</b>; fast-track small-battery EREVs."
        h_badge = "Flexible Line & EREV Agility"
    else:
        h_prevent = "High-cost cell sourcing dependencies."
        h_push = "Expand 800V ultra-fast charging platform scale and capture emerging market hubs (India/ASEAN)."
        h_badge = "Emerging Market Expansion"
    playbooks["HYUNDAI"] = {"prevent": h_prevent, "push": h_push, "badge": h_badge}
    
    # 7. 🇯🇵 Toyota
    if is_v2g_high:
        toyota_prevent = "Ignoring V2G bi-directional inverter integration on next-gen Prius and RAV4 Prime PHEVs."
        toyota_push = "Equip all global PHEV lines with <b>1.5kW-3.3kW Emergency V2H/V2G home backup generators</b>; harvest record HEV profits to fund 2028 solid-state R&D."
        toyota_badge = "PHEV Grid Backup & Solid-State Pivot"
    elif is_eu_high or is_mineral_high:
        toyota_prevent = "Prematurely burning capital on unverified pure-BEV line expansion under regulatory panic."
        toyota_push = "<b>Harvest record cash flow by dominating global HEV demand</b> during the EV chasm; fully fund 2028 commercial solid-state battery R&D."
        toyota_badge = "HEV Cash Harvest & Solid-State Pivot"
    else:
        toyota_prevent = "Allowing software development lags (Arene OS) to become permanent digital handicaps."
        toyota_push = "Form an alliance with Honda and Nissan to co-develop standardized Japanese automotive OS architecture."
        toyota_badge = "Japan OS Coalition"
    playbooks["TOYOTA"] = {"prevent": toyota_prevent, "push": toyota_push, "badge": toyota_badge}
    
    return playbooks

live_playbooks = get_dynamic_oem_playbook_en(eu_relaxation, tariff_level, mineral_inflation, v2g_regulation)

# ==============================================================================
# Dashboard Tabs (Streamlined into 4 Pure Action Tabs)
# ==============================================================================
tab_dynamic, tab_sim, tab_battle, tab_guard = st.tabs([
    "🎯 [Dynamic Playbook] Real-Time Scenario Engine",
    "📊 [Simulation & Calibration] 2030 Market Mix & Data Appendix",
    "🥊 [OEM 1:1 Comparison] Risk Radar & Matrix",
    "🛡️ [German OEM Roadmap] 4 Pre-emptive BCP Guards"
])

# ==============================================================================
# Tab 0: Real-Time Dynamic Scenario Playbook
# ==============================================================================
with tab_dynamic:
    st.markdown("#### 🎯 Exogenous Variable-Linked Dynamic OEM Playbook")
    st.caption("Adjust the 4 sidebar variables to witness real-time diagnostic shifts and tactical playbook recalculations.")
    
    st.markdown(f"""
    <div class="condition-banner">
        <span style="font-weight: 700; color: #38BDF8; font-size: 0.9rem;">📍 Live Scenario Parameters:</span>
        <span class="condition-tag">🇪🇺 EU Delay: {eu_relaxation}% ({'High Mandate Rollback' if eu_relaxation>=65 else 'Partial Delay'})</span>
        <span class="condition-tag">🇺🇸 Western Tariff: {tariff_level}% ({'Tech Fortress' if tariff_level>=65 else 'Moderate Tariffs'})</span>
        <span class="condition-tag">⛏️ Mineral Premium: +${mineral_inflation}/kWh ({'Severe Inflation' if mineral_inflation>=20 else 'Stable'})</span>
        <span class="condition-tag">⚡ V2G Grid Mandate: {v2g_regulation}% ({'Bi-directional Mandated' if v2g_regulation>=60 else 'Incentivized'})</span>
    </div>
    """, unsafe_allow_html=True)
    
    c_p1, c_p2 = st.columns(2)
    
    with c_p1:
        st.markdown(f"""
        <div class="prescribe-card" style="border-left: 5px solid {COLOR_VW};">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
                <h4 style="color:{COLOR_VW} !important; margin:0;">🇩🇪 Volkswagen Group</h4>
                <span class="condition-tag" style="background:#003636; border-color:{COLOR_VW}; color:#5EEAD4;">{live_playbooks['VW']['badge']}</span>
            </div>
            <p>• <b>🚫 Action to Prevent:</b> {live_playbooks['VW']['prevent']}<br>
            • <b>🚀 Weapon to Push Forward:</b> {live_playbooks['VW']['push']}</p>
        </div>
        
        <div class="prescribe-card" style="border-left: 5px solid #64748B;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
                <h4 style="color:#94A3B8 !important; margin:0;">🇩🇪 BMW Group</h4>
                <span class="condition-tag" style="background:#1E293B; border-color:#64748B; color:#CBD5E1;">{live_playbooks['BMW']['badge']}</span>
            </div>
            <p>• <b>🚫 Action to Prevent:</b> {live_playbooks['BMW']['prevent']}<br>
            • <b>🚀 Weapon to Push Forward:</b> {live_playbooks['BMW']['push']}</p>
        </div>
        
        <div class="prescribe-card" style="border-left: 5px solid {COLOR_BENZ};">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
                <h4 style="color:{COLOR_BENZ} !important; margin:0;">🇩🇪 Mercedes-Benz Group</h4>
                <span class="condition-tag" style="background:#2A3439; border-color:{COLOR_BENZ}; color:#E2E8F0;">{live_playbooks['BENZ']['badge']}</span>
            </div>
            <p>• <b>🚫 Action to Prevent:</b> {live_playbooks['BENZ']['prevent']}<br>
            • <b>🚀 Weapon to Push Forward:</b> {live_playbooks['BENZ']['push']}</p>
        </div>
        
        <div class="prescribe-card" style="border-left: 5px solid {COLOR_TESLA};">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
                <h4 style="color:{COLOR_TESLA} !important; margin:0;">🇺🇸 Tesla Inc.</h4>
                <span class="condition-tag" style="background:#2E1065; border-color:{COLOR_TESLA}; color:#C4B5FD;">{live_playbooks['TESLA']['badge']}</span>
            </div>
            <p>• <b>🚫 Action to Prevent:</b> {live_playbooks['TESLA']['prevent']}<br>
            • <b>🚀 Weapon to Push Forward:</b> {live_playbooks['TESLA']['push']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c_p2:
        st.markdown(f"""
        <div class="prescribe-card" style="border-left: 5px solid {COLOR_BYD};">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
                <h4 style="color:{COLOR_BYD} !important; margin:0;">🇨🇳 BYD</h4>
                <span class="condition-tag" style="background:#4C0519; border-color:{COLOR_BYD}; color:#FDA4AF;">{live_playbooks['BYD']['badge']}</span>
            </div>
            <p>• <b>🚫 Action to Prevent:</b> {live_playbooks['BYD']['prevent']}<br>
            • <b>🚀 Weapon to Push Forward:</b> {live_playbooks['BYD']['push']}</p>
        </div>
        
        <div class="prescribe-card" style="border-left: 5px solid {COLOR_HYUNDAI_LIGHT};">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
                <h4 style="color:{COLOR_HYUNDAI_LIGHT} !important; margin:0;">🇰🇷 Hyundai-Kia Group</h4>
                <span class="condition-tag" style="background:#172554; border-color:{COLOR_HYUNDAI_LIGHT}; color:#93C5FD;">{live_playbooks['HYUNDAI']['badge']}</span>
            </div>
            <p>• <b>🚫 Action to Prevent:</b> {live_playbooks['HYUNDAI']['prevent']}<br>
            • <b>🚀 Weapon to Push Forward:</b> {live_playbooks['HYUNDAI']['push']}</p>
        </div>
        
        <div class="prescribe-card" style="border-left: 5px solid {COLOR_TOYOTA};">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 6px;">
                <h4 style="color:{COLOR_TOYOTA} !important; margin:0;">🇯🇵 Toyota</h4>
                <span class="condition-tag" style="background:#451A03; border-color:{COLOR_TOYOTA}; color:#FDE68A;">{live_playbooks['TOYOTA']['badge']}</span>
            </div>
            <p>• <b>🚫 Action to Prevent:</b> {live_playbooks['TOYOTA']['prevent']}<br>
            • <b>🚀 Weapon to Push Forward:</b> {live_playbooks['TOYOTA']['push']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# Tab 1: Simulation & Market Flow (WITH COMPACT DATA APPENDIX AT BOTTOM)
# ==============================================================================
with tab_sim:
    st.markdown("#### 🌐 2030 Global Market Mix & Zero-Sum Share Breakdown")
    st.caption("Live recalculation of powertrain shares and OEM EBIT margins based on slider inputs (including V2G energy revenue).")
    
    col_s1, col_s2 = st.columns([1, 1.1])
    
    with col_s1:
        pt_data = pd.DataFrame({
            "Powertrain": ["Hybrids (HEV/PHEV/EREV)", "Pure Electric (BEV)", "Internal Combustion (ICE)"],
            "Share": [phev_share, bev_share, ice_share],
            "Volume (Million)": [round(total_demand * phev_share / 100, 1), round(total_demand * bev_share / 100, 1), round(total_demand * ice_share / 100, 1)]
        })
        
        fig_donut = px.pie(
            pt_data, values="Share", names="Powertrain",
            color="Powertrain",
            color_discrete_map={
                "Hybrids (HEV/PHEV/EREV)": "#38BDF8",
                "Pure Electric (BEV)": "#34D399",
                "Internal Combustion (ICE)": "#64748B"
            },
            hole=0.55
        )
        fig_donut.update_traces(
            textposition='outside', 
            textinfo='percent+label',
            marker=dict(line=dict(color='#0F172A', width=2))
        )
        fig_donut.update_layout(
            title="<b>2030 Global Powertrain Mix Forecast</b>",
            font=dict(family="Plus Jakarta Sans", size=12, color="#F8FAFC"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(t=50, b=20, l=20, r=20),
            annotations=[dict(text=f'<b>Total<br>90M</b>', x=0.5, y=0.5, font_size=15, showarrow=False, font=dict(color="#F8FAFC"))]
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col_s2:
        vw_vol = 13.5 * (1 + (eu_relaxation - 50) * 0.003 - (tariff_level - 50) * 0.001 + (v2g_regulation - 50) * 0.0008)
        byd_vol = 31.0 * (1 - (tariff_level - 50) * 0.004 + (v2g_regulation - 50) * 0.0005)
        toyota_vol = 25.0 * (1 + (eu_relaxation - 50) * 0.002 - (v2g_regulation - 50) * 0.0008)
        tesla_vol = 6.5 * (1 - (mineral_inflation / 100) + (v2g_regulation - 50) * 0.002)
        hyundai_vol = 8.5 * (1 + (eu_relaxation - 50) * 0.0015 - (tariff_level - 50) * 0.002 + (v2g_regulation - 50) * 0.001)
        bmw_vol = 4.5 * (1 + (eu_relaxation - 50) * 0.002 + (v2g_regulation - 50) * 0.0006)
        benz_vol = 2.0 * (1 + (eu_relaxation - 50) * 0.002 + (v2g_regulation - 50) * 0.0005)
        
        oem_data = pd.DataFrame({
            "OEM": ["BYD", "Toyota", "VW Group", "Hyundai-Kia", "Tesla", "BMW Group", "Mercedes-Benz"],
            "Volume (M Units)": [byd_vol, toyota_vol, vw_vol, hyundai_vol, tesla_vol, bmw_vol, benz_vol],
            "EBIT Margin (%)": [
                max(1.0, 2.8 - (tariff_level * 0.018) + (v2g_regulation * 0.008)),
                max(3.0, 8.6 + (phev_share * 0.02) - (v2g_regulation * 0.012)),
                max(2.0, 6.8 + (eu_relaxation * 0.028) - (mineral_inflation * 0.04) + (v2g_regulation * 0.015)),
                max(3.0, 7.8 - (tariff_level * 0.02) + (v2g_regulation * 0.018)),
                max(3.0, 7.2 - (mineral_inflation * 0.05) + (v2g_regulation * 0.035)),
                max(4.0, 9.5 + (eu_relaxation * 0.02) + (v2g_regulation * 0.010)),
                max(4.0, 10.2 + (eu_relaxation * 0.02) + (v2g_regulation * 0.008))
            ],
            "Color": [COLOR_BYD, COLOR_TOYOTA, COLOR_VW, COLOR_HYUNDAI_LIGHT, COLOR_TESLA, "#334155", COLOR_BENZ]
        })
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=oem_data["OEM"],
            y=oem_data["Volume (M Units)"],
            name="Volume (M Units)",
            marker=dict(color=oem_data["Color"], line=dict(color="#334155", width=1.5)),
            text=[f"{v:.1f}M ({m:.1f}%)" for v, m in zip(oem_data["Volume (M Units)"], oem_data["EBIT Margin (%)"])],
            textposition='outside',
            textfont=dict(color="#F8FAFC")
        ))
        fig_bar.update_layout(
            title="<b>2030 OEM Projected Volume & Margin (V2G Energy Revenue Interlinked)</b>",
            font=dict(family="Plus Jakarta Sans", size=12, color="#F8FAFC"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor="#334155"),
            yaxis=dict(title="Volume (Million Units)", range=[0, 36], gridcolor="#334155"),
            margin=dict(t=50, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # --------------------------------------------------------------------------
    # Compact Appendix Attached at Bottom
    # --------------------------------------------------------------------------
    st.markdown("---")
    with st.expander("📌 Methodological Appendix: Econometric Calibration & Downside Price Stickiness", expanded=False):
        col_c1, col_c2, col_c3 = st.columns([1, 1, 1.2])
        
        with col_c1:
            comp_df = pd.DataFrame({
                "Scenario": ["Raw", "Calibrated", "Shock"],
                "Total Demand (M)": [90.0, 83.5, 75.5],
                "BEV Share (%)": [30.0, 24.5, 18.0]
            })
            fig_comp = px.bar(
                comp_df, x="Scenario", y="Total Demand (M)", 
                color="BEV Share (%)", 
                text_auto=True, 
                color_continuous_scale="Blues",
                title="<b>TIV Demand Contraction</b>"
            )
            fig_comp.update_layout(
                font=dict(family="Plus Jakarta Sans", size=10, color="#F8FAFC"),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor="#334155"),
                yaxis=dict(gridcolor="#334155"),
                margin=dict(t=40, b=20, l=10, r=10),
                height=260
            )
            st.plotly_chart(fig_comp, use_container_width=True)
            
        with col_c2:
            years = [2022, 2023, 2024, 2025, 2026, 2027]
            raw_cell = [151, 139, 115, 105, 95, 85]
            car_msrp_index = [100, 102, 101, 99, 98, 97]
            
            fig_stick = go.Figure()
            fig_stick.add_trace(go.Scatter(x=years, y=raw_cell, name="Cell ($/kWh)", line=dict(color=COLOR_BYD, width=2)))
            fig_stick.add_trace(go.Scatter(x=years, y=car_msrp_index, name="MSRP Index", line=dict(color=COLOR_HYUNDAI_LIGHT, width=2, dash='dot'), yaxis='y2'))
            fig_stick.update_layout(
                title="<b>MSRP Downside Stickiness</b>",
                yaxis=dict(
                    title=dict(text="Cell ($)", font=dict(size=10, color="#F8FAFC")),
                    gridcolor="#334155"
                ),
                yaxis2=dict(
                    title=dict(text="MSRP Index", font=dict(size=10, color="#F8FAFC")),
                    overlaying='y',
                    side='right'
                ),
                font=dict(family="Plus Jakarta Sans", size=10, color="#F8FAFC"),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(x=0.02, y=0.98, font=dict(size=9)),
                margin=dict(t=40, b=20, l=10, r=10),
                height=260
            )
            st.plotly_chart(fig_stick, use_container_width=True)
            
        with col_c3:
            st.markdown("""
            <div class="insight-box">
                <h4>💡 Econometric Calibration Notes</h4>
                <p>• <b>Fleet Aging (12.5 Yrs):</b> High interest rates and vehicle costs expanded fleet age, contracting the annual replacement market to 83.5M units.<br>
                • <b>Price Stickiness:</b> Cell cost drops ($151 ➔ $85) failed to translate to MSRP discounts due to fixed mining contracts, labor inflation, and tariffs.</p>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# Tab 2: OEM Head-to-Head & Risk Radar
# ==============================================================================
with tab_battle:
    st.markdown("#### 🥊 OEM Risk Exposure Radar & Dynamic Strategic Matrix")
    st.caption("The 5 risk vectors dynamically reshape in real-time according to your slider parameters (Tariffs, Minerals, V2G Grid, EU Delays).")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        oem_a = st.selectbox("Select OEM A (German Big 3):", ["🇩🇪 Volkswagen Group", "🇩🇪 BMW Group", "🇩🇪 Mercedes-Benz Group"], index=0)
    with col_sel2:
        oem_b = st.selectbox("Select OEM B (Global 4):", ["🇺🇸 Tesla", "🇨🇳 BYD", "🇰🇷 Hyundai-Kia", "🇯🇵 Toyota"], index=0)
        
    def calculate_dynamic_radar_scores(eu, tariff, mineral, v2g):
        scores_db = {}
        
        vw_china = min(100, int(85 + (tariff * 0.12)))
        vw_fixed = min(100, int(85 + (v2g * 0.10) - (eu * 0.15)))
        vw_sw = min(100, int(80 + (v2g * 0.15)))
        vw_tariff = min(100, int(70 + (tariff * 0.20)))
        vw_capex = min(100, int(80 + (mineral * 0.6) - (eu * 0.15)))
        scores_db["🇩🇪 Volkswagen Group"] = {
            "scores": [vw_china, vw_fixed, vw_sw, vw_tariff, vw_capex],
            "color": COLOR_VW,
            "weak": f"China profit evaporation (Exposure: {vw_china}/100), High German fixed cost ({vw_fixed}/100), CARIAD software delays ({vw_sw}/100).",
            "guard": "Downsize output to 7.5M units (-20% overhead), Rivian Open SDV integration, Gen-2 100km+ PHEV cash defense."
        }
        
        bmw_china = min(100, int(70 + (tariff * 0.10)))
        bmw_fixed = min(100, int(60 + (v2g * 0.08) - (eu * 0.12)))
        bmw_sw = min(100, int(50 + (v2g * 0.10)))
        bmw_tariff = min(100, int(50 + (tariff * 0.15)))
        bmw_capex = min(100, int(55 + (mineral * 0.5) - (eu * 0.10)))
        scores_db["🇩🇪 BMW Group"] = {
            "scores": [bmw_china, bmw_fixed, bmw_sw, bmw_tariff, bmw_capex],
            "color": "#64748B",
            "weak": f"China luxury price erosion ({bmw_china}/100), Neue Klasse early depreciation, Premium margin defense.",
            "guard": "Leverage 'Power of Choice' modular lines (2-week pivot), protect 10%+ EBIT margin on 5/7-Series."
        }
        
        benz_china = min(100, int(75 + (tariff * 0.12)))
        benz_fixed = min(100, int(70 + (v2g * 0.08) - (eu * 0.12)))
        benz_sw = min(100, int(65 + (v2g * 0.12)))
        benz_tariff = min(100, int(60 + (tariff * 0.15)))
        benz_capex = min(100, int(65 + (mineral * 0.5) - (eu * 0.12)))
        scores_db["🇩🇪 Mercedes-Benz Group"] = {
            "scores": [benz_china, benz_fixed, benz_sw, benz_tariff, benz_capex],
            "color": COLOR_BENZ,
            "weak": f"Rigid 2030 BEV goal derailed, EQS residual value depreciation, High China exposure ({benz_china}/100).",
            "guard": "Roll back MMA to multi-powertrain, extend AMG hybrid and ICE lines, maximize Maybach/G-Class margin."
        }
        
        tsla_china = min(100, int(30 + (tariff * 0.10)))
        tsla_fixed = min(100, int(35 + (v2g * 0.05)))
        tsla_sw = max(10, int(30 - (v2g * 0.15)))
        tsla_tariff = min(100, int(75 + (tariff * 0.20)))
        tsla_capex = min(100, int(35 + (mineral * 0.5)))
        scores_db["🇺🇸 Tesla"] = {
            "scores": [tsla_china, tsla_fixed, tsla_sw, tsla_tariff, tsla_capex],
            "color": COLOR_TESLA,
            "weak": f"Lack of sub-$25k volume model, Single-stream auto hardware margin vulnerability, Tariff blocks ({tsla_tariff}/100).",
            "guard": "Scale Megapack utility ESS to 35%+ revenue, monetize NACS charging network, Unboxed 50% cost cut."
        }
        
        byd_china = min(100, int(90 + (tariff * 0.10)))
        byd_fixed = max(10, int(20 + (v2g * 0.05)))
        byd_sw = min(100, int(40 + (v2g * 0.08)))
        byd_tariff = min(100, int(85 + (tariff * 0.15)))
        byd_capex = min(100, int(90 + (mineral * 0.2)))
        scores_db["🇨🇳 BYD"] = {
            "scores": [byd_china, byd_fixed, byd_sw, byd_tariff, byd_capex],
            "color": COLOR_BYD,
            "weak": f"100% US / 35% EU tariff blockade (Tariff Risk: {byd_tariff}/100), Domestic subsidy phase-out.",
            "guard": "Operate Hungary/Brazil assembly hubs, monopolize emerging markets with $15k 5th-Gen DM-i PHEVs."
        }
        
        h_china = max(10, int(45 + (tariff * 0.08)))
        h_fixed = min(100, int(55 + (v2g * 0.05) - (eu * 0.10)))
        h_sw = max(10, int(50 - (v2g * 0.10)))
        h_tariff = min(100, int(75 + (tariff * 0.22)))
        h_capex = min(100, int(70 + (mineral * 0.6) - (eu * 0.10)))
        scores_db["🇰🇷 Hyundai-Kia"] = {
            "scores": [h_china, h_fixed, h_sw, h_tariff, h_capex],
            "color": COLOR_HYUNDAI_LIGHT,
            "weak": f"US 10-25% tariff exposure (Tariff Risk: {h_tariff}/100), Battery cell JV underutilization risk ({h_capex}/100).",
            "guard": "Instantly pivot Georgia HMGMA lines to hybrid mix (85%+ utilization), early launch of EREVs."
        }
        
        toy_china = max(10, int(40 + (tariff * 0.08)))
        toy_fixed = min(100, int(50 + (v2g * 0.05) - (eu * 0.12)))
        toy_sw = min(100, int(80 + (v2g * 0.15)))
        toy_tariff = max(10, int(30 + (tariff * 0.10)))
        toy_capex = min(100, int(60 + (mineral * 0.4) - (eu * 0.15)))
        scores_db["🇯🇵 Toyota"] = {
            "scores": [toy_china, toy_fixed, toy_sw, toy_tariff, toy_capex],
            "color": COLOR_TOYOTA,
            "weak": f"Dedicated BEV architecture lag and long-term OS software deficit (SW Risk: {toy_sw}/100).",
            "guard": "Harvest record HEV cash flow, fully fund 2028 commercial solid-state battery R&D."
        }
        
        return scores_db
        
    dynamic_radar_db = calculate_dynamic_radar_scores(eu_relaxation, tariff_level, mineral_inflation, v2g_regulation)
    
    categories = ["China Market Exposure", "Domestic Fixed/Labor Cost", "Proprietary OS Risk", "Tariff Sensitivity", "Battery Capex Risk"]
    
    col_c1, col_c2 = st.columns([1, 1])
    
    with col_c1:
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(
            r=dynamic_radar_db[oem_a]["scores"] + [dynamic_radar_db[oem_a]["scores"][0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor=hex_to_rgba(dynamic_radar_db[oem_a]["color"], 0.25),
            line=dict(color=dynamic_radar_db[oem_a]["color"], width=2.5),
            name=oem_a
        ))
        fig_r.add_trace(go.Scatterpolar(
            r=dynamic_radar_db[oem_b]["scores"] + [dynamic_radar_db[oem_b]["scores"][0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor=hex_to_rgba(dynamic_radar_db[oem_b]["color"], 0.25),
            line=dict(color=dynamic_radar_db[oem_b]["color"], width=2.5, dash='dash'),
            name=oem_b
        ))
        fig_r.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#334155"),
                angularaxis=dict(gridcolor="#334155")
            ),
            font=dict(family="Plus Jakarta Sans", size=11, color="#F8FAFC"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title="<b>Live Risk Exposure Radar (Dynamically Reshaped by Sliders)</b>",
            margin=dict(t=50, b=20, l=40, r=40)
        )
        st.plotly_chart(fig_r, use_container_width=True)
        
    with col_c2:
        st.markdown(f"""
        <div class="strategy-card" style="border-left: 5px solid {dynamic_radar_db[oem_a]['color']};">
            <h4 style="color: {dynamic_radar_db[oem_a]['color']} !important;">{oem_a}</h4>
            <p><b>🚨 Real-Time Critical Vulnerability:</b> {dynamic_radar_db[oem_a]['weak']}</p>
            <p style="margin-top: 6px;"><b>🛡️ Real-Time Tactical Guard:</b> {dynamic_radar_db[oem_a]['guard']}</p>
        </div>
        
        <div class="strategy-card" style="border-left: 5px solid {dynamic_radar_db[oem_b]['color']};">
            <h4 style="color: {dynamic_radar_db[oem_b]['color']} !important;">{oem_b}</h4>
            <p><b>🚨 Real-Time Critical Vulnerability:</b> {dynamic_radar_db[oem_b]['weak']}</p>
            <p style="margin-top: 6px;"><b>🛡️ Real-Time Tactical Guard:</b> {dynamic_radar_db[oem_b]['guard']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# Tab 4: German Automotive BCP Roadmap
# ==============================================================================
with tab_guard:
    st.markdown("#### 🛡️ 🇩🇪 Pre-emptive BCP Roadmap for German OEMs & Tier-1 Suppliers")
    st.caption("Rigorous turnaround mandates addressing China margin evaporation, CARIAD losses, and supply chain decoupling.")
    
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        # Guard 1
        st.markdown(f"""
        <div class="emergency-card" style="border-left: 5px solid {COLOR_VW};">
            <h4 style="color: {COLOR_VW} !important;">🛡️ Guard 1. Downsizing for Survival & 7.5M Equilibrium</h4>
            <div class="emergency-section">
                <span class="crisis-tag">🚨 Crisis Trigger</span><br>
                Permanent evaporation of <b>Chinese JV earnings (historically 40% of group EBIT)</b> while domestic German plants carry severe fixed overhead and energy costs 2x higher than the US.
            </div>
            <div class="emergency-section">
                <span class="action-tag">⚡ Executive Mandate</span><br>
                Formally abandon the '10M global volume' target; consolidate redundant European assembly lines to <b>cap output at 7.5M-8.0M units, cutting fixed costs by 20%</b>.
            </div>
            <div class="emergency-section">
                <span class="defense-tag">🛡️ Financial Defense</span><br>
                Exit destructive mass-market price wars to defend an <b>8-10% operating margin via 'Margin over Volume'</b>.
            </div>
        </div>
        
        <div class="emergency-card" style="border-left: 5px solid #10B981;">
            <h4 style="color: #34D399 !important;">🛡️ Guard 3. Gen-2 PHEV Cash-Cow Bridge</h4>
            <div class="emergency-section">
                <span class="crisis-tag">🚨 Crisis Trigger</span><br>
                Fleet age expansion to 12.5 years and MSRP stickiness created an EV chasm. An uncompromising 100% BEV pivot risks devastating line utilization drops.
            </div>
            <div class="emergency-section">
                <span class="action-tag">⚡ Executive Mandate</span><br>
                Leverage the 85% probable EU 2035 regulatory revision to position <b>100km+ Gen-2 PHEVs (Golf/Tiguan/Passat)</b> as core volume drivers into the mid-2030s.
            </div>
            <div class="emergency-section">
                <span class="defense-tag">🛡️ Financial Defense</span><br>
                Completely avoid EU fleet carbon fines while capturing <b>10%+ unit margins to fund ongoing structural transformation</b>.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with g_col2:
        # Guard 2
        st.markdown(f"""
        <div class="emergency-card" style="border-left: 5px solid {COLOR_TESLA};">
            <h4 style="color: #A78BFA !important;">🛡️ Guard 2. Open SDV Architecture & Proprietary OS Exit</h4>
            <div class="emergency-section">
                <span class="crisis-tag">🚨 Crisis Trigger</span><br>
                CARIAD operating losses exceeding <b>€2.5B annually ($3B)</b> with failed OS platforms delaying critical Porsche and Audi launches by up to 2 years.
            </div>
            <div class="emergency-section">
                <span class="action-tag">⚡ Executive Mandate</span><br>
                Terminate solo OS development; fully delegate zonal architecture and core software to the <b>Rivian JV, Qualcomm, Google AAOS, and Bosch</b>.
            </div>
            <div class="emergency-section">
                <span class="defense-tag">🛡️ Financial Defense</span><br>
                <b>Cut software development R&D expenditure by 50% ($1.5B/yr savings)</b> and eliminate launch bottlenecks.
            </div>
        </div>
        
        <div class="emergency-card" style="border-left: 5px solid {COLOR_TOYOTA};">
            <h4 style="color: {COLOR_TOYOTA} !important;">🛡️ Guard 4. Capex Risk Sharing & 50:50 Cell JVs</h4>
            <div class="emergency-section">
                <span class="crisis-tag">🚨 Crisis Trigger</span><br>
                Northvolt liquidity crisis highlighting the extreme hazards of unproven European cell startups + PowerCo capex over-allocation amid non-China mineral inflation (+$25/kWh).
            </div>
            <div class="emergency-section">
                <span class="action-tag">⚡ Executive Mandate</span><br>
                Freeze solo gigafactory buildouts; transition cell manufacturing into <b>50:50 joint ventures with Tier-1 cell specialists (e.g., Korean Big 3)</b>.
            </div>
            <div class="emergency-section">
                <span class="defense-tag">🛡️ Financial Defense</span><br>
                <b>De-risk multi-billion-dollar depreciation overhead by 50%</b> while ensuring full compliance with EU Battery Passport regulations.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### 📋 War-time Business Continuity Protocol (BCP Checklist)")
    st.checkbox("✅ [Geopolitical Chokepoint Defense] Established secondary overland logistics routes via Eastern Europe/North Africa + 6-month semiconductor safety stock", value=True)
    st.checkbox("✅ [Regulatory Reversal Defense] Maintained 40%+ flexible manufacturing lines capable of pivoting ICE/PHEV/BEV within 30 days", value=True)
    st.checkbox("✅ [Grid Crisis Defense] Standardized V2G bi-directional grid stabilization protocols across all 2027+ electrified platforms", value=True)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 0.8rem;'>2026~2035 Global Mobility Geopolitical Risk & Pre-emptive BCP Engine | Prepared for German Automotive Leadership</div>", unsafe_allow_html=True)
