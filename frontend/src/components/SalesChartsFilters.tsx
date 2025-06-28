import { useState } from 'react';

interface SalesChartsFiltersProps {
  onChange: (filters: SalesChartsFiltersState) => void;
  initial?: SalesChartsFiltersState;
}

export interface SalesChartsFiltersState {
  startDate: string;
  endDate: string;
  produtoServico: string;
  months: number;
}

export default function SalesChartsFilters({ onChange, initial }: SalesChartsFiltersProps) {
  const [filters, setFilters] = useState<SalesChartsFiltersState>(
    initial || {
      startDate: '',
      endDate: '',
      produtoServico: '',
      months: 6,
    }
  );

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    const newFilters = {
      ...filters,
      [name]: name === 'months' ? Number(value) : value,
    };
    setFilters(newFilters);
    onChange(newFilters);
  };

  return (
    <form className="flex flex-wrap gap-4 mb-6 items-end">
      <div>
        <label className="block text-sm font-medium text-gray-700">Data inicial</label>
        <input
          type="date"
          name="startDate"
          value={filters.startDate}
          onChange={handleChange}
          className="mt-1 block w-36 rounded border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Data final</label>
        <input
          type="date"
          name="endDate"
          value={filters.endDate}
          onChange={handleChange}
          className="mt-1 block w-36 rounded border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Produto/Serviço</label>
        <input
          type="text"
          name="produtoServico"
          value={filters.produtoServico}
          onChange={handleChange}
          placeholder="Todos"
          className="mt-1 block w-44 rounded border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Meses</label>
        <select
          name="months"
          value={filters.months}
          onChange={handleChange}
          className="mt-1 block w-24 rounded border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
        >
          {[3, 6, 12, 24].map((m) => (
            <option key={m} value={m}>{m} meses</option>
          ))}
        </select>
      </div>
    </form>
  );
} 