import React from 'react';
import { X, ArrowRight, ShieldCheck, TrendingDown, DollarSign, Building, AlertTriangle, CheckCircle2 } from 'lucide-react';
import collarData from '../../data/collar_strategy_steps.json';

interface CollarStrategyModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CollarStrategyModal: React.FC<CollarStrategyModalProps> = ({
  isOpen,
  onClose,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-5xl max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Modal Header */}
        <div className="sticky top-0 bg-slate-900/95 border-b border-slate-800 p-5 flex items-center justify-between z-10">
          <div>
            <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-rose-950/70 border border-rose-800/60 text-rose-300 text-xs font-mono font-bold mb-1">
              FINANCIAL ENGINEERING DECONSTRUCTION
            </div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              Geely’s 2018 Zero-Cost Collar &amp; SPV Stealth Acquisition Flow
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-8">
          {/* Top Summary Banner */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-3.5">
              <div className="text-[11px] font-mono text-slate-400 uppercase">Target Company</div>
              <div className="text-base font-bold text-white mt-1">Daimler AG (Mercedes)</div>
              <div className="text-xs text-slate-500">Stuttgart, Germany</div>
            </div>
            <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-3.5">
              <div className="text-[11px] font-mono text-slate-400 uppercase">Acquired Stake / Value</div>
              <div className="text-base font-bold text-rose-400 mt-1 font-mono">9.69% (~$9.0B / €7.3B)</div>
              <div className="text-xs text-slate-500">103,619,340 physical shares</div>
            </div>
            <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-3.5">
              <div className="text-[11px] font-mono text-slate-400 uppercase">Primary Intermediaries</div>
              <div className="text-sm font-bold text-sky-400 mt-1">Morgan Stanley &amp; BoA</div>
              <div className="text-xs text-slate-500">Prime Brokerage Equity Desks</div>
            </div>
            <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-3.5">
              <div className="text-[11px] font-mono text-slate-400 uppercase">SPV Shell Entity</div>
              <div className="text-sm font-bold text-amber-400 mt-1">Tenaciou3 Prospect Ltd</div>
              <div className="text-xs text-slate-500">Offshore Hong Kong SPV</div>
            </div>
          </div>

          {/* Collar Strategy Visual Formula */}
          <div className="bg-gradient-to-r from-blue-950/40 via-slate-900 to-purple-950/40 border border-blue-900/40 rounded-xl p-5">
            <h3 className="text-sm font-bold text-blue-300 uppercase tracking-wider font-mono mb-3 flex items-center gap-2">
              <DollarSign className="w-4 h-4 text-blue-400" />
              The Financial Calculus: How a Zero-Cost Collar Generates 85% LTV Leverage
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3.5">
                <div className="text-xs font-bold text-emerald-400 flex items-center gap-1.5 mb-1.5">
                  <ShieldCheck className="w-4 h-4" /> 1. Buy Put Option (Floor @ 95%)
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Locks in a minimum sale price. Even if Daimler shares collapse 50%, Geely can put shares back to the bank at 95% of value. Downside risk = 0%.
                </p>
              </div>

              <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3.5">
                <div className="text-xs font-bold text-purple-400 flex items-center gap-1.5 mb-1.5">
                  <TrendingDown className="w-4 h-4" /> 2. Sell Call Option (Cap @ 110%)
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Geely sells upside gains above 110%. The premium earned from selling calls exactly pays for the put option purchases (<strong>Net Option Premium = $0</strong>).
                </p>
              </div>

              <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3.5">
                <div className="text-xs font-bold text-amber-400 flex items-center gap-1.5 mb-1.5">
                  <Building className="w-4 h-4" /> 3. Collateralized Margin Loan (85% LTV)
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Because the bank holds 100% principal protection via the floor, it loans $7.5B+ against the shares without margin call liquidation risk. Geely only provided ~$1.5B equity.
                </p>
              </div>
            </div>
          </div>

          {/* Step-by-Step Acquisition Timeline */}
          <div>
            <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider font-mono mb-4 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-rose-400" />
              The 4-Step Stealth Acquisition Execution Flow
            </h3>

            <div className="space-y-4">
              {collarData.stages.map((stage) => (
                <div
                  key={stage.step}
                  className="bg-slate-950/90 border border-slate-800 rounded-xl p-4.5 hover:border-slate-700 transition"
                >
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-800/80 pb-2.5 mb-3">
                    <div className="flex items-center gap-3">
                      <span className="w-7 h-7 rounded-full bg-blue-600/20 text-blue-400 border border-blue-500/40 flex items-center justify-center text-xs font-mono font-bold">
                        {stage.step}
                      </span>
                      <span className="font-bold text-white text-sm">{stage.phase}</span>
                    </div>
                    <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-sky-300 border border-slate-700">
                      Action: {stage.action}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                    <div>
                      <span className="font-semibold text-slate-400 block mb-1">Execution Mechanism:</span>
                      <p className="text-slate-300 whitespace-pre-line">{stage.mechanism}</p>
                    </div>
                    <div>
                      <span className="font-semibold text-emerald-400 block mb-1">Financial Outcome:</span>
                      <p className="text-slate-300">{stage.outcome}</p>
                    </div>
                    <div>
                      <span className="font-semibold text-rose-400 block mb-1">German Regulatory Trigger:</span>
                      <p className="text-slate-400 bg-rose-950/30 p-2 rounded border border-rose-900/30 font-mono text-[11px]">
                        {stage.regulatoryTrigger}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Loopholes & Regulatory Reforms */}
          <div className="bg-slate-950 border border-slate-800 rounded-xl p-4.5">
            <h4 className="text-xs font-bold font-mono text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Exploited Loopholes &amp; Subsequent European Legal Reforms
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              {collarData.regulatoryLoopholesExploited.map((item, idx) => (
                <div key={idx} className="bg-slate-900/80 border border-slate-800 rounded-lg p-3 space-y-2">
                  <div className="font-bold text-amber-300">{item.loophole}</div>
                  <div>
                    <span className="text-rose-400 font-mono font-semibold">Pre-2018 Flaw: </span>
                    <span className="text-slate-400">{item.preFixLaw}</span>
                  </div>
                  <div>
                    <span className="text-emerald-400 font-mono font-semibold">Post-Fix Legal Reform: </span>
                    <span className="text-slate-300">{item.postFixReform}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="border-t border-slate-800 p-4 bg-slate-900/90 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition"
          >
            Close Investigation View
          </button>
        </div>
      </div>
    </div>
  );
};
