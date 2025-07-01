export interface Sale {
  id: number;
  paid_at: string;
  product: string;
  amount: number;
  custo: number;
  payment_method: string;
  observacoes?: string;
  delivery_date?: string | null;
  client?: string;
}

export type SaleFormData = Omit<Sale, 'id'>; 