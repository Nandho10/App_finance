# CHANGELOG

Todas as mudanças importantes do projeto serão documentadas aqui.

## [2025-01-15] - Fase 2: Gestão de Despesas
### Adicionado
- Sistema completo de gestão de despesas
- Formulário de cadastro de despesas com modal
- Filtros avançados por categoria, status, período e data
- Busca por descrição e categoria
- Relatórios de despesas com análises por período
- Gráficos de despesas por categoria e evolução mensal
- Top 5 maiores despesas
- Estatísticas em tempo real (total, quantidade, média)
- Sistema de categorias personalizáveis
- Componente de filtros expansível
- Abas para lista de despesas e relatórios
- Validação de formulários
- Tratamento de erros e estados de loading

### Alterado
- Atualização dos tipos TypeScript para incluir campo `paid_at`
- Melhoria na interface de usuário com design responsivo
- Otimização da performance com filtros client-side

### Corrigido
- Conflitos de nomenclatura entre tipos e componentes
- Imports duplicados no sistema de filtros

## [2025-06-26] - Fase 1: Dashboard e Visualização
### Adicionado
- Estrutura modularizada do backend (core, dashboard, transacoes, usuarios)
- Configuração Docker e docker-compose com PostgreSQL
- Projeto frontend Next.js com Tailwind, TypeScript e componentes do dashboard
- Documentação do MVP e plano de ação em docs/

### Alterado
- Organização das pastas para evitar duplicidades
- Remoção de arquivos e pastas obsoletos

### Corrigido
- Ajuste de .gitignore para não versionar .env

---

Veja detalhes e próximos passos no arquivo `docs/Plano_de_Acao_MVP.md`. 