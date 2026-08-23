import React, { useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
} from 'recharts';
import { DollarSign, Layers, AlertTriangle, Cpu, Car, Radio, ShieldCheck } from 'lucide-react';
import financialData from '../../data/financial_dependency.json';
import supplyChainData from '../../data/supply_chain_lockin.json';

export const Tab2FinancialDependency: React.FC = () => {
  const [selectedSensitivity, setSelectedSensitivity] = useState<'10' | '25' | '50'>('25');

  const regionalData = financialData.unitSales2023.regions;
  const historyData = financialData.historicalTrend;
  const projects = supplyChainData.techAndSupplyChainLockin;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Top Banner Alert */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-950/60 border border-amber-800/50 text-amber-300 text-xs font-mono font-bold mb-2">
              <DollarSign className="w-3.5 h-3.5" />
              STRUCTURAL PROFIT ASYMMETRY &amp; FLAGSHIP CONCENTRATION
            </div>
            <h2 className="text-2xl font-black text-white tracking-tight">
              The China Margin Engine: 30% of Volume, &gt;34% of Operating Profit
            </h2>
            <p className="text-sm text-slate-300 max-w-3xl leading-relaxed mt-1">
              Mercedes-Benz is disproportionately reliant on the Chinese luxury market where its ultra-high-margin top-end flagships (<strong>S-Class, Maybach, G-Class</strong>) generate over one-third of global group EBIT. Sourcing 4-cylinder hybrid engines and smart platforms from Chinese JVs has locked in permanent technological dependency.
            </p>
          </div>
        </div>
      </div>

      {/* Regional Volume vs EBIT Contribution Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7 bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-200 uppercase font-mono tracking-wider">
                2023 Regional Deliveries vs. EBIT Share (%)
              </h3>
              <p className="text-xs text-slate-400">Comparing unit volume share against operational earnings contribution</p>
            </div>
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
              Total EBIT: €19.7B
            </span>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={regionalData} margin={{ top: 20, right: 20, left: -10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="region" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 11 }} tickFormatter={(v) => `${v}%`} />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const d = payload[0].payload;
                      return (
                        <div className="bg-slate-950 border border-slate-700 p-3 rounded-lg shadow-xl text-xs space-y-1">
                          <div className="font-bold text-white text-sm">{d.region}</div>
                          <div className="text-sky-400 font-mono">Deliveries: {d.units.toLocaleString()} units ({d.sharePct}%)</div>
                          <div className="text-rose-400 font-mono">EBIT Contribution: €{d.ebitContributionEurBillion}B ({d.ebitSharePct}%)</div>
                          <div className="text-amber-300 text-[11px] pt-1 border-t border-slate-800">
                            <strong>Flagship Mix:</strong> {d.flagshipConcentration}
                          </div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: '10px', fontSize: '12px' }} />
                <Bar dataKey="sharePct" name="Unit Sales Share (%)" fill="#0284c7" radius={[4, 4, 0, 0]} />
                <Bar dataKey="ebitSharePct" name="EBIT Contribution Share (%)" fill="#e11d48" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="mt-3 grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-xs">
            {regionalData.map((r, idx) => (
              <div key={idx} className="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800/80">
                <div className="text-slate-400 text-[11px] truncate font-medium">{r.region.split(' ')[0]}</div>
                <div className="text-sm font-bold text-white font-mono mt-0.5">€{r.ebitContributionEurBillion}B</div>
                <div className="text-[10px] text-rose-400 font-mono font-semibold">{r.ebitSharePct}% EBIT</div>
              </div>
            ))}
          </div>
        </div>

        {/* Historical Trend Chart (2018-2024) */}
        <div className="lg:col-span-5 bg-slate-900/90 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-bold text-slate-200 uppercase font-mono tracking-wider">
                China EBIT &amp; Volume Trajectory (2018–2024)
              </h3>
            </div>
            <p className="text-xs text-slate-400 mb-4">Historical evolution of Chinese market dependence</p>

            <div className="h-60 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={historyData} margin={{ top: 10, right: 15, left: -15, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="year" stroke="#64748b" tick={{ fontSize: 11 }} />
                  <YAxis stroke="#64748b" tick={{ fontSize: 11 }} tickFormatter={(v) => `${v}%`} domain={[20, 45]} />
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const d = payload[0].payload;
                        return (
                          <div className="bg-slate-950 border border-slate-700 p-2.5 rounded-lg shadow-xl text-xs space-y-1">
                            <div className="font-bold text-white font-mono">{d.year} Financials</div>
                            <div className="text-rose-400 font-mono">China EBIT Share: <strong>{d.chinaEbitSharePct}%</strong></div>
                            <div className="text-sky-400 font-mono">China Volume Share: {d.chinaSharePct}% ({d.chinaSalesK}k units)</div>
                            <div className="text-slate-400 font-mono">Group Revenue: €{d.groupRevenueEurB}B</div>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Legend verticalAlign="top" wrapperStyle={{ paddingBottom: '10px', fontSize: '11px' }} />
                  <Line type="monotone" dataKey="chinaEbitSharePct" name="China EBIT Share (%)" stroke="#f43f5e" strokeWidth={2.5} dot={{ r: 4 }} />
                  <Line type="monotone" dataKey="chinaSharePct" name="China Volume Share (%)" stroke="#38bdf8" strokeWidth={2} strokeDasharray="4 4" dot={{ r: 3 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Sensitivity Stress Test Simulator */}
          <div className="mt-4 p-3.5 rounded-xl bg-slate-950/90 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="font-bold text-slate-300 flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                China Sales Contraction Stress-Test:
              </span>
              <div className="flex gap-1">
                {(['10', '25', '50'] as const).map((lvl) => (
                  <button
                    key={lvl}
                    onClick={() => setSelectedSensitivity(lvl)}
                    className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold transition ${
                      selectedSensitivity === lvl
                        ? 'bg-rose-600 text-white'
                        : 'bg-slate-800 text-slate-400 hover:text-white'
                    }`}
                  >
                    -{lvl}%
                  </button>
                ))}
              </div>
            </div>

            {selectedSensitivity === '10' && (
              <div className="grid grid-cols-3 gap-2 text-center text-xs pt-1">
                <div className="bg-slate-900 p-1.5 rounded border border-slate-800">
                  <div className="text-[10px] text-slate-400">Revenue Lost</div>
                  <div className="font-mono font-bold text-white">-€4.8B</div>
                </div>
                <div className="bg-slate-900 p-1.5 rounded border border-slate-800">
                  <div className="text-[10px] text-rose-400">EBIT Lost</div>
                  <div className="font-mono font-bold text-rose-400">-€1.9B</div>
                </div>
                <div className="bg-slate-900 p-1.5 rounded border border-slate-800">
                  <div className="text-[10px] text-amber-400">Margin Hit</div>
                  <div className="font-mono font-bold text-amber-400">-115 bps</div>
                </div>
              </div>
            )}
            {selectedSensitivity === '25' && (
              <div className="grid grid-cols-3 gap-2 text-center text-xs pt-1">
                <div className="bg-slate-900 p-1.5 rounded border border-slate-800">
                  <div className="text-[10px] text-slate-400">Revenue Lost</div>
                  <div className="font-mono font-bold text-white">-€12.0B</div>
                </div>
                <div className="bg-slate-900 p-1.5 rounded border border-slate-800">
                  <div className="text-[10px] text-rose-400">EBIT Lost</div>
                  <div className="font-mono font-bold text-rose-400">-€4.8B</div>
                </div>
                <div className="bg-slate-900 p-1.5 rounded border border-slate-800">
                  <div className="text-[10px] text-amber-400">Margin Hit</div>
                  <div className="font-mono font-bold text-amber-400">-290 bps</div>
                </div>
              </div>
            )}
            {selectedSensitivity === '50' && (
              <div className="grid grid-cols-3 gap-2 text-center text-xs pt-1">
                <div className="bg-slate-900 p-1.5 rounded border border-slate-800">
                  <div className="text-[10px] text-slate-400">Revenue Lost</div>
                  <div className="font-mono font-bold text-white">-€24.1B</div>
                </div>
                <div className="bg-slate-900 p-1.5 rounded border border-slate-800">
                  <div className="text-[10px] text-rose-400">EBIT Lost</div>
                  <div className="font-mono font-bold text-rose-400">-€9.6B</div>
                </div>
                <div className="bg-slate-900 p-1.5 rounded border border-slate-800">
                  <div className="text-[10px] text-amber-400">Margin Hit</div>
                  <div className="font-mono font-bold text-amber-400">-580 bps</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Technological & Supply Chain Lock-In Explorer */}
      <div>
        <h3 className="text-sm font-bold text-slate-200 uppercase font-mono tracking-wider mb-4 flex items-center gap-2">
          <Layers className="w-4 h-4 text-sky-400" />
          The 3 Pillars of Structural Technological &amp; Supply Chain Lock-In
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {projects.map((proj) => (
            <div
              key={proj.id}
              className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-3">
                  <span className="p-2 rounded-lg bg-slate-800 text-sky-400 border border-slate-700">
                    {proj.id === 'smart_jv' && <Car className="w-4 h-4" />}
                    {proj.id === 'horse_powertrain' && <Cpu className="w-4 h-4" />}
                    {proj.id === 'qianli_ad_telemetry' && <Radio className="w-4 h-4" />}
                  </span>
                  <span className="text-[11px] font-mono px-2.5 py-0.5 rounded bg-rose-950/80 text-rose-300 border border-rose-800/60 font-bold">
                    Risk: {proj.riskScore}
                  </span>
                </div>

                <h4 className="text-base font-bold text-white mb-1">{proj.project}</h4>
                <div className="text-xs text-sky-400 font-medium mb-3">Partner: {proj.partner} ({proj.establishedYear})</div>

                <div className="space-y-2.5 text-xs text-slate-300">
                  <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800/80">
                    <span className="font-semibold text-slate-400 block mb-1 text-[11px]">Integration Mechanism:</span>
                    <p className="text-slate-300 leading-relaxed">{proj.mechanism}</p>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800">
                <span className="font-semibold text-amber-400 block text-[11px] mb-1">Strategic Lock-in Consequence:</span>
                <p className="text-xs text-slate-400 leading-normal">{proj.strategicConsequence}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
