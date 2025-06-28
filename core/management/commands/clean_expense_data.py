from django.core.management.base import BaseCommand
from core.models.category_models import Category
from core.models.transaction_models import Expense

class Command(BaseCommand):
    help = 'Remove todas as despesas e categorias de despesas do banco de dados.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Removendo todas as despesas...'))
        Expense.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Despesas removidas.'))
        self.stdout.write(self.style.WARNING('Removendo todas as categorias de despesas...'))
        Category.objects.filter(type='expense').delete()
        self.stdout.write(self.style.SUCCESS('Categorias de despesas removidas.'))
        self.stdout.write(self.style.SUCCESS('Banco limpo para nova importação de despesas!')) 