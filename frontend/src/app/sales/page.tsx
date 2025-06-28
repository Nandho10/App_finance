'use client';

import { useState, useEffect } from 'react';
import { FiPlus, FiFilter, FiSearch, FiEdit, FiTrash2, FiDollarSign } from 'react-icons/fi';
import SalesModal from '@/components/SalesModal';
import { Sale } from '@/types/sale';

export default function SalesPage() {
  const [sales, setSales] = useState<Sale[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingSale, setEditingSale] = useState<Sale | null>(null);
  const [filters, setFilters] = useState({
    startDate: '',
    endDate: '',
    produtoServico: '',
    formaRecebimento: ''
  });
  const [showFilters, setShowFilters] = useState(false);

  // Carregar vendas
  const loadSales = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters.startDate) params.append('start_date', filters.startDate);
      if (filters.endDate) params.append('end_date', filters.endDate);
      if (filters.produtoServico) params.append('produto_servico', filters.produtoServico);
      if (filters.formaRecebimento) params.append('forma_recebimento', filters.formaRecebimento);

      const response = await fetch(`/api/sales/?${params}`);
      const data = await response.json();
      
      if (data.success) {
        setSales(data.data);
      }
    } catch (error) {
      console.error('Erro ao carregar vendas:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSales();
  }, [filters]);

  // Criar venda
  const handleCreateSale = async (saleData: Omit<Sale, 'id'>) => {
    try {
      const response = await fetch('/api/sales/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(saleData),
      });

      const data = await response.json();
      if (data.success) {
        setShowModal(false);
        loadSales();
      } else {
        alert('Erro ao criar venda: ' + data.error);
      }
    } catch (error) {
      console.error('Erro ao criar venda:', error);
      alert('Erro ao criar venda');
    }
  };

  // Atualizar venda
  const handleUpdateSale = async (id: number, saleData: Partial<Sale>) => {
    try {
      const response = await fetch(`/api/sales/${id}/update/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(saleData),
      });

      const data = await response.json();
      if (data.success) {
        setShowModal(false);
        setEditingSale(null);
        loadSales();
      } else {
        alert('Erro ao atualizar venda: ' + data.error);
      }
    } catch (error) {
      console.error('Erro ao atualizar venda:', error);
      alert('Erro ao atualizar venda');
    }
  };

  // Excluir venda
  const handleDeleteSale = async (id: number) => {
    if (!confirm('Tem certeza que deseja excluir esta venda?')) return;

    try {
      const response = await fetch(`/api/sales/${id}/delete/`, {
        method: 'DELETE',
      });

      const data = await response.json();
      if (data.success) {
        loadSales();
      } else {
        alert('Erro ao excluir venda: ' + data.error);
      }
    } catch (error) {
      console.error('Erro ao excluir venda:', error);
      alert('Erro ao excluir venda');
    }
  };

  // Abrir modal para edição
  const handleEdit = (sale: Sale) => {
    setEditingSale(sale);
    setShowModal(true);
  };

  // Abrir modal para criação
  const handleCreate = () => {
    setEditingSale(null);
    setShowModal(true);
  };

  // Calcular totais
  const totalVendas = sales.reduce((sum, sale) => sum + sale.valor_venda, 0);
  const totalCustos = sales.reduce((sum, sale) => sum + sale.custo, 0);
  const totalLucro = totalVendas - totalCustos;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Vendas</h1>
        <button
          onClick={handleCreate}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700 transition-colors"
        >
          <FiPlus />
          Nova Venda
        </button>
      </div>

      {/* Cards de Resumo */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total de Vendas</p>
              <p className="text-2xl font-bold text-green-600">
                R$ {totalVendas.toFixed(2)}
              </p>
            </div>
            <FiDollarSign className="text-green-600 text-2xl" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total de Custos</p>
              <p className="text-2xl font-bold text-red-600">
                R$ {totalCustos.toFixed(2)}
              </p>
            </div>
            <FiDollarSign className="text-red-600 text-2xl" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Lucro Bruto</p>
              <p className="text-2xl font-bold text-blue-600">
                R$ {totalLucro.toFixed(2)}
              </p>
            </div>
            <FiDollarSign className="text-blue-600 text-2xl" />
          </div>
        </div>
      </div>

      {/* Filtros */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Filtros</h3>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
          >
            <FiFilter />
            {showFilters ? 'Ocultar' : 'Mostrar'} Filtros
          </button>
        </div>

        {showFilters && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Data Início
              </label>
              <input
                type="date"
                value={filters.startDate}
                onChange={(e) => setFilters({ ...filters, startDate: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Data Fim
              </label>
              <input
                type="date"
                value={filters.endDate}
                onChange={(e) => setFilters({ ...filters, endDate: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Produto/Serviço
              </label>
              <input
                type="text"
                placeholder="Buscar produto..."
                value={filters.produtoServico}
                onChange={(e) => setFilters({ ...filters, produtoServico: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Forma de Recebimento
              </label>
              <select
                value={filters.formaRecebimento}
                onChange={(e) => setFilters({ ...filters, formaRecebimento: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Todas</option>
                <option value="dinheiro">Dinheiro</option>
                <option value="cartao_credito">Cartão de Crédito</option>
                <option value="cartao_debito">Cartão de Débito</option>
                <option value="pix">Pix</option>
                <option value="boleto">Boleto</option>
                <option value="outro">Outro</option>
              </select>
            </div>
          </div>
        )}
      </div>

      {/* Tabela de Vendas */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Data
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Produto/Serviço
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Valor Venda
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Custo
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Lucro Bruto
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Forma Recebimento
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {loading ? (
                <tr>
                  <td colSpan={7} className="px-6 py-4 text-center text-gray-500">
                    Carregando...
                  </td>
                </tr>
              ) : sales.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-6 py-4 text-center text-gray-500">
                    Nenhuma venda encontrada
                  </td>
                </tr>
              ) : (
                sales.map((sale) => (
                  <tr key={sale.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(sale.data).toLocaleDateString('pt-BR')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {sale.produto_servico}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">
                      R$ {sale.valor_venda.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600 font-medium">
                      R$ {sale.custo.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-blue-600 font-medium">
                      R$ {sale.lucro_bruto.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {sale.forma_recebimento}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleEdit(sale)}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          <FiEdit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteSale(sale.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          <FiTrash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <SalesModal
          sale={editingSale}
          onClose={() => {
            setShowModal(false);
            setEditingSale(null);
          }}
          onSave={editingSale ? handleUpdateSale : handleCreateSale}
        />
      )}
    </div>
  );
} 