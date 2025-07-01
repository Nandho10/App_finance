import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from core.models import Sale
from django.db import transaction
import os

class Command(BaseCommand):
    help = 'Importa vendas a partir de um arquivo Excel.'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, default='docs/vendas.xlsx', help='Caminho do arquivo Excel de vendas')

    def handle(self, *args, **options):
        file_path = options['file']
        if not os.path.exists(file_path):
            raise CommandError(f"Arquivo não encontrado: {file_path}")

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            raise CommandError(f"Erro ao ler o arquivo Excel: {e}")

        expected_columns = ['paid_at', 'product', 'amount', 'payment_method', 'observacoes', 'delivery_date', 'client']
        for col in expected_columns:
            if col not in df.columns:
                raise CommandError(f"Coluna obrigatória ausente: {col}")

        sales = []
        for idx, row in df.iterrows():
            try:
                sale = Sale(
                    paid_at=pd.to_datetime(row['paid_at']).date(),
                    product=str(row['product']),
                    amount=float(row['amount']),
                    custo=0.0,
                    payment_method=str(row['payment_method']),
                    observacoes=str(row['observacoes']) if not pd.isna(row['observacoes']) else '',
                    delivery_date=pd.to_datetime(row['delivery_date']).date() if not pd.isna(row['delivery_date']) else None,
                    client=str(row['client']) if not pd.isna(row['client']) else ''
                )
                sales.append(sale)
            except Exception as e:
                raise CommandError(f"Erro na linha {idx+2}: {e}")

        with transaction.atomic():
            Sale.objects.all().delete()
            Sale.objects.bulk_create(sales)
        self.stdout.write(self.style.SUCCESS(f"Importação concluída: {len(sales)} vendas importadas.")) 