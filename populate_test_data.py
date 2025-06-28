#!/usr/bin/env python
"""
Script para popular o banco de dados com dados de teste para o MVP
Execute com: python manage.py shell < populate_test_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_app.settings')
django.setup()

from core.models import User, Category, Income, Expense
from django.utils import timezone

def create_test_data():
    """Cria dados de teste no banco de dados"""
    
    print("Criando dados de teste...")
    
    # Criar usuário de teste
    user, created = User.objects.get_or_create(
        username='test_user',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Usuário',
            'last_name': 'Teste'
        }
    )
    
    if created:
        print(f"Usuário criado: {user.username}")
    else:
        print(f"Usuário já existe: {user.username}")
    
    # Criar categorias
    categories_data = [
        # Categorias de receita
        {'name': 'Salário', 'type': 'income'},
        {'name': 'Freelance', 'type': 'income'},
        {'name': 'Investimentos', 'type': 'income'},
        {'name': 'Bônus', 'type': 'income'},
        
        # Categorias de despesa
        {'name': 'Alimentação', 'type': 'expense'},
        {'name': 'Transporte', 'type': 'expense'},
        {'name': 'Moradia', 'type': 'expense'},
        {'name': 'Lazer', 'type': 'expense'},
        {'name': 'Saúde', 'type': 'expense'},
        {'name': 'Educação', 'type': 'expense'},
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            user=user,
            name=cat_data['name'],
            type=cat_data['type']
        )
        categories[cat_data['name']] = category
        if created:
            print(f"Categoria criada: {category.name}")
    
    # Criar receitas de teste
    incomes_data = [
        {
            'description': 'Salário Janeiro',
            'amount': Decimal('8500.00'),
            'category': 'Salário',
            'received_at': datetime.now().date().replace(day=15)
        },
        {
            'description': 'Freelance Projeto A',
            'amount': Decimal('1200.00'),
            'category': 'Freelance',
            'received_at': datetime.now().date().replace(day=14)
        },
        {
            'description': 'Dividendos',
            'amount': Decimal('500.00'),
            'category': 'Investimentos',
            'received_at': datetime.now().date().replace(day=13)
        },
        {
            'description': 'Bônus Trimestral',
            'amount': Decimal('2000.00'),
            'category': 'Bônus',
            'received_at': datetime.now().date().replace(day=12)
        },
    ]
    
    for income_data in incomes_data:
        income, created = Income.objects.get_or_create(
            user=user,
            description=income_data['description'],
            amount=income_data['amount'],
            category=categories[income_data['category']],
            received_at=income_data['received_at']
        )
        if created:
            print(f"Receita criada: {income.description} - R$ {income.amount}")
    
    # Criar despesas de teste
    expenses_data = [
        {
            'description': 'Supermercado',
            'amount': Decimal('450.00'),
            'category': 'Alimentação',
            'paid_at': datetime.now().date().replace(day=14),
            'payment_method': 'credit_card'
        },
        {
            'description': 'Combustível',
            'amount': Decimal('200.00'),
            'category': 'Transporte',
            'paid_at': datetime.now().date().replace(day=13),
            'payment_method': 'cash'
        },
        {
            'description': 'Cinema',
            'amount': Decimal('80.00'),
            'category': 'Lazer',
            'paid_at': datetime.now().date().replace(day=12),
            'payment_method': 'pix'
        },
        {
            'description': 'Conta de Luz',
            'amount': Decimal('150.00'),
            'category': 'Moradia',
            'paid_at': datetime.now().date().replace(day=11),
            'payment_method': 'transfer'
        },
        {
            'description': 'Farmácia',
            'amount': Decimal('120.00'),
            'category': 'Saúde',
            'paid_at': datetime.now().date().replace(day=10),
            'payment_method': 'credit_card'
        },
    ]
    
    for expense_data in expenses_data:
        expense, created = Expense.objects.get_or_create(
            user=user,
            description=expense_data['description'],
            amount=expense_data['amount'],
            category=categories[expense_data['category']],
            paid_at=expense_data['paid_at'],
            payment_method=expense_data['payment_method']
        )
        if created:
            print(f"Despesa criada: {expense.description} - R$ {expense.amount}")
    
    print("\nDados de teste criados com sucesso!")
    print(f"Total de receitas: {Income.objects.filter(user=user).count()}")
    print(f"Total de despesas: {Expense.objects.filter(user=user).count()}")
    print(f"Total de categorias: {Category.objects.filter(user=user).count()}")
    
    # Calcular totais
    total_income = Income.objects.filter(user=user).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')
    total_expenses = Expense.objects.filter(user=user).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')
    balance = total_income - total_expenses
    
    print(f"\nResumo financeiro:")
    print(f"Receitas totais: R$ {total_income}")
    print(f"Despesas totais: R$ {total_expenses}")
    print(f"Saldo: R$ {balance}")

if __name__ == '__main__':
    create_test_data() 