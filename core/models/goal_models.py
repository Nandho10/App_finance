from django.db import models
from .user_models import User
from .category_models import Category

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