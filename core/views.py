from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.utils import timezone
import json
from datetime import datetime, timedelta
from decimal import Decimal

# Simulação de dados para o MVP (será substituído por dados reais do banco)
def get_mock_dashboard_data():
    """Dados simulados para o dashboard - será substituído por dados reais"""
    return {
        'balance': 15420.50,
        'income': 8500.00,
        'expenses': 3200.00,
        'savings': 2200.00,
        'transactions': [
            {
                'id': 1,
                'description': 'Salário',
                'amount': 8500.00,
                'type': 'income',
                'date': '2024-01-15',
                'category': 'Salário'
            },
            {
                'id': 2,
                'description': 'Supermercado',
                'amount': -450.00,
                'type': 'expense',
                'date': '2024-01-14',
                'category': 'Alimentação'
            },
            {
                'id': 3,
                'description': 'Combustível',
                'amount': -200.00,
                'type': 'expense',
                'date': '2024-01-13',
                'category': 'Transporte'
            },
            {
                'id': 4,
                'description': 'Freelance',
                'amount': 1200.00,
                'type': 'income',
                'date': '2024-01-12',
                'category': 'Trabalho'
            },
        ],
        'budgetProgress': [
            {
                'category': 'Alimentação',
                'spent': 450,
                'limit': 800,
                'percentage': 56
            },
            {
                'category': 'Transporte',
                'spent': 200,
                'limit': 400,
                'percentage': 50
            },
            {
                'category': 'Lazer',
                'spent': 150,
                'limit': 300,
                'percentage': 50
            },
        ],
        'chartData': [
            {'name': 'Jan', 'income': 8500, 'expenses': 3200},
            {'name': 'Fev', 'income': 7800, 'expenses': 2900},
            {'name': 'Mar', 'income': 9200, 'expenses': 3500},
        ]
    }

# Dados simulados para despesas
mock_expenses = [
    {
        'id': 1,
        'description': 'Supermercado',
        'amount': 450.00,
        'category': 'Alimentação',
        'date': '2024-01-15',
        'payment_method': 'Cartão de Crédito',
        'status': 'paid'
    },
    {
        'id': 2,
        'description': 'Combustível',
        'amount': 200.00,
        'category': 'Transporte',
        'date': '2024-01-14',
        'payment_method': 'Dinheiro',
        'status': 'paid'
    },
    {
        'id': 3,
        'description': 'Cinema',
        'amount': 80.00,
        'category': 'Lazer',
        'date': '2024-01-13',
        'payment_method': 'PIX',
        'status': 'paid'
    },
    {
        'id': 4,
        'description': 'Conta de Luz',
        'amount': 150.00,
        'category': 'Moradia',
        'date': '2024-01-12',
        'payment_method': 'Débito Automático',
        'status': 'pending'
    }
]

# Dados simulados para receitas
mock_incomes = [
    {
        'id': 1,
        'description': 'Salário',
        'amount': 8500.00,
        'category': 'Salário',
        'date': '2024-01-15',
        'source': 'Empresa ABC',
        'status': 'received'
    },
    {
        'id': 2,
        'description': 'Freelance',
        'amount': 1200.00,
        'category': 'Trabalho',
        'date': '2024-01-14',
        'source': 'Cliente XYZ',
        'status': 'received'
    },
    {
        'id': 3,
        'description': 'Investimentos',
        'amount': 500.00,
        'category': 'Investimentos',
        'date': '2024-01-13',
        'source': 'Corretora',
        'status': 'received'
    },
    {
        'id': 4,
        'description': 'Bônus',
        'amount': 2000.00,
        'category': 'Salário',
        'date': '2024-01-12',
        'source': 'Empresa ABC',
        'status': 'pending'
    }
]

# Dados simulados para orçamento
mock_budgets = [
    {
        'id': 1,
        'category': 'Alimentação',
        'limit': 800.00,
        'spent': 450.00,
        'period': '2024-01',
        'status': 'active'
    },
    {
        'id': 2,
        'category': 'Transporte',
        'limit': 400.00,
        'spent': 200.00,
        'period': '2024-01',
        'status': 'active'
    },
    {
        'id': 3,
        'category': 'Lazer',
        'limit': 300.00,
        'spent': 150.00,
        'period': '2024-01',
        'status': 'active'
    },
    {
        'id': 4,
        'category': 'Moradia',
        'limit': 1200.00,
        'spent': 150.00,
        'period': '2024-01',
        'status': 'active'
    },
    {
        'id': 5,
        'category': 'Saúde',
        'limit': 500.00,
        'spent': 0.00,
        'period': '2024-01',
        'status': 'active'
    }
]

# Contadores para IDs únicos
expense_id_counter = len(mock_expenses) + 1
income_id_counter = len(mock_incomes) + 1
budget_id_counter = len(mock_budgets) + 1

# Importar models
from .models import Income, Expense, Category, BudgetPlan, BudgetCategoryLimit
from .models.user_models import User

# Função para obter dados reais do dashboard
def get_real_dashboard_data():
    """Busca dados reais do banco de dados para o dashboard"""
    try:
        # Por enquanto, vamos usar o primeiro usuário ou criar um se não existir
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Usuário',
                'last_name': 'Teste'
            }
        )
        
        # Calcular período (último mês)
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Buscar receitas do mês
        incomes = Income.objects.filter(
            user=user,
            received_at__gte=start_of_month,
            received_at__lte=end_of_month
        )
        total_income = incomes.aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        # Buscar despesas do mês
        expenses = Expense.objects.filter(
            user=user,
            paid_at__gte=start_of_month,
            paid_at__lte=end_of_month
        )
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        # Calcular saldo (receitas - despesas)
        balance = total_income - total_expenses
        
        # Calcular economias (assumindo 25% das receitas)
        savings = total_income * Decimal('0.25')
        
        # Buscar transações recentes (últimas 10)
        recent_incomes = incomes.order_by('-received_at')[:5]
        recent_expenses = expenses.order_by('-paid_at')[:5]
        
        transactions = []
        
        # Adicionar receitas recentes
        for income in recent_incomes:
            transactions.append({
                'id': income.id,
                'description': income.description or 'Receita',
                'amount': float(income.amount),
                'type': 'income',
                'date': income.received_at.strftime('%Y-%m-%d'),
                'category': income.category.name if income.category else 'Geral'
            })
        
        # Adicionar despesas recentes
        for expense in recent_expenses:
            transactions.append({
                'id': expense.id + 1000,  # ID único para despesas
                'description': expense.description or 'Despesa',
                'amount': -float(expense.amount),  # Negativo para despesas
                'type': 'expense',
                'date': expense.paid_at.strftime('%Y-%m-%d'),
                'category': expense.category.name if expense.category else 'Geral'
            })
        
        # Ordenar transações por data
        transactions.sort(key=lambda x: x['date'], reverse=True)
        transactions = transactions[:10]  # Limitar a 10 transações
        
        # Dados do gráfico (últimos 3 meses)
        chart_data = []
        for i in range(3):
            month_date = today - timedelta(days=30*i)
            month_start = month_date.replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            month_income = Income.objects.filter(
                user=user,
                received_at__gte=month_start,
                received_at__lte=month_end
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
            
            month_expenses = Expense.objects.filter(
                user=user,
                paid_at__gte=month_start,
                paid_at__lte=month_end
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
            
            chart_data.append({
                'name': month_date.strftime('%b'),
                'income': float(month_income),
                'expenses': float(month_expenses)
            })
        
        chart_data.reverse()  # Ordenar cronologicamente
        
        # Progresso do orçamento (dados simulados por enquanto)
        budget_progress = [
            {
                'category': 'Alimentação',
                'spent': float(total_expenses * Decimal('0.3')),
                'limit': 800,
                'percentage': min(100, int((float(total_expenses * Decimal('0.3')) / 800) * 100))
            },
            {
                'category': 'Transporte',
                'spent': float(total_expenses * Decimal('0.2')),
                'limit': 400,
                'percentage': min(100, int((float(total_expenses * Decimal('0.2')) / 400) * 100))
            },
            {
                'category': 'Lazer',
                'spent': float(total_expenses * Decimal('0.1')),
                'limit': 300,
                'percentage': min(100, int((float(total_expenses * Decimal('0.1')) / 300) * 100))
            },
        ]
        
        return {
            'balance': float(balance),
            'income': float(total_income),
            'expenses': float(total_expenses),
            'savings': float(savings),
            'transactions': transactions,
            'budgetProgress': budget_progress,
            'chartData': chart_data
        }
        
    except Exception as e:
        print(f"Erro ao buscar dados reais: {e}")
        # Fallback para dados simulados
        return get_mock_dashboard_data()

@csrf_exempt
@require_http_methods(["GET"])
def dashboard_data(request):
    """Endpoint para dados do dashboard"""
    try:
        # TODO: Implementar autenticação real
        # TODO: Buscar dados reais do banco de dados
        
        data = get_real_dashboard_data()
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def kpis(request):
    """Endpoint para KPIs principais"""
    try:
        data = get_real_dashboard_data()
        kpis = {
            'balance': data['balance'],
            'income': data['income'],
            'expenses': data['expenses'],
            'savings': data['savings']
        }
        return JsonResponse(kpis, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def recent_transactions(request):
    """Endpoint para transações recentes"""
    try:
        data = get_real_dashboard_data()
        return JsonResponse(data['transactions'], safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def budget_progress(request):
    """Endpoint para progresso do orçamento"""
    try:
        data = get_real_dashboard_data()
        return JsonResponse(data['budgetProgress'], safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def chart_data(request):
    """Endpoint para dados do gráfico"""
    try:
        data = get_real_dashboard_data()
        return JsonResponse(data['chartData'], safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Endpoints para Despesas
@csrf_exempt
@require_http_methods(["GET"])
def expenses_list(request):
    """Listar todas as despesas do banco de dados"""
    try:
        user = User.objects.filter(username='test_user').first()
        if not user:
            return JsonResponse([], safe=False)
        expenses = Expense.objects.filter(user=user).order_by('-paid_at')
        result = []
        for exp in expenses:
            result.append({
                'id': exp.id,
                'description': exp.description,
                'amount': float(exp.amount),
                'category': exp.category.name if exp.category else '',
                'paid_at': str(exp.paid_at),
                'payment_method': exp.payment_method,
                'status': 'paid',
            })
        return JsonResponse(result, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def expense_create(request):
    """Criar nova despesa (persistente no banco)"""
    try:
        data = json.loads(request.body)
        # Validação básica
        required_fields = ['description', 'amount', 'category', 'paid_at', 'payment_method']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Campo obrigatório: {field}'}, status=400)
        # Buscar usuário de teste (MVP)
        user = User.objects.filter(username='test_user').first()
        if not user:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=400)
        # Buscar categoria pelo nome
        category = Category.objects.filter(user=user, name=data['category'], type='expense').first()
        if not category:
            return JsonResponse({'error': 'Categoria não encontrada'}, status=400)
        # Converter valor para float/decimal
        try:
            amount = str(data['amount']).replace(',', '.')
            amount = float(amount)
        except Exception:
            return JsonResponse({'error': 'Valor inválido'}, status=400)
        # Criar despesa
        expense = Expense.objects.create(
            user=user,
            category=category,
            amount=amount,
            description=data['description'],
            paid_at=data['paid_at'],
            payment_method=data['payment_method']
        )
        # Retornar despesa criada no formato esperado
        resp = {
            'id': expense.id,
            'description': expense.description,
            'amount': float(expense.amount),
            'category': category.name,
            'paid_at': str(expense.paid_at),
            'payment_method': expense.payment_method,
            'status': 'paid',
        }
        return JsonResponse(resp, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def expense_detail(request, expense_id):
    """Buscar despesa específica"""
    try:
        expense = next((exp for exp in mock_expenses if exp['id'] == int(expense_id)), None)
        if not expense:
            return JsonResponse({'error': 'Despesa não encontrada'}, status=404)
        return JsonResponse(expense)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def expense_update(request, expense_id):
    """Atualizar despesa"""
    try:
        data = json.loads(request.body)
        expense = next((exp for exp in mock_expenses if exp['id'] == int(expense_id)), None)
        
        if not expense:
            return JsonResponse({'error': 'Despesa não encontrada'}, status=404)
        
        # Atualizar campos
        expense.update({
            'description': data.get('description', expense['description']),
            'amount': float(data.get('amount', expense['amount'])),
            'category': data.get('category', expense['category']),
            'date': data.get('date', expense['date']),
            'payment_method': data.get('payment_method', expense['payment_method']),
            'status': data.get('status', expense['status'])
        })
        
        return JsonResponse(expense)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def expense_delete(request, expense_id):
    """Deletar despesa"""
    try:
        global mock_expenses
        expense = next((exp for exp in mock_expenses if exp['id'] == int(expense_id)), None)
        
        if not expense:
            return JsonResponse({'error': 'Despesa não encontrada'}, status=404)
        
        mock_expenses = [exp for exp in mock_expenses if exp['id'] != int(expense_id)]
        return JsonResponse({'message': 'Despesa deletada com sucesso'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def expense_categories(request):
    """Listar categorias de despesas"""
    try:
        categories = [
            'Alimentação',
            'Transporte',
            'Moradia',
            'Lazer',
            'Saúde',
            'Educação',
            'Vestuário',
            'Serviços',
            'Outros'
        ]
        return JsonResponse(categories, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Endpoints para Receitas
@csrf_exempt
@require_http_methods(["GET"])
def incomes_list(request):
    """Listar todas as receitas"""
    try:
        # TODO: Implementar filtros por data, categoria, etc.
        return JsonResponse(mock_incomes, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def income_create(request):
    """Criar nova receita"""
    try:
        global income_id_counter
        data = json.loads(request.body)
        
        # Validação básica
        required_fields = ['description', 'amount', 'category', 'date']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Campo obrigatório: {field}'}, status=400)
        
        # Criar nova receita
        new_income = {
            'id': income_id_counter,
            'description': data['description'],
            'amount': float(data['amount']),
            'category': data['category'],
            'date': data['date'],
            'source': data.get('source', ''),
            'status': data.get('status', 'received')
        }
        
        mock_incomes.append(new_income)
        income_id_counter += 1
        
        return JsonResponse(new_income, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def income_detail(request, income_id):
    """Buscar receita específica"""
    try:
        income = next((inc for inc in mock_incomes if inc['id'] == int(income_id)), None)
        if not income:
            return JsonResponse({'error': 'Receita não encontrada'}, status=404)
        return JsonResponse(income)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def income_update(request, income_id):
    """Atualizar receita"""
    try:
        data = json.loads(request.body)
        income = next((inc for inc in mock_incomes if inc['id'] == int(income_id)), None)
        
        if not income:
            return JsonResponse({'error': 'Receita não encontrada'}, status=404)
        
        # Atualizar campos
        income.update({
            'description': data.get('description', income['description']),
            'amount': float(data.get('amount', income['amount'])),
            'category': data.get('category', income['category']),
            'date': data.get('date', income['date']),
            'source': data.get('source', income['source']),
            'status': data.get('status', income['status'])
        })
        
        return JsonResponse(income)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def income_delete(request, income_id):
    """Deletar receita"""
    try:
        global mock_incomes
        income = next((inc for inc in mock_incomes if inc['id'] == int(income_id)), None)
        
        if not income:
            return JsonResponse({'error': 'Receita não encontrada'}, status=404)
        
        mock_incomes = [inc for inc in mock_incomes if inc['id'] != int(income_id)]
        return JsonResponse({'message': 'Receita deletada com sucesso'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def income_categories(request):
    """Listar categorias de receitas"""
    try:
        categories = [
            'Salário',
            'Freelance',
            'Investimentos',
            'Bônus',
            'Comissões',
            'Aluguel',
            'Vendas',
            'Outros'
        ]
        return JsonResponse(categories, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Endpoints para Orçamento
@csrf_exempt
@require_http_methods(["GET"])
def budgets_list(request):
    """Listar todos os orçamentos"""
    try:
        # Calcular gastos reais por categoria
        for budget in mock_budgets:
            category_expenses = [exp for exp in mock_expenses if exp['category'] == budget['category']]
            budget['spent'] = sum(exp['amount'] for exp in category_expenses)
            budget['percentage'] = min(100, (budget['spent'] / budget['limit']) * 100) if budget['limit'] > 0 else 0
            budget['remaining'] = budget['limit'] - budget['spent']
            budget['status'] = 'over' if budget['spent'] > budget['limit'] else 'active'
        
        return JsonResponse(mock_budgets, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def budget_create(request):
    """Criar novo orçamento"""
    try:
        global budget_id_counter
        data = json.loads(request.body)
        
        # Validação básica
        required_fields = ['category', 'limit', 'period']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Campo obrigatório: {field}'}, status=400)
        
        # Verificar se já existe orçamento para esta categoria no período
        existing_budget = next((budget for budget in mock_budgets 
                              if budget['category'] == data['category'] 
                              and budget['period'] == data['period']), None)
        
        if existing_budget:
            return JsonResponse({'error': 'Já existe orçamento para esta categoria neste período'}, status=400)
        
        # Criar novo orçamento
        new_budget = {
            'id': budget_id_counter,
            'category': data['category'],
            'limit': float(data['limit']),
            'spent': 0.00,
            'period': data['period'],
            'status': 'active',
            'percentage': 0,
            'remaining': float(data['limit'])
        }
        
        mock_budgets.append(new_budget)
        budget_id_counter += 1
        
        return JsonResponse(new_budget, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def budget_detail(request, budget_id):
    """Buscar orçamento específico"""
    try:
        budget = next((budget for budget in mock_budgets if budget['id'] == int(budget_id)), None)
        if not budget:
            return JsonResponse({'error': 'Orçamento não encontrado'}, status=404)
        return JsonResponse(budget)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def budget_update(request, budget_id):
    """Atualizar orçamento"""
    try:
        data = json.loads(request.body)
        budget = next((budget for budget in mock_budgets if budget['id'] == int(budget_id)), None)
        
        if not budget:
            return JsonResponse({'error': 'Orçamento não encontrado'}, status=404)
        
        # Atualizar campos
        if 'limit' in data:
            budget['limit'] = float(data['limit'])
            budget['remaining'] = budget['limit'] - budget['spent']
            budget['percentage'] = min(100, (budget['spent'] / budget['limit']) * 100) if budget['limit'] > 0 else 0
            budget['status'] = 'over' if budget['spent'] > budget['limit'] else 'active'
        
        if 'period' in data:
            budget['period'] = data['period']
        
        return JsonResponse(budget)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def budget_delete(request, budget_id):
    """Deletar orçamento"""
    try:
        global mock_budgets
        budget = next((budget for budget in mock_budgets if budget['id'] == int(budget_id)), None)
        
        if not budget:
            return JsonResponse({'error': 'Orçamento não encontrado'}, status=404)
        
        mock_budgets = [budget for budget in mock_budgets if budget['id'] != int(budget_id)]
        return JsonResponse({'message': 'Orçamento deletado com sucesso'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def budget_alerts(request):
    """Buscar alertas de orçamento"""
    try:
        alerts = []
        
        for budget in mock_budgets:
            # Calcular gastos reais
            category_expenses = [exp for exp in mock_expenses if exp['category'] == budget['category']]
            spent = sum(exp['amount'] for exp in category_expenses)
            
            # Verificar alertas
            percentage = (spent / budget['limit']) * 100 if budget['limit'] > 0 else 0
            
            if percentage >= 90:
                alerts.append({
                    'category': budget['category'],
                    'type': 'warning' if percentage < 100 else 'danger',
                    'message': f'Orçamento de {budget["category"]} está em {percentage:.1f}%',
                    'percentage': percentage,
                    'spent': spent,
                    'limit': budget['limit']
                })
        
        return JsonResponse(alerts, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def budget_analysis(request):
    """Análise preditiva do orçamento"""
    try:
        analysis = {
            'total_budget': sum(budget['limit'] for budget in mock_budgets),
            'total_spent': sum(budget['spent'] for budget in mock_budgets),
            'total_remaining': sum(budget['remaining'] for budget in mock_budgets),
            'overall_percentage': 0,
            'predictions': []
        }
        
        if analysis['total_budget'] > 0:
            analysis['overall_percentage'] = (analysis['total_spent'] / analysis['total_budget']) * 100
        
        # Análise por categoria
        for budget in mock_budgets:
            if budget['limit'] > 0:
                daily_rate = budget['spent'] / 15  # Assumindo 15 dias do mês
                days_remaining = 15  # Assumindo mês de 30 dias
                predicted_spent = daily_rate * 30
                
                analysis['predictions'].append({
                    'category': budget['category'],
                    'current_spent': budget['spent'],
                    'predicted_spent': predicted_spent,
                    'will_exceed': predicted_spent > budget['limit'],
                    'excess_amount': max(0, predicted_spent - budget['limit'])
                })
        
        return JsonResponse(analysis, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
