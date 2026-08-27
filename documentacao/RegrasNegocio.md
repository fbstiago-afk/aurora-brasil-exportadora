# Regras de Negócio — Aurora Brasil Exportadora S.A.

Este documento descreve as regras comerciais, financeiras e logísticas que governam a geração
dos dados e que devem orientar a leitura das medidas DAX.

## 1. Cadeia financeira (identidade contábil exata)

```
Receita Bruta USD   = Quantidade × Preço Unitário USD
Receita Líquida USD = Receita Bruta USD − Desconto USD
Receita Líquida BRL = Receita Líquida USD × Taxa de Câmbio (data de faturamento)
Custo Total USD     = Custo Produto USD + Frete USD + Seguro USD + Despesas Exportação USD
Margem Bruta USD    = Receita Líquida USD − Custo Total USD
Margem Bruta %      = Margem Bruta USD ÷ Receita Líquida USD
```

Essas cinco identidades são verificadas linha a linha em `validate_data.py`, com tolerância zero
(erro máximo observado: 0,00 USD) — os valores foram arredondados a cada etapa do encadeamento,
não apenas no resultado final, para que a soma de partes arredondadas bata com o total.

## 2. Preço e reajuste

O preço praticado parte do `PrecoListaUSD` do SKU e recebe: reajuste anual (2022=base,
+4,5% em 2023, +9% em 2024, +15,5% em 2025, +19% em 2026 sobre a base), prêmio de 4% em mercados
"Principais" (Alemanha, EUA, Reino Unido etc.) ou desconto de 2% em mercados menos maduros, e
ruído aleatório de ±4,5% por transação.

## 3. Descontos comerciais

O desconto é função do perfil do cliente (0,01 a 0,19 de desconto-base, atribuído na geração),
acrescido de escalonamento para pedidos grandes (acima de US$ 60 mil) e de uma probabilidade de
0,7% de desconto excepcional (12% a 20% extra) — a anomalia deliberada do item 23 da
especificação original. Clientes Food Service recebem +5 p.p. de desconto-base, refletindo o
maior poder de barganha de redes de alimentação.

## 4. Custo do produto

`CustoProdutoBRL = CustoBaseBRL do SKU × Índice de Custo da categoria no ano × Quantidade`. O
índice de custo simula inflação de insumos: estável na maioria das categorias, mas com um choque
real em **Cacau** (índice sobe de 1,00 em 2022 para 1,62 em 2025, refletindo a alta histórica do
cacau no período, e recua para 1,49 em 2026). `CustoProdutoUSD` é a conversão pela taxa de câmbio
da própria transação.

## 5. Frete, seguro e despesas — dependentes do Incoterm

| Incoterm | Frete pago pela Aurora | Seguro pago pela Aurora |
|---|---|---|
| EXW | Não | Não |
| FCA | Parcial (8%) | Não |
| FOB | Parcial (10%) | Não |
| CFR | Integral | Não |
| CIF | Integral | Sim |
| DDP | Integral + tarifa de importação do país destino | Sim |

O frete por quilo também depende do lead time médio do país (rotas mais longas custam mais), do
modal (aéreo custa ~3,6× o marítimo) e sofre um choque de +38% entre outubro/2024 e janeiro/2025,
simulando uma crise de disponibilidade de container. Despesas de exportação somam 1,6% a 3,4% da
receita líquida mais uma taxa fixa por item do pedido.

## 6. Câmbio

A taxa USD/BRL segue uma trajetória histórica plausível por âncoras (5,20 em jan/2022, mínima de
4,85 em meados de 2023, pico de 6,12 no fim de 2025, e acomodação em 5,68 em jul/2026), com ruído
diário. As demais seis moedas (EUR, GBP, CAD, JPY, CNY, AED) derivam do USD por uma razão fixa
mais deriva própria, para que cada moeda tenha uma dinâmica levemente diferente sem perder
coerência com o dólar.

## 7. Sazonalidade

Cada categoria tem um índice mensal próprio (ex.: Açaí tem pico em dezembro–janeiro, verão no
hemisfério sul; Café tem pico em setembro–outubro; Produtos Naturais são mais estáveis ao longo
do ano). O índice multiplica o volume-alvo mensal de cada cliente.

## 8. Logística e atrasos

O atraso é função da avaliação da transportadora (fornecedores com nota abaixo de 3,7 têm mais
atraso), da rota (uma rota específica — Santos→Jebel Ali, Emirados Árabes — tem +30 p.p. de
probabilidade de atraso, ver `InsightsOcultos.md` I5) e do mesmo choque logístico de
outubro/2024–janeiro/2025 que afeta o frete. Os motivos de atraso são sorteados entre sete causas
reais de comércio exterior (congestionamento portuário, documentação, inspeção alfandegária,
atraso do armador, clima, indisponibilidade de container, atraso de produção).

## 9. Prazo e inadimplência

O prazo de pagamento (`PrazoPagamentoPadrao`) é definido por cliente na dimensão. O comportamento
de pagamento é um perfil independente por cliente: 58% pontuais, 26% com atraso leve, 10% com
atraso relevante e 6% inadimplentes (atraso médio de ~260 dias ou não pagamento). Cerca de 4,5%
das invoices recebem pagamento parcial.

## 10. Metas e forecast

As metas mensais por vendedor são calculadas de trás para frente a partir do realizado, para
produzir uma distribuição realista de atingimento (≈20% dos vendedores acima de 120%, ≈30% entre
100–120%, ≈30% entre 80–100%, ≈20% abaixo de 80%) — nunca todo mundo bate a meta e nunca todo
mundo fica abaixo. O forecast é revisado três vezes por ano (janeiro, maio, setembro); a precisão
melhora conforme o horizonte de projeção diminui, simulando o ciclo real de revisão orçamentária.

## 11. Ciclo de vida de cliente e produto

Clientes têm `StatusCliente` calculado dinamicamente pela última data de faturamento (Ativo até
180 dias, Inativo até 365 dias, Perdido acima disso, ou Prospect se nunca comprou). Produtos têm
`StatusProduto` fixo (Ativo, Novo — lançado a partir de 2025, ou Descontinuado — perdendo peso de
mix a partir de 2024).
