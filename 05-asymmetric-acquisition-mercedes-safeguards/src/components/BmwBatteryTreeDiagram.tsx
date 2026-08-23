import React from 'react';
import { BatteryCharging, Globe, ArrowRight, ShieldAlert, Layers, Factory, Anchor } from 'lucide-react';

export const BmwBatteryTreeDiagram: React.FC = () => {
  return (
    <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-4">
        <div>
          <div className="text-xs font-mono font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-1.5">
            <BatteryCharging className="w-4 h-4 text-indigo-400" />
            UPSTREAM REFINING &amp; EXPORT HUB VULNERABILITY TREE
          </div>
          <h3 className="text-lg font-black text-white mt-1">
            BMW Group: Battery Value Chain Dependency &amp; Shenyang Export Trap
          </h3>
        </div>
        <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-900 text-indigo-300 border border-slate-700">
          Target: BMW Group (Shenyang / Munich)
        </span>
      </div>

      {/* Value Chain Dependency Flow */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Tier 1: Raw Materials Refining */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 space-y-2 relative">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono font-bold text-rose-400 uppercase px-2 py-0.5 bg-rose-950/80 rounded border border-rose-800">
              Stage 1: Mineral Monopoly
            </span>
          </div>
          <h4 className="text-sm font-bold text-white">Upstream Refining</h4>
          <p className="text-xs text-slate-300">
            65% of Lithium, 75% of Cobalt, and 90% of anode Graphite refined in mainland China under state export permits.
          </p>
          <div className="text-[11px] text-rose-400 font-mono pt-1">
            Risk: Export permit embargoes
          </div>
        </div>

        {/* Tier 2: Cell Chemistry Giants */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 space-y-2 relative">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono font-bold text-amber-400 uppercase px-2 py-0.5 bg-amber-950/80 rounded border border-amber-800">
              Stage 2: Cell Champions
            </span>
          </div>
          <h4 className="text-sm font-bold text-white">CATL &amp; EVE Energy</h4>
          <p className="text-xs text-slate-300">
            BMW signed multi-billion multi-year contracts with CATL and EVE Energy for Gen-6 cylindrical &amp; prismatic battery cells.
          </p>
          <div className="text-[11px] text-amber-400 font-mono pt-1">
            Risk: Pricing &amp; chemistry lock-in
          </div>
        </div>

        {/* Tier 3: Shenyang Mega-Plant */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 space-y-2 relative">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono font-bold text-indigo-400 uppercase px-2 py-0.5 bg-indigo-950/80 rounded border border-indigo-800">
              Stage 3: Shenyang Hub
            </span>
          </div>
          <h4 className="text-sm font-bold text-white">BMW Brilliance (75%)</h4>
          <p className="text-xs text-slate-300">
            BMW raised its BBA stake to 75% for €3.7B, converting Tiexi and Dadong plants into its primary global pure EV manufacturing core.
          </p>
          <div className="text-[11px] text-indigo-400 font-mono pt-1">
            Risk: Fixed sunk capital trap
          </div>
        </div>

        {/* Tier 4: Global Export Flow */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 space-y-2 relative">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-mono font-bold text-emerald-400 uppercase px-2 py-0.5 bg-emerald-950/80 rounded border border-emerald-800">
              Stage 4: Reverse Export
            </span>
          </div>
          <h4 className="text-sm font-bold text-white">Global iX3 Exports</h4>
          <p className="text-xs text-slate-300">
            BMW exports Chinese-manufactured iX3 pure electric SUVs from China back into European and global markets.
          </p>
          <div className="text-[11px] text-emerald-400 font-mono pt-1">
            Risk: EU Countervailing tariffs (21.3%)
          </div>
        </div>
      </div>

      {/* Strategic Summary Box */}
      <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 text-xs text-slate-300 space-y-2">
        <div className="font-bold text-indigo-300 uppercase font-mono flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-rose-400" />
          The BMW Reverse-Export Vulnerability Paradox:
        </div>
        <p className="leading-relaxed">
          While BMW achieved record sales by leveraging China as an export powerhouse, it became caught in a geopolitical crossfire. When the European Commission imposed anti-subsidy countervailing duties on Chinese EV imports, BMW's Shenyang-built iX3 faced direct punitive tariffs, penalizing the German automaker with its own domestic European trade barriers.
        </p>
      </div>
    </div>
  );
};
