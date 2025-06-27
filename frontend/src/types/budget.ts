export interface Budget {
  id: number;
  category: string;
  limit: number;
  spent: number;
  period: string;
  status: 'active' | 'over' | 'inactive';
  percentage: number;
  remaining: number;
}

export interface CreateBudgetData {
  category: string;
  limit: number;
  period: string;
}

export interface UpdateBudgetData {
  limit?: number;
  period?: string;
}

export interface BudgetAlert {
  category: string;
  type: 'warning' | 'danger';
  message: string;
  percentage: number;
  spent: number;
  limit: number;
}

export interface BudgetAnalysis {
  total_budget: number;
  total_spent: number;
  total_remaining: number;
  overall_percentage: number;
  predictions: BudgetPrediction[];
}

export interface BudgetPrediction {
  category: string;
  current_spent: number;
  predicted_spent: number;
  will_exceed: boolean;
  excess_amount: number;
} 