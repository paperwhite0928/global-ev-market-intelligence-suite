import React, { useState } from 'react';
import { SHAP_IMPORTANCE } from '../data/mockPanelGenerator';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  ZAxis,
  LineChart,
  Line,
  Legend
} from 'recharts';
import { Cpu, Award, Zap, HelpCircle } from 'lucide-react';

export const Tab3XGBoostShap: React.FC = () => {
  const [selectedFeature, setSelectedFeature] = useState<string>('public_chargers_per_million_capita');

  // Synthetic SHAP Dependence Data generator for chosen feature
  const dependenceData = React.useMemo(() => {
    const points: { x: number; shapValue: number; region: string }[] = [];
    const regions = ['US', 'EU', 'CN'];

    for (let i = 0; i < 150; i++) {
      const region = regions[i % 3];
      let xVal = 0;
      let shapVal = 0;

      if (selectedFeature === 'public_chargers_per_million_capita') {
        xVal = 200 + i * 10 + (Math.random() * 50 - 25);
        // Non-linear s-curve threshold
        shapVal = -0.3 + 0.8 / (1 + Math.exp(-(xVal - 600) / 120)) + (Math.random() * 0.1 - 0.05);
      } else if (selectedFeature === 'applied_tariff_rate_pct') {
        xVal = Math.max(0, i * 0.7 + (Math.random() * 5 - 2.5));
        // Penalty jump at 25% and 100%
        shapVal = -0.01 * xVal - (xVal > 25 ? 0.2 : 0) - (xVal > 90 ? 0.4 : 0) + (Math.random() * 0.08 - 0.04);
      } else if (selectedFeature === 'battery_pack_price_usd_kwh') {
        xVal = 85 + i * 0.5 + (Math.random() * 4 - 2);
        shapVal = 0.4 - 0.005 * xVal + (Math.random() * 0.06 - 0.03);
      } else if (selectedFeature === 'used_ev_depreciation_rate_pct') {
        xVal = 15 + i * 0.15 + (Math.random() * 2 - 1);
        shapVal = 0.2 - 0.018 * xVal + (Math.random() * 0.05 - 0.025);
      } else {
        // Lithium
        xVal = 8000 + i * 400 + (Math.random() * 2000 - 1000);
        shapVal = 0.15 - (xVal > 30000 ? 0.000012 * (xVal - 30000) : 0) + (Math.random() * 0.04 - 0.02);
      }

      points.push({ x: parseFloat(xVal.toFixed(1)), shapValue: parseFloat(shapVal.toFixed(3)), region });
    }

    return points;
  }, [selectedFeature]);

  // Actual vs Predicted 2025 Test Set Mock Time-Series
  const actualVsPredData = [
    { date: '2025-01', actual: 124500, predicted: 122100 },
    { date: '2025-02', actual: 128900, predicted: 127400 },
    { date: '2025-03', actual: 139200, predicted: 138000 },
    { date: '2025-04', actual: 142100, predicted: 143500 },
    { date: '2025-05', actual: 148000, predicted: 146800 },
    { date: '2025-06', actual: 156400, predicted: 155100 },
    { date: '2025-07', actual: 161000, predicted: 162300 },
    { date: '2025-08', actual: 167500, predicted: 165900 },
    { date: '2025-09', actual: 174200, predicted: 173100 },
    { date: '2025-10', actual: 181000, predicted: 182400 },
    { date: '2025-11', actual: 189500, predicted: 187900 },
    { date: '2025-12', actual: 198000, predicted: 196800 }
  ];

  return (
    <div className="space-y-6">
      {/* XGBoost Metrics Card */}
      <div className="bg-slate-800/90 border border-slate-700 rounded-xl p-5 shadow-lg">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-1.5 bg-purple-600/20 text-purple-400 rounded-lg border border-purple-500/30">
                <Cpu className="w-5 h-5" />
              </span>
              <h2 className="text-lg font-bold text-slate-100">
                XGBoost Regressor & SHAP TreeExplainer Model
              </h2>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Time-Series Validation Split: <strong className="text-slate-200">Train (2020–2024: 1,260 samples)</strong> | <strong className="text-slate-200">Test Holdout (2025: 252 samples)</strong>.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="bg-slate-900 px-4 py-2 rounded-lg border border-slate-700 text-center">
              <span className="text-[10px] text-slate-400 block uppercase font-medium">Test Set R²</span>
              <span className="text-lg font-bold text-emerald-400">0.912</span>
            </div>
            <div className="bg-slate-900 px-4 py-2 rounded-lg border border-slate-700 text-center">
              <span className="text-[10px] text-slate-400 block uppercase font-medium">RMSE</span>
              <span className="text-lg font-bold text-blue-400">1,420 <span className="text-xs font-normal">units</span></span>
            </div>
            <div className="bg-slate-900 px-4 py-2 rounded-lg border border-slate-700 text-center">
              <span className="text-[10px] text-slate-400 block uppercase font-medium">MAE</span>
              <span className="text-lg font-bold text-amber-400">1,080 <span className="text-xs font-normal">units</span></span>
            </div>
          </div>
        </div>
      </div>

      {/* SHAP Global Importance Bar Chart */}
      <div className="bg-slate-800/90 border border-slate-700 rounded-xl p-5 shadow-lg">
        <div className="mb-4">
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Award className="w-5 h-5 text-emerald-400" />
            SHAP Global Feature Importance (|mean SHAP value|)
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Quantifies the average marginal contribution of each driver variable to the log BEV sales prediction.
          </p>
        </div>

        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={SHAP_IMPORTANCE}
              layout="vertical"
              margin={{ top: 5, right: 30, left: 180, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis type="number" stroke="#94A3B8" tick={{ fontSize: 11 }} />
              <YAxis
                type="category"
                dataKey="label"
                stroke="#94A3B8"
                tick={{ fontSize: 11 }}
                width={170}
              />
              <Tooltip
                contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '0.5rem', color: '#F8FAFC' }}
                formatter={(val: any) => [Number(val).toFixed(3), 'mean |SHAP| impact']}
              />
              <Bar dataKey="importance" fill="#10B981" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* SHAP Dependence Plot */}
      <div className="bg-slate-800/90 border border-slate-700 rounded-xl p-5 shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
          <div>
            <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <Zap className="w-5 h-5 text-amber-400" />
              Interactive SHAP Dependence Scatter Plot
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Examines non-linear marginal effects and threshold boundaries for specific input variables.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400">Select Variable:</span>
            <select
              value={selectedFeature}
              onChange={(e) => setSelectedFeature(e.target.value)}
              className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-1.5 focus:outline-none focus:border-blue-500"
            >
              <option value="public_chargers_per_million_capita">Public Chargers Density</option>
              <option value="applied_tariff_rate_pct">Applied Tariff Rate (%)</option>
              <option value="battery_pack_price_usd_kwh">Battery Pack Price ($/kWh)</option>
              <option value="used_ev_depreciation_rate_pct">Used EV Depreciation Rate (%)</option>
              <option value="lithium_carbonate_price_usd_ton">Lithium Carbonate Price ($/ton)</option>
            </select>
          </div>
        </div>

        <div className="h-72 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 10, right: 20, left: 10, bottom: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis
                type="number"
                dataKey="x"
                name="Variable Value"
                stroke="#94A3B8"
                tick={{ fontSize: 11 }}
              />
              <YAxis
                type="number"
                dataKey="shapValue"
                name="SHAP Value"
                stroke="#94A3B8"
                tick={{ fontSize: 11 }}
                label={{ value: 'SHAP Value (log sales impact)', angle: -90, position: 'insideLeft', fill: '#94A3B8', fontSize: 11 }}
              />
              <ZAxis range={[30, 30]} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '0.5rem', color: '#F8FAFC' }}
                cursor={{ strokeDasharray: '3 3' }}
              />
              <Scatter name="SHAP Samples" data={dependenceData} fill="#3B82F6" opacity={0.75} />
            </ScatterChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-3 bg-slate-900/60 p-3 rounded-lg border border-slate-700/60 text-xs text-slate-300 flex items-start gap-2">
          <HelpCircle className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
          <div>
            <strong>SHAP Dependence Insight:</strong>{' '}
            {selectedFeature === 'public_chargers_per_million_capita' &&
              'Non-linear threshold: Increasing charger density from 200 to 600 per million capita generates the steepest positive demand inflection, after which marginal gains gradually saturate.'}
            {selectedFeature === 'applied_tariff_rate_pct' &&
              'Discontinuous penalty: Tariff rates below 15% show minimal demand friction, whereas tariffs exceeding 25% (EU Chinese duties) and 100% (US Biden tariffs) trigger steep negative demand jumps.'}
            {selectedFeature === 'battery_pack_price_usd_kwh' &&
              'Monotonic cost curve: Declining battery prices below $100/kWh unlock mass-market parity, accelerating positive SHAP contributions.'}
            {selectedFeature === 'used_ev_depreciation_rate_pct' &&
              'Resale risk penalty: When used EV depreciation exceeds 25% annually, total cost of ownership (TCO) anxiety severely dampens new car purchases.'}
            {selectedFeature === 'lithium_carbonate_price_usd_ton' &&
              'Commodity price threshold: Lithium prices below $25,000/ton exert minimal drag, but severe spikes above $50,000/ton (2022 shock) create lagged battery pack price increases.'}
          </div>
        </div>
      </div>

      {/* 2025 Test Set Actual vs Predicted Chart */}
      <div className="bg-slate-800/90 border border-slate-700 rounded-xl p-5 shadow-lg">
        <div className="mb-4">
          <h3 className="text-base font-bold text-slate-100">
            2025 Test Holdout Set: Actual vs. XGBoost Predicted Sales
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Out-of-sample forecast validation evaluating generalizability on 2025 test dataset.
          </p>
        </div>

        <div className="h-64 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={actualVsPredData} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="date" stroke="#94A3B8" tick={{ fontSize: 11 }} />
              <YAxis stroke="#94A3B8" tick={{ fontSize: 11 }} tickFormatter={(val) => `${(val / 1000).toFixed(0)}k`} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '0.5rem', color: '#F8FAFC' }}
                formatter={(val: any) => [Number(val).toLocaleString() + ' units', 'Sales']}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              <Line type="monotone" dataKey="actual" name="Actual BEV Sales" stroke="#10B981" strokeWidth={2.5} dot={{ r: 4 }} />
              <Line type="monotone" dataKey="predicted" name="XGBoost Predicted" stroke="#8B5CF6" strokeWidth={2} strokeDasharray="5 5" dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
