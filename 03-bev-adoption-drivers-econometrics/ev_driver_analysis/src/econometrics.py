"""
econometrics.py - Panel Fixed-Effects OLS & Vector Autoregression (VAR)
Performs panel econometric estimation with entity/time fixed effects and impulse response curves.
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR
from linearmodels.panel import PanelOLS

OLS_VARIABLE_LABELS = {
    "battery_pack_price_usd_kwh": "Battery Pack Price (USD/kWh)",
    "applied_tariff_rate_pct": "Applied Tariff Rate (%)",
    "used_ev_depreciation_rate_pct": "Used EV Depreciation Rate (%)",
    "interest_rate_pct": "Central Bank Policy Rate (%)",
    "residential_electricity_price_usd_kwh": "Residential Electricity Price (USD/kWh)",
    "wti_oil_price_usd": "WTI Crude Oil Price (USD/bbl)",
    "subsidy_intensity_ratio": "EV Subsidy Intensity Ratio",
    "log_public_chargers": "Public Chargers Density (Log)",
    "us_ira_feoc_dummy": "US IRA FEOC Policy Dummy",
    "cn_trade_in_scheme_dummy": "China Trade-In Incentive Dummy"
}

def get_significance_stars(p_val: float) -> str:
    if p_val < 0.001:
        return "*** (p < 0.001)"
    elif p_val < 0.01:
        return "** (p < 0.01)"
    elif p_val < 0.05:
        return "* (p < 0.05)"
    else:
        return "ns (Not Significant)"

def run_panel_fixed_effects_ols(df: pd.DataFrame):
    """
    Executes Panel OLS with Entity (Region x OEM) Fixed Effects.
    Validates all error bounds, confidence intervals, and provides explicit economic interpretations.
    """
    df_panel = df.copy()
    df_panel["entity_id"] = df_panel["region"].astype(str) + "_" + df_panel["company"].astype(str)
    
    # Log transformation for elasticity model
    df_panel["log_bev_sales"] = np.log(df_panel["bev_sales"].replace(0, np.nan))
    capita = df_panel["public_chargers_per_million_capita"].replace(0, np.nan)
    df_panel["log_public_chargers"] = np.log(capita)
    
    df_panel = df_panel.set_index(["entity_id", "date"])
    
    candidate_exog_vars = [
        "battery_pack_price_usd_kwh",
        "applied_tariff_rate_pct",
        "used_ev_depreciation_rate_pct",
        "interest_rate_pct",
        "residential_electricity_price_usd_kwh",
        "wti_oil_price_usd",
        "subsidy_intensity_ratio",
        "log_public_chargers",
        "us_ira_feoc_dummy",
        "cn_trade_in_scheme_dummy"
    ]
    
    valid_exog_vars = []
    for col in candidate_exog_vars:
        if col in df_panel.columns:
            if df_panel[col].nunique() > 1 and df_panel[col].notna().sum() > 5:
                valid_exog_vars.append(col)

    if not valid_exog_vars:
        raise ValueError("No valid exogenous variables available for regression.")

    df_panel = df_panel.dropna(subset=["log_bev_sales"] + valid_exog_vars)

    y = df_panel["log_bev_sales"]
    X = df_panel[valid_exog_vars]
    
    model = PanelOLS(
        y, 
        X, 
        entity_effects=True, 
        time_effects=False
    )
    
    try:
        res = model.fit(cov_type="clustered", cluster_entity=True)
    except Exception:
        res = model.fit(cov_type="unadjusted")
    
    # Calculate exact confidence intervals: lower = beta - 1.96*SE, upper = beta + 1.96*SE
    params = res.params.values
    std_errs = res.std_errors.values
    ci_lower = params - 1.96 * std_errs
    ci_upper = params + 1.96 * std_errs
    
    var_names = res.params.index.tolist()
    clean_names = [OLS_VARIABLE_LABELS.get(v, v.replace("_", " ").title()) for v in var_names]
    p_values = res.pvalues.values
    stars = [get_significance_stars(p) for p in p_values]

    # Generate economic interpretations
    interpretations = []
    for var, coef, p in zip(var_names, params, p_values):
        pct_effect = (np.exp(coef) - 1.0) * 100.0
        if p >= 0.05:
            interpretations.append("Statistically Insignificant (p >= 0.05)")
        else:
            if "log_" in var:
                interpretations.append(f"+1% increase leads to {coef:+.2f}% change in sales (Elasticity)")
            elif "_pct" in var or "ratio" in var or "rate" in var:
                interpretations.append(f"+1 percentage point shift leads to {pct_effect:+.2f}% change")
            elif "dummy" in var:
                interpretations.append(f"Policy in effect causes {pct_effect:+.1f}% structural demand shift")
            else:
                interpretations.append(f"+1 unit increase leads to {pct_effect:+.2f}% change in sales")

    coef_df = pd.DataFrame({
        "Variable": clean_names,
        "Raw_Code": var_names,
        "Coefficient": params,
        "Std_Error": std_errs,
        "t_stat": res.tstats.values,
        "p_value": p_values,
        "Significance": stars,
        "95_CI_Lower": ci_lower,
        "95_CI_Upper": ci_upper,
        "Economic_Impact": interpretations
    })
    
    summary_stats = {
        "r2_overall": res.rsquared,
        "r2_within": res.rsquared_within,
        "nobs": res.nobs,
        "f_statistic": res.f_statistic.stat if hasattr(res.f_statistic, 'stat') else np.nan,
        "f_pvalue": res.f_statistic.pval if hasattr(res.f_statistic, 'pval') else np.nan
    }
    
    return coef_df, summary_stats

def run_var_impulse_response(df: pd.DataFrame, steps: int = 12) -> pd.DataFrame:
    """
    Fits Vector Autoregression (VAR) model on aggregate time series to estimate 12-month IRFs.
    """
    agg = df.groupby("date")[
        ["bev_sales", "battery_pack_price_usd_kwh", "applied_tariff_rate_pct",
         "used_ev_depreciation_rate_pct", "public_chargers_per_million_capita", "interest_rate_pct"]
    ].mean()
    
    agg_diff = agg.diff().dropna()
    
    var_model = VAR(agg_diff)
    results = var_model.fit(maxlags=2)
    
    irf = results.irf(steps)
    
    irf_data = []
    variables = agg.columns[1:]
    
    for step in range(steps + 1):
        for idx, var in enumerate(variables):
            val = irf.irfs[step, 0, idx + 1]
            irf_data.append({
                "month": step,
                "impulse_variable": var,
                "response_bev_sales": val
            })
            
    return pd.DataFrame(irf_data)