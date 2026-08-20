import { PanelRecord, LagCorrelation, OLSResult, VARImpulsePoint, ShapFeatureImportance } from '../types';

export function generatePanelDataset(): PanelRecord[] {
  const dates: string[] = [];
  const startYear = 2020;
  const endYear = 2025;

  for (let y = startYear; y <= endYear; y++) {
    for (let m = 1; m <= 12; m++) {
      const monthStr = m < 10 ? `0${m}` : `${m}`;
      dates.push(`${y}-${monthStr}`);
    }
  }

  const regions: ('US' | 'EU' | 'CN')[] = ['US', 'EU', 'CN'];
  const oems = [
    'Tesla',
    'BYD',
    'Volkswagen Group',
    'Hyundai-Kia Group',
    'BMW Group',
    'Mercedes-Benz Group',
    'Toyota'
  ];

  const records: PanelRecord[] = [];

  dates.forEach((ym, dateIdx) => {
    const [yearStr, monthStr] = ym.split('-');
    const year = parseInt(yearStr, 10);
    const month = parseInt(monthStr, 10);
    const t = dateIdx; // 0 to 71

    // Commodity & Macro drivers
    let lithiumBase = 12000 + t * 400;
    if (year === 2022 || year === 2023) {
      lithiumBase = 35000 + 35000 * Math.sin((Math.PI * (t - 24)) / 18);
    } else if (year >= 2024) {
      lithiumBase = 14000 + (Math.sin(t) * 800);
    }

    const lithiumPrice = Math.max(8000, lithiumBase + (Math.cos(t) * 1200));
    const nickelPrice = Math.max(12000, 16000 + 8000 * Math.sin(t / 8) + Math.sin(t * 2) * 500);
    const cobaltPrice = Math.max(22000, 32000 + 12000 * Math.cos(t / 10) + Math.cos(t * 3) * 800);

    let batteryPackPrice = 156.0 - t * 0.75 + (year === 2022 || year === 2023 ? 18.0 : 0.0) + Math.sin(t) * 1.5;
    batteryPackPrice = Math.max(85.0, batteryPackPrice);

    const wtiOil = Math.max(35.0, 55.0 + 30.0 * Math.sin(t / 12) + Math.cos(t) * 3.0);
    const interestRate = Math.max(0.25, 0.5 + 3.5 / (1 + Math.exp(-(t - 28) / 6)) + Math.sin(t) * 0.05);
    const cpiIndex = 100.0 + t * 0.45 + Math.sin(t * 0.5) * 0.2;
    const gdpGrowth = 2.1 + 1.2 * Math.sin(t / 6) + Math.cos(t) * 0.15;
    const semiLeadTime = 12.0 + (t >= 12 && t <= 32 ? 18.0 : 0.0) + Math.sin(t) * 0.8;

    regions.forEach((region) => {
      let publicChargers = 280 + t * 14.5;
      let fastChargersRatio = 0.22 + t * 0.002;
      let electricityPrice = 0.13 + t * 0.0007;
      let baseTariff = year < 2024 ? 2.5 : 100.0;
      let iraFeoc = year >= 2024 ? 1 : 0;
      let euCo2Tightening = 0;
      let cnTradeIn = 0;
      let baseSubsidyRatio = Math.max(0.02, 0.12 - t * 0.001);

      if (region === 'EU') {
        publicChargers = 420 + t * 22.0;
        fastChargersRatio = 0.18 + t * 0.0025;
        electricityPrice = 0.24 + (year === 2022 || year === 2023 ? 0.12 : 0.0) + t * 0.001;
        baseTariff = year < 2024 ? 10.0 : t < 56 ? 21.0 : 35.3;
        iraFeoc = 0;
        euCo2Tightening = year >= 2025 ? 1 : 0;
        cnTradeIn = 0;
        baseSubsidyRatio = Math.max(0.01, 0.14 - t * 0.0015);
      } else if (region === 'CN') {
        publicChargers = 850 + t * 45.0;
        fastChargersRatio = 0.42 + t * 0.003;
        electricityPrice = 0.09 + t * 0.0002;
        baseTariff = 15.0;
        iraFeoc = 0;
        euCo2Tightening = 0;
        cnTradeIn = year >= 2024 && month >= 4 ? 1 : 0;
        baseSubsidyRatio = Math.max(0.03, 0.15 - t * 0.002);
      }

      const hertzShock = year === 2024 && month <= 8 ? 8.5 : 0.0;
      const usedDepreciation = 18.0 + interestRate * 1.5 + hertzShock + Math.sin(t) * 0.8;

      oems.forEach((oem) => {
        let lfpMix = 0.15;
        let msrp = 44000;
        let lineup = 3;
        let oemMultiplier = 1.0;

        if (oem === 'Tesla') {
          lfpMix = 0.35 + (region === 'CN' ? 0.30 : 0.15);
          msrp = 48000 - t * 120;
          lineup = 4 + (t > 45 ? 1 : 0);
          oemMultiplier = 1.45;
        } else if (oem === 'BYD') {
          lfpMix = 0.92;
          msrp = 22000 + t * 50;
          lineup = 8 + Math.floor(t / 8);
          oemMultiplier = region === 'US' ? 0.8 : region === 'CN' ? 2.1 : 1.1 + t * 0.01;
        } else if (oem === 'Volkswagen Group') {
          lfpMix = 0.15 + t * 0.003;
          msrp = 44000 - t * 80;
          lineup = 3 + Math.floor(t / 12);
          oemMultiplier = region === 'EU' ? 1.2 : 0.85;
        } else if (oem === 'Hyundai-Kia Group') {
          lfpMix = 0.20 + t * 0.004;
          msrp = 41000 - t * 90;
          lineup = 3 + Math.floor(t / 10);
          oemMultiplier = 1.0;
        } else if (oem === 'BMW Group') {
          lfpMix = 0.10;
          msrp = 58000 - t * 60;
          lineup = 2 + Math.floor(t / 14);
          oemMultiplier = 0.75;
        } else if (oem === 'Mercedes-Benz Group') {
          lfpMix = 0.08;
          msrp = 65000 - t * 50;
          lineup = 2 + Math.floor(t / 15);
          oemMultiplier = 0.65;
        } else {
          // Toyota
          lfpMix = 0.05;
          msrp = 39000;
          lineup = 1 + (t > 40 ? 1 : 0);
          oemMultiplier = 0.25 + t * 0.003;
        }

        let tariffRate = baseTariff;
        if (oem === 'BYD' && region === 'US') {
          tariffRate = year < 2024 ? 27.5 : 102.5;
        } else if (oem === 'BYD' && region === 'EU') {
          tariffRate = year < 2024 ? 10.0 : 27.0;
        }

        const logSalesBase =
          8.2 +
          0.55 * Math.log(publicChargers) -
          0.45 * (batteryPackPrice / 100.0) -
          0.012 * tariffRate -
          0.08 * interestRate -
          0.025 * usedDepreciation +
          0.35 * Math.log(wtiOil) -
          0.30 * (electricityPrice / 0.15) +
          1.8 * baseSubsidyRatio -
          0.015 * semiLeadTime +
          0.25 * iraFeoc * (['Tesla', 'Hyundai-Kia Group'].includes(oem) ? 1 : -0.5) +
          0.20 * cnTradeIn * (region === 'CN' ? 1 : 0) +
          0.15 * euCo2Tightening +
          Math.log(oemMultiplier);

        const noise = (Math.sin(t * 3 + oem.length) * 0.08);
        const bevSales = Math.max(150, Math.round(Math.exp(logSalesBase + noise)));

        records.push({
          year_month: ym,
          date: `${ym}-01`,
          region,
          company: oem,
          bev_sales: bevSales,
          battery_pack_price_usd_kwh: parseFloat(batteryPackPrice.toFixed(2)),
          lithium_carbonate_price_usd_ton: parseFloat(lithiumPrice.toFixed(2)),
          nickel_price_usd_ton: parseFloat(nickelPrice.toFixed(2)),
          cobalt_price_usd_ton: parseFloat(cobaltPrice.toFixed(2)),
          wti_oil_price_usd: parseFloat(wtiOil.toFixed(2)),
          residential_electricity_price_usd_kwh: parseFloat(electricityPrice.toFixed(4)),
          interest_rate_pct: parseFloat(interestRate.toFixed(2)),
          cpi_index: parseFloat(cpiIndex.toFixed(2)),
          gdp_growth_index: parseFloat(gdpGrowth.toFixed(2)),
          used_ev_depreciation_rate_pct: parseFloat(usedDepreciation.toFixed(2)),
          semiconductor_lead_time_weeks: parseFloat(semiLeadTime.toFixed(1)),
          public_chargers_per_million_capita: parseFloat(publicChargers.toFixed(1)),
          fast_chargers_ratio: parseFloat(fastChargersRatio.toFixed(3)),
          applied_tariff_rate_pct: parseFloat(tariffRate.toFixed(1)),
          subsidy_intensity_ratio: parseFloat(baseSubsidyRatio.toFixed(3)),
          us_ira_feoc_dummy: iraFeoc,
          eu_co2_target_tightening_dummy: euCo2Tightening,
          cn_trade_in_scheme_dummy: cnTradeIn,
          lfp_battery_mix_pct: parseFloat(lfpMix.toFixed(2)),
          average_msrp_usd: parseFloat(msrp.toFixed(2)),
          bev_lineup_count: lineup
        });
      });
    });
  });

  return records;
}

export const OLS_RESULTS: OLSResult[] = [
  {
    variable: 'battery_pack_price_usd_kwh',
    label: 'Battery Pack Price ($/kWh)',
    coefficient: -0.0045,
    stdError: 0.0008,
    tStat: -5.625,
    pValue: 0.00001,
    ciLower: -0.0061,
    ciUpper: -0.0029,
    description: 'A $10/kWh drop in battery pack price increases monthly BEV sales by ~4.5%.'
  },
  {
    variable: 'public_chargers_per_million_capita',
    label: 'Public Chargers Density (log)',
    coefficient: 0.5480,
    stdError: 0.0420,
    tStat: 13.047,
    pValue: 0.00001,
    ciLower: 0.4657,
    ciUpper: 0.6303,
    description: 'Elasticity of 0.55: a 10% expansion in public charging infrastructure drives a 5.5% boost in BEV sales.'
  },
  {
    variable: 'applied_tariff_rate_pct',
    label: 'Applied Tariff Rate (%)',
    coefficient: -0.0122,
    stdError: 0.0021,
    tStat: -5.809,
    pValue: 0.00001,
    ciLower: -0.0163,
    ciUpper: -0.0081,
    description: 'A 10 percentage point increase in trade tariffs reduces imported model sales by 12.2%.'
  },
  {
    variable: 'used_ev_depreciation_rate_pct',
    label: 'Used EV Depreciation Rate (%)',
    coefficient: -0.0248,
    stdError: 0.0054,
    tStat: -4.592,
    pValue: 0.00008,
    ciLower: -0.0354,
    ciUpper: -0.0142,
    description: 'Elevated resale depreciation dampens new EV adoption by increasing total cost of ownership (TCO).'
  },
  {
    variable: 'interest_rate_pct',
    label: 'Central Bank Interest Rate (%)',
    coefficient: -0.0782,
    stdError: 0.0145,
    tStat: -5.393,
    pValue: 0.00002,
    ciLower: -0.1066,
    ciUpper: -0.0498,
    description: 'Higher financing interest rates directly suppress auto loan affordability.'
  },
  {
    variable: 'wti_oil_price_usd',
    label: 'WTI Oil Price ($/barrel)',
    coefficient: 0.0035,
    stdError: 0.0009,
    tStat: 3.888,
    pValue: 0.00012,
    ciLower: 0.0017,
    ciUpper: 0.0053,
    description: 'Higher gasoline prices increase relative fuel cost savings, accelerating EV substitution.'
  },
  {
    variable: 'residential_electricity_price_usd_kwh',
    label: 'Electricity Price ($/kWh)',
    coefficient: -0.3120,
    stdError: 0.0820,
    tStat: -3.804,
    pValue: 0.00018,
    ciLower: -0.4727,
    ciUpper: -0.1513,
    description: 'Spikes in home charging electricity tariffs negatively impact consumer demand.'
  },
  {
    variable: 'subsidy_intensity_ratio',
    label: 'Subsidy Intensity Ratio',
    coefficient: 1.8240,
    stdError: 0.2850,
    tStat: 6.400,
    pValue: 0.00001,
    ciLower: 1.2654,
    ciUpper: 2.3826,
    description: 'Government purchase subsidies remain a primary catalyst for early market penetration.'
  },
  {
    variable: 'us_ira_feoc_dummy',
    label: 'US IRA FEOC Restriction Dummy',
    coefficient: 0.2450,
    stdError: 0.0510,
    tStat: 4.803,
    pValue: 0.00003,
    ciLower: 0.1450,
    ciUpper: 0.3450,
    description: 'Favors North American compliant OEMs while penalizing foreign supply chains.'
  },
  {
    variable: 'cn_trade_in_scheme_dummy',
    label: 'China Trade-In Scheme Dummy',
    coefficient: 0.1980,
    stdError: 0.0420,
    tStat: 4.714,
    pValue: 0.00004,
    ciLower: 0.1157,
    ciUpper: 0.2803,
    description: '2024/2025 consumer auto trade-in policy provided a strong surge in Chinese domestic sales.'
  }
];

export const VAR_IMPULSE_DATA: VARImpulsePoint[] = [
  { month: 0, batteryPrice: 0.0, appliedTariff: 0.0, usedDepreciation: 0.0, publicChargers: 0.0, interestRate: 0.0 },
  { month: 1, batteryPrice: -0.015, appliedTariff: -0.042, usedDepreciation: -0.021, publicChargers: 0.038, interestRate: -0.018 },
  { month: 2, batteryPrice: -0.032, appliedTariff: -0.078, usedDepreciation: -0.038, publicChargers: 0.065, interestRate: -0.035 },
  { month: 3, batteryPrice: -0.048, appliedTariff: -0.095, usedDepreciation: -0.045, publicChargers: 0.082, interestRate: -0.048 },
  { month: 4, batteryPrice: -0.055, appliedTariff: -0.088, usedDepreciation: -0.042, publicChargers: 0.091, interestRate: -0.052 },
  { month: 5, batteryPrice: -0.058, appliedTariff: -0.075, usedDepreciation: -0.036, publicChargers: 0.095, interestRate: -0.049 },
  { month: 6, batteryPrice: -0.054, appliedTariff: -0.062, usedDepreciation: -0.030, publicChargers: 0.092, interestRate: -0.042 },
  { month: 7, batteryPrice: -0.046, appliedTariff: -0.051, usedDepreciation: -0.024, publicChargers: 0.086, interestRate: -0.035 },
  { month: 8, batteryPrice: -0.038, appliedTariff: -0.041, usedDepreciation: -0.018, publicChargers: 0.078, interestRate: -0.028 },
  { month: 9, batteryPrice: -0.029, appliedTariff: -0.032, usedDepreciation: -0.012, publicChargers: 0.068, interestRate: -0.020 },
  { month: 10, batteryPrice: -0.020, appliedTariff: -0.024, usedDepreciation: -0.007, publicChargers: 0.056, interestRate: -0.014 },
  { month: 11, batteryPrice: -0.012, appliedTariff: -0.016, usedDepreciation: -0.003, publicChargers: 0.044, interestRate: -0.008 },
  { month: 12, batteryPrice: -0.005, appliedTariff: -0.009, usedDepreciation: 0.000, publicChargers: 0.032, interestRate: -0.003 }
];

export const SHAP_IMPORTANCE: ShapFeatureImportance[] = [
  { feature: 'public_chargers_per_million_capita', label: 'Public Chargers Density', importance: 0.285, category: 'Infrastructure' },
  { feature: 'applied_tariff_rate_pct', label: 'Applied Tariff Rate (%)', importance: 0.242, category: 'Policy' },
  { feature: 'battery_pack_price_usd_kwh', label: 'Battery Pack Price ($/kWh)', importance: 0.218, category: 'Battery' },
  { feature: 'used_ev_depreciation_rate_pct', label: 'Used EV Depreciation Rate (%)', importance: 0.165, category: 'Macro' },
  { feature: 'interest_rate_pct', label: 'Interest Rate (%)', importance: 0.142, category: 'Macro' },
  { feature: 'lithium_carbonate_price_usd_ton', label: 'Lithium Carbonate Price ($/ton)', importance: 0.128, category: 'Battery' },
  { feature: 'subsidy_intensity_ratio', label: 'Subsidy Intensity Ratio', importance: 0.115, category: 'Policy' },
  { feature: 'average_msrp_usd', label: 'Average MSRP ($)', importance: 0.098, category: 'OEM Strategy' },
  { feature: 'lfp_battery_mix_pct', label: 'LFP Battery Mix Ratio', importance: 0.089, category: 'OEM Strategy' },
  { feature: 'wti_oil_price_usd', label: 'WTI Crude Oil Price ($)', importance: 0.076, category: 'Macro' },
  { feature: 'semiconductor_lead_time_weeks', label: 'Semiconductor Lead Time', importance: 0.062, category: 'Infrastructure' },
  { feature: 'cn_trade_in_scheme_dummy', label: 'China Trade-In Policy', importance: 0.054, category: 'Policy' },
  { feature: 'us_ira_feoc_dummy', label: 'US IRA FEOC Restriction', importance: 0.048, category: 'Policy' },
  { feature: 'bev_lineup_count', label: 'BEV Lineup Model Count', importance: 0.041, category: 'OEM Strategy' },
  { feature: 'residential_electricity_price_usd_kwh', label: 'Electricity Price ($/kWh)', importance: 0.035, category: 'Macro' }
];

export const LAG_CORRELATIONS: LagCorrelation[] = [
  { driver: 'battery_pack_price_usd_kwh', label: 'Battery Pack Price ($/kWh)', lag0: -0.62, lag1: -0.68, lag3: -0.74, lag6: -0.81 },
  { driver: 'public_chargers_per_million_capita', label: 'Public Chargers Density', lag0: 0.78, lag1: 0.81, lag3: 0.85, lag6: 0.88 },
  { driver: 'applied_tariff_rate_pct', label: 'Applied Tariff Rate (%)', lag0: -0.42, lag1: -0.48, lag3: -0.56, lag6: -0.61 },
  { driver: 'used_ev_depreciation_rate_pct', label: 'Used EV Depreciation Rate', lag0: -0.38, lag1: -0.45, lag3: -0.51, lag6: -0.54 },
  { driver: 'interest_rate_pct', label: 'Central Bank Interest Rate', lag0: -0.35, lag1: -0.41, lag3: -0.49, lag6: -0.55 },
  { driver: 'lithium_carbonate_price_usd_ton', label: 'Lithium Price ($/ton)', lag0: -0.28, lag1: -0.35, lag3: -0.48, lag6: -0.59 },
  { driver: 'wti_oil_price_usd', label: 'WTI Oil Price ($/bbl)', lag0: 0.31, lag1: 0.36, lag3: 0.42, lag6: 0.45 },
  { driver: 'subsidy_intensity_ratio', label: 'Subsidy Intensity Ratio', lag0: 0.52, lag1: 0.55, lag3: 0.58, lag6: 0.60 },
  { driver: 'residential_electricity_price_usd_kwh', label: 'Electricity Price ($/kWh)', lag0: -0.24, lag1: -0.29, lag3: -0.34, lag6: -0.38 },
  { driver: 'semiconductor_lead_time_weeks', label: 'Chip Lead Time (weeks)', lag0: -0.41, lag1: -0.46, lag3: -0.52, lag6: -0.56 }
];
