# App Financeiro - Frontend

Frontend do aplicativo de gestão financeira pessoal desenvolvido com Next.js 14, TypeScript e Tailwind CSS.

## 🚀 Tecnologias

- **Next.js 14** - Framework React com App Router
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Framework CSS utilitário
- **Recharts** - Biblioteca de gráficos
- **Lucide React** - Ícones
- **Axios** - Cliente HTTP
- **React Hook Form** - Gerenciamento de formulários
- **Zod** - Validação de schemas

## 📁 Estrutura do Projeto

```
src/
├── app/                    # App Router do Next.js
│   ├── globals.css        # Estilos globais
│   ├── layout.tsx         # Layout principal
│   └── page.tsx           # Página inicial (Dashboard)
├── components/            # Componentes React
│   ├── DashboardHeader.tsx
│   ├── KPICard.tsx
│   ├── TransactionChart.tsx
│   ├── RecentTransactions.tsx
│   └── BudgetProgress.tsx
└── types/                 # Tipos TypeScript
    └── dashboard.ts
```

## 🎨 Componentes

### DashboardHeader
Cabeçalho com navegação e informações do usuário.

### KPICard
Cards de indicadores de performance (KPI) com:
- Saldo atual
- Receitas
- Despesas
- Economias

### TransactionChart
Gráfico de linha mostrando evolução de receitas e despesas ao longo do tempo.

### RecentTransactions
Lista das transações mais recentes com formatação de valores e datas.

### BudgetProgress
Barras de progresso para acompanhamento de orçamentos por categoria.

## 🚀 Como Executar

1. **Instalar dependências:**
   ```bash
   npm install
   ```

2. **Executar em desenvolvimento:**
   ```bash
   npm run dev
   ```

3. **Acessar:**
   ```
   http://localhost:3000
   ```

## 📊 Funcionalidades do Dashboard

- **Visão Geral Financeira**: KPIs principais em cards
- **Gráfico de Evolução**: Receitas vs Despesas por período
- **Progresso de Orçamento**: Acompanhamento por categoria
- **Transações Recentes**: Lista das últimas movimentações
- **Design Responsivo**: Adaptado para desktop e mobile

## 🎯 Próximos Passos

- [ ] Integração com API Django
- [ ] Autenticação de usuários
- [ ] Formulários de transações
- [ ] Filtros e busca
- [ ] Modo escuro
- [ ] Notificações em tempo real

## 🔧 Scripts Disponíveis

- `npm run dev` - Servidor de desenvolvimento
- `npm run build` - Build de produção
- `npm run start` - Servidor de produção
- `npm run lint` - Verificação de código 