# Dashboard Blueprint — Aurora Brasil Exportadora S.A.

Este documento atende ao item 30 da especificação original de base de dados. As 11 páginas
efetivamente construídas no PBIR, com KPIs, visuais, filtros, tooltips e drill-throughs, estão
documentadas com detalhe em `DashboardPages.md`; aqui fica o mapa de intenção por página.

| # | Página | Pergunta central | KPIs principais |
|---|---|---|---|
| 01 | Executive Overview | Estamos crescendo, atingindo meta e rentáveis? | Receita USD, Margem %, Atingimento %, Toneladas |
| 02 | Sales Performance | O ritmo comercial está no compromisso assumido? | Receita, Meta, Gap, Ticket Médio, Pedidos |
| 03 | Customers | Quem sustenta a receita e quem está saindo? | Clientes Ativos, Novos, Perdidos, Churn, Receita em Risco |
| 04 | Customer Potential | Onde há receita não capturada? | Receita 12M, Potencial, Share of Wallet, Gap |
| 05 | Products | Qual portfólio cresce com rentabilidade? | Receita, Margem, Volume, Preço médio/kg |
| 06 | Markets | Quais mercados sustentam o futuro? | Receita exportada, Volume, Crescimento, Margem |
| 07 | Profitability | Onde o valor é consumido entre receita e margem? | Receita Bruta, Descontos, Custo Total, Margem |
| 08 | Logistics | Onde a operação perde prazo? | OTIF, Lead Time, % Atrasos, Frete/kg |
| 09 | Sales Team | Quem entrega e quem depende de uma conta? | Receita, Atingimento, Novos Clientes, Margem |
| 10 | Finance | Quanto ainda não virou caixa? | Contas a Receber, Saldo em Aberto, Saldo Vencido, Inadimplência |
| 11 | Forecast & Budget | Vamos fechar acima ou abaixo do compromisso? | Realizado, Orçado, Forecast, Gap |

Tooltips dedicados: Cliente, Produto, País, Vendedor.
Drill-throughs: Detalhe Cliente (histórico completo da conta), Detalhe Mercado (diagnóstico
completo do país).

Ver `DashboardPages.md` para o inventário completo de visuais por página.
