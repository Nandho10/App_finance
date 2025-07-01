import { Sale } from "@/types/sale";
import { Bar, Line, Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Tooltip,
  Legend,
  TimeScale,
  Filler,
} from "chart.js";
import "chartjs-adapter-date-fns";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Tooltip,
  Legend,
  TimeScale,
  Filler
);

interface SalesChartsProps {
  sales: Sale[];
}

export default function SalesCharts({ sales }: SalesChartsProps) {
  // Gráfico de barras: volume de vendas por produto
  const produtosMap: Record<string, number> = {};
  sales.forEach(s => {
    produtosMap[s.product] = (produtosMap[s.product] || 0) + s.amount;
  });
  const produtosLabels = Object.keys(produtosMap);
  const produtosData = Object.values(produtosMap);

  // Gráfico de linhas: evolução do lucro ao longo do tempo (por mês)
  const lucroPorMes: Record<string, number> = {};
  sales.forEach(s => {
    const mes = s.paid_at.slice(0, 7); // yyyy-mm
    lucroPorMes[mes] = (lucroPorMes[mes] || 0) + (s.amount - s.custo);
  });
  const meses = Object.keys(lucroPorMes).sort();
  const lucros = meses.map(m => lucroPorMes[m]);

  // Gráfico de rosca: top 5 clientes
  const clientesMap: Record<string, number> = {};
  sales.forEach(s => {
    if (!s.client) return;
    clientesMap[s.client] = (clientesMap[s.client] || 0) + s.amount;
  });
  const topClientes = Object.entries(clientesMap)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);
  const clientesLabels = topClientes.map(([c]) => c);
  const clientesData = topClientes.map(([, v]) => v);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div className="bg-white rounded shadow p-4">
        <div className="font-semibold mb-2">Vendas por Produto/Serviço</div>
        <Bar
          data={{
            labels: produtosLabels,
            datasets: [
              {
                label: "Total Vendido (R$)",
                data: produtosData,
                backgroundColor: "#2563eb",
              },
            ],
          }}
          options={{
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } },
          }}
        />
      </div>
      <div className="bg-white rounded shadow p-4">
        <div className="font-semibold mb-2">Evolução do Lucro (mensal)</div>
        <Line
          data={{
            labels: meses,
            datasets: [
              {
                label: "Lucro Bruto (R$)",
                data: lucros,
                borderColor: "#16a34a",
                backgroundColor: "#bbf7d0",
                fill: true,
                tension: 0.3,
              },
            ],
          }}
          options={{
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } },
          }}
        />
      </div>
      <div className="bg-white rounded shadow p-4">
        <div className="font-semibold mb-2">Top 5 Clientes</div>
        <Doughnut
          data={{
            labels: clientesLabels,
            datasets: [
              {
                label: "Total Vendido (R$)",
                data: clientesData,
                backgroundColor: [
                  "#2563eb",
                  "#16a34a",
                  "#f59e42",
                  "#f43f5e",
                  "#a21caf",
                ],
              },
            ],
          }}
          options={{
            responsive: true,
            plugins: { legend: { position: "bottom" } },
          }}
        />
      </div>
    </div>
  );
} 