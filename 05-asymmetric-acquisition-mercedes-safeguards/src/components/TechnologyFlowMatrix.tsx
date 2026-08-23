import React, { useState } from 'react';
import { ArrowLeftRight, Cpu, Layers, Database, Cog, Factory } from 'lucide-react';
import flowData from '../../data/technology_flow_matrix.json';

export const TechnologyFlowMatrix: React.FC = () => {
  const [activeDomainIdx, setActiveDomainIdx] = useState<number>(0);

  const dimensions = flowData.historicalVsPresent.dimensions;
  const domains = flowData.domainSpecificEvidence;

  const domainIcons = [
    <Factory className="w-4 h-4" />,
    <Layers className="w-4 h-4" />,
    <Cpu className="w-4 h-4" />,
    <Database className="w-4 h-4" />,
    <Cog className="w-4 h-4" />
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Header */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="space-y-1.5">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-950/60 border border-rose-800/50 text-rose-300 text-xs font-mono font-bold">
            <ArrowLeftRight className="w-3.5 h-3.5" />
            TECHNOLOGY FLOW DIRECTIONALITY &amp; DOMAIN-SPECIFIC EVIDENCE
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            Technology Exfiltration &amp; Reverse Flow Dynamics: Historical Cooperation (1984–2020) vs. Present Competition (2025)
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            Historical technology transfer flowed unilaterally from Europe to China; today, critical software stacks, battery chemistries, and sensor platforms face domestic Chinese priority and strict outbound export controls, cementing a <strong>'Role Reversal'</strong>.
          </p>
        </div>
      </div>

      {/* Main Comparative Table with Severity Badges */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 overflow-x-auto space-y-4">
        <h3 className="text-sm font-bold text-slate-200 uppercase font-mono tracking-wider flex items-center gap-2">
          <ArrowLeftRight className="w-4 h-4 text-rose-400" />
          5-Dimensional Comparative Paradigm &amp; Severity Assessment
        </h3>

        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-950/80 text-slate-400 font-mono">
              <th className="p-3 w-1/6">Dimension</th>
              <th className="p-3 w-1/6">Threat Severity</th>
              <th className="p-3 w-1/3 text-blue-400">Historical Cooperation (1984–2020)</th>
              <th className="p-3 w-1/3 text-rose-400">Present Competition (2025)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {dimensions.map((dim, idx) => (
              <tr key={idx} className="hover:bg-slate-950/50 transition">
                <td className="p-3.5 font-bold text-white font-mono bg-slate-950/30">{dim.dimension}</td>
                <td className="p-3.5">
                  <span
                    className={`px-2 py-0.5 rounded text-[11px] font-mono font-bold ${
                      dim.severity === 'critical'
                        ? 'bg-rose-950 text-rose-300 border border-rose-800'
                        : 'bg-amber-950 text-amber-300 border border-amber-800'
                    }`}
                  >
                    {dim.severityTag}
                  </span>
                </td>
                <td className="p-3.5 leading-relaxed bg-blue-950/10 border-l border-blue-900/20">{dim.pastCooperation}</td>
                <td className="p-3.5 leading-relaxed bg-rose-950/10 border-l border-rose-900/20">{dim.presentCompetition}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Domain-Specific Breakdown Cards with Color Coded Conclusions */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-base font-bold text-white">5 Core Technological Domains: Empirical Evidence Breakdown</h3>
            <p className="text-xs text-slate-400">Evaluates residual European advantages against Chinese supply chain capture across 5 critical engineering domains.</p>
          </div>
          <span className="text-xs font-mono px-2.5 py-0.5 rounded bg-slate-800 text-rose-300 border border-slate-700">
            Severity Filter
          </span>
        </div>

        {/* Domain Navigation */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
          {domains.map((d, idx) => (
            <button
              key={idx}
              onClick={() => setActiveDomainIdx(idx)}
              className={`p-3 rounded-xl border text-left transition flex flex-col justify-between ${
                activeDomainIdx === idx
                  ? d.severity === 'critical'
                    ? 'bg-rose-950/80 border-rose-500 text-white shadow-lg shadow-rose-950/40'
                    : d.severity === 'moderate'
                    ? 'bg-amber-950/80 border-amber-500 text-white shadow-lg shadow-amber-950/40'
                    : 'bg-yellow-950/80 border-yellow-500 text-white shadow-lg shadow-yellow-950/40'
                  : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:text-white hover:bg-slate-900'
              }`}
            >
              <div className="flex items-center gap-1.5 mb-1 text-slate-300">
                {domainIcons[idx]}
                <span className="text-[10px] font-mono font-bold">Domain 0{idx + 1}</span>
              </div>
              <div className="text-xs font-bold truncate">{d.domain.split('(')[0]}</div>
              <span className="text-[10px] font-mono mt-1 font-semibold text-slate-400">{d.severityTag.split(' ')[0]}</span>
            </button>
          ))}
        </div>

        {/* Active Domain Detail Card */}
        {(() => {
          const cur = domains[activeDomainIdx];
          const isCrit = cur.severity === 'critical';
          const isMod = cur.severity === 'moderate';

          return (
            <div className="p-5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-4 animate-in fade-in duration-200">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                <h4 className="text-sm font-bold text-white">{cur.domain}</h4>
                <div className="flex gap-2">
                  <span
                    className={`text-xs font-mono font-bold px-2.5 py-0.5 rounded ${
                      isCrit
                        ? 'bg-rose-950 text-rose-300 border border-rose-800'
                        : isMod
                        ? 'bg-orange-950 text-orange-300 border border-orange-800'
                        : 'bg-yellow-950 text-yellow-300 border border-yellow-800'
                    }`}
                  >
                    {cur.severityTag}
                  </span>
                  <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded bg-slate-900 text-slate-300 border border-slate-700">
                    {cur.leverageRetained}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800 space-y-1.5">
                  <span className="text-blue-400 font-bold block font-mono">🇪🇺 European Status &amp; Residual Advantages:</span>
                  <p className="text-slate-300 leading-relaxed">{cur.europeStatus}</p>
                </div>
                <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800 space-y-1.5">
                  <span className="text-rose-400 font-bold block font-mono">🇨🇳 Chinese Dominance &amp; Supply Chain Control:</span>
                  <p className="text-slate-300 leading-relaxed">{cur.chinaStatus}</p>
                </div>
              </div>

              {/* Conclusion Box */}
              <div
                className={`p-4 rounded-xl text-xs flex items-start gap-2 border ${
                  isCrit
                    ? 'bg-rose-950/40 border-rose-800/80 text-rose-100'
                    : isMod
                    ? 'bg-orange-950/40 border-orange-800/80 text-orange-100'
                    : 'bg-yellow-950/40 border-yellow-800/80 text-yellow-100'
                }`}
              >
                <span
                  className={`font-mono font-bold flex-shrink-0 ${
                    isCrit ? 'text-rose-400' : isMod ? 'text-orange-400' : 'text-yellow-400'
                  }`}
                >
                  Strategic Flow Reversal Conclusion:
                </span>
                <span className="leading-relaxed font-medium">{cur.flowDirection}</span>
              </div>
            </div>
          );
        })()}
      </div>
    </div>
  );
};
