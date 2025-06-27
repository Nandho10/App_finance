export interface Transaction {
  id: number;
  description: string;
  amount: number;
  type: 'income' | 'expense';
  date: string;
  category: string;
}

export interface BudgetProgress {
  category: string;
  spent: number;
  limit: number;
  percentage: number;
}

export interface ChartData {
  name: string;
  income: number;
  expenses: number;
}

export interface DashboardData {
  balance: number;
  income: number;
  expenses: number;
  savings: number;
  transactions: Transaction[];
  budgetProgress: BudgetProgress[];
  chartData: ChartData[];
}

export interface KPICardProps {
  title: string;
  value: number;
  type: 'balance' | 'income' | 'expense' | 'savings';
  trend: string;
  trendDirection: 'up' | 'down';
} 