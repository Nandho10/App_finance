from django.db import models
from .user_models import User
from .category_models import Category

class BudgetPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_income_base = models.DecimalField(max_digits=12, decimal_places=2)
    month_reference = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orçamento - {self.month_reference}"

class BudgetCategoryLimit(models.Model):
    budget_plan = models.ForeignKey(BudgetPlan, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    amount_limit = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.category.name}: {self.percentage}%" 