#!/usr/bin/env python
import pandas as pd
import os

def check_excel_structure():
    file_path = r"E:\Nandho\Financas\App_financeiro\docs\vendas.xlsx"
    
    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        return
    
    try:
        # Ler o arquivo Excel
        df = pd.read_excel(file_path)
        
        print("=== ESTRUTURA DA PLANILHA DE VENDAS ===")
        print(f"Total de linhas: {len(df)}")
        print(f"Total de colunas: {len(df.columns)}")
        print(f"\nColunas encontradas:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1}. {col}")
        
        print(f"\nPrimeiras 3 linhas de dados:")
        print(df.head(3).to_string())
        
        print(f"\nTipos de dados das colunas:")
        print(df.dtypes)
        
        # Verificar valores únicos em algumas colunas
        print(f"\nValores únicos por coluna (primeiras 5 colunas):")
        for col in df.columns[:5]:
            unique_values = df[col].dropna().unique()
            print(f"\n{col}:")
            for val in unique_values[:10]:  # Mostrar apenas os primeiros 10 valores únicos
                print(f"  - {val}")
            if len(unique_values) > 10:
                print(f"  ... e mais {len(unique_values) - 10} valores")
        
    except Exception as e:
        print(f"Erro ao ler arquivo: {str(e)}")

if __name__ == "__main__":
    check_excel_structure() 