"""
feature_engineering.py - Feature Engineering, Lags, VIF Collinearity Filtering
Calculates 1, 3, and 6-month lagged variables, VIF, and lag cross-correlations.
"""

import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

NUMERIC_DRIVERS = [
    "battery_pack_price_usd_kwh",
    "lithium_carbonate_price_usd_ton",
    "wti_oil_price_usd",
    "residential_electricity_price_usd_kwh",
    "interest_rate_pct",
    "used_ev_depreciation_rate_pct",
    "semiconductor_lead_time_weeks",
    "public_chargers_per_million_capita",
    "applied_tariff_rate_pct",
    "subsidy_intensity_ratio"
]

def add_lag_features(df: pd.DataFrame, lags=[1, 3, 6]) -> pd.DataFrame:
    """Generates panel-aware lagged variables per region and company."""
    df_engineered = df.copy()
    
    for col in NUMERIC_DRIVERS:
        for lag in lags:
            df_engineered[f"{col}_lag_{lag}"] = (
                df_engineered.groupby(["region", "company"])[col].shift(lag)
            )
            
    return df_engineered

def compute_vif(df: pd.DataFrame, features: list = None) -> pd.DataFrame:
    """Computes Variance Inflation Factor (VIF) to detect multicollinearity."""
    if features is None:
        features = NUMERIC_DRIVERS
        
    X = df[features].dropna()
    vif_data = pd.DataFrame()
    vif_data["feature"] = features
    vif_data["VIF"] = [
        variance_inflation_factor(X.values, i) for i in range(X.shape[1])
    ]
    return vif_data.sort_values(by="VIF", ascending=False)

def compute_lag_cross_correlation(df: pd.DataFrame, target: str = "bev_sales") -> pd.DataFrame:
    """Computes lag cross-correlations (lag 0, 1, 3, 6) against target variable."""
    results = []
    
    for col in NUMERIC_DRIVERS:
        row = {"driver": col, "lag_0": df[col].corr(df[target])}
        for lag in [1, 3, 6]:
            lag_col = f"{col}_lag_{lag}"
            if lag_col in df.columns:
                row[f"lag_{lag}"] = df[lag_col].corr(df[target])
            else:
                row[f"lag_{lag}"] = np.nan
        results.append(row)
        
    return pd.DataFrame(results)

if __name__ == "__main__":
    from src.data_loader import load_panel_dataset
    df = load_panel_dataset()
    df_lags = add_lag_features(df)
    vif = compute_vif(df_lags)
    print("VIF Table:")
    print(vif)
