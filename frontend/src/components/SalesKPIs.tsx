import { Sale } from "@/types/sale";

interface SalesKPIsProps {
  sales: Sale[];
}

export default function SalesKPIs({ sales }: SalesKPIsProps) {
  const totalVendido = sales.reduce((acc, s) => acc + s.amount, 0);
  const lucroTotal = sales.reduce((acc, s) => acc + (s.amount - s.custo), 0);
  const ticketMedio = sales.length ? totalVendido / sales.length : 0;

  // Top 5 clientes por valor vendido
  const clientesMap: Record<string, number> = {};
  sales.forEach(s => {
    if (!s.client) return;
    clientesMap[s.client] = (clientesMap[s.client] || 0) + s.amount;
  });
  const topClientes = Object.entries(clientesMap)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div className="bg-white rounded shadow p-4">
        <div className="text-gray-500 text-sm">Total Vendido</div>
        <div className="text-2xl font-bold text-blue-700">{totalVendido.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</div>
      </div>
      <div className="bg-white rounded shadow p-4">
        <div className="text-gray-500 text-sm">Lucro Total</div>
        <div className="text-2xl font-bold text-green-700">{lucroTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</div>
      </div>
      <div className="bg-white rounded shadow p-4">
        <div className="text-gray-500 text-sm">Ticket Médio</div>
        <div className="text-2xl font-bold text-indigo-700">{ticketMedio.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</div>
      </div>
      <div className="bg-white rounded shadow p-4">
        <div className="text-gray-500 text-sm mb-1">Top 5 Clientes</div>
        <ul className="text-sm">
          {topClientes.length === 0 && <li className="text-gray-400">Nenhum cliente</li>}
          {topClientes.map(([cliente, valor]) => (
            <li key={cliente} className="flex justify-between">
              <span>{cliente}</span>
              <span className="font-semibold">{valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
} 