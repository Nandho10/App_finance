import { TrendingUp, TrendingDown, DollarSign, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { KPICardProps } from '@/types/dashboard';

export default function KPICard({ title, value, type, trend, trendDirection }: KPICardProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  };

  const getIcon = () => {
    switch (type) {
      case 'balance':
        return <DollarSign className="text-primary-600" size={24} />;
      case 'income':
        return <ArrowUpRight className="text-success-600" size={24} />;
      case 'expense':
        return <ArrowDownRight className="text-danger-600" size={24} />;
      case 'savings':
        return <TrendingUp className="text-warning-600" size={24} />;
      default:
        return <DollarSign className="text-gray-600" size={24} />;
    }
  };

  const getColorClass = () => {
    switch (type) {
      case 'balance':
        return 'text-primary-600';
      case 'income':
        return 'text-success-600';
      case 'expense':
        return 'text-danger-600';
      case 'savings':
        return 'text-warning-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className={`text-2xl font-bold ${getColorClass()}`}>
            {formatCurrency(value)}
          </p>
        </div>
        <div className="p-3 bg-gray-50 rounded-lg">
          {getIcon()}
        </div>
      </div>
      
      <div className="mt-4 flex items-center space-x-2">
        {trendDirection === 'up' ? (
          <TrendingUp size={16} className="text-success-600" />
        ) : (
          <TrendingDown size={16} className="text-danger-600" />
        )}
        <span className={`text-sm font-medium ${
          trendDirection === 'up' ? 'text-success-600' : 'text-danger-600'
        }`}>
          {trend}
        </span>
        <span className="text-sm text-gray-500">vs mês anterior</span>
      </div>
    </div>
  );
} 