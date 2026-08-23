import React from 'react';
import { Layers, Split, Lock, ShieldAlert, DollarSign, Database, CheckCircle2, AlertOctagon } from 'lucide-react';

export const Tab3LockinDualTrack: React.FC = () => {
  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Top Hero Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-950/60 border border-purple-800/50 text-purple-300 text-xs font-mono font-bold">
            <Layers className="w-3.5 h-3.5" />
            THE STRUCTURAL REALITY: WHY COMPLETE DECOUPLING IS IMPOSSIBLE
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            The Lock-In Dilemma &amp; The "In China for China" Dual-Track Architecture
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            European political leaders frequently call for rapid industrial decoupling from China. However, for the German Auto Triad, sudden decoupling represents immediate financial insolvency. Below is the economic reality and the pragmatic dual-track architecture currently being deployed.
          </p>
        </div>
      </div>

      {/* 3 Reasons Why Immediate Decoupling is Impossible */}
      <div>
        <h3 className="text-sm font-bold text-slate-200 uppercase font-mono tracking-wider mb-4 flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-rose-400" />
          The 3 Pillars of Irreversible Structural Lock-In
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="p-2 rounded-lg bg-rose-950 text-rose-400 border border-rose-800/60">
                <DollarSign className="w-4 h-4" />
              </span>
              <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800 font-bold">
                Pillar 1
              </span>
            </div>
            <h4 className="text-base font-bold text-white">1. Sunk CapEx in Mega-Fabs</h4>
            <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/70 p-3 rounded-xl border border-slate-800">
              The Triad has sunk over <strong>€45 Billion in cumulative manufacturing capital</strong> across Shenyang (BMW), Anting/Hefei (VW), and Beijing (Mercedes). Writing off these state-of-the-art facilities would trigger catastrophic balance-sheet impairment charges.
            </p>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="p-2 rounded-lg bg-amber-950 text-amber-400 border border-amber-800/60">
                <Layers className="w-4 h-4" />
              </span>
              <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800 font-bold">
                Pillar 2
              </span>
            </div>
            <h4 className="text-base font-bold text-white">2. Cash-Flow Funding for R&amp;D</h4>
            <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/70 p-3 rounded-xl border border-slate-800">
              Chinese joint ventures generated <strong>€10B–€14B in annual dividends and licensing fees</strong> that funded the German OEMs' entire global transition toward SDVs, autonomous driving, and solid-state battery R&amp;D.
            </p>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="p-2 rounded-lg bg-teal-950 text-teal-400 border border-teal-800/60">
                <Database className="w-4 h-4" />
              </span>
              <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-teal-950 text-teal-300 border border-teal-800 font-bold">
                Pillar 3
              </span>
            </div>
            <h4 className="text-base font-bold text-white">3. Cost Parity (+25% Gap)</h4>
            <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/70 p-3 rounded-xl border border-slate-800">
              Without access to the Chinese LFP battery supply chain and power electronics integration, pure EV manufacturing in Europe or North America is structurally <strong>20% to 30% more expensive per vehicle</strong>.
            </p>
          </div>
        </div>
      </div>

      {/* The "In China for China" Dual-Track Operating Model */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-5">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <div className="text-xs font-mono font-bold text-sky-400 uppercase tracking-wider">
              PRAGMATIC TRANSITIONAL DEFENSE ARCHITECTURE
            </div>
            <h3 className="text-lg font-black text-white mt-0.5">
              The "In China for China" Dual-Track &amp; Data Air-Gap Framework
            </h3>
          </div>
          <span className="text-xs font-mono px-3 py-1 rounded bg-blue-950 text-blue-300 border border-blue-800 font-bold">
            BIFURCATED R&amp;D
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Left Track: In China for China */}
          <div className="p-4 rounded-xl bg-slate-950/90 border border-rose-900/50 space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-bold text-rose-400 flex items-center gap-2">
                <Split className="w-4 h-4" /> TRACK A: DOMESTIC CHINESE FLEET
              </h4>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">
                100% LOCALIZED
              </span>
            </div>
            <div className="text-xs font-bold text-slate-200">100% Localized Ecosystem (Regulatory &amp; Supply Chain Compliance)</div>
            <ul className="space-y-2 text-xs text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-rose-400 font-mono font-bold">•</span>
                <span>XPENG CEA zonal E/E (VW) &amp; Momenta AD (Mercedes)</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-rose-400 font-mono font-bold">•</span>
                <span>Horizon Robotics &amp; Huawei silicon interfaces</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-rose-400 font-mono font-bold">•</span>
                <span>CATL &amp; EVE Energy domestic LFP battery cells</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-rose-400 font-mono font-bold">•</span>
                <span>Domestic cloud servers complying with PRC Intelligence Law Art. 7</span>
              </li>
            </ul>
          </div>

          {/* Right Track: Global Western Fleet */}
          <div className="p-4 rounded-xl bg-slate-950/90 border border-emerald-900/50 space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-bold text-emerald-400 flex items-center gap-2">
                <Lock className="w-4 h-4" /> TRACK B: WESTERN &amp; ALLIED GLOBAL FLEET
              </h4>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                SOVEREIGN AIR-GAP
              </span>
            </div>
            <div className="text-xs font-bold text-slate-200">Sovereign Cloud &amp; Allied Stack (Data Sovereignty &amp; Defense Compliance)</div>
            <ul className="space-y-2 text-xs text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 font-mono font-bold">•</span>
                <span>Rivian Open SDV (VW), MB.OS (Mercedes), Google AAOS</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 font-mono font-bold">•</span>
                <span>Qualcomm Snapdragon &amp; NVIDIA DRIVE compute platforms</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 font-mono font-bold">•</span>
                <span>CRMA/IRA-compliant allied cell suppliers (PowerCo, Panasonic, LG/Samsung/SK)</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 font-mono font-bold">•</span>
                <span>NATO-certified sovereign data air-gap (zero foreign peering)</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Data Air-Gap Callout */}
        <div className="p-3.5 rounded-xl bg-blue-950/40 border border-blue-800/40 text-xs text-slate-300 flex items-center gap-3">
          <Lock className="w-5 h-5 text-sky-400 flex-shrink-0" />
          <p className="leading-relaxed">
            <strong>The Hard Air-Gap Rule:</strong> No telemetry data, vehicle sensor streams, or customer driving profiles from Chinese domestic vehicles may cross into Western headquarters networks, ensuring compliance with both China's Data Security Law and European GDPR.
          </p>
        </div>
      </div>
    </div>
  );
};
