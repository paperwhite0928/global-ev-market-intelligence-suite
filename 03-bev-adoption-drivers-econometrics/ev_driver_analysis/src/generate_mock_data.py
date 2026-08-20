"""
generate_mock_data.py - Synthetic Fallback Panel Data Generator
Generates a realistic 1,512-row monthly panel dataset (72 months: 2020-01 to 2025-12 x 3 regions x 7 OEMs).
Embedded Shocks & Trends:
- 2022 Lithium Carbonate Price Spike ($70k+/ton)
- 2024 US (100%) and EU Anti-Subsidy Tariff Increases
- 2024 Hertz Used-EV Liquidation / Depreciation Shock
- BYD Rapid Growth Acceleration & High LFP Mix
- Toyota Low Initial BEV Baseline
"""

import pandas as pd
import numpy as np

# Official Annual BEV Sales Baseline from Company IR Reports (2020 - 2025)
OFFICIAL_ANNUAL_SALES = {
    "BYD": {2020: 130970, 2021: 320810, 2022: 911140, 2023: 1574822, 2024: 1764992, 2025: 2256714},
    "Tesla": {2020: 499647, 2021: 936222, 2022: 1313851, 2023: 1808581, 2024: 1789226, 2025: 1636129},
    "Hyundai-Kia Group": {2020: 90000, 2021: 142000, 2022: 338000, 2023: 425000, 2024: 457000, 2025: 513669},
    "Volkswagen Group": {2020: 231600, 2021: 452900, 2022: 572100, 2023: 771100, 2024: 744571, 2025: 983120},
    "BMW Group": {2020: 44541, 2021: 103855, 2022: 215755, 2023: 376183, 2024: 426594, 2025: 442072},
    "Mercedes-Benz Group": {2020: 50000, 2021: 99300, 2022: 149227, 2023: 240668, 2024: 224000, 2025: 168823},
    "Toyota": {2020: 5000, 2021: 14000, 2022: 24000, 2023: 104000, 2024: 140000, 2025: 180000}
}

# Regional Distribution Share by OEM (CN, EU, US)
REGIONAL_SHARES = {
    "BYD": {"CN": 0.90, "EU": 0.08, "US": 0.02},
    "Tesla": {"CN": 0.33, "EU": 0.27, "US": 0.40},
    "Hyundai-Kia Group": {"CN": 0.08, "EU": 0.46, "US": 0.46},
    "Volkswagen Group": {"CN": 0.28, "EU": 0.60, "US": 0.12},
    "BMW Group": {"CN": 0.30, "EU": 0.52, "US": 0.18},
    "Mercedes-Benz Group": {"CN": 0.28, "EU": 0.54, "US": 0.18},
    "Toyota": {"CN": 0.25, "EU": 0.35, "US": 0.40}
}

# Monthly Seasonal Weights (Sum = 12.0)
MONTHLY_WEIGHTS = {
    1: 0.72, 2: 0.68, 3: 1.05, 4: 0.88, 5: 0.95, 6: 1.12,
    7: 0.90, 8: 0.92, 9: 1.15, 10: 1.02, 11: 1.18, 12: 1.43
}

def generate_panel_data(output_path: str = None) -> pd.DataFrame:
    np.random.seed(42)
    
    dates = pd.date_range(start="2020-01-01", end="2025-12-01", freq="MS")
    regions = ["US", "EU", "CN"]
    oems = [
        "Tesla", "BYD", "Volkswagen Group", "Hyundai-Kia Group",
        "BMW Group", "Mercedes-Benz Group", "Toyota"
    ]
    
    records = []
    
    for date_idx, dt in enumerate(dates):
        year = dt.year
        month = dt.month
        ym_str = dt.strftime("%Y-%m")
        t = date_idx  # 0 to 71
        
        # 1. Macro & Commodity Drivers (Calibrated to Real World Benchmarks)
        # Lithium Carbonate ($/ton): 2020: $7k -> 2022: $70k -> 2024: $13k
        if year == 2020:
            lithium_base = 7500 + t * 200
        elif year == 2021:
            lithium_base = 10000 + (t - 12) * 2000
        elif year == 2022:
            lithium_base = 38000 + 33000 * np.sin(np.pi * (t - 24) / 12)
        elif year == 2023:
            lithium_base = 35000 - (t - 36) * 1800
        else: # 2024-2025
            lithium_base = 13500 + np.random.normal(0, 400)
            
        lithium_price = max(7000, lithium_base + np.random.normal(0, 800))
        nickel_price = max(13000, 16500 + 7000 * np.sin(t / 8) + np.random.normal(0, 600))
        cobalt_price = max(24000, 34000 + 11000 * np.cos(t / 10) + np.random.normal(0, 800))
        
        # Battery Pack Price ($/kWh): 2020: $137 -> 2022: $151 -> 2024: $115 -> 2025: $105
        if year == 2020:
            b_base = 137.0 - month * 0.4
        elif year == 2021:
            b_base = 132.0 + month * 0.3
        elif year == 2022:
            b_base = 145.0 + 8.0 * np.sin(np.pi * month / 12)
        elif year == 2023:
            b_base = 148.0 - (month * 0.8)
        elif year == 2024:
            b_base = 125.0 - (month * 0.9)
        else:
            b_base = 110.0 - (month * 0.5)
            
        battery_pack_price = max(92.0, b_base + np.random.normal(0, 1.2))
        
        # WTI Oil Price ($/bbl): 2020: $39 -> 2022: $94 (peak $120) -> 2024: $76
        if year == 2020:
            oil_base = 32.0 + month * 1.5
        elif year == 2021:
            oil_base = 52.0 + month * 2.0
        elif year == 2022:
            oil_base = 85.0 + 25.0 * np.sin(np.pi * month / 12)
        elif year == 2023:
            oil_base = 78.0 + np.random.normal(0, 3.0)
        else:
            oil_base = 76.0 + np.random.normal(0, 2.5)
        wti_oil = max(30.0, oil_base)
        
        # Central Bank Policy Interest Rate (%): 2020: 0.25% -> 2023: 5.25% -> 2025: 4.25%
        if year <= 2021:
            interest_rate = 0.25 + np.random.normal(0, 0.02)
        elif year == 2022:
            interest_rate = 0.50 + (month * 0.35)
        elif year == 2023:
            interest_rate = 4.75 + (month * 0.05)
        elif year == 2024:
            interest_rate = 5.25 - (0.50 if month >= 9 else 0.0)
        else: # 2025
            interest_rate = 4.50 - (month * 0.04)
        interest_rate = max(0.25, round(interest_rate, 2))
        
        cpi_index = round(100.0 + t * 0.42 + np.random.normal(0, 0.2), 2)
        gdp_growth = round(2.3 + 1.1 * np.sin(t / 6) + np.random.normal(0, 0.15), 2)
        semi_lead_time = round(12.0 + (16.0 if 12 <= t <= 32 else 0.0) + np.random.normal(0, 0.8), 1)
        
        for region in regions:
            # Regional Public Charging Infrastructure & Policies
            if region == "US":
                public_chargers = round(320 + t * 15.2 + np.random.normal(0, 8), 1)
                fast_chargers_ratio = round(0.22 + t * 0.0022, 3)
                electricity_price = round(0.132 + t * 0.00065, 4)
                base_tariff = 2.5 if year < 2024 else 102.5  # 102.5% US Section 301 on China EV
                ira_feoc = 1.0 if (year >= 2024) else 0.0
                eu_co2_tightening = 0.0
                cn_trade_in = 0.0
                base_subsidy_ratio = round(max(0.02, 0.10 - t * 0.0008), 3)
                
            elif region == "EU":
                public_chargers = round(520 + t * 24.5 + np.random.normal(0, 12), 1)
                fast_chargers_ratio = round(0.20 + t * 0.0028, 3)
                electricity_price = round(0.235 + (0.09 if 2022 <= year <= 2023 else 0.0) + t * 0.0008, 4)
                base_tariff = 10.0 if year < 2024 else (20.0 if t < 56 else 35.3) # EU Countervailing late 2024
                ira_feoc = 0.0
                eu_co2_tightening = 1.0 if (year >= 2025) else 0.0
                cn_trade_in = 0.0
                base_subsidy_ratio = round(max(0.01, 0.12 - t * 0.0012), 3)
                
            else: # CN
                public_chargers = round(1100 + t * 48.0 + np.random.normal(0, 20), 1)
                fast_chargers_ratio = round(0.44 + t * 0.0032, 3)
                electricity_price = round(0.088 + t * 0.00018, 4)
                base_tariff = 15.0
                ira_feoc = 0.0
                eu_co2_tightening = 0.0
                cn_trade_in = 1.0 if (year >= 2024 and month >= 4) else 0.0
                base_subsidy_ratio = round(max(0.03, 0.14 - t * 0.0018), 3)

            # Used EV Depreciation Shock (Hertz sell-off & Price cuts in 2023-2024)
            hertz_shock = 9.5 if (year == 2024 and month <= 8) else 0.0
            used_depreciation = round(16.0 + (interest_rate * 1.8) + hertz_shock + np.random.normal(0, 0.8), 2)

            for oem in oems:
                # 1. Target Monthly Volume directly anchored to Official IR Annual Sales
                annual_target = OFFICIAL_ANNUAL_SALES[oem][year]
                reg_share = REGIONAL_SHARES[oem][region]
                month_weight = MONTHLY_WEIGHTS[month] / 12.0
                
                # Base monthly volume exactly calibrating to the target
                base_monthly_sales = annual_target * reg_share * month_weight
                
                # Micro-variation from macro drivers
                macro_shock = (
                    - 0.08 * ((battery_pack_price - 125.0) / 30.0)
                    - 0.05 * ((interest_rate - 2.5) / 2.5)
                    - 0.06 * ((used_depreciation - 22.0) / 10.0)
                    + 0.04 * (np.log(public_chargers) - 6.5)
                )
                
                # Special policy shocks (IRA FEOC for non-US/China batteries, China trade-in)
                if oem == "BYD" and region == "US":
                    macro_shock -= 0.65 if year >= 2024 else 0.0
                elif oem == "BYD" and region == "EU":
                    macro_shock -= 0.18 if year >= 2024 and month >= 10 else 0.0
                elif oem == "Tesla" and region == "US":
                    macro_shock += 0.08 if year >= 2024 else 0.0
                elif oem in ["BYD", "Tesla"] and region == "CN" and cn_trade_in == 1.0:
                    macro_shock += 0.12

                final_sales = int(max(10, base_monthly_sales * (1.0 + macro_shock + np.random.normal(0, 0.03))))

                # OEM Product Attributes
                if oem == "Tesla":
                    lfp_mix = 0.38 + (0.32 if region == "CN" else 0.12)
                    msrp = 48500 - (t * 110) + np.random.normal(0, 300)
                    lineup = 4 + (1 if t > 45 else 0)
                elif oem == "BYD":
                    lfp_mix = 0.92
                    msrp = 21500 + (t * 45) + np.random.normal(0, 200)
                    lineup = 8 + int(t / 8)
                elif oem == "Volkswagen Group":
                    lfp_mix = 0.15 + t * 0.003
                    msrp = 44500 - (t * 70) + np.random.normal(0, 300)
                    lineup = 3 + int(t / 12)
                elif oem == "Hyundai-Kia Group":
                    lfp_mix = 0.20 + t * 0.004
                    msrp = 41500 - (t * 80) + np.random.normal(0, 300)
                    lineup = 3 + int(t / 10)
                elif oem == "BMW Group":
                    lfp_mix = 0.10
                    msrp = 58500 - (t * 50) + np.random.normal(0, 400)
                    lineup = 2 + int(t / 14)
                elif oem == "Mercedes-Benz Group":
                    lfp_mix = 0.08
                    msrp = 66000 - (t * 40) + np.random.normal(0, 500)
                    lineup = 2 + int(t / 15)
                else: # Toyota
                    lfp_mix = 0.05
                    msrp = 39500
                    lineup = 1 + (1 if t > 40 else 0)

                tariff_rate = base_tariff
                if oem == "BYD" and region == "US":
                    tariff_rate = 27.5 if year < 2024 else 102.5
                elif oem == "BYD" and region == "EU":
                    tariff_rate = 10.0 if year < 2024 else (20.0 if t < 56 else 37.0)

                records.append({
                    "year_month": ym_str,
                    "date": dt,
                    "region": region,
                    "company": oem,
                    "bev_sales": final_sales,
                    "battery_pack_price_usd_kwh": round(battery_pack_price, 2),
                    "lithium_carbonate_price_usd_ton": round(lithium_price, 2),
                    "nickel_price_usd_ton": round(nickel_price, 2),
                    "cobalt_price_usd_ton": round(cobalt_price, 2),
                    "wti_oil_price_usd": round(wti_oil, 2),
                    "residential_electricity_price_usd_kwh": round(electricity_price, 4),
                    "interest_rate_pct": round(interest_rate, 2),
                    "cpi_index": round(cpi_index, 2),
                    "gdp_growth_index": round(gdp_growth, 2),
                    "used_ev_depreciation_rate_pct": round(used_depreciation, 2),
                    "semiconductor_lead_time_weeks": round(semi_lead_time, 1),
                    "public_chargers_per_million_capita": round(public_chargers, 1),
                    "fast_chargers_ratio": round(fast_chargers_ratio, 3),
                    "applied_tariff_rate_pct": round(tariff_rate, 1),
                    "subsidy_intensity_ratio": round(base_subsidy_ratio, 3),
                    "us_ira_feoc_dummy": int(ira_feoc),
                    "eu_co2_target_tightening_dummy": int(eu_co2_tightening),
                    "cn_trade_in_scheme_dummy": int(cn_trade_in),
                    "lfp_battery_mix_pct": round(lfp_mix, 2),
                    "average_msrp_usd": round(msrp, 2),
                    "bev_lineup_count": lineup
                })
                
    df = pd.DataFrame(records)
    if output_path:
        df.to_csv(output_path, index=False)
    return df

                
    df = pd.DataFrame(records)
    if output_path:
        df.to_csv(output_path, index=False)
    return df

if __name__ == "__main__":
    df = generate_panel_data("data/processed/bev_panel_dataset.csv")
    print(f"Generated panel dataset with shape {df.shape}")
