# Medidas Power BI — Sugestão por Área (Aurora Brasil Exportadora S.A.)

Este documento atende ao item 29 da especificação original de base de dados. As 159 medidas
efetivamente implementadas no modelo estão documentadas com fórmula completa em
`MedidasDAX.md`; aqui fica apenas o mapa por área de negócio, para referência rápida.

## Receita
`Receita USD`, `Receita BRL`, `Receita LY`, `Receita YoY %`, `Receita PM`, `Receita MoM %`,
`Receita YTD`, `Receita Rolling 12M`, `Receita Rolling 3M`, `Receita Rolling 6M`, `CAGR Receita`.

## Margem
`Margem Bruta USD`, `Margem Bruta %`, `Margem por Kg`, `Custo por Kg`, `Frete % Receita`,
`Impacto Desconto %`, `Margem YoY %`, `Margem YoY p.p.`.

## Clientes
`Clientes Ativos`, `Novos Clientes`, `Clientes Perdidos`, `Clientes Reativados`, `Recencia Media
Dias`, `Frequencia Media`, `Receita por Cliente`, `Share of Wallet`, `LTV Estimado`, `Segmento
RFV`, `Score RFV Total`.

## Logística
`OTIF %`, `On Time %`, `In Full %`, `Lead Time Real`, `Dias de Atraso Medio`, `Frete por Kg`,
`% Embarques Atrasados`.

## Metas
`Meta Receita USD`, `Atingimento %`, `Gap Meta USD`, `Receita Forecast USD`, `Forecast x Meta`,
`Status Meta`.

## Câmbio
`Taxa Media USD BRL`, `Taxa Media Ponderada`, `Efeito Cambio BRL`, `Crescimento Operacional BRL`,
`Variacao Cambial %`.

## Pareto / ABC / Concentração
`Ranking Cliente`, `Receita Acumulada Cliente %`, `Classe ABC Cliente`, `Participacao Top 1/5/10/20`,
aplicadas também a Produto e País.

Ver `MedidasDAX.md` para a lista completa com fórmula DAX, formato e dependências de cada
medida.
