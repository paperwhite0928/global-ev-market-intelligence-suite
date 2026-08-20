# 🚘 Toyota Multi-Pathway vs BEV Strategy Intelligence
> **A Data-Driven Empirical Validation of Toyota's Hybrid-First Electrification Strategy & 2026–2030 Predictive Scenarios**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Data-Verified](https://img.shields.io/badge/Data-Toyota%20IR%20%7C%20IEA%20Official-059669?style=for-the-badge)](https://global.toyota/en/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

## Executive Summary

When global automakers and capital markets rushed into an aggressive "all-in Battery Electric Vehicle (BEV)" pivot between 2020 and 2023, **Toyota Motor Corporation took a widely scrutinized, contrarian stance**: adhering to its **"Multi-Pathway" approach**, with **Hybrid Electric Vehicles (HEV)** remaining the core pillar.

This project empirically proves the economic and environmental validity of Toyota's strategy using **100% verified official data** (Toyota Global IR, IEA, London Metal Exchange). Furthermore, it provides an **interactive 2026–2030 predictive forecasting engine** exclusively modeling Toyota's future profitability, sales mix, and next-generation battery roadmap.

```
                    ┌─────────────────────────────────────────────────────────┐
                    │            THE TOYOTA PLAYBOOK IN A NUTSHELL            │
                    ├────────────────────────────┬────────────────────────────┤
                    │   2024 Global HEV Volume   │   FY2024 Operating Margin  │
                    │       4.16M Units          │            11.9%           │
                    │  (+21.6% YoY / 91.8% Mix)  │   (Record ¥5.35T Op Profit)│
                    ├────────────────────────────┼────────────────────────────┤
                    │ Battery Resource Principle │ 2024–2030 Cum. Profit (Est)│
                    │         1 : 6 : 90         │           $269.4B          │
                    │  (1 BEV = 90 HEV Minerals) │ (Self-funded Solid-State)  │
                    └────────────────────────────┴────────────────────────────┘
```

---

## Key Strategic Insights (Data-Driven)

### 1. 🏆 The Pragmatic Triumph (Cash Cow Validation)
- In 2024, Toyota sold **4.16 million HEVs** (representing **91.8% of its electrified sales**) while maintaining a steady 141k BEVs.
- While competitors suffered massive margin erosion and EV division losses during the "EV Chasm", Toyota achieved an **all-time high operating profit of ¥5.35 Trillion (~$37.8B) with an 11.9% operating margin**.

### 2. 🌐 Macro Shielding: Mineral Volatility & Charging Deficits
- **Battery Mineral Volatility**: Lithium carbonate spiked from **$8,500/ton (2020)** to **$78,000/ton (2022)** before dropping to **$14,000/ton (2024)**. Toyota’s small 1.3 kWh HEV battery packs shielded the company from massive margin shocks that crippled large-pack BEV makers.
- **Charging Infrastructure Reality**: IEA data reveals North America has only **~710 public chargers per million inhabitants**, making hybrids the only globally viable mass-market electrification solution today.

### 3. 🔋 The 1:6:90 Principle & Fleet Carbon Abatement
- The battery raw materials required for **one 75 kWh BEV** can produce **six 15 kWh PHEVs** or **ninety 1.3 kWh HEVs**.
- In mineral-constrained markets, deploying 90 HEVs achieves **~43.2 tons of annual CO2 abatement** vs. **~3.2 tons for 1 BEV** (**13.5x higher fleet carbon reduction efficiency**).

### 4. 🔮 Toyota-Dedicated 2026–2030 Forecast Scenarios
- **Base Scenario (Pragmatic Multi-Pathway)**: HEV volume stabilizes at 5.2M units while BEV ramps to 1.8M by 2030. Cumulative 2024–2030 operating profit reaches **$269.4B**, fully funding gigacasting and next-gen solid-state battery plants without external debt.
- **Bull Scenario (Extended Chasm & Hybrid Supercycle)**: HEV demand surges >6.2M units, sustaining peak margins of 11.8%+ and generating **$288B+ cumulative cash flow**.
- **Accelerated Scenario (Solid-State Tech Leapfrog)**: Commercialization of solid-state batteries in 2027 scales BEV volume to 2.8M units by 2030 with healthy margins.

---

## Verified Data Sources

All datasets in this repository are cross-verified against primary official disclosures:
- **Toyota Motor Corporation**: Official Global Newsroom (*Sales, Production & Export Results*, Consolidated Financial Statements Form 20-F).
- **International Energy Agency (IEA)**: *Global EV Outlook 2024* (Public and fast charging infrastructure).
- **London Metal Exchange (LME) & Fastmarkets**: Benchmark battery raw material spot prices (Lithium, Nickel, Cobalt, Graphite).
- **OEM Investor Relations**: Official BEV delivery disclosures (Tesla, BYD, Volkswagen Group, BMW Group, Mercedes-Benz, Hyundai-Kia, Ford, GM).

---

## Interactive Dashboard Suite

The project includes an **institutional-grade Streamlit application** structured into 5 executive strategy tabs:

| Tab | Focus Area | Interactive Capabilities |
| :--- | :--- | :--- |
| **1. Strategic Proof** | Toyota Playbook & Financials | Region selector, powertrain mix bar charts, revenue/margin dual-axis trends. |
| **2. Macro Reality** | Minerals & Charging Gaps | LME commodity price lines, IEA charging density per million inhabitants. |
| **3. Battery Economics** | 1:6:90 Resource Optimization | Battery equivalency comparisons and fleet CO2 abatement multiplier. |
| **4. Forecast Simulator** | **Toyota 2026–2030 Engine** | Scenario presets (Base/Bull/Accelerated) + sliders for 2030 targets, battery pack costs, and HEV margin premiums. |
| **5. Strategic Takeaways** | Executive Summary & Lessons | Core strategic takeaways for corporate strategy and investment decision-making. |

---

## Project Structure

```text
02-toyota-hybrid-multipathway-strategy/
├── data/
│   ├── raw/                  # Verified primary source datasets
│   │   ├── toyota_electrified_sales.csv   # Toyota + Lexus official sales (2019-2025)
│   │   ├── financials.csv                 # Toyota consolidated revenue & margins
│   │   ├── battery_material_prices.csv    # LME/Fastmarkets mineral prices
│   │   ├── charging_infrastructure.csv    # IEA official charger statistics
│   │   ├── company_bev_sales.csv          # Peer OEM official BEV deliveries
│   │   ├── ev_investments.csv             # Corporate CAPEX & R&D disclosures
│   │   └── tariff_events.csv              # Global trade & EV policy timeline
│   └── processed/            # Cleaned, normalized analysis tables
├── src/
│   ├── clean_data.py         # Automated data cleaning pipeline
│   ├── forecast.py           # Toyota-dedicated 2026-2030 simulation engine
│   ├── load_data.py          # Data ingestion utilities
│   ├── utils.py              # Directory paths & formatting helpers
│   └── visualization.py      # Plotting configurations
├── dashboard/
│   └── app.py                # Executive Streamlit Intelligence Dashboard (Port 8501)
├── notebooks/                # Exploratory research notebooks (01 to 07)
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
└── README.md                 # Strategic intelligence documentation
```

---

## Quick Start Guide

### 1. Local Setup
```bash
# Navigate to project directory
cd 02-toyota-hybrid-multipathway-strategy

# Install dependencies
pip install -r requirements.txt

# Run data processing pipeline
python -m src.clean_data

# Launch the Executive Dashboard on Port 8501
streamlit run dashboard/app.py --server.port 8501
```

Access the interactive dashboard at **`http://localhost:8501`**.

---

## License

This project is licensed under the [MIT License](LICENSE).
All financial and operational figures are sourced from audited public filings for educational and strategic analysis purposes.
