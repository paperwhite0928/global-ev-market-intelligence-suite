import React, { useState } from 'react';
import { ResponsiveContainer, BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ReferenceLine } from 'recharts';
import { TrendingDown, Activity, Layers, ShieldAlert } from 'lucide-react';
import historicalDeliveries from '../../data/historical_deliveries.json';

export const Tab2PeakVsPresent: React.FC = () => {
  const [mainCategory, setMainCategory] = useState<'perf' | 'dep' | 'radar'>('perf');
  const [perfSub, setPerfSub] = useState<'oem' | 'prod' | 'share'>('oem');
  const [depMetric, setDepMetric] = useState<string>('vote');
  const [radarMode, setRadarMode] = useState<'overlay' | 'split'>('overlay');

  const chartData = historicalDeliveries.timeSeries.map((d: any) => ({
    year: d.year,
    'Volkswagen (VW Deep Blue)': d.vwChinaK,
    'Mercedes-Benz (Silver)': d.mercedesChinaK,
    'BMW Group (White)': d.bmwChinaK,
    'Total Deliveries': d.totalTriadChinaK,
    'Local Production (Yellow)': d.totalTriadLocalProdK,
    'Market Share (%)': d.triadChinaMarketSharePct,
    'EV Penetration (%)': d.chineseEvPenetrationPct,
    // Disaggregated metrics
    'Volkswagen': depMetric === 'ebit' ? d.vwEbitShare : depMetric === 'cost' ? d.vwComponentsCost : depMetric === 'cr3' ? d.vwSupplierConcentration : depMetric === 'data' ? d.vwDataStorage : depMetric === 'vote' ? d.vwVotingPower : d.vwSubstitutability,
    'Mercedes-Benz': depMetric === 'ebit' ? d.mercedesEbitShare : depMetric === 'cost' ? d.mercedesComponentsCost : depMetric === 'cr3' ? d.mercedesSupplierConcentration : depMetric === 'data' ? d.mercedesDataStorage : depMetric === 'vote' ? d.mercedesVotingPower : d.mercedesSubstitutability,
    'BMW Group': depMetric === 'ebit' ? d.bmwEbitShare : depMetric === 'cost' ? d.bmwComponentsCost : depMetric === 'cr3' ? d.bmwSupplierConcentration : depMetric === 'data' ? d.bmwDataStorage : depMetric === 'vote' ? d.bmwVotingPower : d.bmwSubstitutability,
    'Triad Composite Avg': depMetric === 'ebit' ? d.chinaEbitSharePct : depMetric === 'cost' ? d.chineseComponentsCostPct : depMetric === 'cr3' ? d.supplierConcentrationCr3Pct : depMetric === 'data' ? d.dataStorageIsolationPct : depMetric === 'vote' ? d.votingPowerPct : d.substitutabilityYears
  }));

  const radarData = [
    { subject: '1. EBIT Share', 'Mercedes-Benz': 31.5, 'Volkswagen Group': 38.0, 'BMW Group': 28.5, 'Triad Benchmark': 32.7, fullMark: 100 },
    { subject: '2. BOM Cost', 'Mercedes-Benz': 42.0, 'Volkswagen Group': 58.5, 'BMW Group': 48.0, 'Triad Benchmark': 49.5, fullMark: 100 },
    { subject: '3. Supplier CR3', 'Mercedes-Benz': 68.0, 'Volkswagen Group': 76.5, 'BMW Group': 82.0, 'Triad Benchmark': 75.5, fullMark: 100 },
    { subject: '4. Data Isolation', 'Mercedes-Benz': 100.0, 'Volkswagen Group': 100.0, 'BMW Group': 100.0, 'Triad Benchmark': 100.0, fullMark: 100 },
    { subject: '5. Effective Voting', 'Mercedes-Benz': 37.5, 'Volkswagen Group': 15.0, 'BMW Group': 20.0, 'Triad Benchmark': 24.2, fullMark: 100 },
    { subject: '6. Lead Time Score', 'Mercedes-Benz': 74.0, 'Volkswagen Group': 96.0, 'BMW Group': 84.0, 'Triad Benchmark': 84.0, fullMark: 100 }
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Hero Header */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-950/60 border border-rose-800/50 text-rose-300 text-xs font-mono font-bold">
            <TrendingDown className="w-3.5 h-3.5" />
            2019–2025 STATUTORY TIME-SERIES &amp; 3-OEM DEPENDENCY AUDIT
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            2019–2025 Continuous Time-Series Market Collapse &amp; Quantitative Dependency Audit
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            The German Auto Triad's structural exposure is parameterize across <strong>6 measurable statutory dimensions (EBIT Share 32.7%, BOM Cost 49.5%, Top-3 Supplier Concentration 75.5%, Data Ring-fencing 100%, Voting Power 37.5%, and Replacement Lead Time 4.2 Years)</strong>.
          </p>
        </div>
      </div>

      {/* Main Category Tabs */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setMainCategory('perf')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                mainCategory === 'perf' ? 'bg-blue-600 text-white' : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              📊 1. Basic Market Performance
            </button>
            <button
              onClick={() => setMainCategory('dep')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                mainCategory === 'dep' ? 'bg-blue-600 text-white' : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              📐 2. 6 Measurable Dependency Time-Series
            </button>
            <button
              onClick={() => setMainCategory('radar')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                mainCategory === 'radar' ? 'bg-rose-600 text-white' : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              🕸️ 3. 6-Dimension Dependency Radar
            </button>
          </div>

          {/* Sub Controls */}
          {mainCategory === 'perf' && (
            <div className="flex gap-1.5">
              <button
                onClick={() => setPerfSub('oem')}
                className={`px-2.5 py-1 rounded text-xs transition ${perfSub === 'oem' ? 'bg-slate-800 text-white font-bold' : 'text-slate-400'}`}
              >
                3-OEM Deliveries
              </button>
              <button
                onClick={() => setPerfSub('prod')}
                className={`px-2.5 py-1 rounded text-xs transition ${perfSub === 'prod' ? 'bg-slate-800 text-white font-bold' : 'text-slate-400'}`}
              >
                Production vs Sales
              </button>
              <button
                onClick={() => setPerfSub('share')}
                className={`px-2.5 py-1 rounded text-xs transition ${perfSub === 'share' ? 'bg-slate-800 text-white font-bold' : 'text-slate-400'}`}
              >
                Share vs EV Penetration
              </button>
            </div>
          )}

          {mainCategory === 'dep' && (
            <select
              value={depMetric}
              onChange={(e) => setDepMetric(e.target.value)}
              className="bg-slate-950 text-slate-200 border border-slate-800 rounded px-2.5 py-1 text-xs"
            >
              <option value="ebit">1. China EBIT Share (%)</option>
              <option value="cost">2. Chinese Component BOM Cost (%)</option>
              <option value="cr3">3. Supplier Concentration CR3 (%)</option>
              <option value="data">4. Data Isolation Ratio (%)</option>
              <option value="vote">5. Effective Chinese Voting Power (%)</option>
              <option value="sub">6. Replacement Lead Time (Years)</option>
            </select>
          )}

          {mainCategory === 'radar' && (
            <div className="flex gap-1.5">
              <button
                onClick={() => setRadarMode('overlay')}
                className={`px-2.5 py-1 rounded text-xs transition ${radarMode === 'overlay' ? 'bg-slate-800 text-white font-bold' : 'text-slate-400'}`}
              >
                Overlay View
              </button>
              <button
                onClick={() => setRadarMode('split')}
                className={`px-2.5 py-1 rounded text-xs transition ${radarMode === 'split' ? 'bg-slate-800 text-white font-bold' : 'text-slate-400'}`}
              >
                3-Split View
              </button>
            </div>
          )}
        </div>

        {/* Chart View Area */}
        <div className="w-full pt-2">
          {mainCategory === 'perf' ? (
            <div className="h-[380px]">
              <ResponsiveContainer width="100%" height="100%">
                {perfSub === 'oem' ? (
                  <BarChart data={chartData} margin={{ top: 20, right: 20, bottom: 20, left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="year" stroke="#94a3b8" />
                    <YAxis stroke="#94a3b8" />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} />
                    <Legend />
                    <Bar dataKey="Volkswagen (VW Deep Blue)" fill="#002D72" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="Mercedes-Benz (Silver)" fill="#94A3B8" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="BMW Group (White)" fill="#FFFFFF" stroke="#CBD5E1" strokeWidth={1.5} radius={[4, 4, 0, 0]} />
                  </BarChart>
                ) : perfSub === 'prod' ? (
                  <BarChart data={chartData} margin={{ top: 20, right: 20, bottom: 20, left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="year" stroke="#94a3b8" />
                    <YAxis stroke="#94a3b8" />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} />
                    <Legend />
                    <Bar dataKey="Local Production (Yellow)" fill="#EAB308" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="Total Deliveries" fill="#DC2626" radius={[4, 4, 0, 0]} />
                  </BarChart>
                ) : (
                  <LineChart data={chartData} margin={{ top: 20, right: 20, bottom: 20, left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="year" stroke="#94a3b8" />
                    <YAxis stroke="#94a3b8" />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} />
                    <Legend />
                    <Line type="monotone" dataKey="Market Share (%)" stroke="#8B4513" strokeWidth={3.5} dot={{ r: 4 }} />
                    <Line type="monotone" dataKey="EV Penetration (%)" stroke="#DC2626" strokeWidth={3.5} dot={{ r: 4 }} />
                  </LineChart>
                )}
              </ResponsiveContainer>
            </div>
          ) : mainCategory === 'dep' ? (
            <div className="space-y-4">
              <div className="h-[380px]">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData} margin={{ top: 20, right: 20, bottom: 20, left: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="year" stroke="#94a3b8" />
                    <YAxis domain={depMetric === 'vote' ? [0, 45] : ['auto', 'auto']} stroke="#94a3b8" />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} />
                    <Legend />
                    {depMetric === 'vote' && (
                      <ReferenceLine y={25} stroke="#ef4444" strokeDasharray="4 4" label={{ value: '25% Veto Threshold', fill: '#fda4af', fontSize: 11 }} />
                    )}
                    <Line type="monotone" dataKey="Volkswagen" stroke="#00439C" strokeWidth={3.5} dot={{ r: 5 }} />
                    <Line type="monotone" dataKey="Mercedes-Benz" stroke="#94A3B8" strokeWidth={3.5} dot={{ r: 5 }} />
                    <Line type="monotone" dataKey="BMW Group" stroke="#FFFFFF" strokeWidth={3.5} dot={{ r: 5, fill: '#FFFFFF', stroke: '#cbd5e1', strokeWidth: 1.5 }} />
                    <Line type="monotone" dataKey="Triad Composite Avg" stroke="#F43F5E" strokeWidth={4} dot={{ r: 6 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {depMetric === 'vote' && (
                <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-xl text-xs text-slate-300 space-y-1">
                  <div className="font-bold text-rose-300 flex items-center gap-1.5">
                    <ShieldAlert className="w-4 h-4 text-rose-400" />
                    Chinese Equity &amp; Effective AGM Voting Power (%)
                  </div>
                  <div>• <strong>Mercedes-Benz (Top 35.8% ➔ 37.5%):</strong> Geely (9.69%) + BAIC (9.98%) = 19.67% stake commands 37.5% effective voting power at 52–55% AGM turnout, <strong>exceeding the German AktG §179 25% blocking minority threshold</strong>.</div>
                  <div>• <strong>Volkswagen &amp; BMW (Bottom 0.0%):</strong> Parent equity is 0%, but local joint ventures create operational asset lock-in.</div>
                  <div>• <strong>Triad Group Average (Middle 11.9% ➔ 12.5%):</strong> Aggregate parent weighting across the 3 German OEMs.</div>
                </div>
              )}
            </div>
          ) : radarMode === 'overlay' ? (
            <div className="h-[420px] rounded-xl p-2" style={{ backgroundColor: 'rgba(170, 68, 0, 0.35)', border: '1px solid #AA4400' }}>
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                  <PolarGrid stroke="#FDA4AF" strokeOpacity={0.3} />
                  <PolarAngleAxis dataKey="subject" stroke="#F8FAFC" fontSize={11} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#FED7AA" />
                  <Radar name="Volkswagen Group (VW Deep Blue)" dataKey="Volkswagen Group" stroke="#00439C" fill="#00439C" fillOpacity={0.45} strokeWidth={2.5} />
                  <Radar name="Mercedes-Benz (Silver)" dataKey="Mercedes-Benz" stroke="#94A3B8" fill="#94A3B8" fillOpacity={0.35} strokeWidth={2.5} />
                  <Radar name="BMW Group (BMW White)" dataKey="BMW Group" stroke="#FFFFFF" fill="#FFFFFF" fillOpacity={0.35} strokeWidth={2.5} />
                  <Radar name="Triad Benchmark (Red)" dataKey="Triad Benchmark" stroke="#F43F5E" strokeWidth={3} strokeDasharray="4 4" fill="none" />
                  <Legend />
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-3 rounded-xl border border-blue-950 text-center" style={{ backgroundColor: '#000000' }}>
                <h4 className="text-xs font-bold text-blue-400 mb-1">Volkswagen Group (Black Background)</h4>
                <div className="h-[260px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={radarData} outerRadius="75%">
                      <PolarGrid stroke="#334155" />
                      <PolarAngleAxis dataKey="subject" stroke="#64748b" fontSize={9} />
                      <Radar name="Volkswagen Group" dataKey="Volkswagen Group" stroke="#00439C" fill="#00439C" fillOpacity={0.45} strokeWidth={2} />
                      <Radar name="Triad Benchmark" dataKey="Triad Benchmark" stroke="#F43F5E" strokeWidth={1.5} strokeDasharray="3 3" fill="none" />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="p-3 rounded-xl border border-rose-900 text-center" style={{ backgroundColor: 'rgba(185, 28, 28, 0.35)' }}>
                <h4 className="text-xs font-bold text-rose-300 mb-1">Mercedes-Benz (Red Background)</h4>
                <div className="h-[260px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={radarData} outerRadius="75%">
                      <PolarGrid stroke="#881337" />
                      <PolarAngleAxis dataKey="subject" stroke="#FDA4AF" fontSize={9} />
                      <Radar name="Mercedes-Benz" dataKey="Mercedes-Benz" stroke="#94A3B8" fill="#94A3B8" fillOpacity={0.35} strokeWidth={2} />
                      <Radar name="Triad Benchmark" dataKey="Triad Benchmark" stroke="#FFFFFF" strokeWidth={1.5} strokeDasharray="3 3" fill="none" />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="p-3 rounded-xl border border-amber-900 text-center" style={{ backgroundColor: 'rgba(202, 138, 4, 0.35)' }}>
                <h4 className="text-xs font-bold text-yellow-300 mb-1">BMW Group (Yellow Background)</h4>
                <div className="h-[260px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={radarData} outerRadius="75%">
                      <PolarGrid stroke="#A16207" />
                      <PolarAngleAxis dataKey="subject" stroke="#FDE047" fontSize={9} />
                      <Radar name="BMW Group" dataKey="BMW Group" stroke="#FFFFFF" fill="#FFFFFF" fillOpacity={0.35} strokeWidth={2} />
                      <Radar name="Triad Benchmark" dataKey="Triad Benchmark" stroke="#F43F5E" strokeWidth={1.5} strokeDasharray="3 3" fill="none" />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* 3 Red Threat Metric Alerts */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2">
          <div className="p-3.5 rounded-xl bg-rose-950/60 border border-rose-800 text-xs text-rose-200">
            📉 <strong>Deliveries Collapse (Critical):</strong> 5.65M units ➔ 4.06M units (<span className="font-bold text-rose-300">-1.59M units / -28.1%</span>)
          </div>
          <div className="p-3.5 rounded-xl bg-rose-950/60 border border-rose-800 text-xs text-rose-200">
            📉 <strong>Market Share Halved (Critical):</strong> 25.1% ➔ 12.8% (<span className="font-bold text-rose-300">-12.3%p share erosion</span>)
          </div>
          <div className="p-3.5 rounded-xl bg-rose-950/60 border border-rose-800 text-xs text-rose-200">
            📉 <strong>China EBIT Collapse (Critical):</strong> €15.2B ➔ €7.9B (<span className="font-bold text-rose-300">-48.0% profit halved</span>)
          </div>
        </div>
      </div>

      {/* COMPREHENSIVE 2019-2025 FULL TIME-SERIES TABLE (VALUE-BASED DYNAMIC HEATMAP) */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-4">
        <div className="border-b border-slate-800 pb-3">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Activity className="w-4 h-4 text-sky-400" />
            2019–2025 Continuous Time-Series Comprehensive Audit Matrix
          </h3>
          <p className="text-xs text-slate-400">
            🎨 <strong>Value-Based Dynamic Heatmap</strong>: Benchmark mapped per 7-year mean. Safe metrics render in <span className="text-blue-400 font-bold">🟦 Blue</span>, midpoints in <span className="text-white font-bold">⬜ White</span>, and threats in <span className="text-rose-400 font-bold">🟥 Deep Red</span>.
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-right text-xs border-collapse font-mono">
            <thead>
              <tr className="border-b-2 border-slate-700 bg-slate-950 text-slate-400 text-center">
                <th className="p-3 text-left font-sans font-bold min-w-[190px] text-white">Metric Description</th>
                <th className="p-2.5 text-slate-300">2019</th>
                <th className="p-2.5 text-slate-300">2020</th>
                <th className="p-2.5 text-slate-300">2021</th>
                <th className="p-2.5 text-slate-300">2022</th>
                <th className="p-2.5 text-slate-300">2023</th>
                <th className="p-2.5 text-slate-300">2024</th>
                <th className="p-2.5 text-slate-300">2025</th>
                <th className="p-2.5 bg-slate-950 text-center text-slate-200">2019–2025 Delta</th>
                <th className="p-2.5 bg-slate-950 text-center text-slate-200">Risk Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {(() => {
                const computeStyle = (val: number, valList: number[], higherIsBetter: boolean) => {
                  const avg = valList.reduce((a, b) => a + b, 0) / valList.length;
                  const minV = Math.min(...valList);
                  const maxV = Math.max(...valList);
                  if (maxV === minV) return { backgroundColor: '#FFFFFF', color: '#0F172A', fontWeight: 'bold' };

                  let t = 0;
                  if (higherIsBetter) {
                    t = val >= avg 
                      ? (maxV > avg ? (val - avg) / (maxV - avg) : 0) 
                      : (avg > minV ? -(avg - val) / (avg - minV) : 0);
                  } else {
                    t = val <= avg 
                      ? (avg > minV ? (avg - val) / (avg - minV) : 0) 
                      : (maxV > avg ? -(val - avg) / (maxV - avg) : 0);
                  }

                  if (t > 0) {
                    const r = Math.round(255 - t * (255 - 30));
                    const g = Math.round(255 - t * (255 - 64));
                    const b = Math.round(255 - t * (255 - 175));
                    return { backgroundColor: `rgb(${r}, ${g}, ${b})`, color: t > 0.45 ? '#FFFFFF' : '#0F172A', fontWeight: t > 0.6 ? 800 : 700, border: Math.abs(t) < 0.15 ? '2px solid #94A3B8' : '1px solid rgba(0,0,0,0.1)' };
                  } else if (t < 0) {
                    const s = Math.abs(t);
                    const r = Math.round(255 - s * (255 - 190));
                    const g = Math.round(255 - s * (255 - 18));
                    const b = Math.round(255 - s * (255 - 60));
                    return { backgroundColor: `rgb(${r}, ${g}, ${b})`, color: s > 0.45 ? '#FFFFFF' : '#881337', fontWeight: s > 0.6 ? 800 : 700, border: Math.abs(t) < 0.15 ? '2px solid #94A3B8' : '1px solid rgba(0,0,0,0.1)' };
                  } else {
                    return { backgroundColor: '#FFFFFF', color: '#0F172A', fontWeight: 900, border: '2px solid #94A3B8' };
                  }
                };

                const dataRows = [
                  { section: '📈 1. Basic Market Performance (2019–2025)' },
                  { name: '• Volkswagen China Deliveries (k units)', vals: [4233, 3850, 3300, 3180, 3236, 2980, 2780], disp: ['4,233', '3,850', '3,300', '3,180', '3,236', '2,980', '2,780'], hib: true, delta: '-1,453 (-34.3%)', badge: '🔴 Severe Plunge', bCls: 'bg-rose-950 text-rose-300 border-rose-800' },
                  { name: '• Mercedes-Benz China Deliveries (k units)', vals: [693, 774, 758, 751, 737, 675, 630], disp: ['693', '774', '758', '751', '737', '675', '630'], hib: true, delta: '-63 (-9.1%)', badge: '🟠 Margin Hostage', bCls: 'bg-amber-950 text-amber-300 border-amber-800' },
                  { name: '• BMW Group China Deliveries (k units)', vals: [724, 777, 846, 792, 825, 705, 650], disp: ['724', '777', '846', '792', '825', '705', '650'], hib: true, delta: '-74 (-10.2%)', badge: '🟠 Share Encroached', bCls: 'bg-amber-950 text-amber-300 border-amber-800' },
                  { name: '• Triad Composite Deliveries (k units)', vals: [5650, 5401, 4904, 4723, 4798, 4360, 4060], disp: ['5,650', '5,401', '4,904', '4,723', '4,798', '4,360', '4,060'], hib: true, delta: '-1,590 (-28.1%)', badge: '🔴 Severe Plunge', bCls: 'bg-rose-950 text-rose-300 border-rose-800' },
                  { name: '• Triad China Local Production (k units)', vals: [5055, 4824, 4370, 4260, 4323, 3915, 3620], disp: ['5,055', '4,824', '4,370', '4,260', '4,323', '3,915', '3,620'], hib: true, delta: '-1,435 (-28.4%)', badge: '🔴 Asset Sunk', bCls: 'bg-rose-950 text-rose-300 border-rose-800' },
                  { name: '• Local Production Share (%)', vals: [89.5, 89.3, 89.1, 90.2, 90.1, 89.8, 89.2], disp: ['89.5%', '89.3%', '89.1%', '90.2%', '90.1%', '89.8%', '89.2%'], hib: false, delta: '-0.3%p (90% Lock-in)', badge: '🔴 Exit Constrained', bCls: 'bg-rose-950 text-rose-300 border-rose-800' },
                  { name: '• Triad China Market Share (%)', vals: [25.1, 24.5, 21.5, 19.8, 18.2, 15.1, 12.8], disp: ['25.1%', '24.5%', '21.5%', '19.8%', '18.2%', '15.1%', '12.8%'], hib: true, delta: '-12.3%p (Halved)', badge: '🔴 Share Collapse', bCls: 'bg-rose-950 text-rose-300 border-rose-800' },
                  { name: '• China NEV Penetration Rate (%)', vals: [4.9, 5.8, 15.5, 27.8, 35.7, 47.5, 53.5], disp: ['4.9%', '5.8%', '15.5%', '27.8%', '35.7%', '47.5%', '53.5%'], hib: false, delta: '+48.6%p (Surge)', badge: '🔴 ICE Displaced', bCls: 'bg-rose-950 text-rose-300 border-rose-800' },
                  { section: '📐 2. 6 Measurable Dependency Time-Series (2019–2025)' },
                  { name: '1. China EBIT Share (%)', vals: [37.8, 39.2, 40.8, 37.6, 35.2, 33.5, 32.7], disp: ['37.8%', '39.2%', '40.8%', '37.6%', '35.2%', '33.5%', '32.7%'], hib: false, delta: '-5.1%p (-€7.3B Halved)', badge: '🔴 Margin Hostage', bCls: 'bg-rose-950 text-rose-300 border-rose-800' },
                  { name: '2. Chinese Component BOM Cost (%)', vals: [32.0, 36.5, 40.2, 44.5, 47.0, 48.8, 49.5], disp: ['32.0%', '36.5%', '40.2%', '44.5%', '47.0%', '48.8%', '49.5%'], hib: false, delta: '+17.5%p (Surge)', badge: '🔴 BOM Dependent', bCls: 'bg-rose-950 text-rose-300 border-rose-800' },
                  { name: '3. Chinese Supplier Concentration (CR3 %)', vals: [45.0, 52.0, 61.5, 68.0, 72.0, 74.2, 75.5], disp: ['45.0%', '52.0%', '61.5%', '68.0%', '72.0%', '74.2%', '75.5%'], hib: false, delta: '+30.5%p (Monopoly)', badge: '🔴 Supply Captive', bCls: 'bg-rose-950 text-rose-300 border-rose-800' },
                  { name: '4. Local Data Isolation Ratio (%)', vals: [25.0, 45.0, 85.0, 95.0, 100.0, 100.0, 100.0], disp: ['25.0%', '45.0%', '85.0%', '95.0%', '100.0%', '100.0%', '100.0%'], hib: false, delta: '+75.0%p (0% Exfil)', badge: '🔴 Data Blockade', bCls: 'bg-rose-950 text-rose-300 border-rose-800' },
                  { name: '5. Chinese Equity & Effective Voting Power (%)', vals: [11.9, 12.1, 12.2, 12.3, 12.4, 12.5, 12.5], disp: ['11.9%', '12.1%', '12.2%', '12.3%', '12.4%', '12.5%', '12.5%'], hib: false, delta: '+0.6%p (MB 37.5%)', badge: '🔴 Veto Captured', bCls: 'bg-rose-950 text-rose-300 border-rose-800' },
                  { name: '6. Non-China Replacement Lead Time (Years)', vals: [1.5, 2.0, 2.7, 3.2, 3.7, 4.0, 4.2], disp: ['1.5 yrs', '2.0 yrs', '2.7 yrs', '3.2 yrs', '3.7 yrs', '4.0 yrs', '4.2 yrs'], hib: false, delta: '+2.7 yrs (50 mos)', badge: '🔴 Irreplaceable', bCls: 'bg-rose-950 text-rose-300 border-rose-800' },
                ];

                return dataRows.map((r, idx) => {
                  if (r.section) {
                    return (
                      <tr key={idx} className="bg-slate-950/70 text-left font-bold text-sky-400 font-sans">
                        <td colSpan={10} className="p-2.5">{r.section}</td>
                      </tr>
                    );
                  }
                  return (
                    <tr key={idx}>
                      <td className="p-2.5 text-left font-sans text-white">{r.name}</td>
                      {r.vals!.map((v, i) => {
                        const style = computeStyle(v, r.vals!, r.hib!);
                        return (
                          <td key={i} className="p-2.5" style={style}>
                            {r.disp![i]}
                          </td>
                        );
                      })}
                      <td className="p-2.5 text-center text-rose-300 font-bold bg-slate-950">{r.delta}</td>
                      <td className="p-2.5 text-center bg-slate-950">
                        <span className={`px-2 py-0.5 rounded border text-[10px] font-bold ${r.bCls}`}>{r.badge}</span>
                      </td>
                    </tr>
                  );
                });
              })()}
            </tbody>
          </table>
        </div>
      </div>

      {/* 6 MEASURABLE DEPENDENCY DIMENSIONS MATRIX TABLE (RED HIGH-SEVERITY THEME) */}
      <div className="bg-slate-900/90 border border-rose-900/80 rounded-2xl p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-rose-950 pb-3">
          <div>
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Layers className="w-4 h-4 text-rose-400" />
              Triad 6-Dimension Quantitative Dependency Matrix (2025 Audit Baseline)
            </h3>
            <p className="text-xs text-slate-400">Statutory audit matrix parameterizing 6 core dimensions under critical threat thematic styling.</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-rose-900/60 text-slate-400 bg-slate-950/80">
                <th className="p-3 font-bold w-[22%]">Dimension</th>
                <th className="p-3 font-bold text-slate-300 w-[20%]">Mercedes-Benz Group</th>
                <th className="p-3 font-bold text-sky-400 w-[20%]">Volkswagen Group</th>
                <th className="p-3 font-bold text-white w-[20%]">BMW Group</th>
                <th className="p-3 font-bold text-rose-300 w-[18%]">Triad Composite Avg</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-rose-950/60 text-slate-300">
              <tr className="bg-slate-950/40">
                <td className="p-3 font-bold text-white">1. China EBIT Share</td>
                <td className="p-3 text-rose-200 bg-rose-950/30">31.5% (€2.40B Dependent / S-Class Concentration)</td>
                <td className="p-3 text-rose-200 bg-rose-950/50">38.0% (JV Equity Method Earnings Concentration)</td>
                <td className="p-3 text-amber-200 bg-amber-950/30">28.5% (Shenyang BBA Operating Concentration)</td>
                <td className="p-3 font-bold text-rose-300 bg-rose-950/70">32.7% (Persistent Lock-in vs 41.0% Peak)</td>
              </tr>
              <tr className="bg-slate-950/40">
                <td className="p-3 font-bold text-white">2. Chinese Component BOM Cost</td>
                <td className="p-3 text-amber-200 bg-amber-950/30">42.0% (CATL Cells + Local Electrics)</td>
                <td className="p-3 text-rose-200 bg-rose-950/70 font-bold">58.5% (92.8% Domestic Sourced in Chinese Fabs)</td>
                <td className="p-3 text-amber-200 bg-amber-950/40">48.0% (Shenyang iX3 &amp; CATL Battery Packs)</td>
                <td className="p-3 font-bold text-rose-300 bg-rose-950/70">49.5% (Surged from 32% in 2019 to 49.5%)</td>
              </tr>
              <tr className="bg-slate-950/40">
                <td className="p-3 font-bold text-white">3. Chinese Supplier Concentration (CR3)</td>
                <td className="p-3 text-rose-200 bg-rose-950/40">68.0% (CATL, Momenta, BAIC Electronics)</td>
                <td className="p-3 text-rose-200 bg-rose-950/60">76.5% (CATL, Gotion, XPENG, SAIC)</td>
                <td className="p-3 text-rose-200 bg-rose-950/80 font-bold">82.0% (CATL &amp; EVE Energy Duopoly)</td>
                <td className="p-3 font-bold text-rose-300 bg-rose-950/70">75.5% (Concentration expanded from 45% in 2019)</td>
              </tr>
              <tr className="bg-slate-950/40">
                <td className="p-3 font-bold text-white">4. Local Data Isolation Ratio</td>
                <td className="p-3 text-rose-200 bg-rose-950/70">100.0% (DSL Statutory Local Air-gap)</td>
                <td className="p-3 text-rose-200 bg-rose-950/70">100.0% (Hefei VCTC Cloud Isolation)</td>
                <td className="p-3 text-rose-200 bg-rose-950/70">100.0% (Shenyang Server 100% Retained)</td>
                <td className="p-3 font-bold text-rose-300 bg-rose-950/80">100.0% (0% Outbound Telemetry Allowed under DSL)</td>
              </tr>
              <tr className="bg-slate-950/40">
                <td className="p-3 font-bold text-white">5. Chinese Equity &amp; Effective Voting Power</td>
                <td className="p-3 text-rose-200 bg-rose-950/80 font-bold">19.67% Stake / 37.5% AGM Effective Veto (1st &amp; 2nd Largest Shareholder)</td>
                <td className="p-3 text-slate-400 bg-slate-950/50">0% Parent Equity / JV Operational Lock-in</td>
                <td className="p-3 text-amber-200 bg-amber-950/30">0% Parent Equity / €3.73B Sunk BBA 75% Stake</td>
                <td className="p-3 font-bold text-rose-300 bg-rose-950/70">12.5% Parent Average (Mercedes Concentration)</td>
              </tr>
              <tr className="bg-slate-950/40">
                <td className="p-3 font-bold text-white">6. Non-China Replacement Lead Time</td>
                <td className="p-3 text-rose-200 bg-rose-950/50">36 to 48 Months (3–4 Years)</td>
                <td className="p-3 text-rose-200 bg-rose-950/70 font-bold">48 to 60 Months (4–5 Years)</td>
                <td className="p-3 text-rose-200 bg-rose-950/60">42 to 54 Months (3.5–4.5 Years)</td>
                <td className="p-3 font-bold text-rose-300 bg-rose-950/80">4.2 Years (Protracted Rebalancing Lead Time)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
