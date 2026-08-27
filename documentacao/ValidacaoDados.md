# Relatorio de Validacao — Aurora Brasil Exportadora

Seed: `20260816` | Periodo: 2022-01-01 a 2026-07-31

**Resultado geral: APROVADO**

## Testes

```
=== 1. UNICIDADE DE CHAVES ===
OK    | dCliente[ClienteID] sem duplicidades (330 chaves)
OK    | dProduto[ProdutoID] sem duplicidades (106 chaves)
OK    | dVendedor[VendedorID] sem duplicidades (20 chaves)
OK    | dPais[PaisID] sem duplicidades (28 chaves)
OK    | dPorto[PortoID] sem duplicidades (49 chaves)
OK    | dTransportadora[TransportadoraID] sem duplicidades (13 chaves)
OK    | dCalendario[Data] sem duplicidades (1,673 chaves)
OK    | fVendas[VendaID] sem duplicidades (96,443 chaves)
OK    | fEmbarques[EmbarqueID] sem duplicidades (28,465 chaves)
OK    | fRecebimentos[RecebimentoID] sem duplicidades (28,465 chaves)
=== 2. INTEGRIDADE REFERENCIAL ===
OK    | fVendas[ClienteID] -> dCliente
OK    | fVendas[ProdutoID] -> dProduto
OK    | fVendas[VendedorID] -> dVendedor
OK    | fVendas[PaisID] -> dPais
OK    | fEmbarques[ClienteID] -> dCliente
OK    | fEmbarques[PortoOrigemID] -> dPorto
OK    | fEmbarques[PortoDestinoID] -> dPorto
OK    | fEmbarques[TransportadoraID] -> dTransportadora
OK    | fEmbarques[PedidoID] -> fVendas
OK    | fRecebimentos[ClienteID] -> dCliente
OK    | fRecebimentos[Invoice] -> fVendas
OK    | fMetas[VendedorID] -> dVendedor
OK    | fVendas[DataFaturamento] dentro de dCalendario
OK    | fVendas[DataPedido] dentro de dCalendario
=== 3. CONSISTENCIA FINANCEIRA (tolerancia 0,05 USD) ===
OK    | Receita Bruta = Qtd x Preco (erro max 0.0000)
OK    | Receita Liquida = Bruta - Desconto (erro max 0.0000)
OK    | Custo Total = Produto + Frete + Seguro + Despesas (erro max 0.0000)
OK    | Margem = Receita Liquida - Custo Total (erro max 0.0000)
OK    | Receita BRL = Receita USD x Taxa (erro max 0.0050)
OK    | Receita liquida sempre positiva
OK    | Descontos nao negativos
=== 4. COERENCIA TEMPORAL ===
OK    | DataFaturamento >= DataPedido
OK    | Entrega real posterior ao embarque real
OK    | Embarque real nao anterior ao previsto
OK    | Pagamento posterior ao faturamento
OK    | Vencimento posterior ao faturamento
OK    | Nenhuma data fora do periodo
=== 5. NULOS EM CHAVES ===
OK    | dCliente: 0 celulas nulas (aceitavel em colunas de evento em aberto)
OK    | dProduto: 0 celulas nulas (aceitavel em colunas de evento em aberto)
OK    | fVendas: 0 celulas nulas (aceitavel em colunas de evento em aberto)
OK    | fEmbarques: 1536 celulas nulas (aceitavel em colunas de evento em aberto)
OK    | fRecebimentos: 0 celulas nulas (aceitavel em colunas de evento em aberto)
```

## Estatisticas

```
Clientes cadastrados............: 330
Clientes com venda..............: 328
Produtos (SKUs).................: 106
Vendedores......................: 20
Paises atendidos................: 28
Linhas em fVendas...............: 96,443
Pedidos.........................: 29,210
Pedidos cancelados..............: 559
Embarques.......................: 28,465
Receita liquida total (USD).....: 435,660,635.97
Receita liquida total (BRL).....: 2,437,645,689.74
Margem bruta total (USD)........: 111,413,912.27
Margem bruta media (%)..........: 25.57%
Desconto medio (%)..............: 8.82%
Ticket medio por pedido (USD)...: 15,305.13
Volume total (toneladas)........: 56,619.2
Preco medio por kg (USD)........: 7.69
Linhas com margem negativa......: 5.26%
Entregas realizadas.............: 27,697
% entregas atrasadas............: 16.57%
Atraso medio (dias, atrasados)..: 9.3
Lead time medio real (dias).....: 23.4
Mix modal (%)...................: Maritimo 83.0%, Aereo 14.6%, Rodoviario 2.4%
Saldo em aberto (USD)...........: 28,314,979.06
Inadimplencia (vencido/total %).: 0.82%
Prazo medio recebimento (dias)..: 10.8 de atraso sobre o vencimento

--- Receita liquida por ano (USD) ---
2022: 78,035,736.86   [margem 22.8%]
2023: 84,236,664.25  (+7.9% YoY)   [margem 20.9%]
2024: 100,368,623.81  (+19.2% YoY)   [margem 24.6%]
2025: 108,416,235.82  (+8.0% YoY)   [margem 29.0%]
2026: 64,603,375.23  (-40.4% YoY)   [margem 30.7%]
  (2026 parcial: jan-jul)

--- Concentracao de clientes (Pareto) ---
Top  1 clientes:   9.6% da receita
Top  5 clientes:  26.5% da receita
Top 10 clientes:  32.3% da receita
Top 20 clientes:  41.7% da receita
Top 50 clientes:  60.8% da receita
108 clientes (32.9%) concentram 80% da receita

--- Top 8 paises por receita ---
Alemanha                        86,837,530.09  (19.9%)
Estados Unidos                  46,680,086.03  (10.7%)
Reino Unido                     38,781,670.57  ( 8.9%)
Paises Baixos                   32,101,315.10  ( 7.4%)
Espanha                         28,083,638.87  ( 6.4%)
Canada                          23,828,518.16  ( 5.5%)
Franca                          23,747,200.07  ( 5.5%)
Italia                          19,556,445.95  ( 4.5%)

--- Receita e margem por categoria ---
Cafe                            82,990,226.80  margem  30.0%
Acai                            61,809,365.39  margem  17.4%
Castanhas                       60,664,178.12  margem  29.9%
Frutas Processadas              60,329,015.46  margem  24.7%
Cacau                           59,915,599.49  margem  16.2%
Mel                             45,661,581.69  margem  32.2%
Ingredientes Alimenticios       39,145,023.62  margem  20.5%
Produtos Naturais               25,145,645.40  margem  41.0%

--- Incoterms ---
FOB     43.8%
CIF     31.1%
FCA      8.6%
CFR      7.6%
EXW      5.9%
DDP      3.0%
```

## Linhas por tabela

| Tabela | Linhas | Colunas |
|---|---:|---:|
| dCalendario | 1,673 | 15 |
| dCliente | 330 | 24 |
| dProduto | 106 | 18 |
| dVendedor | 20 | 10 |
| dPais | 28 | 11 |
| dPorto | 49 | 6 |
| dTransportadora | 13 | 7 |
| fVendas | 96,443 | 29 |
| fEmbarques | 28,465 | 23 |
| fCambio | 11,711 | 5 |
| fMetas | 768 | 12 |
| fOrcamento | 4,014 | 11 |
| fForecast | 11,514 | 11 |
| fRecebimentos | 28,465 | 12 |
