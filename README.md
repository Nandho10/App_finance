# App Financeiro

Aplicativo de gestão financeira pessoal com backend em Django/PostgreSQL e frontend em Next.js.

## 🚀 Tecnologias Utilizadas

### Backend
- Django 4.2+
- Django REST Framework
- PostgreSQL
- Docker

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

## 📊 Funcionalidades do Dashboard (MVP)
- Visão geral financeira (KPIs)
- Gráfico de receitas vs despesas
- Progresso de orçamento por categoria
- Lista de transações recentes
- Design responsivo

## 🎯 Roadmap MVP
- [x] Estrutura modularizada (backend)
- [x] Docker + PostgreSQL
- [x] Dashboard inicial (frontend)
- [ ] Integração frontend-backend
- [ ] CRUD de despesas e receitas
- [ ] Sistema de orçamento
- [ ] Autenticação de usuários

Veja detalhes em `docs/Plano_de_Acao_MVP.md`.

## 📝 Scripts Úteis
- `docker-compose up --build` — Sobe backend e banco
- `docker-compose exec web python manage.py migrate` — Migrações
- `docker-compose exec web python manage.py createsuperuser` — Superusuário
- `npm run dev` (na pasta frontend) — Frontend Next.js

## 📦 Dependências Principais

### Backend
- Django>=4.2
- psycopg2-binary>=2.9

### Frontend
- next, react, tailwindcss, recharts, axios, react-hook-form, zod, typescript

## 📚 Documentação
- Plano de MVP: `docs/Plano_de_Acao_MVP.md`
- Documentação técnica: `docs/`

---

> Projeto em desenvolvimento contínuo. Sugestões e contribuições são bem-vindas! 