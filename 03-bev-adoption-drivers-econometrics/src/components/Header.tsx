import React from 'react';
import { Zap, Filter, Code2, RefreshCw, BarChart2, Cpu, TrendingUp, Sliders } from 'lucide-react';

interface HeaderProps {
  selectedRegions: string[];
  setSelectedRegions: React.Dispatch<React.SetStateAction<string[]>>;
  selectedOEMs: string[];
  setSelectedOEMs: React.Dispatch<React.SetStateAction<string[]>>;
  activeTab: number;
  setActiveTab: (tab: number) => void;
  onOpenCodeModal: () => void;
  allRegions: string[];
  allOEMs: string[];
  totalRowsCount: number;
}

export const Header: React.FC<HeaderProps> = ({
  selectedRegions,
  setSelectedRegions,
  selectedOEMs,
  setSelectedOEMs,
  activeTab,
  setActiveTab,
  onOpenCodeModal,
  allRegions,
  allOEMs,
  totalRowsCount,
}) => {
  const toggleRegion = (region: string) => {
    if (selectedRegions.includes(region)) {
      if (selectedRegions.length > 1) {
        setSelectedRegions(selectedRegions.filter((r) => r !== region));
      }
    } else {
      setSelectedRegions([...selectedRegions, region]);
    }
  };

  const toggleOEM = (oem: string) => {
    if (selectedOEMs.includes(oem)) {
      if (selectedOEMs.length > 1) {
        setSelectedOEMs(selectedOEMs.filter((o) => o !== oem));
      }
    } else {
      setSelectedOEMs([...selectedOEMs, oem]);
    }
  };

  const resetFilters = () => {
    setSelectedRegions(allRegions);
    setSelectedOEMs(allOEMs);
  };

  return (
    <header className="bg-slate-900 border-b border-slate-800 text-white sticky top-0 z-30 shadow-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Top bar */}
        <div className="py-4 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 bg-blue-600/20 border border-blue-500/30 rounded-xl text-blue-400">
              <Zap className="w-7 h-7" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold text-slate-100 tracking-tight">
                  Global BEV Adoption Drivers Analysis
                </h1>
                <span className="px-2 py-0.5 text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">
                  2020 – 2025 Panel
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Econometric Panel Fixed-Effects OLS, VAR Impulse Responses, XGBoost & SHAP Analysis
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <span className="text-xs text-slate-400 block">Dataset Scope</span>
              <span className="text-sm font-semibold text-slate-200">
                {totalRowsCount} Rows | 72 Months | 21 Units
              </span>
            </div>

            <button
              id="open-python-code-btn"
              onClick={onOpenCodeModal}
              className="flex items-center gap-2 px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-blue-400 border border-slate-700 rounded-lg text-sm font-medium transition-colors shadow-sm"
            >
              <Code2 className="w-4 h-4" />
              <span>Python Code Repository</span>
            </button>
          </div>
        </div>

        {/* Filters Bar */}
        <div className="py-2.5 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-4 flex-wrap">
            {/* Region Filter */}
            <div className="flex items-center gap-1.5">
              <span className="text-slate-400 font-medium flex items-center gap-1">
                <Filter className="w-3.5 h-3.5" /> Regions:
              </span>
              <div className="flex gap-1">
                {allRegions.map((r) => {
                  const active = selectedRegions.includes(r);
                  return (
                    <button
                      key={r}
                      onClick={() => toggleRegion(r)}
                      className={`px-2.5 py-1 rounded font-medium transition-all ${
                        active
                          ? 'bg-blue-600 text-white shadow-sm'
                          : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                      }`}
                    >
                      {r}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* OEM Filter */}
            <div className="flex items-center gap-1.5">
              <span className="text-slate-400 font-medium">OEMs:</span>
              <div className="flex flex-wrap gap-1">
                {allOEMs.map((oem) => {
                  const active = selectedOEMs.includes(oem);
                  return (
                    <button
                      key={oem}
                      onClick={() => toggleOEM(oem)}
                      className={`px-2 py-0.5 rounded text-[11px] transition-all ${
                        active
                          ? 'bg-slate-700 text-blue-300 font-medium border border-blue-500/30'
                          : 'bg-slate-800/60 text-slate-400 hover:text-slate-300'
                      }`}
                    >
                      {oem}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          <button
            onClick={resetFilters}
            className="flex items-center gap-1 text-slate-400 hover:text-white transition-colors"
            title="Reset to all regions and OEMs"
          >
            <RefreshCw className="w-3 h-3" />
            <span>Reset Filters</span>
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-t border-slate-800 overflow-x-auto scrollbar-none">
          <button
            id="nav-tab-1"
            onClick={() => setActiveTab(1)}
            className={`flex items-center gap-2 py-3 px-4 border-b-2 font-medium text-sm whitespace-nowrap transition-colors ${
              activeTab === 1
                ? 'border-blue-500 text-blue-400 bg-blue-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <BarChart2 className="w-4 h-4" />
            <span>1. Data & Lag Cross-Correlations</span>
          </button>

          <button
            id="nav-tab-2"
            onClick={() => setActiveTab(2)}
            className={`flex items-center gap-2 py-3 px-4 border-b-2 font-medium text-sm whitespace-nowrap transition-colors ${
              activeTab === 2
                ? 'border-blue-500 text-blue-400 bg-blue-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <TrendingUp className="w-4 h-4" />
            <span>2. Econometric Panel OLS & VAR</span>
          </button>

          <button
            id="nav-tab-3"
            onClick={() => setActiveTab(3)}
            className={`flex items-center gap-2 py-3 px-4 border-b-2 font-medium text-sm whitespace-nowrap transition-colors ${
              activeTab === 3
                ? 'border-blue-500 text-blue-400 bg-blue-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Cpu className="w-4 h-4" />
            <span>3. XGBoost & SHAP Feature Importance</span>
          </button>

          <button
            id="nav-tab-4"
            onClick={() => setActiveTab(4)}
            className={`flex items-center gap-2 py-3 px-4 border-b-2 font-medium text-sm whitespace-nowrap transition-colors ${
              activeTab === 4
                ? 'border-blue-500 text-blue-400 bg-blue-500/5'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Sliders className="w-4 h-4" />
            <span>4. Interactive Scenario Simulator</span>
          </button>
        </div>
      </div>
    </header>
  );
};
