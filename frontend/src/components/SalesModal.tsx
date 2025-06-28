'use client';

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
    data: '',
    produto_servico: '',
    valor_venda: 0,
    custo: 0,
    forma_recebimento: '',
    observacoes: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (sale) {
      setFormData({
        data: sale.data,
        produto_servico: sale.produto_servico,
        valor_venda: sale.valor_venda,
        custo: sale.custo,
        forma_recebimento: sale.forma_recebimento,
        observacoes: sale.observacoes || ''
      });
    } else {
      // Definir data atual para nova venda
      const today = new Date().toISOString().split('T')[0];
      setFormData({
        data: today,
        produto_servico: '',
        valor_venda: 0,
        custo: 0,
        forma_recebimento: '',
        observacoes: ''
      });
    }
  }, [sale]);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.data) {
      newErrors.data = 'Data é obrigatória';
    }

    if (!formData.produto_servico.trim()) {
      newErrors.produto_servico = 'Produto/Serviço é obrigatório';
    }

    if (formData.valor_venda <= 0) {
      newErrors.valor_venda = 'Valor da venda deve ser maior que zero';
    }

    if (formData.custo < 0) {
      newErrors.custo = 'Custo não pode ser negativo';
    }

    if (!formData.forma_recebimento) {
      newErrors.forma_recebimento = 'Forma de recebimento é obrigatória';
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

    // Limpar erro do campo quando o usuário começar a digitar
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: ''
      }));
    }
  };

  const lucroBruto = formData.valor_venda - formData.custo;

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
          {/* Data */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Data *
            </label>
            <input
              type="date"
              value={formData.data}
              onChange={(e) => handleInputChange('data', e.target.value)}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.data ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.data && (
              <p className="text-red-500 text-sm mt-1">{errors.data}</p>
            )}
          </div>

          {/* Produto/Serviço */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Produto/Serviço *
            </label>
            <input
              type="text"
              value={formData.produto_servico}
              onChange={(e) => handleInputChange('produto_servico', e.target.value)}
              placeholder="Digite o produto ou serviço"
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.produto_servico ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.produto_servico && (
              <p className="text-red-500 text-sm mt-1">{errors.produto_servico}</p>
            )}
          </div>

          {/* Valor da Venda */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Valor da Venda *
            </label>
            <input
              type="number"
              step="0.01"
              min="0"
              value={formData.valor_venda}
              onChange={(e) => handleInputChange('valor_venda', parseFloat(e.target.value) || 0)}
              placeholder="0,00"
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.valor_venda ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.valor_venda && (
              <p className="text-red-500 text-sm mt-1">{errors.valor_venda}</p>
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

          {/* Lucro Bruto (Calculado) */}
          <div className="bg-gray-50 p-3 rounded-md">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Lucro Bruto
            </label>
            <p className="text-lg font-semibold text-blue-600">
              R$ {lucroBruto.toFixed(2)}
            </p>
          </div>

          {/* Forma de Recebimento */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Forma de Recebimento *
            </label>
            <select
              value={formData.forma_recebimento}
              onChange={(e) => handleInputChange('forma_recebimento', e.target.value)}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.forma_recebimento ? 'border-red-500' : 'border-gray-300'
              }`}
            >
              <option value="">Selecione...</option>
              <option value="dinheiro">Dinheiro</option>
              <option value="cartao_credito">Cartão de Crédito</option>
              <option value="cartao_debito">Cartão de Débito</option>
              <option value="pix">Pix</option>
              <option value="boleto">Boleto</option>
              <option value="outro">Outro</option>
            </select>
            {errors.forma_recebimento && (
              <p className="text-red-500 text-sm mt-1">{errors.forma_recebimento}</p>
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
              placeholder="Observações adicionais..."
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
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
              {sale ? 'Atualizar' : 'Criar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 