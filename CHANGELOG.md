# CHANGELOG

Todas as mudanças importantes do projeto serão documentadas aqui.

## [2025-01-16] - Fase 4: Módulo de Vendas
### Adicionado
- **Modelagem de Vendas**: Novo modelo `Venda` com campos para data, produto/serviço, valor da venda, custo, forma de recebimento e observações
- **Cálculo Automático de Lucro**: Propriedade `lucro_bruto` que calcula automaticamente a margem de lucro por venda
- **Admin Django Configurado**: Interface administrativa para o modelo Venda com filtros e busca
- **Migração de Banco de Dados**: Tabela de vendas criada e funcional
- **Configuração SQLite Local**: Ajuste temporário para desenvolvimento local sem Docker
- **API REST Completa**: Endpoints para CRUD completo de vendas
  - `GET /api/sales/` - Listar vendas com filtros
  - `POST /api/sales/create/` - Criar nova venda
  - `GET /api/sales/{id}/` - Obter detalhes de venda
  - `PUT /api/sales/{id}/update/` - Atualizar venda
  - `DELETE /api/sales/{id}/delete/` - Excluir venda
- **Validações Robustas**: Validação de campos obrigatórios, formatos de data e valores numéricos
- **Filtros Avançados**: Filtros por data, produto/serviço e forma de recebimento
- **Frontend Completo**: Interface de usuário para gestão de vendas
  - Página de listagem com tabela responsiva
  - Modal para criar e editar vendas
  - Filtros por período, produto/serviço e forma de recebimento
  - Cards de resumo com totais (vendas, custos, lucro bruto)
  - Integração completa com a API REST
  - Validações em tempo real no formulário
  - Cálculo automático de lucro bruto
- **Tipos TypeScript**: Definições completas de tipos para vendas
- **Serviços de API**: Funções para comunicação com o backend
- **Navegação**: Link de vendas adicionado ao Sidebar

### Alterado
- **Remoção de Modelo Duplicado**: Eliminado o modelo `Sale` antigo para evitar conflitos
- **Configuração de Banco**: Alterado temporariamente para SQLite para desenvolvimento local
- **Estrutura de Models**: Organização dos modelos em arquivos separados por funcionalidade

### Corrigido
- **Conflitos de Nomenclatura**: Resolvido conflito entre modelos `Sale` e `Venda`
- **Dependências**: Instalação e configuração correta do Django REST Framework

## [2025-01-16] - Fase 3: Módulo de Receitas (100% Banco de Dados)
### Adicionado
- **CRUD Completo de Receitas**: Endpoints para criar, listar, editar e excluir receitas usando Django ORM
- **CRUD Completo de Categorias de Receitas**: Gerenciamento dinâmico de categorias com validações
- **Lógica de Migração Inteligente**: Ao excluir categoria, opção de migrar receitas ou excluir todas
- **Importação Excel**: Sistema completo para importar receitas e categorias via arquivo Excel
  - Comando de gerenciamento `import_income_excel`
  - Endpoint API para upload de arquivos
  - Mapeamento automático de colunas
  - Criação automática de categorias
  - Validação e tratamento de erros
- **KPIs e Relatórios Avançados**:
  - Receita total do mês atual e anterior
  - Receita por categoria com filtros por período
  - Evolução mensal da receita (configurável)
  - Receita média por mês (últimos 6 meses)
  - Top fontes de receita com percentuais
  - Crescimento percentual entre meses
- **Admin Django Configurado**: Interface administrativa para todos os modelos
- **Dependências Atualizadas**: Pandas, openpyxl e xlrd para importação Excel
- **Funcionalidade de edição de receitas no frontend**
- **Modal de edição integrado com backend**

### Alterado
- **Migração de Dados Mockados**: Todos os endpoints de receitas agora usam banco de dados
- **Estrutura de URLs**: Novos endpoints organizados por funcionalidade
- **Validações**: Sistema robusto de validação de dados e tratamento de erros
- **Documentação**: README atualizado com todas as funcionalidades e endpoints

### Corrigido
- **Consistência de Dados**: Garantia de integridade referencial entre receitas e categorias
- **Tratamento de Erros**: Melhor feedback para usuários em caso de problemas
- **Performance**: Otimização de queries com select_related e agregações

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

## [Unreleased]

### Added
- Sistema completo de receitas com banco de dados
- CRUD completo para categorias de receitas
- Lógica de migração/exclusão ao deletar categoria
- Importação inteligente via Excel com comando de gerenciamento
- Endpoint API para importação de receitas
- KPIs e relatórios de receitas
- Configuração do admin Django para modelos relacionados
- Modal de criação de receitas no frontend
- **Funcionalidade de edição de receitas no frontend**
- **Modal de edição integrado com backend**
- **Funcionalidade de edição de despesas no frontend**
- **Modal de edição de despesas integrado com backend**
- feat: CRUD completo de categorias de despesas (criar, editar, excluir, migrar despesas entre categorias, exclusão em massa), endpoints REST e registro no admin.
- feat: importação inteligente de despesas e categorias via Excel, com mapeamento automático de colunas e criação automática de categorias.
- feat: endpoints de KPIs e relatórios de despesas (total do mês, por categoria, evolução mensal, top categorias), seguindo padrão dos endpoints de receitas.
- feat: integração do frontend com os endpoints reais de despesas (KPIs, relatórios, categorias), dashboards e relatórios agora usam dados do backend.

### Changed
- Migração de mocks para banco de dados real
- Atualização da documentação com novas funcionalidades
- Melhoria na estrutura de tipos TypeScript

### Fixed
- Botão "Nova Receita" não abria modal
- **Botão "Editar" não tinha funcionalidade implementada (Receitas)**
- **Botão "Editar" não tinha funcionalidade implementada (Despesas)**

## [0.1.0] - 2025-06-28

### Added
- Estrutura inicial do projeto Django
- Configuração do frontend Next.js
- Modelos básicos de dados
- Sistema de autenticação
- Dashboard básico

---

Veja detalhes e próximos passos no arquivo `docs/Plano_de_Acao_MVP.md`. 