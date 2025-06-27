import { ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { Transaction } from '@/types/dashboard';

interface RecentTransactionsProps {
  transactions: Transaction[];
}

export default function RecentTransactions({ transactions }: RecentTransactionsProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(Math.abs(value));
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  return (
    <div className="space-y-4">
      {transactions.map((transaction) => (
        <div key={transaction.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center space-x-3">
            <div className={`p-2 rounded-full ${
              transaction.type === 'income' 
                ? 'bg-success-100 text-success-600' 
                : 'bg-danger-100 text-danger-600'
            }`}>
              {transaction.type === 'income' ? (
                <ArrowUpRight size={16} />
              ) : (
                <ArrowDownRight size={16} />
              )}
            </div>
            
            <div>
              <p className="font-medium text-gray-900">{transaction.description}</p>
              <p className="text-sm text-gray-500">{transaction.category}</p>
            </div>
          </div>
          
          <div className="text-right">
            <p className={`font-semibold ${
              transaction.type === 'income' ? 'text-success-600' : 'text-danger-600'
            }`}>
              {transaction.type === 'income' ? '+' : '-'} {formatCurrency(transaction.amount)}
            </p>
            <p className="text-sm text-gray-500">{formatDate(transaction.date)}</p>
          </div>
        </div>
      ))}
      
      <div className="text-center pt-4">
        <button className="text-primary-600 hover:text-primary-700 font-medium">
          Ver todas as transações
        </button>
      </div>
    </div>
  );
} 