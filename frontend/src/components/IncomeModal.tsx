import { useState, useEffect } from 'react';
import { incomeService } from '@/services/api';
import { CreateIncomeData, Income, UpdateIncomeData } from '@/types/income';

interface IncomeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: (income: Income) => void;
  onUpdated?: (income: Income) => void;
  editingIncome?: Income | null;
}

export default function IncomeModal({ 
  isOpen, 
  onClose, 
  onCreated, 
  onUpdated,
  editingIncome 
}: IncomeModalProps) {
  const [form, setForm] = useState<CreateIncomeData>({
    description: '',
    amount: 0,
    category: '',
    date: '',
    source: '',
    status: 'received',
  });
  const [categories, setCategories] = useState<{ id: number; name: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const isEditing = !!editingIncome;

  useEffect(() => {
    if (isOpen) {
      incomeService.getCategories().then((cats: any) => {
        // Suporte tanto para array de string quanto array de objetos
        if (Array.isArray(cats) && typeof cats[0] === 'object') {
          setCategories(cats);
        } else if (Array.isArray(cats)) {
          setCategories(cats.map((name: string, idx: number) => ({ id: idx, name })));
        }
      });

      if (isEditing && editingIncome) {
        // Preencher formulário com dados da receita sendo editada
        setForm({
          description: editingIncome.description,
          amount: editingIncome.amount,
          category: editingIncome.category,
          date: editingIncome.date,
          source: editingIncome.source || '',
          status: editingIncome.status,
        });
      } else {
        // Limpar formulário para nova receita
        setForm({
          description: '',
          amount: 0,
          category: '',
          date: '',
          source: '',
          status: 'received',
        });
      }
      setError(null);
      setSuccess(false);
    }
  }, [isOpen, editingIncome, isEditing]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);
    try {
      if (!form.description || !form.amount || !form.category || !form.date) {
        setError('Preencha todos os campos obrigatórios.');
        setLoading(false);
        return;
      }

      if (isEditing && editingIncome) {
        // Atualizar receita existente
        const updateData: UpdateIncomeData = {
          description: form.description,
          amount: Number(form.amount),
          category_id: Number(form.category),
          date: form.date,
          source: form.source,
          status: form.status,
        };
        const updatedIncome = await incomeService.updateIncome(editingIncome.id, updateData);
        setSuccess(true);
        onUpdated?.(updatedIncome);
        setTimeout(() => {
          setSuccess(false);
          onClose();
        }, 1000);
      } else {
        // Criar nova receita
        const data = { ...form, amount: Number(form.amount), category_id: Number(form.category) };
        delete data.category;
        const income = await incomeService.createIncome(data);
        setSuccess(true);
        onCreated(income);
        setTimeout(() => {
          setSuccess(false);
          onClose();
        }, 1000);
      }
    } catch (err) {
      setError(isEditing ? 'Erro ao atualizar receita.' : 'Erro ao cadastrar receita.');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-md p-6 relative">
        <button
          className="absolute top-2 right-2 text-gray-400 hover:text-gray-700"
          onClick={onClose}
          disabled={loading}
        >
          ×
        </button>
        <h2 className="text-2xl font-bold mb-4">
          {isEditing ? 'Editar Receita' : 'Nova Receita'}
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Descrição*</label>
            <input
              type="text"
              name="description"
              value={form.description}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
              required
              disabled={loading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Valor (R$)*</label>
            <input
              type="number"
              name="amount"
              value={form.amount}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
              min="0.01"
              step="0.01"
              required
              disabled={loading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Categoria*</label>
            <select
              name="category"
              value={form.category}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
              required
              disabled={loading}
            >
              <option value="">Selecione</option>
              {categories.map((cat) => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Data*</label>
            <input
              type="date"
              name="date"
              value={form.date}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
              required
              disabled={loading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Fonte</label>
            <input
              type="text"
              name="source"
              value={form.source}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
              disabled={loading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Status</label>
            <select
              name="status"
              value={form.status}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
              disabled={loading}
            >
              <option value="received">Recebido</option>
              <option value="pending">Pendente</option>
              <option value="overdue">Atrasado</option>
            </select>
          </div>
          {error && <div className="text-red-600 text-sm">{error}</div>}
          {success && <div className="text-green-600 text-sm">
            {isEditing ? 'Receita atualizada com sucesso!' : 'Receita cadastrada com sucesso!'}
          </div>}
          <button
            type="submit"
            className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
            disabled={loading}
          >
            {loading ? 'Salvando...' : (isEditing ? 'Atualizar' : 'Salvar')}
          </button>
        </form>
      </div>
    </div>
  );
} 