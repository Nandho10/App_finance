from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q, F, Count
from django.utils import timezone
from django.core.serializers import serialize
from django.forms.models import model_to_dict
import json
from datetime import datetime, timedelta
from decimal import Decimal
from django.db import transaction

# Importar modelos
from .models.category_models import Category
from .models.transaction_models import Income, Expense
from .models.sales_models import Venda
from .models.user_models import User

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
    """Atualizar despesa no banco de dados"""
    try:
        data = json.loads(request.body)
        from core.models.transaction_models import Expense
        expense = Expense.objects.filter(id=expense_id).first()
        
        if not expense:
            return JsonResponse({'error': 'Despesa não encontrada'}, status=404)
        
        # Atualizar campos
        if 'description' in data:
            expense.description = data['description']
        
        if 'amount' in data:
            expense.amount = Decimal(str(data['amount']))
        
        if 'category' in data:
            if data['category']:
                category = Category.objects.filter(name=data['category'], type='expense').first()
                if not category:
                    return JsonResponse({'error': 'Categoria não encontrada'}, status=400)
                expense.category = category
            else:
                expense.category = None
        
        if 'paid_at' in data:
            expense.paid_at = datetime.strptime(data['paid_at'], '%Y-%m-%d').date()
        
        if 'payment_method' in data:
            expense.payment_method = data['payment_method']
        
        expense.save()
        
        return JsonResponse({
            'id': expense.id,
            'description': expense.description,
            'amount': float(expense.amount),
            'category': expense.category.name if expense.category else 'Sem categoria',
            'date': expense.paid_at.strftime('%Y-%m-%d'),
            'paid_at': expense.paid_at.strftime('%Y-%m-%d'),
            'payment_method': expense.payment_method,
            'status': 'paid',
            'created_at': expense.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': f'Valor inválido: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def expense_delete(request, expense_id):
    """Deletar despesa (do banco de dados)"""
    try:
        from core.models.transaction_models import Expense
        expense = Expense.objects.filter(id=expense_id).first()
        if not expense:
            return JsonResponse({'error': 'Despesa não encontrada'}, status=404)
        expense.delete()
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

@csrf_exempt
@require_http_methods(["GET"])
def expense_categories_list(request):
    """Listar categorias de despesas do banco de dados"""
    try:
        categories = Category.objects.filter(type='expense').values('id', 'name', 'type')
        return JsonResponse(list(categories), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Endpoints para Receitas
@csrf_exempt
@require_http_methods(["GET"])
def incomes_list(request):
    """Listar todas as receitas do banco de dados"""
    try:
        # Buscar receitas do banco de dados
        incomes = Income.objects.select_related('category').all()
        
        # Converter para formato JSON
        incomes_data = []
        for income in incomes:
            incomes_data.append({
                'id': income.id,
                'description': income.description,
                'amount': float(income.amount),
                'category': income.category.name if income.category else 'Sem categoria',
                'category_id': income.category.id if income.category else None,
                'date': income.received_at.strftime('%Y-%m-%d'),
                'source': income.description,  # Usar description como source
                'status': 'received',  # Assumir que todas estão recebidas
                'created_at': income.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return JsonResponse(incomes_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def income_create(request):
    """Criar nova receita no banco de dados"""
    try:
        data = json.loads(request.body)
        
        # Validação básica
        required_fields = ['description', 'amount', 'date']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Campo obrigatório: {field}'}, status=400)
        
        # Buscar categoria se fornecida
        category = None
        if 'category_id' in data and data['category_id']:
            category = Category.objects.filter(id=data['category_id'], type='income').first()
            if not category:
                return JsonResponse({'error': 'Categoria não encontrada'}, status=400)
        
        # Criar nova receita
        income = Income.objects.create(
            description=data['description'],
            amount=Decimal(str(data['amount'])),
            category=category,
            received_at=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            user_id=1  # TODO: Usar usuário autenticado
        )
        
        return JsonResponse({
            'id': income.id,
            'description': income.description,
            'amount': float(income.amount),
            'category': income.category.name if income.category else 'Sem categoria',
            'category_id': income.category.id if income.category else None,
            'date': income.received_at.strftime('%Y-%m-%d'),
            'source': income.description,
            'status': 'received',
            'created_at': income.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': f'Valor inválido: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def income_detail(request, income_id):
    """Buscar receita específica do banco de dados"""
    try:
        income = Income.objects.select_related('category').filter(id=income_id).first()
        if not income:
            return JsonResponse({'error': 'Receita não encontrada'}, status=404)
        
        return JsonResponse({
            'id': income.id,
            'description': income.description,
            'amount': float(income.amount),
            'category': income.category.name if income.category else 'Sem categoria',
            'category_id': income.category.id if income.category else None,
            'date': income.received_at.strftime('%Y-%m-%d'),
            'source': income.description,
            'status': 'received',
            'created_at': income.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def income_update(request, income_id):
    """Atualizar receita no banco de dados"""
    try:
        data = json.loads(request.body)
        income = Income.objects.filter(id=income_id).first()
        
        if not income:
            return JsonResponse({'error': 'Receita não encontrada'}, status=404)
        
        # Atualizar campos
        if 'description' in data:
            income.description = data['description']
        
        if 'amount' in data:
            income.amount = Decimal(str(data['amount']))
        
        if 'date' in data:
            income.received_at = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        if 'category_id' in data:
            if data['category_id']:
                category = Category.objects.filter(id=data['category_id'], type='income').first()
                if not category:
                    return JsonResponse({'error': 'Categoria não encontrada'}, status=400)
                income.category = category
            else:
                income.category = None
        
        income.save()
        
        return JsonResponse({
            'id': income.id,
            'description': income.description,
            'amount': float(income.amount),
            'category': income.category.name if income.category else 'Sem categoria',
            'category_id': income.category.id if income.category else None,
            'date': income.received_at.strftime('%Y-%m-%d'),
            'source': income.description,
            'status': 'received',
            'created_at': income.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': f'Valor inválido: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def income_delete(request, income_id):
    """Deletar receita do banco de dados"""
    try:
        income = Income.objects.filter(id=income_id).first()
        
        if not income:
            return JsonResponse({'error': 'Receita não encontrada'}, status=404)
        
        income.delete()
        return JsonResponse({'message': 'Receita deletada com sucesso'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def income_categories(request):
    """Listar categorias de receitas do banco de dados"""
    try:
        # Buscar categorias de receitas do banco de dados
        categories = Category.objects.filter(type='income').values('id', 'name', 'type')
        return JsonResponse(list(categories), safe=False)
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

# Endpoints CRUD para Categorias de Receitas
@csrf_exempt
@require_http_methods(["POST"])
def income_category_create(request):
    """Criar nova categoria de receita"""
    try:
        data = json.loads(request.body)
        
        # Validação básica
        required_fields = ['name']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Campo obrigatório: {field}'}, status=400)
        
        # Verificar se já existe categoria com este nome
        existing_category = Category.objects.filter(
            name=data['name'], 
            type='income'
        ).first()
        
        if existing_category:
            return JsonResponse({'error': 'Já existe uma categoria com este nome'}, status=400)
        
        # Criar nova categoria
        category = Category.objects.create(
            name=data['name'],
            type='income',
            user_id=1  # TODO: Usar usuário autenticado
        )
        
        return JsonResponse({
            'id': category.id,
            'name': category.name,
            'type': category.type
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def income_category_detail(request, category_id):
    """Buscar categoria específica"""
    try:
        category = Category.objects.filter(id=category_id, type='income').first()
        if not category:
            return JsonResponse({'error': 'Categoria não encontrada'}, status=404)
        
        return JsonResponse({
            'id': category.id,
            'name': category.name,
            'type': category.type
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def income_category_update(request, category_id):
    """Atualizar categoria de receita"""
    try:
        data = json.loads(request.body)
        category = Category.objects.filter(id=category_id, type='income').first()
        
        if not category:
            return JsonResponse({'error': 'Categoria não encontrada'}, status=404)
        
        # Verificar se o novo nome já existe em outra categoria
        if 'name' in data:
            existing_category = Category.objects.filter(
                name=data['name'], 
                type='income'
            ).exclude(id=category_id).first()
            
            if existing_category:
                return JsonResponse({'error': 'Já existe uma categoria com este nome'}, status=400)
            
            category.name = data['name']
            category.save()
        
        return JsonResponse({
            'id': category.id,
            'name': category.name,
            'type': category.type
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def income_category_delete(request, category_id):
    """Deletar categoria de receita com lógica de migração"""
    try:
        category = Category.objects.filter(id=category_id, type='income').first()
        
        if not category:
            return JsonResponse({'error': 'Categoria não encontrada'}, status=404)
        
        # Verificar se existem receitas nesta categoria
        incomes_count = Income.objects.filter(category=category).count()
        
        if incomes_count > 0:
            # Se há receitas, retornar informações para o frontend decidir
            return JsonResponse({
                'message': f'Esta categoria possui {incomes_count} receita(s)',
                'incomes_count': incomes_count,
                'category_id': category_id,
                'category_name': category.name,
                'requires_action': True
            }, status=409)
        
        # Se não há receitas, deletar diretamente
        category.delete()
        return JsonResponse({'message': 'Categoria deletada com sucesso'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def income_category_migrate(request, category_id):
    """Migrar receitas de uma categoria para outra antes de deletar"""
    try:
        data = json.loads(request.body)
        
        if 'target_category_id' not in data:
            return JsonResponse({'error': 'ID da categoria de destino é obrigatório'}, status=400)
        
        source_category = Category.objects.filter(id=category_id, type='income').first()
        target_category = Category.objects.filter(id=data['target_category_id'], type='income').first()
        
        if not source_category:
            return JsonResponse({'error': 'Categoria de origem não encontrada'}, status=404)
        
        if not target_category:
            return JsonResponse({'error': 'Categoria de destino não encontrada'}, status=404)
        
        # Migrar todas as receitas
        migrated_count = Income.objects.filter(category=source_category).update(category=target_category)
        
        # Deletar categoria de origem
        source_category.delete()
        
        return JsonResponse({
            'message': f'{migrated_count} receita(s) migrada(s) com sucesso',
            'migrated_count': migrated_count
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def income_category_delete_with_incomes(request, category_id):
    """Deletar categoria e todas as suas receitas"""
    try:
        category = Category.objects.filter(id=category_id, type='income').first()
        
        if not category:
            return JsonResponse({'error': 'Categoria não encontrada'}, status=404)
        
        # Deletar todas as receitas da categoria
        deleted_incomes = Income.objects.filter(category=category).delete()
        
        # Deletar a categoria
        category.delete()
        
        return JsonResponse({
            'message': f'Categoria e {deleted_incomes[0]} receita(s) deletada(s) com sucesso',
            'deleted_incomes_count': deleted_incomes[0]
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def import_income_excel_api(request):
    """Importar receitas e categorias via Excel via API"""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'Arquivo não fornecido'}, status=400)
        
        uploaded_file = request.FILES['file']
        
        # Verificar extensão do arquivo
        if not uploaded_file.name.endswith(('.xlsx', '.xls')):
            return JsonResponse({'error': 'Arquivo deve ser Excel (.xlsx ou .xls)'}, status=400)
        
        # Salvar arquivo temporariamente
        import tempfile
        import os
        import pandas as pd
        from django.core.files.storage import default_storage
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            for chunk in uploaded_file.chunks():
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name
        
        try:
            # Ler arquivo Excel
            df = pd.read_excel(tmp_file_path)
            
            # Mapeamento padrão de colunas
            column_mapping = {
                'description': ['descrição', 'description', 'desc', 'nome'],
                'amount': ['valor', 'amount', 'montante', 'preço'],
                'category': ['categoria', 'category', 'cat'],
                'date': ['data', 'date', 'data_recebimento', 'received_at'],
                'source': ['fonte', 'source', 'origem']
            }
            
            # Encontrar colunas correspondentes
            found_columns = {}
            for field, possible_names in column_mapping.items():
                for col in df.columns:
                    if col.lower() in [name.lower() for name in possible_names]:
                        found_columns[field] = col
                        break
            
            # Validar colunas obrigatórias
            required_fields = ['description', 'amount', 'date']
            missing_fields = [field for field in required_fields if field not in found_columns]
            
            if missing_fields:
                return JsonResponse({
                    'error': f'Colunas obrigatórias não encontradas: {missing_fields}',
                    'available_columns': list(df.columns)
                }, status=400)
            
            # Processar dados
            categories_created = 0
            incomes_created = 0
            errors = []
            
            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        # Extrair dados
                        description = str(row[found_columns['description']]).strip()
                        amount = float(row[found_columns['amount']])
                        
                        # Processar data
                        if pd.isna(row[found_columns['date']]):
                            errors.append(f'Linha {index + 2}: Data inválida')
                            continue
                        
                        try:
                            if isinstance(row[found_columns['date']], str):
                                date = datetime.strptime(str(row[found_columns['date']]), '%Y-%m-%d').date()
                            else:
                                date = row[found_columns['date']].date()
                        except:
                            errors.append(f'Linha {index + 2}: Formato de data inválido')
                            continue
                        
                        # Processar categoria
                        category = None
                        if 'category' in found_columns:
                            category_name = str(row[found_columns['category']]).strip()
                            if category_name and category_name.lower() != 'nan':
                                category, created = Category.objects.get_or_create(
                                    name=category_name,
                                    type='income',
                                    user_id=1  # TODO: Usar usuário autenticado
                                )
                                if created:
                                    categories_created += 1
                        
                        # Criar receita
                        income = Income.objects.create(
                            description=description,
                            amount=Decimal(str(amount)),
                            category=category,
                            received_at=date,
                            user_id=1  # TODO: Usar usuário autenticado
                        )
                        incomes_created += 1
                            
                    except Exception as e:
                        errors.append(f'Linha {index + 2}: {str(e)}')
                        continue
            
            # Limpar arquivo temporário
            os.unlink(tmp_file_path)
            
            return JsonResponse({
                'message': 'Importação concluída com sucesso',
                'categories_created': categories_created,
                'incomes_created': incomes_created,
                'errors': errors,
                'total_processed': len(df)
            })
            
        except Exception as e:
            # Limpar arquivo temporário em caso de erro
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
            raise e
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Endpoints para KPIs e Relatórios de Receitas
@csrf_exempt
@require_http_methods(["GET"])
def income_kpis(request):
    """KPIs de receitas"""
    try:
        from django.db.models import Sum, Avg, Count
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        # Período atual (mês atual)
        now = timezone.now()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_month_end = (current_month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Mês anterior
        last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        last_month_end = current_month_start - timedelta(days=1)
        
        # Receita total do mês atual
        current_month_income = Income.objects.filter(
            received_at__gte=current_month_start,
            received_at__lte=current_month_end
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Receita total do mês anterior
        last_month_income = Income.objects.filter(
            received_at__gte=last_month_start,
            received_at__lte=last_month_end
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Receita média por mês (últimos 6 meses)
        six_months_ago = current_month_start - timedelta(days=180)
        avg_monthly_income = Income.objects.filter(
            received_at__gte=six_months_ago
        ).aggregate(avg=Avg('amount'))['avg'] or Decimal('0.00')
        
        # Crescimento percentual
        growth_percentage = 0
        if last_month_income > 0:
            growth_percentage = ((current_month_income - last_month_income) / last_month_income) * 100
        
        # Total de receitas do mês
        income_count = Income.objects.filter(
            received_at__gte=current_month_start,
            received_at__lte=current_month_end
        ).count()
        
        return JsonResponse({
            'current_month_total': float(current_month_income),
            'last_month_total': float(last_month_income),
            'avg_monthly_income': float(avg_monthly_income),
            'growth_percentage': round(growth_percentage, 2),
            'income_count': income_count,
            'period': {
                'current_month': current_month_start.strftime('%Y-%m'),
                'last_month': last_month_start.strftime('%Y-%m')
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def income_by_category(request):
    """Receita por categoria"""
    try:
        from django.db.models import Sum, Count
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        # Parâmetros de filtro
        month = request.GET.get('month')
        year = request.GET.get('year')
        
        if month and year:
            start_date = datetime(int(year), int(month), 1).date()
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        else:
            # Mês atual
            now = timezone.now()
            start_date = now.replace(day=1).date()
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Buscar receitas por categoria
        category_incomes = Income.objects.filter(
            received_at__gte=start_date,
            received_at__lte=end_date
        ).values('category__name').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        # Formatar dados
        result = []
        for item in category_incomes:
            result.append({
                'category': item['category__name'] or 'Sem categoria',
                'total': float(item['total']),
                'count': item['count']
            })
        
        return JsonResponse({
            'data': result,
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def income_evolution(request):
    """Evolução mensal da receita"""
    try:
        from django.db.models import Sum, Count
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        # Parâmetros
        months = int(request.GET.get('months', 6))
        
        # Calcular datas
        now = timezone.now()
        end_date = now.replace(day=1) - timedelta(days=1)
        start_date = (end_date - timedelta(days=months * 30)).replace(day=1)
        
        # Buscar dados mensais
        monthly_data = []
        current_date = start_date
        
        while current_date <= end_date:
            month_start = current_date.replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            total = Income.objects.filter(
                received_at__gte=month_start,
                received_at__lte=month_end
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            
            monthly_data.append({
                'month': current_date.strftime('%Y-%m'),
                'total': float(total),
                'count': Income.objects.filter(
                    received_at__gte=month_start,
                    received_at__lte=month_end
                ).count()
            })
            
            current_date = (month_start + timedelta(days=32)).replace(day=1)
        
        return JsonResponse({
            'data': monthly_data,
            'period': {
                'start_date': start_date.strftime('%Y-%m'),
                'end_date': end_date.strftime('%Y-%m'),
                'months': months
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def top_income_sources(request):
    """Top fontes de receita"""
    try:
        from django.db.models import Sum, Count
        from django.utils import timezone
        from datetime import datetime, timedelta
        
        # Parâmetros
        limit = int(request.GET.get('limit', 10))
        months = int(request.GET.get('months', 3))
        
        # Calcular período
        now = timezone.now()
        start_date = (now - timedelta(days=months * 30)).date()
        
        # Buscar top fontes por categoria
        top_sources = Income.objects.filter(
            received_at__gte=start_date
        ).values('category__name').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')[:limit]
        
        # Formatar dados
        result = []
        for item in top_sources:
            result.append({
                'category': item['category__name'] or 'Sem categoria',
                'total': float(item['total']),
                'count': item['count'],
                'percentage': 0  # Será calculado abaixo
            })
        
        # Calcular percentuais
        total_amount = sum(item['total'] for item in result)
        if total_amount > 0:
            for item in result:
                item['percentage'] = round((item['total'] / total_amount) * 100, 2)
        
        return JsonResponse({
            'data': result,
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': now.date().strftime('%Y-%m-%d'),
                'months': months
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def expense_category_create(request):
    """Criar nova categoria de despesa"""
    try:
        data = json.loads(request.body)
        required_fields = ['name']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Campo obrigatório: {field}'}, status=400)
        existing_category = Category.objects.filter(
            name=data['name'], 
            type='expense'
        ).first()
        if existing_category:
            return JsonResponse({'error': 'Já existe uma categoria com este nome'}, status=400)
        category = Category.objects.create(
            name=data['name'],
            type='expense',
            user_id=1  # TODO: Usar usuário autenticado
        )
        return JsonResponse({
            'id': category.id,
            'name': category.name,
            'type': category.type
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def expense_category_detail(request, category_id):
    """Buscar categoria de despesa específica"""
    try:
        category = Category.objects.filter(id=category_id, type='expense').first()
        if not category:
            return JsonResponse({'error': 'Categoria não encontrada'}, status=404)
        return JsonResponse({
            'id': category.id,
            'name': category.name,
            'type': category.type
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def expense_category_update(request, category_id):
    """Atualizar categoria de despesa"""
    try:
        data = json.loads(request.body)
        category = Category.objects.filter(id=category_id, type='expense').first()
        if not category:
            return JsonResponse({'error': 'Categoria não encontrada'}, status=404)
        if 'name' in data:
            existing_category = Category.objects.filter(
                name=data['name'], 
                type='expense'
            ).exclude(id=category_id).first()
            if existing_category:
                return JsonResponse({'error': 'Já existe uma categoria com este nome'}, status=400)
            category.name = data['name']
            category.save()
        return JsonResponse({
            'id': category.id,
            'name': category.name,
            'type': category.type
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def expense_category_delete(request, category_id):
    """Deletar categoria de despesa com lógica de migração"""
    try:
        category = Category.objects.filter(id=category_id, type='expense').first()
        if not category:
            return JsonResponse({'error': 'Categoria não encontrada'}, status=404)
        from core.models import Expense
        expenses_count = Expense.objects.filter(category=category).count()
        if expenses_count > 0:
            return JsonResponse({
                'message': f'Esta categoria possui {expenses_count} despesa(s)',
                'expenses_count': expenses_count,
                'category_id': category_id,
                'category_name': category.name,
                'requires_action': True
            }, status=409)
        category.delete()
        return JsonResponse({'message': 'Categoria deletada com sucesso'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def expense_category_migrate(request, category_id):
    """Migrar despesas de uma categoria para outra antes de deletar"""
    try:
        data = json.loads(request.body)
        if 'target_category_id' not in data:
            return JsonResponse({'error': 'ID da categoria de destino é obrigatório'}, status=400)
        source_category = Category.objects.filter(id=category_id, type='expense').first()
        target_category = Category.objects.filter(id=data['target_category_id'], type='expense').first()
        if not source_category:
            return JsonResponse({'error': 'Categoria de origem não encontrada'}, status=404)
        if not target_category:
            return JsonResponse({'error': 'Categoria de destino não encontrada'}, status=404)
        from core.models import Expense
        migrated_count = Expense.objects.filter(category=source_category).update(category=target_category)
        source_category.delete()
        return JsonResponse({
            'message': f'{migrated_count} despesa(s) migrada(s) com sucesso',
            'migrated_count': migrated_count
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def expense_category_delete_with_expenses(request, category_id):
    """Deletar categoria e todas as suas despesas"""
    try:
        category = Category.objects.filter(id=category_id, type='expense').first()
        if not category:
            return JsonResponse({'error': 'Categoria não encontrada'}, status=404)
        from core.models import Expense
        deleted_expenses = Expense.objects.filter(category=category).delete()
        category.delete()
        return JsonResponse({
            'message': f'Categoria e {deleted_expenses[0]} despesa(s) deletada(s) com sucesso',
            'deleted_expenses_count': deleted_expenses[0]
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def import_expense_excel_api(request):
    """Importar despesas e categorias via Excel via API"""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'Arquivo não fornecido'}, status=400)
        uploaded_file = request.FILES['file']
        # Verificar extensão do arquivo
        if not uploaded_file.name.endswith(('.xlsx', '.xls')):
            return JsonResponse({'error': 'Arquivo deve ser Excel (.xlsx ou .xls)'}, status=400)
        import tempfile
        import os
        import pandas as pd
        from django.core.files.storage import default_storage
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            for chunk in uploaded_file.chunks():
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name
        try:
            df = pd.read_excel(tmp_file_path)
            column_mapping = {
                'description': ['descrição', 'description', 'desc', 'nome'],
                'amount': ['valor', 'amount', 'montante', 'preço'],
                'category': ['categoria', 'category', 'cat'],
                'date': ['data', 'date', 'data_pagamento', 'paid_at'],
                'payment_method': ['forma_pagamento', 'payment_method', 'metodo', 'método']
            }
            found_columns = {}
            for field, possible_names in column_mapping.items():
                for col in df.columns:
                    if col.lower() in [name.lower() for name in possible_names]:
                        found_columns[field] = col
                        break
            required_fields = ['description', 'amount', 'date']
            missing_fields = [field for field in required_fields if field not in found_columns]
            if missing_fields:
                return JsonResponse({
                    'error': f'Colunas obrigatórias não encontradas: {missing_fields}',
                    'available_columns': list(df.columns)
                }, status=400)
            categories_created = 0
            expenses_created = 0
            errors = []
            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        description = str(row[found_columns['description']]).strip()
                        amount = float(row[found_columns['amount']])
                        if pd.isna(row[found_columns['date']]):
                            errors.append(f'Linha {index + 2}: Data inválida')
                            continue
                        try:
                            if isinstance(row[found_columns['date']], str):
                                date = datetime.strptime(str(row[found_columns['date']]), '%Y-%m-%d').date()
                            else:
                                date = row[found_columns['date']].date()
                        except:
                            errors.append(f'Linha {index + 2}: Formato de data inválido')
                            continue
                        category = None
                        if 'category' in found_columns:
                            category_name = str(row[found_columns['category']]).strip()
                            if category_name and category_name.lower() != 'nan':
                                category, created = Category.objects.get_or_create(
                                    name=category_name,
                                    type='expense',
                                    user_id=1  # TODO: Usar usuário autenticado
                                )
                                if created:
                                    categories_created += 1
                        payment_method = None
                        if 'payment_method' in found_columns:
                            payment_method = str(row[found_columns['payment_method']]).strip()
                            if payment_method.lower() == 'nan':
                                payment_method = None
                        expense = Expense.objects.create(
                            description=description,
                            amount=Decimal(str(amount)),
                            category=category,
                            paid_at=date,
                            payment_method=payment_method,
                            user_id=1  # TODO: Usar usuário autenticado
                        )
                        expenses_created += 1
                    except Exception as e:
                        errors.append(f'Linha {index + 2}: {str(e)}')
                        continue
            os.unlink(tmp_file_path)
            return JsonResponse({
                'message': 'Importação concluída com sucesso',
                'categories_created': categories_created,
                'expenses_created': expenses_created,
                'errors': errors,
                'total_processed': len(df)
            })
        except Exception as e:
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
            raise e
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def expense_kpis(request):
    """KPIs de despesas"""
    try:
        from django.db.models import Sum, Avg, Count
        from django.utils import timezone
        from datetime import datetime, timedelta
        from core.models import Expense
        now = timezone.now()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_month_end = (current_month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
        last_month_end = current_month_start - timedelta(days=1)
        current_month_expense = Expense.objects.filter(
            paid_at__gte=current_month_start,
            paid_at__lte=current_month_end
        ).aggregate(total=Sum('amount'))['total'] or 0
        last_month_expense = Expense.objects.filter(
            paid_at__gte=last_month_start,
            paid_at__lte=last_month_end
        ).aggregate(total=Sum('amount'))['total'] or 0
        six_months_ago = current_month_start - timedelta(days=180)
        avg_monthly_expense = Expense.objects.filter(
            paid_at__gte=six_months_ago
        ).aggregate(avg=Avg('amount'))['avg'] or 0
        growth_percentage = 0
        if last_month_expense > 0:
            growth_percentage = ((current_month_expense - last_month_expense) / last_month_expense) * 100
        expense_count = Expense.objects.filter(
            paid_at__gte=current_month_start,
            paid_at__lte=current_month_end
        ).count()
        return JsonResponse({
            'current_month_total': float(current_month_expense),
            'last_month_total': float(last_month_expense),
            'avg_monthly_expense': float(avg_monthly_expense),
            'growth_percentage': round(growth_percentage, 2),
            'expense_count': expense_count,
            'period': {
                'current_month': current_month_start.strftime('%Y-%m'),
                'last_month': last_month_start.strftime('%Y-%m')
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def expense_by_category(request):
    """Despesas por categoria"""
    try:
        from django.db.models import Sum, Count
        from django.utils import timezone
        from datetime import datetime, timedelta
        from core.models import Expense
        month = request.GET.get('month')
        year = request.GET.get('year')
        if month and year:
            start_date = datetime(int(year), int(month), 1).date()
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        else:
            now = timezone.now()
            start_date = now.replace(day=1).date()
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        category_expenses = Expense.objects.filter(
            paid_at__gte=start_date,
            paid_at__lte=end_date
        ).values('category__name').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        result = []
        for item in category_expenses:
            result.append({
                'category': item['category__name'] or 'Sem categoria',
                'total': float(item['total']),
                'count': item['count']
            })
        return JsonResponse({
            'data': result,
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def expense_evolution(request):
    """Evolução mensal das despesas"""
    try:
        from django.db.models import Sum, Count
        from django.utils import timezone
        from datetime import datetime, timedelta
        from core.models import Expense
        months = int(request.GET.get('months', 6))
        now = timezone.now()
        end_date = now.replace(day=1) - timedelta(days=1)
        start_date = (end_date - timedelta(days=months * 30)).replace(day=1)
        monthly_data = []
        current_date = start_date
        while current_date <= end_date:
            month_start = current_date.replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            total = Expense.objects.filter(
                paid_at__gte=month_start,
                paid_at__lte=month_end
            ).aggregate(total=Sum('amount'))['total'] or 0
            monthly_data.append({
                'month': current_date.strftime('%Y-%m'),
                'total': float(total),
                'count': Expense.objects.filter(
                    paid_at__gte=month_start,
                    paid_at__lte=month_end
                ).count()
            })
            current_date = (month_start + timedelta(days=32)).replace(day=1)
        return JsonResponse({
            'data': monthly_data,
            'period': {
                'start_date': start_date.strftime('%Y-%m'),
                'end_date': end_date.strftime('%Y-%m'),
                'months': months
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def top_expense_categories(request):
    """Top categorias de despesas"""
    try:
        from django.db.models import Sum, Count
        from django.utils import timezone
        from datetime import datetime, timedelta
        from core.models import Expense
        limit = int(request.GET.get('limit', 10))
        months = int(request.GET.get('months', 3))
        now = timezone.now()
        start_date = (now - timedelta(days=months * 30)).date()
        top_categories = Expense.objects.filter(
            paid_at__gte=start_date
        ).values('category__name').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')[:limit]
        result = []
        for item in top_categories:
            result.append({
                'category': item['category__name'] or 'Sem categoria',
                'total': float(item['total']),
                'count': item['count'],
                'percentage': 0
            })
        total_amount = sum(item['total'] for item in result)
        if total_amount > 0:
            for item in result:
                item['percentage'] = round((item['total'] / total_amount) * 100, 2)
        return JsonResponse({
            'data': result,
            'period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': now.date().strftime('%Y-%m-%d'),
                'months': months
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ==================== VENDAS ====================

@csrf_exempt
@require_http_methods(["GET"])
def sales_list(request):
    """Listar todas as vendas com filtros opcionais"""
    try:
        # Parâmetros de filtro
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        produto_servico = request.GET.get('produto_servico')
        forma_recebimento = request.GET.get('forma_recebimento')
        
        # Query base
        vendas = Venda.objects.all()
        
        # Aplicar filtros
        if start_date:
            vendas = vendas.filter(data__gte=start_date)
        if end_date:
            vendas = vendas.filter(data__lte=end_date)
        if produto_servico:
            vendas = vendas.filter(produto_servico__icontains=produto_servico)
        if forma_recebimento:
            vendas = vendas.filter(forma_recebimento=forma_recebimento)
        
        # Ordenar por data (mais recente primeiro)
        vendas = vendas.order_by('-data')
        
        # Serializar dados
        sales_data = []
        for venda in vendas:
            sales_data.append({
                'id': venda.id,
                'data': venda.data.strftime('%Y-%m-%d'),
                'produto_servico': venda.produto_servico,
                'valor_venda': float(venda.valor_venda),
                'custo': float(venda.custo),
                'lucro_bruto': float(venda.lucro_bruto),
                'forma_recebimento': venda.forma_recebimento,
                'observacoes': venda.observacoes or '',
            })
        
        return JsonResponse({
            'success': True,
            'data': sales_data,
            'total': len(sales_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def sale_create(request):
    """Criar nova venda"""
    try:
        data = json.loads(request.body)
        
        # Validações básicas
        required_fields = ['data', 'produto_servico', 'valor_venda', 'custo', 'forma_recebimento']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({
                    'success': False,
                    'error': f'Campo obrigatório: {field}'
                }, status=400)
        
        # Validar valores numéricos
        try:
            valor_venda = Decimal(str(data['valor_venda']))
            custo = Decimal(str(data['custo']))
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'error': 'Valor da venda e custo devem ser números válidos'
            }, status=400)
        
        # Validar data
        try:
            data_venda = datetime.strptime(data['data'], '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': 'Data deve estar no formato YYYY-MM-DD'
            }, status=400)
        
        # Criar venda
        venda = Venda.objects.create(
            data=data_venda,
            produto_servico=data['produto_servico'],
            valor_venda=valor_venda,
            custo=custo,
            forma_recebimento=data['forma_recebimento'],
            observacoes=data.get('observacoes', '')
        )
        
        return JsonResponse({
            'success': True,
            'data': {
                'id': venda.id,
                'data': venda.data.strftime('%Y-%m-%d'),
                'produto_servico': venda.produto_servico,
                'valor_venda': float(venda.valor_venda),
                'custo': float(venda.custo),
                'lucro_bruto': float(venda.lucro_bruto),
                'forma_recebimento': venda.forma_recebimento,
                'observacoes': venda.observacoes or '',
            },
            'message': 'Venda criada com sucesso'
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def sale_detail(request, sale_id):
    """Obter detalhes de uma venda específica"""
    try:
        venda = Venda.objects.get(id=sale_id)
        
        return JsonResponse({
            'success': True,
            'data': {
                'id': venda.id,
                'data': venda.data.strftime('%Y-%m-%d'),
                'produto_servico': venda.produto_servico,
                'valor_venda': float(venda.valor_venda),
                'custo': float(venda.custo),
                'lucro_bruto': float(venda.lucro_bruto),
                'forma_recebimento': venda.forma_recebimento,
                'observacoes': venda.observacoes or '',
            }
        })
        
    except Venda.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Venda não encontrada'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def sale_update(request, sale_id):
    """Atualizar uma venda existente"""
    try:
        venda = Venda.objects.get(id=sale_id)
        data = json.loads(request.body)
        
        # Atualizar campos se fornecidos
        if 'data' in data:
            try:
                venda.data = datetime.strptime(data['data'], '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': 'Data deve estar no formato YYYY-MM-DD'
                }, status=400)
        
        if 'produto_servico' in data:
            venda.produto_servico = data['produto_servico']
        
        if 'valor_venda' in data:
            try:
                venda.valor_venda = Decimal(str(data['valor_venda']))
            except (ValueError, TypeError):
                return JsonResponse({
                    'success': False,
                    'error': 'Valor da venda deve ser um número válido'
                }, status=400)
        
        if 'custo' in data:
            try:
                venda.custo = Decimal(str(data['custo']))
            except (ValueError, TypeError):
                return JsonResponse({
                    'success': False,
                    'error': 'Custo deve ser um número válido'
                }, status=400)
        
        if 'forma_recebimento' in data:
            venda.forma_recebimento = data['forma_recebimento']
        
        if 'observacoes' in data:
            venda.observacoes = data['observacoes']
        
        venda.save()
        
        return JsonResponse({
            'success': True,
            'data': {
                'id': venda.id,
                'data': venda.data.strftime('%Y-%m-%d'),
                'produto_servico': venda.produto_servico,
                'valor_venda': float(venda.valor_venda),
                'custo': float(venda.custo),
                'lucro_bruto': float(venda.lucro_bruto),
                'forma_recebimento': venda.forma_recebimento,
                'observacoes': venda.observacoes or '',
            },
            'message': 'Venda atualizada com sucesso'
        })
        
    except Venda.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Venda não encontrada'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def sale_delete(request, sale_id):
    """Excluir uma venda"""
    try:
        venda = Venda.objects.get(id=sale_id)
        venda.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Venda excluída com sucesso'
        })
        
    except Venda.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Venda não encontrada'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

# ==================== KPIs E RELATÓRIOS DE VENDAS ====================

@csrf_exempt
@require_http_methods(["GET"])
def sales_kpis(request):
    """KPIs principais de vendas"""
    try:
        # Parâmetros de filtro
        month = request.GET.get('month')
        year = request.GET.get('year')
        
        # Se não especificado, usar mês atual
        if not month or not year:
            today = timezone.now().date()
            month = today.month
            year = today.year
        
        # Filtrar vendas do período
        vendas = Venda.objects.filter(
            data__year=year,
            data__month=month
        )
        
        # Calcular KPIs
        total_vendas = vendas.aggregate(
            total=Sum('valor_venda')
        )['total'] or 0
        
        total_custos = vendas.aggregate(
            total=Sum('custo')
        )['total'] or 0
        
        total_lucro = total_vendas - total_custos
        
        quantidade_vendas = vendas.count()
        
        ticket_medio = total_vendas / quantidade_vendas if quantidade_vendas > 0 else 0
        
        # Margem de lucro
        margem_lucro = (total_lucro / total_vendas * 100) if total_vendas > 0 else 0
        
        # Mês anterior para comparação
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year
        
        vendas_anterior = Venda.objects.filter(
            data__year=prev_year,
            data__month=prev_month
        ).aggregate(
            total=Sum('valor_venda')
        )['total'] or 0
        
        # Crescimento percentual
        crescimento = 0
        if vendas_anterior > 0:
            crescimento = ((total_vendas - vendas_anterior) / vendas_anterior) * 100
        
        return JsonResponse({
            'success': True,
            'data': {
                'total_vendas': float(total_vendas),
                'total_custos': float(total_custos),
                'total_lucro': float(total_lucro),
                'quantidade_vendas': quantidade_vendas,
                'ticket_medio': float(ticket_medio),
                'margem_lucro': float(margem_lucro),
                'crescimento_percentual': float(crescimento),
                'periodo': f"{year}-{month:02d}"
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def sales_by_product(request):
    """Vendas por produto/serviço"""
    try:
        # Parâmetros de filtro
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        limit = int(request.GET.get('limit', 10))
        
        # Query base
        vendas = Venda.objects.all()
        
        # Aplicar filtros de data
        if start_date:
            vendas = vendas.filter(data__gte=start_date)
        if end_date:
            vendas = vendas.filter(data__lte=end_date)
        
        # Agrupar por produto/serviço
        produtos_data = vendas.values('produto_servico').annotate(
            total_vendas=Sum('valor_venda'),
            total_custos=Sum('custo'),
            quantidade=Count('id')
        ).annotate(
            lucro_bruto=F('total_vendas') - F('total_custos')
        ).order_by('-total_vendas')[:limit]
        
        # Calcular totais para percentuais
        total_geral = vendas.aggregate(
            total=Sum('valor_venda')
        )['total'] or 0
        
        # Formatar dados
        produtos = []
        for produto in produtos_data:
            percentual = (produto['total_vendas'] / total_geral * 100) if total_geral > 0 else 0
            produtos.append({
                'produto_servico': produto['produto_servico'],
                'total_vendas': float(produto['total_vendas']),
                'total_custos': float(produto['total_custos']),
                'lucro_bruto': float(produto['lucro_bruto']),
                'quantidade': produto['quantidade'],
                'percentual': float(percentual)
            })
        
        return JsonResponse({
            'success': True,
            'data': produtos,
            'total_geral': float(total_geral)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def sales_evolution(request):
    """Evolução mensal das vendas"""
    try:
        # Parâmetros
        months = int(request.GET.get('months', 6))
        
        # Calcular data de início
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=months * 30)
        
        # Buscar todas as vendas do período
        vendas = Venda.objects.filter(
            data__gte=start_date,
            data__lte=end_date
        ).order_by('data')
        
        # Agrupar por mês usando Python
        vendas_por_mes = {}
        for venda in vendas:
            periodo = f"{venda.data.year}-{venda.data.month:02d}"
            if periodo not in vendas_por_mes:
                vendas_por_mes[periodo] = {
                    'total_vendas': 0,
                    'total_custos': 0,
                    'quantidade': 0
                }
            
            vendas_por_mes[periodo]['total_vendas'] += float(venda.valor_venda)
            vendas_por_mes[periodo]['total_custos'] += float(venda.custo)
            vendas_por_mes[periodo]['quantidade'] += 1
        
        # Formatar dados
        evolution = []
        for periodo in sorted(vendas_por_mes.keys()):
            dados = vendas_por_mes[periodo]
            evolution.append({
                'periodo': periodo,
                'total_vendas': dados['total_vendas'],
                'total_custos': dados['total_custos'],
                'lucro_bruto': dados['total_vendas'] - dados['total_custos'],
                'quantidade': dados['quantidade']
            })
        
        return JsonResponse({
            'success': True,
            'data': evolution
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def top_sales_products(request):
    """Top produtos/serviços por lucro"""
    try:
        # Parâmetros
        limit = int(request.GET.get('limit', 5))
        months = int(request.GET.get('months', 6))
        
        # Calcular data de início
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=months * 30)
        
        # Buscar top produtos por lucro
        top_produtos = Venda.objects.filter(
            data__gte=start_date,
            data__lte=end_date
        ).values('produto_servico').annotate(
            total_vendas=Sum('valor_venda'),
            total_custos=Sum('custo'),
            quantidade=Count('id')
        ).annotate(
            lucro_bruto=F('total_vendas') - F('total_custos')
        ).order_by('-lucro_bruto')[:limit]
        
        # Formatar dados
        produtos = []
        for produto in top_produtos:
            produtos.append({
                'produto_servico': produto['produto_servico'],
                'total_vendas': float(produto['total_vendas']),
                'total_custos': float(produto['total_custos']),
                'lucro_bruto': float(produto['lucro_bruto']),
                'quantidade': produto['quantidade'],
                'margem_lucro': float((produto['lucro_bruto'] / produto['total_vendas'] * 100) if produto['total_vendas'] > 0 else 0)
            })
        
        return JsonResponse({
            'success': True,
            'data': produtos
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
