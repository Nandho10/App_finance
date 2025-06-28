# Comandos para Limpar e Importar Despesas

## 1. Limpar todas as despesas e categorias de despesas

```powershell
docker-compose exec web python manage.py clean_expense_data
```

## 2. Importar a planilha de despesas

```powershell
curl.exe -X POST "http://localhost:8000/api/import-expense-excel/" -F "file=@E:\Nandho\Financas\App_financeiro\docs\Despesas.xlsx"
```

> **Observação:**
> - Execute o comando 1 antes de cada nova carga para garantir que os dados antigos sejam removidos.
> - Certifique-se de que o arquivo `Despesas.xlsx` está atualizado e salvo antes de rodar o comando 2. 