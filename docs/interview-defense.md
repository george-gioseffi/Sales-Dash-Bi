# Defesa para Entrevista

## Por que você usou star schema?

Porque o relatório combina vendas transacionais com metas mensais. Um star schema deixa o modelo mais fácil de entender, melhora o comportamento das medidas DAX e escala melhor do que uma única tabela larga e desnormalizada.

## Por que separar vendas e metas?

Porque são processos de negócio com grãos diferentes. Vendas são transacionais no nível de linha de pedido, enquanto metas são dados mensais de planejamento por região e canal. Separar as duas preserva a precisão analítica.

## Por que focar em profit margin e não só em receita?

Porque receita sozinha pode esconder crescimento ineficiente. Neste projeto, algumas subcategorias de alto volume, como printers e tables, geram vendas relevantes, mas performam mal em margem. É exatamente esse tipo de problema que a liderança precisa enxergar.

## Por que você escolheu esses visuais?

Priorizei visuais que respondem perguntas de negócio com rapidez: cards para resumo executivo, linhas para tendência, barras para ranking e scatter para a relação entre sales e profit. Cada gráfico tem uma função de decisão.

## Que decisões esse dashboard ajuda a tomar?

Ele apoia revisão de preços, alocação de foco regional, priorização de canais, otimização de portfólio e gestão de metas. O modelo foi pensado para ajudar a liderança a decidir onde acelerar, onde proteger margem e onde intervir.

## Como você evoluiria este projeto?

Eu adicionaria cenários de budget e forecast, lógica de retenção de clientes, cotas por representante, cobertura de estoque e uma waterfall de lucratividade. Também empacotaria o relatório final em PBIP com metadados prontos para deploy.

## Por que adicionar uma dimensão separada de região?

Porque as metas existem no grão regional, enquanto a geografia de vendas vai até cidade e estado. Uma dimensão dedicada de região evita duplicação de meta e mantém a análise de realizado versus meta correta.
