"use client";
import { useEffect, useState } from "react";
import { getSales, createSale, updateSale, deleteSale } from "@/services/api";
import { Sale, SaleFormData } from "@/types/sale";
import SalesModal from "@/components/SalesModal";
import SalesKPIs from "@/components/SalesKPIs";
import SalesCharts from "@/components/SalesCharts";

export default function SalesPage() {
  const [sales, setSales] = useState<Sale[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [editingSale, setEditingSale] = useState<Sale | null>(null);
  const [filters, setFilters] = useState({
    paid_at_start: "",
    paid_at_end: "",
    product: "",
    client: "",
  });

  const fetchSales = async () => {
    setLoading(true);
    try {
      const data = await getSales(filters);
      setSales(data);
      setError(null);
    } catch (e: any) {
      setError(e.message);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchSales();
    // eslint-disable-next-line
  }, [filters]);

  const handleOpenModal = (sale?: Sale) => {
    setEditingSale(sale || null);
    setShowModal(true);
  };
  const handleCloseModal = () => {
    setEditingSale(null);
    setShowModal(false);
  };
  const handleSaveSale = async (data: SaleFormData) => {
    try {
      if (editingSale) {
        await updateSale(editingSale.id, data);
      } else {
        await createSale(data);
      }
      fetchSales();
      handleCloseModal();
    } catch (e: any) {
      alert(e.message);
    }
  };
  const handleDelete = async (id: number) => {
    if (!window.confirm("Deseja realmente excluir esta venda?")) return;
    try {
      await deleteSale(id);
      fetchSales();
    } catch (e: any) {
      alert(e.message);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Vendas</h1>
      <SalesKPIs sales={sales} />
      <SalesCharts sales={sales} />
      {/* Filtros */}
      <div className="flex flex-wrap gap-2 mb-4">
        <input
          type="date"
          value={filters.paid_at_start}
          onChange={e => setFilters(f => ({ ...f, paid_at_start: e.target.value }))}
          className="border px-2 py-1 rounded"
          placeholder="Data início"
        />
        <input
          type="date"
          value={filters.paid_at_end}
          onChange={e => setFilters(f => ({ ...f, paid_at_end: e.target.value }))}
          className="border px-2 py-1 rounded"
          placeholder="Data fim"
        />
        <input
          type="text"
          value={filters.product}
          onChange={e => setFilters(f => ({ ...f, product: e.target.value }))}
          className="border px-2 py-1 rounded"
          placeholder="Produto/Serviço"
        />
        <input
          type="text"
          value={filters.client}
          onChange={e => setFilters(f => ({ ...f, client: e.target.value }))}
          className="border px-2 py-1 rounded"
          placeholder="Cliente"
        />
        <button
          onClick={() => setFilters({ paid_at_start: "", paid_at_end: "", product: "", client: "" })}
          className="ml-2 px-3 py-1 border rounded bg-gray-100 hover:bg-gray-200"
        >
          Limpar
        </button>
      </div>
      {/* Botão Nova Venda */}
      <button
        onClick={() => handleOpenModal()}
        className="mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Nova Venda
      </button>
      {/* Tabela de vendas */}
      {loading ? (
        <div>Carregando...</div>
      ) : error ? (
        <div className="text-red-500">{error}</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full border">
            <thead>
              <tr className="bg-gray-100">
                <th className="p-2 border">Data</th>
                <th className="p-2 border">Produto/Serviço</th>
                <th className="p-2 border">Valor</th>
                <th className="p-2 border">Custo</th>
                <th className="p-2 border">Lucro Bruto</th>
                <th className="p-2 border">Forma de Pagamento</th>
                <th className="p-2 border">Cliente</th>
                <th className="p-2 border">Ações</th>
              </tr>
            </thead>
            <tbody>
              {sales.map(sale => (
                <tr key={sale.id}>
                  <td className="p-2 border">{sale.paid_at}</td>
                  <td className="p-2 border">{sale.product}</td>
                  <td className="p-2 border">{sale.amount.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
                  <td className="p-2 border">{sale.custo.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
                  <td className="p-2 border">{(sale.amount - sale.custo).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
                  <td className="p-2 border">{sale.payment_method}</td>
                  <td className="p-2 border">{sale.client}</td>
                  <td className="p-2 border">
                    <button className="text-blue-600 mr-2" onClick={() => handleOpenModal(sale)}>Editar</button>
                    <button className="text-red-600" onClick={() => handleDelete(sale.id)}>Excluir</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {/* Modal de venda */}
      {showModal && (
        <SalesModal
          sale={editingSale}
          onClose={handleCloseModal}
          onSave={handleSaveSale}
        />
      )}
    </div>
  );
} 