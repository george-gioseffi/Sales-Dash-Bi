# Blueprint do Dashboard

O relatório foi desenhado como uma experiência executiva de analytics com seis páginas principais e uma página opcional de metodologia. A direção visual é propositalmente corporativa, contida e orientada à decisão, em vez de decorativa.

## Princípios Globais de Design

- Usar um canvas claro em off-white para manter o relatório limpo e bom para apresentação.
- Reservar o azul navy profundo para as métricas mais importantes e para a estrutura visual.
- Usar verde discreto para desempenho favorável e vermelho controlado para variações negativas.
- Evitar gauges desnecessários, excesso de pizza, bordas pesadas ou visuais sem valor analítico.
- Limitar slicers aos controles realmente úteis para o negócio: data, região, canal, categoria e segmento.

## Página 1. Visão Executiva

Propósito: Entregar a história completa do negócio em menos de 20 segundos.  
Público-alvo: Executivos, recrutadores e patrocinadores do negócio.  
Visuais recomendados:

- Cards de KPI para Total Sales, Total Profit, Profit Margin %, Total Orders, Average Order Value, Return Rate %, e Sales vs Target Variance
- Gráfico de linha mensal para Sales e Profit
- Barra por região ranqueada por Total Sales
- Barra ou treemap de contribuição por categoria
- Card compacto ou bullet chart de atingimento de meta

Filtros essenciais:

- Data
- Região
- Canal de Vendas
- Categoria

Leitura-chave: O usuário deve enxergar rapidamente o tamanho do negócio, se a performance está saudável e onde está o principal motor de receita.

## Página 2. Análise de Vendas

Propósito: Explicar o que está puxando a receita.  
Público-alvo: Gestores comerciais e operações de vendas.  
Visuais recomendados:

- Tendência mensal de vendas
- Coluna empilhada por canal ao longo do tempo
- Barras de ranking por categoria e subcategoria
- Matrix região x canal
- Cards de volume de pedidos e ticket médio

Filtros essenciais:

- Data
- Região
- Canal de Vendas
- Segmento

Leitura-chave: Receita deve ser entendida como uma composição de drivers de produto, geografia e canal, e não apenas como um total agregado.

## Página 3. Análise de Lucratividade

Propósito: Mostrar que vender muito não significa necessariamente ter receita de qualidade.  
Público-alvo: Finanças parceiras do negócio e liderança comercial.  
Visuais recomendados:

- Faixa de KPIs de lucro e margem
- Barras de margem por categoria e subcategoria
- Scatter com Sales no eixo X e Profit no eixo Y por produto ou subcategoria
- Comparação entre Discount % e Profit Margin %
- Tabela de produtos com baixo lucro e alto volume

Filtros essenciais:

- Data
- Região
- Categoria
- Canal de Vendas

Leitura-chave: O relatório deve evidenciar onde desconto, preço ou mix estão corroendo lucratividade.

## Página 4. Insights de Clientes e Produtos

Propósito: Entender mix de segmentos, concentração e contribuição de produtos.  
Público-alvo: Estratégia comercial e gestão de categorias.  
Visuais recomendados:

- Participação de segmento por vendas
- Crescimento de segmento versus ano anterior
- Top produtos por vendas
- Top produtos por lucro
- Visão estilo Pareto mostrando concentração

Filtros essenciais:

- Data
- Segmento
- Categoria
- Região

Leitura-chave: Nem todo crescimento é equilibrado; um conjunto limitado de produtos e segmentos pode dominar o mix do negócio.

## Página 5. Performance Geográfica e de Canais

Propósito: Comparar qualidade de execução entre regiões e canais.  
Público-alvo: Liderança regional e times de planejamento comercial.  
Visuais recomendados:

- Ranking de região por vendas
- Ranking de região por margem
- Gráfico de contribuição por canal
- Heatmap ou matrix região x canal
- Mapa apenas se permanecer claro e agregar valor real

Filtros essenciais:

- Data
- Região
- Canal de Vendas
- Segmento

Leitura-chave: Escala regional e eficiência de canal precisam aparecer lado a lado, não em análises separadas.

## Página 6. Metas e Tendências

Propósito: Acompanhar aderência ao plano e momento do negócio ao longo do tempo.  
Público-alvo: Liderança e times de planejamento.  
Visuais recomendados:

- Linha mensal de realizado versus meta
- KPI de Target Attainment %
- Barras de variância por região ou canal
- Cards de MoM e YoY
- Pequenos múltiplos ou tendência por região

Filtros essenciais:

- Data
- Região
- Canal de Vendas

Leitura-chave: A liderança deve entender se a meta está sendo perdida por um ponto isolado ou por um padrão mais amplo de execução.

## Página 7. Metodologia

Propósito: Deixar o case pronto para entrevista e autoexplicativo para quem navega pelo GitHub.  
Público-alvo: Recrutadores, professores e revisores técnicos.  
Visuais recomendados:

- Bloco curto de contexto de negócio
- Diagrama simplificado do star schema
- Cards com definição de KPIs
- Painel de premissas e limitações

Leitura-chave: O relatório deve provar não apenas habilidade visual, mas também disciplina analítica.
