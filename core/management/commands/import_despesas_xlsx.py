import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models.category_models import Category
from core.models.transaction_models import Expense
from core.models.user_models import User
from decimal import Decimal
from datetime import datetime
import os


class Command(BaseCommand):
    help = 'Importar despesas da planilha Despesas.xlsx'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            default=1,
            help='ID do usuário (padrão: 1)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Executar sem salvar no banco (apenas simular)'
        )

    def handle(self, *args, **options):
        file_path = r"E:\Nandho\Financas\App_financeiro\docs\Despesas.xlsx"
        user_id = options['user_id']
        dry_run = options['dry_run']

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'Arquivo não encontrado: {file_path}')
            )
            return

        try:
            # Ler arquivo Excel
            df = pd.read_excel(file_path)
            
            self.stdout.write(
                self.style.SUCCESS(f'Total de linhas encontradas: {len(df)}')
            )
            
            # Mapeamento específico para a planilha
            column_mapping = {
                'paid_at': 'paid_at',
                'category': 'category', 
                'description': 'description',
                'favored': 'favored',
                'account': 'account',
                'payment_method': 'payment_method',
                'amount': 'amount',
                'paid': 'paid',
                'user': 'user'
            }
            
            # Verificar se todas as colunas necessárias existem
            missing_columns = []
            for expected_col in ['paid_at', 'category', 'description', 'amount']:
                if expected_col not in df.columns:
                    missing_columns.append(expected_col)
            
            if missing_columns:
                self.stdout.write(
                    self.style.ERROR(f'Colunas obrigatórias não encontradas: {missing_columns}')
                )
                return
            
            self.stdout.write(
                self.style.SUCCESS('Colunas encontradas e mapeadas corretamente')
            )
            
            # Processar dados
            categories_created = 0
            expenses_created = 0
            errors = []
            
            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        # Extrair dados básicos
                        description = str(row['description']).strip()
                        amount = float(row['amount'])
                        
                        # Processar data
                        if pd.isna(row['paid_at']):
                            errors.append(f'Linha {index + 2}: Data inválida')
                            continue
                        
                        try:
                            if isinstance(row['paid_at'], str):
                                date = datetime.strptime(str(row['paid_at']), '%Y-%m-%d').date()
                            else:
                                date = row['paid_at'].date()
                        except:
                            errors.append(f'Linha {index + 2}: Formato de data inválido')
                            continue
                        
                        # Processar categoria
                        category = None
                        if not pd.isna(row['category']):
                            category_name = str(row['category']).strip()
                            if category_name and category_name.lower() != 'nan':
                                category, created = Category.objects.get_or_create(
                                    name=category_name,
                                    type='expense',
                                    user_id=user_id
                                )
                                if created:
                                    categories_created += 1
                        
                        # Processar favorecido
                        favored = None
                        if not pd.isna(row['favored']):
                            favored = str(row['favored']).strip()
                            if favored.lower() == 'nan':
                                favored = None
                        
                        # Processar forma de pagamento
                        payment_method = 'cash'  # padrão
                        if not pd.isna(row['payment_method']):
                            payment_method_raw = str(row['payment_method']).strip().lower()
                            if payment_method_raw and payment_method_raw != 'nan':
                                # Mapear formas de pagamento específicas da planilha
                                payment_mapping = {
                                    'compra elo debito vista': 'credit_card',
                                    'boleto': 'transfer',
                                    'pix': 'pix',
                                    'dinheiro': 'cash',
                                    'cash': 'cash',
                                    'cartão de crédito': 'credit_card',
                                    'cartao de credito': 'credit_card',
                                    'credit_card': 'credit_card',
                                    'transferência': 'transfer',
                                    'transferencia': 'transfer',
                                    'transfer': 'transfer'
                                }
                                payment_method = payment_mapping.get(payment_method_raw, 'cash')
                        
                        # Verificar se já foi pago
                        if not pd.isna(row['paid']) and str(row['paid']).strip().lower() != 'pago':
                            # Pular despesas não pagas
                            continue
                        
                        if not dry_run:
                            # Criar despesa
                            expense = Expense.objects.create(
                                description=description,
                                amount=Decimal(str(amount)),
                                category=category,
                                favored=favored,
                                paid_at=date,
                                payment_method=payment_method,
                                user_id=user_id
                            )
                            expenses_created += 1
                        else:
                            expenses_created += 1
                            
                    except Exception as e:
                        errors.append(f'Linha {index + 2}: {str(e)}')
                        continue
            
            # Relatório final
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nImportação concluída!\n'
                    f'Categorias criadas: {categories_created}\n'
                    f'Despesas criadas: {expenses_created}\n'
                    f'Erros: {len(errors)}'
                )
            )
            
            if errors:
                self.stdout.write(
                    self.style.WARNING('\nErros encontrados:')
                )
                for error in errors[:10]:  # Mostrar apenas os primeiros 10 erros
                    self.stdout.write(f'  - {error}')
                if len(errors) > 10:
                    self.stdout.write(f'  ... e mais {len(errors) - 10} erros')
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao processar arquivo: {str(e)}')
            ) 