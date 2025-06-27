import { BudgetProgress as BudgetProgressType } from '@/types/dashboard';

interface BudgetProgressProps {
  data: BudgetProgressType[];
}

export default function BudgetProgress({ data }: BudgetProgressProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 90) return 'bg-danger-500';
    if (percentage >= 75) return 'bg-warning-500';
    return 'bg-success-500';
  };

  return (
    <div className="space-y-4">
      {data.map((item, index) => (
        <div key={index} className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium text-gray-700">{item.category}</span>
            <span className="text-sm text-gray-500">
              {formatCurrency(item.spent)} / {formatCurrency(item.limit)}
            </span>
          </div>
          
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(item.percentage)}`}
              style={{ width: `${Math.min(item.percentage, 100)}%` }}
            />
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-xs text-gray-500">
              {item.percentage}% utilizado
            </span>
            <span className="text-xs text-gray-500">
              {formatCurrency(item.limit - item.spent)} restante
            </span>
          </div>
        </div>
      ))}
      
      <div className="pt-4 border-t border-gray-200">
        <button className="w-full text-primary-600 hover:text-primary-700 font-medium text-sm">
          Gerenciar orçamentos
        </button>
      </div>
    </div>
  );
} 