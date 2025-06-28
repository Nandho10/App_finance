import { useState, useEffect } from 'react';
import { Expense } from '@/types/expense';

interface ExpenseReportsProps {
  expenses: Expense[];
}

interface CategoryData {
  category: string;
  total: number;
  percentage: number;
  count: number;
}

interface MonthlyData {
  month: string;
  total: number;
  count: number;
}

export default function ExpenseReports({ expenses }: ExpenseReportsProps) {
  const [selectedPeriod, setSelectedPeriod] = useState('month');
  const [categoryData, setCategoryData] = useState<CategoryData[]>([]);
  const [monthlyData, setMonthlyData] = useState<MonthlyData[]>([]);

  useEffect(() => {
    calculateReports();
  }, [expenses, selectedPeriod]);

  const calculateReports = () => {
    const now = new Date();
    let filteredExpenses = [...expenses];

    // Filtrar por período selecionado
    switch (selectedPeriod) {
      case 'week':
        const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        filteredExpenses = filteredExpenses.filter(expense => {
          const expDate = new Date(expense.paid_at || expense.date);
          return expDate >= weekAgo;
        });
        break;
      case 'month':
        const monthAgo = new Date(now.getFullYear(), now.getMonth(), 1);
        filteredExpenses = filteredExpenses.filter(expense => {
          const expDate = new Date(expense.paid_at || expense.date);
          return expDate >= monthAgo;
        });
        break;
      case 'quarter':
        const quarterAgo = new Date(now.getFullYear(), Math.floor(now.getMonth() / 3) * 3, 1);
        filteredExpenses = filteredExpenses.filter(expense => {
          const expDate = new Date(expense.paid_at || expense.date);
          return expDate >= quarterAgo;
        });
        break;
      case 'year':
        const yearAgo = new Date(now.getFullYear(), 0, 1);
        filteredExpenses = filteredExpenses.filter(expense => {
          const expDate = new Date(expense.paid_at || expense.date);
          return expDate >= yearAgo;
        });
        break;
    }

    // Calcular dados por categoria
    const categoryMap = new Map<string, { total: number; count: number }>();
    filteredExpenses.forEach(expense => {
      const current = categoryMap.get(expense.category) || { total: 0, count: 0 };
      categoryMap.set(expense.category, {
        total: current.total + expense.amount,
        count: current.count + 1
      });
    });

    const totalAmount = filteredExpenses.reduce((sum, exp) => sum + exp.amount, 0);
    const categoryDataArray: CategoryData[] = Array.from(categoryMap.entries()).map(([category, data]) => ({
      category,
      total: data.total,
      percentage: totalAmount > 0 ? (data.total / totalAmount) * 100 : 0,
      count: data.count
    })).sort((a, b) => b.total - a.total);

    setCategoryData(categoryDataArray);

    // Calcular dados mensais (últimos 6 meses)
    const monthlyMap = new Map<string, { total: number; count: number }>();
    for (let i = 5; i >= 0; i--) {
      const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
      const monthKey = date.toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' });
      monthlyMap.set(monthKey, { total: 0, count: 0 });
    }

    filteredExpenses.forEach(expense => {
      const expDate = new Date(expense.paid_at || expense.date);
      const monthKey = expDate.toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' });
      const current = monthlyMap.get(monthKey);
      if (current) {
        current.total += expense.amount;
        current.count += 1;
      }
    });

    const monthlyDataArray: MonthlyData[] = Array.from(monthlyMap.entries()).map(([month, data]) => ({
      month,
      total: data.total,
      count: data.count
    }));

    setMonthlyData(monthlyDataArray);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const getCategoryColor = (index: number) => {
    const colors = [
      'bg-blue-500', 'bg-green-500', 'bg-yellow-500', 'bg-red-500',
      'bg-purple-500', 'bg-pink-500', 'bg-indigo-500', 'bg-gray-500'
    ];
    return colors[index % colors.length];
  };

  return (
    <div className="space-y-6">
      {/* Seletor de Período */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Relatórios</h3>
          <select
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="week">Esta semana</option>
            <option value="month">Este mês</option>
            <option value="quarter">Este trimestre</option>
            <option value="year">Este ano</option>
          </select>
        </div>

        {/* Resumo */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <p className="text-2xl font-bold text-blue-600">
              {formatCurrency(expenses.reduce((sum, exp) => sum + exp.amount, 0))}
            </p>
            <p className="text-sm text-gray-600">Total Geral</p>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <p className="text-2xl font-bold text-green-600">
              {formatCurrency(categoryData.reduce((sum, cat) => sum + cat.total, 0))}
            </p>
            <p className="text-sm text-gray-600">Total do Período</p>
          </div>
          <div className="text-center p-4 bg-yellow-50 rounded-lg">
            <p className="text-2xl font-bold text-yellow-600">
              {expenses.length}
            </p>
            <p className="text-sm text-gray-600">Total de Despesas</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Gráfico por Categoria */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Despesas por Categoria</h3>
          {categoryData.length === 0 ? (
            <p className="text-gray-500 text-center py-8">Nenhum dado disponível para o período selecionado</p>
          ) : (
            <div className="space-y-4">
              {categoryData.map((item, index) => (
                <div key={item.category} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`w-4 h-4 rounded-full ${getCategoryColor(index)}`}></div>
                    <div>
                      <p className="font-medium text-gray-900">{item.category}</p>
                      <p className="text-sm text-gray-500">{item.count} despesas</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-gray-900">{formatCurrency(item.total)}</p>
                    <p className="text-sm text-gray-500">{item.percentage.toFixed(1)}%</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Gráfico Mensal */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Evolução Mensal</h3>
          {monthlyData.length === 0 ? (
            <p className="text-gray-500 text-center py-8">Nenhum dado disponível</p>
          ) : (
            <div className="space-y-4">
              {monthlyData.map((item) => (
                <div key={item.month} className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-gray-900">{item.month}</p>
                    <p className="text-sm text-gray-500">{item.count} despesas</p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-gray-900">{formatCurrency(item.total)}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Top 5 Maiores Despesas */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Top 5 Maiores Despesas</h3>
        {expenses.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Nenhuma despesa registrada</p>
        ) : (
          <div className="space-y-3">
            {expenses
              .sort((a, b) => b.amount - a.amount)
              .slice(0, 5)
              .map((expense, index) => (
                <div key={expense.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-semibold">
                      {index + 1}
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{expense.description}</p>
                      <p className="text-sm text-gray-500">{expense.category}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-red-600">{formatCurrency(expense.amount)}</p>
                    <p className="text-sm text-gray-500">
                      {new Date(expense.paid_at || expense.date).toLocaleDateString('pt-BR')}
                    </p>
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
} 