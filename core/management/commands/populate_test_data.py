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
            {'description': 'Salário Janeiro', 'amount': Decimal('8500.00'), 'category': 'Salário', 'received_at': today.replace(day=15), 'account': 'Conta Principal'},
            {'description': 'Freelance Projeto A', 'amount': Decimal('1200.00'), 'category': 'Freelance', 'received_at': today.replace(day=14), 'account': 'Conta Freelance'},
            {'description': 'Dividendos', 'amount': Decimal('500.00'), 'category': 'Investimentos', 'received_at': today.replace(day=13), 'account': 'Conta Investimentos'},
            {'description': 'Bônus Trimestral', 'amount': Decimal('2000.00'), 'category': 'Bônus', 'received_at': today.replace(day=12), 'account': 'Conta Principal'},
        ]
        for income_data in incomes_data:
            Income.objects.get_or_create(
                user=user,
                description=income_data['description'],
                amount=income_data['amount'],
                category=categories[income_data['category']],
                received_at=income_data['received_at'],
                account=income_data['account']
            )
        # Despesas
        expenses_data = [
            {'description': 'Supermercado', 'amount': Decimal('450.00'), 'category': 'Alimentação', 'paid_at': today.replace(day=14), 'payment_method': 'credit_card', 'favored': 'Supermercado ABC'},
            {'description': 'Combustível', 'amount': Decimal('200.00'), 'category': 'Transporte', 'paid_at': today.replace(day=13), 'payment_method': 'cash', 'favored': 'Posto Petrobras'},
            {'description': 'Cinema', 'amount': Decimal('80.00'), 'category': 'Lazer', 'paid_at': today.replace(day=12), 'payment_method': 'pix', 'favored': 'Cinema Shopping'},
            {'description': 'Conta de Luz', 'amount': Decimal('150.00'), 'category': 'Moradia', 'paid_at': today.replace(day=11), 'payment_method': 'transfer', 'favored': 'Companhia de Energia'},
            {'description': 'Farmácia', 'amount': Decimal('120.00'), 'category': 'Saúde', 'paid_at': today.replace(day=10), 'payment_method': 'credit_card', 'favored': 'Farmácia Popular'},
        ]
        for expense_data in expenses_data:
            Expense.objects.get_or_create(
                user=user,
                description=expense_data['description'],
                amount=expense_data['amount'],
                category=categories[expense_data['category']],
                paid_at=expense_data['paid_at'],
                payment_method=expense_data['payment_method'],
                favored=expense_data['favored']
            )
        self.stdout.write(self.style.SUCCESS('Dados de teste criados com sucesso!'))
        self.stdout.write('Acesse http://localhost:3000 para ver o dashboard')
        self.stdout.write('Acesse http://localhost:8000/api/dashboard/ para ver a API') 