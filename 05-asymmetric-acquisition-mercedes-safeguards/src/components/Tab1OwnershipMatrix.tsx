import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { AlertCircle, ArrowUpRight, CheckCircle, HelpCircle, Shield, Users } from 'lucide-react';
import shareholderData from '../../data/shareholder_structure.json';

interface Tab1OwnershipMatrixProps {
  onOpenCollarModal: () => void;
}

export const Tab1OwnershipMatrix: React.FC<Tab1OwnershipMatrixProps> = ({ onOpenCollarModal }) => {
  const data = shareholderData.shareholders;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Top Banner Alert */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-rose-600/5 rounded-full blur-3xl pointer-events-none" />
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-950/60 border border-rose-800/50 text-rose-300 text-xs font-mono font-bold">
              <AlertCircle className="w-3.5 h-3.5" />
              FRAGMENTED FREE-FLOAT VS. CONCENTRATED CHINESE COALITION
            </div>
            <h2 className="text-2xl font-black text-white tracking-tight">
              The 19.67% Dual-Stake Reality in Mercedes-Benz Group AG
            </h2>
            <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
              Between 2018 and 2021, two distinct Chinese power centers—private tech giant <strong>Geely (9.69%)</strong> and Beijing municipal state-owned enterprise <strong>BAIC Group (9.98%)</strong>—amassed a combined 19.67% equity stake in Germany's crowning automotive flagship, creating an insurmountable de facto voting bloc.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={onOpenCollarModal}
              className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold shadow-lg shadow-rose-900/30 transition"
            >
              <span>Explore Geely Collar Engineering</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Grid: Donut Chart & Detailed Shareholder Profiles */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Shareholder Donut & AGM Dynamics */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-slate-200 uppercase font-mono tracking-wider">
                Ownership Distribution (% of Shares)
              </h3>
              <span className="text-xs font-mono text-slate-400">Total: 1,069.8M shares</span>
            </div>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    innerRadius={65}
                    outerRadius={95}
                    paddingAngle={3}
                    dataKey="stakePct"
                  >
                    {data.map((entry) => (
                      <Cell key={entry.id} fill={entry.color} stroke="#0f172a" strokeWidth={2} />
                    ))}
                  </Pie>
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        const d = payload[0].payload;
                        return (
                          <div className="bg-slate-950 border border-slate-700 p-3 rounded-lg shadow-xl text-xs">
                            <div className="font-bold text-white mb-1">{d.name}</div>
                            <div className="text-rose-400 font-mono">Stake: <strong>{d.stakePct}%</strong> ({d.sharesMillion}M shares)</div>
                            <div className="text-slate-400 mt-1">{d.type}</div>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Legend
                    verticalAlign="bottom"
                    layout="horizontal"
                    formatter={(value, entry: any) => (
                      <span className="text-[11px] text-slate-300 font-medium">
                        {value} ({entry.payload.stakePct}%)
                      </span>
                    )}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* AGM Effective Power Callout */}
            <div className="mt-4 p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 font-semibold flex items-center gap-1.5">
                  <Users className="w-3.5 h-3.5 text-sky-400" />
                  Average German AGM Attendance:
                </span>
                <span className="font-mono font-bold text-white">52.5%</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-rose-300 font-semibold flex items-center gap-1.5">
                  <Shield className="w-3.5 h-3.5 text-rose-400" />
                  Effective Chinese Voting Power:
                </span>
                <span className="font-mono font-black text-rose-400 text-sm">~37.47%</span>
              </div>
              <p className="text-[11px] text-slate-400 leading-normal pt-1 border-t border-slate-800">
                Because European institutional and retail shareholders frequently fail to attend or vote, a disciplined 19.67% bloc wields over <strong>37% of present votes</strong>, forming an unassailable blocking minority over supermajority (75%) resolutions.
              </p>
            </div>
          </div>
        </div>

        {/* Right Column: Key Shareholder Cards */}
        <div className="lg:col-span-7 space-y-4">
          <h3 className="text-sm font-bold text-slate-300 uppercase font-mono tracking-wider flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-sky-400" />
            Major Strategic &amp; Institutional Ownership Profiles
          </h3>

          <div className="space-y-3">
            {data.map((sh) => (
              <div
                key={sh.id}
                className={`p-4 rounded-xl border transition-all ${
                  sh.id === 'baic' || sh.id === 'geely'
                    ? 'bg-slate-900/90 border-rose-900/40 hover:border-rose-700/60 shadow-lg shadow-rose-950/20'
                    : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-2 mb-2.5">
                  <div className="flex items-center gap-2.5">
                    <span
                      className="w-3.5 h-3.5 rounded-full flex-shrink-0"
                      style={{ backgroundColor: sh.color }}
                    />
                    <span className="font-bold text-white text-sm">{sh.name}</span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                      {sh.type}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-slate-400">({sh.sharesMillion}M shares)</span>
                    <span
                      className="text-sm font-mono font-black px-2.5 py-0.5 rounded"
                      style={{
                        backgroundColor: `${sh.color}20`,
                        color: sh.color,
                        border: `1px solid ${sh.color}40`,
                      }}
                    >
                      {sh.stakePct}%
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5 text-xs text-slate-300">
                  <div>
                    <span className="text-[11px] font-semibold text-slate-400 block">Board Influence / Strategic Tie:</span>
                    <p className="mt-0.5 text-slate-200">{sh.boardInfluence}</p>
                  </div>
                  <div>
                    <span className="text-[11px] font-semibold text-slate-400 block">Acquisition Context:</span>
                    <p className="mt-0.5 text-slate-400">{sh.details}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
