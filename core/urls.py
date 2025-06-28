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
    path('api/expenses/categories/', views.expense_categories, name='expense_categories'),
    path('api/expenses/<int:expense_id>/', views.expense_detail, name='expense_detail'),
    path('api/expenses/<int:expense_id>/update/', views.expense_update, name='expense_update'),
    path('api/expenses/<int:expense_id>/delete/', views.expense_delete, name='expense_delete'),
    
    # API Endpoints - Receitas
    path('api/incomes/', views.incomes_list, name='incomes_list'),
    path('api/incomes/create/', views.income_create, name='income_create'),
    path('api/incomes/categories/', views.income_categories, name='income_categories'),
    path('api/incomes/<int:income_id>/', views.income_detail, name='income_detail'),
    path('api/incomes/<int:income_id>/update/', views.income_update, name='income_update'),
    path('api/incomes/<int:income_id>/delete/', views.income_delete, name='income_delete'),
    
    # API Endpoints - Categorias de Receitas (CRUD Completo)
    path('api/income-categories/create/', views.income_category_create, name='income_category_create'),
    path('api/income-categories/<int:category_id>/', views.income_category_detail, name='income_category_detail'),
    path('api/income-categories/<int:category_id>/update/', views.income_category_update, name='income_category_update'),
    path('api/income-categories/<int:category_id>/delete/', views.income_category_delete, name='income_category_delete'),
    path('api/income-categories/<int:category_id>/migrate/', views.income_category_migrate, name='income_category_migrate'),
    path('api/income-categories/<int:category_id>/delete-with-incomes/', views.income_category_delete_with_incomes, name='income_category_delete_with_incomes'),
    
    # API Endpoints - Categorias de Despesas (CRUD Completo)
    path('api/expense-categories/create/', views.expense_category_create, name='expense_category_create'),
    path('api/expense-categories/<int:category_id>/', views.expense_category_detail, name='expense_category_detail'),
    path('api/expense-categories/<int:category_id>/update/', views.expense_category_update, name='expense_category_update'),
    path('api/expense-categories/<int:category_id>/delete/', views.expense_category_delete, name='expense_category_delete'),
    path('api/expense-categories/<int:category_id>/migrate/', views.expense_category_migrate, name='expense_category_migrate'),
    path('api/expense-categories/<int:category_id>/delete-with-expenses/', views.expense_category_delete_with_expenses, name='expense_category_delete_with_expenses'),
    path('api/expense-categories/', views.expense_categories_list, name='expense_categories_list'),
    
    # API Endpoints - Orçamento
    path('api/budgets/', views.budgets_list, name='budgets_list'),
    path('api/budgets/create/', views.budget_create, name='budget_create'),
    path('api/budgets/alerts/', views.budget_alerts, name='budget_alerts'),
    path('api/budgets/analysis/', views.budget_analysis, name='budget_analysis'),
    path('api/budgets/<int:budget_id>/', views.budget_detail, name='budget_detail'),
    path('api/budgets/<int:budget_id>/update/', views.budget_update, name='budget_update'),
    path('api/budgets/<int:budget_id>/delete/', views.budget_delete, name='budget_delete'),
    
    # API Endpoint - Importação Excel
    path('api/import-income-excel/', views.import_income_excel_api, name='import_income_excel_api'),
    path('api/import-expense-excel/', views.import_expense_excel_api, name='import_expense_excel_api'),
    
    # API Endpoints - KPIs e Relatórios de Receitas
    path('api/income-kpis/', views.income_kpis, name='income_kpis'),
    path('api/income-by-category/', views.income_by_category, name='income_by_category'),
    path('api/income-evolution/', views.income_evolution, name='income_evolution'),
    path('api/top-income-sources/', views.top_income_sources, name='top_income_sources'),
    
    # API Endpoints - KPIs e Relatórios de Despesas
    path('api/expense-kpis/', views.expense_kpis, name='expense_kpis'),
    path('api/expense-by-category/', views.expense_by_category, name='expense_by_category'),
    path('api/expense-evolution/', views.expense_evolution, name='expense_evolution'),
    path('api/top-expense-categories/', views.top_expense_categories, name='top_expense_categories'),
] 