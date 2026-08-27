# Insights Ocultos — Aurora Brasil Exportadora S.A.

Este documento registra os padrões implantados **deliberadamente** durante a geração da base
(`generate_data.py`). Ele não deve ser consultado antes de uma primeira análise exploratória do
dashboard — sirva-se dele apenas para conferir suas próprias descobertas (ver
`InsightsEncontrados.md` para a versão redigida a partir da análise, sem olhar este arquivo
primeiro).

## I1 — Cliente importante em queda

**Kingsmere Imports Ltd** (Reino Unido) tem receita anual (USD): 2022 ≈ 6,77M → 2023 ≈ 4,66M →
2024 ≈ 6,12M (recuperação) → 2025 ≈ 6,45M (estabilidade) → 2026 YTD ≈ 2,29M, projetando uma queda
de aproximadamente 30–40% no ano. Visível na tabela "Carteira detalhada" da página *Customers* e
no drill-through *Detalhe Cliente*.

## I2 / I19 — Margem sendo corroída (Cacau)

A categoria **Cacau** aumenta receita nominal ao longo do período, mas sua margem percentual cai
de forma progressiva: 25,0% (2022) → 20,0% (2023) → 11,7% (2024) → 9,4% (2025), com recuperação
parcial em 2026 (≈15,6%) quando o índice de custo da categoria recua. Visível na página
*Profitability* (ponte por categoria) e em *Products* (matriz BCG adaptada, onde Cacau aparece com
crescimento positivo e margem baixa).

## I3 — Vendedor dependente de um cliente

**Isabela Marchetti Rangel** tem 43,7% de sua receita concentrada em um único cliente
(**Rheinquell Lebensmittel GmbH**). Outros casos semelhantes (>30% em um cliente): Gustavo
Peixoto Andrade (33,8%), Thiago Bandeira Cordeiro (33,0%), Aline Furtado Bezerra (54,7%) e Rafael
Monteiro Lacerda (61,2%, sobre carteira pequena). Visível na medida `Concentracao Carteira
Vendedor`, página *Sales Team*.

## I4 — Mercado emergente

**Coreia do Sul**: receita de US$ 0,69M (2022) para US$ 4,03M (2025) e US$ 2,85M já no YTD de
2026 — crescimento consistente ano a ano desde 2023. Visível no mapa e no ranking de países da
página *Markets*.

## I5 — Problema logístico (rota crítica)

A rota **Santos → Jebel Ali (Emirados Árabes Unidos)** apresenta 45,1% de embarques atrasados,
quase três vezes a média geral de 16,6%. Rotas secundárias também acima da média: Israel (21,5%)
e Portugal (19,2%). Visível no gráfico "Rotas com maior incidência de atraso" da página
*Logistics*.

## I6 — Câmbio favorável

A taxa USD/BRL sobe de forma sustentada entre 2024 e o fim de 2025 (pico de 6,12 em dez/2025),
favorecendo a receita convertida em BRL mesmo em períodos de crescimento operacional mais fraco.
Visível na medida `Efeito Cambio BRL`, que isola esse componente do `Crescimento Operacional BRL`.

## I7 — Produto campeão

**Café Arábica Especial 25kg Caixa Master** combina peso crescente no mix, alta margem e demanda
resiliente ao longo do período — reforçado deliberadamente por peso de seleção crescente ano a
ano na geração de vendas. Visível na tabela de portfólio da página *Products*.

## I8 — Produto problemático

**Polpa de Açaí Congelada 60kg Saca Juta** tem receita relevante, mas margem estruturalmente
baixa (categoria Açaí é a segunda menor margem do portfólio) e frete por quilo 55% acima do
padrão da categoria (produto refrigerado). Visível cruzando *Products* (margem) com *Logistics*
(frete por kg).

## I9 — Churn (90 / 180 / 365 dias)

Quatro clientes relevantes ficam sem comprar por janelas específicas a partir de 2025:
**Kaneyama Trading Co., Ltd.** (90 dias, a partir de 12/04/2025), **Desert Pearl Import LLC**
(180 dias, a partir de 10/03/2025), **Silverfern Trading Ltd** e **Aurora Bay Foods Ltd.** (365
dias cada). Adicionalmente, oito clientes (entre eles Neve Shaked Import Ltd., Altmark
Lebensmittel GmbH e Silver Creek Trading LLC) encerram a relação definitivamente entre 2024 e
2025. Visível nas medidas `Clientes Perdidos`, `Clientes Em Risco` e `Receita em Risco`.

## I10 — Sazonalidade

Cada categoria tem um pico de demanda claramente diferente: Açaí pico em dez–jan (verão),
Café pico em set–out, Castanhas pico em out–nov, Mel pico em nov–dez, Produtos Naturais mais
estável ao ano todo. Visível no gráfico "Peso histórico de cada mês" da página *Forecast &
Budget* (medida `Sazonalidade Historica %`).

## I11 — Concentração de receita

Os 10 maiores clientes (entre eles as contas de IDs 76, 220, 281, 158, 84, 89, 28, 10, 190 e 126,
reforçadas com um multiplicador de receita na geração) respondem por 32,3% da receita total; os
6 maiores tiveram a base multiplicada por ~2,05× deliberadamente. Visível nas medidas
`Participacao Top 5/10/20` e no gráfico de Pareto da página *Customers*.

## I12 — Clientes menores altamente rentáveis

Nem toda receita alta implica margem alta: cruzando `Receita USD` com `Margem Bruta %` no
scatter de clientes da página *Profitability*, aparecem contas pequenas com margem acima de 35%
ao lado de contas grandes com margem abaixo de 20% — resultado direto de diferentes perfis de
desconto (`desc_perfil`) atribuídos por cliente na geração.

## I13 — Food Service com desconto agressivo

Clientes do tipo **Food Service** têm desconto médio de 15,1% (o maior entre os sete tipos de
cliente) e a menor margem percentual (23,8%), resultado de um acréscimo deliberado de +5 p.p. no
perfil de desconto desse segmento. Visível cruzando `Desconto %` e `Margem Bruta %` por
`TipoCliente`.

## I14 — Aumento repentino de custo/frete (anomalia rara)

Choque logístico entre outubro/2024 e janeiro/2025: custo de frete por quilo sobe 38% nesse
intervalo específico, visível como um pico isolado na série `Frete por Kg` ao longo do tempo.

## I15 — Mercado em retração

**Argentina** cai de forma consistente: US$ 1,34M (2022) → US$ 1,59M (2025) → US$ 0,74M (YTD
2026), refletindo risco-país elevado e o cenário macro regional simulado. Visível no ranking de
países com pior crescimento YoY.

## I16 — Margem negativa pontual

Aproximadamente 5,2% das linhas de `fVendas` apresentam margem bruta negativa, concentradas em
transações com desconto excepcional (anomalia de 0,7% de probabilidade, 12–20 p.p. extras de
desconto) combinadas a frete elevado. Visível filtrando `Margem Bruta USD < 0` em uma tabela
detalhada.

## I17 — Clientes inadimplentes

6% dos clientes têm perfil "Inadimplente" (atraso médio de pagamento acima de 250 dias),
responsáveis por boa parte do `Saldo Vencido +90` na página *Finance*. A inadimplência agregada
da carteira é de 1,56% do total a receber.

## I18 — Grupo "só café" (white space)

Doze clientes (entre eles Portofelice Alimentari S.r.l., Redwood Commodities Inc. e Nordvik
Trading AB) compram exclusivamente a categoria Café, apesar de perfis de porte que sugeririam
capacidade de compra em outras categorias — oportunidade clara de cross-sell, visível na medida
`White Space Categorias` cruzada com `Score de Oportunidade`.

## I19 — Ver I2 (mesmo padrão, categoria Cacau)

## I20 — Vendedor que cresce descontando

**Thiago Bandeira Cordeiro** tem o maior desconto médio da equipe (18,0%) e ainda assim mantém
crescimento de receita acima da média — um padrão de "crescimento comprado" que deveria acender
alerta em uma revisão de política comercial. Visível cruzando `Desconto %` e `Receita YoY %` por
vendedor na página *Sales Team*.

## Padrões adicionais implícitos na estrutura da base

- **Produtos descontinuados** (6 SKUs) perdem peso de mix a partir de 2024 e somem quase
  completamente do sortimento em 2025–2026.
- **Produtos novos** (7 SKUs) só ganham peso relevante de venda a partir de 2025, simulando ramp-up
  de lançamento.
- **Cohorts de aquisição**: 42% da carteira é "legada" (cadastrada antes de 2022), com o restante
  distribuído em ondas anuais até 2026 — permite análise de retenção por safra de aquisição.
- **Vendedor inativo**: Marcelo Duarte Siqueira aparece como desligado (`Status = Inativo`) em
  `dVendedor`, mantendo o histórico de vendas anterior ao desligamento intacto.
