# Notas Técnicas

## Transformações Esperadas no Power Query

Os CSVs já estão estruturados para reporting, mas estes passos no Power Query continuam recomendados para manter o modelo semântico limpo e explícito:

1. Aplicar tipos de dados explícitos em todas as colunas importadas.
2. Renomear as tabelas para os nomes finais do modelo:
   - `fact_sales`
   - `fact_targets`
   - `dim_date`
   - `dim_product`
   - `dim_customer`
   - `dim_geography`
   - `dim_region`
   - `dim_channel`
   - `dim_sales_rep`
3. Remover da visão de relatório colunas de chave natural que não forem mais necessárias depois da validação dos relacionamentos.
4. Ocultar chaves substitutas na camada de relatório.
5. Confirmar que `ReturnedFlag` está tipada como número inteiro, e não texto.
6. Confirmar que campos percentuais como `DiscountPct` estão em decimal e formatados como percentual.
7. Ordenar `dim_date[Month Name]` por `dim_date[Month Number]`.
8. Marcar `dim_date` como tabela de datas usando `dim_date[Date]`.

## Notas de Modelagem

- Usar `OrderDateKey` como relacionamento ativo para inteligência temporal.
- Manter `ShipDateKey` como relacionamento inativo para análises futuras de logística ou prazo de entrega.
- Usar `dim_region` nas páginas que comparam realizado versus meta.
- Usar `dim_geography` para drilldown por estado e cidade quando a análise de metas não for o foco principal.

## Formatação Sugerida

- Moeda: BRL ou formatação monetária neutra, conforme a preferência de apresentação
- Percentuais: uma casa decimal nas páginas executivas e duas casas nas páginas de detalhe
- Quantidades e pedidos: separador de milhar e zero casas decimais

## Sequência Recomendada de Montagem no Power BI

1. Carregar todos os CSVs processed de `data/processed/`.
2. Criar os relacionamentos exatamente como definidos em `docs/data-model.md`.
3. Marcar `dim_date[Date]` como a tabela de datas.
4. Importar o theme de `assets/theme/sales-performance-theme.json`.
5. Criar as medidas DAX de `docs/dax-measures.md`.
6. Ocultar chaves e colunas técnicas.
7. Montar as páginas de acordo com `docs/dashboard-blueprint.md`.
