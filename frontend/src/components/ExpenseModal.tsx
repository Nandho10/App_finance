import { useState, useEffect } from 'react';
import { expenseService } from '@/services/api';
import { Expense, CreateExpenseData, UpdateExpenseData } from '@/types/expense';

interface ExpenseModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: (expense: Expense) => void;
  onUpdated?: (expense: Expense) => void;
  editingExpense?: Expense | null;
}

const paymentMethods = [
  { value: 'cash', label: 'Dinheiro' },
  { value: 'credit_card', label: 'Cartão de Crédito' },
  { value: 'pix', label: 'PIX' },
  { value: 'transfer', label: 'Transferência' },
];

export default function ExpenseModal({ 
  isOpen, 
  onClose, 
  onCreated, 
  onUpdated,
  editingExpense 
}: ExpenseModalProps) {
  const [form, setForm] = useState<CreateExpenseData>({
    description: '',
    amount: 0,
    category: '',
    paid_at: '',
    payment_method: 'cash',
  });
  const [categories, setCategories] = useState<{id: number, name: string, type: string}[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const isEditing = !!editingExpense;

  useEffect(() => {
    if (isOpen) {
      expenseService.getCategories().then(setCategories);

      if (isEditing && editingExpense) {
        // Corrige o valor do payment_method se vier como label
        let paymentMethodValue = editingExpense.payment_method;
        const found = paymentMethods.find(pm => pm.value === paymentMethodValue);
        if (!found) {
          // Tenta mapear pelo label (caso tenha vindo como texto)
          const byLabel = paymentMethods.find(pm => pm.label === paymentMethodValue);
          paymentMethodValue = byLabel ? byLabel.value : 'cash';
        }
        setForm({
          description: editingExpense.description,
          amount: editingExpense.amount,
          category: editingExpense.category_id ? String(editingExpense.category_id) : '',
          paid_at: editingExpense.paid_at || editingExpense.date || '',
          payment_method: paymentMethodValue,
        });
      } else {
        // Limpar formulário para nova despesa
        setForm({
          description: '',
          amount: 0,
          category: '',
          paid_at: '',
          payment_method: 'cash',
        });
      }
      setError(null);
      setSuccess(false);
    }
  }, [isOpen, editingExpense, isEditing]);

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
      if (!form.description || !form.amount || !form.category || !form.paid_at) {
        setError('Preencha todos os campos obrigatórios.');
        setLoading(false);
        return;
      }

      if (isEditing && editingExpense) {
        // Atualizar despesa existente
        const updateData: UpdateExpenseData = {
          description: form.description,
          amount: Number(form.amount),
          category_id: Number(form.category),
          paid_at: form.paid_at,
          payment_method: form.payment_method,
        };
        console.log('Payload enviado para atualização:', updateData);
        const updatedExpense = await expenseService.updateExpense(editingExpense.id, updateData);
        setSuccess(true);
        onUpdated?.(updatedExpense);
        setTimeout(() => {
          setSuccess(false);
          onClose();
        }, 1000);
      } else {
        // Criar nova despesa
        const data = { ...form, amount: Number(form.amount), category_id: Number(form.category) };
        delete data.category;
        const expense = await expenseService.createExpense(data);
        setSuccess(true);
        onCreated(expense);
        setTimeout(() => {
          setSuccess(false);
          onClose();
        }, 1000);
      }
    } catch (err) {
      setError(isEditing ? 'Erro ao atualizar despesa.' : 'Erro ao cadastrar despesa.');
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
          {isEditing ? 'Editar Despesa' : 'Nova Despesa'}
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
              name="paid_at"
              value={form.paid_at}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
              required
              disabled={loading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Método de Pagamento*</label>
            <select
              name="payment_method"
              value={form.payment_method}
              onChange={handleChange}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2"
              required
              disabled={loading}
            >
              {paymentMethods.map((pm) => (
                <option key={pm.value} value={pm.value}>{pm.label}</option>
              ))}
            </select>
          </div>
          {error && <div className="text-red-600 text-sm">{error}</div>}
          {success && <div className="text-green-600 text-sm">
            {isEditing ? 'Despesa atualizada com sucesso!' : 'Despesa cadastrada com sucesso!'}
          </div>}
          <div className="flex justify-end">
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              disabled={loading}
            >
              {loading ? 'Salvando...' : (isEditing ? 'Atualizar' : 'Salvar')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 