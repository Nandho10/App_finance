# Plano de Migração - Módulo de Receitas e Categorias Dinâmicas

## Objetivo
Migrar todos os endpoints de receitas e categorias para uso exclusivo do banco de dados (Django ORM), eliminando mocks e garantindo flexibilidade e escalabilidade para o controle financeiro familiar.

---

## Etapas do Plano

### 1. CRUD Completo de Categorias de Receitas
- Permitir criar, listar, editar e excluir categorias de receitas via API REST.
- As categorias serão salvas no banco de dados.
- Ao excluir uma categoria, perguntar ao usuário se deseja:
  - Migrar as receitas para outra categoria existente.
  - Excluir todas as receitas relacionadas.
- Visual e experiência seguindo o padrão das telas já existentes.

### 2. Endpoints 100% Banco de Dados
- Todos os endpoints de receitas e categorias usarão apenas o banco de dados (Django ORM).
- Nenhum dado de mock será utilizado.

### 3. Importação Inteligente do Excel
- Será criado um assistente para importar receitas e categorias do Excel.
- O sistema irá mapear as colunas do arquivo para os campos do banco, permitindo ajuste dos nomes antes de importar.
- Se uma categoria não existir, será criada automaticamente.
- O usuário poderá receber ajuda para preparar o arquivo Excel.

### 4. KPIs e Relatórios
- Receita total do mês
- Receita por categoria
- Evolução mensal da receita
- Receita média por mês
- Top fontes de receita

---

## Status Atual

| Item                                      | Status         |
|-------------------------------------------|----------------|
| CRUD de receitas (banco)                  | ✅ Pronto      |
| CRUD de categorias de receitas (banco)    | ❌ Falta       |
| Lógica de exclusão/migração de receitas   | ❌ Falta       |
| Importação do Excel                       | ❌ Falta       |
| Documentação detalhada                    | ❌ Falta       |

---

## Próximos Passos
1. Implementar CRUD completo de categorias de receitas no backend.
2. Implementar lógica de migração/exclusão ao deletar categoria.
3. Planejar/importar do Excel e documentar endpoints.

---

## Observações
- Categorias de receitas podem ser criadas, editadas e excluídas livremente pelo usuário via frontend.
- Ao excluir uma categoria, o sistema perguntará se deseja migrar receitas para outra ou excluir todas.
- O visual seguirá o padrão das telas já existentes.
- O assistente de importação do Excel ajudará a mapear colunas e criar categorias automaticamente. 