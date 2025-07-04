import axios from 'axios';
import { DashboardData, Transaction, BudgetProgress, ChartData } from '@/types/dashboard';
import { Expense, CreateExpenseData, UpdateExpenseData, ExpenseFilters } from '@/types/expense';
import { Income, CreateIncomeData, UpdateIncomeData, IncomeFilters } from '@/types/income';
import { Budget, CreateBudgetData, UpdateBudgetData, BudgetAlert, BudgetAnalysis } from '@/types/budget';
import { Sale, SaleFormData, SalesFilters, SalesKPIs, SalesByProduct, SalesEvolution, TopSalesProduct } from '@/types/sale';

// Configuração base do axios
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para logs de debug
api.interceptors.request.use(
  (config) => config,
  (error: any) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error: any) => Promise.reject(error)
);

// Serviços da API - Dashboard
export const dashboardService = {
  // Buscar todos os dados do dashboard
  getDashboardData: async (): Promise<DashboardData> => {
    const response = await api.get('/api/dashboard/');
    return response.data;
  },

  // Buscar apenas KPIs
  getKPIs: async () => {
    const response = await api.get('/api/kpis/');
    return response.data;
  },

  // Buscar transações recentes
  getRecentTransactions: async (): Promise<Transaction[]> => {
    const response = await api.get('/api/transactions/');
    return response.data;
  },

  // Buscar progresso do orçamento
  getBudgetProgress: async (): Promise<BudgetProgress[]> => {
    const response = await api.get('/api/budget/');
    return response.data;
  },

  // Buscar dados do gráfico
  getChartData: async (): Promise<ChartData[]> => {
    const response = await api.get('/api/chart/');
    return response.data;
  },
};

// Serviços da API - Despesas
export const expenseService = {
  // Listar todas as despesas
  getExpenses: async (filters?: ExpenseFilters): Promise<Expense[]> => {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
    }
    const response = await api.get(`/api/expenses/?${params.toString()}`);
    return response.data;
  },

  // Buscar despesa específica
  getExpense: async (id: number): Promise<Expense> => {
    const response = await api.get(`/api/expenses/${id}/`);
    return response.data;
  },

  // Criar nova despesa
  createExpense: async (data: CreateExpenseData): Promise<Expense> => {
    const response = await api.post('/api/expenses/create/', data);
    return response.data;
  },

  // Atualizar despesa
  updateExpense: async (id: number, data: UpdateExpenseData): Promise<Expense> => {
    const response = await api.put(`/api/expenses/${id}/update/`, data);
    return response.data;
  },

  // Deletar despesa
  deleteExpense: async (id: number): Promise<void> => {
    await api.delete(`/api/expenses/${id}/delete/`);
  },

  // Buscar categorias de despesas (novo endpoint)
  getCategories: async (): Promise<any[]> => {
    const response = await api.get('/api/expense-categories/');
    return response.data;
  },

  // KPIs de despesas
  getKPIs: async () => {
    const response = await api.get('/api/expense-kpis/');
    return response.data;
  },

  // Despesas por categoria
  getByCategory: async (params?: { month?: string; year?: string }) => {
    const query = params ? `?${new URLSearchParams(params as any).toString()}` : '';
    const response = await api.get(`/api/expense-by-category/${query}`);
    return response.data;
  },

  // Evolução mensal das despesas
  getEvolution: async (months?: number) => {
    const query = months ? `?months=${months}` : '';
    const response = await api.get(`/api/expense-evolution/${query}`);
    return response.data;
  },

  // Top categorias de despesas
  getTopCategories: async (params?: { limit?: number; months?: number }) => {
    const query = params ? `?${new URLSearchParams(params as any).toString()}` : '';
    const response = await api.get(`/api/top-expense-categories/${query}`);
    return response.data;
  },

  // Criar categoria de despesa
  createCategory: async (data: { name: string }) => {
    const response = await api.post('/api/expense-categories/create/', data);
    return response.data;
  },

  // Atualizar categoria de despesa
  updateCategory: async (id: number, data: { name: string }) => {
    const response = await api.put(`/api/expense-categories/${id}/update/`, data);
    return response.data;
  },

  // Deletar categoria de despesa
  deleteCategory: async (id: number) => {
    return api.delete(`/api/expense-categories/${id}/delete/`);
  },

  // Migrar despesas para outra categoria
  migrateCategory: async (id: number, target_category_id: number | string) => {
    return api.post(`/api/expense-categories/${id}/migrate/`, { target_category_id });
  },

  // Deletar categoria e todas as despesas
  deleteCategoryWithExpenses: async (id: number) => {
    return api.delete(`/api/expense-categories/${id}/delete-with-expenses/`);
  },
};

// Serviços da API - Receitas
export const incomeService = {
  // Listar todas as receitas
  getIncomes: async (filters?: IncomeFilters): Promise<Income[]> => {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
    }
    
    const response = await api.get(`/api/incomes/?${params.toString()}`);
    return response.data;
  },

  // Buscar receita específica
  getIncome: async (id: number): Promise<Income> => {
    const response = await api.get(`/api/incomes/${id}/`);
    return response.data;
  },

  // Criar nova receita
  createIncome: async (data: CreateIncomeData): Promise<Income> => {
    const response = await api.post('/api/incomes/create/', data);
    return response.data;
  },

  // Atualizar receita
  updateIncome: async (id: number, data: UpdateIncomeData): Promise<Income> => {
    const response = await api.put(`/api/incomes/${id}/update/`, data);
    return response.data;
  },

  // Deletar receita
  deleteIncome: async (id: number): Promise<void> => {
    await api.delete(`/api/incomes/${id}/delete/`);
  },

  // Buscar categorias de receitas
  getCategories: async (): Promise<string[]> => {
    const response = await api.get('/api/incomes/categories/');
    return response.data;
  },
};

// Serviços da API - Orçamento
export const budgetService = {
  // Listar todos os orçamentos
  getBudgets: async (): Promise<Budget[]> => {
    const response = await api.get('/api/budgets/');
    return response.data;
  },

  // Buscar orçamento específico
  getBudget: async (id: number): Promise<Budget> => {
    const response = await api.get(`/api/budgets/${id}/`);
    return response.data;
  },

  // Criar novo orçamento
  createBudget: async (data: CreateBudgetData): Promise<Budget> => {
    const response = await api.post('/api/budgets/create/', data);
    return response.data;
  },

  // Atualizar orçamento
  updateBudget: async (id: number, data: UpdateBudgetData): Promise<Budget> => {
    const response = await api.put(`/api/budgets/${id}/update/`, data);
    return response.data;
  },

  // Deletar orçamento
  deleteBudget: async (id: number): Promise<void> => {
    await api.delete(`/api/budgets/${id}/delete/`);
  },

  // Buscar alertas de orçamento
  getAlerts: async (): Promise<BudgetAlert[]> => {
    const response = await api.get('/api/budgets/alerts/');
    return response.data;
  },

  // Buscar análise preditiva
  getAnalysis: async (): Promise<BudgetAnalysis> => {
    const response = await api.get('/api/budgets/analysis/');
    return response.data;
  },
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

// --- Vendas ---
export async function getSales(params = {}) {
  const query = new URLSearchParams(params as any).toString();
  const res = await fetch(`${API_BASE}/api/sales/${query ? `?${query}` : ''}`);
  if (!res.ok) throw new Error('Erro ao buscar vendas');
  return res.json();
}

export async function getSale(id: number) {
  const res = await fetch(`${API_BASE}/api/sales/${id}/`);
  if (!res.ok) throw new Error('Erro ao buscar venda');
  return res.json();
}

export async function createSale(data: any) {
  const res = await fetch(`${API_BASE}/api/sales/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Erro ao criar venda');
  return res.json();
}

export async function updateSale(id: number, data: any) {
  const res = await fetch(`${API_BASE}/api/sales/${id}/`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Erro ao atualizar venda');
  return res.json();
}

export async function deleteSale(id: number) {
  const res = await fetch(`${API_BASE}/api/sales/${id}/`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Erro ao deletar venda');
  return res.json();
}

export default api; 