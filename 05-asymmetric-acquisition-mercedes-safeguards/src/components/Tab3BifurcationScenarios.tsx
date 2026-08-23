import React, { useState } from 'react';
import { Split, Sliders, LineChart as ChartIcon } from 'lucide-react';
import { ResponsiveContainer, ComposedChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';
import bifurcationData from '../../data/bifurcation_scenarios.json';

export const Tab3BifurcationScenarios: React.FC = () => {
  const [selectedScenario, setSelectedScenario] = useState<'A' | 'B' | 'C'>('B');
  const [forecastView, setForecastView] = useState<'margin' | 'share' | 'battery'>('margin');

  // Embedded Interactive Calculator Levers (Inside Tab 5)
  const [capitalDilution, setCapitalDilution] = useState<number>(15);
  const [alliedTurnout, setAlliedTurnout] = useState<number>(85);
  const [tariffRate, setTariffRate] = useState<number>(21);
  const [chinaVolumeShock, setChinaVolumeShock] = useState<number>(15);
  const [mineralPremium, setMineralPremium] = useState<number>(20);
  const [bevVolume, setBevVolume] = useState<number>(1200000);

  const applyPreset = (preset: 'A' | 'B' | 'C') => {
    setSelectedScenario(preset);
    if (preset === 'A') {
      setCapitalDilution(0);
      setAlliedTurnout(52);
      setChinaVolumeShock(5);
      setMineralPremium(5);
      setBevVolume(800000);
      setTariffRate(10);
    } else if (preset === 'B') {
      setCapitalDilution(15);
      setAlliedTurnout(85);
      setChinaVolumeShock(15);
      setMineralPremium(20);
      setBevVolume(1200000);
      setTariffRate(21);
    } else {
      setCapitalDilution(30);
      setAlliedTurnout(90);
      setChinaVolumeShock(40);
      setMineralPremium(35);
      setBevVolume(2000000);
      setTariffRate(35);
    }
  };

  // Exact Disaggregated AktG §179 Math
  const S_cn_0 = 19.67;
  const S_allied_0 = 35.0;
  const S_float_0 = 45.33;

  const S_cn = S_cn_0 / (1.0 + (capitalDilution / 100.0));
  const S_allied = (S_allied_0 + capitalDilution) / (1.0 + (capitalDilution / 100.0));
  const S_float = S_float_0 / (1.0 + (capitalDilution / 100.0));

  const T_cn = 1.0;
  const T_allied = alliedTurnout / 100.0;
  const T_float = 0.38;

  const totalTurnout = (S_cn * T_cn) + (S_allied * T_allied) + (S_float * T_float);
  const effectiveCnPower = (S_cn * T_cn / totalTurnout) * 100.0;
  const hasBlockingMinority = (S_cn * T_cn / totalTurnout) >= 0.2500000;

  // Dynamic Financial Calculations
  const unitPackPenalty = (82.0 * 128.0 * (mineralPremium / 100.0)) / 1.08;
  const totalBatteryPenaltyB = (bevVolume * unitPackPenalty) / 1e9;
  const chinaEbitLossB = 12.8 * (chinaVolumeShock / 100.0) * 1.25;
  const tariffLossB = (32000 * 42500 * (tariffRate / 100.0) * 0.7) / 1e9;

  const baseEbit = 36.5;
  const totalDeductionsB = totalBatteryPenaltyB + chinaEbitLossB + tariffLossB;
  const dynAdjustedEbit = Math.max(5.0, Number((baseEbit - totalDeductionsB).toFixed(2)));
  const dynMarginPct = Number(((dynAdjustedEbit / 380.0) * 100.0).toFixed(2));

  const isSweetSpot = dynMarginPct >= 7.8 && !hasBlockingMinority;
  const isCliffEdge = dynMarginPct < 5.0 || chinaVolumeShock >= 35;

  // Dynamic 2026-2035 10-year forecast curve based on active sliders
  const forecastData = bifurcationData.forecastTimeSeries2026_2035.map((d, idx) => {
    let customMargin = dynMarginPct;
    if (idx > 0) {
      if (isSweetSpot) {
        customMargin = Number((dynMarginPct + (10.2 - dynMarginPct) * (idx / 10.0)).toFixed(2));
      } else if (isCliffEdge) {
        customMargin = Number((Math.max(1.5, dynMarginPct - 2.0 * Math.exp(-idx / 2.0) + 0.45 * idx)).toFixed(2));
      } else {
        customMargin = Number((Math.max(3.5, dynMarginPct - 0.42 * idx)).toFixed(2));
      }
    }
    return {
      year: d.year,
      'Scenario A: Status Quo': forecastView === 'margin' ? d.scenA_margin : forecastView === 'share' ? d.scenA_share : d.scenA_batteryAutonomy,
      'Scenario B: Phased De-risking (Recommended)': forecastView === 'margin' ? d.scenB_margin : forecastView === 'share' ? d.scenB_share : d.scenB_batteryAutonomy,
      'Scenario C: Abrupt Decoupling': forecastView === 'margin' ? d.scenC_margin : forecastView === 'share' ? d.scenC_share : d.scenC_batteryAutonomy,
      'Live Simulation Path': forecastView === 'margin' ? customMargin : isSweetSpot ? d.scenB_share : d.scenA_share
    };
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Top Hero Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-950/60 border border-rose-800/50 text-rose-300 text-xs font-mono font-bold">
            <Split className="w-3.5 h-3.5" />
            2026–2035 3-PATH REGULATORY SCENARIOS &amp; 10-YEAR FORECAST ENGINE
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            3 Strategic Bifurcation Scenarios &amp; 2026–2035 Simulation Engine
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            Click the preset buttons or adjust the 6 active policy levers below to recalculate real-time operating margins, AktG §179 voting thresholds, and 10-year dynamic trajectories.
          </p>
        </div>
      </div>

      {/* 3 Preset Selector Buttons */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          onClick={() => applyPreset('A')}
          className={`p-5 rounded-2xl border text-left transition flex flex-col justify-between ${
            selectedScenario === 'A'
              ? 'bg-rose-950/70 border-rose-500 text-white shadow-xl shadow-rose-950/40'
              : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:text-white hover:bg-slate-900'
          }`}
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">
              Scenario A Preset
            </span>
            <span className="text-xs font-mono font-bold text-rose-400">🔴 2035 Subcontractor Decline</span>
          </div>
          <h3 className="text-base font-bold text-white mb-1">Scenario A: Status Quo</h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            Entrenched 25% blocking vetoes. Operating margins halved to 4.2% by 2035 with loss of software autonomy.
          </p>
        </button>

        <button
          onClick={() => applyPreset('B')}
          className={`p-5 rounded-2xl border text-left transition flex flex-col justify-between ${
            selectedScenario === 'B'
              ? 'bg-emerald-950/70 border-emerald-500 text-white shadow-xl shadow-emerald-950/40'
              : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:text-white hover:bg-slate-900'
          }`}
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
              Scenario B Preset (Recommended)
            </span>
            <span className="text-xs font-mono font-bold text-emerald-400">🟢 2035 Sovereignty Recovery</span>
          </div>
          <h3 className="text-base font-bold text-white mb-1">Scenario B: Phased De-risking</h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            Eliminates 25% blocking vetoes. Operating margins expand to 10.2% post-2032, securing global leadership.
          </p>
        </button>

        <button
          onClick={() => applyPreset('C')}
          className={`p-5 rounded-2xl border text-left transition flex flex-col justify-between ${
            selectedScenario === 'C'
              ? 'bg-rose-950/70 border-rose-500 text-white shadow-xl shadow-rose-950/40'
              : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:text-white hover:bg-slate-900'
          }`}
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">
              Scenario C Preset
            </span>
            <span className="text-xs font-mono font-bold text-rose-400">🔴 2026-28 Liquidity Cliff</span>
          </div>
          <h3 className="text-base font-bold text-white mb-1">Scenario C: Abrupt Decoupling</h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            Abrupt exit causes near-term margin collapse to 1.8% and severe industrial shocks across Germany.
          </p>
        </button>
      </div>

      {/* Dynamic Unified Scenario Evaluation Box */}
      <div
        className={`p-6 rounded-2xl border-2 space-y-4 ${
          isSweetSpot
            ? 'bg-slate-900/90 border-emerald-500'
            : 'bg-slate-900/90 border-rose-500'
        }`}
      >
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
          <div>
            <span
              className={`text-xs font-mono font-bold px-3 py-1 rounded uppercase ${
                isSweetSpot
                  ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                  : 'bg-rose-950 text-rose-300 border border-rose-800'
              }`}
            >
              {isSweetSpot ? '🟢 STRATEGIC SWEET SPOT (OPTIMAL ROBUSTNESS)' : isCliffEdge ? '🔴 HIGH-RISK CLIFF-EDGE (CRITICAL CRISIS)' : '🔴 STATUS QUO DEPENDENCY (SEVERE CAPTURE)'}
            </span>
            <h3 className="text-xl font-black text-white mt-1.5">
              {isSweetSpot
                ? 'Scenario B: Phased De-risking (2035 Sovereignty Recovery: Recommended)'
                : isCliffEdge
                ? 'Scenario C: Abrupt Decoupling (2026-2028 Liquidity Cliff)'
                : 'Scenario A: Status Quo (2035 Subcontractor Decline)'}
            </h3>
          </div>
          <div className="text-right">
            <span className="text-xs font-medium text-slate-300">Simulated EBIT &amp; Margin:</span>
            <div className={`text-2xl font-black font-mono ${isSweetSpot ? 'text-emerald-400' : 'text-rose-400'}`}>
              €{dynAdjustedEbit.toFixed(1)}B <span className="text-sm font-normal text-white">({dynMarginPct.toFixed(2)}%)</span>
            </div>
          </div>
        </div>

        {/* 4 Quantitative Output Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-center">
          <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-xs font-bold text-white">1. Adjusted Total EBIT</div>
            <div className={`text-xl font-black font-mono mt-1 ${isSweetSpot ? 'text-emerald-400' : 'text-rose-400'}`}>
              €{dynAdjustedEbit.toFixed(1)}B
            </div>
            <div className="text-[11px] text-slate-300 mt-0.5">Deductions: -€{totalDeductionsB.toFixed(2)}B</div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-xs font-bold text-white">2. Chinese Effective Voting Power</div>
            <div className={`text-xl font-black font-mono mt-1 ${hasBlockingMinority ? 'text-rose-400' : 'text-emerald-400'}`}>
              {effectiveCnPower.toFixed(2)}%
            </div>
            <div className="text-[11px] text-slate-300 mt-0.5">Diluted Stake: {S_cn.toFixed(2)}%</div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-xs font-bold text-white">3. Battery Pack Penalty</div>
            <div className={`text-xl font-black font-mono mt-1 ${unitPackPenalty > 1500 ? 'text-orange-400' : 'text-white'}`}>
              +€{unitPackPenalty.toFixed(0)}
            </div>
            <div className="text-[11px] text-slate-300 mt-0.5">Total: -€{totalBatteryPenaltyB.toFixed(2)}B</div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
            <div className="text-xs font-bold text-white">4. AktG §179 Veto Status</div>
            <div className={`text-sm font-black mt-1.5 ${hasBlockingMinority ? 'text-rose-400' : 'text-emerald-400'}`}>
              {hasBlockingMinority ? '🔴 25% Veto Active (High Risk)' : '🟢 25% Veto Eliminated (Safe)'}
            </div>
            <div className="text-[11px] text-slate-300 mt-0.5">Threshold: &lt;25.00% Required</div>
          </div>
        </div>
      </div>

      {/* 6 Parametric Sliders */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2 border-b border-slate-800 pb-3">
          <Sliders className="w-4 h-4 text-emerald-400" />
          Real-Time Parametric Sliders (6 Active Levers)
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-white font-bold">1. Strategic Capital Dilution:</span>
              <span className="text-emerald-400 font-bold">+{capitalDilution}% Shares</span>
            </div>
            <input
              type="range"
              min="0"
              max="45"
              step="5"
              value={capitalDilution}
              onChange={(e) => setCapitalDilution(Number(e.target.value))}
              className="w-full accent-emerald-500"
            />
            <p className="text-[11px] text-slate-400">Diluted Chinese Stake: <strong className="text-white">{S_cn.toFixed(2)}%</strong></p>
          </div>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-white font-bold">2. Allied Proxy Turnout (85%+ Drives Total 69%+):</span>
              <span className="text-sky-400 font-bold">{alliedTurnout}% Mobilized</span>
            </div>
            <input
              type="range"
              min="50"
              max="95"
              step="1"
              value={alliedTurnout}
              onChange={(e) => setAlliedTurnout(Number(e.target.value))}
              className="w-full accent-sky-500"
            />
            <p className="text-[11px] text-slate-400">Effective Voting Power: <strong className="text-white">{effectiveCnPower.toFixed(2)}%</strong> (Total Turnout: {totalTurnout.toFixed(1)}%)</p>
          </div>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-white font-bold">3. China Volume Shock:</span>
              <span className="text-rose-400 font-bold">-{chinaVolumeShock}% Contraction</span>
            </div>
            <input
              type="range"
              min="5"
              max="50"
              step="5"
              value={chinaVolumeShock}
              onChange={(e) => setChinaVolumeShock(Number(e.target.value))}
              className="w-full accent-rose-500"
            />
            <p className="text-[11px] text-slate-400">EBIT Impact: <strong className="text-rose-400">-€{chinaEbitLossB.toFixed(2)}B</strong></p>
          </div>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-white font-bold">4. Non-China Mineral Premium:</span>
              <span className="text-orange-400 font-bold">+{mineralPremium}% Surcharge</span>
            </div>
            <input
              type="range"
              min="5"
              max="40"
              step="5"
              value={mineralPremium}
              onChange={(e) => setMineralPremium(Number(e.target.value))}
              className="w-full accent-orange-500"
            />
            <p className="text-[11px] text-slate-400">Unit Pack Penalty: <strong className="text-orange-400">+€{unitPackPenalty.toFixed(0)}/EV</strong></p>
          </div>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-white font-bold">5. Triad BEV Annual Volume:</span>
              <span className="text-white font-bold">{(bevVolume / 1000000).toFixed(2)}M Units</span>
            </div>
            <input
              type="range"
              min="500000"
              max="2500000"
              step="100000"
              value={bevVolume}
              onChange={(e) => setBevVolume(Number(e.target.value))}
              className="w-full accent-slate-400"
            />
            <p className="text-[11px] text-slate-400">Total Battery Surcharge: <strong className="text-white">-€{totalBatteryPenaltyB.toFixed(2)}B</strong></p>
          </div>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-white font-bold">6. EU Countervailing Tariff:</span>
              <span className="text-rose-400 font-bold">{tariffRate}% Duty</span>
            </div>
            <input
              type="range"
              min="10"
              max="40"
              step="1"
              value={tariffRate}
              onChange={(e) => setTariffRate(Number(e.target.value))}
              className="w-full accent-rose-500"
            />
            <p className="text-[11px] text-slate-400">Re-Export Tariff Hit: <strong className="text-rose-400">-€{(tariffLossB * 1000).toFixed(0)}M</strong></p>
          </div>
        </div>
      </div>

      {/* 2026–2035 10-Year Dynamic Forecast Trajectory Chart */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <ChartIcon className="w-4 h-4 text-emerald-400" />
              2026–2035 10-Year Forecast Bifurcation Trajectories
            </h3>
            <p className="text-xs text-slate-400">Dynamic forecast curves update in real time as sliders are adjusted.</p>
          </div>

          <div className="flex gap-2">
            <button
              onClick={() => setForecastView('margin')}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition ${
                forecastView === 'margin' ? 'bg-emerald-600 text-white' : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              1. Global EBIT Margin (%)
            </button>
            <button
              onClick={() => setForecastView('share')}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition ${
                forecastView === 'share' ? 'bg-emerald-600 text-white' : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              2. China Market Share (%)
            </button>
            <button
              onClick={() => setForecastView('battery')}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition ${
                forecastView === 'battery' ? 'bg-emerald-600 text-white' : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              3. Battery Supply Autonomy (%)
            </button>
          </div>
        </div>

        <div className="h-[360px] w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={forecastData} margin={{ top: 20, right: 20, bottom: 20, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="year" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" label={{ value: forecastView === 'margin' ? 'EBIT Margin (%)' : forecastView === 'share' ? 'Market Share (%)' : 'Autonomy (%)', angle: -90, position: 'insideLeft', fill: '#94a3b8', fontSize: 11 }} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} />
              <Legend />
              <Line type="monotone" dataKey="Scenario A: Status Quo" stroke="#F43F5E" strokeWidth={2.5} strokeDasharray="5 5" dot={{ r: 3 }} />
              <Line type="monotone" dataKey="Scenario B: Phased De-risking (Recommended)" stroke="#10B981" strokeWidth={3.5} dot={{ r: 4 }} />
              <Line type="monotone" dataKey="Scenario C: Abrupt Decoupling" stroke="#6366F1" strokeWidth={2} strokeDasharray="3 3" dot={{ r: 3 }} />
              {forecastView === 'margin' && (
                <Line type="monotone" dataKey="Live Simulation Path" stroke="#FCD34D" strokeWidth={4} dot={{ r: 5 }} />
              )}
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
