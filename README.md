# 🚗 Global EV Market Intelligence & Scenario Forecasting Suite
> **An End-to-End Strategic Intelligence, Econometric Causal Modeling & Geopolitical Scenario Simulation Suite for the Global Automotive Electrification Transition (2020–2035)**

---

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Data-Verified](https://img.shields.io/badge/Data-IEA%20%7C%20OEM%20IR%20%7C%20LME-059669?style=for-the-badge)](https://www.iea.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## 📌 1. Project Overview & Core Mission

The global automotive industry is undergoing its most turbulent structural transition in a century. Moving beyond simple hype cycles and aggressive mandates, this suite provides an **institutional-grade, empirical quantitative framework** that:

1. **Evaluates Historical Market Share Dynamics (2020–2025)**: Tracks 100% pure BEV delivery volumes, regional penetration rates, and battery chemistry adoption across the top 6 global automotive groups.
2. **Empirically Validates Powertrain Diversification**: Investigates the economic, financial, and carbon abatement validity of **Toyota's Hybrid-First "Multi-Pathway"** strategy against pure-play BEV competitors.
3. **Quantifies Macroeconomic & Policy Causal Drivers**: Combines **Panel Fixed-Effects Econometrics (Panel OLS, VAR)** and **Explainable Machine Learning (XGBoost + SHAP TreeExplainer)** across 3 major economic zones (**US, EU, CN**).
4. **Stress-Tests Geopolitical & Trade Risks (2026–2035)**: Simulates regulatory whiplash (EU 2035 mandate delays), tariff escalation, supply chain decoupling, and power grid constraints, formulating a pre-emptive **Business Continuity Planning (BCP)** playbook for legacy automakers.

---

## 📊 2. Verified Data Provenance & Calibration

All datasets across the 4 modules are calibrated with 100% fidelity against primary audited disclosures and benchmark institutions:

* **Primary OEM Financial & Delivery Reports**: SEC Form 10-K / 20-F, Quarterly Earnings Disclosures, and IR Press Releases (**Toyota Motor Corporation, Tesla Inc., BYD Company, Volkswagen Group, Hyundai-Kia Group, BMW Group, Mercedes-Benz Group**).
* **International Energy Agency (IEA)**: *Global EV Outlook (2020–2025)* for global fleet sizes, penetration rates, and public/fast charger infrastructure densities.
* **Commodity Benchmark Pricing**: London Metal Exchange (LME) & Fastmarkets spot and contract prices for battery-grade Lithium Carbonate, Nickel, Cobalt, and Graphite.
* **Macroeconomic & Policy Levers**: U.S. Federal Reserve Economic Data (FRED), European Central Bank (ECB), and official trade tariff schedules (U.S. Section 301, EU Countervailing Duties).

---

## 🛠 3. Unified Tech Stack

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       UNIFIED TECH STACK                                        │
├──────────────────────────────┬──────────────────────────────────┬───────────────────────────────┤
│    Languages & Runtime       │     Analytics & Econometrics     │     Interactive Frontends     │
├──────────────────────────────┼──────────────────────────────────┼───────────────────────────────┤
│ • Python 3.10+               │ • Pandas & NumPy                 │ • Streamlit (Ports 8501-8503) │
│ • TypeScript / JavaScript    │ • Linearmodels (Panel Fixed OLS) │ • Plotly Express & Graph Obj. │
│ • Node.js & Vite 6           │ • Statsmodels (VAR Modeling)     │ • React 19 & Tailwind CSS     │
│ • HTML5 / CSS3 / ESBuild     │ • Scikit-Learn & XGBoost / SHAP  │ • Standalone Responsive HTML5 │
└──────────────────────────────┴──────────────────────────────────┴───────────────────────────────┘
```

---

## 📂 4. 4-Stage Project Architecture & Strategic Insights

```text
global-automotive-strategy-suite/
│
├── 01-global-bev-market-intelligence/      # 📊 Stage 1: Global Pure BEV Market Deliveries & Battery Strategy
├── 02-toyota-hybrid-multipathway-strategy/ # 🚘 Stage 2: Toyota Multi-Pathway Proof & 2026-2030 Forecasting Engine
├── 03-bev-adoption-drivers-econometrics/   # ⚡ Stage 3: 3-Region Panel Econometrics & XGBoost-SHAP Causal Platform
└── 04-mobility-geopolitical-bcp-engine/    # 🛡️ Stage 4: 2026-2035 Geopolitical Risk Simulator & BCP Playbook
```

---

### 📊 Stage 1: Global BEV Market Overview & Market Share Analysis (2020–2025)
* **Directory**: [`01-global-bev-market-intelligence/`](./01-global-bev-market-intelligence)
* **Architecture**: Standalone Python build script compiling a single-view, responsive Plotly HTML dashboard ([`dashboard.html`](./01-global-bev-market-intelligence/dashboard.html)).
* **Key Strategic Takeaways**:
  * **Global Market Expansion**: Pure BEVs grew **7.0x from 2.00M units (3.1% penetration) to 14.00M units (19.7% penetration)** in 5 years.
  * **BYD's Vertical Dominance**: Surged **+17.2x (131k $\rightarrow$ 2.26M units, 16.1% share)**, claiming the Global #1 pure BEV spot through complete in-house battery (Blade LFP) and power electronics integration.
  * **Tesla's Normalization**: Diluted from 24.98% (2020) to **11.71% (1.64M units in 2025)** under product aging and intensifying price competition.
  * **Legacy Differentiation**: **Volkswagen Group (983k units, 7.0% share)** and **Hyundai-Kia Group (514k units, 3.7% share)** secured resilient podium positions via dedicated modular architectures (MEB and 800V E-GMP).

---

### 🚘 Stage 2: Toyota Multi-Pathway (HEV-First) Strategy Validation (2019–2030)
* **Directory**: [`02-toyota-hybrid-multipathway-strategy/`](./02-toyota-hybrid-multipathway-strategy)
* **Architecture**: Streamlit Executive Application (Port **8501**), automated data cleaning pipeline, and 2026–2030 simulation engine.
* **Key Strategic Takeaways**:
  * **Cash Cow Validation**: In FY2024, Toyota delivered **4.16M HEVs (91.8% of electrified volume)**, producing an all-time record operating profit of **¥5.35 Trillion (~$37.8B) with an 11.9% margin** while competitors bled cash on pure EV discounting.
  * **The 1:6:90 Principle**: Battery raw materials for a single 75 kWh BEV can produce **6 PHEVs (15 kWh) or 90 HEVs (1.3 kWh)**. In mineral-constrained supply chains, deploying 90 HEVs achieves **~43.2 tons/year fleet CO2 reduction vs 3.2 tons for 1 BEV** (**13.5x higher carbon efficiency**).
  * **Self-Funded Solid-State Transition**: Generated **$269B+ in cumulative operating cash flows** (2024–2030) to fully self-fund gigacasting and next-generation Solid-State Battery plants (launching 2027–2028) without debt.

---

### ⚡ Stage 3: Causal Driver Econometrics & ML Modeling (US, EU, CN)
* **Directory**: [`03-bev-adoption-drivers-econometrics/`](./03-bev-adoption-drivers-econometrics)
* **Architecture**: Dual-stack engine featuring a Python Streamlit econometric dashboard (Port **8502**) and a modern React 19 + TypeScript frontend.
* **Key Strategic Takeaways**:
  * **Charging Infrastructure Prerequisite**: Public charger density (+0.78 correlation) is the single most persistent positive driver across all lag specifications (0M, 1M, 3M, 6M) and SHAP feature importance rankings.
  * **Commodity Price Transmission**: Battery pack cost deflation ($151/kWh in 2022 $\rightarrow$ $105/kWh in 2025) transmits to vehicle deliveries with a **1 to 3-month lag (-0.42 correlation)**.
  * **Protectionist Tariff Shock**: US 100% tariffs and EU anti-subsidy duties caused immediate import contraction, accelerating market bifurcation between China/Global South and tariff-protected Western markets.

---

### 🛡️ Stage 4: Geopolitical Scenario Simulator & Pre-emptive BCP Playbook (2026–2035)
* **Directory**: [`04-mobility-geopolitical-bcp-engine/`](./04-mobility-geopolitical-bcp-engine)
* **Architecture**: Dynamic Streamlit Simulator (Port **8503**), 35-page strategic consulting whitepaper, and 12-slide executive pitch deck.
* **Key Strategic Takeaways**:
  * **4 Exogenous Levers**: Models EU 2035 Mandate Delay Intensity, Western Tariffs & Connected Car Embargoes, Non-China Mineral Premiums (+$0–$50/kWh), and AI Grid Crisis / V2G Mandates in real-time.
  * **The 4 Pre-emptive BCP Guards for German Leadership**:
    1. **Guard 1 (Downsizing & 7.5M Equilibrium)**: Consolidate European assembly to 7.5M–8.0M units, cutting fixed costs by 20% to defend 8–10% EBIT (*Margin over Volume*).
    2. **Guard 2 (Open SDV Alliances)**: Terminate CARIAD solo OS development ($3B/yr burn); delegate zonal architecture to **Rivian JV, Qualcomm, Google AAOS, and Bosch**.
    3. **Guard 3 (Gen-2 PHEV Cash-Cow Bridge)**: Capitalize on EU regulatory flexibility by deploying **100km+ Gen-2 PHEVs** to fund transition capex.
    4. **Guard 4 (50:50 Cell JVs)**: Freeze solo gigafactories; partner with Tier-1 battery specialists to split multi-billion depreciation risks.

---

## 💻 5. Getting Started & Execution Guide

### ⚙️ Prerequisites & Environment Setup

Ensure **Python 3.10+** and Git are installed. It is recommended to create an isolated Python virtual environment:

```powershell
# 1. Clone or navigate to the root workspace
cd global-automotive-strategy-suite

# 2. Create and activate a Python virtual environment
python -m venv .venv

# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
# source .venv/bin/activate

# 3. (Optional) Install all suite dependencies at once
pip install -r requirements.txt
```

---

### 🚀 Step-by-Step Module Execution Commands

Each application operates on its designated localhost port to enable simultaneous multi-window strategic analysis:

```
┌────────────────────────┬───────────────────────────────────────────┬──────────────┬─────────────────────────┐
│         Module         │            Directory Location             │ Local Port   │     Access Endpoint     │
├────────────────────────┼───────────────────────────────────────────┼──────────────┼─────────────────────────┤
│ 01. Market Overview    │ 01-global-bev-market-intelligence/        │ Local File   │ dashboard.html          │
│ 02. Toyota Strategy    │ 02-toyota-hybrid-multipathway-strategy/   │ Port 8501    │ http://localhost:8501   │
│ 03. Adoption Drivers   │ 03-bev-adoption-drivers-econometrics/     │ Port 8502    │ http://localhost:8502   │
│ 04. Geopolitical BCP   │ 04-mobility-geopolitical-bcp-engine/      │ Port 8503    │ http://localhost:8503   │
└────────────────────────┴───────────────────────────────────────────┴──────────────┴─────────────────────────┘
```

#### 📊 1. Run Stage 1: Global BEV Market Intelligence Dashboard
```powershell
cd 01-global-bev-market-intelligence
pip install -r requirements.txt
python src/dashboard.py
```
> Automatically generates [`dashboard.html`](./01-global-bev-market-intelligence/dashboard.html) and opens it in your default web browser.

---

#### 🚘 2. Run Stage 2: Toyota Multi-Pathway Strategy Simulator (Port 8501)
```powershell
cd ../02-toyota-hybrid-multipathway-strategy
pip install -r requirements.txt
python -m src.clean_data
streamlit run dashboard/app.py --server.port 8501
```
> Access live dashboard at **`http://localhost:8501`**.

---

#### ⚡ 3. Run Stage 3: BEV Adoption Drivers Econometric Platform (Port 8502)
```powershell
cd ../03-bev-adoption-drivers-econometrics
pip install -r ev_driver_analysis/requirements.txt
streamlit run ev_driver_analysis/app.py --server.port 8502
```
> Access live dashboard at **`http://localhost:8502`**.  
> *(Optional: Launch React 19 web app by running `npm install && npm run dev`)*.

---

#### 🛡️ 4. Run Stage 4: Geopolitical Risk & Pre-emptive BCP Engine (Port 8503)
```powershell
cd ../04-mobility-geopolitical-bcp-engine
pip install -r requirements.txt
streamlit run app.py --server.port 8503
```
> Access live dashboard at **`http://localhost:8503`**.

---

## 📑 6. Complete Deliverable Artifacts Manifest

```text
├── README.md                                # Master Portfolio Architecture & Guide
│
├── 01-global-bev-market-intelligence/
│   ├── src/dashboard.py                     # Single-View HTML Builder
│   ├── dashboard.html                       # Standalone Plotly Report
│   ├── requirements.txt                     # Dependencies (pandas, plotly, numpy)
│   └── data/                                # 2020-2025 Historical Sales & Battery Strategy
│
├── 02-toyota-hybrid-multipathway-strategy/
│   ├── dashboard/app.py                     # Streamlit Forecast Application (Port 8501)
│   ├── src/clean_data.py                    # Automated Data Cleaning Pipeline
│   ├── src/forecast.py                      # 2026-2030 Simulation Engine
│   ├── notebooks/ (01 to 07)                # Exploratory Research Notebooks
│   ├── LICENSE                              # MIT License
│   └── requirements.txt                     # Dependencies
│
├── 03-bev-adoption-drivers-econometrics/
│   ├── ev_driver_analysis/app.py            # Streamlit Econometric Platform (Port 8502)
│   ├── ev_driver_analysis/src/              # Panel OLS, VAR IRF, XGBoost & SHAP Modules
│   ├── src/ (App.tsx, components)           # React 19 + TypeScript Application
│   ├── package.json                         # Node Package Specification
│   └── ev_driver_analysis/requirements.txt  # Dependencies
│
└── 04-mobility-geopolitical-bcp-engine/
    ├── app.py                               # Geopolitical Risk Simulator (Port 8503)
    ├── mobility_geopolitical_risk_whitepaper.md # 35-Page Strategic Consulting Whitepaper
    ├── presentation_pitch_deck.md           # 12-Slide Executive Board Pitch Deck
    └── requirements.txt                     # Dependencies
```

---

## 📄 License & Compliance

This project suite is open-sourced under the [MIT License](https://opensource.org/licenses/MIT).  
All corporate financial figures, production metrics, and commodity indices are compiled from public regulatory filings and benchmark industry disclosures for research, educational, and corporate strategy evaluation.

---
<div align="center">
<b>Global EV Market Intelligence & Scenario Forecasting Suite</b><br>
<i>Empirical Data · Econometric Rigor · Strategic Foresight</i>
</div>
