'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { ChartData } from '@/types/dashboard';

interface TransactionChartProps {
  data: ChartData[];
}

export default function TransactionChart({ data }: TransactionChartProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {formatCurrency(entry.value)}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="name" 
            stroke="#6b7280"
            fontSize={12}
          />
          <YAxis 
            stroke="#6b7280"
            fontSize={12}
            tickFormatter={formatCurrency}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="income" 
            stroke="#22c55e" 
            strokeWidth={3}
            dot={{ fill: '#22c55e', strokeWidth: 2, r: 6 }}
            activeDot={{ r: 8 }}
            name="Receitas"
          />
          <Line 
            type="monotone" 
            dataKey="expenses" 
            stroke="#ef4444" 
            strokeWidth={3}
            dot={{ fill: '#ef4444', strokeWidth: 2, r: 6 }}
            activeDot={{ r: 8 }}
            name="Despesas"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
} 