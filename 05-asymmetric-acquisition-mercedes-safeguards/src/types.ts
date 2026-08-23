export interface Shareholder {
  id: string;
  name: string;
  stakePct: number;
  sharesMillion: number;
  type: string;
  color: string;
  entryYear: number | null;
  peakYear: number | null;
  boardInfluence: string;
  details: string;
}

export interface ShareholderStructureData {
  totalSharesMillion: number;
  marketCapEurBillion: number;
  combinedChineseStakePct: number;
  shareholders: Shareholder[];
  agmAttendanceDynamics: {
    averageAgmAttendanceRatePct: number;
    effectiveChineseVotingPowerPct: number;
    explanation: string;
  };
}

export interface RegionalFinancial {
  region: string;
  units: number;
  sharePct: number;
  localBuiltBeijingBenz?: number;
  localBuilt?: number;
  importedUnits: number;
  flagshipConcentration: string;
  ebitContributionEurBillion: number;
  ebitSharePct: number;
}

export interface HistoricalFinancial {
  year: number;
  globalSalesK: number;
  chinaSalesK: number;
  chinaSharePct: number;
  groupRevenueEurB: number;
  groupEbitEurB: number;
  chinaEbitSharePct: number;
}

export interface CollarStage {
  step: number;
  phase: string;
  action: string;
  mechanism: string;
  outcome: string;
  regulatoryTrigger: string;
}

export interface SupplyChainProject {
  id: string;
  project: string;
  partner: string;
  establishedYear: number;
  headquarters: string;
  productionSite: string;
  mechanism: string;
  riskScore: string;
  strategicConsequence: string;
}

export interface CrossSectorSafeguard {
  id: string;
  sectorName: string;
  vulnerabilityProfile: string;
  threatVectors: string[];
  safeguards: {
    investmentScreening: string;
    supplyChainQuotas: string;
    dataAirGapping: string;
    corporateGovernance: string;
  };
}

export interface ThreeProngedConclusion {
  title: string;
  tag: string;
  color: string;
  summary: string;
}
