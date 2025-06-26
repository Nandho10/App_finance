from django.db import models
from .user_models import User
from .category_models import Category

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    limit = models.DecimalField(max_digits=12, decimal_places=2)
    closing_day = models.PositiveSmallIntegerField()
    due_day = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

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