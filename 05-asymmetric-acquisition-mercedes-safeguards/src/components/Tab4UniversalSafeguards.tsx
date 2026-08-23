import React, { useState } from 'react';
import { ShieldCheck, Cpu, Car, BatteryCharging, Dna, CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';
import crossSectorData from '../../data/cross_sector_safeguards.json';

export const Tab4UniversalSafeguards: React.FC = () => {
  const [activeSector, setActiveSector] = useState<string>('automotive');
  const sectors = crossSectorData.sectors;

  const currentSector = sectors.find((s) => s.id === activeSector) || sectors[0];

  const sectorIcons: Record<string, React.ReactNode> = {
    automotive: <Car className="w-5 h-5" />,
    semiconductor: <Cpu className="w-5 h-5" />,
    battery: <BatteryCharging className="w-5 h-5" />,
    biopharma: <Dna className="w-5 h-5" />,
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-950/60 border border-emerald-800/50 text-emerald-300 text-xs font-mono font-bold">
            <ShieldCheck className="w-3.5 h-3.5" />
            CROSS-INDUSTRY INSTITUTIONAL PLAYBOOK
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            Universal Strategic Industry Safeguards: 4 Critical Sectors
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            The Mercedes-Benz case is not an isolated automotive vulnerability. The exact same financial engineering, data exfiltration, and supply chain capture mechanisms are threatening Semiconductors, Battery Materials, and Bio/Pharma. Below is the multi-sector institutional defense protocol.
          </p>
        </div>
      </div>

      {/* Sector Selection Tabs */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {sectors.map((sec) => {
          const isSelected = activeSector === sec.id;
          return (
            <button
              key={sec.id}
              onClick={() => setActiveSector(sec.id)}
              className={`p-4 rounded-xl border text-left transition flex items-center gap-3 ${
                isSelected
                  ? 'bg-blue-950/80 border-blue-500/80 text-white shadow-lg shadow-blue-950/50'
                  : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-900'
              }`}
            >
              <div
                className={`p-2 rounded-lg ${
                  isSelected ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-400'
                }`}
              >
                {sectorIcons[sec.id]}
              </div>
              <div>
                <div className="text-xs font-mono uppercase font-bold">{sec.id}</div>
                <div className="text-xs font-bold text-white truncate">{sec.sectorName.split(' ')[0]}</div>
              </div>
            </button>
          );
        })}
      </div>

      {/* Active Sector Deep-Dive Card */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-6">
        {/* Header of Active Sector */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-600 text-white shadow-md">
              {sectorIcons[currentSector.id]}
            </div>
            <div>
              <h3 className="text-lg font-black text-white">{currentSector.sectorName}</h3>
              <p className="text-xs text-slate-400">{currentSector.vulnerabilityProfile}</p>
            </div>
          </div>
          <span className="text-xs font-mono px-3 py-1 rounded bg-slate-800 text-sky-400 border border-slate-700 font-bold self-start md:self-auto">
            Sector Defense Mandate
          </span>
        </div>

        {/* Sector Threat Vectors */}
        <div className="p-4 rounded-xl bg-rose-950/30 border border-rose-900/40 space-y-2">
          <div className="text-xs font-mono font-bold text-rose-300 uppercase tracking-wider flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5" />
            Key Sector Vulnerability Vectors:
          </div>
          <ul className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs text-slate-300 pt-1">
            {currentSector.threatVectors.map((tv, idx) => (
              <li key={idx} className="bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/80 flex items-start gap-2">
                <span className="text-rose-400 font-bold font-mono">0{idx + 1}.</span>
                <span>{tv}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* 4 Pillars of Safeguards */}
        <div>
          <h4 className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            The 4-Pillar Strategic Countermeasure Matrix
          </h4>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* 1. Investment Screening */}
            <div className="p-4 rounded-xl bg-slate-950/90 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-sky-400 uppercase font-mono">
                  1. Synthetic Investment Screening
                </span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-sky-950 text-sky-300 border border-sky-800">
                  CFIUS / AWV
                </span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                {currentSector.safeguards.investmentScreening}
              </p>
            </div>

            {/* 2. Supply Chain Quotas */}
            <div className="p-4 rounded-xl bg-slate-950/90 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-emerald-400 uppercase font-mono">
                  2. China+1 Sourcing Redundancy
                </span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                  &lt;30% CAP
                </span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                {currentSector.safeguards.supplyChainQuotas}
              </p>
            </div>

            {/* 3. Data Air-Gapping */}
            <div className="p-4 rounded-xl bg-slate-950/90 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-purple-400 uppercase font-mono">
                  3. Sovereign Data Air-Gapping
                </span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800">
                  ZERO PEERING
                </span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                {currentSector.safeguards.dataAirGapping}
              </p>
            </div>

            {/* 4. Corporate Governance */}
            <div className="p-4 rounded-xl bg-slate-950/90 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-amber-400 uppercase font-mono">
                  4. Geopolitical Risk Committee
                </span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800">
                  EXIT CLAUSE
                </span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                {currentSector.safeguards.corporateGovernance}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
