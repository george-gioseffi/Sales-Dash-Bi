# Lógica de Geração dos Dados

## Visão Geral

O dataset é sintético, mas foi projetado para parecer plausível em contexto empresarial. A geração usa seeds fixas para manter a reprodutibilidade e, ao mesmo tempo, preservar um comportamento comercial consistente ao longo do tempo, entre regiões, canais e mix de produtos.

Scripts principais:

- `scripts/generate_sales_dataset.py`
- `scripts/build_targets_table.py`
- `scripts/build_star_schema.py`
- `scripts/run_full_build.py`

## Intervalo Temporal

- Cobertura: 1 de janeiro de 2024 a 31 de dezembro de 2025
- Granularidade: linhas transacionais de venda
- Horizonte analítico: 24 meses completos para suportar análises YoY e MoM

## Lógica Comercial Embutida

### Sazonalidade

- Novembro e dezembro foram modelados como meses mais fortes de receita.
- Fevereiro e o meio do ano tendem a ser períodos um pouco mais fracos.
- Foi aplicado um fator moderado de crescimento em 2025 para simular expansão ano contra ano.

### Contraste Regional

- `Southeast` concentra o maior peso de vendas e a pressão de preço mais agressiva.
- `South` aparece como mercado secundário forte, com boa receita e margem estável.
- `Northeast`, `Midwest` e `North` têm menor volume, mas com perfis distintos de margem e meta.

### Comportamento por Canal

- `Online` concentra maior volume de pedidos e maior taxa de devolução.
- `Retail Stores` equilibram volume e margem com desconto mais moderado.
- `Distributors` movimentam quantidades maiores, mas absorvem maior pressão de desconto.
- `Direct Sales` gera menos volume total do que Online, porém entrega melhor margem e maior lucro por pedido.

### Economia de Produto

- Produtos de tecnologia concentram a maior contribuição de receita, especialmente laptops e monitores.
- Impressoras e mesas foram modeladas com economia mais apertada e maior sensibilidade a desconto.
- Subcategorias de suprimentos de escritório têm ticket menor, mas margem estruturalmente mais saudável.

### Relação Entre Desconto e Margem

- Os descontos não são aleatórios. Eles variam por região, canal, segmento, sazonalidade e sensibilidade de produto.
- Linhas com maior desconto preservam a base de custo original, o que naturalmente comprime a margem.
- Isso permite analisar se o crescimento de topline está sendo comprado às custas de lucratividade.

### Metas

- As metas ficam em tabela separada no grão `mês x região x canal de vendas`.
- Elas foram calibradas com base no run-rate real, combinando fatores de stretch por região, canal e sazonalidade.
- O resultado é um atingimento médio próximo ao plano, com combinações acima e abaixo da meta, sem perfeição artificial.

## Reprodutibilidade

- Seed aleatória: `42`
- Comando para rebuild:

```bash
python scripts/run_full_build.py
```
