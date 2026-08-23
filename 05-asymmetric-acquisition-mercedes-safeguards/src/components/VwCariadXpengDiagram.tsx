import React from 'react';
import { Cpu, AlertCircle, ArrowDown, ArrowRight, Layers, DollarSign, CheckCircle2 } from 'lucide-react';

export const VwCariadXpengDiagram: React.FC = () => {
  const timeline = [
    {
      year: '2020–2022',
      phase: 'The CARIAD Software Capital Trap',
      status: 'CRITICAL FAILURE',
      color: 'border-rose-800 bg-rose-950/30 text-rose-400',
      details: 'VW created CARIAD to build a proprietary "E3 2.0" software stack. Result: >$3B/year in operating burn, chronic architecture bugs, and 2-year launch delays for Porsche Macan EV and Audi Q6 e-tron.'
    },
    {
      year: '2023',
      phase: '$700M XPENG Stake & Role Reversal',
      status: 'TECH SOVEREIGNTY INVERSION',
      color: 'border-amber-800 bg-amber-950/30 text-amber-400',
      details: 'Conceding internal software failure, VW bought a 4.99% equity stake in Chinese startup XPENG for $700M. VW shifted from historic technology exporter to Chinese software licensee.'
    },
    {
      year: '2024–2025',
      phase: 'China Electronic Architecture (CEA) Co-Development',
      status: 'ZONAL E/E DEPENDENCY',
      color: 'border-teal-800 bg-teal-950/30 text-teal-400',
      details: 'VW and XPENG established joint engineering project teams in Guangzhou and Hefei to license XPENG\'s central computing and zonal E/E architecture for all new VW-branded EVs built in China from 2026.'
    },
    {
      year: '2025+',
      phase: 'Silicon & ADAS Ecosystem Entanglement',
      status: 'DEEP LOCAL LOCK-IN',
      color: 'border-purple-800 bg-purple-950/30 text-purple-400',
      details: 'VW formed the "CARIUS" joint venture with Chinese AI chipmaker Horizon Robotics, integrating Chinese smart-cockpit chips and localized algorithms to survive domestic price wars.'
    }
  ];

  return (
    <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-4">
        <div>
          <div className="text-xs font-mono font-bold text-teal-400 uppercase tracking-wider flex items-center gap-1.5">
            <Cpu className="w-4 h-4 text-teal-400" />
            SOFTWARE SOVEREIGNTY &amp; E/E ARCHITECTURE ROLE REVERSAL
          </div>
          <h3 className="text-lg font-black text-white mt-1">
            Volkswagen's CARIAD Collapse &amp; The XPENG (CEA) Licensing Pivot
          </h3>
        </div>
        <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-900 text-teal-300 border border-slate-700">
          Target: Volkswagen Group (Hefei / Wolfsburg)
        </span>
      </div>

      {/* Visual Timeline Cards */}
      <div className="space-y-3">
        {timeline.map((item, idx) => (
          <div
            key={idx}
            className={`p-4 rounded-xl border ${item.color} flex flex-col md:flex-row md:items-center justify-between gap-4`}
          >
            <div className="space-y-1 md:max-w-xs flex-shrink-0">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-black px-2 py-0.5 rounded bg-slate-950/80 text-white border border-slate-800">
                  {item.year}
                </span>
                <span className="text-[10px] font-mono font-bold uppercase tracking-wider">{item.status}</span>
              </div>
              <h4 className="text-sm font-bold text-white mt-1">{item.phase}</h4>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/60 p-3 rounded-lg border border-slate-800/80 flex-1">
              {item.details}
            </p>
          </div>
        ))}
      </div>

      {/* Comparison Callout */}
      <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        <div>
          <span className="font-bold text-slate-400 block mb-1">Historical Paradigm (1984–2020):</span>
          <p className="text-slate-300 leading-relaxed">
            Volkswagen taught China how to build modern cars (Santana, Passat, MQB platform), retaining 100% of powertrain and electronic intellectual property in Germany.
          </p>
        </div>
        <div>
          <span className="font-bold text-teal-400 block mb-1">Current Inverted Paradigm (2024+):</span>
          <p className="text-slate-300 leading-relaxed">
            Volkswagen relies on Chinese EV startups (XPENG) and chipmakers (Horizon) to provide the central computing brains and ADAS algorithms for its vehicles.
          </p>
        </div>
      </div>
    </div>
  );
};
