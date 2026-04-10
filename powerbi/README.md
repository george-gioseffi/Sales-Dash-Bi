# Notas de Montagem no Power BI

## Status

O repositório está preparado para um fluxo baseado em PBIP, mas um artefato `.pbip` completo ainda não foi gerado neste ambiente porque a montagem final do canvas depende do Power BI Desktop.

O que já está pronto:

- dados raw e processed reproduzíveis
- exports do star schema
- biblioteca DAX
- arquivo de tema
- blueprint do dashboard
- previews visuais em `screenshots/`
- guia final de montagem em `powerbi/final-dashboard-handoff.md`

## Fluxo Recomendado no Power BI Desktop

1. Crie um novo arquivo no Power BI Desktop.
2. Importe todos os CSVs de `data/processed/`.
3. Renomeie as tabelas para os nomes documentados.
4. Monte os relacionamentos definidos em `docs/data-model.md`.
5. Marque `dim_date[Date]` como a tabela de datas.
6. Ordene `dim_date[Month Name]` por `dim_date[Month Number]`.
7. Crie as medidas DAX de `docs/dax-measures.md`.
8. Importe `assets/theme/sales-performance-theme.json`.
9. Monte as páginas seguindo `docs/dashboard-blueprint.md`.
10. Salve o relatório como PBIP, se desejar, e exporte as screenshots para `screenshots/`.

## Assets de Preview para Portfólio

O repositório já inclui seis previews estáticos do dashboard gerados a partir dos dados reais do projeto:

```bash
python scripts/generate_dashboard_previews.py
```

Essas imagens servem para fortalecer a apresentação no GitHub até que screenshots nativas do Power BI Desktop substituam os mesmos arquivos.

## Sugestão de Naming para PBIP

- Nome do relatório: `Sales Performance Analytics`
- Pasta sugerida: `powerbi/SalesPerformanceAnalytics/`
- Arquivo opcional: `powerbi/Sales Performance Analytics.pbip`

## Limitação Prática

Como o arquivo nativo ainda não foi gerado aqui, o artefato final `.pbix` ou `.pbip`, as interações reais do relatório e as screenshots nativas ainda dependem de abrir o Power BI Desktop na máquina.

Essa limitação é intencional e honesta. A Microsoft documenta que a conversão de PBIX para PBIP e a criação de PBIR acontecem pelo fluxo de Save As do Power BI Desktop, não por um caminho suportado de conversão apenas via terminal.
