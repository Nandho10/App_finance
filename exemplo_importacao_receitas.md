# Exemplo de Importação de Receitas via Excel

## Formato do Arquivo Excel

O sistema aceita arquivos Excel (.xlsx ou .xls) com as seguintes colunas:

### Colunas Obrigatórias
- **Descrição**: Nome/descrição da receita
- **Valor**: Valor da receita (número)
- **Data**: Data de recebimento (formato: YYYY-MM-DD)

### Colunas Opcionais
- **Categoria**: Nome da categoria (será criada automaticamente se não existir)
- **Fonte**: Origem da receita

## Exemplo de Estrutura do Excel

| Descrição | Valor | Data | Categoria | Fonte |
|-----------|-------|------|-----------|-------|
| Salário Janeiro | 5000.00 | 2024-01-05 | Salário | Empresa ABC |
| Freelance Projeto X | 1500.00 | 2024-01-10 | Freelance | Cliente XYZ |
| Dividendos | 300.00 | 2024-01-15 | Investimentos | Corretora |
| Bônus | 2000.00 | 2024-01-20 | Salário | Empresa ABC |
| Venda Produto | 800.00 | 2024-01-25 | Vendas | Cliente |

## Mapeamento Automático de Colunas

O sistema reconhece automaticamente as colunas baseado nos nomes:

### Descrição
- `descrição`, `description`, `desc`, `nome`

### Valor
- `valor`, `amount`, `montante`, `preço`

### Data
- `data`, `date`, `data_recebimento`, `received_at`

### Categoria
- `categoria`, `category`, `cat`

### Fonte
- `fonte`, `source`, `origem`

## Como Importar

### Via Comando Django
```bash
# Importar arquivo
python manage.py import_income_excel receitas.xlsx --user-id 1

# Simular importação (não salva no banco)
python manage.py import_income_excel receitas.xlsx --dry-run

# Especificar planilha
python manage.py import_income_excel receitas.xlsx --sheet-name "Receitas"
```

### Via API
```bash
# Upload via curl
curl -X POST \
  -F "file=@receitas.xlsx" \
  http://localhost:8000/api/import-income-excel/
```

### Via Frontend (futuro)
- Interface web para upload de arquivos
- Preview dos dados antes da importação
- Mapeamento manual de colunas se necessário

## Validações

O sistema valida:
- ✅ Formato de data válido
- ✅ Valor numérico positivo
- ✅ Descrição não vazia
- ✅ Criação automática de categorias
- ✅ Tratamento de dados duplicados

## Relatório de Importação

Após a importação, você receberá:
- Número de categorias criadas
- Número de receitas importadas
- Lista de erros (se houver)
- Total de linhas processadas

## Dicas

1. **Prepare o arquivo**: Certifique-se de que as datas estão no formato correto
2. **Teste primeiro**: Use `--dry-run` para verificar se tudo está correto
3. **Backup**: Faça backup dos dados antes de importar grandes volumes
4. **Categorias**: Use nomes consistentes para categorias
5. **Valores**: Use ponto como separador decimal (ex: 1500.50)

## Exemplo de Resposta da API

```json
{
  "message": "Importação concluída com sucesso",
  "categories_created": 2,
  "incomes_created": 5,
  "errors": [],
  "total_processed": 5
}
``` 