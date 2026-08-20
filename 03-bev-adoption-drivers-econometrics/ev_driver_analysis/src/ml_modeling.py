"""
ml_modeling.py - XGBoost Regressor & SHAP Feature Interpretation
Train/Test split on TimeSeries (Train: 2020-2024, Test: 2025). Computes test metrics & SHAP values.
"""

import pandas as pd
import numpy as np
import xgboost as xgb
import shap
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

FEATURE_COLS = [
    "battery_pack_price_usd_kwh",
    "lithium_carbonate_price_usd_ton",
    "nickel_price_usd_ton",
    "cobalt_price_usd_ton",
    "wti_oil_price_usd",
    "residential_electricity_price_usd_kwh",
    "interest_rate_pct",
    "cpi_index",
    "gdp_growth_index",
    "used_ev_depreciation_rate_pct",
    "semiconductor_lead_time_weeks",
    "public_chargers_per_million_capita",
    "fast_chargers_ratio",
    "applied_tariff_rate_pct",
    "subsidy_intensity_ratio",
    "us_ira_feoc_dummy",
    "eu_co2_target_tightening_dummy",
    "cn_trade_in_scheme_dummy",
    "lfp_battery_mix_pct",
    "average_msrp_usd",
    "bev_lineup_count"
]

def train_xgboost_model(df: pd.DataFrame):
    """
    Trains XGBoost model on time-series split (Train: <=2024, Test: 2025).
    Returns model, performance metrics, and SHAP explainer objects.
    """
    df_encoded = pd.get_dummies(df, columns=["region", "company"], drop_first=False)
    
    feature_matrix = [c for c in df_encoded.columns if c in FEATURE_COLS or c.startswith("region_") or c.startswith("company_")]
    
    train_mask = df_encoded["date"] < "2025-01-01"
    test_mask = df_encoded["date"] >= "2025-01-01"
    
    X_train = df_encoded.loc[train_mask, feature_matrix]
    y_train = np.log(df_encoded.loc[train_mask, "bev_sales"])
    
    X_test = df_encoded.loc[test_mask, feature_matrix]
    y_test = np.log(df_encoded.loc[test_mask, "bev_sales"])
    
    model = xgb.XGBRegressor(
        n_estimators=180,
        learning_rate=0.04,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    y_pred_log = model.predict(X_test)
    y_pred = np.exp(y_pred_log)
    y_test_exp = np.exp(y_test)
    
    metrics = {
        "r2": r2_score(y_test_exp, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_test_exp, y_pred)),
        "mae": mean_absolute_error(y_test_exp, y_pred),
        "train_samples": len(X_train),
        "test_samples": len(X_test)
    }
    
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_test)
    
    importance_df = pd.DataFrame({
        "feature": feature_matrix,
        "importance": np.abs(shap_values.values).mean(axis=0)
    }).sort_values(by="importance", ascending=False)
    
    test_df = df.loc[test_mask].copy()
    test_df["predicted_bev_sales"] = y_pred.astype(int)
    
    return model, metrics, importance_df, shap_values, X_test, test_df

if __name__ == "__main__":
    from src.data_loader import load_panel_dataset
    df = load_panel_dataset()
    model, metrics, importance_df, shap_values, X_test, test_df = train_xgboost_model(df)
    print("XGBoost Metrics:", metrics)
    print("Top 5 Features:", importance_df.head())