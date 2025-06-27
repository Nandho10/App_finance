export interface Income {
  id: number;
  description: string;
  amount: number;
  category: string;
  date: string;
  source: string;
  status: 'received' | 'pending' | 'overdue';
}

export interface CreateIncomeData {
  description: string;
  amount: number;
  category: string;
  date: string;
  source?: string;
  status?: 'received' | 'pending' | 'overdue';
}

export interface UpdateIncomeData {
  description?: string;
  amount?: number;
  category?: string;
  date?: string;
  source?: string;
  status?: 'received' | 'pending' | 'overdue';
}

export interface IncomeFilters {
  category?: string;
  date_from?: string;
  date_to?: string;
  status?: string;
  source?: string;
}

export interface IncomeStats {
  total: number;
  by_category: { [category: string]: number };
  by_month: { [month: string]: number };
  average: number;
} 