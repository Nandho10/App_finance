from django.db import models
from .user_models import User

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