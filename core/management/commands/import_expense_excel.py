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
    help = 'Importar despesas e categorias de um arquivo Excel'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Caminho para o arquivo Excel'
        )
        parser.add_argument(
            '--user-id',
            type=int,
            default=1,
            help='ID do usuário (padrão: 1)'
        )
        parser.add_argument(
            '--sheet-name',
            type=str,
            default=0,
            help='Nome da planilha (padrão: primeira planilha)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Executar sem salvar no banco (apenas simular)'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        user_id = options['user_id']
        sheet_name = options['sheet_name']
        dry_run = options['dry_run']

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'Arquivo não encontrado: {file_path}')
            )
            return

        try:
            # Ler arquivo Excel
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Mostrar colunas disponíveis
            self.stdout.write(
                self.style.SUCCESS(f'Colunas encontradas: {list(df.columns)}')
            )
            
            # Mapeamento padrão de colunas
            column_mapping = {
                'description': ['descrição', 'description', 'desc', 'nome'],
                'amount': ['valor', 'amount', 'montante', 'preço'],
                'category': ['categoria', 'category', 'cat'],
                'date': ['data', 'date', 'data_pagamento', 'paid_at'],
                'payment_method': ['forma_pagamento', 'payment_method', 'metodo', 'método', 'pagamento'],
                'favored': ['favorecido', 'favored', 'para_quem', 'beneficiario', 'beneficiário']
            }
            
            # Encontrar colunas correspondentes
            found_columns = {}
            for field, possible_names in column_mapping.items():
                for col in df.columns:
                    if col.lower() in [name.lower() for name in possible_names]:
                        found_columns[field] = col
                        break
            
            self.stdout.write(
                self.style.SUCCESS(f'Colunas mapeadas: {found_columns}')
            )
            
            # Validar colunas obrigatórias
            required_fields = ['description', 'amount', 'date']
            missing_fields = [field for field in required_fields if field not in found_columns]
            
            if missing_fields:
                self.stdout.write(
                    self.style.ERROR(f'Colunas obrigatórias não encontradas: {missing_fields}')
                )
                return
            
            # Processar dados
            categories_created = 0
            expenses_created = 0
            errors = []
            
            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        # Extrair dados
                        description = str(row[found_columns['description']]).strip()
                        amount = float(row[found_columns['amount']])
                        date_str = str(row[found_columns['date']])
                        
                        # Processar data
                        if pd.isna(row[found_columns['date']]):
                            errors.append(f'Linha {index + 2}: Data inválida')
                            continue
                        
                        try:
                            if isinstance(row[found_columns['date']], str):
                                date = datetime.strptime(date_str, '%Y-%m-%d').date()
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
                                    type='expense',
                                    user_id=user_id
                                )
                                if created:
                                    categories_created += 1
                        
                        # Processar forma de pagamento
                        payment_method = 'cash'  # padrão
                        if 'payment_method' in found_columns:
                            payment_method_raw = str(row[found_columns['payment_method']]).strip().lower()
                            if payment_method_raw and payment_method_raw != 'nan':
                                # Mapear formas de pagamento
                                payment_mapping = {
                                    'dinheiro': 'cash',
                                    'cash': 'cash',
                                    'cartão de crédito': 'credit_card',
                                    'cartao de credito': 'credit_card',
                                    'credit_card': 'credit_card',
                                    'pix': 'pix',
                                    'transferência': 'transfer',
                                    'transferencia': 'transfer',
                                    'transfer': 'transfer'
                                }
                                payment_method = payment_mapping.get(payment_method_raw, 'cash')
                        
                        # Processar favorecido
                        favored = None
                        if 'favored' in found_columns:
                            favored = str(row[found_columns['favored']]).strip()
                            if favored.lower() == 'nan':
                                favored = None
                        
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
                for error in errors:
                    self.stdout.write(f'  - {error}')
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao processar arquivo: {str(e)}')
            ) 