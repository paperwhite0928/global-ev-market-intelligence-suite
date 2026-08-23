import React from 'react';
import { Landmark, Scale, Network } from 'lucide-react';
import { STATE_CAPITALISM_MECHANISMS } from '../data/autoTriadData';

export const Tab3StateCapitalism: React.FC = () => {
  const pillars = STATE_CAPITALISM_MECHANISMS.sixEvidencePillars;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Top Hero Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-950/60 border border-rose-800/50 text-rose-300 text-xs font-mono font-bold">
            <Landmark className="w-3.5 h-3.5" />
            STATE-CORPORATE CO-OPTIMIZATION &amp; 6 EVIDENCE PILLARS
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            Chinese State Capitalism Institutional Architecture: The Corporate Objective Function
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            Corporate strategy in state capitalism is not irrational price dumping, but a <strong>multi-variable optimization system where commercial profits are weighted alongside national strategic priorities (market dominance, technology assimilation, supply chain capture)</strong>.
          </p>
        </div>
      </div>

      {/* Theoretical Model Callout */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-950 to-blue-950/40 border border-slate-800 space-y-3">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
          <h3 className="text-sm font-bold text-sky-400 font-mono uppercase tracking-wider flex items-center gap-2">
            <Scale className="w-4 h-4 text-sky-400" />
            Corporate Objective Function Comparison
          </h3>
          <span className="text-xs font-mono px-2.5 py-0.5 rounded bg-slate-800 text-slate-300">Economic Model</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1.5">
            <span className="font-bold text-blue-400 block font-mono">Western Free-Market Objective:</span>
            <div className="p-2.5 rounded bg-slate-900 text-sky-300 font-mono font-bold text-xs border border-slate-800">
              max Profit(t) = Revenue(t) - Cost(t)
            </div>
            <p className="text-slate-400 text-[11px] leading-relaxed">
              Subordinated to quarterly shareholder return on equity (ROE) and operating margin (EBIT) maximization.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1.5">
            <span className="font-bold text-rose-400 block font-mono">Chinese State Capitalism Objective:</span>
            <div className="p-2.5 rounded bg-slate-900 text-rose-300 font-mono font-bold text-xs border border-slate-800">
              max Utility = Profit(firm) + &lambda; &middot; Strategic_Objective(state)
            </div>
            <p className="text-slate-400 text-[11px] leading-relaxed">
              Subsidized by state policy finance, absorbing near-term losses to secure global monopoly scale (&lambda; weight).
            </p>
          </div>
        </div>
      </div>

      {/* 6 Institutional Evidence Pillars Grid */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold text-slate-200 uppercase font-mono tracking-wider flex items-center gap-2">
          <Network className="w-4 h-4 text-amber-400" />
          6 Institutional Evidence Pillars of State-Corporate Integration
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {pillars.map((p, idx) => (
            <div
              key={p.id}
              className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-3 hover:border-slate-700 transition flex flex-col justify-between"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-amber-300 border border-slate-700">
                    PILLAR 0{idx + 1}
                  </span>
                </div>
                <h4 className="text-sm font-bold text-white leading-snug">{p.name}</h4>
                <div className="text-[11px] font-mono text-sky-400 font-semibold bg-slate-950/80 p-2 rounded border border-slate-800/80">
                  &sect; {p.legalBasis}
                </div>
                <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/50 p-3 rounded-lg border border-slate-800/60">
                  {p.mechanism}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
