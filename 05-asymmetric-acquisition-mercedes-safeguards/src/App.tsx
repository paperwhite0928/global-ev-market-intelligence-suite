import React, { useState } from 'react';
import { Header } from './components/Header';
import { Tab2PeakVsPresent } from './components/Tab2PeakVsPresent';
import { Tab1TriadOverview } from './components/Tab1TriadOverview';
import { Tab1OwnershipMatrix } from './components/Tab1OwnershipMatrix';
import { Tab3IdarStrategy } from './components/Tab3IdarStrategy';
import { TechnologyFlowMatrix } from './components/TechnologyFlowMatrix';
import { Tab3BifurcationScenarios } from './components/Tab3BifurcationScenarios';
import { Tab3LockinDualTrack } from './components/Tab3LockinDualTrack';
import { Tab2FinancialDependency } from './components/Tab2FinancialDependency';
import { MultiVariablePolicySandbox } from './components/MultiVariablePolicySandbox';
import { Tab5CrossIndustryPlaybook } from './components/Tab5CrossIndustryPlaybook';
import { Tab5ExecutiveConclusion } from './components/Tab5ExecutiveConclusion';

export default function App() {
  const [activeTab, setActiveTab] = useState<number>(1);

  return (
    <div className="min-h-screen bg-[#070b12] text-slate-100 font-sans selection:bg-blue-600 selection:text-white flex flex-col justify-between">
      <div>
        {/* Navigation & Header */}
        <Header activeTab={activeTab} setActiveTab={setActiveTab} />

        {/* Main Tab Content Container */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
          {/* Tab 1: 2019-2025 Market Collapse & Quantitative Dependency */}
          {activeTab === 1 && <Tab2PeakVsPresent />}

          {/* Tab 2: Triad Encroachment & Hostage Dilemmas */}
          {activeTab === 2 && (
            <div className="space-y-6">
              <Tab1TriadOverview />
              <Tab1OwnershipMatrix />
            </div>
          )}

          {/* Tab 3: China's Asymmetric Openness & IDAR Framework */}
          {activeTab === 3 && <Tab3IdarStrategy />}

          {/* Tab 4: Technology Exfiltration & Reverse Flow Dynamics */}
          {activeTab === 4 && <TechnologyFlowMatrix />}

          {/* Tab 5: 3 Strategic Scenarios & Interactive Simulation Engine */}
          {activeTab === 5 && <Tab3BifurcationScenarios />}

          {/* Tab 6: Sunk Capital (€45B) & 'In China for China' Dual-Track Air-Gap */}
          {activeTab === 6 && (
            <div className="space-y-6">
              <Tab3LockinDualTrack />
              <Tab2FinancialDependency />
            </div>
          )}

          {/* Tab 7: 5 Strategic Truths & Policy Actions */}
          {activeTab === 7 && <MultiVariablePolicySandbox />}

          {/* Tab 8: Cross-Industry Safeguards & Board Verdict */}
          {activeTab === 8 && (
            <div className="space-y-6">
              <Tab5CrossIndustryPlaybook />
              <Tab5ExecutiveConclusion />
            </div>
          )}
        </main>
      </div>

      {/* Footer with Audited Metadata */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4">
          <p>
            China Tech-Absorption (IDAR) &amp; Asymmetric Lock-in: German Auto Triad Dependency &amp; Safeguards (2019–2025)
          </p>
          <p className="mt-1 text-[11px] text-slate-600">
            Core Thesis: Phased De-risking of Structural Chinese Dependency and Restoration of Western Strategic Autonomy • Audited Institutional Baseline
          </p>
        </div>
      </footer>
    </div>
  );
}
