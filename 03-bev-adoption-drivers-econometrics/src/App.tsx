import { useState, useMemo } from 'react';
import { generatePanelDataset } from './data/mockPanelGenerator';
import { Header } from './components/Header';
import { Tab1DataInspection } from './components/Tab1DataInspection';
import { Tab2Econometrics } from './components/Tab2Econometrics';
import { Tab3XGBoostShap } from './components/Tab3XGBoostShap';
import { Tab4ScenarioSimulator } from './components/Tab4ScenarioSimulator';
import { PythonCodeModal } from './components/PythonCodeModal';

export default function App() {
  const allRegions = ['US', 'EU', 'CN'];
  const allOEMs = [
    'Tesla',
    'BYD',
    'Volkswagen Group',
    'Hyundai-Kia Group',
    'BMW Group',
    'Mercedes-Benz Group',
    'Toyota'
  ];

  const [selectedRegions, setSelectedRegions] = useState<string[]>(allRegions);
  const [selectedOEMs, setSelectedOEMs] = useState<string[]>(allOEMs);
  const [activeTab, setActiveTab] = useState<number>(1);
  const [isCodeModalOpen, setIsCodeModalOpen] = useState<boolean>(false);

  // Generate full dataset once
  const fullDataset = useMemo(() => generatePanelDataset(), []);

  // Filter dataset by regions and OEMs
  const filteredDataset = useMemo(() => {
    return fullDataset.filter(
      (r) => selectedRegions.includes(r.region) && selectedOEMs.includes(r.company)
    );
  }, [fullDataset, selectedRegions, selectedOEMs]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-blue-600 selection:text-white">
      {/* Navigation & Header */}
      <Header
        selectedRegions={selectedRegions}
        setSelectedRegions={setSelectedRegions}
        selectedOEMs={selectedOEMs}
        setSelectedOEMs={setSelectedOEMs}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenCodeModal={() => setIsCodeModalOpen(true)}
        allRegions={allRegions}
        allOEMs={allOEMs}
        totalRowsCount={filteredDataset.length}
      />

      {/* Main Tab Content Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 1 && <Tab1DataInspection data={filteredDataset} />}
        {activeTab === 2 && <Tab2Econometrics />}
        {activeTab === 3 && <Tab3XGBoostShap />}
        {activeTab === 4 && <Tab4ScenarioSimulator />}
      </main>

      {/* Python Code Modal */}
      <PythonCodeModal
        isOpen={isCodeModalOpen}
        onClose={() => setIsCodeModalOpen(false)}
      />

      {/* Footer */}
      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        <p>
          Global BEV Adoption Drivers Analysis Platform • Econometric Panel Fixed-Effects OLS & Machine Learning Pipeline
        </p>
      </footer>
    </div>
  );
}
