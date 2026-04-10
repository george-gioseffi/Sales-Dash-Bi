# Racional de Modelagem

## Por Que Usar Star Schema

O relatório foi pensado para sustentar storytelling executivo e discussão técnica em entrevista. O star schema mantém o modelo semântico legível, melhora o comportamento das medidas e evita a ambiguidade comum quando muitas colunas descritivas vivem dentro de uma única fato larga.

## Por Que Separar Vendas e Metas

Vendas e metas operam em grãos diferentes e não devem ficar misturadas na mesma tabela. Vendas são transacionais; metas são dados mensais de planejamento. Mantê-las separadas preserva precisão, simplifica medidas de variância e espelha a forma como dados de planejamento costumam ser tratados em modelos reais.

## Por Que Adicionar `dim_region`

`dim_geography` é útil para análises por estado e cidade, mas as metas existem no nível de região. Adicionar `dim_region` evita duplicação de meta e cria uma camada executiva mais limpa para comparação regional.

## Por Que Manter Order Date e Ship Date

Order date é a linha do tempo analítica principal, enquanto ship date abre espaço para análises futuras de logística e entrega. Modelar os dois desde o início melhora a extensibilidade sem complicar a primeira versão do dashboard.
