#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o Semantic Model (TMDL) do projeto AuroraBrasilExportadora.pbip."""
import os, uuid, hashlib, json
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(BASE, "dados")
PBI = os.path.join(BASE, "PowerBI")
SM = os.path.join(PBI, "AuroraBrasilExportadora.SemanticModel")
DEF = os.path.join(SM, "definition")
TBL = os.path.join(DEF, "tables")
for p in [PBI, SM, DEF, TBL]:
    os.makedirs(p, exist_ok=True)

def lt(seed):
    """lineageTag deterministico (reprodutivel entre execucoes)."""
    h = hashlib.md5(seed.encode()).hexdigest()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"

# ---------------------------------------------------------------- tipos
DATE_COLS = {"Data", "DataCadastro", "DataAdmissao", "DataPedido", "DataFaturamento",
             "InicioMes", "FimMes", "DataPrevistaEmbarque", "DataRealEmbarque",
             "DataPrevistaEntrega", "DataRealEntrega", "DataVencimento",
             "DataPagamento", "DataForecast"}
INT_COLS = {"Ano", "NumeroMes", "AnoMesNumero", "SemanaAno", "NumeroDiaSemana", "ClienteID",
            "ProdutoID", "VendedorID", "PaisID", "PortoID", "TransportadoraID", "VendaID",
            "EmbarqueID", "RecebimentoID", "PaisDestinoID", "PortoOrigemID", "PortoDestinoID",
            "Quantidade", "VidaUtilDias", "PrazoPagamentoPadrao", "VendedorResponsavelID",
            "LeadTimeMedio", "LeadTimePrevisto", "LeadTimeReal", "DiasAtraso", "Mes",
            "MetaNovosClientes", "MetaPedidos"}

FMT_USD = '"US$ "#,0.00'
FMT_NUM = "#,0.00"
FMT_INT = "#,0"

# Descricoes de tabela
TAB_DESC = {
 "dCalendario": "Dimensao de datas continua de 01/01/2022 a 31/07/2026. Marcada como tabela de datas.",
 "dCliente": "Dimensao de clientes internacionais B2B, incluindo potencial anual estimado para Share of Wallet.",
 "dProduto": "Dimensao de SKUs exportados, com categoria, embalagem, custo base e margem alvo.",
 "dVendedor": "Dimensao da equipe comercial com hierarquia Diretor > Gerente Regional > Executivo de Contas.",
 "dPais": "Dimensao geografica de mercados de destino, com risco, lead time e tarifa media de importacao.",
 "dPorto": "Dimensao de portos e aeroportos de origem e destino (UN/LOCODE).",
 "dTransportadora": "Dimensao de operadores logisticos internacionais.",
 "fVendas": "Fato transacional na granularidade item de pedido faturado. Tabela principal do modelo.",
 "fEmbarques": "Fato logistico na granularidade pedido embarcado.",
 "fCambio": "Fato de cotacoes diarias por moeda contra o BRL.",
 "fMetas": "Fato de metas comerciais na granularidade mes x vendedor.",
 "fOrcamento": "Fato de orcamento anual aprovado na granularidade mes x regiao x categoria.",
 "fForecast": "Fato de forecast com revisoes periodicas (Jan/Mai/Set) na granularidade mes x regiao x categoria.",
 "fRecebimentos": "Fato financeiro de contas a receber na granularidade invoice.",
}

# Colunas ocultas (chaves e tecnicas)
HIDE = {"Data" if False else "ClienteID", "ProdutoID", "VendedorID", "PaisID", "PortoID", "TransportadoraID",
        "VendaID", "EmbarqueID", "RecebimentoID", "PaisDestinoID", "PortoOrigemID",
        "PortoDestinoID", "VendedorResponsavelID", "AnoMesNumero", "NumeroMes",
        "NumeroDiaSemana", "InicioMes", "FimMes"}

SORT_BY = {("dCalendario", "Mes"): "NumeroMes",
           ("dCalendario", "MesAbreviado"): "NumeroMes",
           ("dCalendario", "AnoMes"): "AnoMesNumero",
           ("dCalendario", "DiaSemana"): "NumeroDiaSemana",
           ("fMetas", "AnoMes"): "AnoMesNumero",
           ("fOrcamento", "AnoMes"): "AnoMesNumero",
           ("fForecast", "AnoMes"): "AnoMesNumero"}


M_INDENT = "\t\t\t\t"


def m_query(tabela, cols_tipos):
    """Power Query parametrizado por pBasePath, com etapas nomeadas.

    Toda linha recebe o mesmo prefixo de tabs (M_INDENT); a indentacao relativa
    do M usa espacos. O parser TMDL usa a indentacao da primeira linha do bloco
    como prefixo e a remove de todas as demais - misturar tabs e espacos entre a
    primeira linha e as seguintes quebra a leitura do modelo.
    """
    tipos = ",".join(f'{{"{c}", {t}}}' for c, t in cols_tipos)
    linhas = [
        'let',
        '    Origem = Csv.Document(',
        f'        File.Contents(pBasePath & "{tabela}.csv"),',
        '        [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]',
        '    ),',
        '    CabecalhoPromovido = Table.PromoteHeaders(Origem, [PromoteAllScalars = true]),',
        '    TiposAplicados = Table.TransformColumnTypes(',
        '        CabecalhoPromovido,',
        f'        {{{tipos}}},',
        '        "pt-BR"',
        '    ),',
        # Nao usar Table.RemoveRowsWithErrors: ele descarta a linha inteira em
        # silencio quando um unico valor nao converte (ex.: LeadTimeReal vazio em
        # embarque nao entregue). Aqui o erro vira null e a contagem de linhas
        # continua batendo com ValidacaoDados.md.
        '    ErrosTratados = Table.ReplaceErrorValues(',
        '        TiposAplicados,',
        '        List.Transform(Table.ColumnNames(TiposAplicados), each {_, null})',
        '    )',
        'in',
        '    ErrosTratados',
    ]
    return "\n".join(M_INDENT + l for l in linhas)


def tipo_pq(col, serie):
    if col in DATE_COLS:
        return "type date"
    if col in INT_COLS:
        return "Int64.Type"
    if pd.api.types.is_float_dtype(serie):
        return "type number"
    return "type text"


def tipo_tmdl(col, serie):
    if col in DATE_COLS:
        return "dateTime"
    if col in INT_COLS:
        return "int64"
    if pd.api.types.is_float_dtype(serie):
        return "double"
    return "string"


def gerar_tabela_tmdl(nome):
    df = pd.read_csv(os.path.join(DADOS, f"{nome}.csv"), sep=";", decimal=",",
                     encoding="utf-8-sig", nrows=4000)
    # Em TMDL a descricao (///) vem ANTES da declaracao do objeto e na mesma
    # indentacao dela - para a tabela, portanto, na coluna 0.
    linhas = []
    if nome in TAB_DESC:
        linhas.append(f"/// {TAB_DESC[nome]}")
    linhas += [f"table {nome}", f"\tlineageTag: {lt('t'+nome)}"]
    if nome == "dCalendario":
        linhas.append("\tdataCategory: Time")
    linhas.append("")
    cols_tipos = []
    for c in df.columns:
        dt = tipo_tmdl(c, df[c])
        cols_tipos.append((c, tipo_pq(c, df[c])))
        summarize = "none"
        if dt in ("double", "int64") and c not in HIDE:
            summarize = "sum"
        if dt in ("double", "int64") and c in HIDE:
            summarize = "none"
        linhas.append(f"\tcolumn {c}")
        linhas.append(f"\t\tdataType: {dt}")
        if dt == "dateTime":
            linhas.append('\t\tformatString: yyyy-mm-dd')
        elif dt == "double":
            linhas.append(f'\t\tformatString: {FMT_NUM}')
        elif dt == "int64":
            linhas.append(f'\t\tformatString: {FMT_INT}')
        if c in HIDE:
            linhas.append("\t\tisHidden")
        if nome == "dCalendario" and c == "Data":
            linhas.append("\t\tisKey")
        linhas.append(f"\t\tlineageTag: {lt(nome+'.'+c)}")
        linhas.append(f"\t\tsummarizeBy: {summarize}")
        linhas.append(f"\t\tsourceColumn: {c}")
        if (nome, c) in SORT_BY:
            linhas.append(f"\t\tsortByColumn: {SORT_BY[(nome, c)]}")
        linhas.append("")
        linhas.append("\t\tannotation SummarizationSetBy = Automatic")
        linhas.append("")
    linhas.append(f"\tpartition {nome} = m")
    linhas.append("\t\tmode: import")
    linhas.append("\t\tsource =")
    linhas.append(m_query(nome, cols_tipos))
    linhas.append("")
    linhas.append("\tannotation PBI_ResultType = Table")
    linhas.append("")
    return "\n".join(linhas)


TABELAS = ["dCalendario", "dCliente", "dProduto", "dVendedor", "dPais", "dPorto",
           "dTransportadora", "fVendas", "fEmbarques", "fCambio", "fMetas",
           "fOrcamento", "fForecast", "fRecebimentos"]


# ---------------------------------------------------------------- MEDIDAS
def M(nome, dax, pasta, fmt=FMT_USD, desc="", fence=False):
    return dict(nome=nome, dax=dax, pasta=pasta, fmt=fmt, desc=desc, fence=fence)


def M_html(nome, arquivo, desc=""):
    """Medida que devolve HTML, lida de scripts/html/<arquivo>.

    Vai para o TMDL entre ``` (mesmo idioma que o Power BI usa para expressoes
    com HTML/aspas/caracteres especiais) e sem formatString - o valor e texto.
    """
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html", arquivo)
    with open(caminho, encoding="utf-8") as f:
        dax = f.read().rstrip()
    return M(nome, dax, "17 Paineis HTML", fmt=None, desc=desc, fence=True)

FP = "#,0.0 %"      # percentual
FQ = "#,0"          # inteiro
FD = "#,0.0"        # decimal 1 casa
FBRL = '"R$ "#,0.00'

MEDIDAS = [
# ---------------- 01 Receita
M("Receita Bruta USD", "SUM(fVendas[ReceitaBrutaUSD])", "01 Receita", FMT_USD,
  "Faturamento bruto em USD antes de descontos comerciais."),
M("Descontos USD", "SUM(fVendas[DescontoUSD])", "01 Receita", FMT_USD,
  "Total de descontos comerciais concedidos."),
M("Desconto %", "DIVIDE([Descontos USD], [Receita Bruta USD])", "01 Receita", FP),
M("Receita USD", "SUM(fVendas[ReceitaLiquidaUSD])", "01 Receita", FMT_USD,
  "Receita liquida em USD. Medida base de todo o relatorio."),
M("Receita BRL", "SUM(fVendas[ReceitaLiquidaBRL])", "01 Receita", FBRL,
  "Receita liquida convertida a BRL pela taxa da data de faturamento."),
M("Receita por Kg", "DIVIDE([Receita USD], [Peso Total Kg])", "01 Receita", FMT_USD),
M("Receita Pedido", "SUM(fVendas[ReceitaLiquidaUSD])", "01 Receita", FMT_USD),
M("Receita por Data de Pedido",
  "CALCULATE([Receita USD], USERELATIONSHIP(dCalendario[Data], fVendas[DataPedido]))",
  "01 Receita", FMT_USD, "Receita reconhecida pela data do pedido (relacionamento inativo)."),
# ---------------- 02 Crescimento
M("Receita LY", "CALCULATE([Receita USD], SAMEPERIODLASTYEAR(dCalendario[Data]))", "02 Crescimento", FMT_USD),
M("Receita YoY", "[Receita USD] - [Receita LY]", "02 Crescimento", FMT_USD),
M("Receita YoY %", "DIVIDE([Receita YoY], [Receita LY])", "02 Crescimento", FP),
M("Receita PM", "CALCULATE([Receita USD], DATEADD(dCalendario[Data], -1, MONTH))", "02 Crescimento", FMT_USD),
M("Receita MoM", "[Receita USD] - [Receita PM]", "02 Crescimento", FMT_USD),
M("Receita MoM %", "DIVIDE([Receita MoM], [Receita PM])", "02 Crescimento", FP),
M("Receita YTD", "TOTALYTD([Receita USD], dCalendario[Data])", "02 Crescimento", FMT_USD),
M("Receita YTD LY",
  "CALCULATE([Receita YTD], SAMEPERIODLASTYEAR(dCalendario[Data]))", "02 Crescimento", FMT_USD),
M("Receita YTD YoY %", "DIVIDE([Receita YTD] - [Receita YTD LY], [Receita YTD LY])", "02 Crescimento", FP),
M("Receita Rolling 3M",
  "CALCULATE([Receita USD], DATESINPERIOD(dCalendario[Data], MAX(dCalendario[Data]), -3, MONTH))",
  "02 Crescimento", FMT_USD),
M("Receita Rolling 6M",
  "CALCULATE([Receita USD], DATESINPERIOD(dCalendario[Data], MAX(dCalendario[Data]), -6, MONTH))",
  "02 Crescimento", FMT_USD),
M("Receita Rolling 12M",
  "CALCULATE([Receita USD], DATESINPERIOD(dCalendario[Data], MAX(dCalendario[Data]), -12, MONTH))",
  "02 Crescimento", FMT_USD),
M("Receita Media Mensal 12M", "DIVIDE([Receita Rolling 12M], 12)", "02 Crescimento", FMT_USD),
M("CAGR Receita",
  """VAR _Ini = CALCULATE([Receita USD], ALL(dCalendario), dCalendario[Ano] = MIN(dCalendario[Ano]))
VAR _Fim = CALCULATE([Receita USD], ALL(dCalendario), dCalendario[Ano] = MAX(dCalendario[Ano]))
VAR _N = MAX(dCalendario[Ano]) - MIN(dCalendario[Ano])
RETURN IF(_N > 0 && _Ini > 0, ( _Fim / _Ini ) ^ DIVIDE(1, _N) - 1)""", "02 Crescimento", FP),
M("Margem YoY p.p.",
  "[Margem Bruta %] - CALCULATE([Margem Bruta %], SAMEPERIODLASTYEAR(dCalendario[Data]))",
  "02 Crescimento", "#,0.0", "Variacao da margem percentual em pontos percentuais versus ano anterior."),
M("Volume YoY %",
  """VAR _LY = CALCULATE([Peso Total Kg], SAMEPERIODLASTYEAR(dCalendario[Data]))
RETURN DIVIDE([Peso Total Kg] - _LY, _LY)""", "02 Crescimento", FP),
# ---------------- 03 Volume
M("Quantidade", "SUM(fVendas[Quantidade])", "03 Volume", FQ),
M("Peso Total Kg", "SUM(fVendas[PesoTotalKg])", "03 Volume", FD),
M("Toneladas", "DIVIDE([Peso Total Kg], 1000)", "03 Volume", FD),
M("Pedidos", "DISTINCTCOUNT(fVendas[PedidoID])", "03 Volume", FQ),
M("Linhas de Pedido", "COUNTROWS(fVendas)", "03 Volume", FQ),
M("Ticket Medio USD", "DIVIDE([Receita USD], [Pedidos])", "03 Volume", FMT_USD),
M("Ticket Medio BRL", "DIVIDE([Receita BRL], [Pedidos])", "03 Volume", FBRL),
M("Preco Medio por Kg", "DIVIDE([Receita Bruta USD], [Peso Total Kg])", "03 Volume", FMT_USD),
# ---------------- 04 Margem
M("Custo Produto USD", "SUM(fVendas[CustoProdutoUSD])", "04 Margem", FMT_USD),
M("Frete USD", "SUM(fVendas[FreteUSD])", "04 Margem", FMT_USD),
M("Seguro USD", "SUM(fVendas[SeguroUSD])", "04 Margem", FMT_USD),
M("Despesas Exportacao USD", "SUM(fVendas[DespesasExportacaoUSD])", "04 Margem", FMT_USD),
M("Custo Total USD", "SUM(fVendas[CustoTotalUSD])", "04 Margem", FMT_USD),
M("Margem Bruta USD", "SUM(fVendas[MargemBrutaUSD])", "04 Margem", FMT_USD,
  "Receita liquida menos custo de produto, frete, seguro e despesas de exportacao."),
M("Margem Bruta BRL", "SUMX(fVendas, fVendas[MargemBrutaUSD] * fVendas[TaxaCambio])", "04 Margem", FBRL),
M("Margem Bruta %", "DIVIDE([Margem Bruta USD], [Receita USD])", "04 Margem", FP),
M("Margem por Kg", "DIVIDE([Margem Bruta USD], [Peso Total Kg])", "04 Margem", FMT_USD),
M("Custo por Kg", "DIVIDE([Custo Total USD], [Peso Total Kg])", "04 Margem", FMT_USD),
M("Frete % Receita", "DIVIDE([Frete USD], [Receita USD])", "04 Margem", FP),
M("Impacto Desconto %", "DIVIDE([Descontos USD], [Receita Bruta USD])", "04 Margem", FP),
M("Margem LY", "CALCULATE([Margem Bruta USD], SAMEPERIODLASTYEAR(dCalendario[Data]))", "04 Margem", FMT_USD),
M("Margem YoY %", "DIVIDE([Margem Bruta USD] - [Margem LY], [Margem LY])", "04 Margem", FP),
M("Margem YTD", "TOTALYTD([Margem Bruta USD], dCalendario[Data])", "04 Margem", FMT_USD),
# ---------------- 05 Clientes
M("Clientes Ativos", "CALCULATE(DISTINCTCOUNT(fVendas[ClienteID]), fVendas[StatusPedido] = \"Faturado\")",
  "05 Clientes", FQ, "Clientes com ao menos um faturamento no contexto de filtro."),
M("Clientes 90D",
  """VAR _Fim = MAX(dCalendario[Data])
RETURN CALCULATE(DISTINCTCOUNT(fVendas[ClienteID]),
    DATESINPERIOD(dCalendario[Data], _Fim, -90, DAY), ALL(dCalendario))""", "05 Clientes", FQ),
M("Clientes Base", "COUNTROWS(dCliente)", "05 Clientes", FQ),
M("Novos Clientes",
  """VAR _Ini = MIN(dCalendario[Data])
VAR _Fim = MAX(dCalendario[Data])
RETURN COUNTROWS(FILTER(VALUES(dCliente[ClienteID]),
    VAR _Prim = CALCULATE(MIN(fVendas[DataFaturamento]), ALL(dCalendario))
    RETURN NOT ISBLANK(_Prim) && _Prim >= _Ini && _Prim <= _Fim))""",
  "05 Clientes", FQ, "Clientes cuja primeira compra historica ocorreu dentro do periodo filtrado."),
M("Clientes Perdidos",
  """VAR _Fim = MAX(dCalendario[Data])
RETURN COUNTROWS(FILTER(VALUES(dCliente[ClienteID]),
    VAR _Ult = CALCULATE(MAX(fVendas[DataFaturamento]), ALL(dCalendario), dCalendario[Data] <= _Fim)
    RETURN NOT ISBLANK(_Ult) && _Ult < _Fim - 365))""",
  "05 Clientes", FQ, "Sem compras nos ultimos 365 dias em relacao ao fim do periodo."),
M("Clientes Em Risco",
  """VAR _Fim = MAX(dCalendario[Data])
RETURN COUNTROWS(FILTER(VALUES(dCliente[ClienteID]),
    VAR _Ult = CALCULATE(MAX(fVendas[DataFaturamento]), ALL(dCalendario), dCalendario[Data] <= _Fim)
    RETURN NOT ISBLANK(_Ult) && _Ult < _Fim - 180 && _Ult >= _Fim - 365))""", "05 Clientes", FQ),
M("Clientes Inativos 90D",
  """VAR _Fim = MAX(dCalendario[Data])
RETURN COUNTROWS(FILTER(VALUES(dCliente[ClienteID]),
    VAR _Ult = CALCULATE(MAX(fVendas[DataFaturamento]), ALL(dCalendario), dCalendario[Data] <= _Fim)
    RETURN NOT ISBLANK(_Ult) && _Ult < _Fim - 90))""", "05 Clientes", FQ),
M("Clientes Reativados",
  """VAR _Ini = MIN(dCalendario[Data])
VAR _Fim = MAX(dCalendario[Data])
RETURN COUNTROWS(FILTER(VALUES(dCliente[ClienteID]),
    VAR _Comprou = CALCULATE([Pedidos]) > 0
    VAR _Ant = CALCULATE(MAX(fVendas[DataFaturamento]), ALL(dCalendario), dCalendario[Data] < _Ini)
    RETURN _Comprou && NOT ISBLANK(_Ant) && _Ant < _Ini - 180))""",
  "05 Clientes", FQ, "Comprou no periodo apos 180 dias ou mais sem compras."),
M("Taxa de Churn %", "DIVIDE([Clientes Perdidos], [Clientes Perdidos] + [Clientes Ativos])", "05 Clientes", FP),
M("Receita em Risco",
  """VAR _Fim = MAX(dCalendario[Data])
RETURN SUMX(FILTER(VALUES(dCliente[ClienteID]),
    VAR _Ult = CALCULATE(MAX(fVendas[DataFaturamento]), ALL(dCalendario), dCalendario[Data] <= _Fim)
    RETURN NOT ISBLANK(_Ult) && _Ult < _Fim - 180),
    CALCULATE([Receita Rolling 12M]))""", "05 Clientes", FMT_USD),
M("Receita por Cliente", "DIVIDE([Receita USD], [Clientes Ativos])", "05 Clientes", FMT_USD),
M("Frequencia Media", "DIVIDE([Pedidos], [Clientes Ativos])", "05 Clientes", FD),
M("Recencia Dias",
  "DATEDIFF(CALCULATE(MAX(fVendas[DataFaturamento])), MAX(dCalendario[Data]), DAY)", "05 Clientes", FQ),
M("Recencia Media Dias", "AVERAGEX(VALUES(dCliente[ClienteID]), [Recencia Dias])", "05 Clientes", FD),
M("Data Primeira Compra", "CALCULATE(MIN(fVendas[DataFaturamento]), ALL(dCalendario))",
  "05 Clientes", "yyyy-mm-dd"),
M("Data Ultima Compra", "CALCULATE(MAX(fVendas[DataFaturamento]))", "05 Clientes", "yyyy-mm-dd"),
M("LTV Estimado",
  "[Receita Rolling 12M] * 3 * [Margem Bruta %]", "05 Clientes", FMT_USD,
  "Proxy de valor vitalicio: receita 12M projetada em 3 anos ponderada pela margem."),
# ---------------- 06 RFV
M("Score Recencia",
  """VAR _R = [Recencia Dias]
RETURN SWITCH(TRUE(), ISBLANK(_R), BLANK(), _R <= 45, 5, _R <= 90, 4, _R <= 180, 3, _R <= 365, 2, 1)""",
  "06 RFV", FQ),
M("Score Frequencia",
  """VAR _F = [Pedidos]
RETURN SWITCH(TRUE(), _F = 0, BLANK(), _F >= 40, 5, _F >= 20, 4, _F >= 10, 3, _F >= 4, 2, 1)""",
  "06 RFV", FQ),
M("Score Valor",
  """VAR _V = [Receita USD]
VAR _Rk = RANKX(ALLSELECTED(dCliente[ClienteID]), [Receita USD], , DESC)
VAR _N = COUNTROWS(ALLSELECTED(dCliente[ClienteID]))
VAR _P = DIVIDE(_Rk, _N)
RETURN IF(ISBLANK(_V), BLANK(), SWITCH(TRUE(), _P <= 0.1, 5, _P <= 0.3, 4, _P <= 0.6, 3, _P <= 0.85, 2, 1))""",
  "06 RFV", FQ),
M("Score RFV Total", "[Score Recencia] + [Score Frequencia] + [Score Valor]", "06 RFV", FQ),
M("Segmento RFV",
  """VAR _R = [Score Recencia] VAR _F = [Score Frequencia] VAR _V = [Score Valor]
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
    "Perdidos")""", "06 RFV", "", "Classificacao RFV dinamica calculada no contexto do relatorio."),
# ---------------- 07 Pareto / ABC / Concentracao
M("Ranking Cliente", "RANKX(ALLSELECTED(dCliente[RazaoSocial]), [Receita USD], , DESC, DENSE)",
  "07 Pareto e ABC", FQ),
M("Ranking Produto", "RANKX(ALLSELECTED(dProduto[Produto]), [Receita USD], , DESC, DENSE)",
  "07 Pareto e ABC", FQ),
M("Ranking Pais", "RANKX(ALLSELECTED(dPais[Pais]), [Receita USD], , DESC, DENSE)", "07 Pareto e ABC", FQ),
M("Receita Acumulada Cliente",
  """VAR _R = [Ranking Cliente]
RETURN SUMX(FILTER(ALLSELECTED(dCliente[RazaoSocial]), [Ranking Cliente] <= _R), [Receita USD])""",
  "07 Pareto e ABC", FMT_USD),
M("Receita Acumulada Cliente %",
  "DIVIDE([Receita Acumulada Cliente], CALCULATE([Receita USD], ALLSELECTED(dCliente[RazaoSocial])))",
  "07 Pareto e ABC", FP),
M("Classe ABC Cliente",
  """VAR _P = [Receita Acumulada Cliente %]
RETURN SWITCH(TRUE(), ISBLANK(_P), BLANK(), _P <= 0.8, "A", _P <= 0.95, "B", "C")""",
  "07 Pareto e ABC", ""),
M("Receita Acumulada Produto %",
  """VAR _R = [Ranking Produto]
VAR _Ac = SUMX(FILTER(ALLSELECTED(dProduto[Produto]), [Ranking Produto] <= _R), [Receita USD])
RETURN DIVIDE(_Ac, CALCULATE([Receita USD], ALLSELECTED(dProduto[Produto])))""", "07 Pareto e ABC", FP),
M("Classe ABC Produto",
  """VAR _P = [Receita Acumulada Produto %]
RETURN SWITCH(TRUE(), ISBLANK(_P), BLANK(), _P <= 0.8, "A", _P <= 0.95, "B", "C")""",
  "07 Pareto e ABC", ""),
M("Participacao Top 1",
  """VAR _T = CALCULATE([Receita USD], ALLSELECTED(dCliente))
RETURN DIVIDE(MAXX(TOPN(1, ALLSELECTED(dCliente[ClienteID]), [Receita USD], DESC), [Receita USD]), _T)""",
  "07 Pareto e ABC", FP),
M("Participacao Top 5",
  """VAR _T = CALCULATE([Receita USD], ALLSELECTED(dCliente))
RETURN DIVIDE(SUMX(TOPN(5, ALLSELECTED(dCliente[ClienteID]), [Receita USD], DESC), [Receita USD]), _T)""",
  "07 Pareto e ABC", FP),
M("Participacao Top 10",
  """VAR _T = CALCULATE([Receita USD], ALLSELECTED(dCliente))
RETURN DIVIDE(SUMX(TOPN(10, ALLSELECTED(dCliente[ClienteID]), [Receita USD], DESC), [Receita USD]), _T)""",
  "07 Pareto e ABC", FP),
M("Participacao Top 20",
  """VAR _T = CALCULATE([Receita USD], ALLSELECTED(dCliente))
RETURN DIVIDE(SUMX(TOPN(20, ALLSELECTED(dCliente[ClienteID]), [Receita USD], DESC), [Receita USD]), _T)""",
  "07 Pareto e ABC", FP),
M("Concentracao Carteira Vendedor",
  """VAR _T = [Receita USD]
RETURN DIVIDE(MAXX(TOPN(1, VALUES(dCliente[ClienteID]), [Receita USD], DESC), [Receita USD]), _T)""",
  "07 Pareto e ABC", FP, "Participacao do maior cliente na carteira do vendedor selecionado."),
# ---------------- 08 Potencial
M("Potencial Anual USD", "SUM(dCliente[PotencialAnualEstimadoUSD])", "08 Potencial", FMT_USD),
M("Receita 12M", "[Receita Rolling 12M]", "08 Potencial", FMT_USD),
M("Share of Wallet", "DIVIDE([Receita 12M], [Potencial Anual USD])", "08 Potencial", FP,
  "Receita dos ultimos 12 meses dividida pelo potencial anual estimado do cliente."),
M("Potencial Nao Capturado", "MAX([Potencial Anual USD] - [Receita 12M], 0)", "08 Potencial", FMT_USD),
M("Score de Oportunidade",
  """VAR _SoW = [Share of Wallet]
VAR _Gap = [Potencial Nao Capturado]
RETURN IF(ISBLANK(_SoW), BLANK(), _Gap * (1 - _SoW))""", "08 Potencial", FMT_USD,
  "Prioriza clientes com grande gap absoluto e baixa penetracao."),
M("Categorias Compradas", "CALCULATE(DISTINCTCOUNT(dProduto[Categoria]), fVendas)", "08 Potencial", FQ),
M("Categorias Disponiveis", "CALCULATE(DISTINCTCOUNT(dProduto[Categoria]), ALL(dProduto))", "08 Potencial", FQ),
M("Penetracao Categorias %", "DIVIDE([Categorias Compradas], [Categorias Disponiveis])", "08 Potencial", FP),
M("White Space Categorias", "[Categorias Disponiveis] - [Categorias Compradas]", "08 Potencial", FQ),
# ---------------- 09 Metas
M("Meta Receita USD", "SUM(fMetas[MetaReceitaUSD])", "09 Metas", FMT_USD),
M("Meta Volume Kg", "SUM(fMetas[MetaVolumeKg])", "09 Metas", FD),
M("Meta Margem USD", "SUM(fMetas[MetaMargemUSD])", "09 Metas", FMT_USD),
M("Meta Novos Clientes", "SUM(fMetas[MetaNovosClientes])", "09 Metas", FQ),
M("Meta Pedidos", "SUM(fMetas[MetaPedidos])", "09 Metas", FQ),
M("Atingimento %", "DIVIDE([Receita USD], [Meta Receita USD])", "09 Metas", FP),
M("Gap Meta USD", "[Receita USD] - [Meta Receita USD]", "09 Metas", FMT_USD),
M("Atingimento Volume %", "DIVIDE([Peso Total Kg], [Meta Volume Kg])", "09 Metas", FP),
M("Atingimento Margem %", "DIVIDE([Margem Bruta USD], [Meta Margem USD])", "09 Metas", FP),
M("Atingimento Novos Clientes %", "DIVIDE([Novos Clientes], [Meta Novos Clientes])", "09 Metas", FP),
M("Status Meta",
  """VAR _A = [Atingimento %]
RETURN SWITCH(TRUE(), ISBLANK(_A), BLANK(), _A >= 1.2, "Superado", _A >= 1, "Atingido",
    _A >= 0.9, "Proximo", _A >= 0.8, "Abaixo", "Muito abaixo")""", "09 Metas", ""),
# ---------------- 10 Forecast e Orcamento
M("Receita Orcada USD", "SUM(fOrcamento[ReceitaOrcadaUSD])", "10 Forecast e Orcamento", FMT_USD),
M("Margem Orcada USD", "SUM(fOrcamento[MargemOrcadaUSD])", "10 Forecast e Orcamento", FMT_USD),
M("Volume Orcado Kg", "SUM(fOrcamento[VolumeOrcadoKg])", "10 Forecast e Orcamento", FD),
M("Receita Forecast USD",
  """VAR _UltRev = CALCULATE(MAX(fForecast[DataForecast]), ALLSELECTED(fForecast))
RETURN CALCULATE(SUM(fForecast[ReceitaForecastUSD]), fForecast[DataForecast] = _UltRev)""",
  "10 Forecast e Orcamento", FMT_USD, "Considera apenas a revisao de forecast mais recente."),
M("Margem Forecast USD",
  """VAR _UltRev = CALCULATE(MAX(fForecast[DataForecast]), ALLSELECTED(fForecast))
RETURN CALCULATE(SUM(fForecast[MargemForecastUSD]), fForecast[DataForecast] = _UltRev)""",
  "10 Forecast e Orcamento", FMT_USD),
M("Actual vs Budget USD", "[Receita USD] - [Receita Orcada USD]", "10 Forecast e Orcamento", FMT_USD),
M("Actual vs Budget %", "DIVIDE([Receita USD], [Receita Orcada USD])", "10 Forecast e Orcamento", FP),
M("Forecast x Meta", "[Receita Forecast USD] - [Meta Receita USD]", "10 Forecast e Orcamento", FMT_USD),
M("Forecast x Orcado", "[Receita Forecast USD] - [Receita Orcada USD]", "10 Forecast e Orcamento", FMT_USD),
M("Forecast Gap", "[Receita Forecast USD] - [Receita USD]", "10 Forecast e Orcamento", FMT_USD),
M("Sazonalidade Historica %",
  """VAR _Mes = SELECTEDVALUE(dCalendario[NumeroMes])
VAR _RecMes = CALCULATE([Receita USD], ALL(dCalendario), dCalendario[NumeroMes] = _Mes)
VAR _RecTot = CALCULATE([Receita USD], ALL(dCalendario))
RETURN DIVIDE(_RecMes, _RecTot)""", "10 Forecast e Orcamento", FP,
  "Peso historico do mes no total do periodo — base do orcamento adaptativo."),
M("Projecao Fechamento Ano",
  """VAR _Ano = MAX(dCalendario[Ano])
VAR _Realizado = CALCULATE([Receita USD], ALL(dCalendario), dCalendario[Ano] = _Ano,
        dCalendario[Data] <= MAX(fVendas[DataFaturamento]))
VAR _PesoRealizado = CALCULATE([Sazonalidade Historica %], ALL(dCalendario))
VAR _MesesDecorridos = CALCULATE(MAX(dCalendario[NumeroMes]), ALL(dCalendario),
        dCalendario[Data] <= MAX(fVendas[DataFaturamento]), dCalendario[Ano] = _Ano)
RETURN DIVIDE(_Realizado, DIVIDE(_MesesDecorridos, 12)) """,
  "10 Forecast e Orcamento", FMT_USD,
  "Projecao linear de fechamento do ano com base no realizado acumulado."),
# ---------------- 11 Logistica
M("Embarques", "DISTINCTCOUNT(fEmbarques[EmbarqueID])", "11 Logistica", FQ),
M("Entregas Realizadas", "CALCULATE([Embarques], NOT(ISBLANK(fEmbarques[DiasAtraso])))", "11 Logistica", FQ),
M("Embarques Atrasados", "CALCULATE([Embarques], fEmbarques[DiasAtraso] > 0)", "11 Logistica", FQ),
M("% Embarques Atrasados", "DIVIDE([Embarques Atrasados], [Entregas Realizadas])", "11 Logistica", FP),
M("On Time %", "DIVIDE([Entregas Realizadas] - [Embarques Atrasados], [Entregas Realizadas])", "11 Logistica", FP),
M("In Full %",
  "DIVIDE(CALCULATE([Embarques], fEmbarques[StatusEmbarque] <> \"Aguardando embarque\"), [Embarques])",
  "11 Logistica", FP),
M("OTIF %", "[On Time %] * [In Full %]", "11 Logistica", FP,
  "On Time In Full: proporcao de entregas no prazo e completas."),
M("Lead Time Previsto", "AVERAGE(fEmbarques[LeadTimePrevisto])", "11 Logistica", FD),
M("Lead Time Real", "AVERAGE(fEmbarques[LeadTimeReal])", "11 Logistica", FD),
M("Desvio Lead Time", "[Lead Time Real] - [Lead Time Previsto]", "11 Logistica", FD),
M("Dias de Atraso Medio", "CALCULATE(AVERAGE(fEmbarques[DiasAtraso]), fEmbarques[DiasAtraso] > 0)",
  "11 Logistica", FD),
M("Peso Embarcado Kg", "SUM(fEmbarques[PesoKg])", "11 Logistica", FD),
M("Frete Embarque USD", "SUM(fEmbarques[FreteUSD])", "11 Logistica", FMT_USD),
M("Frete por Kg", "DIVIDE([Frete Embarque USD], [Peso Embarcado Kg])", "11 Logistica", FMT_USD),
# ---------------- 12 Financeiro
M("Contas a Receber", "SUM(fRecebimentos[ValorUSD])", "12 Financeiro", FMT_USD),
M("Recebido USD", "SUM(fRecebimentos[ValorRecebidoUSD])", "12 Financeiro", FMT_USD),
M("Saldo em Aberto", "SUM(fRecebimentos[SaldoUSD])", "12 Financeiro", FMT_USD),
M("Saldo Vencido",
  "CALCULATE([Saldo em Aberto], fRecebimentos[Status] IN {\"Vencido\", \"Parcial\"})", "12 Financeiro", FMT_USD),
M("Inadimplencia %", "DIVIDE([Saldo Vencido], [Contas a Receber])", "12 Financeiro", FP),
M("Dias Medios de Atraso",
  "CALCULATE(AVERAGE(fRecebimentos[DiasAtraso]), fRecebimentos[DiasAtraso] > 0)", "12 Financeiro", FD),
M("Prazo Medio Recebimento",
  """AVERAGEX(FILTER(fRecebimentos, NOT ISBLANK(fRecebimentos[DataPagamento])),
    DATEDIFF(fRecebimentos[DataFaturamento], fRecebimentos[DataPagamento], DAY))""",
  "12 Financeiro", FD, "PMR em dias entre faturamento e pagamento efetivo."),
M("Faixa Aging",
  """VAR _Hoje = MAX(dCalendario[Data])
VAR _D = AVERAGEX(fRecebimentos, DATEDIFF(fRecebimentos[DataVencimento], _Hoje, DAY))
RETURN SWITCH(TRUE(), _D < 0, "A vencer", _D <= 30, "1-30 dias", _D <= 60, "31-60 dias",
    _D <= 90, "61-90 dias", _D <= 180, "91-180 dias", "+180 dias")""", "12 Financeiro", ""),
M("Saldo Vencido +90",
  """VAR _Hoje = MAX(dCalendario[Data])
RETURN CALCULATE([Saldo em Aberto],
    FILTER(fRecebimentos, DATEDIFF(fRecebimentos[DataVencimento], _Hoje, DAY) > 90))""",
  "12 Financeiro", FMT_USD),
# ---------------- 13 Cambio
M("Taxa Media USD BRL",
  "CALCULATE(AVERAGE(fCambio[TaxaBRL]), fCambio[Moeda] = \"USD\")", "13 Cambio", "#,0.0000"),
M("Taxa Media Ponderada", "DIVIDE([Receita BRL], [Receita USD])", "13 Cambio", "#,0.0000"),
M("Taxa Media LY",
  "CALCULATE([Taxa Media Ponderada], SAMEPERIODLASTYEAR(dCalendario[Data]))", "13 Cambio", "#,0.0000"),
M("Efeito Cambio BRL", "[Receita USD] * ([Taxa Media Ponderada] - [Taxa Media LY])", "13 Cambio", FBRL,
  "Parcela da variacao da receita em BRL explicada apenas pela variacao cambial."),
M("Crescimento Operacional BRL",
  """VAR _LY_BRL = CALCULATE([Receita BRL], SAMEPERIODLASTYEAR(dCalendario[Data]))
RETURN [Receita BRL] - _LY_BRL - [Efeito Cambio BRL]""", "13 Cambio", FBRL),
M("Variacao Cambial %", "DIVIDE([Taxa Media Ponderada] - [Taxa Media LY], [Taxa Media LY])", "13 Cambio", FP),
# ---------------- 14 Inteligencia Comercial
M("Contribuicao para Crescimento",
  "DIVIDE([Receita YoY], CALCULATE([Receita YoY], ALLSELECTED()))", "14 Inteligencia Comercial", FP,
  "Quanto o elemento explica da variacao total de receita do periodo."),
M("Maior Crescimento Mercado",
  """VAR _T = TOPN(1, ALLSELECTED(dPais[Pais]), [Receita YoY], DESC)
RETURN CONCATENATEX(_T, dPais[Pais], ", ")""", "14 Inteligencia Comercial", ""),
M("Maior Queda Mercado",
  """VAR _T = TOPN(1, ALLSELECTED(dPais[Pais]), [Receita YoY], ASC)
RETURN CONCATENATEX(_T, dPais[Pais], ", ")""", "14 Inteligencia Comercial", ""),
M("Cliente Maior Queda",
  """VAR _T = TOPN(1, ALLSELECTED(dCliente[RazaoSocial]), [Receita YoY], ASC)
RETURN CONCATENATEX(_T, dCliente[RazaoSocial], ", ")""", "14 Inteligencia Comercial", ""),
M("Texto Insight Crescimento",
  """VAR _Total = CALCULATE([Receita YoY], ALLSELECTED(dPais))
VAR _TopPais = TOPN(1, ALLSELECTED(dPais[Pais]), [Receita YoY], DESC)
VAR _Nome = CONCATENATEX(_TopPais, dPais[Pais], ", ")
VAR _Val = MAXX(_TopPais, [Receita YoY])
VAR _Part = DIVIDE(_Val, _Total)
RETURN IF(ISBLANK(_Total) || _Total = 0, "Sem base comparativa no periodo selecionado.",
    _Nome & " respondeu por " & FORMAT(_Part, "0.0%") & " da variacao de receita do periodo ("
    & FORMAT(_Val, "$#,0,,.0M") & ").")""", "14 Inteligencia Comercial", "",
  "Texto dinamico com sustentacao matematica para a area de insights."),
M("Texto Insight Margem",
  """VAR _pp = [Margem YoY p.p.]
RETURN IF(ISBLANK(_pp), "Sem comparativo YoY.",
    "Margem bruta " & IF(_pp >= 0, "avancou ", "recuou ") & FORMAT(ABS(_pp), "0.0")
    & " p.p. YoY, hoje em " & FORMAT([Margem Bruta %], "0.0%") & ".")""",
  "14 Inteligencia Comercial", ""),
M("Alerta Rota Critica",
  """VAR _T = TOPN(1, ALLSELECTED(dPais[Pais]), [% Embarques Atrasados], DESC)
VAR _Nome = CONCATENATEX(_T, dPais[Pais], ", ")
VAR _V = MAXX(_T, [% Embarques Atrasados])
RETURN IF(ISBLANK(_V), BLANK(), _Nome & ": " & FORMAT(_V, "0.0%") & " de entregas atrasadas")""",
  "14 Inteligencia Comercial", ""),
# ---------------- 15 Formatacao e Titulos
M("Cor Semaforo Meta",
  """VAR _A = [Atingimento %]
RETURN SWITCH(TRUE(), ISBLANK(_A), "#8C96A5", _A >= 1, "#1F8A70", _A >= 0.9, "#D9A441", "#C0453B")""",
  "15 Formatacao", ""),
M("Cor Variacao",
  "IF([Receita YoY] >= 0, \"#1F8A70\", \"#C0453B\")", "15 Formatacao", ""),
M("Icone Tendencia", "IF([Receita YoY] >= 0, \"▲\", \"▼\")", "15 Formatacao", ""),
M("KPI Receita Contexto",
  """IF(ISBLANK([Receita LY]), "sem comparativo",
    [Icone Tendencia] & " " & FORMAT([Receita YoY %], "0.0%") & " YoY  ("
    & FORMAT([Receita YoY], "$#,0,,.1M") & ")")""", "15 Formatacao", ""),
M("Titulo Periodo",
  """VAR _Ini = MIN(dCalendario[Data]) VAR _Fim = MAX(dCalendario[Data])
RETURN IF(YEAR(_Ini) = YEAR(_Fim) && MONTH(_Ini) = MONTH(_Fim),
    FORMAT(_Ini, "mmm/yyyy"),
    FORMAT(_Ini, "mmm/yy") & " - " & FORMAT(_Fim, "mmm/yy"))""", "16 Titulos Dinamicos", ""),
M("Titulo Filtros",
  """VAR _Cont = IF(ISFILTERED(dPais[Continente]),
        CONCATENATEX(VALUES(dPais[Continente]), dPais[Continente], ", "), "Global")
RETURN _Cont & " — " & [Titulo Periodo]""", "16 Titulos Dinamicos", ""),
M("Titulo Receita por Pais", '"Receita por Pais — " & [Titulo Filtros]', "16 Titulos Dinamicos", ""),
M("Titulo Performance Comercial", '"Performance Comercial — " & [Titulo Filtros]', "16 Titulos Dinamicos", ""),
M("Titulo Rentabilidade", '"Ponte de Rentabilidade — " & [Titulo Periodo]', "16 Titulos Dinamicos", ""),

# --- paineis HTML (visual custom "HTML Content") -------------------------
# Os .dax sao gerados por scripts/gen_paineis.pl a partir de um spec unico,
# para que os 11 paineis fiquem consistentes entre si.
M_html("HTML Painel Executivo",    "painel_p01.dax", "Painel de KPIs da pagina 01 Executive Overview."),
M_html("HTML Painel Vendas",       "painel_p02.dax", "Painel de KPIs da pagina 02 Sales Performance."),
M_html("HTML Painel Clientes",     "painel_p03.dax", "Painel de KPIs da pagina 03 Customers."),
M_html("HTML Painel Potencial",    "painel_p04.dax", "Painel de KPIs da pagina 04 Customer Potential."),
M_html("HTML Painel Produtos",     "painel_p05.dax", "Painel de KPIs da pagina 05 Products."),
M_html("HTML Painel Mercados",     "painel_p06.dax", "Painel de KPIs da pagina 06 Markets."),
M_html("HTML Painel Rentabilidade","painel_p07.dax", "Painel de KPIs da pagina 07 Profitability."),
M_html("HTML Painel Logistica",    "painel_p08.dax", "Painel de KPIs da pagina 08 Logistics."),
M_html("HTML Painel Equipe",       "painel_p09.dax", "Painel de KPIs da pagina 09 Sales Team."),
M_html("HTML Painel Financeiro",   "painel_p10.dax", "Painel de KPIs da pagina 10 Finance."),
M_html("HTML Painel Forecast",     "painel_p11.dax", "Painel de KPIs da pagina 11 Forecast e Budget."),

# paineis das paginas de drill-through
M_html("HTML Painel Detalhe Cliente", "painel_dt_cliente.dax",
       "Painel de KPIs da pagina de drill-through Detalhe Cliente."),
M_html("HTML Painel Detalhe Mercado", "painel_dt_pais.dax",
       "Painel de KPIs da pagina de drill-through Detalhe Mercado."),

# tooltips HTML (um por dimensao) - gerados por scripts/gen_tooltips.pl
M_html("HTML Tooltip Cliente",  "tooltip_cliente.dax",  "Tooltip HTML de cliente."),
M_html("HTML Tooltip Produto",  "tooltip_produto.dax",  "Tooltip HTML de produto."),
M_html("HTML Tooltip Pais",     "tooltip_pais.dax",     "Tooltip HTML de mercado."),
M_html("HTML Tooltip Vendedor", "tooltip_vendedor.dax", "Tooltip HTML de vendedor."),

# guia de analise embutido no relatorio
M_html("HTML Guia de Analise", "guia_analise.dax",
       "Guia de analise: o que cada pagina responde e o que cada visual permite analisar."),
]


def medidas_tmdl():
    L = ["/// Tabela dedicada as medidas DAX. Nao contem dados analiticos.",
         "table _Medidas",
         f"\tlineageTag: {lt('t_Medidas')}", ""]
    for m in MEDIDAS:
        dax = m["dax"].strip()
        # A descricao (///) precisa vir IMEDIATAMENTE antes da declaracao da
        # medida. Emitir aqui, e nao com L.insert() depois, evita que ela caia no
        # meio do bloco de propriedades da medida anterior.
        if m["desc"]:
            L.append(f"\t/// {m['desc']}")
        corpo = "\n".join("\t\t\t" + l for l in dax.split("\n"))
        if m.get("fence"):
            # ``` protege expressoes com HTML, aspas e caracteres especiais.
            L.append(f"\tmeasure '{m['nome']}' = ```")
            L.append(corpo)
            L.append("\t\t\t```")
        elif "\n" in dax:
            L.append(f"\tmeasure '{m['nome']}' =")
            L.append(corpo)
        else:
            L.append(f"\tmeasure '{m['nome']}' = {dax}")
        if m["fmt"]:
            L.append(f'\t\tformatString: {m["fmt"]}')
        L.append(f"\t\tdisplayFolder: {m['pasta']}")
        L.append(f"\t\tlineageTag: {lt('m'+m['nome'])}")
        L.append("")
    L += ["\tcolumn Coluna",
          "\t\tdataType: int64",
          "\t\tisHidden",
          f"\t\tlineageTag: {lt('c_MedidasColuna')}",
          "\t\tsummarizeBy: none",
          "\t\tsourceColumn: Coluna",
          "",
          "\tpartition _Medidas = m",
          "\t\tmode: import",
          "\t\tsource =",
          '\t\t\t\tlet',
          '\t\t\t\t    Origem = #table(type table [Coluna = Int64.Type], {{1}})',
          '\t\t\t\tin',
          '\t\t\t\t    Origem',
          "",
          "\tannotation PBI_ResultType = Table",
          ""]
    return "\n".join(L)


# ---------------------------------------------------------------- relacoes
RELACOES = [
 ("dCalendario", "Data", "fVendas", "DataFaturamento", True),
 ("dCalendario", "Data", "fVendas", "DataPedido", False),
 ("dCliente", "ClienteID", "fVendas", "ClienteID", True),
 ("dProduto", "ProdutoID", "fVendas", "ProdutoID", True),
 ("dVendedor", "VendedorID", "fVendas", "VendedorID", True),
 ("dPais", "PaisID", "fVendas", "PaisID", True),
 ("dCalendario", "Data", "fEmbarques", "DataRealEmbarque", True),
 ("dCalendario", "Data", "fEmbarques", "DataRealEntrega", False),
 ("dCliente", "ClienteID", "fEmbarques", "ClienteID", True),
 ("dPais", "PaisID", "fEmbarques", "PaisDestinoID", True),
 ("dPorto", "PortoID", "fEmbarques", "PortoOrigemID", True),
 ("dTransportadora", "TransportadoraID", "fEmbarques", "TransportadoraID", True),
 ("dCalendario", "Data", "fRecebimentos", "DataFaturamento", True),
 ("dCalendario", "Data", "fRecebimentos", "DataVencimento", False),
 ("dCalendario", "Data", "fRecebimentos", "DataPagamento", False),
 ("dCliente", "ClienteID", "fRecebimentos", "ClienteID", True),
 ("dVendedor", "VendedorID", "fMetas", "VendedorID", True),
 ("dCalendario", "Data", "fMetas", "Data", True),
 ("dCalendario", "Data", "fOrcamento", "Data", True),
 ("dCalendario", "Data", "fForecast", "Data", True),
 ("dCalendario", "Data", "fCambio", "Data", True),
]


def relacoes_tmdl():
    L = []
    for t1, c1, t2, c2, ativo in RELACOES:
        rid = lt(f"rel{t1}{c1}{t2}{c2}")
        L.append(f"relationship {rid}")
        if not ativo:
            L.append("\tisActive: false")
        L.append(f"\tfromColumn: {t2}.{c2}")
        L.append(f"\ttoColumn: {t1}.{c1}")
        L.append("")
    return "\n".join(L)


def main():
    # tabelas
    for t in TABELAS:
        with open(os.path.join(TBL, f"{t}.tmdl"), "w", encoding="utf-8") as f:
            f.write(gerar_tabela_tmdl(t))
    with open(os.path.join(TBL, "_Medidas.tmdl"), "w", encoding="utf-8") as f:
        f.write(medidas_tmdl())

    # relationships
    with open(os.path.join(DEF, "relationships.tmdl"), "w", encoding="utf-8") as f:
        f.write(relacoes_tmdl())

    # parametro pBasePath
    caminho_padrao = "E:\\Projetos BI\\02 - Aurora Exportação\\dados\\"
    with open(os.path.join(DEF, "expressions.tmdl"), "w", encoding="utf-8") as f:
        f.write(f'''/// Diretorio raiz dos arquivos CSV. Altere apenas aqui para apontar o projeto
/// para a pasta sincronizada do Google Drive (ex.: "G:\\\\Meu Drive\\\\Aurora Brasil Exportadora\\\\dados\\\\").
expression pBasePath = "{caminho_padrao}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
\tlineageTag: {lt('exprBasePath')}
\tqueryGroup: '00 Parametros'

\tannotation PBI_NavigationStepName = Navigation

\tannotation PBI_ResultType = Text

''')

    # model.tmdl
    ordem = TABELAS + ["_Medidas"]
    refs = "\n".join(f"ref table {t}" for t in ordem)
    with open(os.path.join(DEF, "model.tmdl"), "w", encoding="utf-8") as f:
        f.write(f'''model Model
\tculture: pt-BR
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tdiscourageImplicitMeasures
\tsourceQueryCulture: pt-BR
\tdataAccessOptions
\t\tlegacyRedirects
\t\treturnErrorValuesAsNull

annotation PBI_QueryOrder = {json.dumps(["pBasePath"] + ordem)}

annotation __PBI_TimeIntelligenceEnabled = 0

annotation PBI_ProTooling = ["DevMode"]

queryGroup '00 Parametros'
\tannotation PBI_QueryGroupOrder = 0

queryGroup '01 Dimensoes'
\tannotation PBI_QueryGroupOrder = 1

queryGroup '02 Fatos'
\tannotation PBI_QueryGroupOrder = 2

queryGroup '90 Auxiliares'
\tannotation PBI_QueryGroupOrder = 3

{refs}

ref cultureInfo pt-BR
''')

    with open(os.path.join(DEF, "database.tmdl"), "w", encoding="utf-8") as f:
        f.write("database\n\tcompatibilityLevel: 1567\n")

    os.makedirs(os.path.join(DEF, "cultures"), exist_ok=True)
    with open(os.path.join(DEF, "cultures", "pt-BR.tmdl"), "w", encoding="utf-8") as f:
        f.write("cultureInfo pt-BR\n\n\tlinguisticMetadata =\n\t\t\t{\n\t\t\t  \"Version\": \"1.0.0\",\n\t\t\t  \"Language\": \"pt-BR\"\n\t\t\t}\n\t\tcontentType: json\n")

    with open(os.path.join(SM, "definition.pbism"), "w", encoding="utf-8") as f:
        json.dump({"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
                   "version": "4.2", "settings": {}}, f, indent=2)

    with open(os.path.join(SM, ".platform"), "w", encoding="utf-8") as f:
        json.dump({"$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
                   "metadata": {"type": "SemanticModel", "displayName": "AuroraBrasilExportadora"},
                   "config": {"version": "2.0", "logicalId": lt("smLogical")}}, f, indent=2)

    print(f"Tabelas TMDL: {len(TABELAS)+1} | Medidas: {len(MEDIDAS)} | Relacionamentos: {len(RELACOES)}")
    pastas = sorted({m['pasta'] for m in MEDIDAS})
    print("Display folders:", ", ".join(pastas))


if __name__ == "__main__":
    main()
