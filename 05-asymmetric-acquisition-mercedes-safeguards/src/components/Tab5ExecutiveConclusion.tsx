import React, { useState } from 'react';
import { CheckSquare, Lock, Scale, Cpu, Battery, Dna, Car, Globe, Database, Shield } from 'lucide-react';

export const Tab5ExecutiveConclusion: React.FC = () => {
  const [selectedSectorIdx, setSelectedSectorIdx] = useState(0);

  const sectors = [
    {
      id: "automotive",
      sector: "Automotive & Intelligent Mobility (SDV)",
      icon: <Car className="w-5 h-5 text-sky-400" />,
      color: "#38BDF8",
      border: "border-sky-700/60",
      bgBadge: "bg-sky-950 text-sky-300 border-sky-800",
      riskScore: 88,
      riskLevel: "CRITICAL RISK",
      vulnerability: "China sales concentration >30%, flagship margin hostage risks, software stack dependence on Momenta/XPENG, and vehicle telemetry exfiltration exposure under PRC Art. 7.",
      chinaPlusOneTitle: "1. China+1 Sourcing & Platform Quotas",
      chinaPlusOne: "Enforce strict China+1 sourcing quotas: mandate a maximum 25% single-country BOM dependency for key vehicle platforms, power electronics, and sub-tier microcontrollers.",
      ipBlackBoxingTitle: "2. Intellectual Property (IP) Black-Boxing",
      ipBlackBoxing: "Provide only compiled binary firmware to Chinese JVs; strictly air-gap core SDV source code (MB.OS / Rivian-VW), neural network weights, and cryptographic keys inside European HSMs.",
      dataAirGapTitle: "3. Sovereign Data Air-Gapping",
      dataAirGap: "Complete physical & cryptographic air-gapping: European/US fleet telemetry isolated on NATO-certified sovereign cloud, legally preventing extraterritorial transfer under PRC Intelligence Law Art. 7.",
      governanceTitle: "4. Board-Level Geopolitical Risk Committee",
      governance: "Supervisory Board Geopolitical Risk Committee with statutory unilateral JV exit, asset buy-back rights, and AktG §179 capital safeguards against 25% blocking minority encroachment."
    },
    {
      id: "semiconductors",
      sector: "Semiconductors & EDA Design Tools",
      icon: <Cpu className="w-5 h-5 text-amber-400" />,
      color: "#F59E0B",
      border: "border-amber-700/60",
      bgBadge: "bg-amber-950 text-amber-300 border-amber-800",
      riskScore: 92,
      riskLevel: "EXTREME RISK",
      vulnerability: "Subsidized legacy node (28nm+) foundry dumping, mandatory IP disclosure pressures in mainland test centers, and weaponization of critical packaging choke-points.",
      chinaPlusOneTitle: "1. China+1 Sourcing & Fabrication Quotas",
      chinaPlusOne: "Mandate a minimum 40% wafer fabrication allocation to democratic semiconductor alliances (US, EU Chips Act hubs, Japan, Taiwan, and allied fabs).",
      ipBlackBoxingTitle: "2. Intellectual Property (IP) Black-Boxing",
      ipBlackBoxing: "Black-box proprietary RTL circuit designs and GDSII tape-out data; strictly prohibit joint EDA co-development and co-simulation in non-allied R&D hubs.",
      dataAirGapTitle: "3. Sovereign Data Air-Gapping",
      dataAirGap: "Enforce zero-trust architecture across offshore design centers with cryptographic prevention of outbound cloud schematic file transfers.",
      governanceTitle: "4. Board-Level Geopolitical Risk Committee",
      governance: "Mandate formal export control compliance and joint EU FDI/German AWG (Foreign Trade Act) reviews on all advanced packaging and back-end test joint ventures."
    },
    {
      id: "battery",
      sector: "Battery Materials & Energy Storage",
      icon: <Battery className="w-5 h-5 text-emerald-400" />,
      color: "#10B981",
      border: "border-emerald-700/60",
      bgBadge: "bg-emerald-950 text-emerald-300 border-emerald-800",
      riskScore: 85,
      riskLevel: "HIGH VULNERABILITY",
      vulnerability: "Single-nation monopoly over upstream refining (Lithium 65%, Graphite 90%), cell export restriction risks, and remote telemetry exposure in smart grid BMS inverters.",
      chinaPlusOneTitle: "1. CRMA & IRA Multilateral Sourcing Quotas",
      chinaPlusOne: "Scale CRMA/IRA-compliant quotas: minimum 50% non-FEOC battery materials by 2026 scaling to 80% allied by 2030, leveraging PowerCo, Panasonic, and Korean Big 3 alliances.",
      ipBlackBoxingTitle: "2. Intellectual Property (IP) Black-Boxing",
      ipBlackBoxing: "Retain proprietary dry electrode coating, solid-state electrolyte formulations, and high-nickel cathode recipes in European/US trade secret vaults with zero technology transfer to JVs.",
      dataAirGapTitle: "3. Sovereign Data Air-Gapping",
      dataAirGap: "Battery Management System (BMS) firmware telemetry, cell health diagnostics, and smart grid inverters physically decoupled from Chinese server infrastructure.",
      governanceTitle: "4. Board-Level Geopolitical Risk Committee",
      governance: "Form 50:50 cell gigafactory JVs exclusively with allied Tier-1 battery specialists, backed by 10-year sovereign offtake agreements and critical mineral stockpiling."
    },
    {
      id: "biotech",
      sector: "Biotechnology & Pharmaceuticals",
      icon: <Dna className="w-5 h-5 text-purple-400" />,
      color: "#A855F7",
      border: "border-purple-700/60",
      bgBadge: "bg-purple-950 text-purple-300 border-purple-800",
      riskScore: 80,
      riskLevel: "HIGH VULNERABILITY",
      vulnerability: "Active Pharmaceutical Ingredient (API) supply concentration >80%, forced genomic dataset requisition under national intelligence statutes, and bioreactor process IP exfiltration.",
      chinaPlusOneTitle: "1. Strategic API Reserves & Onshore Quotas",
      chinaPlusOne: "Strategic National Stockpile mandate: minimum 6-month onshore Active Pharmaceutical Ingredient (API) buffer reserve and 35% domestic manufacturing capacity.",
      ipBlackBoxingTitle: "2. Intellectual Property (IP) Black-Boxing",
      ipBlackBoxing: "Black-box mRNA sequence engineering, viral vector designs, and proprietary continuous bioreactor fermentation parameters under multi-layered cryptographic protection.",
      dataAirGapTitle: "3. Sovereign Genomic Data Air-Gapping",
      dataAirGap: "HIPAA & GDPR genomic air-gaps: all Western DNA/RNA patient sequencing datasets processed and stored exclusively on sovereign European/US on-premises servers.",
      governanceTitle: "4. Board-Level Geopolitical Risk Committee",
      governance: "Mandatory inclusion of irrevocable clinical trial license revocation clauses upon state regulatory interference or unauthorized Party Committee access."
    }
  ];

  const boardChecklist = [
    {
      id: 1,
      category: "1. Shareholder Governance Oversight",
      action: "Are non-EU voting rights strictly controlled below 25% under German AktG §179?",
      detail: "Execute 15% strategic dilution and mobilize proxy turnout to achieve total AGM turnout >= 70.0% (or allied-only turnout >= 85.0%), reducing effective Chinese voting power to 24.43% (<25.0%) to eliminate the Sperrminorität blocking veto."
    },
    {
      id: 2,
      category: "2. Software Source Code Black-Boxing",
      action: "Is firmware supplied to Chinese JVs exclusively in compiled binary format?",
      detail: "Verify that autonomous driving neural networks and vehicle OS root algorithm source code are cryptographically isolated inside European Hardware Security Modules (HSMs)."
    },
    {
      id: 3,
      category: "3. Outbound Data Air-Gapping",
      action: "Is complete physical and cryptographic air-gapping operational between mainland vehicle telemetry servers and Western headquarters infrastructure?",
      detail: "Verify independent operation on NATO-certified sovereign clouds to prevent mandatory data requisition under PRC National Intelligence Law Art. 7."
    },
    {
      id: 4,
      category: "4. 30% Battery Supply Concentration Cap",
      action: "Is single-country battery cell and refined material dependency capped below 30% of total platform BOM value?",
      detail: "Enforce China+1 quotas through 10-year sovereign offtake agreements with Korean Big 3 (LG, Samsung, SK) and European/North American refining facilities."
    },
    {
      id: 5,
      category: "5. Unilateral JV Exit & IP Revocation Clause",
      action: "Do joint venture contracts contain explicit covenants permitting unilateral asset disposal and license termination upon state technology transfer mandates?",
      detail: "Codify automatic buy-back options and immediate IP license invalidation clauses upon breach of contract or mandatory transfer decrees by state-owned partners."
    },
    {
      id: 6,
      category: "6. Board Geopolitical Risk Committee",
      action: "Are all new non-EU capital projects and technology licensing agreements subject to prior unanimous approval by a board-level Geopolitical Risk Committee?",
      detail: "Operate quarterly national security risk audits and monitor domestic Party Committee (Company Law Art. 19) activities within joint venture subsidiaries."
    }
  ];

  const currentSec = sectors[selectedSectorIdx];

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-950/60 border border-emerald-800/50 text-emerald-300 text-xs font-mono font-bold">
            <Shield className="w-3.5 h-3.5" />
            UNIVERSAL CROSS-INDUSTRY DEFENSE FRAMEWORK
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            Universal Cross-Industry Defense Protocol (4 Critical Sectors) &amp; Supervisory Board Verdict
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            Structural vulnerability diagnostics and 4-pillar safeguard rules (Quotas, IP Black-Boxing, Data Air-Gap, Governance) spanning Automotive SDVs, Advanced Semiconductors &amp; EDA, Battery Materials, and Biopharma.
          </p>
        </div>
      </div>

      {/* 4-Sector Pill Selector */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {sectors.map((sec, idx) => (
          <button
            key={sec.id}
            onClick={() => setSelectedSectorIdx(idx)}
            className={`p-3.5 rounded-xl border text-left transition flex flex-col justify-between ${
              selectedSectorIdx === idx
                ? `bg-slate-800/90 ${sec.border} ring-2 ring-sky-500/40`
                : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              {sec.icon}
              <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${sec.bgBadge}`}>
                {sec.riskScore}/100
              </span>
            </div>
            <div className="text-xs font-bold text-white">{sec.sector.split('(')[0]}</div>
            <div className="text-[10px] text-slate-400 font-mono mt-0.5">{sec.riskLevel}</div>
          </button>
        ))}
      </div>

      {/* Sector Deep-Dive Card */}
      <div className={`p-6 rounded-2xl bg-slate-900/90 border ${currentSec.border} space-y-4`}>
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center gap-3">
            {currentSec.icon}
            <div>
              <h3 className="text-base font-bold text-white">{currentSec.sector}</h3>
              <p className="text-xs text-slate-400 font-mono">Sector Code: {currentSec.id.toUpperCase()} • Institutional Safeguard Matrix</p>
            </div>
          </div>
          <span className={`text-xs font-mono font-bold px-3 py-1 rounded border ${currentSec.bgBadge}`}>
            {currentSec.riskLevel}
          </span>
        </div>

        <div className="p-3 rounded-xl bg-rose-950/40 border border-rose-900/60 text-xs text-rose-200">
          <strong className="text-rose-300 font-mono">🔴 Identified Structural Vulnerability:</strong> {currentSec.vulnerability}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 border-t-2 border-t-emerald-400 space-y-2">
            <div className="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
              <Globe className="w-3.5 h-3.5" /> {currentSec.chinaPlusOneTitle}
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">{currentSec.chinaPlusOne}</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 border-t-2 border-t-sky-400 space-y-2">
            <div className="text-xs font-bold text-sky-400 flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5" /> {currentSec.ipBlackBoxingTitle}
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">{currentSec.ipBlackBoxing}</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 border-t-2 border-t-purple-400 space-y-2">
            <div className="text-xs font-bold text-purple-400 flex items-center gap-1.5">
              <Database className="w-3.5 h-3.5" /> {currentSec.dataAirGapTitle}
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">{currentSec.dataAirGap}</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 border-t-2 border-t-amber-400 space-y-2">
            <div className="text-xs font-bold text-amber-400 flex items-center gap-1.5">
              <Scale className="w-3.5 h-3.5" /> {currentSec.governanceTitle}
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">{currentSec.governance}</p>
          </div>
        </div>
      </div>

      {/* 6 Board Supervisory Checklist Cards */}
      <div className="space-y-3">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <CheckSquare className="w-4 h-4 text-sky-400" />
          📋 C-Level &amp; Supervisory Board 6-Point Oversight Checklist
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {boardChecklist.map((item) => (
            <div
              key={item.id}
              className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-2.5 hover:border-slate-700 transition"
            >
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
                <span className="text-xs font-mono font-bold text-sky-400">{item.category}</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                  CHECK 0{item.id}
                </span>
              </div>
              <h4 className="text-sm font-bold text-white leading-snug">{item.action}</h4>
              <p className="text-xs text-slate-300 leading-relaxed bg-slate-950 p-3 rounded-xl border border-slate-800/80">
                {item.detail}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Final Executive Verdict Card */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-950 to-emerald-950/40 border border-emerald-800/60 text-center space-y-3">
        <div className="text-xs font-mono text-emerald-400 font-bold uppercase tracking-wider">
          FINAL STRATEGIC VERDICT FOR EUROPEAN INDUSTRY
        </div>
        <h3 className="text-lg font-bold text-white max-w-3xl mx-auto leading-relaxed">
          "China is no longer merely an assembly hub or a high-margin consumer market; it is a formidable state-backed technological competitor. European and Western industry must avoid the trap of abrupt cliff-edge exits, harness current cash flows to fund Western rebalancing, and execute a resolute <strong>'Phased De-risking (Scenario B)'</strong> to regain capital and technological sovereignty."
        </h3>
      </div>
    </div>
  );
};
