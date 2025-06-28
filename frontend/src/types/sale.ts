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

// KPIs e Relatórios
export interface SalesKPIs {
  total_vendas: number;
  total_custos: number;
  total_lucro: number;
  quantidade_vendas: number;
  ticket_medio: number;
  margem_lucro: number;
  crescimento_percentual: number;
  periodo: string;
}

export interface SalesKPIsResponse {
  success: boolean;
  data: SalesKPIs;
}

export interface SalesByProduct {
  produto_servico: string;
  total_vendas: number;
  total_custos: number;
  lucro_bruto: number;
  quantidade: number;
  percentual: number;
}

export interface SalesByProductResponse {
  success: boolean;
  data: SalesByProduct[];
  total_geral: number;
}

export interface SalesEvolution {
  periodo: string;
  total_vendas: number;
  total_custos: number;
  lucro_bruto: number;
  quantidade: number;
}

export interface SalesEvolutionResponse {
  success: boolean;
  data: SalesEvolution[];
}

export interface TopSalesProduct {
  produto_servico: string;
  total_vendas: number;
  total_custos: number;
  lucro_bruto: number;
  quantidade: number;
  margem_lucro: number;
}

export interface TopSalesProductResponse {
  success: boolean;
  data: TopSalesProduct[];
} 