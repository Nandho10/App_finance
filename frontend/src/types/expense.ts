export interface Expense {
  id: number;
  description: string;
  amount: number;
  category: string;
  date: string;
  payment_method: string;
  status: 'paid' | 'pending' | 'overdue';
}

export interface CreateExpenseData {
  description: string;
  amount: number;
  category: string;
  date: string;
  payment_method?: string;
  status?: 'paid' | 'pending' | 'overdue';
}

export interface UpdateExpenseData {
  description?: string;
  amount?: number;
  category?: string;
  date?: string;
  payment_method?: string;
  status?: 'paid' | 'pending' | 'overdue';
}

export interface ExpenseFilters {
  category?: string;
  date_from?: string;
  date_to?: string;
  status?: string;
  payment_method?: string;
}

export interface ExpenseStats {
  total: number;
  by_category: { [category: string]: number };
  by_month: { [month: string]: number };
  average: number;
} 