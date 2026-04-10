# Handoff Final do Dashboard

## Resumo da Auditoria

### O que já está pronto

- datasets de vendas e metas reproduzíveis
- CSVs em star schema dentro de `data/processed/`
- biblioteca DAX em `docs/dax-measures.md`
- documentação de modelo em `docs/data-model.md`
- direção visual em `docs/dashboard-blueprint.md`
- tema em `assets/theme/sales-performance-theme.json`

### O que este handoff fecha

- previews das páginas do dashboard gerados com os dados reais
- guia exato de montagem no Power BI Desktop
- padronização final dos nomes das screenshots no README

## Arquivos Fonte de Verdade

- `README.md`
- `docs/data-model.md`
- `docs/dax-measures.md`
- `docs/dashboard-blueprint.md`
- `docs/design-decisions.md`
- `docs/page-by-page-kpi-map.md`
- `assets/theme/sales-performance-theme.json`
- `screenshots/README.md`

## Datasets a Importar

Use as tabelas processed em `data/processed/`:

- `dim_date.csv`
- `dim_product.csv`
- `dim_customer.csv`
- `dim_geography.csv`
- `dim_region.csv`
- `dim_channel.csv`
- `dim_sales_rep.csv`
- `fact_sales.csv`
- `fact_targets.csv`

## Configuração do Modelo

### Nomes das Tabelas

Renomeie as tabelas no Power BI exatamente para:

- `dim_date`
- `dim_product`
- `dim_customer`
- `dim_geography`
- `dim_region`
- `dim_channel`
- `dim_sales_rep`
- `fact_sales`
- `fact_targets`

### Relacionamentos Obrigatórios

Siga `docs/data-model.md`. Pontos principais:

- `dim_date[DateKey]` com `fact_sales[OrderDateKey]` como relacionamento ativo
- `dim_date[DateKey]` com `fact_sales[ShipDateKey]` como relacionamento inativo
- `dim_date[DateKey]` com `fact_targets[DateKey]` como relacionamento ativo
- `dim_region[RegionKey]` ligado a `fact_sales[RegionKey]` e `fact_targets[RegionKey]`
- `dim_channel[ChannelKey]` ligado a `fact_sales[ChannelKey]` e `fact_targets[ChannelKey]`

### Configuração Obrigatória da Tabela de Datas

- marcar `dim_date[Date]` como tabela de datas
- ordenar `dim_date[Month Name]` por `dim_date[Month Number]`

## Padrões Visuais

- canvas em `16:9`
- fundo `#F7F6F3`
- cor principal `#123B5D`
- cor positiva `#2C6E49`
- cor negativa `#D1495B`
- cor de apoio `#7C8EA3`
- uma faixa de KPIs no topo de cada página
- slicers horizontais quando fizer sentido

## Especificação das Páginas

## 1. Visão Executiva

### KPIs

- Total Sales
- Total Profit
- Profit Margin %
- Total Orders
- Average Order Value
- Return Rate %
- Target Attainment %

### Visuais

- gráfico de linha com `dim_date[Date]` e as medidas `Total Sales` e `Total Profit`
- gráfico de linha com `dim_date[Date]`, `Total Sales` e `Sales Target`
- barra horizontal com `dim_region[Region]` por `Total Sales`
- barra horizontal com `dim_product[Category]` por `Total Sales`

### Slicers

- Data
- Região
- Canal de Vendas
- Categoria

## 2. Análise de Vendas

### KPIs

- Total Sales
- Total Orders
- Average Order Value
- Total Quantity

### Visuais

- linha ou área para `Total Sales` por mês
- coluna empilhada ou área por mês com `Total Sales` por `dim_channel[SalesChannel]`
- barra horizontal de `dim_product[Category]` por `Total Sales`
- barra horizontal de `dim_product[SubCategory]` por `Total Sales`
- barra horizontal de `dim_region[Region]` por `Total Sales`
- matrix ou heatmap com região x canal usando `Total Sales`

### Slicers

- Data
- Região
- Canal de Vendas
- Segmento

## 3. Análise de Lucratividade

### KPIs

- Total Profit
- Profit Margin %
- Discount %
- Profit per Order

### Visuais

- barra horizontal de `dim_product[Category]` por `Profit Margin %`
- scatter com `Total Sales` no eixo X e `Total Profit` no eixo Y por `dim_product[SubCategory]`
- scatter com `Discount %` no eixo X e `Profit Margin %` no eixo Y por `dim_product[SubCategory]`
- barra horizontal de produtos com menor margem
- barra horizontal de `dim_channel[SalesChannel]` por `Total Profit`
- barra horizontal de `dim_region[Region]` por `Profit Margin %`

### Slicers

- Data
- Região
- Categoria
- Canal de Vendas

## 4. Insights de Clientes e Produtos

### KPIs

- Total Customers
- Sales per Customer
- Top 10 Product Share %
- Enterprise Sales YoY %

### Visuais

- gráfico de barras agrupadas por `dim_customer[Segment]` com `Total Sales` e `Total Profit`
- barra horizontal de crescimento por segmento com `Sales YoY %`
- barra horizontal dos principais produtos por `Total Sales`
- barra horizontal dos principais produtos por `Total Profit`
- linha de concentração acumulada com `% of Total Sales`

### Slicers

- Data
- Segmento
- Categoria
- Região

## 5. Performance Geográfica e de Canais

### KPIs

- Total Sales
- Total Profit
- Profit Margin %
- Profit per Order

### Visuais

- barra horizontal de `dim_region[Region]` por `Total Sales`
- barra horizontal de `dim_region[Region]` por `Profit Margin %`
- barra horizontal de `dim_channel[SalesChannel]` por `% of Total Sales`
- matrix ou heatmap de região x canal com `Total Sales`
- matrix ou heatmap de região x canal com `Profit Margin %`
- barra horizontal de `dim_channel[SalesChannel]` por `Profit per Order`

### Slicers

- Data
- Região
- Canal de Vendas
- Segmento

## 6. Metas e Tendências

### KPIs

- Sales Target
- Target Attainment %
- Sales vs Target Variance
- Sales YoY %
- Profit YoY %

### Visuais

- linha mensal com `Total Sales` vs `Sales Target`
- gráfico de colunas com `Sales vs Target Variance`
- barra horizontal de `dim_region[Region]` por `Target Attainment %`
- barra horizontal de `dim_channel[SalesChannel]` por `Target Attainment %`
- linha mensal com `Sales YoY %` e `Profit YoY %`
- matrix ou heatmap com vendas mensais de 2025 por região

### Slicers

- Data
- Região
- Canal de Vendas

## Regras de Interação

- sincronizar slicers apenas quando a comparação ficar mais clara, especialmente Data e Região
- desabilitar cross-highlighting onde ele gerar ruído visual
- deixar visuais mais detalhados na metade inferior de cada página
- usar `dim_region` em páginas sensíveis a metas, em vez de `dim_geography`

## Fluxo das Screenshots

As screenshots nativas exportadas do Power BI devem usar estes nomes:

1. `screenshots/01-executive-overview.png`
2. `screenshots/02-sales-analysis.png`
3. `screenshots/03-profitability-analysis.png`
4. `screenshots/04-customer-product-insights.png`
5. `screenshots/05-geography-channel-performance.png`
6. `screenshots/06-targets-trends.png`

## Próximo Passo Nativo no Power BI

O próximo passo é manual dentro do Power BI Desktop:

1. importar os CSVs de `data/processed/`
2. criar os relacionamentos do modelo
3. aplicar o tema
4. inserir as medidas DAX
5. montar as 6 páginas finais
6. exportar as 6 screenshots nativas
7. substituir os previews atuais pelos exports do Desktop

Quando isso estiver concluído de verdade, o commit correto será:

`feat(report): add final Power BI dashboard pages and native screenshots`

## Limitação Prática

O Power BI Desktop está instalado na máquina, mas o canvas do relatório não pôde ser montado programaticamente pelo terminal. Por isso, este repositório inclui:

- guia exato para a montagem do arquivo no Desktop
- seis previews estáticos do dashboard gerados com os dados reais

Esses previews podem ser substituídos diretamente pelas screenshots nativas depois da montagem final.

Isso também está alinhado ao comportamento atual documentado pela Microsoft: a conversão de PBIX para PBIP e a criação de PBIR dependem do fluxo do próprio Power BI Desktop e não de um processo suportado apenas via terminal.
