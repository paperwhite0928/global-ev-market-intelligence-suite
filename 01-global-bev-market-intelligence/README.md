# ⚡ Global Pure BEV Market Intelligence Suite (2020–2025)
> **China's Surge, Legacy Disruption & Battery Chemistry Shifts in Global Pure Electric Vehicles**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Data Source](https://img.shields.io/badge/Data-IEA%20%7C%20OEM%20IR-059669?style=for-the-badge)](https://www.iea.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

This project provides an empirical, single-view interactive business intelligence dashboard analyzing **official 2020–2025 global Battery Electric Vehicle (BEV) market performance and battery strategies across 6 major automotive groups** (BYD, Tesla, Volkswagen Group, Hyundai-Kia Group, BMW Group, Mercedes-Benz Group).

---

## 🚀 Quick Start Guide

This project is built with zero complex web server configuration. A single execution compiles and opens an interactive single-view HTML dashboard (`dashboard.html`) directly in your browser.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate and Launch Dashboard
```bash
python src/dashboard.py
```
> The dashboard HTML (`dashboard.html`) will be generated automatically and opened in your default web browser.

---

## 📊 Executive Market Synthesis (2020–2025)

Over the 5-year period between 2020 and 2025, global pure BEV deliveries expanded **7.0x from 2.00M units (3.1% penetration) to 14.00M units (19.7% penetration)**. During this explosive transition, market leadership fundamentally transformed:

```
[2020] Tesla Dominance (25.0% Share) ────▶ [2025] BYD Ascends to #1 (16.1%) vs Tesla Normalizes (#2, 11.7%)
[2020] Legacy Leadership (VW 11.6%)   ────▶ [2025] Legacy EV Chasm Pressure & Margin Compression (VW 7.0%)
```

---

## 🔍 Core Strategic Market Takeaways

### 1. 🟥 BYD's Hyper-Scaling via Vertical Integration
* **Data**: 131k units (6.5% share in 2020) ➡️ **2.26M units (16.1% share in 2025)** (+2.13M units added, **17.2x expansion**).
* **Strategic Drivers**:
  * 100% in-house manufacturing across cells (Blade Battery LFP), power electronics, and drivetrains provided unassailable cost advantages.
  * Domestic Chinese scale enabled aggressive mass-market price parity ($15k–$25k price brackets) followed by international expansion into Europe, Southeast Asia, and Latin America.

### 2. 🟪 Tesla's Transition from Monopolist to Mature Player
* **Data**: 25.0% global market share in 2020 ➡️ **11.7% in 2025 (-13.3%p share contraction)**.
* **Strategic Drivers**:
  * After peaking in 2023 (1.81M units), deliveries normalized through 2024 (-1.0%) and 2025 (-8.4%) to 1.64M units.
  * Heavy reliance on aging Model 3/Y architectures and delayed sub-$25k offerings constrained incremental market expansion despite price cut campaigns.

### 3. 🩶 Legacy OEMs: Dedicated Architectures & The "EV Chasm"
* **Mercedes-Benz Group**: Luxury BEV demand faced price resistance; volume contracted from 241k (2023) to **169k units (2025, 1.2% share)**.
* **Volkswagen Group**: Maintained legacy volume leadership at **983k units (7.0% share)** via the MEB platform, but lost significant market share in China to domestic OEMs.
* **Hyundai-Kia Group**: Expanded to **514k units (3.7% share)** on the strength of its 800V E-GMP dedicated platform in Western markets.

### 4. 🔋 Battery Technology Strategy & Raw Material Dynamics
* **LFP / Cell-to-Pack (CTP)**: Emerged as the dominant chemistry for mass-market affordability (BYD 100%, Tesla Standard Range).
* **High-Nickel NCM/NCA**: Remained the gold standard for premium range and charging speed, but exposed legacy OEMs to battery commodity volatility during the 2022–2024 pricing spikes.

---

## 📈 Empirical Data Fact Sheet (2020 vs 2025)

| Automaker (OEM) | 2020 Volume | 2020 Share | 2025 Volume | 2025 Share | **5-Yr Net Added** | 5-Yr Growth | Primary Battery Strategy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 🟥 **BYD** | 130,970 | 6.55% | **2,256,714** | **16.12%** | **+2,125,744** | **17.2x** | Blade Battery (100% LFP) |
| 🟪 **Tesla Inc.** | 499,550 | 24.98% | **1,640,000** | **11.71%** | **+1,140,450** | **3.3x** | LFP (RWD) / NCA (AWD/Perf) |
| 🩵 **Volkswagen Group** | 231,600 | 11.58% | **983,000** | **7.02%** | **+751,400** | **4.2x** | NCM Mainstream + LFP Entry |
| 🟦 **Hyundai-Kia Group** | 90,000 | 4.50% | **513,669** | **3.67%** | **+423,669** | **5.7x** | NCM (E-GMP 800V) + LFP |
| ⬛ **BMW Group** | 44,531 | 2.23% | **442,072** | **3.16%** | **+397,541** | **9.9x** | NCM (Gen5/Gen6 Prismatic) |
| 🩶 **Mercedes-Benz Group** | 50,000 | 2.50% | **168,800** | **1.21%** | **+118,800** | **3.4x** | NCM (EVA / MMA Dedicated) |
| 🌐 **Global Total BEV Market** | **2,000,000** | 100.0% | **14,000,000** | 100.0% | **+12,000,000** | **7.0x** | IEA Official Statistics |

---

## 🖥️ Dashboard Architecture

Built in a modern responsive layout with four dedicated interactive tabs:

1. **📊 1. Global Market Overview**: Penetration trajectory, historical volume curves, 2025 leaderboard, top-6 delivery distribution.
2. **📈 2. Market Share & Growth Dynamics**: 5-year global market share evolution and annual YoY growth rate comparisons.
3. **🔋 3. Battery Technology Strategy**: Chemistries matrix (LFP, NCM, NCA, Blade) and technical spec cards (cost, density, safety).
4. **🚀 4. YoY Growth & Net Volume Expansion**: Trajectory against global benchmark, annual net volume additions, and 5-year pivot expansion table.

---

## 🎨 OEM Brand Identity Color Palette

All charts and UI elements strictly follow OEM corporate branding guidelines:
* **BYD**: Vivid Crimson Red (`#E11D48`)
* **Tesla Inc.**: Electric Violet (`#7C3AED`)
* **Volkswagen Group**: Electrified Cyan / Teal (`#00A8A8`)
* **BMW Group**: Pure Obsidian Black (`#000000`)
* **Hyundai-Kia Group**: Deep Indigo Blue (`#00287A`)
* **Mercedes-Benz Group**: Metallic Slate Grey (`#7F8C8D`)

---

## 📁 Repository Structure

```text
01-global-bev-market-intelligence/
├── data/
│   ├── ev_sales_by_company.csv      # Annual official pure BEV deliveries by OEM (2020-2025)
│   ├── global_bev_market.csv        # IEA official global BEV volume & market penetration
│   ├── market_share_by_company.csv  # Historical OEM market share calculations
│   └── battery_strategy.csv         # Battery chemistry & packaging deployment status
├── src/
│   └── dashboard.py                 # Core dashboard compilation & browser launch script
├── dashboard.html                   # Single-view interactive dashboard (auto-compiled)
├── requirements.txt                 # Python dependencies
└── README.md                        # Strategic documentation & market analysis
```

---

## 📚 Data Provenance & Verification

* **BYD**: Official Annual Financial Disclosures & Monthly IR NEV Passenger BEV Sales Announcements.
* **Tesla Inc.**: Official IR Quarterly Production & Deliveries Reports (SEC Form 10-K).
* **Volkswagen Group**: Annual Financial Reports & Official Deliveries to Customers Disclosures.
* **Hyundai-Kia Group**: Hyundai Motor & Kia Global Wholesale Delivery Disclosures.
* **BMW Group**: Annual Reports & Investor Relations Key Performance Indicators.
* **Mercedes-Benz Group**: Mercedes-Benz Group IR Fact Sheets & Delivery Releases.
* **Global Market**: International Energy Agency (IEA) *Global EV Outlook* Official Database.

---
*Authored for Global Automotive Market Analysis & Strategy Review | Pure BEV Intelligence*
