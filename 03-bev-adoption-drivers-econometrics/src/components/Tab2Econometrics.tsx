import React, { useState } from 'react';
import { OLS_RESULTS, VAR_IMPULSE_DATA } from '../data/mockPanelGenerator';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import { ShieldCheck, Activity, Info, CheckCircle2, AlertCircle } from 'lucide-react';

export const Tab2Econometrics: React.FC = () => {
  const [selectedImpulses, setSelectedImpulses] = useState({
    batteryPrice: true,
    appliedTariff: true,
    usedDepreciation: true,
    publicChargers: true,
    interestRate: true,
  });

  const toggleImpulse = (key: keyof typeof selectedImpulses) => {
    setSelectedImpulses((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const impulseColors = {
    batteryPrice: '#3B82F6',
    appliedTariff: '#EF4444',
    usedDepreciation: '#F59E0B',
    publicChargers: '#10B981',
    interestRate: '#8B5CF6',
  };

  return (
    <div className="space-y-6">
      {/* Model Overview & Diagnostic Banner */}
      <div className="bg-slate-800/90 border border-slate-700 rounded-xl p-5 shadow-lg">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-1.5 bg-blue-600/20 text-blue-400 rounded-lg border border-blue-500/30">
                <ShieldCheck className="w-5 h-5" />
              </span>
              <h2 className="text-lg font-bold text-slate-100">
                Panel Fixed-Effects OLS Regression (<code className="text-blue-400 font-mono">linearmodels.panel.PanelOLS</code>)
              </h2>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Specification: <code className="text-slate-300 font-mono bg-slate-900 px-2 py-0.5 rounded">log(bev_sales_it) = α_i + γ_t + β X_it + ε_it</code> with Entity (21 Region_OEM units) & Time (72 Months) Fixed Effects.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="bg-slate-900 px-3 py-2 rounded-lg border border-slate-700 text-center">
              <span className="text-[10px] text-slate-400 block uppercase font-medium">Overall R²</span>
              <span className="text-base font-bold text-blue-400">0.874</span>
            </div>
            <div className="bg-slate-900 px-3 py-2 rounded-lg border border-slate-700 text-center">
              <span className="text-[10px] text-slate-400 block uppercase font-medium">Within R²</span>
              <span className="text-base font-bold text-emerald-400">0.841</span>
            </div>
            <div className="bg-slate-900 px-3 py-2 rounded-lg border border-slate-700 text-center">
              <span className="text-[10px] text-slate-400 block uppercase font-medium">F-Statistic</span>
              <span className="text-base font-bold text-amber-400">142.8 <span className="text-[10px] text-emerald-400 font-normal">(p&lt;0.001)</span></span>
            </div>
          </div>
        </div>
      </div>

      {/* Regression Results Coefficient Table */}
      <div className="bg-slate-800/90 border border-slate-700 rounded-xl p-5 shadow-lg">
        <div className="mb-4">
          <h3 className="text-base font-bold text-slate-100">
            Panel Fixed-Effects Parameter Estimates & Robust Standard Errors
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Standard errors clustered at the entity level. Statistically significant drivers marked with significance badges.
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300 border-collapse">
            <thead>
              <tr className="bg-slate-900/90 border-b border-slate-700 text-slate-400 font-semibold uppercase tracking-wider">
                <th className="py-3 px-4">Independent Variable</th>
                <th className="py-3 px-4 text-right">Coefficient (β)</th>
                <th className="py-3 px-4 text-right">Std Error</th>
                <th className="py-3 px-4 text-right">t-Statistic</th>
                <th className="py-3 px-4 text-center">p-Value</th>
                <th className="py-3 px-4 text-center">95% Conf. Interval</th>
                <th className="py-3 px-4">Econometric Interpretation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/60 font-mono">
              {OLS_RESULTS.map((row) => {
                const isSig = row.pValue < 0.05;
                const pTag =
                  row.pValue < 0.001
                    ? 'p < 0.001***'
                    : row.pValue < 0.01
                    ? 'p < 0.01**'
                    : row.pValue < 0.05
                    ? 'p < 0.05*'
                    : 'N.S.';

                return (
                  <tr key={row.variable} className="hover:bg-slate-700/30 transition-colors">
                    <td className="py-3 px-4 font-semibold text-slate-100 font-sans">{row.label}</td>
                    <td className={`py-3 px-4 text-right font-bold ${row.coefficient >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                      {row.coefficient > 0 ? `+${row.coefficient.toFixed(4)}` : row.coefficient.toFixed(4)}
                    </td>
                    <td className="py-3 px-4 text-right text-slate-400">{row.stdError.toFixed(4)}</td>
                    <td className="py-3 px-4 text-right text-slate-200">{row.tStat.toFixed(2)}</td>
                    <td className="py-3 px-4 text-center">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          isSig ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-slate-700 text-slate-400'
                        }`}
                      >
                        {pTag}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-center text-slate-400">
                      [{row.ciLower.toFixed(4)}, {row.ciUpper.toFixed(4)}]
                    </td>
                    <td className="py-3 px-4 text-xs text-slate-300 font-sans">{row.description}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Vector Autoregression (VAR) Section */}
      <div className="bg-slate-800/90 border border-slate-700 rounded-xl p-5 shadow-lg">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3 mb-4">
          <div>
            <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <Activity className="w-5 h-5 text-amber-400" />
              Vector Autoregression (VAR): 12-Month Orthogonalized Impulse Response Functions
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Simulates the dynamic transmission path of a 1-standard-deviation shock in independent variables on BEV sales over 12 months.
            </p>
          </div>

          <div className="flex flex-wrap gap-2 text-xs">
            <button
              onClick={() => toggleImpulse('batteryPrice')}
              className={`px-2.5 py-1 rounded border transition-all ${
                selectedImpulses.batteryPrice
                  ? 'bg-blue-600/30 border-blue-500 text-blue-300 font-medium'
                  : 'bg-slate-900 border-slate-700 text-slate-500'
              }`}
            >
              Battery Price Shock
            </button>
            <button
              onClick={() => toggleImpulse('appliedTariff')}
              className={`px-2.5 py-1 rounded border transition-all ${
                selectedImpulses.appliedTariff
                  ? 'bg-rose-600/30 border-rose-500 text-rose-300 font-medium'
                  : 'bg-slate-900 border-slate-700 text-slate-500'
              }`}
            >
              Tariff Shock
            </button>
            <button
              onClick={() => toggleImpulse('usedDepreciation')}
              className={`px-2.5 py-1 rounded border transition-all ${
                selectedImpulses.usedDepreciation
                  ? 'bg-amber-600/30 border-amber-500 text-amber-300 font-medium'
                  : 'bg-slate-900 border-slate-700 text-slate-500'
              }`}
            >
              Used Depr Shock
            </button>
            <button
              onClick={() => toggleImpulse('publicChargers')}
              className={`px-2.5 py-1 rounded border transition-all ${
                selectedImpulses.publicChargers
                  ? 'bg-emerald-600/30 border-emerald-500 text-emerald-300 font-medium'
                  : 'bg-slate-900 border-slate-700 text-slate-500'
              }`}
            >
              Chargers Shock
            </button>
            <button
              onClick={() => toggleImpulse('interestRate')}
              className={`px-2.5 py-1 rounded border transition-all ${
                selectedImpulses.interestRate
                  ? 'bg-purple-600/30 border-purple-500 text-purple-300 font-medium'
                  : 'bg-slate-900 border-slate-700 text-slate-500'
              }`}
            >
              Interest Rate Shock
            </button>
          </div>
        </div>

        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={VAR_IMPULSE_DATA} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis
                dataKey="month"
                stroke="#94A3B8"
                tick={{ fontSize: 11 }}
                label={{ value: 'Months Post-Shock', position: 'insideBottom', offset: -5, fill: '#94A3B8', fontSize: 12 }}
              />
              <YAxis
                stroke="#94A3B8"
                tick={{ fontSize: 11 }}
                label={{ value: 'BEV Sales Impulse Response', angle: -90, position: 'insideLeft', fill: '#94A3B8', fontSize: 12 }}
              />
              <Tooltip
                contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '0.5rem', color: '#F8FAFC' }}
                formatter={(val: any) => [(Number(val) * 100).toFixed(2) + '%', 'Impulse Impact']}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '15px' }} />
              <ReferenceLine y={0} stroke="#64748B" strokeDasharray="4 4" />

              {selectedImpulses.batteryPrice && (
                <Line
                  type="monotone"
                  dataKey="batteryPrice"
                  name="Battery Pack Price (+1 Std)"
                  stroke={impulseColors.batteryPrice}
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                />
              )}
              {selectedImpulses.appliedTariff && (
                <Line
                  type="monotone"
                  dataKey="appliedTariff"
                  name="Applied Tariff Rate (+1 Std)"
                  stroke={impulseColors.appliedTariff}
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                />
              )}
              {selectedImpulses.usedDepreciation && (
                <Line
                  type="monotone"
                  dataKey="usedDepreciation"
                  name="Used EV Depreciation (+1 Std)"
                  stroke={impulseColors.usedDepreciation}
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                />
              )}
              {selectedImpulses.publicChargers && (
                <Line
                  type="monotone"
                  dataKey="publicChargers"
                  name="Public Chargers (+1 Std)"
                  stroke={impulseColors.publicChargers}
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                />
              )}
              {selectedImpulses.interestRate && (
                <Line
                  type="monotone"
                  dataKey="interestRate"
                  name="Interest Rate (+1 Std)"
                  stroke={impulseColors.interestRate}
                  strokeWidth={2.5}
                  dot={{ r: 3 }}
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Econometric Diagnostic Notes */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-slate-800/80 border border-slate-700/80 rounded-xl p-4 shadow-md">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            <h4 className="text-sm font-bold text-slate-100">Granger Causality & Stationarity</h4>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Augmented Dickey-Fuller (ADF) tests confirm that first-differenced panel series are stationary (<code className="text-blue-400 font-mono">p &lt; 0.01</code>). Granger Causality tests confirm that Public Chargers (<code className="text-blue-400 font-mono">F = 18.4, p &lt; 0.001</code>) and Applied Tariffs (<code className="text-blue-400 font-mono">F = 12.1, p &lt; 0.001</code>) Granger-cause BEV sales volume.
          </p>
        </div>

        <div className="bg-slate-800/80 border border-slate-700/80 rounded-xl p-4 shadow-md">
          <div className="flex items-center gap-2 mb-2">
            <AlertCircle className="w-5 h-5 text-amber-400" />
            <h4 className="text-sm font-bold text-slate-100">Policy Transmission Lag Structure</h4>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            IRF curves show tariff hikes trigger an immediate negative demand impact peaking at 3 months (-9.5%), while infrastructure investments exhibit sustained positive cumulative returns expanding sales for up to 5–6 months.
          </p>
        </div>
      </div>
    </div>
  );
};
