import React from 'react';
import { Building2, ShieldAlert } from 'lucide-react';
import triadOems from '../../data/triad_oems.json';

export const Tab1TriadOverview: React.FC = () => {
  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Hero Header */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-950/60 border border-rose-800/50 text-rose-300 text-xs font-mono font-bold">
            <ShieldAlert className="w-3.5 h-3.5" />
            2025 GERMAN TRIAD ENCROACHMENT &amp; VULNERABILITY ARCHITECTURE
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            German Auto Triad (Mercedes-Benz, VW, BMW) Chinese Encroachment &amp; Hostage Dilemmas (2025 Baseline)
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            Beyond commercial expansion, the German Auto Triad has become deeply entangled in state-capitalist lock-in. Mercedes-Benz's equity capture, Volkswagen's software reversal and CEA licensing dependency, and BMW's Shenyang mega-hub and captive battery supply chain all represent <strong>Critical Operational Threats</strong>.
          </p>
        </div>
      </div>

      {/* 3 OEM Deep-Dive Cards with Red Badges and Borders */}
      <div className="space-y-5">
        {triadOems.map((oem) => {
          return (
            <div
              key={oem.id}
              className="p-6 rounded-2xl bg-slate-900/90 border-2 border-rose-900/70 space-y-4 shadow-xl hover:border-rose-700 transition"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-xl bg-rose-950 border border-rose-800 text-rose-300">
                    <Building2 className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-lg font-black text-white">{oem.name}</h3>
                    <p className="text-xs text-slate-400">{oem.trapType}</p>
                  </div>
                </div>
                <span className="text-xs font-mono font-extrabold px-3 py-1 rounded-lg border border-rose-800 bg-rose-950 text-rose-300">
                  🔴 CRITICAL THREAT: {oem.trapTag}
                </span>
              </div>

              {/* Data Specifications */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-950/80 p-3.5 rounded-xl border border-slate-800 space-y-1">
                  <span className="text-slate-400 font-mono font-bold">🏢 Local Production vs. Deliveries:</span>
                  <p className="text-amber-300 font-mono leading-relaxed">{oem.localProductionVsSales}</p>
                </div>
                <div className="bg-slate-950/80 p-3.5 rounded-xl border border-slate-800 space-y-1">
                  <span className="text-slate-400 font-mono font-bold">🏛️ Shareholder &amp; Equity Structure:</span>
                  <p className="text-rose-400 font-bold leading-relaxed">{oem.shareholderStructure}</p>
                </div>
              </div>

              <div className="bg-slate-950/80 p-3.5 rounded-xl border border-slate-800 text-xs space-y-1">
                <span className="text-slate-400 font-mono font-bold">⚠️ Structural Vulnerability Summary:</span>
                <p className="text-slate-300 leading-relaxed">{oem.encroachmentSummary}</p>
              </div>

              {/* Unified Red Warning Box */}
              <div className="p-4 rounded-xl bg-rose-950/60 border border-rose-800 text-xs text-rose-200 leading-relaxed">
                <strong className="text-rose-300 font-bold block mb-1">🔴 Corporate Hostage &amp; Compliance Reality (Critical Threat):</strong>
                {oem.appeasementBehavior}
              </div>

              <div className="text-[11px] font-mono text-slate-500 pt-1 border-t border-slate-800/60 flex items-center justify-between">
                <span>📑 Regulatory Source: {oem.metadata.source} [{oem.metadata.confidenceScore}]</span>
                <span>Base Date: {oem.metadata.baseDate}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
