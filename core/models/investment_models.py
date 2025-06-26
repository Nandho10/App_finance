from django.db import models
from .user_models import User

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