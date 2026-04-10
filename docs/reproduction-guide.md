# Guia de Reprodução

## 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

## 2. Regerar os Dados

```bash
python scripts/run_full_build.py
```

Saídas esperadas:

- Tabelas raw em `data/raw/`
- Tabelas em star schema em `data/processed/`

## 3. Montar o Relatório no Power BI Desktop

1. Abra o Power BI Desktop.
2. Importe todos os CSVs de `data/processed/`.
3. Renomeie as tabelas para os nomes documentados em `docs/data-model.md`.
4. Crie os relacionamentos listados em `docs/data-model.md`.
5. Marque `dim_date[Date]` como a tabela de datas do modelo.
6. Ordene `dim_date[Month Name]` por `dim_date[Month Number]`.
7. Crie as medidas DAX de `docs/dax-measures.md`.
8. Importe o tema de `assets/theme/sales-performance-theme.json`.
9. Monte as páginas seguindo `docs/dashboard-blueprint.md`.
10. Exporte as screenshots para `screenshots/`.

## 4. Gerar Imagens de Preview para Portfólio

Se você quiser uma camada visual imediata para GitHub antes de exportar screenshots nativas do Power BI:

```bash
python scripts/generate_dashboard_previews.py
```

## 5. Desenho Recomendado para Slicers

- Slicers globais: Data, Região, Canal de Vendas, Categoria
- Slicers diagnósticos quando fizer sentido: Segmento, SubCategory

## 6. Etapas Finais Manuais

Estas etapas ainda dependem do Power BI Desktop:

- composição final das páginas
- configuração de bookmarks e tooltips
- exportação das screenshots
- save opcional em PBIP e commit final
