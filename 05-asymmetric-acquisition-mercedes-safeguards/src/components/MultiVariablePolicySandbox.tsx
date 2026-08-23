import React from 'react';
import { Lightbulb, ShieldAlert, TrendingDown, Scale, Lock, DollarSign } from 'lucide-react';

export const MultiVariablePolicySandbox: React.FC = () => {
  const coreInsights = [
    {
      id: 1,
      tag: "TRUTH 01: TARIFF PARADOX",
      title: "1. Unilateral Countervailing Duties Fail to Protect Western OEMs and Amplify Backfire Risks",
      icon: <ShieldAlert className="w-5 h-5 text-rose-400" />,
      color: "border-rose-900/50 bg-rose-950/20",
      takeaway: "As demonstrated by BMW Shenyang (iX3), Western OEMs re-exporting finished vehicles from China bear the primary financial burden of EU countervailing tariffs (20.7%).",
      detail: "Chinese competitors circumvent border tariffs by establishing greenfield assembly facilities in Eastern Europe (e.g., BYD in Hungary, Geely in Poland), while European OEMs re-exporting vehicles from China suffer compressed margins. Standalone border duties cannot protect industrial sovereignty without localized production incentives."
    },
    {
      id: 2,
      tag: "TRUTH 02: THE COST OF DECOUPLING",
      title: "2. Immediate Cliff-Edge Decoupling Represents an Irreversible Economic Self-Harm",
      icon: <TrendingDown className="w-5 h-5 text-amber-400" />,
      color: "border-amber-900/50 bg-amber-950/20",
      takeaway: "Abruptly abandoning €45.0B in cumulative sunk CapEx and €12.8B in annual JV dividend inflows instantly starves Western headquarters of transition R&D capital.",
      detail: "Western EV manufacturing remains structurally 20–30% more expensive without Chinese scale. A phased, managed rebalancing—using current joint venture cash flows to finance the transition of Western manufacturing footprints—is the only economically viable path."
    },
    {
      id: 3,
      tag: "TRUTH 03: GOVERNANCE DEFENSE",
      title: "3. Countering Asymmetric IDAR Requires Prioritizing Capital Governance (AktG §179)",
      icon: <Scale className="w-5 h-5 text-sky-400" />,
      color: "border-sky-900/50 bg-sky-950/20",
      takeaway: "A 19.67% non-EU equity stake commands a 35.8% voting share during low AGM attendance (~55%), securing a blocking minority (>25%) under German Corporate Law (§179 AktG).",
      detail: "Executing 15% strategic capital dilution and mobilizing proxy turnout to achieve total AGM turnout >= 70.0% (or allied-only turnout >= 85.0%) reduces effective voting power to 24.43% (<25.0%), dismantling blocking vetoes and restoring board restructuring autonomy."
    },
    {
      id: 4,
      tag: "TRUTH 04: SUPPLY CHAIN ALLIANCE",
      title: "4. Unit Battery Cost Premiums (+€1,944/EV) Must Be Mitigated via Multilateral Sourcing Alliances",
      icon: <DollarSign className="w-5 h-5 text-purple-400" />,
      color: "border-purple-900/50 bg-purple-950/20",
      takeaway: "Upstream raw material concentration (65% Lithium refining, 90% Graphite) and LFP manufacturing scale create structural cost penalties individual OEM balance sheets cannot absorb alone.",
      detail: "OEMs and policymakers must scale CRMA and IRA-compliant procurement alliances (integrating European in-house cell initiatives, Japanese, and Korean Tier-1 suppliers) to establish non-monopolistic scale parity and hedge upstream processing risks."
    },
    {
      id: 5,
      tag: "TRUTH 05: DATA AIR-GAP MANDATE",
      title: "5. 'In China for China' Dual-Track Architecture is the Core of Technological Data Air-Gapping",
      icon: <Lock className="w-5 h-5 text-emerald-400" />,
      color: "border-emerald-900/50 bg-emerald-950/20",
      takeaway: "Mandatory compliance with PRC Intelligence Law (Art. 7) prevents a single unified software stack from serving both mainland and Western defense-aligned markets.",
      detail: "Formally bifurcate system architectures: deploy 100% localized digital ecosystems for the mainland domestic market, while mandating hardware-level and NATO-certified sovereign data air-gapping (zero foreign peering) for global vehicle fleets."
    }
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Top Hero Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 relative overflow-hidden">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-950/60 border border-amber-800/50 text-amber-300 text-xs font-mono font-bold">
            <Lightbulb className="w-3.5 h-3.5" />
            STRATEGIC IMPLICATIONS &amp; EXECUTIVE TRUTHS
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            5 Executive Strategic Truths &amp; Policy Action Framework
          </h2>
          <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
            Beyond theoretical modeling, this econometric suite provides C-Suite executives and European policymakers with <strong>5 actionable empirical truths and decisive policy directives</strong>.
          </p>
        </div>
      </div>

      {/* 5 Core Strategic Insights Grid */}
      <div className="space-y-4">
        {coreInsights.map((insight) => (
          <div
            key={insight.id}
            className={`p-6 rounded-2xl border ${insight.color} space-y-3 hover:border-slate-700 transition`}
          >
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
              <span className="text-xs font-mono font-bold text-slate-400">{insight.tag}</span>
              <div className="p-1.5 rounded-lg bg-slate-950 border border-slate-800">
                {insight.icon}
              </div>
            </div>

            <h3 className="text-lg font-bold text-white leading-snug">{insight.title}</h3>

            <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800/90 text-xs text-amber-300 font-medium leading-relaxed">
              🎯 <strong>Core Takeaway:</strong> {insight.takeaway}
            </div>

            <p className="text-xs text-slate-300 leading-relaxed pl-1">
              {insight.detail}
            </p>
          </div>
        ))}
      </div>

      {/* Bottom Summary Callout */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-950 to-blue-950/40 border border-slate-800 text-center space-y-2">
        <div className="text-xs font-mono text-sky-400 font-bold uppercase">Final Strategic Directive</div>
        <h4 className="text-base font-bold text-white max-w-2xl mx-auto">
          "Neither passive appeasement (Status Quo) nor emotional abrupt exit solves the crisis. Harnessing current cash flows while executing a resolute 'Phased De-risking' with sovereign capital and data air-gaps is the only viable path to long-term industrial victory."
        </h4>
      </div>
    </div>
  );
};
