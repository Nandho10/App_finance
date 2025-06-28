export interface Sale {
  id: number;
  data: string;
  produto_servico: string;
  valor_venda: number;
  custo: number;
  lucro_bruto: number;
  forma_recebimento: string;
  observacoes?: string;
}

export interface SaleFormData {
  data: string;
  produto_servico: string;
  valor_venda: number;
  custo: number;
  forma_recebimento: string;
  observacoes?: string;
}

export interface SalesFilters {
  startDate: string;
  endDate: string;
  produtoServico: string;
  formaRecebimento: string;
}

export interface SalesResponse {
  success: boolean;
  data: Sale[];
  total: number;
}

export interface SaleResponse {
  success: boolean;
  data: Sale;
  message?: string;
} 