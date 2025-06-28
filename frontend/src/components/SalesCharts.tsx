'use client';

import { useState, useEffect } from 'react';
import { salesService } from '@/services/api';
import { SalesByProduct, SalesEvolution, TopSalesProduct } from '@/types/sale';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
  Filler,
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';
import SalesChartsFilters, { SalesChartsFiltersState } from './SalesChartsFilters';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
  Filler
);

interface SalesChartsProps {
  months?: number;
}

export default function SalesCharts({ months = 6 }: SalesChartsProps) {
  const [salesByProduct, setSalesByProduct] = useState<SalesByProduct[]>([]);
  const [salesEvolution, setSalesEvolution] = useState<SalesEvolution[]>([]);
  const [topProducts, setTopProducts] = useState<TopSalesProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<SalesChartsFiltersState>({
    startDate: '',
    endDate: '',
    produtoServico: '',
    months: months,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        const byProduct = await salesService.getByProduct({
          start_date: filters.startDate,
          end_date: filters.endDate,
          limit: 10,
        });
        const evolution = await salesService.getEvolution(filters.months);
        const top = await salesService.getTopProducts({
          limit: 5,
          months: filters.months,
        });
        setSalesByProduct(
          filters.produtoServico
            ? byProduct.filter((item) =>
                item.produto_servico
                  .toLowerCase()
                  .includes(filters.produtoServico.toLowerCase())
              )
            : byProduct
        );
        setSalesEvolution(evolution);
        setTopProducts(
          filters.produtoServico
            ? top.filter((item) =>
                item.produto_servico
                  .toLowerCase()
                  .includes(filters.produtoServico.toLowerCase())
              )
            : top
        );
      } catch (err) {
        console.error('Erro ao buscar dados dos gráficos:', err);
        setError('Erro ao carregar dados dos gráficos');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [filters]);

  if (loading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  // Dados para o gráfico de vendas por produto
  const productChartData = {
    labels: salesByProduct.map(item => item.produto_servico),
    datasets: [
      {
        label: 'Vendas (R$)',
        data: salesByProduct.map(item => item.total_vendas),
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1,
      },
      {
        label: 'Lucro (R$)',
        data: salesByProduct.map(item => item.lucro_bruto),
        backgroundColor: 'rgba(34, 197, 94, 0.8)',
        borderColor: 'rgba(34, 197, 94, 1)',
        borderWidth: 1,
      }
    ],
  };

  // Dados para o gráfico de evolução mensal
  const evolutionChartData = {
    labels: salesEvolution.map(item => item.periodo),
    datasets: [
      {
        label: 'Vendas (R$)',
        data: salesEvolution.map(item => item.total_vendas),
        borderColor: 'rgba(59, 130, 246, 1)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4,
      },
      {
        label: 'Lucro (R$)',
        data: salesEvolution.map(item => item.lucro_bruto),
        borderColor: 'rgba(34, 197, 94, 1)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        fill: true,
        tension: 0.4,
      }
    ],
  };

  // Dados para o gráfico de pizza dos top produtos
  const topProductsChartData = {
    labels: topProducts.map(item => item.produto_servico),
    datasets: [
      {
        data: topProducts.map(item => item.lucro_bruto),
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(34, 197, 94, 0.8)',
          'rgba(168, 85, 247, 0.8)',
          'rgba(251, 146, 60, 0.8)',
          'rgba(239, 68, 68, 0.8)',
        ],
        borderWidth: 2,
        borderColor: '#fff',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
    },
  };

  const lineChartOptions = {
    ...chartOptions,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value: any) {
            return formatCurrency(value);
          }
        }
      }
    }
  };

  return (
    <div className="space-y-6">
      <SalesChartsFilters onChange={setFilters} initial={filters} />
      {/* Gráfico de evolução mensal */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Evolução Mensal das Vendas
        </h3>
        <div className="h-80">
          <Line data={evolutionChartData} options={lineChartOptions} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Gráfico de vendas por produto */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Vendas por Produto/Serviço
          </h3>
          <div className="h-80">
            <Bar data={productChartData} options={chartOptions} />
          </div>
        </div>

        {/* Gráfico de pizza dos top produtos */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Top Produtos por Lucro
          </h3>
          <div className="h-80">
            <Doughnut data={topProductsChartData} options={chartOptions} />
          </div>
        </div>
      </div>
    </div>
  );
} 