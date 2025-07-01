from django.contrib import admin
from .models.category_models import Category
from .models.transaction_models import Income, Expense
from .models.user_models import User
from .models import Sale

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'user']
    list_filter = ['type', 'user']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'category', 'account', 'received_at', 'user']
    list_filter = ['category', 'received_at', 'user']
    search_fields = ['description', 'account']
    date_hierarchy = 'received_at'
    ordering = ['-received_at']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'category', 'favored', 'payment_method', 'paid_at', 'user']
    list_filter = ['category', 'payment_method', 'paid_at', 'user']
    search_fields = ['description', 'favored']
    date_hierarchy = 'paid_at'
    ordering = ['-paid_at']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']

admin.site.register(Sale)
