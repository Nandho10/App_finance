from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from core.models import User, Category, Income, Expense

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste para o dashboard do MVP'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Populando banco de dados com dados de teste...'))
        # Criar usuário de teste
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Usuário',
                'last_name': 'Teste'
            }
        )
        # Categorias
        categories_data = [
            {'name': 'Salário', 'type': 'income'},
            {'name': 'Freelance', 'type': 'income'},
            {'name': 'Investimentos', 'type': 'income'},
            {'name': 'Bônus', 'type': 'income'},
            {'name': 'Alimentação', 'type': 'expense'},
            {'name': 'Transporte', 'type': 'expense'},
            {'name': 'Moradia', 'type': 'expense'},
            {'name': 'Lazer', 'type': 'expense'},
            {'name': 'Saúde', 'type': 'expense'},
            {'name': 'Educação', 'type': 'expense'},
        ]
        categories = {}
        for cat_data in categories_data:
            category, _ = Category.objects.get_or_create(
                user=user,
                name=cat_data['name'],
                type=cat_data['type']
            )
            categories[cat_data['name']] = category
        # Receitas
        today = timezone.now().date()
        incomes_data = [
            {'description': 'Salário Janeiro', 'amount': Decimal('8500.00'), 'category': 'Salário', 'received_at': today.replace(day=15)},
            {'description': 'Freelance Projeto A', 'amount': Decimal('1200.00'), 'category': 'Freelance', 'received_at': today.replace(day=14)},
            {'description': 'Dividendos', 'amount': Decimal('500.00'), 'category': 'Investimentos', 'received_at': today.replace(day=13)},
            {'description': 'Bônus Trimestral', 'amount': Decimal('2000.00'), 'category': 'Bônus', 'received_at': today.replace(day=12)},
        ]
        for income_data in incomes_data:
            Income.objects.get_or_create(
                user=user,
                description=income_data['description'],
                amount=income_data['amount'],
                category=categories[income_data['category']],
                received_at=income_data['received_at']
            )
        # Despesas
        expenses_data = [
            {'description': 'Supermercado', 'amount': Decimal('450.00'), 'category': 'Alimentação', 'paid_at': today.replace(day=14), 'payment_method': 'credit_card'},
            {'description': 'Combustível', 'amount': Decimal('200.00'), 'category': 'Transporte', 'paid_at': today.replace(day=13), 'payment_method': 'cash'},
            {'description': 'Cinema', 'amount': Decimal('80.00'), 'category': 'Lazer', 'paid_at': today.replace(day=12), 'payment_method': 'pix'},
            {'description': 'Conta de Luz', 'amount': Decimal('150.00'), 'category': 'Moradia', 'paid_at': today.replace(day=11), 'payment_method': 'transfer'},
            {'description': 'Farmácia', 'amount': Decimal('120.00'), 'category': 'Saúde', 'paid_at': today.replace(day=10), 'payment_method': 'credit_card'},
        ]
        for expense_data in expenses_data:
            Expense.objects.get_or_create(
                user=user,
                description=expense_data['description'],
                amount=expense_data['amount'],
                category=categories[expense_data['category']],
                paid_at=expense_data['paid_at'],
                payment_method=expense_data['payment_method']
            )
        self.stdout.write(self.style.SUCCESS('Dados de teste criados com sucesso!'))
        self.stdout.write('Acesse http://localhost:3000 para ver o dashboard')
        self.stdout.write('Acesse http://localhost:8000/api/dashboard/ para ver a API') 