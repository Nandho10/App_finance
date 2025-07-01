import { useState, useEffect } from 'react';
import { FiX } from 'react-icons/fi';
import { Sale, SaleFormData } from '@/types/sale';

interface SalesModalProps {
  sale?: Sale | null;
  onClose: () => void;
  onSave: (data: SaleFormData | Partial<Sale>) => void;
}

export default function SalesModal({ sale, onClose, onSave }: SalesModalProps) {
  const [formData, setFormData] = useState<SaleFormData>({
    paid_at: '',
    product: '',
    amount: 0,
    custo: 0,
    payment_method: '',
    observacoes: '',
    delivery_date: '',
    client: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (sale) {
      setFormData({
        paid_at: sale.paid_at,
        product: sale.product,
        amount: sale.amount,
        custo: sale.custo,
        payment_method: sale.payment_method,
        observacoes: sale.observacoes || '',
        delivery_date: sale.delivery_date || '',
        client: sale.client || ''
      });
    } else {
      const today = new Date().toISOString().split('T')[0];
      setFormData({
        paid_at: today,
        product: '',
        amount: 0,
        custo: 0,
        payment_method: '',
        observacoes: '',
        delivery_date: '',
        client: ''
      });
    }
  }, [sale]);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    if (!formData.paid_at) {
      newErrors.paid_at = 'Data de Pagamento é obrigatória';
    }
    if (!formData.product.trim()) {
      newErrors.product = 'Produto é obrigatório';
    }
    if (formData.amount <= 0) {
      newErrors.amount = 'Valor deve ser maior que zero';
    }
    if (formData.custo < 0) {
      newErrors.custo = 'Custo não pode ser negativo';
    }
    if (!formData.payment_method) {
      newErrors.payment_method = 'Forma de Pagamento é obrigatória';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) {
      return;
    }
    onSave(formData);
  };

  const handleInputChange = (field: keyof SaleFormData, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: ''
      }));
    }
  };

  const lucroBruto = formData.amount - formData.custo;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-800">
            {sale ? 'Editar Venda' : 'Nova Venda'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <FiX className="w-5 h-5" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Data de Pagamento */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Data de Pagamento *
            </label>
            <input
              type="date"
              value={formData.paid_at}
              onChange={(e) => handleInputChange('paid_at', e.target.value)}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.paid_at ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.paid_at && (
              <p className="text-red-500 text-sm mt-1">{errors.paid_at}</p>
            )}
          </div>
          {/* Data de Entrega */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Data de Entrega
            </label>
            <input
              type="date"
              value={formData.delivery_date || ''}
              onChange={(e) => handleInputChange('delivery_date', e.target.value)}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 border-gray-300"
            />
          </div>
          {/* Cliente */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Cliente
            </label>
            <input
              type="text"
              value={formData.client || ''}
              onChange={(e) => handleInputChange('client', e.target.value)}
              placeholder="Nome do cliente"
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 border-gray-300"
            />
          </div>
          {/* Produto */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Produto *
            </label>
            <input
              type="text"
              value={formData.product}
              onChange={(e) => handleInputChange('product', e.target.value)}
              placeholder="Digite o produto"
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.product ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.product && (
              <p className="text-red-500 text-sm mt-1">{errors.product}</p>
            )}
          </div>
          {/* Valor */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Valor *
            </label>
            <input
              type="number"
              step="0.01"
              min="0"
              value={formData.amount}
              onChange={(e) => handleInputChange('amount', parseFloat(e.target.value) || 0)}
              placeholder="0,00"
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.amount ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.amount && (
              <p className="text-red-500 text-sm mt-1">{errors.amount}</p>
            )}
          </div>
          {/* Custo */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Custo *
            </label>
            <input
              type="number"
              step="0.01"
              min="0"
              value={formData.custo}
              onChange={(e) => handleInputChange('custo', parseFloat(e.target.value) || 0)}
              placeholder="0,00"
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.custo ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.custo && (
              <p className="text-red-500 text-sm mt-1">{errors.custo}</p>
            )}
          </div>
          {/* Forma de Pagamento */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Forma de Pagamento *
            </label>
            <select
              value={formData.payment_method}
              onChange={(e) => handleInputChange('payment_method', e.target.value)}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.payment_method ? 'border-red-500' : 'border-gray-300'
              }`}
            >
              <option value="">Selecione a forma de pagamento</option>
              <option value="dinheiro">Dinheiro</option>
              <option value="cartao_credito">Cartão de Crédito</option>
              <option value="cartao_debito">Cartão de Débito</option>
              <option value="pix">Pix</option>
              <option value="boleto">Boleto</option>
              <option value="outro">Outro</option>
            </select>
            {errors.payment_method && (
              <p className="text-red-500 text-sm mt-1">{errors.payment_method}</p>
            )}
          </div>
          {/* Observações */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Observações
            </label>
            <textarea
              value={formData.observacoes}
              onChange={(e) => handleInputChange('observacoes', e.target.value)}
              placeholder="Observações (opcional)"
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 border-gray-300"
            />
          </div>
          {/* Lucro Bruto (Calculado) */}
          <div className="bg-gray-50 p-3 rounded-md">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Lucro Bruto (calculado)
            </label>
            <div className="text-lg font-semibold text-green-700">
              {lucroBruto.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
            </div>
          </div>
          {/* Botões */}
          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              {sale ? 'Salvar Alterações' : 'Cadastrar Venda'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 