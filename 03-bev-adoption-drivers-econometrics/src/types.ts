export interface PanelRecord {
  year_month: string;
  date: string;
  region: 'US' | 'EU' | 'CN';
  company: string;
  bev_sales: number;
  battery_pack_price_usd_kwh: number;
  lithium_carbonate_price_usd_ton: number;
  nickel_price_usd_ton: number;
  cobalt_price_usd_ton: number;
  wti_oil_price_usd: number;
  residential_electricity_price_usd_kwh: number;
  interest_rate_pct: number;
  cpi_index: number;
  gdp_growth_index: number;
  used_ev_depreciation_rate_pct: number;
  semiconductor_lead_time_weeks: number;
  public_chargers_per_million_capita: number;
  fast_chargers_ratio: number;
  applied_tariff_rate_pct: number;
  subsidy_intensity_ratio: number;
  us_ira_feoc_dummy: number;
  eu_co2_target_tightening_dummy: number;
  cn_trade_in_scheme_dummy: number;
  lfp_battery_mix_pct: number;
  average_msrp_usd: number;
  bev_lineup_count: number;
  // Lagged fields
  battery_pack_price_usd_kwh_lag_1?: number;
  battery_pack_price_usd_kwh_lag_3?: number;
  battery_pack_price_usd_kwh_lag_6?: number;
  public_chargers_per_million_capita_lag_1?: number;
  public_chargers_per_million_capita_lag_3?: number;
  public_chargers_per_million_capita_lag_6?: number;
}

export interface LagCorrelation {
  driver: string;
  label: string;
  lag0: number;
  lag1: number;
  lag3: number;
  lag6: number;
}

export interface OLSResult {
  variable: string;
  label: string;
  coefficient: number;
  stdError: number;
  tStat: number;
  pValue: number;
  ciLower: number;
  ciUpper: number;
  description: string;
}

export interface VARImpulsePoint {
  month: number;
  batteryPrice: number;
  appliedTariff: number;
  usedDepreciation: number;
  publicChargers: number;
  interestRate: number;
}

export interface ShapFeatureImportance {
  feature: string;
  label: string;
  importance: number;
  category: 'Battery' | 'Macro' | 'Policy' | 'Infrastructure' | 'OEM Strategy';
}

export interface PythonCodeFile {
  path: string;
  name: string;
  content: string;
}
