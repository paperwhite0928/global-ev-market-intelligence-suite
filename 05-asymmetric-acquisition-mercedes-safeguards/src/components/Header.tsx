import React from 'react';
import { ShieldAlert, TrendingDown, Layers, Split, Building2, ShieldCheck, ArrowLeftRight, Scale, Lightbulb } from 'lucide-react';

interface HeaderProps {
  activeTab: number;
  setActiveTab: (tab: number) => void;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 1, label: '1. 2019–2025 Market Collapse & Dependency', icon: TrendingDown },
    { id: 2, label: '2. Triad Encroachment & Hostage Dilemmas', icon: Building2 },
    { id: 3, label: '3. IDAR Strategy & Asymmetric Openness', icon: Scale },
    { id: 4, label: '4. Technology Exfiltration & Reverse Flow', icon: ArrowLeftRight },
    { id: 5, label: '5. 3 Scenarios & Quantitative Calculator', icon: Split },
    { id: 6, label: '6. €45B Sunk Capital & Dual-Track Air-Gap', icon: Layers },
    { id: 7, label: '7. 5 Strategic Truths & Policy Actions', icon: Lightbulb },
    { id: 8, label: '8. Cross-Sector Safeguards & Board Checklist', icon: ShieldCheck },
  ];

  return (
    <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur sticky top-0 z-40">
      {/* Top Threat Alert Bar */}
      <div className="bg-rose-950/40 border-b border-rose-800/40 px-4 py-1.5 flex flex-wrap items-center justify-between text-xs gap-2">
        <div className="flex items-center gap-2 text-rose-300 font-medium">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
          </span>
          <span className="font-mono font-bold tracking-wider uppercase text-[11px] bg-rose-900/60 text-rose-200 px-1.5 py-0.5 rounded border border-rose-700/50">
            AUDITED STRATEGIC INTELLIGENCE SUITE
          </span>
          <span>China Tech-Absorption (IDAR) &amp; Asymmetric Lock-in: German Auto Triad Dependency &amp; Safeguards (2019–2025)</span>
        </div>
        <div className="text-[11px] font-mono text-slate-400">
          Core Thesis: Phased De-risking of Chinese Dependency &amp; Restoration of Strategic Autonomy
        </div>
      </div>

      {/* Main Title & Nav Container */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between py-4 gap-4">
          <div>
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-blue-950/60 border border-blue-800/50 text-blue-400">
                <ShieldAlert className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-lg sm:text-xl font-extrabold text-white tracking-tight flex items-center gap-2">
                  The German Auto Triad's China Trap
                  <span className="text-xs font-mono font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                    STAGE 05
                  </span>
                </h1>
                <p className="text-xs sm:text-sm text-slate-400">
                  Asymmetric IDAR Absorption, Governance Vulnerabilities (AktG §179) &amp; The Phased De-risking Playbook (2019–2035)
                </p>
              </div>

            </div>
          </div>

          {/* Macro KPI Ribbon with Strict Severity Coloring */}
          <div className="flex items-center gap-2.5 overflow-x-auto pb-1 md:pb-0">
            <div className="bg-slate-900/90 border border-rose-900/60 rounded-lg px-3 py-1.5 min-w-[130px]">
              <div className="text-[10px] uppercase font-mono font-bold text-rose-300">Triad Sales Collapse</div>
              <div className="text-base font-extrabold text-rose-400 font-mono">-1.59M <span className="text-xs text-rose-200 font-normal">(-28.1%)</span></div>
            </div>
            <div className="bg-slate-900/90 border border-orange-900/60 rounded-lg px-3 py-1.5 min-w-[130px]">
              <div className="text-[10px] uppercase font-mono font-bold text-orange-300">Mercedes Chinese Stake</div>
              <div className="text-base font-extrabold text-orange-400 font-mono">19.67% <span className="text-xs text-orange-200 font-normal">voting</span></div>
            </div>
            <div className="bg-slate-900/90 border border-rose-900/60 rounded-lg px-3 py-1.5 min-w-[130px]">
              <div className="text-[10px] uppercase font-mono font-bold text-rose-300">China Market Share Plunge</div>
              <div className="text-base font-extrabold text-rose-400 font-mono">12.8% <span className="text-xs text-rose-200 font-normal">(-12.3%p)</span></div>
            </div>
            <div className="bg-slate-900/90 border border-orange-900/60 rounded-lg px-3 py-1.5 min-w-[130px]">
              <div className="text-[10px] uppercase font-mono font-bold text-orange-300">Local Production Lock-in</div>
              <div className="text-base font-extrabold text-orange-400 font-mono">89.2% <span className="text-xs text-orange-200 font-normal">in China</span></div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-1 border-t border-slate-800/60 overflow-x-auto py-2">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
};
