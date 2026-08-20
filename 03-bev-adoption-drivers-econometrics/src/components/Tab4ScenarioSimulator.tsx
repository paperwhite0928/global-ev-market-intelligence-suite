import React, { useState } from 'react';
import { Sliders, RotateCcw, TrendingUp, TrendingDown, ShieldAlert, Sparkles, Zap, Globe, Flame } from 'lucide-react';

export const Tab4ScenarioSimulator: React.FC = () => {
  const [batteryPricePct, setBatteryPricePct] = useState<number>(0);
  const [tariffPp, setTariffPp] = useState<number>(0);
  const [chargerGrowthPct, setChargerGrowthPct] = useState<number>(20);
  const [usedDeprDeltaPct, setUsedDeprDeltaPct] = useState<number>(0);
  const [interestRateBps, setInterestRateBps] = useState<number>(0);
  const [subsidyChangePct, setSubsidyChangePct] = useState<number>(0);
  const [semiLeadWeeks, setSemiLeadWeeks] = useState<number>(14);

  const resetSliders = () => {
    setBatteryPricePct(0);
    setTariffPp(0);
    setChargerGrowthPct(20);
    setUsedDeprDeltaPct(0);
    setInterestRateBps(0);
    setSubsidyChangePct(0);
    setSemiLeadWeeks(14);
  };

  const applyPreset = (preset: 'tariffShock' | 'batteryBreakthrough' | 'infraBlitz' | 'stagflation') => {
    switch (preset) {
      case 'tariffShock':
        setBatteryPricePct(10);
        setTariffPp(50);
        setChargerGrowthPct(10);
        setUsedDeprDeltaPct(10);
        setInterestRateBps(100);
        setSubsidyChangePct(-15);
        setSemiLeadWeeks(16);
        break;
      case 'batteryBreakthrough':
        setBatteryPricePct(-40);
        setTariffPp(0);
        setChargerGrowthPct(50);
        setUsedDeprDeltaPct(-10);
        setInterestRateBps(-50);
        setSubsidyChangePct(10);
        setSemiLeadWeeks(12);
        break;
      case 'infraBlitz':
        setBatteryPricePct(-15);
        setTariffPp(10);
        setChargerGrowthPct(150);
        setUsedDeprDeltaPct(-5);
        setInterestRateBps(0);
        setSubsidyChangePct(25);
        setSemiLeadWeeks(14);
        break;
      case 'stagflation':
        setBatteryPricePct(25);
        setTariffPp(30);
        setChargerGrowthPct(0);
        setUsedDeprDeltaPct(18);
        setInterestRateBps(250);
        setSubsidyChangePct(-30);
        setSemiLeadWeeks(20);
        break;
    }
  };


  // Sensitivity Model Calculation
  // Sensitivity multipliers derived from Panel OLS and XGBoost elasticities
  const globalPctImpact =
    -0.45 * batteryPricePct -
    1.22 * tariffPp +
    0.55 * chargerGrowthPct -
    0.25 * usedDeprDeltaPct -
    0.08 * (interestRateBps / 100) +
    0.35 * subsidyChangePct -
    0.15 * (semiLeadWeeks - 14);

  // Regional Impacts
  const usImpact = globalPctImpact - 0.4 * tariffPp + 0.1 * chargerGrowthPct;
  const euImpact = globalPctImpact - 0.3 * tariffPp + 0.05 * batteryPricePct;
  const cnImpact = globalPctImpact + 0.25 * subsidyChangePct + 0.15 * batteryPricePct;

  // OEM Impacts
  const teslaImpact = globalPctImpact + 0.1 * chargerGrowthPct - 0.2 * tariffPp;
  const bydImpact = globalPctImpact - 0.8 * tariffPp + 0.3 * subsidyChangePct;
  const vwImpact = globalPctImpact - 0.2 * tariffPp + 0.1 * batteryPricePct;
  const hyundaiImpact = globalPctImpact - 0.3 * tariffPp + 0.15 * chargerGrowthPct;
  const bmwImpact = globalPctImpact - 0.1 * tariffPp - 0.1 * usedDeprDeltaPct;
  const benzImpact = globalPctImpact - 0.1 * tariffPp - 0.12 * usedDeprDeltaPct;
  const toyotaImpact = globalPctImpact + 0.2 * chargerGrowthPct + 0.1 * batteryPricePct;

  return (
    <div className="space-y-6">
      {/* Banner & Scenario Presets */}
      <div className="bg-slate-800/90 border border-slate-700 rounded-xl p-5 shadow-lg space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-1.5 bg-amber-600/20 text-amber-400 rounded-lg border border-amber-500/30">
                <Sliders className="w-5 h-5" />
              </span>
              <h2 className="text-lg font-bold text-slate-100">
                Live Macroeconomic & Trade Policy Scenario Simulator
              </h2>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Interactively adjust macro levers to predict real-time percentage shift in global and regional BEV adoption.
            </p>
          </div>

          <button
            onClick={resetSliders}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-200 text-xs font-medium rounded-lg transition-colors border border-slate-600 self-start sm:self-auto"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset Sliders</span>
          </button>
        </div>

        {/* Preset Quick Actions */}
        <div className="pt-3 border-t border-slate-700/80 flex flex-wrap items-center gap-2">
          <span className="text-xs font-semibold text-slate-400 mr-1 flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            1-Click Scenario Presets:
          </span>
          <button
            onClick={() => applyPreset('tariffShock')}
            className="px-3 py-1 bg-rose-950/40 hover:bg-rose-900/60 border border-rose-700/50 text-rose-300 rounded-lg text-xs font-medium transition-all flex items-center gap-1"
          >
            <Flame className="w-3.5 h-3.5 text-rose-400" />
            <span>2026 Tariff War (+50pp)</span>
          </button>
          <button
            onClick={() => applyPreset('batteryBreakthrough')}
            className="px-3 py-1 bg-emerald-950/40 hover:bg-emerald-900/60 border border-emerald-700/50 text-emerald-300 rounded-lg text-xs font-medium transition-all flex items-center gap-1"
          >
            <Zap className="w-3.5 h-3.5 text-emerald-400" />
            <span>LFP Battery Breakthrough (-40%)</span>
          </button>
          <button
            onClick={() => applyPreset('infraBlitz')}
            className="px-3 py-1 bg-blue-950/40 hover:bg-blue-900/60 border border-blue-700/50 text-blue-300 rounded-lg text-xs font-medium transition-all flex items-center gap-1"
          >
            <Globe className="w-3.5 h-3.5 text-blue-400" />
            <span>Global Infra Expansion (+150%)</span>
          </button>
          <button
            onClick={() => applyPreset('stagflation')}
            className="px-3 py-1 bg-purple-950/40 hover:bg-purple-900/60 border border-purple-700/50 text-purple-300 rounded-lg text-xs font-medium transition-all flex items-center gap-1"
          >
            <ShieldAlert className="w-3.5 h-3.5 text-purple-400" />
            <span>Global Rate Spike (+250bps)</span>
          </button>
        </div>
      </div>

      {/* Sliders Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">

        {/* Slider 1: Battery Pack Price */}
        <div className="bg-slate-800/80 border border-slate-700 p-4 rounded-xl shadow-md space-y-2">
          <div className="flex justify-between items-center text-xs">
            <label className="font-semibold text-slate-200">Battery Pack Price Change (%)</label>
            <span className={`font-mono font-bold ${batteryPricePct > 0 ? 'text-rose-400' : batteryPricePct < 0 ? 'text-emerald-400' : 'text-slate-400'}`}>
              {batteryPricePct > 0 ? `+${batteryPricePct}%` : `${batteryPricePct}%`}
            </span>
          </div>
          <input
            type="range"
            min="-50"
            max="50"
            step="5"
            value={batteryPricePct}
            onChange={(e) => setBatteryPricePct(parseInt(e.target.value, 10))}
            className="w-full accent-blue-500 cursor-pointer h-2 bg-slate-700 rounded-lg"
          />
          <div className="flex justify-between text-[10px] text-slate-400">
            <span>-50% (Cost Breakthrough)</span>
            <span>+50% (Supply Spike)</span>
          </div>
        </div>

        {/* Slider 2: Tariff Rate Delta */}
        <div className="bg-slate-800/80 border border-slate-700 p-4 rounded-xl shadow-md space-y-2">
          <div className="flex justify-between items-center text-xs">
            <label className="font-semibold text-slate-200">Applied Tariff Delta (Percentage Pts)</label>
            <span className={`font-mono font-bold ${tariffPp > 0 ? 'text-rose-400' : tariffPp < 0 ? 'text-emerald-400' : 'text-slate-400'}`}>
              {tariffPp > 0 ? `+${tariffPp} pp` : `${tariffPp} pp`}
            </span>
          </div>
          <input
            type="range"
            min="-20"
            max="80"
            step="5"
            value={tariffPp}
            onChange={(e) => setTariffPp(parseInt(e.target.value, 10))}
            className="w-full accent-rose-500 cursor-pointer h-2 bg-slate-700 rounded-lg"
          />
          <div className="flex justify-between text-[10px] text-slate-400">
            <span>-20 pp (Free Trade)</span>
            <span>+80 pp (100% Tariffs)</span>
          </div>
        </div>

        {/* Slider 3: Charger Expansion */}
        <div className="bg-slate-800/80 border border-slate-700 p-4 rounded-xl shadow-md space-y-2">
          <div className="flex justify-between items-center text-xs">
            <label className="font-semibold text-slate-200">Public Chargers Expansion (%)</label>
            <span className="font-mono font-bold text-emerald-400">+{chargerGrowthPct}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="200"
            step="10"
            value={chargerGrowthPct}
            onChange={(e) => setChargerGrowthPct(parseInt(e.target.value, 10))}
            className="w-full accent-emerald-500 cursor-pointer h-2 bg-slate-700 rounded-lg"
          />
          <div className="flex justify-between text-[10px] text-slate-400">
            <span>0% (Baseline)</span>
            <span>+200% (Infra Surge)</span>
          </div>
        </div>

        {/* Slider 4: Used EV Depreciation Delta */}
        <div className="bg-slate-800/80 border border-slate-700 p-4 rounded-xl shadow-md space-y-2">
          <div className="flex justify-between items-center text-xs">
            <label className="font-semibold text-slate-200">Used EV Depreciation Change (%)</label>
            <span className={`font-mono font-bold ${usedDeprDeltaPct > 0 ? 'text-rose-400' : usedDeprDeltaPct < 0 ? 'text-emerald-400' : 'text-slate-400'}`}>
              {usedDeprDeltaPct > 0 ? `+${usedDeprDeltaPct}%` : `${usedDeprDeltaPct}%`}
            </span>
          </div>
          <input
            type="range"
            min="-20"
            max="20"
            step="2"
            value={usedDeprDeltaPct}
            onChange={(e) => setUsedDeprDeltaPct(parseInt(e.target.value, 10))}
            className="w-full accent-amber-500 cursor-pointer h-2 bg-slate-700 rounded-lg"
          />
          <div className="flex justify-between text-[10px] text-slate-400">
            <span>-20% (Resale Stability)</span>
            <span>+20% (Fleet Dump Shock)</span>
          </div>
        </div>

        {/* Slider 5: Interest Rate Delta */}
        <div className="bg-slate-800/80 border border-slate-700 p-4 rounded-xl shadow-md space-y-2">
          <div className="flex justify-between items-center text-xs">
            <label className="font-semibold text-slate-200">Interest Rate Change (bps)</label>
            <span className={`font-mono font-bold ${interestRateBps > 0 ? 'text-rose-400' : interestRateBps < 0 ? 'text-emerald-400' : 'text-slate-400'}`}>
              {interestRateBps > 0 ? `+${interestRateBps} bps` : `${interestRateBps} bps`}
            </span>
          </div>
          <input
            type="range"
            min="-300"
            max="300"
            step="25"
            value={interestRateBps}
            onChange={(e) => setInterestRateBps(parseInt(e.target.value, 10))}
            className="w-full accent-purple-500 cursor-pointer h-2 bg-slate-700 rounded-lg"
          />
          <div className="flex justify-between text-[10px] text-slate-400">
            <span>-300 bps (Rate Cuts)</span>
            <span>+300 bps (Monetary Tightening)</span>
          </div>
        </div>

        {/* Slider 6: Subsidy Intensity */}
        <div className="bg-slate-800/80 border border-slate-700 p-4 rounded-xl shadow-md space-y-2">
          <div className="flex justify-between items-center text-xs">
            <label className="font-semibold text-slate-200">Subsidy Intensity Change (%)</label>
            <span className={`font-mono font-bold ${subsidyChangePct >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
              {subsidyChangePct > 0 ? `+${subsidyChangePct}%` : `${subsidyChangePct}%`}
            </span>
          </div>
          <input
            type="range"
            min="-50"
            max="50"
            step="5"
            value={subsidyChangePct}
            onChange={(e) => setSubsidyChangePct(parseInt(e.target.value, 10))}
            className="w-full accent-cyan-500 cursor-pointer h-2 bg-slate-700 rounded-lg"
          />
          <div className="flex justify-between text-[10px] text-slate-400">
            <span>-50% (Subsidy Phasedown)</span>
            <span>+50% (Incentive Boost)</span>
          </div>
        </div>
      </div>

      {/* Main Simulated Impact Display */}
      <div className="bg-slate-900 border-2 border-blue-500/40 rounded-xl p-6 shadow-2xl relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-blue-400 block">
              Simulated Global Impact on Monthly BEV Sales
            </span>
            <div className="flex items-center gap-3 mt-1">
              <span
                className={`text-4xl md:text-5xl font-black font-mono tracking-tight ${
                  globalPctImpact >= 0 ? 'text-emerald-400' : 'text-rose-400'
                }`}
              >
                {globalPctImpact >= 0 ? `+${globalPctImpact.toFixed(2)}%` : `${globalPctImpact.toFixed(2)}%`}
              </span>
              <div className="flex items-center gap-1">
                {globalPctImpact >= 0 ? (
                  <TrendingUp className="w-8 h-8 text-emerald-400" />
                ) : (
                  <TrendingDown className="w-8 h-8 text-rose-400" />
                )}
              </div>
            </div>
            <p className="text-xs text-slate-400 mt-2">
              Combined elasticity impact across battery costs, tariff friction, infrastructure expansion, and monetary policy.
            </p>
          </div>

          {/* Regional Impact Breakdown Pills */}
          <div className="bg-slate-800/90 border border-slate-700/80 p-4 rounded-xl min-w-[280px] space-y-2.5">
            <span className="text-xs font-bold text-slate-300 block border-b border-slate-700 pb-1">
              Regional Demand Impact
            </span>
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-medium">United States (US):</span>
              <span className={`font-mono font-bold ${usImpact >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                {usImpact >= 0 ? `+${usImpact.toFixed(2)}%` : `${usImpact.toFixed(2)}%`}
              </span>
            </div>
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-medium">European Union (EU):</span>
              <span className={`font-mono font-bold ${euImpact >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                {euImpact >= 0 ? `+${euImpact.toFixed(2)}%` : `${euImpact.toFixed(2)}%`}
              </span>
            </div>
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-medium">China (CN):</span>
              <span className={`font-mono font-bold ${cnImpact >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                {cnImpact >= 0 ? `+${cnImpact.toFixed(2)}%` : `${cnImpact.toFixed(2)}%`}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* OEM Vulnerability Matrix */}
      <div className="bg-slate-800/90 border border-slate-700 rounded-xl p-5 shadow-lg">
        <div className="mb-4">
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-blue-400" />
            OEM Demand Sensitivity & Tariff Vulnerability Matrix
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Evaluates firm-level exposure based on supply chain location, LFP battery mix, and export dependence.
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
          {[
            { oem: 'Tesla', impact: teslaImpact },
            { oem: 'BYD', impact: bydImpact },
            { oem: 'Volkswagen', impact: vwImpact },
            { oem: 'Hyundai-Kia', impact: hyundaiImpact },
            { oem: 'BMW', impact: bmwImpact },
            { oem: 'Mercedes', impact: benzImpact },
            { oem: 'Toyota', impact: toyotaImpact }
          ].map((item) => (
            <div
              key={item.oem}
              className="bg-slate-900 border border-slate-700 p-3 rounded-lg text-center space-y-1"
            >
              <span className="text-[11px] font-semibold text-slate-300 block truncate">{item.oem}</span>
              <span
                className={`text-sm font-bold font-mono block ${
                  item.impact >= 0 ? 'text-emerald-400' : 'text-rose-400'
                }`}
              >
                {item.impact >= 0 ? `+${item.impact.toFixed(1)}%` : `${item.impact.toFixed(1)}%`}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Policy Insights */}
      <div className="bg-slate-800/80 border border-slate-700 rounded-xl p-5 shadow-md flex items-start gap-3">
        <Sparkles className="w-6 h-6 text-amber-400 shrink-0 mt-1" />
        <div className="text-xs text-slate-300 space-y-1">
          <h4 className="font-bold text-slate-100 text-sm">Strategic Executive Policy Insights</h4>
          <p>
            • <strong>Infrastructure Leverage:</strong> Expanding public charging stations by +50% offsets a +15 percentage point trade tariff hike, demonstrating that consumer range accessibility is a stronger growth catalyst than import duties.
          </p>
          <p>
            • <strong>TCO Resale Protection:</strong> Stabilizing used EV depreciation via battery health certification reduces total cost of ownership friction, driving new car sales growth.
          </p>
        </div>
      </div>
    </div>
  );
};
