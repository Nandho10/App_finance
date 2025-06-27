from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # API Endpoints
    path('api/dashboard/', views.dashboard_data, name='dashboard_data'),
    path('api/kpis/', views.kpis, name='kpis'),
    path('api/transactions/', views.recent_transactions, name='recent_transactions'),
    path('api/budget/', views.budget_progress, name='budget_progress'),
    path('api/chart/', views.chart_data, name='chart_data'),
    
    # API Endpoints - Despesas
    path('api/expenses/', views.expenses_list, name='expenses_list'),
    path('api/expenses/create/', views.expense_create, name='expense_create'),
    path('api/expenses/<int:expense_id>/', views.expense_detail, name='expense_detail'),
    path('api/expenses/<int:expense_id>/update/', views.expense_update, name='expense_update'),
    path('api/expenses/<int:expense_id>/delete/', views.expense_delete, name='expense_delete'),
    path('api/expenses/categories/', views.expense_categories, name='expense_categories'),
    
    # API Endpoints - Receitas
    path('api/incomes/', views.incomes_list, name='incomes_list'),
    path('api/incomes/create/', views.income_create, name='income_create'),
    path('api/incomes/<int:income_id>/', views.income_detail, name='income_detail'),
    path('api/incomes/<int:income_id>/update/', views.income_update, name='income_update'),
    path('api/incomes/<int:income_id>/delete/', views.income_delete, name='income_delete'),
    path('api/incomes/categories/', views.income_categories, name='income_categories'),
    
    # API Endpoints - Orçamento
    path('api/budgets/', views.budgets_list, name='budgets_list'),
    path('api/budgets/create/', views.budget_create, name='budget_create'),
    path('api/budgets/<int:budget_id>/', views.budget_detail, name='budget_detail'),
    path('api/budgets/<int:budget_id>/update/', views.budget_update, name='budget_update'),
    path('api/budgets/<int:budget_id>/delete/', views.budget_delete, name='budget_delete'),
    path('api/budgets/alerts/', views.budget_alerts, name='budget_alerts'),
    path('api/budgets/analysis/', views.budget_analysis, name='budget_analysis'),
] 