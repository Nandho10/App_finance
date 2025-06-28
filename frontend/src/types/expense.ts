export interface Expense {
  id: number;
  description: string;
  amount: number;
  category: string;
  category_id?: number;
  date: string;
  paid_at?: string;
  payment_method: string;
  status: 'paid' | 'pending' | 'overdue';
}

export interface CreateExpenseData {
  description: string;
  amount: number;
  category: string;
  paid_at: string;
  payment_method: string;
}

export interface UpdateExpenseData {
  description?: string;
  amount?: number;
  category?: string;
  paid_at?: string;
  payment_method?: string;
  status?: 'paid' | 'pending' | 'overdue';
}

export interface ExpenseFilters {
  search?: string;
  category?: string;
  status?: string;
  period?: string;
  start_date?: string;
  end_date?: string;
  payment_method?: string;
}

export interface ExpenseStats {
  total: number;
  by_category: { [category: string]: number };
  by_month: { [month: string]: number };
  average: number;
} 