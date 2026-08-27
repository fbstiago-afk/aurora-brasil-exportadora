# Paginas do Dashboard — Aurora Brasil Exportadora S.A.

Formato 1280x720 (16:9). Navegacao lateral fixa via visual `pageNavigator`.

| # | Pagina | Tipo | Visuais |
|---|---|---|---|
| 1 | 01 Executive Overview | Relatorio | 19 |
| 2 | 02 Sales Performance | Relatorio | 14 |
| 3 | 03 Customers | Relatorio | 16 |
| 4 | 04 Customer Potential | Relatorio | 12 |
| 5 | 05 Products | Relatorio | 13 |
| 6 | 06 Markets | Relatorio | 12 |
| 7 | 07 Profitability | Relatorio | 13 |
| 8 | 08 Logistics | Relatorio | 14 |
| 9 | 09 Sales Team | Relatorio | 12 |
| 10 | 10 Finance | Relatorio | 13 |
| 11 | 11 Forecast e Budget | Relatorio | 12 |
| 12 | Tooltip Cliente | Tooltip | 2 |
| 13 | Tooltip Produto | Tooltip | 2 |
| 14 | Tooltip Pais | Tooltip | 2 |
| 15 | Tooltip Vendedor | Tooltip | 2 |
| 16 | Detalhe Cliente | Drillthrough | 11 |
| 17 | Detalhe Mercado | Drillthrough | 11 |

## Perguntas que cada pagina responde

### 01 Executive Overview

- card — ATINGIMENTO DA META
- card — CLIENTES ATIVOS
- card — MARGEM BRUTA
- card — OTIF LOGISTICO
- card — PEDIDOS FATURADOS
- card — RECEITA EM BRL
- card — RECEITA USD
- card — VOLUME EXPORTADO
- filledMap — Receita por mercado
- lineClusteredColumnComboChart — Receita mensal: realizado x ano anterior x meta
- pivotTable — Destaques por mercado
- slicer — Ano
- slicer — Continente
- textbox
- waterfallChart — De onde veio a variacao de receita YoY

### 02 Sales Performance

- card — GAP VERSUS META
- card — META
- card — PEDIDOS
- card — RECEITA
- card — TICKET MEDIO
- clusteredBarChart — Receita por executivo comercial
- clusteredBarChart — Regiao comercial: realizado x meta
- lineClusteredColumnComboChart — Realizado mensal e atingimento acumulado
- pivotTable — Decomposicao por canal e categoria
- slicer — Ano
- textbox

### 03 Customers

- card — CHURN
- card — CLIENTES ATIVOS
- card — NOVOS
- card — PERDIDOS
- card — REATIVADOS
- card — RECEITA EM RISCO
- clusteredBarChart — Distribuicao RFV da carteira
- clusteredBarChart — Receita por classe ABC
- lineChart — Clientes ativos por porte (base de cohort)
- lineClusteredColumnComboChart — Pareto de clientes
- pivotTable — Carteira detalhada — ordenar por recencia para achar risco
- slicer — Continente
- textbox

### 04 Customer Potential

- card — GAP NAO CAPTURADO
- card — POTENCIAL ESTIMADO
- card — RECEITA 12 MESES
- card — SHARE OF WALLET
- clusteredBarChart — Penetracao por categoria (clientes compradores)
- pivotTable — Ranking de oportunidade
- pivotTable — White space por segmento
- scatterChart — Receita x Share of Wallet — bolha = potencial
- textbox

### 05 Products

- card — MARGEM
- card — PRECO MEDIO/KG
- card — RECEITA
- card — VOLUME
- clusteredBarChart — Receita e margem por categoria
- lineChart — Evolucao da margem por categoria
- pivotTable — Portfolio por SKU
- scatterChart — Matriz BCG adaptada: crescimento x margem
- slicer — Categoria
- textbox

### 06 Markets

- card — CRESCIMENTO YOY
- card — MARGEM
- card — RECEITA EXPORTADA
- card — VOLUME
- clusteredBarChart — Ranking de mercados
- map — Distribuicao global da receita
- pivotTable — Mercado x categoria
- scatterChart — Market Opportunity Matrix
- textbox

### 07 Profitability

- card — CUSTO TOTAL
- card — DESCONTOS
- card — MARGEM %
- card — MARGEM BRUTA
- card — RECEITA BRUTA
- pivotTable — Ponte economica detalhada
- pivotTable — Rentabilidade por vendedor e Incoterm
- scatterChart — Cliente: receita x margem
- textbox
- waterfallChart — Formacao da margem por categoria

### 08 Logistics

- card — ATRASO MEDIO
- card — EMBARQUES ATRASADOS
- card — FRETE POR KG
- card — LEAD TIME REAL
- card — OTIF
- clusteredBarChart — Motivos de atraso
- clusteredBarChart — Performance por transportadora
- clusteredBarChart — Rotas com maior incidencia de atraso
- lineChart — Lead time real x previsto
- pivotTable — Modal e porto de origem
- textbox

### 09 Sales Team

- card — ATINGIMENTO MEDIO
- card — MARGEM
- card — NOVOS CLIENTES
- card — RECEITA DA EQUIPE
- clusteredBarChart — Dependencia do maior cliente da carteira
- clusteredBarChart — Realizado x meta por vendedor
- pivotTable — Ranking comercial
- scatterChart — Quadrante: crescimento x atingimento
- textbox

### 10 Finance

- card — CONTAS A RECEBER
- card — INADIMPLENCIA
- card — RECEBIDO
- card — SALDO EM ABERTO
- card — SALDO VENCIDO
- clusteredBarChart — Aging da carteira
- clusteredBarChart — Saldo vencido por forma de pagamento
- clusteredBarChart — Situacao dos titulos
- pivotTable — Principais devedores
- textbox

### 11 Forecast e Budget

- card — FORECAST
- card — GAP FORECAST
- card — ORCADO
- card — PROJECAO DO ANO
- card — REALIZADO
- columnChart — Peso historico de cada mes (base do orcamento adaptativo)
- lineChart — Linha temporal: realizado, orcado, forecast e meta
- pivotTable — Realizado x orcado x forecast por regiao
- textbox

### Tooltip Cliente

- tableEx
- textbox

### Tooltip Produto

- tableEx
- textbox

### Tooltip Pais

- tableEx
- textbox

### Tooltip Vendedor

- tableEx
- textbox

### Detalhe Cliente

- card — CLASSIFICACAO RFV
- card — MARGEM
- card — RECEITA
- card — SHARE OF WALLET
- clusteredBarChart — Mix de categorias compradas
- lineChart — Historico mensal da conta
- pivotTable — Detalhe por produto
- textbox

### Detalhe Mercado

- card — CRESCIMENTO
- card — MARGEM
- card — OTIF
- card — RECEITA
- clusteredBarChart — Clientes do mercado
- lineChart — Evolucao do mercado
- pivotTable — Categorias e desempenho logistico
- textbox
