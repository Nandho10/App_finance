from django.db import models
from django.contrib.auth.models import AbstractUser

# Usuário Customizado
class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

# Categorias (Receitas, Despesas, Vendas)
class Category(models.Model):
    TYPE_CHOICES = [
        ('income', 'Receita'),
        ('expense', 'Despesa'),
        ('sale', 'Venda'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

# Receitas
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, limit_choices_to={'type': 'income'}, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    received_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"R$ {self.amount} - {self.received_at}"

# Despesas
class Expense(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Dinheiro'),
        ('credit_card', 'Cartão de Crédito'),
        ('pix', 'PIX'),
        ('transfer', 'Transferência'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, limit_choices_to={'type': 'expense'}, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    paid_at = models.DateField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    is_installment = models.BooleanField(default=False)
    installment_number = models.PositiveIntegerField(null=True, blank=True)
    total_installments = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"R$ {self.amount} - {self.paid_at}"

# Vendas
class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Dinheiro'),
        ('pix', 'PIX'),
        ('transfer', 'Transferência'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_or_service = models.CharField(max_length=255)
    client = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    received_at = models.DateField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venda: {self.product_or_service} - R$ {self.amount}"

# Cartão de Crédito
class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    limit = models.DecimalField(max_digits=12, decimal_places=2)
    closing_day = models.PositiveSmallIntegerField()
    due_day = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

# Transações no Cartão de Crédito
class CreditCardTransaction(models.Model):
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, limit_choices_to={'type': 'expense'}, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    transaction_date = models.DateField()
    is_installment = models.BooleanField(default=False)
    installment_number = models.PositiveIntegerField(null=True, blank=True)
    total_installments = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.description} - R$ {self.amount}"

# Investimentos
class Investment(models.Model):
    INVESTMENT_TYPES = [
        ('renda_fixa', 'Renda Fixa'),
        ('renda_variavel', 'Renda Variável'),
        ('cripto', 'Cripto'),
        ('outros', 'Outros'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=INVESTMENT_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    applied_at = models.DateField()
    current_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    monthly_return_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - R$ {self.amount}"

# Orçamento
class BudgetPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_income_base = models.DecimalField(max_digits=12, decimal_places=2)
    month_reference = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orçamento - {self.month_reference}"

# Limite por Categoria no Orçamento
class BudgetCategoryLimit(models.Model):
    budget_plan = models.ForeignKey(BudgetPlan, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    amount_limit = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.category.name}: {self.percentage}%"

# Metas Financeiras
class FinancialGoal(models.Model):
    GOAL_TYPES = [
        ('save', 'Economizar'),
        ('invest', 'Investir'),
        ('reduce_expense', 'Reduzir Despesas'),
        ('increase_income', 'Aumentar Receitas'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, help_text="Obrigatório para metas de redução de despesas.")
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Meta: {self.description or self.get_type_display()}"
