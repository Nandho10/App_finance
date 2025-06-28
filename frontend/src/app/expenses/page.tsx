'use client';

import { useState, useEffect } from 'react';
import { Expense, ExpenseFilters } from '@/types/expense';
import { expenseService } from '@/services/api';
import ExpenseModal from '@/components/ExpenseModal';
import ExpenseFiltersComponent from '@/components/ExpenseFilters';
import ExpenseReports from '@/components/ExpenseReports';
import { useRef } from 'react';

export default function ExpensesPage() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [filteredExpenses, setFilteredExpenses] = useState<Expense[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingExpense, setEditingExpense] = useState<Expense | null>(null);
  const [activeTab, setActiveTab] = useState<'list' | 'reports'>('list');
  const [filters, setFilters] = useState<ExpenseFilters>({});
  const [categoryModalOpen, setCategoryModalOpen] = useState(false);

  useEffect(() => {
    loadExpenses();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [expenses, filters]);

  const loadExpenses = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await expenseService.getExpenses();
      setExpenses(data);
    } catch (err) {
      console.error('Erro ao carregar despesas:', err);
      setError('Erro ao carregar despesas. Verifique se o backend está rodando.');
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...expenses];

    // Filtro por busca de texto
    if (filters.search) {
      const searchTerm = filters.search.toLowerCase();
      filtered = filtered.filter(expense =>
        expense.description.toLowerCase().includes(searchTerm) ||
        expense.category.toLowerCase().includes(searchTerm)
      );
    }

    // Filtro por categoria
    if (filters.category) {
      filtered = filtered.filter(expense => expense.category === filters.category);
    }

    // Filtro por status
    if (filters.status) {
      filtered = filtered.filter(expense => expense.status === filters.status);
    }

    // Filtro por período
    if (filters.period) {
      const now = new Date();
      const expenseDate = new Date();
      
      switch (filters.period) {
        case 'today':
          filtered = filtered.filter(expense => {
            const expDate = new Date(expense.paid_at || expense.date);
            return expDate.toDateString() === now.toDateString();
          });
          break;
        case 'week':
          const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
          filtered = filtered.filter(expense => {
            const expDate = new Date(expense.paid_at || expense.date);
            return expDate >= weekAgo;
          });
          break;
        case 'month':
          const monthAgo = new Date(now.getFullYear(), now.getMonth(), 1);
          filtered = filtered.filter(expense => {
            const expDate = new Date(expense.paid_at || expense.date);
            return expDate >= monthAgo;
          });
          break;
        case 'quarter':
          const quarterAgo = new Date(now.getFullYear(), Math.floor(now.getMonth() / 3) * 3, 1);
          filtered = filtered.filter(expense => {
            const expDate = new Date(expense.paid_at || expense.date);
            return expDate >= quarterAgo;
          });
          break;
        case 'year':
          const yearAgo = new Date(now.getFullYear(), 0, 1);
          filtered = filtered.filter(expense => {
            const expDate = new Date(expense.paid_at || expense.date);
            return expDate >= yearAgo;
          });
          break;
      }
    }

    // Filtro por data específica
    if (filters.start_date) {
      const startDate = new Date(filters.start_date);
      filtered = filtered.filter(expense => {
        const expDate = new Date(expense.paid_at || expense.date);
        return expDate >= startDate;
      });
    }

    if (filters.end_date) {
      const endDate = new Date(filters.end_date);
      endDate.setHours(23, 59, 59, 999); // Fim do dia
      filtered = filtered.filter(expense => {
        const expDate = new Date(expense.paid_at || expense.date);
        return expDate <= endDate;
      });
    }

    setFilteredExpenses(filtered);
  };

  const handleFiltersChange = (newFilters: ExpenseFilters) => {
    setFilters(newFilters);
  };

  const handleClearFilters = () => {
    setFilters({});
  };

  const handleDeleteExpense = async (id: number) => {
    if (!confirm('Tem certeza que deseja deletar esta despesa?')) return;
    
    try {
      console.log('Tentando deletar despesa com ID:', id);
      console.log('URL da API:', `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/expenses/${id}/delete/`);
      
      await expenseService.deleteExpense(id);
      console.log('Despesa deletada com sucesso');
      
      setExpenses(expenses.filter(exp => exp.id !== id));
    } catch (err) {
      console.error('Erro detalhado ao deletar despesa:', err);
      console.error('Response data:', err.response?.data);
      console.error('Response status:', err.response?.status);
      alert('Erro ao deletar despesa');
    }
  };

  const handleEditExpense = (expense: Expense) => {
    setEditingExpense(expense);
    setModalOpen(true);
  };

  const handleUpdateExpense = (updatedExpense: Expense) => {
    setExpenses((prev) => 
      prev.map((expense) => 
        expense.id === updatedExpense.id ? updatedExpense : expense
      )
    );
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setEditingExpense(null);
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
      case 'paid':
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
      case 'paid':
        return 'Pago';
      case 'pending':
        return 'Pendente';
      case 'overdue':
        return 'Vencido';
      default:
        return status;
    }
  };

  const paymentMethodLabel = (value: string) => {
    switch (value) {
      case 'cash': return 'Dinheiro';
      case 'credit_card': return 'Cartão de Crédito';
      case 'pix': return 'PIX';
      case 'transfer': return 'Transferência';
      default: return value;
    }
  };

  // Novo componente Modal para CRUD de categorias de despesas
  function ExpenseCategoryModal({ isOpen, onClose }) {
    const [categories, setCategories] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [newCategory, setNewCategory] = useState('');
    const [editingCategory, setEditingCategory] = useState<any | null>(null);
    const [editName, setEditName] = useState('');
    const [actionMessage, setActionMessage] = useState('');

    useEffect(() => {
      if (isOpen) loadCategories();
    }, [isOpen]);

    const loadCategories = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await expenseService.getCategories();
        setCategories(data);
      } catch (err) {
        setError('Erro ao carregar categorias');
      } finally {
        setLoading(false);
      }
    };

    const handleCreate = async () => {
      if (!newCategory.trim()) return;
      setLoading(true);
      setError(null);
      try {
        await expenseService.createCategory({ name: newCategory });
        setNewCategory('');
        setActionMessage('Categoria criada com sucesso!');
        loadCategories();
      } catch (err) {
        setError('Erro ao criar categoria');
      } finally {
        setLoading(false);
      }
    };

    const handleEdit = (cat: any) => {
      setEditingCategory(cat);
      setEditName(cat.name);
    };

    const handleUpdate = async () => {
      if (!editingCategory || !editName.trim()) return;
      setLoading(true);
      setError(null);
      try {
        await expenseService.updateCategory(editingCategory.id, { name: editName });
        setEditingCategory(null);
        setEditName('');
        setActionMessage('Categoria atualizada!');
        loadCategories();
      } catch (err) {
        setError('Erro ao atualizar categoria');
      } finally {
        setLoading(false);
      }
    };

    const handleDelete = async (cat: any) => {
      if (!confirm('Deseja realmente excluir esta categoria?')) return;
      setLoading(true);
      setError(null);
      try {
        // Tenta deletar normalmente
        await expenseService.deleteCategory(cat.id);
        setActionMessage('Categoria excluída!');
        loadCategories();
      } catch (err: any) {
        // Se houver despesas, sugere migração ou exclusão em massa
        if (err.response?.status === 409 && err.response?.data?.requires_action) {
          if (confirm('Esta categoria possui despesas. Deseja migrar para outra categoria antes de excluir?')) {
            // Migração
            const targetId = prompt('ID da categoria de destino:');
            if (targetId) {
              await expenseService.migrateCategory(cat.id, targetId);
              setActionMessage('Despesas migradas e categoria excluída!');
              loadCategories();
            }
          } else if (confirm('Deseja excluir todas as despesas desta categoria?')) {
            await expenseService.deleteCategoryWithExpenses(cat.id);
            setActionMessage('Categoria e despesas excluídas!');
            loadCategories();
          }
        } else {
          setError('Erro ao excluir categoria');
        }
      } finally {
        setLoading(false);
      }
    };

    return (
      <div className={`fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40 ${isOpen ? '' : 'hidden'}`}>
        <div className="bg-white rounded-lg shadow-lg w-full max-w-lg p-6 relative">
          <button className="absolute top-2 right-2 text-gray-400 hover:text-gray-600" onClick={onClose}>&times;</button>
          <h2 className="text-xl font-bold mb-4">Gerenciar Categorias de Despesas</h2>
          {error && <div className="bg-red-100 text-red-700 p-2 rounded mb-2">{error}</div>}
          {actionMessage && <div className="bg-green-100 text-green-700 p-2 rounded mb-2">{actionMessage}</div>}
          <div className="mb-4 flex gap-2">
            <input
              type="text"
              className="border rounded px-2 py-1 flex-1"
              placeholder="Nova categoria"
              value={newCategory}
              onChange={e => setNewCategory(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleCreate()}
            />
            <button className="bg-blue-600 text-white px-4 py-1 rounded" onClick={handleCreate} disabled={loading}>Adicionar</button>
          </div>
          <ul className="divide-y divide-gray-200 max-h-64 overflow-y-auto">
            {categories.map(cat => (
              <li key={cat.id} className="flex items-center justify-between py-2">
                {editingCategory?.id === cat.id ? (
                  <>
                    <input
                      type="text"
                      className="border rounded px-2 py-1 flex-1"
                      value={editName}
                      onChange={e => setEditName(e.target.value)}
                      onKeyDown={e => e.key === 'Enter' && handleUpdate()}
                    />
                    <button className="ml-2 text-green-600" onClick={handleUpdate} disabled={loading}>Salvar</button>
                    <button className="ml-2 text-gray-500" onClick={() => setEditingCategory(null)}>Cancelar</button>
                  </>
                ) : (
                  <>
                    <span>{cat.name}</span>
                    <div>
                      <button className="ml-2 text-blue-600" onClick={() => handleEdit(cat)}>Editar</button>
                      <button className="ml-2 text-red-600" onClick={() => handleDelete(cat)} disabled={loading}>Excluir</button>
                    </div>
                  </>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando despesas...</p>
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
            onClick={loadExpenses}
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
      <ExpenseCategoryModal isOpen={categoryModalOpen} onClose={() => setCategoryModalOpen(false)} />
      <ExpenseModal
        isOpen={modalOpen}
        onClose={handleCloseModal}
        onCreated={(expense) => {
          setExpenses((prev) => [expense, ...prev]);
        }}
        onUpdated={handleUpdateExpense}
        editingExpense={editingExpense}
      />
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Despesas</h1>
            <p className="text-gray-600 mt-2">Gerencie suas despesas e controle seus gastos</p>
          </div>
          <div className="flex gap-2">
            <button
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg"
              onClick={() => setModalOpen(true)}
            >
              + Nova Despesa
            </button>
            <button
              className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg"
              onClick={() => setCategoryModalOpen(true)}
            >
              Categorias
            </button>
          </div>
        </div>

        {/* Abas */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('list')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'list'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Lista de Despesas
              </button>
              <button
                onClick={() => setActiveTab('reports')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'reports'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Relatórios
              </button>
            </nav>
          </div>
        </div>

        {activeTab === 'list' ? (
          <>
            {/* Filtros */}
            <ExpenseFiltersComponent
              filters={filters}
              onFiltersChange={handleFiltersChange}
              onClearFilters={handleClearFilters}
            />

            {/* Estatísticas */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900">Total de Despesas</h3>
                <p className="text-3xl font-bold text-red-600">
                  {formatCurrency(filteredExpenses.reduce((sum, exp) => sum + exp.amount, 0))}
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  {filteredExpenses.length} de {expenses.length} despesas
                </p>
              </div>
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900">Quantidade</h3>
                <p className="text-3xl font-bold text-blue-600">{filteredExpenses.length}</p>
              </div>
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900">Média</h3>
                <p className="text-3xl font-bold text-green-600">
                  {filteredExpenses.length > 0 
                    ? formatCurrency(filteredExpenses.reduce((sum, exp) => sum + exp.amount, 0) / filteredExpenses.length)
                    : formatCurrency(0)
                  }
                </p>
              </div>
            </div>

            {/* Lista de Despesas */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900">Lista de Despesas</h2>
              </div>
              
              {filteredExpenses.length === 0 ? (
                <div className="px-6 py-12 text-center">
                  <p className="text-gray-500 text-lg">
                    {expenses.length === 0 ? 'Nenhuma despesa encontrada' : 'Nenhuma despesa corresponde aos filtros aplicados'}
                  </p>
                  <p className="text-gray-400 mt-2">
                    {expenses.length === 0 ? 'Clique em "Nova Despesa" para começar' : 'Tente ajustar os filtros ou limpar todos os filtros'}
                  </p>
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
                          Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Ações
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {filteredExpenses.map((expense) => (
                        <tr key={expense.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900">
                              {expense.description}
                            </div>
                            <div className="text-sm text-gray-500">
                              {paymentMethodLabel(expense.payment_method)}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-bold text-red-600">
                              {formatCurrency(expense.amount)}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                              {expense.category}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className="text-sm text-gray-700">
                              {formatDate(expense.paid_at || expense.date)}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(expense.status)}`}>
                              {getStatusText(expense.status)}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <button 
                              onClick={() => handleEditExpense(expense)}
                              className="text-blue-600 hover:text-blue-900 mr-3"
                            >
                              Editar
                            </button>
                            <button 
                              onClick={() => handleDeleteExpense(expense.id)}
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
          </>
        ) : (
          <ExpenseReports expenses={expenses} />
        )}
      </div>
    </div>
  );
} 