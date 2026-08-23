import React from 'react';
import { Lock, Unlock, ShieldAlert, Landmark, Scale, CheckCircle2 } from 'lucide-react';
import idarData from '../../data/idar_asymmetric_strategy.json';

export const Tab3IdarStrategy: React.FC = () => {
  const { coreConcepts, inboundMechanisms, outboundLegalStatutes, executiveTakeaways } = idarData;

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* 1. Hero Header & Core Concepts */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden space-y-4">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-950/60 border border-rose-800/50 text-rose-300 text-xs font-mono font-bold">
            <Scale className="w-3.5 h-3.5" />
            STATE-LED MERCANTILISM &amp; ASYMMETRIC OPENNESS FRAMEWORK
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            China's Asymmetric Openness &amp; IDAR (Introduce, Digest, Absorb, Re-innovate) Strategy Framework
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            Illustrates the structural weaponization of systemic asymmetry: leveraging Western capital and market openness to absorb foreign technologies (3 Inbound Mechanisms), followed by statutorily ring-fencing domestic IP and critical resources behind national security laws (4 Outbound Statutes).
          </p>
        </div>

        {/* 2 Core Concepts Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <div className="flex items-center gap-2 text-rose-400 text-xs font-mono font-bold">
              <Landmark className="w-4 h-4" />
              1. State-Led Mercantilism &amp; State Capitalism
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              {coreConcepts.stateLedMercantilism.definition}
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
            <div className="flex items-center gap-2 text-amber-400 text-xs font-mono font-bold">
              <Unlock className="w-4 h-4" />
              2. Asymmetric Openness (One-Way Market Access)
            </div>
            <div className="text-xs font-mono font-bold text-amber-300">
              "{coreConcepts.asymmetricOpenness.slogan}"
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              {coreConcepts.asymmetricOpenness.mechanism}
            </p>
          </div>
        </div>

        {/* IDAR 3-Step Flow */}
        <div className="pt-2">
          <div className="text-xs font-mono font-bold text-sky-400 uppercase mb-2">IDAR 3-Phase Process:</div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {coreConcepts.idarStrategy.phases.map((phase, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <div className="flex items-center justify-between text-[11px] font-mono">
                  <span className="px-2 py-0.5 rounded bg-sky-950 text-sky-300 font-bold border border-sky-800/60">{phase.step}</span>
                  <span className="text-slate-500 font-bold">Phase 0{idx + 1}</span>
                </div>
                <h4 className="text-sm font-bold text-white pt-1">{phase.name}</h4>
                <p className="text-xs text-slate-400 leading-tight">{phase.detail}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 2. Inbound Absorption 3 Mechanisms */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-5">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Unlock className="w-4 h-4 text-blue-400" />
            📥 Inbound Absorption: 3 Core Assimilation Mechanisms &amp; Empirical Case Studies
          </h3>
          <span className="text-xs font-mono text-blue-400 font-bold px-2.5 py-0.5 rounded bg-blue-950 border border-blue-800">
            Inbound Absorption
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {inboundMechanisms.map((mech) => (
            <div key={mech.id} className="p-5 rounded-xl bg-slate-950/90 border border-slate-800 space-y-3 flex flex-col justify-between">
              <div className="space-y-2">
                <h4 className="text-sm font-bold text-white leading-snug">{mech.mechanism}</h4>
                <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/70 p-2.5 rounded-lg border border-slate-800">
                  {mech.method}
                </p>
                <div className="space-y-2 pt-1">
                  <span className="text-[10px] font-mono font-bold text-slate-400 uppercase">Empirical Case Studies:</span>
                  {mech.cases.map((c: any, cIdx: number) => (
                    <div key={cIdx} className="p-2.5 rounded-lg bg-slate-900/50 border border-slate-800/60 text-xs space-y-1">
                      <strong className="text-sky-400 block font-mono text-[11px]">
                        {c.sector ? `[${c.sector}] ${c.example}` : c.company ? `[M&A] ${c.company} (${c.buyer})` : `[Policy] ${c.policy}`}
                      </strong>
                      <p className="text-slate-400 text-[11px] leading-tight">{c.result || c.impact}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 3. Outbound Containment 4 Legal Statutes */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-5">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Lock className="w-4 h-4 text-purple-400" />
            🔒 Outbound Lockdown: 4 Legal Statutes Blocking Critical IP &amp; Asset Repatriation
          </h3>
          <span className="text-xs font-mono text-purple-400 font-bold px-2.5 py-0.5 rounded bg-purple-950 border border-purple-800">
            Outbound Containment
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {outboundLegalStatutes.map((stat) => (
            <div key={stat.id} className="p-4 rounded-xl bg-slate-950/90 border border-slate-800 space-y-2.5">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="text-white font-bold text-xs">{stat.name}</span>
                <span className="px-2 py-0.5 rounded bg-purple-950 text-purple-300 font-bold border border-purple-800 text-[10px]">
                  {stat.enactment}
                </span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-2 rounded border border-slate-800">
                {stat.coreContent}
              </p>
              <div className="space-y-1 pt-1">
                <span className="text-[10px] font-mono font-bold text-slate-400 uppercase">Controlled Categories:</span>
                {stat.restrictedTech.map((item, iIdx) => (
                  <div key={iIdx} className="text-xs bg-slate-900/40 p-1.5 rounded border border-slate-800/40 space-y-0.5">
                    <strong className="text-rose-400 font-mono text-[11px]">• {item.item}:</strong>
                    <p className="text-[11px] text-slate-400 leading-tight">{item.detail}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 4. Executive Takeaways */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-5 rounded-2xl bg-gradient-to-br from-rose-950/40 to-slate-900 border border-rose-800/60 space-y-2">
          <div className="flex items-center gap-2 text-rose-400 font-mono text-xs font-bold">
            <ShieldAlert className="w-4 h-4" />
            Takeaway 1: Systemic Asymmetry as a Geopolitical Weapon
          </div>
          <h4 className="text-base font-bold text-white">{executiveTakeaways.systemicWeaponization.title}</h4>
          <p className="text-xs text-slate-200 leading-relaxed">
            {executiveTakeaways.systemicWeaponization.explanation}
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-gradient-to-br from-emerald-950/40 to-slate-900 border border-emerald-800/60 space-y-2">
          <div className="flex items-center gap-2 text-emerald-400 font-mono text-xs font-bold">
            <CheckCircle2 className="w-4 h-4" />
            Takeaway 2: The Structural Imperative for Western De-risking
          </div>
          <h4 className="text-base font-bold text-white">{executiveTakeaways.deriskingRootCause.title}</h4>
          <p className="text-xs text-slate-200 leading-relaxed">
            {executiveTakeaways.deriskingRootCause.explanation}
          </p>
        </div>
      </div>
    </div>
  );
};
