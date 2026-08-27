# Dicionario de Dados — Aurora Brasil Exportadora S.A.

Todas as colunas de todas as tabelas estao documentadas. Separador `;`, decimal `,`, codificacao UTF-8 com BOM, datas em ISO `AAAA-MM-DD`.

## dCalendario

*Dimensao de datas continua de 01/01/2022 a 31/07/2026. Marcada como tabela de datas.*

Granularidade: **1 linha por dia** | Linhas: **1,673** | Colunas: **15**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `Data` | Data | Data do calendario (chave da dimensao de datas) | 2022-01-01 | Diaria, sem lacunas |
| `Ano` | Inteiro | Ano civil | 2022 | 2022 a 2026 |
| `Trimestre` | Texto | Trimestre do ano | T1 | T1 a T4 |
| `NumeroMes` | Inteiro | Numero do mes | 1 | 1 a 12 |
| `Mes` | Inteiro | Numero do mes | Janeiro | 1 a 12 |
| `MesAbreviado` | Texto | Abreviacao do mes | Jan | Ordenado por NumeroMes |
| `AnoMes` | Texto | Rotulo mes/ano | Jan/22 | Ordenado por AnoMesNumero |
| `AnoMesNumero` | Inteiro | Chave numerica AAAAMM | 202201 | Coluna tecnica, oculta |
| `SemanaAno` | Inteiro | Semana ISO do ano | 52 | 1 a 53 |
| `NumeroDiaSemana` | Inteiro | Numero do dia da semana | 6 | 1=Segunda a 7=Domingo |
| `DiaSemana` | Texto | Nome do dia da semana | Sabado | Ordenado por NumeroDiaSemana |
| `FimDeSemana` | Texto | Indica fim de semana | Sim | Sim/Nao |
| `DiaUtil` | Texto | Indica dia util | Nao | Sim/Nao |
| `InicioMes` | Data | Primeiro dia do mes | 2022-01-01 | Derivada |
| `FimMes` | Data | Ultimo dia do mes | 2022-01-31 | Derivada |

## dCliente

*Dimensao de clientes internacionais B2B, incluindo potencial anual estimado para Share of Wallet.*

Granularidade: **1 linha por cliente** | Linhas: **330** | Colunas: **24**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `ClienteID` | Inteiro | Chave do cliente | 1 | PK em dCliente, FK nas fatos |
| `CodigoCliente` | Texto | Codigo comercial do cliente | CL0001 | Formato CL0000 |
| `RazaoSocial` | Texto | Razao social ficticia | Changtai Trading Co., Ltd. | Unica |
| `NomeFantasia` | Texto | Nome fantasia | Changtai Trading | Livre |
| `TipoCliente` | Texto | Tipo de operacao do cliente | Industria | Importador, Distribuidor, Rede Varejista, Industria, Food Service, Atacadista, Private Label |
| `Segmento` | Texto | Segmento de atuacao | Industria de Bebidas | Derivado do tipo |
| `Subsegmento` | Texto | Posicionamento do portfolio comprado | Organico | Premium, Mainstream, Organico, Industrial, Gourmet |
| `Porte` | Texto | Porte pelo potencial anual | Pequeno | Grande >=4M, Medio >=1,2M, Pequeno >=350k, Micro |
| `Pais` | Texto | Pais do cliente ou do porto | China | Consistente com dPais |
| `CodigoPais` | Texto | Codigo ISO alpha-3 | CHN | 3 letras |
| `Continente` | Texto | Continente do mercado | Asia | 6 continentes atendidos |
| `RegiaoComercial` | Texto | Regiao comercial de gestao | Asia Oriental | Ex.: Europa Ocidental |
| `Cidade` | Texto | Cidade | Shenzhen | Coerente com o pais |
| `EstadoProvincia` | Texto | Estado ou provincia | Guangdong | Coerente com a cidade |
| `MoedaPreferencial` | Texto | Moeda de negociacao preferida | CNY | USD, EUR, GBP, CAD, JPY, CNY, AED |
| `Idioma` | Texto | Idioma principal de relacionamento | Mandarim | Coerente com o pais |
| `DataCadastro` | Data | Data de abertura do cadastro | 2021-12-01 | Anterior ou igual a primeira compra |
| `VendedorResponsavelID` | Inteiro | FK do executivo responsavel | 13 | Existe em dVendedor |
| `CanalVenda` | Texto | Canal de originacao | Venda Direta | Venda Direta, Representante Local, Trading Parceira, E-commerce B2B, Feira Internacional |
| `ClassificacaoCliente` | Texto | Classificacao estrategica manual | Chave | Estrategico, Chave, Regular, Ocasional |
| `LimiteCreditoUSD` | Decimal | Limite de credito aprovado | 39247.73 | 6% a 22% do potencial |
| `PrazoPagamentoPadrao` | Inteiro | Prazo contratual em dias | 90 | 0, 30, 45, 60, 90 ou 120 |
| `StatusCliente` | Texto | Status derivado da ultima compra | Ativo | Ativo <=180d, Inativo <=365d, Perdido, Prospect |
| `PotencialAnualEstimadoUSD` | Decimal | Compra anual potencial estimada | 471488.92 | Base do Share of Wallet |

## dProduto

*Dimensao de SKUs exportados, com categoria, embalagem, custo base e margem alvo.*

Granularidade: **1 linha por SKU** | Linhas: **106** | Colunas: **18**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `ProdutoID` | Inteiro | Chave do produto | 1 | PK em dProduto |
| `SKU` | Texto | Codigo do SKU | CAF-CAF-025-001 | CAT-SUB-PESO-ID |
| `Produto` | Texto | Descricao comercial do SKU | Cafe Arabica Especial 25kg Caixa | Unica |
| `Categoria` | Texto | Categoria do portfolio | Cafe | 8 categorias |
| `Subcategoria` | Texto | Subcategoria/tipo | Cafe Arabica Especial | 30 subcategorias |
| `Linha` | Texto | Linha de posicionamento | Premium | Premium, Standard, Organico, Ingredientes, Congelados |
| `Marca` | Texto | Marca proprietaria | Aurora Origins | 5 marcas |
| `TipoEmbalagem` | Texto | Formato de embalagem | Caixa Master | Saca, Big Bag, Caixa, Pouch, Balde, Tambor, Cartucho |
| `PesoLiquidoKg` | Decimal | Peso liquido por unidade | 25.0 | Base do calculo de peso total |
| `UnidadeMedida` | Texto | Unidade de medida | KG | KG |
| `OrigemBrasil` | Texto | Indica produto de origem brasileira | Sim | Sim |
| `EstadoOrigem` | Texto | Estado brasileiro de origem | Minas Gerais | UF produtora |
| `CustoBaseBRL` | Decimal | Custo padrao por unidade em BRL | 762.01 | Reajustado por indice anual de categoria |
| `PrecoListaUSD` | Decimal | Preco de tabela por unidade | 244.35 | Base do preco praticado |
| `MargemAlvo` | Decimal | Margem alvo definida no pricing | 0.346 | 0,10 a 0,55 |
| `VidaUtilDias` | Inteiro | Shelf life em dias | 540 | 240 a 730 |
| `Certificacao` | Texto | Certificacao do SKU | Organico BR | Organico, Fair Trade, Rainforest, Kosher, Halal, BRCGS |
| `StatusProduto` | Texto | Ciclo de vida do SKU | Ativo | Ativo, Novo, Descontinuado |

## dVendedor

*Dimensao da equipe comercial com hierarquia Diretor > Gerente Regional > Executivo de Contas.*

Granularidade: **1 linha por profissional** | Linhas: **20** | Colunas: **10**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `VendedorID` | Inteiro | Chave do vendedor | 1 | PK em dVendedor |
| `CodigoVendedor` | Texto | Matricula comercial | VD001 | VD000 |
| `NomeVendedor` | Texto | Nome do profissional | Ricardo Salgueiro Mendes | Ficticio |
| `Cargo` | Texto | Cargo na estrutura | Diretor Comercial | Diretor Comercial, Gerente Regional, Executivo de Contas |
| `Gerente` | Texto | Nome do gestor imediato | Ricardo Salgueiro Mendes | Vazio para o diretor |
| `RegiaoResponsavel` | Texto | Regiao sob responsabilidade | Global | Consistente com REGIAO_PAISES |
| `ContinenteResponsavel` | Texto | Continente sob responsabilidade | Global | - |
| `DataAdmissao` | Data | Data de admissao | 2015-07-03 | Anterior ao periodo analisado |
| `MetaAnualUSD` | Decimal | Meta anual individual | 0.0 | 0 para o diretor |
| `Status` | Texto | Situacao do registro | Ativo | Ativo/Inativo/Em Revisao |

## dPais

*Dimensao geografica de mercados de destino, com risco, lead time e tarifa media de importacao.*

Granularidade: **1 linha por pais** | Linhas: **28** | Colunas: **11**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `PaisID` | Inteiro | Chave do pais | 1 | PK em dPais |
| `Pais` | Texto | Pais do cliente ou do porto | Estados Unidos | Consistente com dPais |
| `CodigoISO` | Texto | Codigo ISO alpha-3 | USA | 3 letras |
| `Continente` | Texto | Continente do mercado | America do Norte | 6 continentes atendidos |
| `Regiao` | Texto | Regiao geoeconomica | NAFTA | - |
| `Moeda` | Texto | Moeda de referencia do mercado | USD | - |
| `IdiomaPrincipal` | Texto | Idioma principal | Ingles | - |
| `ClassificacaoMercado` | Texto | Maturidade do mercado | Principal | Principal, Secundario, Emergente |
| `RiscoPais` | Texto | Risco comercial do pais | Baixo | Baixo, Medio, Alto |
| `LeadTimeMedio` | Inteiro | Lead time medio de referencia em dias | 22 | Base do lead time previsto |
| `TarifaMediaImportacao` | Decimal | Tarifa media de importacao em % | 4.2 | Impacta despesas em DDP |

## dPorto

*Dimensao de portos e aeroportos de origem e destino (UN/LOCODE).*

Granularidade: **1 linha por terminal** | Linhas: **49** | Colunas: **6**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `PortoID` | Inteiro | Chave do porto | 1 | PK em dPorto |
| `Porto` | Texto | Nome do porto ou aeroporto | Porto de Santos | Unico |
| `Cidade` | Texto | Cidade | Santos | Coerente com o pais |
| `Pais` | Texto | Pais do cliente ou do porto | Brasil | Consistente com dPais |
| `CodigoUNLOCODE` | Texto | Codigo UN/LOCODE | BRSSZ | 5 caracteres |
| `TipoPorto` | Texto | Modalidade do terminal | Maritimo | Maritimo, Aereo, Fluvial |

## dTransportadora

*Dimensao de operadores logisticos internacionais.*

Granularidade: **1 linha por operador** | Linhas: **13** | Colunas: **7**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `TransportadoraID` | Inteiro | Chave da transportadora | 1 | PK em dTransportadora |
| `Transportadora` | Texto | Nome do operador logistico | Meridian Blue Lines | Ficticio |
| `ModalPrincipal` | Texto | Modal predominante | Maritimo | Maritimo, Aereo, Rodoviario |
| `Pais` | Texto | Pais do cliente ou do porto | Dinamarca | Consistente com dPais |
| `AvaliacaoFornecedor` | Decimal | Nota de avaliacao do fornecedor | 4.6 | 3,4 a 4,7 |
| `LeadTimeMedio` | Inteiro | Lead time medio de referencia em dias | 26 | Base do lead time previsto |
| `Status` | Texto | Situacao do registro | Ativo | Ativo/Inativo/Em Revisao |

## fVendas

*Fato transacional na granularidade item de pedido faturado. Tabela principal do modelo.*

Granularidade: **1 linha por item de pedido** | Linhas: **96,443** | Colunas: **29**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `VendaID` | Inteiro | Chave da linha de venda | 1 | PK de fVendas |
| `PedidoID` | Texto | Numero do pedido | PED-2022-000001 | Agrupa varias linhas |
| `DataPedido` | Data | Data de emissao do pedido | 2022-01-02 | Relacionamento inativo com dCalendario |
| `DataFaturamento` | Data | Data de faturamento | 2022-01-22 | Relacionamento ativo com dCalendario |
| `ClienteID` | Inteiro | Chave do cliente | 1 | PK em dCliente, FK nas fatos |
| `ProdutoID` | Inteiro | Chave do produto | 65 | PK em dProduto |
| `VendedorID` | Inteiro | Chave do vendedor | 13 | PK em dVendedor |
| `PaisID` | Inteiro | Chave do pais | 15 | PK em dPais |
| `Quantidade` | Inteiro | Unidades de embalagem vendidas | 9 | Inteiro >= 1 |
| `PesoTotalKg` | Decimal | Peso total da linha | 540.0 | Quantidade x PesoLiquidoKg |
| `PrecoUnitarioUSD` | Decimal | Preco praticado por unidade | 630.39 | Preco lista x reajuste x premio de mercado |
| `ReceitaBrutaUSD` | Decimal | Receita bruta da linha | 5673.51 | Quantidade x PrecoUnitarioUSD |
| `DescontoUSD` | Decimal | Desconto comercial concedido | 150.9 | >= 0 |
| `ReceitaLiquidaUSD` | Decimal | Receita liquida da linha | 5522.61 | ReceitaBruta - Desconto |
| `TaxaCambio` | Decimal | Taxa USD/BRL da data de faturamento | 5.2387 | Coerente com fCambio |
| `ReceitaLiquidaBRL` | Decimal | Receita liquida convertida | 28931.3 | ReceitaLiquidaUSD x TaxaCambio |
| `CustoProdutoBRL` | Decimal | Custo do produto em BRL | 18478.71 | CustoBaseBRL x indice de custo x quantidade |
| `CustoProdutoUSD` | Decimal | Custo do produto em USD | 3527.35 | CustoProdutoBRL / TaxaCambio |
| `FreteUSD` | Decimal | Frete internacional assumido pela Aurora | 0.0 | Depende do Incoterm e do modal |
| `SeguroUSD` | Decimal | Seguro internacional | 0.0 | Apenas CIF e DDP |
| `DespesasExportacaoUSD` | Decimal | Despesas de exportacao e desembaraco | 235.51 | 1,6% a 3,4% da receita liquida |
| `CustoTotalUSD` | Decimal | Custo total da linha | 3762.86 | Produto + Frete + Seguro + Despesas |
| `MargemBrutaUSD` | Decimal | Margem bruta da linha | 1759.75 | ReceitaLiquida - CustoTotal |
| `MargemBrutaPercentual` | Decimal | Margem percentual da linha | 0.3186 | MargemBruta / ReceitaLiquida |
| `MoedaNegociacao` | Texto | Moeda contratada com o cliente | CNY | Herdada de dCliente |
| `Incoterm` | Texto | Incoterm da operacao | EXW | FOB, CIF, CFR, EXW, FCA, DDP |
| `CanalVenda` | Texto | Canal de originacao | Venda Direta | Venda Direta, Representante Local, Trading Parceira, E-commerce B2B, Feira Internacional |
| `NumeroInvoice` | Texto | Numero da invoice de exportacao | INV-2022-000001 | Chave de ligacao com fRecebimentos |
| `StatusPedido` | Texto | Situacao do pedido | Faturado | Faturado, Em Producao, Cancelado |

## fEmbarques

*Fato logistico na granularidade pedido embarcado.*

Granularidade: **1 linha por pedido embarcado** | Linhas: **28,465** | Colunas: **23**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `EmbarqueID` | Inteiro | Chave do embarque | 1 | PK de fEmbarques |
| `PedidoID` | Texto | Numero do pedido | PED-2022-000001 | Agrupa varias linhas |
| `ClienteID` | Inteiro | Chave do cliente | 1 | PK em dCliente, FK nas fatos |
| `PaisDestinoID` | Inteiro | FK do pais de destino | 15 | Existe em dPais |
| `PortoOrigemID` | Inteiro | FK do porto de origem | 3 | Terminal brasileiro |
| `PortoDestinoID` | Inteiro | FK do porto de destino | 34 | Terminal internacional |
| `TransportadoraID` | Inteiro | Chave da transportadora | 8 | PK em dTransportadora |
| `DataPrevistaEmbarque` | Data | Data prevista de embarque | 2022-01-27 | Posterior ao faturamento |
| `DataRealEmbarque` | Data | Data efetiva de embarque | 2022-01-27 | Vazia se ainda nao embarcado |
| `DataPrevistaEntrega` | Data | Data prevista de entrega | 2022-03-09 | Embarque previsto + lead time previsto |
| `DataRealEntrega` | Data | Data efetiva de entrega | 2022-03-08 | Vazia se em transito |
| `Modal` | Texto | Modal utilizado | Maritimo | Maritimo (~85%), Aereo, Rodoviario |
| `Container` | Texto | Identificacao do container ou ULD | LCLU5623871 | - |
| `TipoContainer` | Texto | Tipo de equipamento | LCL Consolidado | 20 DRY, 40 HC, 40 REEFER, LCL, ULD |
| `PesoKg` | Decimal | Peso total embarcado | 1640.0 | Soma das linhas do pedido |
| `VolumeM3` | Decimal | Volume cubado | 4.82 | Derivado do peso e da densidade |
| `FreteUSD` | Decimal | Frete internacional assumido pela Aurora | 0.0 | Depende do Incoterm e do modal |
| `SeguroUSD` | Decimal | Seguro internacional | 0.0 | Apenas CIF e DDP |
| `LeadTimePrevisto` | Inteiro | Lead time contratado em dias | 41 | - |
| `LeadTimeReal` | Inteiro | Lead time efetivo em dias | 40 | Vazio se nao entregue |
| `DiasAtraso` | Inteiro | Atraso versus data prevista | -1 | Negativo = adiantado |
| `StatusEmbarque` | Texto | Situacao do embarque | Entregue no prazo | Entregue no prazo, Entregue com atraso, Em transito, Aguardando embarque |
| `MotivoAtraso` | Texto | Causa raiz do atraso | Indisponibilidade de container | Vazio quando nao ha atraso |

## fCambio

*Fato de cotacoes diarias por moeda contra o BRL.*

Granularidade: **1 linha por data e moeda** | Linhas: **11,711** | Colunas: **5**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `Data` | Data | Data do calendario (chave da dimensao de datas) | 2022-01-01 | Diaria, sem lacunas |
| `Moeda` | Texto | Moeda de referencia do mercado | USD | - |
| `TaxaBRL` | Decimal | Cotacao da moeda em BRL | 5.22 | - |
| `VariacaoDia` | Decimal | Variacao percentual diaria | 0.0 | - |
| `VariacaoMes` | Decimal | Variacao percentual mensal | 0.0 | - |

## fMetas

*Fato de metas comerciais na granularidade mes x vendedor.*

Granularidade: **1 linha por mes e vendedor** | Linhas: **768** | Colunas: **12**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `Data` | Data | Data do calendario (chave da dimensao de datas) | 2022-01-01 | Diaria, sem lacunas |
| `Ano` | Inteiro | Ano civil | 2022 | 2022 a 2026 |
| `Mes` | Inteiro | Numero do mes | 1 | 1 a 12 |
| `AnoMes` | Texto | Rotulo mes/ano | Jan/22 | Ordenado por AnoMesNumero |
| `AnoMesNumero` | Inteiro | Chave numerica AAAAMM | 202201 | Coluna tecnica, oculta |
| `VendedorID` | Inteiro | Chave do vendedor | 7 | PK em dVendedor |
| `Regiao` | Texto | Regiao geoeconomica | America do Norte | - |
| `MetaReceitaUSD` | Decimal | Meta de receita liquida | 34457.63 | Mes x vendedor |
| `MetaVolumeKg` | Decimal | Meta de volume | 4648.91 | Mes x vendedor |
| `MetaMargemUSD` | Decimal | Meta de margem bruta | 6933.66 | Mes x vendedor |
| `MetaNovosClientes` | Inteiro | Meta de novos clientes | 0 | Inteiro |
| `MetaPedidos` | Inteiro | Meta de pedidos | 4 | Inteiro |

## fOrcamento

*Fato de orcamento anual aprovado na granularidade mes x regiao x categoria.*

Granularidade: **1 linha por mes, regiao e categoria** | Linhas: **4,014** | Colunas: **11**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `Data` | Data | Data do calendario (chave da dimensao de datas) | 2022-01-01 | Diaria, sem lacunas |
| `AnoMesNumero` | Inteiro | Chave numerica AAAAMM | 202201 | Coluna tecnica, oculta |
| `AnoMes` | Texto | Rotulo mes/ano | Jan/22 | Ordenado por AnoMesNumero |
| `Ano` | Inteiro | Ano civil | 2022 | 2022 a 2026 |
| `Mes` | Inteiro | Numero do mes | 1 | 1 a 12 |
| `Regiao` | Texto | Regiao geoeconomica | America Latina | - |
| `Categoria` | Texto | Categoria do portfolio | Cafe | 8 categorias |
| `ReceitaOrcadaUSD` | Decimal | Receita orcada aprovada | 20235.5 | Mes x regiao x categoria |
| `CustoOrcadoUSD` | Decimal | Custo orcado | 13825.12 | - |
| `MargemOrcadaUSD` | Decimal | Margem orcada | 5844.72 | - |
| `VolumeOrcadoKg` | Decimal | Volume orcado | 1788.73 | - |

## fForecast

*Fato de forecast com revisoes periodicas (Jan/Mai/Set) na granularidade mes x regiao x categoria.*

Granularidade: **1 linha por revisao, mes, regiao e categoria** | Linhas: **11,514** | Colunas: **11**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `Data` | Data | Data do calendario (chave da dimensao de datas) | 2022-01-01 | Diaria, sem lacunas |
| `AnoMesNumero` | Inteiro | Chave numerica AAAAMM | 202201 | Coluna tecnica, oculta |
| `AnoMes` | Texto | Rotulo mes/ano | Jan/22 | Ordenado por AnoMesNumero |
| `Ano` | Inteiro | Ano civil | 2022 | 2022 a 2026 |
| `Mes` | Inteiro | Numero do mes | 1 | 1 a 12 |
| `Regiao` | Texto | Regiao geoeconomica | America Latina | - |
| `Categoria` | Texto | Categoria do portfolio | Cafe | 8 categorias |
| `ReceitaForecastUSD` | Decimal | Receita projetada na revisao | 18389.65 | - |
| `MargemForecastUSD` | Decimal | Margem projetada | 6561.61 | - |
| `VolumeForecastKg` | Decimal | Volume projetado | 1640.43 | - |
| `DataForecast` | Data | Data da revisao de forecast | 2022-01-01 | Revisoes em Jan, Mai e Set |

## fRecebimentos

*Fato financeiro de contas a receber na granularidade invoice.*

Granularidade: **1 linha por invoice** | Linhas: **28,465** | Colunas: **12**

| Campo | Tipo | Descricao | Exemplo | Regra |
|---|---|---|---|---|
| `RecebimentoID` | Inteiro | Chave do titulo | 1 | PK de fRecebimentos |
| `Invoice` | Texto | Numero da invoice | INV-2022-000001 | FK logica para fVendas[NumeroInvoice] |
| `ClienteID` | Inteiro | Chave do cliente | 1 | PK em dCliente, FK nas fatos |
| `DataFaturamento` | Data | Data de faturamento | 2022-01-22 | Relacionamento ativo com dCalendario |
| `DataVencimento` | Data | Vencimento do titulo | 2022-04-22 | Faturamento + prazo do cliente |
| `DataPagamento` | Data | Data da liquidacao | 2022-04-22 | Vazia se em aberto |
| `ValorUSD` | Decimal | Valor faturado do titulo | 16369.94 | - |
| `ValorRecebidoUSD` | Decimal | Valor efetivamente recebido | 16369.94 | - |
| `SaldoUSD` | Decimal | Saldo em aberto | 0.0 | Valor - Recebido |
| `Status` | Texto | Situacao do registro | Pago | Ativo/Inativo/Em Revisao |
| `DiasAtraso` | Inteiro | Atraso versus data prevista | 0 | Negativo = adiantado |
| `FormaPagamento` | Texto | Instrumento de pagamento | Conta Aberta | Carta de Credito, Cobranca Documentaria, Antecipada, Conta Aberta, A Vista |
