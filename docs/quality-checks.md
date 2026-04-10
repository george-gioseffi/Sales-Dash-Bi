# Checagens de Qualidade

As validações abaixo foram usadas para confirmar a qualidade dos dados gerados antes da documentação do dashboard.

## Checagens Estruturais

| Checagem | Resultado |
| --- | --- |
| Linhas de vendas transacionais | 9.586 |
| Pedidos distintos | 4.407 |
| Clientes distintos | 257 |
| Produtos distintos | 28 |
| Regiões distintas | 5 |
| Canais distintos | 4 |
| Linhas de metas mensais | 480 |
| Linhas de calendário | 731 |

## Resultados de Validação

| Validação | Resultado |
| --- | --- |
| Scan de nulos em colunas-chave de vendas | Aprovado: 0 nulos |
| Scan de nulos em colunas de valores | Aprovado: 0 nulos |
| Validação de intervalo de datas | Aprovado: 2024-01-01 a 2025-12-31 |
| Ship date anterior ao order date | Aprovado: 0 linhas |
| Valores negativos de venda | Aprovado: 0 linhas |
| Valores negativos de custo | Aprovado: 0 linhas |
| Gross sales menor do que net sales | Aprovado: 0 linhas |
| Checagem de consistência de lucro (`Sales - Cost = Profit`) | Aprovado: 100% das linhas dentro da tolerância |
| Completude de metas por mês-região-canal | Aprovado: 480 de 480 linhas esperadas |

## Checagens de Sanidade de Negócio

- O crescimento de vendas de 2024 para 2025 é positivo, mas não exagerado: `+12,99%`
- O crescimento do lucro é positivo, porém mais lento do que o crescimento das vendas: `+10,20%`
- A margem caiu de `25,07%` para `24,45%`, criando uma discussão crível sobre preço e mix
- O atingimento médio da meta ficou em `98,18%`, com combinações acima e abaixo do plano
- A taxa de devolução é baixa, mas não zero, `1,74%`, com `Online` mostrando a maior pressão operacional
