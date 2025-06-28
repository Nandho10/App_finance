'use client';

import { useState, useEffect } from 'react';
import { salesService } from '@/services/api';
import { SalesKPIs } from '@/types/sale';
import { KPICard } from './KPICard';

interface SalesKPIsProps {
  month?: string;
  year?: string;
}

export default function SalesKPIs({ month, year }: SalesKPIsProps) {
  const [kpis, setKpis] = useState<SalesKPIs | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchKPIs = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const params: { month?: string; year?: string } = {};
        if (month) params.month = month;
        if (year) params.year = year;
        
        const data = await salesService.getKPIs(params);
        setKpis(data);
      } catch (err) {
        console.error('Erro ao buscar KPIs de vendas:', err);
        setError('Erro ao carregar KPIs de vendas');
      } finally {
        setLoading(false);
      }
    };

    fetchKPIs();
  }, [month, year]);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-1/2"></div>
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

  if (!kpis) {
    return null;
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <KPICard
        title="Total de Vendas"
        value={formatCurrency(kpis.total_vendas)}
        subtitle={`${kpis.quantidade_vendas} vendas`}
        trend={kpis.crescimento_percentual}
        trendLabel="vs mês anterior"
        color="blue"
      />
      
      <KPICard
        title="Lucro Bruto"
        value={formatCurrency(kpis.total_lucro)}
        subtitle={formatPercentage(kpis.margem_lucro)}
        trend={kpis.margem_lucro}
        trendLabel="margem"
        color="green"
      />
      
      <KPICard
        title="Ticket Médio"
        value={formatCurrency(kpis.ticket_medio)}
        subtitle="por venda"
        color="purple"
      />
      
      <KPICard
        title="Crescimento"
        value={formatPercentage(kpis.crescimento_percentual)}
        subtitle="vs mês anterior"
        trend={kpis.crescimento_percentual}
        trendLabel="crescimento"
        color={kpis.crescimento_percentual >= 0 ? "green" : "red"}
      />
    </div>
  );
} 