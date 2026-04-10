# Dicionário de Dados

## Tabelas Raw

### `sales_transactions.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| Order ID | texto | Identificador único do pedido no nível de cabeçalho |
| Order Line Number | inteiro | Número da linha dentro do pedido |
| Order Date | data | Data da transação usada como calendário principal do relatório |
| Ship Date | data | Data de expedição, disponível para análise logística |
| Customer ID | texto | Chave natural do cliente |
| Customer Name | texto | Nome de exibição do cliente |
| Segment | texto | Segmento do cliente: Consumer, Small Business ou Enterprise |
| Country | texto | Nome do país |
| Region | texto | Região comercial |
| State | texto | Sigla do estado |
| City | texto | Nome da cidade |
| Product ID | texto | Chave natural do produto |
| Product Name | texto | Nome de exibição do produto |
| Category | texto | Categoria principal de produto |
| Sub-Category | texto | Subcategoria de produto |
| Sales Amount | decimal | Venda líquida após desconto |
| Quantity | inteiro | Unidades vendidas na linha |
| Unit Price | decimal | Preço de venda antes da multiplicação pela quantidade |
| Gross Sales Amount | decimal | Venda bruta antes do desconto |
| Discount | decimal | Percentual de desconto aplicado na linha |
| Discount Amount | decimal | Valor concedido em desconto |
| Cost | decimal | Valor estimado de custo da linha |
| Profit | decimal | Venda menos custo |
| Sales Channel | texto | Canal usado na venda |
| Sales Rep | texto | Representante comercial responsável |
| Returned Flag | inteiro | Indicador binário de devolução |

### `monthly_targets.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| Target Month | data | Primeiro dia do mês da meta |
| Region | texto | Atribuição regional da meta |
| Sales Channel | texto | Atribuição da meta por canal |
| Sales Target | decimal | Valor da meta mensal de vendas |

### `customers_master.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| Customer ID | texto | Chave do cliente |
| Customer Name | texto | Nome do cliente |
| Segment | texto | Segmento de negócio |
| Country | texto | País |
| Region | texto | Região de origem |
| State | texto | Estado de origem |
| City | texto | Cidade de origem |

### `products_master.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| Product ID | texto | Chave do produto |
| Product Name | texto | Nome do produto |
| Category | texto | Categoria do produto |
| Sub-Category | texto | Subcategoria do produto |
| Base Price | decimal | Preço-base sintético usado na geração |
| Base Cost Ratio | decimal | Perfil-base de custo usado na geração |
| Discount Sensitivity | decimal | Sensibilidade relativa a cortes de preço |
| Demand Weight | decimal | Frequência relativa na geração de transações |
| Quantity Base | decimal | Perfil-base de quantidade |
| Return Bias | decimal | Tendência específica de devolução do produto |

### `channels_master.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| Sales Channel | texto | Nome do canal |
| Volume Weight | decimal | Peso relativo de alocação de pedidos |
| Discount Bias | decimal | Pressão de desconto específica do canal |
| Cost Bias | decimal | Ajuste de custo específico do canal |
| Return Bias | decimal | Tendência de devolução específica do canal |
| Lead Days | decimal | Prazo médio de expedição em dias |

### `sales_reps_master.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| Sales Rep | texto | Nome do representante comercial |
| Home Region | texto | Região principal de atuação |

## Tabelas do Modelo Processed

### `fact_sales.csv`

Cada linha representa um item de pedido no grão `pedido x produto x data do pedido`.

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| SalesKey | inteiro | Chave substituta da linha |
| OrderID | texto | Identificador do pedido |
| OrderLineNumber | inteiro | Posição da linha dentro do pedido |
| OrderDateKey | inteiro | Chave ativa de data |
| ShipDateKey | inteiro | Chave inativa da data de envio |
| CustomerKey | inteiro | Ligação com `dim_customer` |
| GeographyKey | inteiro | Ligação com `dim_geography` |
| RegionKey | inteiro | Ligação com `dim_region` para alinhamento regional das metas |
| ProductKey | inteiro | Ligação com `dim_product` |
| ChannelKey | inteiro | Ligação com `dim_channel` |
| SalesRepKey | inteiro | Ligação com `dim_sales_rep` |
| SalesAmount | decimal | Venda líquida |
| GrossSalesAmount | decimal | Venda bruta antes do desconto |
| DiscountAmount | decimal | Valor do desconto |
| DiscountPct | decimal | Percentual de desconto |
| Quantity | inteiro | Unidades vendidas |
| UnitPrice | decimal | Preço unitário de venda |
| CostAmount | decimal | Valor de custo |
| ProfitAmount | decimal | Valor de lucro |
| ReturnedFlag | inteiro | Indicador de devolução |

### `fact_targets.csv`

Cada linha representa uma meta mensal no grão `mês x região x canal`.

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| TargetKey | inteiro | Chave substituta |
| DateKey | inteiro | Ligação com `dim_date` |
| RegionKey | inteiro | Ligação com `dim_region` |
| ChannelKey | inteiro | Ligação com `dim_channel` |
| SalesTargetAmount | decimal | Valor mensal da meta de vendas |

### `dim_date.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| DateKey | inteiro | Chave substituta no formato `YYYYMMDD` |
| Date | data | Data do calendário |
| Year | inteiro | Ano calendário |
| Quarter | texto | Rótulo do trimestre |
| Month Number | inteiro | Número do mês para ordenação |
| Month Name | texto | Nome do mês para exibição |
| Year-Month | texto | Rótulo no grão de mês |
| Week Number | inteiro | Semana ISO |
| Is Current Year | inteiro | Flag para o maior ano do dataset |

### `dim_product.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| ProductKey | inteiro | Chave substituta |
| ProductID | texto | Identificador natural do produto |
| ProductName | texto | Nome do produto |
| Category | texto | Categoria |
| SubCategory | texto | Subcategoria |

### `dim_customer.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| CustomerKey | inteiro | Chave substituta |
| CustomerID | texto | Identificador natural do cliente |
| CustomerName | texto | Nome do cliente |
| Segment | texto | Segmento do cliente |
| GeographyKey | inteiro | Chave da geografia de origem |

### `dim_geography.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| GeographyKey | inteiro | Chave substituta |
| Country | texto | País |
| Region | texto | Região |
| State | texto | Estado |
| City | texto | Cidade |

### `dim_region.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| RegionKey | inteiro | Chave substituta |
| Country | texto | País |
| Region | texto | Região |

### `dim_channel.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| ChannelKey | inteiro | Chave substituta |
| SalesChannel | texto | Nome do canal |

### `dim_sales_rep.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| SalesRepKey | inteiro | Chave substituta |
| SalesRep | texto | Representante comercial |
| HomeRegion | texto | Região-base do representante |
