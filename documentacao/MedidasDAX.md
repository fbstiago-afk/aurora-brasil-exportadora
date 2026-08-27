# Medidas DAX — Aurora Brasil Exportadora S.A.

Total: **159 medidas**, todas na tabela `_Medidas`, organizadas em 16 display folders.

## 01 Receita

### `Receita Bruta USD`

Faturamento bruto em USD antes de descontos comerciais.

```dax
Receita Bruta USD =
SUM(fVendas[ReceitaBrutaUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Descontos USD`

Total de descontos comerciais concedidos.

```dax
Descontos USD =
SUM(fVendas[DescontoUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Desconto %`

```dax
Desconto % =
DIVIDE([Descontos USD], [Receita Bruta USD])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Descontos USD`, `Receita Bruta USD`

### `Receita USD`

Receita liquida em USD. Medida base de todo o relatorio.

```dax
Receita USD =
SUM(fVendas[ReceitaLiquidaUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Receita BRL`

Receita liquida convertida a BRL pela taxa da data de faturamento.

```dax
Receita BRL =
SUM(fVendas[ReceitaLiquidaBRL])
```

- **Formato:** `"R$ "#,0.00`
- **Dependencias:** colunas base

### `Receita por Kg`

```dax
Receita por Kg =
DIVIDE([Receita USD], [Peso Total Kg])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Peso Total Kg`, `Receita USD`

### `Receita Pedido`

```dax
Receita Pedido =
SUM(fVendas[ReceitaLiquidaUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Receita por Data de Pedido`

Receita reconhecida pela data do pedido (relacionamento inativo).

```dax
Receita por Data de Pedido =
CALCULATE([Receita USD], USERELATIONSHIP(dCalendario[Data], fVendas[DataPedido]))
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita USD`

## 02 Crescimento

### `Receita LY`

```dax
Receita LY =
CALCULATE([Receita USD], SAMEPERIODLASTYEAR(dCalendario[Data]))
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita USD`

### `Receita YoY`

```dax
Receita YoY =
[Receita USD] - [Receita LY]
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita LY`, `Receita USD`

### `Receita YoY %`

```dax
Receita YoY % =
DIVIDE([Receita YoY], [Receita LY])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita LY`, `Receita YoY`

### `Receita PM`

```dax
Receita PM =
CALCULATE([Receita USD], DATEADD(dCalendario[Data], -1, MONTH))
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita USD`

### `Receita MoM`

```dax
Receita MoM =
[Receita USD] - [Receita PM]
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita PM`, `Receita USD`

### `Receita MoM %`

```dax
Receita MoM % =
DIVIDE([Receita MoM], [Receita PM])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita MoM`, `Receita PM`

### `Receita YTD`

```dax
Receita YTD =
TOTALYTD([Receita USD], dCalendario[Data])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita USD`

### `Receita YTD LY`

```dax
Receita YTD LY =
CALCULATE([Receita YTD], SAMEPERIODLASTYEAR(dCalendario[Data]))
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita YTD`

### `Receita YTD YoY %`

```dax
Receita YTD YoY % =
DIVIDE([Receita YTD] - [Receita YTD LY], [Receita YTD LY])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita YTD`, `Receita YTD LY`

### `Receita Rolling 3M`

```dax
Receita Rolling 3M =
CALCULATE([Receita USD], DATESINPERIOD(dCalendario[Data], MAX(dCalendario[Data]), -3, MONTH))
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita USD`

### `Receita Rolling 6M`

```dax
Receita Rolling 6M =
CALCULATE([Receita USD], DATESINPERIOD(dCalendario[Data], MAX(dCalendario[Data]), -6, MONTH))
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita USD`

### `Receita Rolling 12M`

```dax
Receita Rolling 12M =
CALCULATE([Receita USD], DATESINPERIOD(dCalendario[Data], MAX(dCalendario[Data]), -12, MONTH))
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita USD`

### `Receita Media Mensal 12M`

```dax
Receita Media Mensal 12M =
DIVIDE([Receita Rolling 12M], 12)
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita Rolling 12M`

### `CAGR Receita`

```dax
CAGR Receita =
VAR _Ini = CALCULATE([Receita USD], ALL(dCalendario), dCalendario[Ano] = MIN(dCalendario[Ano]))
VAR _Fim = CALCULATE([Receita USD], ALL(dCalendario), dCalendario[Ano] = MAX(dCalendario[Ano]))
VAR _N = MAX(dCalendario[Ano]) - MIN(dCalendario[Ano])
RETURN IF(_N > 0 && _Ini > 0, ( _Fim / _Ini ) ^ DIVIDE(1, _N) - 1)
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita USD`

### `Margem YoY p.p.`

Variacao da margem percentual em pontos percentuais versus ano anterior.

```dax
Margem YoY p.p. =
[Margem Bruta %] - CALCULATE([Margem Bruta %], SAMEPERIODLASTYEAR(dCalendario[Data]))
```

- **Formato:** `#,0.0`
- **Dependencias:** `Margem Bruta %`

### `Volume YoY %`

```dax
Volume YoY % =
VAR _LY = CALCULATE([Peso Total Kg], SAMEPERIODLASTYEAR(dCalendario[Data]))
RETURN DIVIDE([Peso Total Kg] - _LY, _LY)
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Peso Total Kg`

## 03 Volume

### `Quantidade`

```dax
Quantidade =
SUM(fVendas[Quantidade])
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Peso Total Kg`

```dax
Peso Total Kg =
SUM(fVendas[PesoTotalKg])
```

- **Formato:** `#,0.0`
- **Dependencias:** colunas base

### `Toneladas`

```dax
Toneladas =
DIVIDE([Peso Total Kg], 1000)
```

- **Formato:** `#,0.0`
- **Dependencias:** `Peso Total Kg`

### `Pedidos`

```dax
Pedidos =
DISTINCTCOUNT(fVendas[PedidoID])
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Linhas de Pedido`

```dax
Linhas de Pedido =
COUNTROWS(fVendas)
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Ticket Medio USD`

```dax
Ticket Medio USD =
DIVIDE([Receita USD], [Pedidos])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Pedidos`, `Receita USD`

### `Ticket Medio BRL`

```dax
Ticket Medio BRL =
DIVIDE([Receita BRL], [Pedidos])
```

- **Formato:** `"R$ "#,0.00`
- **Dependencias:** `Pedidos`, `Receita BRL`

### `Preco Medio por Kg`

```dax
Preco Medio por Kg =
DIVIDE([Receita Bruta USD], [Peso Total Kg])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Peso Total Kg`, `Receita Bruta USD`

## 04 Margem

### `Custo Produto USD`

```dax
Custo Produto USD =
SUM(fVendas[CustoProdutoUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Frete USD`

```dax
Frete USD =
SUM(fVendas[FreteUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Seguro USD`

```dax
Seguro USD =
SUM(fVendas[SeguroUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Despesas Exportacao USD`

```dax
Despesas Exportacao USD =
SUM(fVendas[DespesasExportacaoUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Custo Total USD`

```dax
Custo Total USD =
SUM(fVendas[CustoTotalUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Margem Bruta USD`

Receita liquida menos custo de produto, frete, seguro e despesas de exportacao.

```dax
Margem Bruta USD =
SUM(fVendas[MargemBrutaUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Margem Bruta BRL`

```dax
Margem Bruta BRL =
SUMX(fVendas, fVendas[MargemBrutaUSD] * fVendas[TaxaCambio])
```

- **Formato:** `"R$ "#,0.00`
- **Dependencias:** colunas base

### `Margem Bruta %`

```dax
Margem Bruta % =
DIVIDE([Margem Bruta USD], [Receita USD])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Margem Bruta USD`, `Receita USD`

### `Margem por Kg`

```dax
Margem por Kg =
DIVIDE([Margem Bruta USD], [Peso Total Kg])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Margem Bruta USD`, `Peso Total Kg`

### `Custo por Kg`

```dax
Custo por Kg =
DIVIDE([Custo Total USD], [Peso Total Kg])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Custo Total USD`, `Peso Total Kg`

### `Frete % Receita`

```dax
Frete % Receita =
DIVIDE([Frete USD], [Receita USD])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Frete USD`, `Receita USD`

### `Impacto Desconto %`

```dax
Impacto Desconto % =
DIVIDE([Descontos USD], [Receita Bruta USD])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Descontos USD`, `Receita Bruta USD`

### `Margem LY`

```dax
Margem LY =
CALCULATE([Margem Bruta USD], SAMEPERIODLASTYEAR(dCalendario[Data]))
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Margem Bruta USD`

### `Margem YoY %`

```dax
Margem YoY % =
DIVIDE([Margem Bruta USD] - [Margem LY], [Margem LY])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Margem Bruta USD`, `Margem LY`

### `Margem YTD`

```dax
Margem YTD =
TOTALYTD([Margem Bruta USD], dCalendario[Data])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Margem Bruta USD`

## 05 Clientes

### `Clientes Ativos`

Clientes com ao menos um faturamento no contexto de filtro.

```dax
Clientes Ativos =
CALCULATE(DISTINCTCOUNT(fVendas[ClienteID]), fVendas[StatusPedido] = "Faturado")
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Clientes 90D`

```dax
Clientes 90D =
VAR _Fim = MAX(dCalendario[Data])
RETURN CALCULATE(DISTINCTCOUNT(fVendas[ClienteID]),
    DATESINPERIOD(dCalendario[Data], _Fim, -90, DAY), ALL(dCalendario))
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Clientes Base`

```dax
Clientes Base =
COUNTROWS(dCliente)
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Novos Clientes`

Clientes cuja primeira compra historica ocorreu dentro do periodo filtrado.

```dax
Novos Clientes =
VAR _Ini = MIN(dCalendario[Data])
VAR _Fim = MAX(dCalendario[Data])
RETURN COUNTROWS(FILTER(VALUES(dCliente[ClienteID]),
    VAR _Prim = CALCULATE(MIN(fVendas[DataFaturamento]), ALL(dCalendario))
    RETURN NOT ISBLANK(_Prim) && _Prim >= _Ini && _Prim <= _Fim))
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Clientes Perdidos`

Sem compras nos ultimos 365 dias em relacao ao fim do periodo.

```dax
Clientes Perdidos =
VAR _Fim = MAX(dCalendario[Data])
RETURN COUNTROWS(FILTER(VALUES(dCliente[ClienteID]),
    VAR _Ult = CALCULATE(MAX(fVendas[DataFaturamento]), ALL(dCalendario), dCalendario[Data] <= _Fim)
    RETURN NOT ISBLANK(_Ult) && _Ult < _Fim - 365))
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Clientes Em Risco`

```dax
Clientes Em Risco =
VAR _Fim = MAX(dCalendario[Data])
RETURN COUNTROWS(FILTER(VALUES(dCliente[ClienteID]),
    VAR _Ult = CALCULATE(MAX(fVendas[DataFaturamento]), ALL(dCalendario), dCalendario[Data] <= _Fim)
    RETURN NOT ISBLANK(_Ult) && _Ult < _Fim - 180 && _Ult >= _Fim - 365))
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Clientes Inativos 90D`

```dax
Clientes Inativos 90D =
VAR _Fim = MAX(dCalendario[Data])
RETURN COUNTROWS(FILTER(VALUES(dCliente[ClienteID]),
    VAR _Ult = CALCULATE(MAX(fVendas[DataFaturamento]), ALL(dCalendario), dCalendario[Data] <= _Fim)
    RETURN NOT ISBLANK(_Ult) && _Ult < _Fim - 90))
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Clientes Reativados`

Comprou no periodo apos 180 dias ou mais sem compras.

```dax
Clientes Reativados =
VAR _Ini = MIN(dCalendario[Data])
VAR _Fim = MAX(dCalendario[Data])
RETURN COUNTROWS(FILTER(VALUES(dCliente[ClienteID]),
    VAR _Comprou = CALCULATE([Pedidos]) > 0
    VAR _Ant = CALCULATE(MAX(fVendas[DataFaturamento]), ALL(dCalendario), dCalendario[Data] < _Ini)
    RETURN _Comprou && NOT ISBLANK(_Ant) && _Ant < _Ini - 180))
```

- **Formato:** `#,0`
- **Dependencias:** `Pedidos`

### `Taxa de Churn %`

```dax
Taxa de Churn % =
DIVIDE([Clientes Perdidos], [Clientes Perdidos] + [Clientes Ativos])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Clientes Ativos`, `Clientes Perdidos`

### `Receita em Risco`

```dax
Receita em Risco =
VAR _Fim = MAX(dCalendario[Data])
RETURN SUMX(FILTER(VALUES(dCliente[ClienteID]),
    VAR _Ult = CALCULATE(MAX(fVendas[DataFaturamento]), ALL(dCalendario), dCalendario[Data] <= _Fim)
    RETURN NOT ISBLANK(_Ult) && _Ult < _Fim - 180),
    CALCULATE([Receita Rolling 12M]))
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita Rolling 12M`

### `Receita por Cliente`

```dax
Receita por Cliente =
DIVIDE([Receita USD], [Clientes Ativos])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Clientes Ativos`, `Receita USD`

### `Frequencia Media`

```dax
Frequencia Media =
DIVIDE([Pedidos], [Clientes Ativos])
```

- **Formato:** `#,0.0`
- **Dependencias:** `Clientes Ativos`, `Pedidos`

### `Recencia Dias`

```dax
Recencia Dias =
DATEDIFF(CALCULATE(MAX(fVendas[DataFaturamento])), MAX(dCalendario[Data]), DAY)
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Recencia Media Dias`

```dax
Recencia Media Dias =
AVERAGEX(VALUES(dCliente[ClienteID]), [Recencia Dias])
```

- **Formato:** `#,0.0`
- **Dependencias:** `Recencia Dias`

### `Data Primeira Compra`

```dax
Data Primeira Compra =
CALCULATE(MIN(fVendas[DataFaturamento]), ALL(dCalendario))
```

- **Formato:** `yyyy-mm-dd`
- **Dependencias:** colunas base

### `Data Ultima Compra`

```dax
Data Ultima Compra =
CALCULATE(MAX(fVendas[DataFaturamento]))
```

- **Formato:** `yyyy-mm-dd`
- **Dependencias:** colunas base

### `LTV Estimado`

Proxy de valor vitalicio: receita 12M projetada em 3 anos ponderada pela margem.

```dax
LTV Estimado =
[Receita Rolling 12M] * 3 * [Margem Bruta %]
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Margem Bruta %`, `Receita Rolling 12M`

## 06 RFV

### `Score Recencia`

```dax
Score Recencia =
VAR _R = [Recencia Dias]
RETURN SWITCH(TRUE(), ISBLANK(_R), BLANK(), _R <= 45, 5, _R <= 90, 4, _R <= 180, 3, _R <= 365, 2, 1)
```

- **Formato:** `#,0`
- **Dependencias:** `Recencia Dias`

### `Score Frequencia`

```dax
Score Frequencia =
VAR _F = [Pedidos]
RETURN SWITCH(TRUE(), _F = 0, BLANK(), _F >= 40, 5, _F >= 20, 4, _F >= 10, 3, _F >= 4, 2, 1)
```

- **Formato:** `#,0`
- **Dependencias:** `Pedidos`

### `Score Valor`

```dax
Score Valor =
VAR _V = [Receita USD]
VAR _Rk = RANKX(ALLSELECTED(dCliente[ClienteID]), [Receita USD], , DESC)
VAR _N = COUNTROWS(ALLSELECTED(dCliente[ClienteID]))
VAR _P = DIVIDE(_Rk, _N)
RETURN IF(ISBLANK(_V), BLANK(), SWITCH(TRUE(), _P <= 0.1, 5, _P <= 0.3, 4, _P <= 0.6, 3, _P <= 0.85, 2, 1))
```

- **Formato:** `#,0`
- **Dependencias:** `Receita USD`

### `Score RFV Total`

```dax
Score RFV Total =
[Score Recencia] + [Score Frequencia] + [Score Valor]
```

- **Formato:** `#,0`
- **Dependencias:** `Score Frequencia`, `Score Recencia`, `Score Valor`

### `Segmento RFV`

Classificacao RFV dinamica calculada no contexto do relatorio.

```dax
Segmento RFV =
VAR _R = [Score Recencia] VAR _F = [Score Frequencia] VAR _V = [Score Valor]
VAR _Prim = [Data Primeira Compra]
VAR _Novo = DATEDIFF(_Prim, MAX(dCalendario[Data]), DAY) <= 180
RETURN SWITCH(TRUE(),
    ISBLANK(_R), "Sem historico",
    _R >= 4 && _F >= 4 && _V >= 4, "Campeoes",
    _R >= 3 && _F >= 3 && _V >= 3, "Leais",
    _Novo && _R >= 4, "Novos",
    _R >= 4 && _F <= 2, "Potenciais",
    _R = 3 && _F >= 3, "Precisam de Atencao",
    _R = 2 && _V >= 3, "Em Risco",
    _R = 2, "Hibernando",
    "Perdidos")
```

- **Formato:** `texto`
- **Dependencias:** `Data Primeira Compra`, `Score Frequencia`, `Score Recencia`, `Score Valor`

## 07 Pareto e ABC

### `Ranking Cliente`

```dax
Ranking Cliente =
RANKX(ALLSELECTED(dCliente[RazaoSocial]), [Receita USD], , DESC, DENSE)
```

- **Formato:** `#,0`
- **Dependencias:** `Receita USD`

### `Ranking Produto`

```dax
Ranking Produto =
RANKX(ALLSELECTED(dProduto[Produto]), [Receita USD], , DESC, DENSE)
```

- **Formato:** `#,0`
- **Dependencias:** `Receita USD`

### `Ranking Pais`

```dax
Ranking Pais =
RANKX(ALLSELECTED(dPais[Pais]), [Receita USD], , DESC, DENSE)
```

- **Formato:** `#,0`
- **Dependencias:** `Receita USD`

### `Receita Acumulada Cliente`

```dax
Receita Acumulada Cliente =
VAR _R = [Ranking Cliente]
RETURN SUMX(FILTER(ALLSELECTED(dCliente[RazaoSocial]), [Ranking Cliente] <= _R), [Receita USD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Ranking Cliente`, `Receita USD`

### `Receita Acumulada Cliente %`

```dax
Receita Acumulada Cliente % =
DIVIDE([Receita Acumulada Cliente], CALCULATE([Receita USD], ALLSELECTED(dCliente[RazaoSocial])))
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita Acumulada Cliente`, `Receita USD`

### `Classe ABC Cliente`

```dax
Classe ABC Cliente =
VAR _P = [Receita Acumulada Cliente %]
RETURN SWITCH(TRUE(), ISBLANK(_P), BLANK(), _P <= 0.8, "A", _P <= 0.95, "B", "C")
```

- **Formato:** `texto`
- **Dependencias:** `Receita Acumulada Cliente %`

### `Receita Acumulada Produto %`

```dax
Receita Acumulada Produto % =
VAR _R = [Ranking Produto]
VAR _Ac = SUMX(FILTER(ALLSELECTED(dProduto[Produto]), [Ranking Produto] <= _R), [Receita USD])
RETURN DIVIDE(_Ac, CALCULATE([Receita USD], ALLSELECTED(dProduto[Produto])))
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Ranking Produto`, `Receita USD`

### `Classe ABC Produto`

```dax
Classe ABC Produto =
VAR _P = [Receita Acumulada Produto %]
RETURN SWITCH(TRUE(), ISBLANK(_P), BLANK(), _P <= 0.8, "A", _P <= 0.95, "B", "C")
```

- **Formato:** `texto`
- **Dependencias:** `Receita Acumulada Produto %`

### `Participacao Top 1`

```dax
Participacao Top 1 =
VAR _T = CALCULATE([Receita USD], ALLSELECTED(dCliente))
RETURN DIVIDE(MAXX(TOPN(1, ALLSELECTED(dCliente[ClienteID]), [Receita USD], DESC), [Receita USD]), _T)
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita USD`

### `Participacao Top 5`

```dax
Participacao Top 5 =
VAR _T = CALCULATE([Receita USD], ALLSELECTED(dCliente))
RETURN DIVIDE(SUMX(TOPN(5, ALLSELECTED(dCliente[ClienteID]), [Receita USD], DESC), [Receita USD]), _T)
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita USD`

### `Participacao Top 10`

```dax
Participacao Top 10 =
VAR _T = CALCULATE([Receita USD], ALLSELECTED(dCliente))
RETURN DIVIDE(SUMX(TOPN(10, ALLSELECTED(dCliente[ClienteID]), [Receita USD], DESC), [Receita USD]), _T)
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita USD`

### `Participacao Top 20`

```dax
Participacao Top 20 =
VAR _T = CALCULATE([Receita USD], ALLSELECTED(dCliente))
RETURN DIVIDE(SUMX(TOPN(20, ALLSELECTED(dCliente[ClienteID]), [Receita USD], DESC), [Receita USD]), _T)
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita USD`

### `Concentracao Carteira Vendedor`

Participacao do maior cliente na carteira do vendedor selecionado.

```dax
Concentracao Carteira Vendedor =
VAR _T = [Receita USD]
RETURN DIVIDE(MAXX(TOPN(1, VALUES(dCliente[ClienteID]), [Receita USD], DESC), [Receita USD]), _T)
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita USD`

## 08 Potencial

### `Potencial Anual USD`

```dax
Potencial Anual USD =
SUM(dCliente[PotencialAnualEstimadoUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Receita 12M`

```dax
Receita 12M =
[Receita Rolling 12M]
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita Rolling 12M`

### `Share of Wallet`

Receita dos ultimos 12 meses dividida pelo potencial anual estimado do cliente.

```dax
Share of Wallet =
DIVIDE([Receita 12M], [Potencial Anual USD])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Potencial Anual USD`, `Receita 12M`

### `Potencial Nao Capturado`

```dax
Potencial Nao Capturado =
MAX([Potencial Anual USD] - [Receita 12M], 0)
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Potencial Anual USD`, `Receita 12M`

### `Score de Oportunidade`

Prioriza clientes com grande gap absoluto e baixa penetracao.

```dax
Score de Oportunidade =
VAR _SoW = [Share of Wallet]
VAR _Gap = [Potencial Nao Capturado]
RETURN IF(ISBLANK(_SoW), BLANK(), _Gap * (1 - _SoW))
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Potencial Nao Capturado`, `Share of Wallet`

### `Categorias Compradas`

```dax
Categorias Compradas =
CALCULATE(DISTINCTCOUNT(dProduto[Categoria]), fVendas)
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Categorias Disponiveis`

```dax
Categorias Disponiveis =
CALCULATE(DISTINCTCOUNT(dProduto[Categoria]), ALL(dProduto))
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Penetracao Categorias %`

```dax
Penetracao Categorias % =
DIVIDE([Categorias Compradas], [Categorias Disponiveis])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Categorias Compradas`, `Categorias Disponiveis`

### `White Space Categorias`

```dax
White Space Categorias =
[Categorias Disponiveis] - [Categorias Compradas]
```

- **Formato:** `#,0`
- **Dependencias:** `Categorias Compradas`, `Categorias Disponiveis`

## 09 Metas

### `Meta Receita USD`

```dax
Meta Receita USD =
SUM(fMetas[MetaReceitaUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Meta Volume Kg`

```dax
Meta Volume Kg =
SUM(fMetas[MetaVolumeKg])
```

- **Formato:** `#,0.0`
- **Dependencias:** colunas base

### `Meta Margem USD`

```dax
Meta Margem USD =
SUM(fMetas[MetaMargemUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Meta Novos Clientes`

```dax
Meta Novos Clientes =
SUM(fMetas[MetaNovosClientes])
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Meta Pedidos`

```dax
Meta Pedidos =
SUM(fMetas[MetaPedidos])
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Atingimento %`

```dax
Atingimento % =
DIVIDE([Receita USD], [Meta Receita USD])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Meta Receita USD`, `Receita USD`

### `Gap Meta USD`

```dax
Gap Meta USD =
[Receita USD] - [Meta Receita USD]
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Meta Receita USD`, `Receita USD`

### `Atingimento Volume %`

```dax
Atingimento Volume % =
DIVIDE([Peso Total Kg], [Meta Volume Kg])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Meta Volume Kg`, `Peso Total Kg`

### `Atingimento Margem %`

```dax
Atingimento Margem % =
DIVIDE([Margem Bruta USD], [Meta Margem USD])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Margem Bruta USD`, `Meta Margem USD`

### `Atingimento Novos Clientes %`

```dax
Atingimento Novos Clientes % =
DIVIDE([Novos Clientes], [Meta Novos Clientes])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Meta Novos Clientes`, `Novos Clientes`

### `Status Meta`

```dax
Status Meta =
VAR _A = [Atingimento %]
RETURN SWITCH(TRUE(), ISBLANK(_A), BLANK(), _A >= 1.2, "Superado", _A >= 1, "Atingido",
    _A >= 0.9, "Proximo", _A >= 0.8, "Abaixo", "Muito abaixo")
```

- **Formato:** `texto`
- **Dependencias:** `Atingimento %`

## 10 Forecast e Orcamento

### `Receita Orcada USD`

```dax
Receita Orcada USD =
SUM(fOrcamento[ReceitaOrcadaUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Margem Orcada USD`

```dax
Margem Orcada USD =
SUM(fOrcamento[MargemOrcadaUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Volume Orcado Kg`

```dax
Volume Orcado Kg =
SUM(fOrcamento[VolumeOrcadoKg])
```

- **Formato:** `#,0.0`
- **Dependencias:** colunas base

### `Receita Forecast USD`

Considera apenas a revisao de forecast mais recente.

```dax
Receita Forecast USD =
VAR _UltRev = CALCULATE(MAX(fForecast[DataForecast]), ALLSELECTED(fForecast))
RETURN CALCULATE(SUM(fForecast[ReceitaForecastUSD]), fForecast[DataForecast] = _UltRev)
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Margem Forecast USD`

```dax
Margem Forecast USD =
VAR _UltRev = CALCULATE(MAX(fForecast[DataForecast]), ALLSELECTED(fForecast))
RETURN CALCULATE(SUM(fForecast[MargemForecastUSD]), fForecast[DataForecast] = _UltRev)
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Actual vs Budget USD`

```dax
Actual vs Budget USD =
[Receita USD] - [Receita Orcada USD]
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita Orcada USD`, `Receita USD`

### `Actual vs Budget %`

```dax
Actual vs Budget % =
DIVIDE([Receita USD], [Receita Orcada USD])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita Orcada USD`, `Receita USD`

### `Forecast x Meta`

```dax
Forecast x Meta =
[Receita Forecast USD] - [Meta Receita USD]
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Meta Receita USD`, `Receita Forecast USD`

### `Forecast x Orcado`

```dax
Forecast x Orcado =
[Receita Forecast USD] - [Receita Orcada USD]
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita Forecast USD`, `Receita Orcada USD`

### `Forecast Gap`

```dax
Forecast Gap =
[Receita Forecast USD] - [Receita USD]
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita Forecast USD`, `Receita USD`

### `Sazonalidade Historica %`

Peso historico do mes no total do periodo — base do orcamento adaptativo.

```dax
Sazonalidade Historica % =
VAR _Mes = SELECTEDVALUE(dCalendario[NumeroMes])
VAR _RecMes = CALCULATE([Receita USD], ALL(dCalendario), dCalendario[NumeroMes] = _Mes)
VAR _RecTot = CALCULATE([Receita USD], ALL(dCalendario))
RETURN DIVIDE(_RecMes, _RecTot)
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita USD`

### `Projecao Fechamento Ano`

Projecao linear de fechamento do ano com base no realizado acumulado.

```dax
Projecao Fechamento Ano =
VAR _Ano = MAX(dCalendario[Ano])
VAR _Realizado = CALCULATE([Receita USD], ALL(dCalendario), dCalendario[Ano] = _Ano,
        dCalendario[Data] <= MAX(fVendas[DataFaturamento]))
VAR _PesoRealizado = CALCULATE([Sazonalidade Historica %], ALL(dCalendario))
VAR _MesesDecorridos = CALCULATE(MAX(dCalendario[NumeroMes]), ALL(dCalendario),
        dCalendario[Data] <= MAX(fVendas[DataFaturamento]), dCalendario[Ano] = _Ano)
RETURN DIVIDE(_Realizado, DIVIDE(_MesesDecorridos, 12))
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Receita USD`, `Sazonalidade Historica %`

## 11 Logistica

### `Embarques`

```dax
Embarques =
DISTINCTCOUNT(fEmbarques[EmbarqueID])
```

- **Formato:** `#,0`
- **Dependencias:** colunas base

### `Entregas Realizadas`

```dax
Entregas Realizadas =
CALCULATE([Embarques], NOT(ISBLANK(fEmbarques[DiasAtraso])))
```

- **Formato:** `#,0`
- **Dependencias:** `Embarques`

### `Embarques Atrasados`

```dax
Embarques Atrasados =
CALCULATE([Embarques], fEmbarques[DiasAtraso] > 0)
```

- **Formato:** `#,0`
- **Dependencias:** `Embarques`

### `% Embarques Atrasados`

```dax
% Embarques Atrasados =
DIVIDE([Embarques Atrasados], [Entregas Realizadas])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Embarques Atrasados`, `Entregas Realizadas`

### `On Time %`

```dax
On Time % =
DIVIDE([Entregas Realizadas] - [Embarques Atrasados], [Entregas Realizadas])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Embarques Atrasados`, `Entregas Realizadas`

### `In Full %`

```dax
In Full % =
DIVIDE(CALCULATE([Embarques], fEmbarques[StatusEmbarque] <> "Aguardando embarque"), [Embarques])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Embarques`

### `OTIF %`

On Time In Full: proporcao de entregas no prazo e completas.

```dax
OTIF % =
[On Time %] * [In Full %]
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `In Full %`, `On Time %`

### `Lead Time Previsto`

```dax
Lead Time Previsto =
AVERAGE(fEmbarques[LeadTimePrevisto])
```

- **Formato:** `#,0.0`
- **Dependencias:** colunas base

### `Lead Time Real`

```dax
Lead Time Real =
AVERAGE(fEmbarques[LeadTimeReal])
```

- **Formato:** `#,0.0`
- **Dependencias:** colunas base

### `Desvio Lead Time`

```dax
Desvio Lead Time =
[Lead Time Real] - [Lead Time Previsto]
```

- **Formato:** `#,0.0`
- **Dependencias:** `Lead Time Previsto`, `Lead Time Real`

### `Dias de Atraso Medio`

```dax
Dias de Atraso Medio =
CALCULATE(AVERAGE(fEmbarques[DiasAtraso]), fEmbarques[DiasAtraso] > 0)
```

- **Formato:** `#,0.0`
- **Dependencias:** colunas base

### `Peso Embarcado Kg`

```dax
Peso Embarcado Kg =
SUM(fEmbarques[PesoKg])
```

- **Formato:** `#,0.0`
- **Dependencias:** colunas base

### `Frete Embarque USD`

```dax
Frete Embarque USD =
SUM(fEmbarques[FreteUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Frete por Kg`

```dax
Frete por Kg =
DIVIDE([Frete Embarque USD], [Peso Embarcado Kg])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Frete Embarque USD`, `Peso Embarcado Kg`

## 12 Financeiro

### `Contas a Receber`

```dax
Contas a Receber =
SUM(fRecebimentos[ValorUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Recebido USD`

```dax
Recebido USD =
SUM(fRecebimentos[ValorRecebidoUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Saldo em Aberto`

```dax
Saldo em Aberto =
SUM(fRecebimentos[SaldoUSD])
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** colunas base

### `Saldo Vencido`

```dax
Saldo Vencido =
CALCULATE([Saldo em Aberto], fRecebimentos[Status] IN {"Vencido", "Parcial"})
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Saldo em Aberto`

### `Inadimplencia %`

```dax
Inadimplencia % =
DIVIDE([Saldo Vencido], [Contas a Receber])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Contas a Receber`, `Saldo Vencido`

### `Dias Medios de Atraso`

```dax
Dias Medios de Atraso =
CALCULATE(AVERAGE(fRecebimentos[DiasAtraso]), fRecebimentos[DiasAtraso] > 0)
```

- **Formato:** `#,0.0`
- **Dependencias:** colunas base

### `Prazo Medio Recebimento`

PMR em dias entre faturamento e pagamento efetivo.

```dax
Prazo Medio Recebimento =
AVERAGEX(FILTER(fRecebimentos, NOT ISBLANK(fRecebimentos[DataPagamento])),
    DATEDIFF(fRecebimentos[DataFaturamento], fRecebimentos[DataPagamento], DAY))
```

- **Formato:** `#,0.0`
- **Dependencias:** colunas base

### `Faixa Aging`

```dax
Faixa Aging =
VAR _Hoje = MAX(dCalendario[Data])
VAR _D = AVERAGEX(fRecebimentos, DATEDIFF(fRecebimentos[DataVencimento], _Hoje, DAY))
RETURN SWITCH(TRUE(), _D < 0, "A vencer", _D <= 30, "1-30 dias", _D <= 60, "31-60 dias",
    _D <= 90, "61-90 dias", _D <= 180, "91-180 dias", "+180 dias")
```

- **Formato:** `texto`
- **Dependencias:** colunas base

### `Saldo Vencido +90`

```dax
Saldo Vencido +90 =
VAR _Hoje = MAX(dCalendario[Data])
RETURN CALCULATE([Saldo em Aberto],
    FILTER(fRecebimentos, DATEDIFF(fRecebimentos[DataVencimento], _Hoje, DAY) > 90))
```

- **Formato:** `"US$ "#,0.00`
- **Dependencias:** `Saldo em Aberto`

## 13 Cambio

### `Taxa Media USD BRL`

```dax
Taxa Media USD BRL =
CALCULATE(AVERAGE(fCambio[TaxaBRL]), fCambio[Moeda] = "USD")
```

- **Formato:** `#,0.0000`
- **Dependencias:** colunas base

### `Taxa Media Ponderada`

```dax
Taxa Media Ponderada =
DIVIDE([Receita BRL], [Receita USD])
```

- **Formato:** `#,0.0000`
- **Dependencias:** `Receita BRL`, `Receita USD`

### `Taxa Media LY`

```dax
Taxa Media LY =
CALCULATE([Taxa Media Ponderada], SAMEPERIODLASTYEAR(dCalendario[Data]))
```

- **Formato:** `#,0.0000`
- **Dependencias:** `Taxa Media Ponderada`

### `Efeito Cambio BRL`

Parcela da variacao da receita em BRL explicada apenas pela variacao cambial.

```dax
Efeito Cambio BRL =
[Receita USD] * ([Taxa Media Ponderada] - [Taxa Media LY])
```

- **Formato:** `"R$ "#,0.00`
- **Dependencias:** `Receita USD`, `Taxa Media LY`, `Taxa Media Ponderada`

### `Crescimento Operacional BRL`

```dax
Crescimento Operacional BRL =
VAR _LY_BRL = CALCULATE([Receita BRL], SAMEPERIODLASTYEAR(dCalendario[Data]))
RETURN [Receita BRL] - _LY_BRL - [Efeito Cambio BRL]
```

- **Formato:** `"R$ "#,0.00`
- **Dependencias:** `Efeito Cambio BRL`, `Receita BRL`

### `Variacao Cambial %`

```dax
Variacao Cambial % =
DIVIDE([Taxa Media Ponderada] - [Taxa Media LY], [Taxa Media LY])
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Taxa Media LY`, `Taxa Media Ponderada`

## 14 Inteligencia Comercial

### `Contribuicao para Crescimento`

Quanto o elemento explica da variacao total de receita do periodo.

```dax
Contribuicao para Crescimento =
DIVIDE([Receita YoY], CALCULATE([Receita YoY], ALLSELECTED()))
```

- **Formato:** `#,0.0 %`
- **Dependencias:** `Receita YoY`

### `Maior Crescimento Mercado`

```dax
Maior Crescimento Mercado =
VAR _T = TOPN(1, ALLSELECTED(dPais[Pais]), [Receita YoY], DESC)
RETURN CONCATENATEX(_T, dPais[Pais], ", ")
```

- **Formato:** `texto`
- **Dependencias:** `Receita YoY`

### `Maior Queda Mercado`

```dax
Maior Queda Mercado =
VAR _T = TOPN(1, ALLSELECTED(dPais[Pais]), [Receita YoY], ASC)
RETURN CONCATENATEX(_T, dPais[Pais], ", ")
```

- **Formato:** `texto`
- **Dependencias:** `Receita YoY`

### `Cliente Maior Queda`

```dax
Cliente Maior Queda =
VAR _T = TOPN(1, ALLSELECTED(dCliente[RazaoSocial]), [Receita YoY], ASC)
RETURN CONCATENATEX(_T, dCliente[RazaoSocial], ", ")
```

- **Formato:** `texto`
- **Dependencias:** `Receita YoY`

### `Texto Insight Crescimento`

Texto dinamico com sustentacao matematica para a area de insights.

```dax
Texto Insight Crescimento =
VAR _Total = CALCULATE([Receita YoY], ALLSELECTED(dPais))
VAR _TopPais = TOPN(1, ALLSELECTED(dPais[Pais]), [Receita YoY], DESC)
VAR _Nome = CONCATENATEX(_TopPais, dPais[Pais], ", ")
VAR _Val = MAXX(_TopPais, [Receita YoY])
VAR _Part = DIVIDE(_Val, _Total)
RETURN IF(ISBLANK(_Total) || _Total = 0, "Sem base comparativa no periodo selecionado.",
    _Nome & " respondeu por " & FORMAT(_Part, "0.0%") & " da variacao de receita do periodo ("
    & FORMAT(_Val, "$#,0,,.0M") & ").")
```

- **Formato:** `texto`
- **Dependencias:** `Receita YoY`

### `Texto Insight Margem`

```dax
Texto Insight Margem =
VAR _pp = [Margem YoY p.p.]
RETURN IF(ISBLANK(_pp), "Sem comparativo YoY.",
    "Margem bruta " & IF(_pp >= 0, "avancou ", "recuou ") & FORMAT(ABS(_pp), "0.0")
    & " p.p. YoY, hoje em " & FORMAT([Margem Bruta %], "0.0%") & ".")
```

- **Formato:** `texto`
- **Dependencias:** `Margem Bruta %`, `Margem YoY p.p.`

### `Alerta Rota Critica`

```dax
Alerta Rota Critica =
VAR _T = TOPN(1, ALLSELECTED(dPais[Pais]), [% Embarques Atrasados], DESC)
VAR _Nome = CONCATENATEX(_T, dPais[Pais], ", ")
VAR _V = MAXX(_T, [% Embarques Atrasados])
RETURN IF(ISBLANK(_V), BLANK(), _Nome & ": " & FORMAT(_V, "0.0%") & " de entregas atrasadas")
```

- **Formato:** `texto`
- **Dependencias:** colunas base

## 15 Formatacao

### `Cor Semaforo Meta`

```dax
Cor Semaforo Meta =
VAR _A = [Atingimento %]
RETURN SWITCH(TRUE(), ISBLANK(_A), "#8C96A5", _A >= 1, "#1F8A70", _A >= 0.9, "#D9A441", "#C0453B")
```

- **Formato:** `texto`
- **Dependencias:** `Atingimento %`

### `Cor Variacao`

```dax
Cor Variacao =
IF([Receita YoY] >= 0, "#1F8A70", "#C0453B")
```

- **Formato:** `texto`
- **Dependencias:** `Receita YoY`

### `Icone Tendencia`

```dax
Icone Tendencia =
IF([Receita YoY] >= 0, "▲", "▼")
```

- **Formato:** `texto`
- **Dependencias:** `Receita YoY`

### `KPI Receita Contexto`

```dax
KPI Receita Contexto =
IF(ISBLANK([Receita LY]), "sem comparativo",
    [Icone Tendencia] & " " & FORMAT([Receita YoY %], "0.0%") & " YoY  ("
    & FORMAT([Receita YoY], "$#,0,,.1M") & ")")
```

- **Formato:** `texto`
- **Dependencias:** `Icone Tendencia`, `Receita LY`, `Receita YoY`, `Receita YoY %`

## 16 Titulos Dinamicos

### `Titulo Periodo`

```dax
Titulo Periodo =
VAR _Ini = MIN(dCalendario[Data]) VAR _Fim = MAX(dCalendario[Data])
RETURN IF(YEAR(_Ini) = YEAR(_Fim) && MONTH(_Ini) = MONTH(_Fim),
    FORMAT(_Ini, "mmm/yyyy"),
    FORMAT(_Ini, "mmm/yy") & " - " & FORMAT(_Fim, "mmm/yy"))
```

- **Formato:** `texto`
- **Dependencias:** colunas base

### `Titulo Filtros`

```dax
Titulo Filtros =
VAR _Cont = IF(ISFILTERED(dPais[Continente]),
        CONCATENATEX(VALUES(dPais[Continente]), dPais[Continente], ", "), "Global")
RETURN _Cont & " — " & [Titulo Periodo]
```

- **Formato:** `texto`
- **Dependencias:** `Titulo Periodo`

### `Titulo Receita por Pais`

```dax
Titulo Receita por Pais =
"Receita por Pais — " & [Titulo Filtros]
```

- **Formato:** `texto`
- **Dependencias:** `Titulo Filtros`

### `Titulo Performance Comercial`

```dax
Titulo Performance Comercial =
"Performance Comercial — " & [Titulo Filtros]
```

- **Formato:** `texto`
- **Dependencias:** `Titulo Filtros`

### `Titulo Rentabilidade`

```dax
Titulo Rentabilidade =
"Ponte de Rentabilidade — " & [Titulo Periodo]
```

- **Formato:** `texto`
- **Dependencias:** `Titulo Periodo`
