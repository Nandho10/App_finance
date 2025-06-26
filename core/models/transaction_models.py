from django.db import models
from .user_models import User
from .category_models import Category

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, limit_choices_to={'type': 'income'}, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    received_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"R$ {self.amount} - {self.received_at}"

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