# Modelo de Dados — Aurora Brasil Exportadora S.A.

Arquitetura **estrela**, com dimensoes conformadas compartilhadas entre as fatos. Nenhum relacionamento bidirecional. Todas as chaves estao ocultas na camada de relatorio.

## Tabelas

| Tabela | Papel | Granularidade | Linhas |
|---|---|---|---|
| `dCalendario` | Dimensao | 1 linha por dia | 1,673 |
| `dCliente` | Dimensao | 1 linha por cliente | 330 |
| `dProduto` | Dimensao | 1 linha por SKU | 106 |
| `dVendedor` | Dimensao | 1 linha por profissional | 20 |
| `dPais` | Dimensao | 1 linha por pais | 28 |
| `dPorto` | Dimensao | 1 linha por terminal | 49 |
| `dTransportadora` | Dimensao | 1 linha por operador | 13 |
| `fVendas` | Fato | 1 linha por item de pedido | 96,443 |
| `fEmbarques` | Fato | 1 linha por pedido embarcado | 28,465 |
| `fCambio` | Fato | 1 linha por data e moeda | 11,711 |
| `fMetas` | Fato | 1 linha por mes e vendedor | 768 |
| `fOrcamento` | Fato | 1 linha por mes, regiao e categoria | 4,014 |
| `fForecast` | Fato | 1 linha por revisao, mes, regiao e categoria | 11,514 |
| `fRecebimentos` | Fato | 1 linha por invoice | 28,465 |
| `_Medidas` | Tabela tecnica | 1 linha fictícia, apenas medidas | 1 |

## Relacionamentos

| De (1) | Para (*) | Cardinalidade | Direcao | Estado |
|---|---|---|---|---|
| `dCalendario[Data]` | `fVendas[DataFaturamento]` | 1:* | Single | Ativo |
| `dCalendario[Data]` | `fVendas[DataPedido]` | 1:* | Single | Inativo (USERELATIONSHIP) |
| `dCliente[ClienteID]` | `fVendas[ClienteID]` | 1:* | Single | Ativo |
| `dProduto[ProdutoID]` | `fVendas[ProdutoID]` | 1:* | Single | Ativo |
| `dVendedor[VendedorID]` | `fVendas[VendedorID]` | 1:* | Single | Ativo |
| `dPais[PaisID]` | `fVendas[PaisID]` | 1:* | Single | Ativo |
| `dCalendario[Data]` | `fEmbarques[DataRealEmbarque]` | 1:* | Single | Ativo |
| `dCalendario[Data]` | `fEmbarques[DataRealEntrega]` | 1:* | Single | Inativo (USERELATIONSHIP) |
| `dCliente[ClienteID]` | `fEmbarques[ClienteID]` | 1:* | Single | Ativo |
| `dPais[PaisID]` | `fEmbarques[PaisDestinoID]` | 1:* | Single | Ativo |
| `dPorto[PortoID]` | `fEmbarques[PortoOrigemID]` | 1:* | Single | Ativo |
| `dTransportadora[TransportadoraID]` | `fEmbarques[TransportadoraID]` | 1:* | Single | Ativo |
| `dCalendario[Data]` | `fRecebimentos[DataFaturamento]` | 1:* | Single | Ativo |
| `dCalendario[Data]` | `fRecebimentos[DataVencimento]` | 1:* | Single | Inativo (USERELATIONSHIP) |
| `dCalendario[Data]` | `fRecebimentos[DataPagamento]` | 1:* | Single | Inativo (USERELATIONSHIP) |
| `dCliente[ClienteID]` | `fRecebimentos[ClienteID]` | 1:* | Single | Ativo |
| `dVendedor[VendedorID]` | `fMetas[VendedorID]` | 1:* | Single | Ativo |
| `dCalendario[Data]` | `fMetas[Data]` | 1:* | Single | Ativo |
| `dCalendario[Data]` | `fOrcamento[Data]` | 1:* | Single | Ativo |
| `dCalendario[Data]` | `fForecast[Data]` | 1:* | Single | Ativo |
| `dCalendario[Data]` | `fCambio[Data]` | 1:* | Single | Ativo |

## Chaves e integridade

- `dCalendario[Data]` marcada como tabela de datas (`dataCategory: Time`, coluna chave).
- Fatos mensais (`fMetas`, `fOrcamento`, `fForecast`) carregam a coluna `Data` com o primeiro dia do mes, evitando relacionar por `AnoMesNumero` (que nao e unico no calendario).
- Relacionamentos inativos existem para `DataPedido`, `DataRealEntrega`, `DataVencimento` e `DataPagamento`, ativados via `USERELATIONSHIP` nas medidas correspondentes.
- `fRecebimentos[Invoice]` liga-se logicamente a `fVendas[NumeroInvoice]`; nao ha relacionamento fisico para evitar ambiguidade — a analise financeira e feita por cliente e data.

## Colunas ocultas

Todas as PKs e FKs, alem de `AnoMesNumero`, `NumeroMes`, `NumeroDiaSemana`, `InicioMes` e `FimMes` (usadas apenas para ordenacao e relacionamento).

## Sort by column

`Mes` e `MesAbreviado` por `NumeroMes`; `AnoMes` por `AnoMesNumero`; `DiaSemana` por `NumeroDiaSemana`.
