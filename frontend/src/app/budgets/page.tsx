'use client';

import { useState, useEffect } from 'react';
import { Budget, BudgetAlert, BudgetAnalysis } from '@/types/budget';
import { budgetService } from '@/services/api';

export default function BudgetsPage() {
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [alerts, setAlerts] = useState<BudgetAlert[]>([]);
  const [analysis, setAnalysis] = useState<BudgetAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadBudgetData();
  }, []);

  const loadBudgetData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [budgetsData, alertsData, analysisData] = await Promise.all([
        budgetService.getBudgets(),
        budgetService.getAlerts(),
        budgetService.getAnalysis()
      ]);
      
      setBudgets(budgetsData);
      setAlerts(alertsData);
      setAnalysis(analysisData);
    } catch (err) {
      console.error('Erro ao carregar dados do orçamento:', err);
      setError('Erro ao carregar dados do orçamento. Verifique se o backend está rodando.');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteBudget = async (id: number) => {
    if (!confirm('Tem certeza que deseja deletar este orçamento?')) return;
    
    try {
      await budgetService.deleteBudget(id);
      setBudgets(budgets.filter(budget => budget.id !== id));
    } catch (err) {
      console.error('Erro ao deletar orçamento:', err);
      alert('Erro ao deletar orçamento');
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'over':
        return 'bg-red-100 text-red-800';
      case 'inactive':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active':
        return 'Ativo';
      case 'over':
        return 'Estourado';
      case 'inactive':
        return 'Inativo';
      default:
        return status;
    }
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 90) return 'bg-red-500';
    if (percentage >= 75) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando orçamentos...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            <p className="font-bold">Erro!</p>
            <p>{error}</p>
          </div>
          <button
            onClick={loadBudgetData}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Orçamento</h1>
            <p className="text-gray-600 mt-2">Gerencie seus limites de gastos por categoria</p>
          </div>
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg">
            + Novo Orçamento
          </button>
        </div>

        {/* Alertas */}
        {alerts.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Alertas</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {alerts.map((alert, index) => (
                <div
                  key={index}
                  className={`p-4 rounded-lg border ${
                    alert.type === 'danger' 
                      ? 'bg-red-50 border-red-200 text-red-800' 
                      : 'bg-yellow-50 border-yellow-200 text-yellow-800'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-semibold">{alert.category}</p>
                      <p className="text-sm">{alert.message}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold">{alert.percentage.toFixed(1)}%</p>
                      <p className="text-sm">
                        {formatCurrency(alert.spent)} / {formatCurrency(alert.limit)}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Análise Geral */}
        {analysis && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900">Orçamento Total</h3>
              <p className="text-3xl font-bold text-blue-600">
                {formatCurrency(analysis.total_budget)}
              </p>
            </div>
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900">Gasto Total</h3>
              <p className="text-3xl font-bold text-red-600">
                {formatCurrency(analysis.total_spent)}
              </p>
            </div>
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900">Restante</h3>
              <p className="text-3xl font-bold text-green-600">
                {formatCurrency(analysis.total_remaining)}
              </p>
            </div>
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900">Progresso</h3>
              <p className="text-3xl font-bold text-purple-600">
                {analysis.overall_percentage.toFixed(1)}%
              </p>
            </div>
          </div>
        )}

        {/* Lista de Orçamentos */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Orçamentos por Categoria</h2>
          </div>
          
          {budgets.length === 0 ? (
            <div className="px-6 py-12 text-center">
              <p className="text-gray-500 text-lg">Nenhum orçamento encontrado</p>
              <p className="text-gray-400 mt-2">Clique em "Novo Orçamento" para começar</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {budgets.map((budget) => (
                <div key={budget.id} className="p-6 hover:bg-gray-50">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-4">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{budget.category}</h3>
                        <p className="text-sm text-gray-500">Período: {budget.period}</p>
                      </div>
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(budget.status)}`}>
                        {getStatusText(budget.status)}
                      </span>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-500">Gasto / Limite</p>
                      <p className="text-lg font-bold">
                        {formatCurrency(budget.spent)} / {formatCurrency(budget.limit)}
                      </p>
                    </div>
                  </div>
                  
                  {/* Barra de Progresso */}
                  <div className="mb-4">
                    <div className="flex justify-between text-sm text-gray-600 mb-1">
                      <span>Progresso</span>
                      <span>{budget.percentage.toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${getProgressColor(budget.percentage)}`}
                        style={{ width: `${Math.min(100, budget.percentage)}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <div className="text-sm text-gray-600">
                      <span className={budget.remaining >= 0 ? 'text-green-600' : 'text-red-600'}>
                        {budget.remaining >= 0 ? 'Restante:' : 'Excedido:'} {formatCurrency(Math.abs(budget.remaining))}
                      </span>
                    </div>
                    <div className="flex space-x-2">
                      <button className="text-blue-600 hover:text-blue-900 text-sm">
                        Editar
                      </button>
                      <button 
                        onClick={() => handleDeleteBudget(budget.id)}
                        className="text-red-600 hover:text-red-900 text-sm"
                      >
                        Deletar
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Análise Preditiva */}
        {analysis && analysis.predictions.length > 0 && (
          <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Análise Preditiva</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {analysis.predictions.map((prediction, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-900 mb-2">{prediction.category}</h3>
                  <div className="space-y-1 text-sm">
                    <p>Gasto atual: {formatCurrency(prediction.current_spent)}</p>
                    <p>Previsão: {formatCurrency(prediction.predicted_spent)}</p>
                    {prediction.will_exceed && (
                      <p className="text-red-600 font-semibold">
                        Excederá em: {formatCurrency(prediction.excess_amount)}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 