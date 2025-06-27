'use client';

import { useState, useEffect } from 'react';
import { Income } from '@/types/income';
import { incomeService } from '@/services/api';

export default function IncomesPage() {
  const [incomes, setIncomes] = useState<Income[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadIncomes();
  }, []);

  const loadIncomes = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await incomeService.getIncomes();
      setIncomes(data);
    } catch (err) {
      console.error('Erro ao carregar receitas:', err);
      setError('Erro ao carregar receitas. Verifique se o backend está rodando.');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteIncome = async (id: number) => {
    if (!confirm('Tem certeza que deseja deletar esta receita?')) return;
    
    try {
      await incomeService.deleteIncome(id);
      setIncomes(incomes.filter(inc => inc.id !== id));
    } catch (err) {
      console.error('Erro ao deletar receita:', err);
      alert('Erro ao deletar receita');
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'received':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'overdue':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'received':
        return 'Recebido';
      case 'pending':
        return 'Pendente';
      case 'overdue':
        return 'Atrasado';
      default:
        return status;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando receitas...</p>
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
            onClick={loadIncomes}
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
            <h1 className="text-3xl font-bold text-gray-900">Receitas</h1>
            <p className="text-gray-600 mt-2">Gerencie suas receitas e controle seus ganhos</p>
          </div>
          <button className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg">
            + Nova Receita
          </button>
        </div>

        {/* Estatísticas */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900">Total de Receitas</h3>
            <p className="text-3xl font-bold text-green-600">
              {formatCurrency(incomes.reduce((sum, inc) => sum + inc.amount, 0))}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900">Quantidade</h3>
            <p className="text-3xl font-bold text-blue-600">{incomes.length}</p>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900">Média</h3>
            <p className="text-3xl font-bold text-green-600">
              {incomes.length > 0 
                ? formatCurrency(incomes.reduce((sum, inc) => sum + inc.amount, 0) / incomes.length)
                : formatCurrency(0)
              }
            </p>
          </div>
        </div>

        {/* Lista de Receitas */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Lista de Receitas</h2>
          </div>
          
          {incomes.length === 0 ? (
            <div className="px-6 py-12 text-center">
              <p className="text-gray-500 text-lg">Nenhuma receita encontrada</p>
              <p className="text-gray-400 mt-2">Clique em "Nova Receita" para começar</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Descrição
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Valor
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Categoria
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Data
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Fonte
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Ações
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {incomes.map((income) => (
                    <tr key={income.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {income.description}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-bold text-green-600">
                          {formatCurrency(income.amount)}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                          {income.category}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {formatDate(income.date)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {income.source}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(income.status)}`}>
                          {getStatusText(income.status)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button className="text-blue-600 hover:text-blue-900 mr-3">
                          Editar
                        </button>
                        <button 
                          onClick={() => handleDeleteIncome(income.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          Deletar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 