#!/usr/bin/env python
import os
import sys
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_app.settings')
django.setup()

from core.models import Expense, User
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta

def test_expenses():
    print("=== TESTE DOS ENDPOINTS DE DESPESAS ===")
    
    # Verificar usuários
    users = User.objects.all()
    print(f"Usuários disponíveis: {users.count()}")
    for user in users:
        print(f"  - ID: {user.id}, Username: {user.username}")
    
    # Testar endpoint de listagem de despesas
    print(f"\n=== TESTE: Listagem de Despesas ===")
    user = User.objects.filter(id=1).first()  # Usar admin onde as despesas foram importadas
    if user:
        expenses = Expense.objects.filter(user=user).order_by('-paid_at')
        print(f"Despesas do usuário {user.username}: {expenses.count()}")
        
        if expenses.exists():
            print("Primeiras 3 despesas:")
            for exp in expenses[:3]:
                print(f"  - {exp.description}: R$ {exp.amount} em {exp.paid_at}")
        else:
            print("Nenhuma despesa encontrada para este usuário")
    else:
        print("Usuário admin não encontrado")
    
    # Testar endpoint de KPIs
    print(f"\n=== TESTE: KPIs de Despesas ===")
    now = timezone.now()
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_month_end = (current_month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    if user:
        current_month_expense = Expense.objects.filter(
            user=user,
            paid_at__gte=current_month_start,
            paid_at__lte=current_month_end
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_expenses = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        
        print(f"Total de despesas (todas): R$ {total_expenses}")
        print(f"Despesas do mês atual: R$ {current_month_expense}")
        
        # Verificar por categoria
        categories = Expense.objects.filter(user=user).values('category__name').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        print(f"\nTop 5 categorias:")
        for cat in categories[:5]:
            print(f"  - {cat['category__name']}: {cat['count']} despesas, R$ {cat['total']}")
    
    # Testar endpoint de despesas por categoria
    print(f"\n=== TESTE: Despesas por Categoria ===")
    if user:
        category_expenses = Expense.objects.filter(
            user=user,
            paid_at__gte=current_month_start,
            paid_at__lte=current_month_end
        ).values('category__name').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        print(f"Despesas por categoria (mês atual):")
        for item in category_expenses:
            print(f"  - {item['category__name']}: R$ {item['total']} ({item['count']} despesas)")

if __name__ == "__main__":
    test_expenses() 