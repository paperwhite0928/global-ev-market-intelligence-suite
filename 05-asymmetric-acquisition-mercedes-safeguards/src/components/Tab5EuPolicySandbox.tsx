import React, { useState } from 'react';
import { Landmark, AlertTriangle, ShieldCheck, FileCheck, CheckCircle2, Lock, Scale, Zap } from 'lucide-react';
import { EU_POLICY_REFORMS } from '../data/autoTriadData';

export const Tab5EuPolicySandbox: React.FC = () => {
  const [selectedReform, setSelectedReform] = useState<number>(0);

  const reforms = EU_POLICY_REFORMS;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-950/60 border border-amber-800/50 text-amber-300 text-xs font-mono font-bold">
            <Landmark className="w-3.5 h-3.5" />
            EU LEGISLATIVE REFORM &amp; INDUSTRIAL STRATEGY SANDBOX
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            Fixing Current EU Policy Flaws: The 3 Strategic Legislative Pillars
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            Simple countervailing anti-subsidy tariffs (21–35%) and reactive FDI screening fail to prevent synthetic equity takeovers and CKD component laundering. Europe requires an aggressive, proactive industrial and data border architecture.
          </p>
        </div>
      </div>

      {/* Grid: 4 Policy Cards (Current Flaws + 3 Reforms) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {reforms.map((item, idx) => (
          <div
            key={item.id}
            className={`p-5 rounded-2xl border transition flex flex-col justify-between ${
              idx === 0
                ? 'bg-slate-900/90 border-rose-900/50 hover:border-rose-700/60 shadow-lg shadow-rose-950/20'
                : 'bg-slate-900/90 border-slate-800 hover:border-slate-700'
            }`}
          >
            <div className="space-y-3">
              <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
                <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded ${item.badgeColor}`}>
                  {item.category}
                </span>
                <span className="text-xs font-mono text-slate-500 font-bold">PILLAR 0{idx}</span>
              </div>

              <h3 className="text-base font-bold text-white">{item.title}</h3>

              <ul className="space-y-2 text-xs text-slate-300">
                {item.points.map((pt, pIdx) => (
                  <li key={pIdx} className="bg-slate-950/70 p-3 rounded-xl border border-slate-800/80 flex items-start gap-2.5">
                    <span className={`font-mono font-bold ${idx === 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                      {pIdx + 1}.
                    </span>
                    <span className="leading-relaxed">{pt}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
              <span>{idx === 0 ? '⚠️ Systemic Regulatory Gap' : '✅ Proposed EU Directive Mandate'}</span>
              <span className="text-sky-400 font-mono font-bold">EU Commission Draft</span>
            </div>
          </div>
        ))}
      </div>

      {/* Comparison Sandbox: Status Quo Tariffs vs. Strategic Data Border Tax */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-blue-950/40 via-slate-900 to-purple-950/40 border border-blue-900/40 space-y-4">
        <h4 className="text-sm font-bold text-sky-300 uppercase font-mono tracking-wider flex items-center gap-2">
          <Zap className="w-4 h-4 text-sky-400" />
          The Strategic Advantage of a Data Border Tax over Simple Tariffs
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 space-y-1.5">
            <span className="text-rose-400 font-bold block">Why Countervailing Tariffs Fail:</span>
            <p className="text-slate-300 leading-relaxed">
              Foreign automakers build assembly plants in Eastern Europe (e.g. BYD in Hungary) to classify vehicles as EU-made, completely evading tariffs while keeping software, chips, and data routed through foreign servers.
            </p>
          </div>
          <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 space-y-1.5">
            <span className="text-emerald-400 font-bold block">Why the Data Border Tax Succeeds:</span>
            <p className="text-slate-300 leading-relaxed">
              Focuses on software architecture and telemetry. Any vehicle whose operating system is legally bound to foreign intelligence laws (PRC Art. 7) is barred from European roads or taxed punitively regardless of where the metal chassis was assembled.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
