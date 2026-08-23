import React, { useState } from 'react';
import { ShieldAlert, Cpu, Car, BatteryCharging, Dna, CheckSquare, Sparkles, ChevronDown, ChevronUp, FileText, Split, AlertTriangle } from 'lucide-react';
import { CROSS_SECTOR_DEFENSE_MATRIX } from '../data/autoTriadData';

export const Tab5CrossIndustryPlaybook: React.FC = () => {
  const [selectedSectorIndex, setSelectedSectorIndex] = useState<number>(0);
  const [isScenarioDrawerOpen, setIsScenarioDrawerOpen] = useState<boolean>(true);

  const sectorIcons = [
    <Car className="w-5 h-5" />,
    <Cpu className="w-5 h-5" />,
    <BatteryCharging className="w-5 h-5" />,
    <Dna className="w-5 h-5" />
  ];

  const currentSector = CROSS_SECTOR_DEFENSE_MATRIX[selectedSectorIndex];

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-950/60 border border-blue-800/50 text-blue-300 text-xs font-mono font-bold">
            <ShieldAlert className="w-3.5 h-3.5" />
            CROSS-INDUSTRY UNIVERSAL DEFENSE FRAMEWORK
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            Universal Enterprise Safeguards: 4 Critical Advanced Industries
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            The vulnerabilities exposed by the German Auto Triad apply identically across all capital-intensive, high-technology Western manufacturing. Below is the multi-sector institutional defense protocol.
          </p>
        </div>
      </div>

      {/* Sector Selection Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {CROSS_SECTOR_DEFENSE_MATRIX.map((sec, idx) => (
          <button
            key={idx}
            onClick={() => setSelectedSectorIndex(idx)}
            className={`p-4 rounded-xl border text-left transition flex items-center gap-3 ${
              selectedSectorIndex === idx
                ? 'bg-blue-950/80 border-blue-500 text-white shadow-lg shadow-blue-950/50'
                : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:text-white hover:bg-slate-900'
            }`}
          >
            <div className={`p-2 rounded-lg ${selectedSectorIndex === idx ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-400'}`}>
              {sectorIcons[idx]}
            </div>
            <div>
              <div className="text-[10px] font-mono uppercase font-bold text-slate-400">Sector 0{idx + 1}</div>
              <div className="text-xs font-bold text-white truncate">{sec.sector.split(' ')[0]}</div>
            </div>
          </button>
        ))}
      </div>

      {/* Active Sector Defense Matrix Table / Cards */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-600 text-white shadow-md">
              {sectorIcons[selectedSectorIndex]}
            </div>
            <div>
              <h3 className="text-lg font-black text-white">{currentSector.sector}</h3>
              <p className="text-xs text-rose-400 font-medium">Vulnerability: {currentSector.vulnerability}</p>
            </div>
          </div>
          <span className="text-xs font-mono px-3 py-1 rounded bg-slate-800 text-sky-400 border border-slate-700 font-bold self-start sm:self-auto">
            Institutional Defense Matrix
          </span>
        </div>

        {/* 4 Safeguard Columns */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
            <span className="text-xs font-bold text-emerald-400 font-mono uppercase block">
              1. China+1 Sourcing Quotas (&lt;30% Cap)
            </span>
            <p className="text-slate-300 leading-relaxed">{currentSector.chinaPlusOne}</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
            <span className="text-xs font-bold text-teal-400 font-mono uppercase block">
              2. Intellectual Property (IP) Black-Boxing
            </span>
            <p className="text-slate-300 leading-relaxed">{currentSector.ipBlackBoxing}</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
            <span className="text-xs font-bold text-purple-400 font-mono uppercase block">
              3. Sovereign Data Air-Gapping
            </span>
            <p className="text-slate-300 leading-relaxed">{currentSector.dataAirGap}</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2">
            <span className="text-xs font-bold text-amber-400 font-mono uppercase block">
              4. Board Geopolitical Risk Committees
            </span>
            <p className="text-slate-300 leading-relaxed">{currentSector.governance}</p>
          </div>
        </div>
      </div>

      {/* Slide-over / Expandable Future Scenario Drawer */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <button
          onClick={() => setIsScenarioDrawerOpen(!isScenarioDrawerOpen)}
          className="w-full p-5 flex items-center justify-between bg-slate-900 hover:bg-slate-850 transition text-left"
        >
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-purple-950 text-purple-400 border border-purple-800/50">
              <Split className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">2026–2035 Strategic Foresight: 2 Divergent Scenarios</h3>
              <p className="text-xs text-slate-400">Comparing "Brand Licensor Demotion" vs. "Sovereign Allied Re-architecture"</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
            <span>{isScenarioDrawerOpen ? 'Collapse Drawer' : 'Expand Foresight'}</span>
            {isScenarioDrawerOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </div>
        </button>

        {isScenarioDrawerOpen && (
          <div className="p-6 border-t border-slate-800 bg-slate-950/60 space-y-4 animate-in fade-in duration-200">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
              {/* Scenario 1: Brand Licensor Demotion */}
              <div className="p-4 rounded-xl bg-rose-950/30 border border-rose-900/50 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-rose-400 text-sm">Scenario A: Brand Licensor Demotion</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">
                    STATUS QUO INERTIA
                  </span>
                </div>
                <p className="text-slate-300 leading-relaxed">
                  German OEMs continue licensing Chinese software (XPENG, Horizon) and battery tech (CATL, EVE) while Chinese shareholders (Geely 9.69%, BAIC 9.98%) veto strategic spin-offs.
                </p>
                <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 text-[11px] text-rose-300">
                  <strong>Outcome:</strong> German automakers are relegated to mere metal-bending brand licensors with compressed margins (4–6% EBIT) while Chinese partners capture all software, battery, and AI value.
                </div>
              </div>

              {/* Scenario 2: Sovereign Allied Re-architecture */}
              <div className="p-4 rounded-xl bg-emerald-950/30 border border-emerald-900/50 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-emerald-400 text-sm">Scenario B: Sovereign Allied Re-architecture</span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                    STRATEGIC RESILIENCE
                  </span>
                </div>
                <p className="text-slate-300 leading-relaxed">
                  German leadership implements the 4-Step Capital Defense (dilution + allied voting bloc) and strictly enforces "In China for China" dual-track air-gapping with European open SDV alliances (Rivian, Qualcomm, Bosch).
                </p>
                <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 text-[11px] text-emerald-300">
                  <strong>Outcome:</strong> Restores European software and battery IP sovereignty, isolates Western vehicle telemetry on sovereign clouds, and defends a resilient 8–10% EBIT margin through 2035.
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
