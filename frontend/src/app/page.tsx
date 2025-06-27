'use client';

import { useState, useEffect } from 'react';
import DashboardHeader from '@/components/DashboardHeader';
import KPICard from '@/components/KPICard';
import TransactionChart from '@/components/TransactionChart';
import RecentTransactions from '@/components/RecentTransactions';
import BudgetProgress from '@/components/BudgetProgress';
import { DashboardData } from '@/types/dashboard';

export default function DashboardPage() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simular dados do dashboard (será substituído pela API real)
    const mockData: DashboardData = {
      balance: 15420.50,
      income: 8500.00,
      expenses: 3200.00,
      savings: 2200.00,
      transactions: [
        { id: 1, description: 'Salário', amount: 8500.00, type: 'income', date: '2024-01-15', category: 'Salário' },
        { id: 2, description: 'Supermercado', amount: -450.00, type: 'expense', date: '2024-01-14', category: 'Alimentação' },
        { id: 3, description: 'Combustível', amount: -200.00, type: 'expense', date: '2024-01-13', category: 'Transporte' },
        { id: 4, description: 'Freelance', amount: 1200.00, type: 'income', date: '2024-01-12', category: 'Trabalho' },
      ],
      budgetProgress: [
        { category: 'Alimentação', spent: 450, limit: 800, percentage: 56 },
        { category: 'Transporte', spent: 200, limit: 400, percentage: 50 },
        { category: 'Lazer', spent: 150, limit: 300, percentage: 50 },
      ],
      chartData: [
        { name: 'Jan', income: 8500, expenses: 3200 },
        { name: 'Fev', income: 7800, expenses: 2900 },
        { name: 'Mar', income: 9200, expenses: 3500 },
      ]
    };

    setTimeout(() => {
      setDashboardData(mockData);
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Erro ao carregar dados do dashboard</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardHeader />
      
      <main className="container mx-auto px-4 py-8">
        {/* KPIs */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <KPICard
            title="Saldo Atual"
            value={dashboardData.balance}
            type="balance"
            trend="+12.5%"
            trendDirection="up"
          />
          <KPICard
            title="Receitas"
            value={dashboardData.income}
            type="income"
            trend="+8.2%"
            trendDirection="up"
          />
          <KPICard
            title="Despesas"
            value={dashboardData.expenses}
            type="expense"
            trend="-5.1%"
            trendDirection="down"
          />
          <KPICard
            title="Economias"
            value={dashboardData.savings}
            type="savings"
            trend="+15.3%"
            trendDirection="up"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Gráfico de Transações */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-semibold mb-4">Evolução Financeira</h2>
              <TransactionChart data={dashboardData.chartData} />
            </div>
          </div>

          {/* Progresso do Orçamento */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold mb-4">Progresso do Orçamento</h2>
            <BudgetProgress data={dashboardData.budgetProgress} />
          </div>
        </div>

        {/* Transações Recentes */}
        <div className="mt-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold mb-4">Transações Recentes</h2>
            <RecentTransactions transactions={dashboardData.transactions} />
          </div>
        </div>
      </main>
    </div>
  );
} 