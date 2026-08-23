import React, { useState } from 'react';
import { ShieldCheck, Sliders, CheckCircle2 } from 'lucide-react';
import { CAPITAL_DEFENSE_STEPS } from '../data/autoTriadData';

export const Tab4CapitalSandbox: React.FC = () => {
  const [dilutionPct, setDilutionPct] = useState<number>(15);
  const [alliedTurnout, setAlliedTurnout] = useState<number>(85);
  const [floatTurnout, setFloatTurnout] = useState<number>(38);

  // Exact Disaggregated German AktG §179 Mathematical Model
  const S_cn_0 = 19.67;
  const S_allied_0 = 35.0;
  const S_float_0 = 45.33;

  const S_cn = S_cn_0 / (1.0 + (dilutionPct / 100.0));
  const S_allied = (S_allied_0 + dilutionPct) / (1.0 + (dilutionPct / 100.0));
  const S_float = S_float_0 / (1.0 + (dilutionPct / 100.0));

  const T_cn = 1.0; // Chinese state block votes 100%
  const T_allied = alliedTurnout / 100.0;
  const T_float = floatTurnout / 100.0;

  const totalRepresentedCapital = (S_cn * T_cn) + (S_allied * T_allied) + (S_float * T_float);
  const effectiveChineseAgmPower = (S_cn * T_cn / totalRepresentedCapital) * 100.0;
  const effectiveAlliedAgmPower = (S_allied * T_allied / totalRepresentedCapital) * 100.0;

  // Exact unrounded blocking minority check (< 25.0%)
  const hasBlockingMinority = (S_cn * T_cn / totalRepresentedCapital) >= 0.2500000;

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-950/60 border border-emerald-800/50 text-emerald-300 text-xs font-mono font-bold">
            <ShieldCheck className="w-3.5 h-3.5" />
            GERMAN AKTG §179 GOVERNANCE &amp; CAPITAL DEFENSE SANDBOX
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            Disaggregated Shareholder Turnout &amp; Dilution Engine
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            Statutory criteria to eliminate the <strong>25% supermajority blocking minority (Sperrminorität)</strong> under German Corporate Law (AktG §179): 
            ① <strong>Model A (Total AGM Attendance)</strong>: Achieving 70.0% total turnout reduces effective voting power to 24.43% (&lt;25.0%). 
            ② <strong>Model B (Disaggregated Weighted Multi-Class)</strong>: When Chinese turnout is 100% and retail is 38%, allied-only turnout of 85.0%+ drives total attendance to 69.04%, achieving an effective voting share of 24.77% (&lt;25.0%).
          </p>
        </div>
      </div>

      {/* Interactive Sandbox Simulator */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Sliders className="w-4 h-4 text-emerald-400" />
            Interactive Governance &amp; Turnout Simulator
          </h3>
          <span className="text-xs font-mono px-2.5 py-0.5 rounded bg-slate-800 text-emerald-300 border border-slate-700">
            Disaggregated AktG §179 Engine
          </span>
        </div>

        {/* Sliders Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-slate-400">1. Strategic Capital Dilution:</span>
              <span className="text-amber-400 font-bold">+{dilutionPct}% New Shares</span>
            </div>
            <input
              type="range"
              min="0"
              max="45"
              step="5"
              value={dilutionPct}
              onChange={(e) => setDilutionPct(Number(e.target.value))}
              className="w-full accent-amber-500"
            />
            <p className="text-[11px] text-slate-500">Issued to European Sovereign Mobility Funds under §182 AktG.</p>
          </div>

          <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-slate-400">2. Allied-Only Turnout:</span>
              <span className="text-emerald-400 font-bold">{alliedTurnout}% (85%+ drives total 69%+)</span>
            </div>
            <input
              type="range"
              min="50"
              max="95"
              step="1"
              value={alliedTurnout}
              onChange={(e) => setAlliedTurnout(Number(e.target.value))}
              className="w-full accent-emerald-500"
            />
            <p className="text-[11px] text-slate-500">Allied-only turnout >=85% drives total turnout to 69.04% ➔ Effective voting power 24.77% (&lt;25.0%)</p>
          </div>

          <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800 space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-slate-400">3. Retail / Float Turnout:</span>
              <span className="text-sky-400 font-bold">{floatTurnout}% Participation</span>
            </div>
            <input
              type="range"
              min="20"
              max="60"
              step="2"
              value={floatTurnout}
              onChange={(e) => setFloatTurnout(Number(e.target.value))}
              className="w-full accent-sky-500"
            />
            <p className="text-[11px] text-slate-500">Public retail shareholder turnout at German AGMs.</p>
          </div>
        </div>

        {/* Dynamic Simulation Outcome Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-center">
            <div className="text-xs font-mono text-slate-400 uppercase">Diluted Chinese Stake</div>
            <div className="text-2xl font-black text-rose-400 font-mono mt-1">{S_cn.toFixed(2)}%</div>
            <div className="text-[11px] text-slate-500">Diluted from 19.67% baseline (Geely 9.69% + BAIC 9.98%)</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-center">
            <div className="text-xs font-mono text-slate-400 uppercase">Effective Chinese AGM Power</div>
            <div className="text-2xl font-black text-amber-400 font-mono mt-1">{effectiveChineseAgmPower.toFixed(2)}%</div>
            <div className={`text-[11px] font-bold mt-0.5 ${hasBlockingMinority ? 'text-rose-400' : 'text-emerald-400'}`}>
              {hasBlockingMinority
                ? `⚠️ Blocking Minority Active (>=25.00% of represented votes)`
                : `✅ 25% Blocking Veto Broken (<25.00% of represented votes)`}
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-center">
            <div className="text-xs font-mono text-slate-400 uppercase">Allied Coalition AGM Power</div>
            <div className="text-2xl font-black text-emerald-400 font-mono mt-1">{effectiveAlliedAgmPower.toFixed(2)}%</div>
            <div className="text-[11px] text-emerald-400 font-bold">
              {effectiveAlliedAgmPower >= 50.0 ? '✅ Absolute Simple Majority (>50%)' : 'Coordinating Majority'}
            </div>
          </div>
        </div>
      </div>

      {/* 4 Detailed Strategy Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {CAPITAL_DEFENSE_STEPS.map((step) => (
          <div
            key={step.step}
            className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3 hover:border-slate-700 transition"
          >
            <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
              <span className="text-xs font-mono font-bold text-slate-400">STEP 0{step.step}</span>
              <span
                className="text-[10px] font-mono font-bold px-2 py-0.5 rounded"
                style={{
                  backgroundColor: `${step.color}20`,
                  color: step.color,
                  border: `1px solid ${step.color}40`,
                }}
              >
                {step.tag}
              </span>
            </div>

            <h4 className="text-base font-bold text-white">{step.title}</h4>
            <div className="text-xs font-mono text-emerald-400 font-semibold">{step.action}</div>

            <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/70 p-3 rounded-xl border border-slate-800">
              {step.mechanism}
            </p>

            <div className="text-[11px] text-slate-400 pt-1 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              <span><strong>Strategic Impact:</strong> {step.effectiveness}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
