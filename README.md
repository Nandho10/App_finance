# App Financeiro

Aplicativo de gestão financeira pessoal com backend em Django/PostgreSQL e frontend em Next.js.

## 🚀 Tecnologias Utilizadas

### Backend
- Django 5.2+
- Django REST Framework
- PostgreSQL
- Docker
- Pandas (importação Excel)

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Recharts
- Lucide React
- Axios
- React Hook Form
- Zod

## 📁 Estrutura do Projeto

```
├── core/           # Backend principal (Django)
├── dashboard/      # App Django: dashboard
├── transacoes/     # App Django: transações
├── usuarios/       # App Django: usuários
├── frontend/       # Frontend Next.js
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── docs/           # Documentação e plano de MVP
```

## 🐳 Como Executar o Projeto (Docker)

1. Copie o arquivo `.env.example` para `.env` e ajuste as variáveis conforme necessário.
2. Execute:
   ```bash
   docker-compose up --build
   ```
3. O backend Django estará disponível em `http://localhost:8000`.
4. Para rodar migrações:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
5. Para criar superusuário:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## 💻 Como Executar o Frontend

1. Acesse a pasta `frontend`:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. Acesse `http://localhost:3000` no navegador.

## 📊 Funcionalidades Implementadas

### ✅ Módulo de Receitas (100% Banco de Dados)
- **CRUD Completo de Receitas**: Criar, listar, editar e excluir receitas
- **CRUD Completo de Categorias**: Gerenciar categorias de receitas dinamicamente
- **Lógica de Migração**: Ao excluir categoria, migrar receitas ou excluir todas
- **Importação Excel**: Importar receitas e categorias via arquivo Excel
- **KPIs e Relatórios**:
  - Receita total do mês
  - Receita por categoria
  - Evolução mensal da receita
  - Receita média por mês
  - Top fontes de receita

### ✅ Dashboard (MVP)
- Visão geral financeira (KPIs)
- Gráfico de receitas vs despesas
- Progresso de orçamento por categoria
- Lista de transações recentes
- Design responsivo

### ✅ Módulo de Vendas (Completo)
- CRUD completo de vendas: criar, listar, editar, excluir
- Importação de vendas via Excel (comando: import_sales_excel)
- KPIs: total vendido, lucro total, ticket médio, top clientes
- Gráficos: vendas por produto, evolução do lucro, top clientes
- Filtros dinâmicos por período, produto, cliente
- Modal de cadastro/edição
- Integração total backend/frontend
- Link de Vendas no menu lateral

### API Endpoints - Vendas
- `GET /api/sales/` - Listar vendas (com filtros)
- `POST /api/sales/` - Criar venda
- `GET /api/sales/{id}/` - Detalhar venda
- `PUT /api/sales/{id}/` - Atualizar venda
- `DELETE /api/sales/{id}/` - Excluir venda

## 🔧 API Endpoints - Receitas

### Categorias de Receitas
- `GET /api/income-categories/` - Listar categorias
- `POST /api/income-categories/create/` - Criar categoria
- `GET /api/income-categories/{id}/` - Detalhes da categoria
- `PUT /api/income-categories/{id}/update/` - Atualizar categoria
- `DELETE /api/income-categories/{id}/delete/` - Deletar categoria
- `POST /api/income-categories/{id}/migrate/` - Migrar receitas
- `DELETE /api/income-categories/{id}/delete-with-incomes/` - Deletar com receitas

### Receitas
- `GET /api/incomes/` - Listar receitas
- `POST /api/incomes/create/` - Criar receita
- `GET /api/incomes/{id}/` - Detalhes da receita
- `PUT /api/incomes/{id}/update/` - Atualizar receita
- `DELETE /api/incomes/{id}/delete/` - Deletar receita

### Importação e Relatórios
- `POST /api/import-income-excel/` - Importar Excel
- `GET /api/income-kpis/` - KPIs de receitas
- `GET /api/income-by-category/` - Receita por categoria
- `GET /api/income-evolution/` - Evolução mensal
- `GET /api/top-income-sources/` - Top fontes de receita

## 🔧 API Endpoints - Despesas

## Categorias de Despesas (CRUD Completo)

Agora o sistema possui endpoints completos para gerenciamento de categorias de despesas, incluindo:
- Criação, listagem, edição e exclusão de categorias de despesas
- Migração de despesas entre categorias antes da exclusão
- Exclusão de categoria junto com todas as despesas

### Endpoints principais
- `POST /api/expense-categories/create/` — criar categoria
- `GET /api/expense-categories/<id>/` — detalhes da categoria
- `PUT /api/expense-categories/<id>/update/` — atualizar categoria
- `DELETE /api/expense-categories/<id>/delete/` — excluir categoria (com lógica de migração)
- `POST /api/expense-categories/<id>/migrate/` — migrar despesas para outra categoria
- `DELETE /api/expense-categories/<id>/delete-with-expenses/` — excluir categoria e todas as despesas

Veja exemplos de uso na documentação da API ou via ferramentas como curl/Postman.

## 📝 Comandos de Gerenciamento

### Importação Excel
```bash
# Importar receitas via linha de comando
python manage.py import_income_excel arquivo.xlsx --user-id 1

# Simular importação (dry-run)
python manage.py import_income_excel arquivo.xlsx --dry-run

# Especificar planilha
python manage.py import_income_excel arquivo.xlsx --sheet-name "Receitas"
```

### População de Dados
```bash
# Popular dados de teste
python manage.py populate_test_data
```

## 🎯 Roadmap MVP
- [x] Estrutura modularizada (backend)
- [x] Docker + PostgreSQL
- [x] Dashboard inicial (frontend)
- [x] CRUD completo de receitas (banco de dados)
- [x] CRUD completo de categorias de receitas
- [x] Importação Excel de receitas
- [x] KPIs e relatórios de receitas
- [ ] Integração frontend-backend
- [ ] CRUD de despesas (banco de dados)
- [ ] Sistema de orçamento
- [ ] Autenticação de usuários

Veja detalhes em `docs/Plano_de_Acao_MVP.md`.

## 📝 Scripts Úteis
- `docker-compose up --build` — Sobe backend e banco
- `docker-compose exec web python manage.py migrate` — Migrações
- `docker-compose exec web python manage.py createsuperuser` — Superusuário
- `docker-compose exec web python manage.py import_income_excel arquivo.xlsx` — Importar Excel
- `npm run dev` (na pasta frontend) — Frontend Next.js

## 📦 Dependências Principais

### Backend
- Django>=5.2
- psycopg2-binary>=2.9
- pandas>=2.1.4
- openpyxl>=3.1.2
- xlrd>=2.0.1

### Frontend
- next, react, tailwindcss, recharts, axios, react-hook-form, zod, typescript

## 📚 Documentação
- Plano de MVP: `docs/Plano_de_Acao_MVP.md`
- Plano de Migração: `docs/Plano_Migracao_Receitas.md`
- Documentação técnica: `docs/`

### Importação de Despesas via Excel

Você pode importar despesas e categorias automaticamente via arquivo Excel:
- Endpoint: `POST /api/import-expense-excel/`
- Formato: arquivo .xlsx ou .xls com colunas como descrição, valor, categoria, data, forma de pagamento (nomes flexíveis)
- O sistema identifica as colunas automaticamente e cria categorias de despesas se não existirem.
- Retorna resumo da importação (quantas despesas/categorias criadas, erros, etc).

Veja exemplos em `exemplo_importacao_receitas.md` (o formato é similar para despesas).

### KPIs e Relatórios de Despesas

- `GET /api/expense-kpis/` — KPIs principais de despesas (total do mês, mês anterior, média, crescimento, quantidade)
- `GET /api/expense-by-category/` — Total e quantidade de despesas por categoria (parâmetros opcionais: month, year)
- `GET /api/expense-evolution/` — Evolução mensal das despesas (parâmetro opcional: months)
- `GET /api/top-expense-categories/` — Top categorias de despesas (parâmetros opcionais: limit, months)

Todos os endpoints retornam dados prontos para dashboards e relatórios financeiros.

### Integração Frontend

Os dashboards, relatórios e KPIs de despesas agora consomem dados reais do backend, utilizando os endpoints REST documentados acima. Os componentes do frontend foram atualizados para refletir os dados do banco de dados em tempo real.

### Gerenciamento de Categorias de Despesas no Frontend

Agora é possível criar, editar, excluir e migrar categorias de despesas diretamente pelo frontend, com integração total ao backend. O modal de categorias permite todas as operações, inclusive migração de despesas antes da exclusão.

> **Nota importante:** Ao criar uma despesa via API (`POST /api/expenses/create/`), o campo `category` deve ser enviado como o **nome da categoria** (string), e não como ID. Caso contrário, será retornado erro 400 (campo obrigatório).

---

> Projeto em desenvolvimento contínuo. Sugestões e contribuições são bem-vindas! 