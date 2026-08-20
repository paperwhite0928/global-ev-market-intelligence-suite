import React, { useState, useMemo } from 'react';
import { PanelRecord } from '../types';
import { LAG_CORRELATIONS } from '../data/mockPanelGenerator';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { Download, Search, ChevronLeft, ChevronRight, Layers, Table as TableIcon } from 'lucide-react';

interface Tab1Props {
  data: PanelRecord[];
}

export const Tab1DataInspection: React.FC<Tab1Props> = ({ data }) => {
  const [groupBy, setGroupBy] = useState<'region' | 'company'>('region');
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 12;

  // KPI calculations
  const totalSales = useMemo(() => data.reduce((acc, r) => acc + r.bev_sales, 0), [data]);
  const avgBatteryPrice = useMemo(() => {
    if (!data.length) return 0;
    return data.reduce((acc, r) => acc + r.battery_pack_price_usd_kwh, 0) / data.length;
  }, [data]);
  const avgChargerDensity = useMemo(() => {
    if (!data.length) return 0;
    return data.reduce((acc, r) => acc + r.public_chargers_per_million_capita, 0) / data.length;
  }, [data]);
  const avgTariff = useMemo(() => {
    if (!data.length) return 0;
    return data.reduce((acc, r) => acc + r.applied_tariff_rate_pct, 0) / data.length;
  }, [data]);
  const avgInterest = useMemo(() => {
    if (!data.length) return 0;
    return data.reduce((acc, r) => acc + r.interest_rate_pct, 0) / data.length;
  }, [data]);

  // Aggregate sales by month and group
  const chartData = useMemo(() => {
    const timeMap: { [date: string]: { [groupKey: string]: number } } = {};
    const keysSet = new Set<string>();

    data.forEach((r) => {
      const date = r.year_month;
      const key = r[groupBy];
      keysSet.add(key);

      if (!timeMap[date]) {
        timeMap[date] = {};
      }
      timeMap[date][key] = (timeMap[date][key] || 0) + r.bev_sales;
    });

    const result = Object.keys(timeMap)
      .sort()
      .map((date) => {
        const row: any = { date };
        keysSet.forEach((k) => {
          row[k] = timeMap[date][k] || 0;
        });
        return row;
      });

    return { result, keys: Array.from(keysSet) };
  }, [data, groupBy]);

  // Table filtering and pagination
  const filteredRows = useMemo(() => {
    if (!searchTerm) return data;
    const term = searchTerm.toLowerCase();
    return data.filter(
      (r) =>
        r.region.toLowerCase().includes(term) ||
        r.company.toLowerCase().includes(term) ||
        r.year_month.includes(term)
    );
  }, [data, searchTerm]);

  const totalPages = Math.ceil(filteredRows.length / pageSize) || 1;
  const paginatedRows = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return filteredRows.slice(start, start + pageSize);
  }, [filteredRows, currentPage]);

  const exportCSV = () => {
    if (!data.length) return;
    const headers = Object.keys(data[0]).join(',');
    const rows = data.map((r) => Object.values(r).join(',')).join('\n');
    const blob = new Blob([`${headers}\n${rows}`], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'bev_panel_dataset_export.csv';
    a.click();
  };

  const OEM_COLORS: { [key: string]: string } = {
    'BYD': '#E11D48',
    'Tesla': '#7C3AED',
    'Volkswagen Group': '#00A8A8',
    'Hyundai-Kia Group': '#1D4ED8',
    'BMW Group': '#475569',
    'Mercedes-Benz Group': '#94A3B8',
    'Toyota': '#FB923C',
    'US': '#3B82F6',
    'EU': '#10B981',
    'CN': '#EF4444'
  };

  const lineColors = ['#E11D48', '#7C3AED', '#00A8A8', '#1D4ED8', '#475569', '#94A3B8', '#FB923C'];

  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-4 shadow-md">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider block">Total BEV Sales</span>
          <div className="text-2xl font-bold text-slate-100 mt-1">
            {totalSales.toLocaleString()} <span className="text-xs font-normal text-slate-400">units</span>
          </div>
          <span className="text-[11px] text-emerald-400 mt-1 block">72-Month Aggregated Sales</span>
        </div>

        <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-4 shadow-md">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider block">Avg Battery Price</span>
          <div className="text-2xl font-bold text-blue-400 mt-1">
            ${avgBatteryPrice.toFixed(1)} <span className="text-xs font-normal text-slate-400">/kWh</span>
          </div>
          <span className="text-[11px] text-slate-400 mt-1 block">Pack-Level Average</span>
        </div>

        <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-4 shadow-md">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider block">Avg Charger Density</span>
          <div className="text-2xl font-bold text-emerald-400 mt-1">
            {avgChargerDensity.toFixed(0)} <span className="text-xs font-normal text-slate-400">/M pop</span>
          </div>
          <span className="text-[11px] text-slate-400 mt-1 block">Public Infrastructure</span>
        </div>

        <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-4 shadow-md">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider block">Avg Tariff Rate</span>
          <div className="text-2xl font-bold text-amber-400 mt-1">
            {avgTariff.toFixed(1)}%
          </div>
          <span className="text-[11px] text-slate-400 mt-1 block">Applied Trade Duties</span>
        </div>

        <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-4 shadow-md">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider block">Avg Interest Rate</span>
          <div className="text-2xl font-bold text-purple-400 mt-1">
            {avgInterest.toFixed(2)}%
          </div>
          <span className="text-[11px] text-slate-400 mt-1 block">Central Bank Policy</span>
        </div>
      </div>

      {/* Monthly Sales Time Series Chart */}
      <div className="bg-slate-800/90 border border-slate-700 rounded-xl p-5 shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
          <div>
            <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <Layers className="w-5 h-5 text-blue-400" />
              Monthly BEV Unit Sales Trend (2020 – 2025)
            </h2>
            <p className="text-xs text-slate-400">
              Aggregated monthly BEV sales volume across selected filters
            </p>
          </div>

          <div className="flex items-center gap-2 bg-slate-900 p-1 rounded-lg border border-slate-700">
            <span className="text-xs text-slate-400 px-2">Group By:</span>
            <button
              onClick={() => setGroupBy('region')}
              className={`px-3 py-1 text-xs font-medium rounded-md transition-all ${
                groupBy === 'region' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'
              }`}
            >
              Region
            </button>
            <button
              onClick={() => setGroupBy('company')}
              className={`px-3 py-1 text-xs font-medium rounded-md transition-all ${
                groupBy === 'company' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-white'
              }`}
            >
              OEM
            </button>
          </div>
        </div>

        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData.result} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="date" stroke="#94A3B8" tick={{ fontSize: 11 }} interval={5} />
              <YAxis stroke="#94A3B8" tick={{ fontSize: 11 }} tickFormatter={(val) => `${(val / 1000).toFixed(0)}k`} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '0.5rem', color: '#F8FAFC' }}
                formatter={(val: any) => [Number(val).toLocaleString() + ' units', 'Sales']}
              />
              <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
              {chartData.keys.map((key, idx) => (
                <Line
                  key={key}
                  type="monotone"
                  dataKey={key}
                  name={key}
                  stroke={OEM_COLORS[key] || lineColors[idx % lineColors.length]}
                  strokeWidth={2.4}
                  dot={false}
                  activeDot={{ r: 5 }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Lag Correlation Table / Matrix */}
      <div className="bg-slate-800/90 border border-slate-700 rounded-xl p-5 shadow-lg">
        <div className="mb-4">
          <h2 className="text-base font-bold text-slate-100">
            Lag Cross-Correlation Matrix against Target (<code className="text-blue-400 font-mono">bev_sales</code>)
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Evaluates lead/lag dependencies at 0, 1, 3, and 6-month horizons to detect delayed transmission of price and policy shocks.
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300 border-collapse">
            <thead>
              <tr className="bg-slate-900/80 border-b border-slate-700 text-slate-400 font-semibold uppercase tracking-wider">
                <th className="py-3 px-4">Independent Driver Variable</th>
                <th className="py-3 px-4 text-center">Lag 0 (Current)</th>
                <th className="py-3 px-4 text-center">Lag 1 Month</th>
                <th className="py-3 px-4 text-center">Lag 3 Months</th>
                <th className="py-3 px-4 text-center">Lag 6 Months</th>
                <th className="py-3 px-4">Trend Insight</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/50">
              {LAG_CORRELATIONS.map((row) => (
                <tr key={row.driver} className="hover:bg-slate-700/30 transition-colors">
                  <td className="py-3 px-4 font-semibold text-slate-100">{row.label}</td>
                  <td className="py-3 px-4 text-center font-mono font-medium">
                    <span className={row.lag0 >= 0 ? 'text-emerald-400' : 'text-rose-400'}>
                      {row.lag0 > 0 ? `+${row.lag0.toFixed(2)}` : row.lag0.toFixed(2)}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-center font-mono font-medium">
                    <span className={row.lag1 >= 0 ? 'text-emerald-400' : 'text-rose-400'}>
                      {row.lag1 > 0 ? `+${row.lag1.toFixed(2)}` : row.lag1.toFixed(2)}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-center font-mono font-medium">
                    <span className={row.lag3 >= 0 ? 'text-emerald-400' : 'text-rose-400'}>
                      {row.lag3 > 0 ? `+${row.lag3.toFixed(2)}` : row.lag3.toFixed(2)}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-center font-mono font-medium">
                    <span className={row.lag6 >= 0 ? 'text-emerald-400' : 'text-rose-400'}>
                      {row.lag6 > 0 ? `+${row.lag6.toFixed(2)}` : row.lag6.toFixed(2)}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-xs text-slate-400">
                    {Math.abs(row.lag6) > Math.abs(row.lag0) ? (
                      <span className="text-amber-400/90 font-medium">Stronger delayed impact at 6-mo lag</span>
                    ) : (
                      <span className="text-slate-400">Immediate contemporaneous effect dominant</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Raw Panel Dataset Inspection Table */}
      <div className="bg-slate-800/90 border border-slate-700 rounded-xl p-5 shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
          <div>
            <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <TableIcon className="w-5 h-5 text-blue-400" />
              Raw Panel Dataset ({filteredRows.length} Records)
            </h2>
            <p className="text-xs text-slate-400">
              Monthly observations indexed by Date, Region, and Company
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value);
                  setCurrentPage(1);
                }}
                placeholder="Search region, OEM, or date..."
                className="pl-9 pr-3 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-blue-500 w-48 sm:w-64"
              />
            </div>

            <button
              onClick={exportCSV}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-medium transition-colors shadow-sm"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export CSV</span>
            </button>
          </div>
        </div>

        <div className="overflow-x-auto border border-slate-700/80 rounded-lg">
          <table className="w-full text-left text-xs text-slate-300">
            <thead>
              <tr className="bg-slate-900 border-b border-slate-700 text-slate-400 font-semibold uppercase tracking-wider">
                <th className="py-2.5 px-3">Date</th>
                <th className="py-2.5 px-3">Region</th>
                <th className="py-2.5 px-3">Company</th>
                <th className="py-2.5 px-3 text-right">BEV Sales</th>
                <th className="py-2.5 px-3 text-right">Battery ($/kWh)</th>
                <th className="py-2.5 px-3 text-right">Chargers (/M cap)</th>
                <th className="py-2.5 px-3 text-right">Tariff (%)</th>
                <th className="py-2.5 px-3 text-right">Used Depr (%)</th>
                <th className="py-2.5 px-3 text-right">Interest (%)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {paginatedRows.map((r, i) => (
                <tr key={`${r.year_month}-${r.region}-${r.company}-${i}`} className="hover:bg-slate-700/20 font-mono">
                  <td className="py-2 px-3 text-slate-200">{r.year_month}</td>
                  <td className="py-2 px-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-700 text-blue-300">
                      {r.region}
                    </span>
                  </td>
                  <td className="py-2 px-3 text-slate-200 font-sans">{r.company}</td>
                  <td className="py-2 px-3 text-right font-bold text-emerald-400">
                    {r.bev_sales.toLocaleString()}
                  </td>
                  <td className="py-2 px-3 text-right">${r.battery_pack_price_usd_kwh.toFixed(1)}</td>
                  <td className="py-2 px-3 text-right">{r.public_chargers_per_million_capita.toFixed(0)}</td>
                  <td className="py-2 px-3 text-right text-amber-300">{r.applied_tariff_rate_pct.toFixed(1)}%</td>
                  <td className="py-2 px-3 text-right">{r.used_ev_depreciation_rate_pct.toFixed(1)}%</td>
                  <td className="py-2 px-3 text-right">{r.interest_rate_pct.toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination Footer */}
        <div className="flex items-center justify-between pt-3 text-xs text-slate-400">
          <span>
            Showing page <strong className="text-slate-200">{currentPage}</strong> of{' '}
            <strong className="text-slate-200">{totalPages}</strong>
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="p-1 rounded bg-slate-900 border border-slate-700 disabled:opacity-40 hover:bg-slate-700"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              className="p-1 rounded bg-slate-900 border border-slate-700 disabled:opacity-40 hover:bg-slate-700"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
