# Modelo de Dados

## Abordagem de Modelagem

O modelo segue um star schema centrado em vendas transacionais e metas mensais. O objetivo principal é manter a lógica analítica simples, performática e fácil de explicar tanto em contexto técnico quanto em contexto de negócio.

## Tabelas Fato

| Tabela | Grão | Propósito |
| --- | --- | --- |
| `fact_sales` | Uma linha de pedido por produto por data do pedido | Análise principal de receita, volume, desconto, custo, lucro e devolução |
| `fact_targets` | Uma linha por mês, região e canal | Acompanhamento de metas e análise de variância |

### Declaração de Grão

- `fact_sales`: cada linha representa um item de venda no grão `pedido x produto x data do pedido`.
- `fact_targets`: cada linha representa uma meta mensal no grão `mês x região x canal de vendas`.

## Tabelas Dimensão

| Tabela | Chave Primária | Papel Principal |
| --- | --- | --- |
| `dim_date` | `DateKey` | Base compartilhada de inteligência temporal |
| `dim_product` | `ProductKey` | Análise de categoria, subcategoria e produto |
| `dim_customer` | `CustomerKey` | Análise de segmento e mix de clientes |
| `dim_geography` | `GeographyKey` | Corte por cidade e estado |
| `dim_region` | `RegionKey` | Alinhamento regional das metas e comparação executiva |
| `dim_channel` | `ChannelKey` | Análise de performance por canal |
| `dim_sales_rep` | `SalesRepKey` | Comparação por representante comercial |

## Relacionamentos

Relacionamentos recomendados no Power BI:

| De | Para | Cardinalidade | Status |
| --- | --- | --- | --- |
| `dim_date[DateKey]` | `fact_sales[OrderDateKey]` | 1:* | Ativo |
| `dim_date[DateKey]` | `fact_sales[ShipDateKey]` | 1:* | Inativo |
| `dim_date[DateKey]` | `fact_targets[DateKey]` | 1:* | Ativo |
| `dim_product[ProductKey]` | `fact_sales[ProductKey]` | 1:* | Ativo |
| `dim_customer[CustomerKey]` | `fact_sales[CustomerKey]` | 1:* | Ativo |
| `dim_geography[GeographyKey]` | `fact_sales[GeographyKey]` | 1:* | Ativo |
| `dim_region[RegionKey]` | `fact_sales[RegionKey]` | 1:* | Ativo |
| `dim_region[RegionKey]` | `fact_targets[RegionKey]` | 1:* | Ativo |
| `dim_channel[ChannelKey]` | `fact_sales[ChannelKey]` | 1:* | Ativo |
| `dim_channel[ChannelKey]` | `fact_targets[ChannelKey]` | 1:* | Ativo |
| `dim_sales_rep[SalesRepKey]` | `fact_sales[SalesRepKey]` | 1:* | Ativo |

## Premissas Analíticas

- `dim_date` deve ser marcada como a tabela oficial de datas usando `dim_date[Date]`.
- Em páginas com metas, os slicers regionais devem usar `dim_region`, e não `dim_geography`, para preservar o grão correto da meta.
- `ShipDateKey` existe para análises logísticas futuras, mas o relatório deve usar `OrderDateKey` como calendário ativo padrão.
- Devoluções são modeladas como flags operacionais, e não como transações totalmente revertidas.
