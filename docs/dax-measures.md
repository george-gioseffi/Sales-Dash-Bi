# Medidas DAX

Esta biblioteca assume os seguintes nomes de tabelas no Power BI:

- `fact_sales`
- `fact_targets`
- `dim_date`
- `dim_product`
- `dim_customer`
- `dim_geography`
- `dim_region`
- `dim_channel`
- `dim_sales_rep`

Antes de usar medidas de inteligência temporal, marque `dim_date[Date]` como a coluna oficial de data do modelo.

## Métricas Centrais

### 1. Total Sales

```DAX
Total Sales =
SUM ( fact_sales[SalesAmount] )
```

Descrição: Soma das vendas líquidas após desconto.  
Uso: Cards principais, linhas de tendência e comparações por categoria e região.

### 2. Gross Sales

```DAX
Gross Sales =
SUM ( fact_sales[GrossSalesAmount] )
```

Descrição: Soma das vendas antes do desconto.  
Uso: Análise de desconto e lógica de ponte entre bruto e líquido.

### 3. Total Profit

```DAX
Total Profit =
SUM ( fact_sales[ProfitAmount] )
```

Descrição: Contribuição total de lucro.  
Uso: Cards de KPI, páginas de lucratividade, scatter plots e visuais de ranking.

### 4. Total Cost

```DAX
Total Cost =
SUM ( fact_sales[CostAmount] )
```

Descrição: Custo total absorvido pelos itens vendidos.  
Uso: Cálculo de margem e comparações entre receita e custo.

### 5. Discount Amount

```DAX
Discount Amount =
SUM ( fact_sales[DiscountAmount] )
```

Descrição: Valor absoluto concedido em desconto.  
Uso: Cards de acompanhamento de desconto e diagnósticos de lucratividade.

### 6. Total Orders

```DAX
Total Orders =
DISTINCTCOUNT ( fact_sales[OrderID] )
```

Descrição: Quantidade de pedidos distintos.  
Uso: Cards de KPI, ticket médio e análise de eficiência por canal.

### 7. Total Quantity

```DAX
Total Quantity =
SUM ( fact_sales[Quantity] )
```

Descrição: Total de unidades vendidas.  
Uso: Análise de volume, mix de produto e checagem de volume com margem fraca.

### 8. Total Customers

```DAX
Total Customers =
DISTINCTCOUNT ( dim_customer[CustomerKey] )
```

Descrição: Quantidade de clientes distintos no contexto atual de filtro.  
Uso: Cards de mix de clientes e análise de sales por cliente.

### 9. Average Order Value

```DAX
Average Order Value =
DIVIDE ( [Total Sales], [Total Orders] )
```

Descrição: Valor médio de venda por pedido.  
Uso: Visão executiva e comparação entre canais.

### 10. Average Unit Price

```DAX
Average Unit Price =
DIVIDE ( [Total Sales], [Total Quantity] )
```

Descrição: Receita média realizada por unidade vendida.  
Uso: Diagnóstico de mix de produto e de preço.

## Lucratividade

### 11. Profit Margin %

```DAX
Profit Margin % =
DIVIDE ( [Total Profit], [Total Sales] )
```

Descrição: Lucro gerado para cada unidade monetária de venda.  
Uso: Cards de margem, comparação por categoria e eficiência por canal.

### 12. Discount %

```DAX
Discount % =
DIVIDE ( [Discount Amount], [Gross Sales] )
```

Descrição: Parcela da venda bruta concedida como desconto.  
Uso: KPI executivo, análise desconto versus margem e revisão de política de preço.

### 13. Returned Lines

```DAX
Returned Lines =
SUM ( fact_sales[ReturnedFlag] )
```

Descrição: Contagem de linhas marcadas como devolvidas.  
Uso: Acompanhamento de devolução e diagnósticos operacionais por canal.

### 14. Return Rate %

```DAX
Return Rate % =
DIVIDE ( [Returned Lines], COUNTROWS ( fact_sales ) )
```

Descrição: Participação de linhas devolvidas no contexto atual.  
Uso: Cards de KPI e checagens de qualidade operacional e serviço.

### 15. Profit per Order

```DAX
Profit per Order =
DIVIDE ( [Total Profit], [Total Orders] )
```

Descrição: Lucro médio gerado por pedido.  
Uso: Benchmark de eficiência por canal e lucratividade.

### 16. Sales per Customer

```DAX
Sales per Customer =
DIVIDE ( [Total Sales], [Total Customers] )
```

Descrição: Receita média gerada por cliente ativo.  
Uso: Análise de segmento e concentração de clientes.

## Inteligência Temporal

### 17. Sales PY

```DAX
Sales PY =
CALCULATE ( [Total Sales], DATEADD ( dim_date[Date], -1, YEAR ) )
```

Descrição: Vendas no mesmo período do ano anterior.  
Uso: Cards de YoY, gráficos de tendência e comparação anual.

### 18. Sales YoY %

```DAX
Sales YoY % =
DIVIDE ( [Total Sales] - [Sales PY], [Sales PY] )
```

Descrição: Taxa de crescimento de vendas ano contra ano.  
Uso: Visão executiva e análise de tendência.

### 19. Profit PY

```DAX
Profit PY =
CALCULATE ( [Total Profit], DATEADD ( dim_date[Date], -1, YEAR ) )
```

Descrição: Lucro no mesmo período do ano anterior.  
Uso: Narrativa de margem YoY e tendência de lucratividade.

### 20. Profit YoY %

```DAX
Profit YoY % =
DIVIDE ( [Total Profit] - [Profit PY], [Profit PY] )
```

Descrição: Taxa de crescimento de lucro ano contra ano.  
Uso: Página de lucratividade e resumo executivo.

### 21. Sales PM

```DAX
Sales PM =
CALCULATE ( [Total Sales], DATEADD ( dim_date[Date], -1, MONTH ) )
```

Descrição: Vendas do mês anterior.  
Uso: Diagnóstico de tendência mês contra mês.

### 22. Sales MoM

```DAX
Sales MoM =
[Total Sales] - [Sales PM]
```

Descrição: Variação absoluta de vendas versus o mês anterior.  
Uso: Cards de tendência e leitura de aceleração ou desaceleração.

### 23. Profit PM

```DAX
Profit PM =
CALCULATE ( [Total Profit], DATEADD ( dim_date[Date], -1, MONTH ) )
```

Descrição: Lucro do mês anterior.  
Uso: Acompanhamento de tendência de lucro.

### 24. Profit MoM

```DAX
Profit MoM =
[Total Profit] - [Profit PM]
```

Descrição: Variação absoluta de lucro versus o mês anterior.  
Uso: Cards de tendência e análise do movimento de lucratividade.

### 25. Running Sales

```DAX
Running Sales =
CALCULATE (
    [Total Sales],
    FILTER (
        ALLSELECTED ( dim_date[Date] ),
        dim_date[Date] <= MAX ( dim_date[Date] )
    )
)
```

Descrição: Vendas acumuladas no intervalo visível de datas.  
Uso: Linhas acumuladas e leitura de progresso no ano.

### 26. Running Profit

```DAX
Running Profit =
CALCULATE (
    [Total Profit],
    FILTER (
        ALLSELECTED ( dim_date[Date] ),
        dim_date[Date] <= MAX ( dim_date[Date] )
    )
)
```

Descrição: Lucro acumulado no intervalo visível de datas.  
Uso: Storytelling de acumulação e contribuição de lucro.

## Metas

### 27. Sales Target

```DAX
Sales Target =
SUM ( fact_targets[SalesTargetAmount] )
```

Descrição: Valor planejado de vendas vindo da tabela de metas.  
Uso: Cards de KPI, bullet charts e visuais de acompanhamento de meta.

### 28. Sales vs Target Variance

```DAX
Sales vs Target Variance =
[Total Sales] - [Sales Target]
```

Descrição: Gap absoluto entre vendas realizadas e meta.  
Uso: Cards executivos e barras de variância.

### 29. Target Attainment %

```DAX
Target Attainment % =
DIVIDE ( [Total Sales], [Sales Target] )
```

Descrição: Performance realizada como percentual da meta.  
Uso: Cards de KPI, formatação condicional e revisão de tendência.

### 30. Sales vs Target Variance %

```DAX
Sales vs Target Variance % =
DIVIDE ( [Sales vs Target Variance], [Sales Target] )
```

Descrição: Variância relativa em relação ao plano.  
Uso: Comentário executivo sobre meta e comparação regional.

## Ranking e Contribuição

### 31. % of Total Sales

```DAX
% of Total Sales =
DIVIDE (
    [Total Sales],
    CALCULATE (
        [Total Sales],
        REMOVEFILTERS ( dim_product ),
        REMOVEFILTERS ( dim_customer ),
        REMOVEFILTERS ( dim_geography ),
        REMOVEFILTERS ( dim_region ),
        REMOVEFILTERS ( dim_channel ),
        REMOVEFILTERS ( dim_sales_rep )
    )
)
```

Descrição: Participação da venda dentro do contexto atual de data.  
Uso: Barras de contribuição, matrizes e análises estilo Pareto.

### 32. % of Total Profit

```DAX
% of Total Profit =
DIVIDE (
    [Total Profit],
    CALCULATE (
        [Total Profit],
        REMOVEFILTERS ( dim_product ),
        REMOVEFILTERS ( dim_customer ),
        REMOVEFILTERS ( dim_geography ),
        REMOVEFILTERS ( dim_region ),
        REMOVEFILTERS ( dim_channel ),
        REMOVEFILTERS ( dim_sales_rep )
    )
)
```

Descrição: Participação do lucro dentro do contexto atual de data.  
Uso: Análise de concentração de lucro e leitura de mix.

### 33. Rank Region by Sales

```DAX
Rank Region by Sales =
RANKX ( ALL ( dim_region[Region] ), [Total Sales], , DESC, DENSE )
```

Descrição: Ranking de vendas entre regiões.  
Uso: Tabelas comparativas por região e formatação condicional.

### 34. Rank Category by Profit

```DAX
Rank Category by Profit =
RANKX ( ALL ( dim_product[Category] ), [Total Profit], , DESC, DENSE )
```

Descrição: Ranking de lucro entre categorias.  
Uso: Scorecards de categoria e matrizes de lucratividade.
