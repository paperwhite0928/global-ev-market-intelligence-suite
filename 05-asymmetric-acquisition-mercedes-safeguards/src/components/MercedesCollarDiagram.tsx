import React, { useState } from 'react';
import { DollarSign, Shield, ArrowRight, TrendingDown, Building, AlertTriangle, CheckCircle } from 'lucide-react';

export const MercedesCollarDiagram: React.FC = () => {
  const [activeStep, setActiveStep] = useState<number>(3);

  const steps = [
    {
      num: 1,
      title: 'Friendly Rejection (Late 2017)',
      actor: 'Li Shufu / Geely ➔ Daimler AG',
      desc: 'Geely offered to buy a 5% new share issue at a discount. Daimler board refused dilution: "Buy on the open market if you want shares."',
      badge: 'DIRECT APPROACH BLOCKED',
      badgeColor: 'bg-slate-800 text-slate-300'
    },
    {
      num: 2,
      title: 'Offshore SPV & Synthetic Swaps',
      actor: 'SPV Tenaciou3 + Morgan Stanley / BoA',
      desc: 'Geely created offshore SPV "Tenaciou3 Prospect Investment Ltd" in Hong Kong. Prime brokers quietly bought shares & cash-settled equity swaps below 3% disclosure limits.',
      badge: 'WpHG 3% DISCLOSURE EVADED',
      badgeColor: 'bg-amber-950 text-amber-300 border border-amber-800'
    },
    {
      num: 3,
      title: 'Zero-Cost Collar & 85% Bank LTV',
      actor: 'Derivatives: Put @ 95% + Call @ 110%',
      desc: 'Geely bought 95% put options (eliminating downside risk) and sold 110% call options (funding puts at $0 net premium). Banks provided $7.5B in 85% LTV margin loans.',
      badge: '$9B BLOCK CONTROLLED WITH $1.5B EQUITY',
      badgeColor: 'bg-rose-950 text-rose-300 border border-rose-800'
    },
    {
      num: 4,
      title: 'Overnight Exercise & 9.69% Shock',
      actor: 'Tenaciou3 converts swaps into physical stock',
      desc: 'On Feb 23, 2018, Geely exercised synthetic rights over a single weekend, filing a sudden 9.69% disclosure with BaFin and becoming Daimler\'s largest single shareholder.',
      badge: 'LARGEST SINGLE SHAREHOLDER OVERNIGHT',
      badgeColor: 'bg-purple-950 text-purple-300 border border-purple-800'
    }
  ];

  return (
    <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-4">
        <div>
          <div className="text-xs font-mono font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
            <DollarSign className="w-4 h-4 text-rose-400" />
            FINANCIAL DERIVATIVE ENGINEERING DECONSTRUCTION
          </div>
          <h3 className="text-lg font-black text-white mt-1">
            Geely's 2018 Zero-Cost Collar &amp; SPV Tenaciou3 Mechanism
          </h3>
        </div>
        <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-900 text-slate-300 border border-slate-700">
          Target: Daimler AG (Mercedes-Benz)
        </span>
      </div>

      {/* Interactive Step Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
        {steps.map((s) => (
          <button
            key={s.num}
            onClick={() => setActiveStep(s.num)}
            className={`p-3 rounded-xl border text-left transition flex flex-col justify-between ${
              activeStep === s.num
                ? 'bg-rose-950/60 border-rose-500 text-white shadow-lg shadow-rose-950/40'
                : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-900'
            }`}
          >
            <div className="flex items-center justify-between mb-1">
              <span className="w-5 h-5 rounded-full bg-slate-800 text-[11px] font-mono font-bold flex items-center justify-center">
                {s.num}
              </span>
              <span className="text-[10px] font-mono">{activeStep === s.num ? 'Active' : ''}</span>
            </div>
            <div className="text-xs font-bold truncate">{s.title.split('(')[0]}</div>
          </button>
        ))}
      </div>

      {/* Active Step Details Box */}
      {(() => {
        const cur = steps.find((s) => s.num === activeStep) || steps[2];
        return (
          <div className="p-5 rounded-xl bg-slate-900/90 border border-slate-700 space-y-4 animate-in fade-in duration-200">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
              <h4 className="text-base font-bold text-white flex items-center gap-2">
                <span className="text-rose-400 font-mono">Step 0{cur.num}:</span> {cur.title}
              </h4>
              <span className={`text-[11px] font-mono font-bold px-2.5 py-0.5 rounded ${cur.badgeColor}`}>
                {cur.badge}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="space-y-1.5">
                <span className="text-slate-400 font-semibold block">Key Financial Counterparties &amp; Instruments:</span>
                <p className="text-sky-300 font-mono bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                  {cur.actor}
                </p>
              </div>
              <div className="space-y-1.5">
                <span className="text-slate-400 font-semibold block">Tactical Execution Detail:</span>
                <p className="text-slate-200 bg-slate-950 p-2.5 rounded-lg border border-slate-800 leading-relaxed">
                  {cur.desc}
                </p>
              </div>
            </div>

            {/* Visual Collar Formula Box for Step 3 */}
            {cur.num === 3 && (
              <div className="p-4 rounded-xl bg-gradient-to-r from-rose-950/40 via-slate-950 to-blue-950/40 border border-rose-900/40 grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                  <div className="font-bold text-emerald-400 mb-1">1. Long Daimler + Buy Put (95%)</div>
                  <p className="text-slate-300 text-[11px]">Guarantees floor value. Bank has zero principal loss risk.</p>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                  <div className="font-bold text-purple-400 mb-1">2. Sell Call (110%)</div>
                  <p className="text-slate-300 text-[11px]">Call premium funds put purchase ($0 Net Cost Collar).</p>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                  <div className="font-bold text-amber-400 mb-1">3. Non-Recourse 85% LTV Loan</div>
                  <p className="text-slate-300 text-[11px]">Morgan Stanley/BoA lend $7.5B against protected shares.</p>
                </div>
              </div>
            )}
          </div>
        );
      })()}
    </div>
  );
};
