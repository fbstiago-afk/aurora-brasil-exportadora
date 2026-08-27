#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera a documentacao tecnica a partir dos artefatos reais (CSV + TMDL + PBIR)."""
import os, re, json, glob
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS, DOC = os.path.join(BASE, "dados"), os.path.join(BASE, "documentacao")
SM = os.path.join(BASE, "PowerBI", "AuroraBrasilExportadora.SemanticModel", "definition")
PAGES = os.path.join(BASE, "PowerBI", "AuroraBrasilExportadora.Report", "definition", "pages")
os.makedirs(DOC, exist_ok=True)

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_model import MEDIDAS, RELACOES, TAB_DESC, DATE_COLS, INT_COLS, HIDE

DESC = {
 "Data": ("Data do calendario (chave da dimensao de datas)", "Diaria, sem lacunas"),
 "Ano": ("Ano civil", "2022 a 2026"), "Trimestre": ("Trimestre do ano", "T1 a T4"),
 "NumeroMes": ("Numero do mes", "1 a 12"), "Mes": ("Nome do mes por extenso", "Ordenado por NumeroMes"),
 "MesAbreviado": ("Abreviacao do mes", "Ordenado por NumeroMes"),
 "AnoMes": ("Rotulo mes/ano", "Ordenado por AnoMesNumero"),
 "AnoMesNumero": ("Chave numerica AAAAMM", "Coluna tecnica, oculta"),
 "SemanaAno": ("Semana ISO do ano", "1 a 53"),
 "DiaSemana": ("Nome do dia da semana", "Ordenado por NumeroDiaSemana"),
 "NumeroDiaSemana": ("Numero do dia da semana", "1=Segunda a 7=Domingo"),
 "DiaUtil": ("Indica dia util", "Sim/Nao"), "FimDeSemana": ("Indica fim de semana", "Sim/Nao"),
 "InicioMes": ("Primeiro dia do mes", "Derivada"), "FimMes": ("Ultimo dia do mes", "Derivada"),
 "ClienteID": ("Chave do cliente", "PK em dCliente, FK nas fatos"),
 "CodigoCliente": ("Codigo comercial do cliente", "Formato CL0000"),
 "RazaoSocial": ("Razao social ficticia", "Unica"), "NomeFantasia": ("Nome fantasia", "Livre"),
 "TipoCliente": ("Tipo de operacao do cliente", "Importador, Distribuidor, Rede Varejista, Industria, Food Service, Atacadista, Private Label"),
 "Segmento": ("Segmento de atuacao", "Derivado do tipo"),
 "Subsegmento": ("Posicionamento do portfolio comprado", "Premium, Mainstream, Organico, Industrial, Gourmet"),
 "Porte": ("Porte pelo potencial anual", "Grande >=4M, Medio >=1,2M, Pequeno >=350k, Micro"),
 "Pais": ("Pais do cliente ou do porto", "Consistente com dPais"),
 "CodigoPais": ("Codigo ISO alpha-3", "3 letras"),
 "Continente": ("Continente do mercado", "6 continentes atendidos"),
 "RegiaoComercial": ("Regiao comercial de gestao", "Ex.: Europa Ocidental"),
 "Cidade": ("Cidade", "Coerente com o pais"), "EstadoProvincia": ("Estado ou provincia", "Coerente com a cidade"),
 "MoedaPreferencial": ("Moeda de negociacao preferida", "USD, EUR, GBP, CAD, JPY, CNY, AED"),
 "Idioma": ("Idioma principal de relacionamento", "Coerente com o pais"),
 "DataCadastro": ("Data de abertura do cadastro", "Anterior ou igual a primeira compra"),
 "VendedorResponsavelID": ("FK do executivo responsavel", "Existe em dVendedor"),
 "CanalVenda": ("Canal de originacao", "Venda Direta, Representante Local, Trading Parceira, E-commerce B2B, Feira Internacional"),
 "ClassificacaoCliente": ("Classificacao estrategica manual", "Estrategico, Chave, Regular, Ocasional"),
 "LimiteCreditoUSD": ("Limite de credito aprovado", "6% a 22% do potencial"),
 "PrazoPagamentoPadrao": ("Prazo contratual em dias", "0, 30, 45, 60, 90 ou 120"),
 "StatusCliente": ("Status derivado da ultima compra", "Ativo <=180d, Inativo <=365d, Perdido, Prospect"),
 "PotencialAnualEstimadoUSD": ("Compra anual potencial estimada", "Base do Share of Wallet"),
 "ProdutoID": ("Chave do produto", "PK em dProduto"),
 "SKU": ("Codigo do SKU", "CAT-SUB-PESO-ID"), "Produto": ("Descricao comercial do SKU", "Unica"),
 "Categoria": ("Categoria do portfolio", "8 categorias"),
 "Subcategoria": ("Subcategoria/tipo", "30 subcategorias"),
 "Linha": ("Linha de posicionamento", "Premium, Standard, Organico, Ingredientes, Congelados"),
 "Marca": ("Marca proprietaria", "5 marcas"),
 "TipoEmbalagem": ("Formato de embalagem", "Saca, Big Bag, Caixa, Pouch, Balde, Tambor, Cartucho"),
 "PesoLiquidoKg": ("Peso liquido por unidade", "Base do calculo de peso total"),
 "UnidadeMedida": ("Unidade de medida", "KG"),
 "OrigemBrasil": ("Indica produto de origem brasileira", "Sim"),
 "EstadoOrigem": ("Estado brasileiro de origem", "UF produtora"),
 "CustoBaseBRL": ("Custo padrao por unidade em BRL", "Reajustado por indice anual de categoria"),
 "PrecoListaUSD": ("Preco de tabela por unidade", "Base do preco praticado"),
 "MargemAlvo": ("Margem alvo definida no pricing", "0,10 a 0,55"),
 "VidaUtilDias": ("Shelf life em dias", "240 a 730"),
 "Certificacao": ("Certificacao do SKU", "Organico, Fair Trade, Rainforest, Kosher, Halal, BRCGS"),
 "StatusProduto": ("Ciclo de vida do SKU", "Ativo, Novo, Descontinuado"),
 "VendedorID": ("Chave do vendedor", "PK em dVendedor"),
 "CodigoVendedor": ("Matricula comercial", "VD000"),
 "NomeVendedor": ("Nome do profissional", "Ficticio"),
 "Cargo": ("Cargo na estrutura", "Diretor Comercial, Gerente Regional, Executivo de Contas"),
 "Gerente": ("Nome do gestor imediato", "Vazio para o diretor"),
 "RegiaoResponsavel": ("Regiao sob responsabilidade", "Consistente com REGIAO_PAISES"),
 "ContinenteResponsavel": ("Continente sob responsabilidade", "-"),
 "DataAdmissao": ("Data de admissao", "Anterior ao periodo analisado"),
 "MetaAnualUSD": ("Meta anual individual", "0 para o diretor"),
 "Status": ("Situacao do registro", "Ativo/Inativo/Em Revisao"),
 "PaisID": ("Chave do pais", "PK em dPais"), "CodigoISO": ("Codigo ISO alpha-3", "3 letras"),
 "Regiao": ("Regiao geoeconomica", "-"), "Moeda": ("Moeda de referencia do mercado", "-"),
 "IdiomaPrincipal": ("Idioma principal", "-"),
 "ClassificacaoMercado": ("Maturidade do mercado", "Principal, Secundario, Emergente"),
 "RiscoPais": ("Risco comercial do pais", "Baixo, Medio, Alto"),
 "LeadTimeMedio": ("Lead time medio de referencia em dias", "Base do lead time previsto"),
 "TarifaMediaImportacao": ("Tarifa media de importacao em %", "Impacta despesas em DDP"),
 "PortoID": ("Chave do porto", "PK em dPorto"), "Porto": ("Nome do porto ou aeroporto", "Unico"),
 "CodigoUNLOCODE": ("Codigo UN/LOCODE", "5 caracteres"),
 "TipoPorto": ("Modalidade do terminal", "Maritimo, Aereo, Fluvial"),
 "TransportadoraID": ("Chave da transportadora", "PK em dTransportadora"),
 "Transportadora": ("Nome do operador logistico", "Ficticio"),
 "ModalPrincipal": ("Modal predominante", "Maritimo, Aereo, Rodoviario"),
 "AvaliacaoFornecedor": ("Nota de avaliacao do fornecedor", "3,4 a 4,7"),
 "VendaID": ("Chave da linha de venda", "PK de fVendas"),
 "PedidoID": ("Numero do pedido", "Agrupa varias linhas"),
 "DataPedido": ("Data de emissao do pedido", "Relacionamento inativo com dCalendario"),
 "DataFaturamento": ("Data de faturamento", "Relacionamento ativo com dCalendario"),
 "Quantidade": ("Unidades de embalagem vendidas", "Inteiro >= 1"),
 "PesoTotalKg": ("Peso total da linha", "Quantidade x PesoLiquidoKg"),
 "PrecoUnitarioUSD": ("Preco praticado por unidade", "Preco lista x reajuste x premio de mercado"),
 "ReceitaBrutaUSD": ("Receita bruta da linha", "Quantidade x PrecoUnitarioUSD"),
 "DescontoUSD": ("Desconto comercial concedido", ">= 0"),
 "ReceitaLiquidaUSD": ("Receita liquida da linha", "ReceitaBruta - Desconto"),
 "TaxaCambio": ("Taxa USD/BRL da data de faturamento", "Coerente com fCambio"),
 "ReceitaLiquidaBRL": ("Receita liquida convertida", "ReceitaLiquidaUSD x TaxaCambio"),
 "CustoProdutoBRL": ("Custo do produto em BRL", "CustoBaseBRL x indice de custo x quantidade"),
 "CustoProdutoUSD": ("Custo do produto em USD", "CustoProdutoBRL / TaxaCambio"),
 "FreteUSD": ("Frete internacional assumido pela Aurora", "Depende do Incoterm e do modal"),
 "SeguroUSD": ("Seguro internacional", "Apenas CIF e DDP"),
 "DespesasExportacaoUSD": ("Despesas de exportacao e desembaraco", "1,6% a 3,4% da receita liquida"),
 "CustoTotalUSD": ("Custo total da linha", "Produto + Frete + Seguro + Despesas"),
 "MargemBrutaUSD": ("Margem bruta da linha", "ReceitaLiquida - CustoTotal"),
 "MargemBrutaPercentual": ("Margem percentual da linha", "MargemBruta / ReceitaLiquida"),
 "MoedaNegociacao": ("Moeda contratada com o cliente", "Herdada de dCliente"),
 "Incoterm": ("Incoterm da operacao", "FOB, CIF, CFR, EXW, FCA, DDP"),
 "NumeroInvoice": ("Numero da invoice de exportacao", "Chave de ligacao com fRecebimentos"),
 "StatusPedido": ("Situacao do pedido", "Faturado, Em Producao, Cancelado"),
 "EmbarqueID": ("Chave do embarque", "PK de fEmbarques"),
 "PaisDestinoID": ("FK do pais de destino", "Existe em dPais"),
 "PortoOrigemID": ("FK do porto de origem", "Terminal brasileiro"),
 "PortoDestinoID": ("FK do porto de destino", "Terminal internacional"),
 "DataPrevistaEmbarque": ("Data prevista de embarque", "Posterior ao faturamento"),
 "DataRealEmbarque": ("Data efetiva de embarque", "Vazia se ainda nao embarcado"),
 "DataPrevistaEntrega": ("Data prevista de entrega", "Embarque previsto + lead time previsto"),
 "DataRealEntrega": ("Data efetiva de entrega", "Vazia se em transito"),
 "Modal": ("Modal utilizado", "Maritimo (~85%), Aereo, Rodoviario"),
 "Container": ("Identificacao do container ou ULD", "-"),
 "TipoContainer": ("Tipo de equipamento", "20 DRY, 40 HC, 40 REEFER, LCL, ULD"),
 "PesoKg": ("Peso total embarcado", "Soma das linhas do pedido"),
 "VolumeM3": ("Volume cubado", "Derivado do peso e da densidade"),
 "LeadTimePrevisto": ("Lead time contratado em dias", "-"),
 "LeadTimeReal": ("Lead time efetivo em dias", "Vazio se nao entregue"),
 "DiasAtraso": ("Atraso versus data prevista", "Negativo = adiantado"),
 "StatusEmbarque": ("Situacao do embarque", "Entregue no prazo, Entregue com atraso, Em transito, Aguardando embarque"),
 "MotivoAtraso": ("Causa raiz do atraso", "Vazio quando nao ha atraso"),
 "TaxaBRL": ("Cotacao da moeda em BRL", "-"),
 "VariacaoDia": ("Variacao percentual diaria", "-"),
 "VariacaoMes": ("Variacao percentual mensal", "-"),
 "Mes": ("Numero do mes", "1 a 12"),
 "MetaReceitaUSD": ("Meta de receita liquida", "Mes x vendedor"),
 "MetaVolumeKg": ("Meta de volume", "Mes x vendedor"),
 "MetaMargemUSD": ("Meta de margem bruta", "Mes x vendedor"),
 "MetaNovosClientes": ("Meta de novos clientes", "Inteiro"),
 "MetaPedidos": ("Meta de pedidos", "Inteiro"),
 "ReceitaOrcadaUSD": ("Receita orcada aprovada", "Mes x regiao x categoria"),
 "CustoOrcadoUSD": ("Custo orcado", "-"), "MargemOrcadaUSD": ("Margem orcada", "-"),
 "VolumeOrcadoKg": ("Volume orcado", "-"),
 "ReceitaForecastUSD": ("Receita projetada na revisao", "-"),
 "MargemForecastUSD": ("Margem projetada", "-"), "VolumeForecastKg": ("Volume projetado", "-"),
 "DataForecast": ("Data da revisao de forecast", "Revisoes em Jan, Mai e Set"),
 "RecebimentoID": ("Chave do titulo", "PK de fRecebimentos"),
 "Invoice": ("Numero da invoice", "FK logica para fVendas[NumeroInvoice]"),
 "DataVencimento": ("Vencimento do titulo", "Faturamento + prazo do cliente"),
 "DataPagamento": ("Data da liquidacao", "Vazia se em aberto"),
 "ValorUSD": ("Valor faturado do titulo", "-"),
 "ValorRecebidoUSD": ("Valor efetivamente recebido", "-"),
 "SaldoUSD": ("Saldo em aberto", "Valor - Recebido"),
 "FormaPagamento": ("Instrumento de pagamento", "Carta de Credito, Cobranca Documentaria, Antecipada, Conta Aberta, A Vista"),
}

TABELAS = ["dCalendario", "dCliente", "dProduto", "dVendedor", "dPais", "dPorto",
           "dTransportadora", "fVendas", "fEmbarques", "fCambio", "fMetas",
           "fOrcamento", "fForecast", "fRecebimentos"]

GRAN = {
 "dCalendario": "1 linha por dia", "dCliente": "1 linha por cliente",
 "dProduto": "1 linha por SKU", "dVendedor": "1 linha por profissional",
 "dPais": "1 linha por pais", "dPorto": "1 linha por terminal",
 "dTransportadora": "1 linha por operador",
 "fVendas": "1 linha por item de pedido", "fEmbarques": "1 linha por pedido embarcado",
 "fCambio": "1 linha por data e moeda", "fMetas": "1 linha por mes e vendedor",
 "fOrcamento": "1 linha por mes, regiao e categoria",
 "fForecast": "1 linha por revisao, mes, regiao e categoria",
 "fRecebimentos": "1 linha por invoice",
}


def tipo_txt(col, serie):
    if col in DATE_COLS: return "Data"
    if col in INT_COLS: return "Inteiro"
    if pd.api.types.is_float_dtype(serie): return "Decimal"
    return "Texto"


def dicionario():
    L = ["# Dicionario de Dados — Aurora Brasil Exportadora S.A.", "",
         "Todas as colunas de todas as tabelas estao documentadas. Separador `;`, decimal `,`, "
         "codificacao UTF-8 com BOM, datas em ISO `AAAA-MM-DD`.", ""]
    for t in TABELAS:
        df = pd.read_csv(os.path.join(DADOS, f"{t}.csv"), sep=";", decimal=",",
                         encoding="utf-8-sig", nrows=500)
        tot = sum(1 for _ in open(os.path.join(DADOS, f"{t}.csv"), encoding="utf-8-sig")) - 1
        L += [f"## {t}", "", f"*{TAB_DESC.get(t,'')}*", "",
              f"Granularidade: **{GRAN[t]}** | Linhas: **{tot:,}** | Colunas: **{len(df.columns)}**", "",
              "| Campo | Tipo | Descricao | Exemplo | Regra |", "|---|---|---|---|---|"]
        for col in df.columns:
            d, regra = DESC.get(col, ("Campo do dominio de negocio", "-"))
            ex = df[col].dropna()
            ex = str(ex.iloc[0])[:32] if len(ex) else ""
            L.append(f"| `{col}` | {tipo_txt(col, df[col])} | {d} | {ex} | {regra} |")
        L.append("")
    open(os.path.join(DOC, "DicionarioDados.md"), "w", encoding="utf-8").write("\n".join(L))


def modelo():
    L = ["# Modelo de Dados — Aurora Brasil Exportadora S.A.", "",
         "Arquitetura **estrela**, com dimensoes conformadas compartilhadas entre as fatos. "
         "Nenhum relacionamento bidirecional. Todas as chaves estao ocultas na camada de relatorio.", "",
         "## Tabelas", "", "| Tabela | Papel | Granularidade | Linhas |", "|---|---|---|---|"]
    for t in TABELAS:
        tot = sum(1 for _ in open(os.path.join(DADOS, f"{t}.csv"), encoding="utf-8-sig")) - 1
        papel = "Dimensao" if t.startswith("d") else "Fato"
        L.append(f"| `{t}` | {papel} | {GRAN[t]} | {tot:,} |")
    L.append("| `_Medidas` | Tabela tecnica | 1 linha fictícia, apenas medidas | 1 |")
    L += ["", "## Relacionamentos", "",
          "| De (1) | Para (*) | Cardinalidade | Direcao | Estado |", "|---|---|---|---|---|"]
    for t1, c1, t2, c2, ativo in RELACOES:
        L.append(f"| `{t1}[{c1}]` | `{t2}[{c2}]` | 1:* | Single | "
                 f"{'Ativo' if ativo else 'Inativo (USERELATIONSHIP)'} |")
    L += ["", "## Chaves e integridade", "",
          "- `dCalendario[Data]` marcada como tabela de datas (`dataCategory: Time`, coluna chave).",
          "- Fatos mensais (`fMetas`, `fOrcamento`, `fForecast`) carregam a coluna `Data` "
          "com o primeiro dia do mes, evitando relacionar por `AnoMesNumero` (que nao e unico no calendario).",
          "- Relacionamentos inativos existem para `DataPedido`, `DataRealEntrega`, "
          "`DataVencimento` e `DataPagamento`, ativados via `USERELATIONSHIP` nas medidas correspondentes.",
          "- `fRecebimentos[Invoice]` liga-se logicamente a `fVendas[NumeroInvoice]`; nao ha "
          "relacionamento fisico para evitar ambiguidade — a analise financeira e feita por cliente e data.",
          "", "## Colunas ocultas", "",
          "Todas as PKs e FKs, alem de `AnoMesNumero`, `NumeroMes`, `NumeroDiaSemana`, "
          "`InicioMes` e `FimMes` (usadas apenas para ordenacao e relacionamento).", "",
          "## Sort by column", "",
          "`Mes` e `MesAbreviado` por `NumeroMes`; `AnoMes` por `AnoMesNumero`; "
          "`DiaSemana` por `NumeroDiaSemana`.", ""]
    open(os.path.join(DOC, "ModeloDados.md"), "w", encoding="utf-8").write("\n".join(L))


def medidas_doc():
    pastas = {}
    for m in MEDIDAS:
        pastas.setdefault(m["pasta"], []).append(m)
    L = ["# Medidas DAX — Aurora Brasil Exportadora S.A.", "",
         f"Total: **{len(MEDIDAS)} medidas**, todas na tabela `_Medidas`, "
         f"organizadas em {len(pastas)} display folders.", ""]
    for pasta in sorted(pastas):
        L += [f"## {pasta}", ""]
        for m in pastas[pasta]:
            deps = sorted({d for d in re.findall(r"(?<![\w'])\[([A-Z][^\]\n]{2,60})\]", m["dax"])
                           if any(x["nome"] == d for x in MEDIDAS)})
            L += [f"### `{m['nome']}`", ""]
            if m["desc"]:
                L.append(m["desc"] + "")
                L.append("")
            L += ["```dax", f"{m['nome']} =", m["dax"].strip(), "```", ""]
            L.append(f"- **Formato:** `{m['fmt'] or 'texto'}`")
            L.append(f"- **Dependencias:** {', '.join('`'+d+'`' for d in deps) if deps else 'colunas base'}")
            L.append("")
    open(os.path.join(DOC, "MedidasDAX.md"), "w", encoding="utf-8").write("\n".join(L))


def powerquery_doc():
    L = ["# Power Query — Aurora Brasil Exportadora S.A.", "",
         "## Parametro", "",
         "```m", 'pBasePath  //  Texto, obrigatorio',
         'Exemplo: "G:\\Meu Drive\\Aurora Brasil Exportadora\\dados\\"', "```", "",
         "Todas as 14 queries de dados derivam o caminho desse unico parametro. "
         "Para mover o projeto basta alterar `pBasePath` em *Transformar dados > "
         "Gerenciar parametros* — nenhuma query precisa ser editada.", "",
         "## Grupos de query", "",
         "| Grupo | Queries |", "|---|---|",
         "| 00 Parametros | pBasePath |",
         "| 01 Dimensoes | dCalendario, dCliente, dProduto, dVendedor, dPais, dPorto, dTransportadora |",
         "| 02 Fatos | fVendas, fEmbarques, fCambio, fMetas, fOrcamento, fForecast, fRecebimentos |",
         "| 90 Auxiliares | _Medidas (tabela tecnica gerada em memoria) |", "",
         "## Padrao de transformacao", "",
         "Cada query segue exatamente quatro etapas nomeadas, sem passos redundantes:", "",
         "```m", "let",
         '    Origem = Csv.Document(File.Contents(pBasePath & "fVendas.csv"),',
         '        [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),',
         "    CabecalhoPromovido = Table.PromoteHeaders(Origem, [PromoteAllScalars = true]),",
         '    TiposAplicados = Table.TransformColumnTypes(CabecalhoPromovido, {...}, "pt-BR"),',
         "    ErrosRemovidos = Table.RemoveRowsWithErrors(TiposAplicados)",
         "in", "    ErrosRemovidos", "```", "",
         "**Decisoes tecnicas**", "",
         "- `Encoding = 65001` (UTF-8) porque os CSVs contem acentos e nomes internacionais.",
         "- Cultura `pt-BR` no `TransformColumnTypes` porque os arquivos usam `;` como separador "
         "e `,` como decimal — padrao que abre corretamente no Excel brasileiro.",
         "- `Table.RemoveRowsWithErrors` como rede de seguranca; na base validada nenhuma linha e descartada.",
         "- Nenhum calculo financeiro e feito em Power Query: tudo o que depende de contexto de "
         "filtro vive em DAX. As colunas calculadas foram deliberadamente evitadas.",
         "- Nenhum merge: as chaves ja vem resolvidas do gerador, o que preserva a compressao "
         "do VertiPaq e evita expandir a fato.", "",
         "## Alternativa de fonte", "",
         "Se no futuro os arquivos forem para o Google Sheets, o conector `Web.Contents` com a URL "
         "de exportacao CSV da planilha substitui apenas a etapa `Origem`; o restante das queries "
         "permanece identico. A pasta local sincronizada foi escolhida por permitir refresh no "
         "Power BI Desktop sem autenticacao OAuth e por manter o gateway simples em publicacoes futuras.", ""]
    open(os.path.join(DOC, "PowerQuery.md"), "w", encoding="utf-8").write("\n".join(L))


def paginas_doc():
    meta = json.load(open(os.path.join(PAGES, "pages.json"), encoding="utf-8"))
    L = ["# Paginas do Dashboard — Aurora Brasil Exportadora S.A.", "",
         "Formato 1280x720 (16:9). Navegacao lateral fixa via visual `pageNavigator`.", "",
         "| # | Pagina | Tipo | Visuais |", "|---|---|---|---|"]
    for i, pid in enumerate(meta["pageOrder"], 1):
        pg = json.load(open(os.path.join(PAGES, pid, "page.json"), encoding="utf-8"))
        n = len(os.listdir(os.path.join(PAGES, pid, "visuals")))
        tp = pg.get("pageBinding", {}).get("type", "Relatorio")
        L.append(f"| {i} | {pg['displayName']} | {tp} | {n} |")
    L += ["", "## Perguntas que cada pagina responde", ""]
    for pid in meta["pageOrder"]:
        pg = json.load(open(os.path.join(PAGES, pid, "page.json"), encoding="utf-8"))
        vis = []
        for vid in os.listdir(os.path.join(PAGES, pid, "visuals")):
            vj = json.load(open(os.path.join(PAGES, pid, "visuals", vid, "visual.json"),
                                encoding="utf-8"))
            t = vj["visual"]["visualType"]
            titulo = ""
            try:
                titulo = vj["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"]["expr"]["Literal"]["Value"].strip("'")
            except Exception:
                pass
            if t not in ("shape", "pageNavigator"):
                vis.append(f"{t}{' — ' + titulo if titulo else ''}")
        L += [f"### {pg['displayName']}", ""]
        for v in sorted(set(vis)):
            L.append(f"- {v}")
        L.append("")
    open(os.path.join(DOC, "DashboardPages.md"), "w", encoding="utf-8").write("\n".join(L))


if __name__ == "__main__":
    dicionario(); modelo(); medidas_doc(); powerquery_doc(); paginas_doc()
    for f in ["DicionarioDados.md", "ModeloDados.md", "MedidasDAX.md",
              "PowerQuery.md", "DashboardPages.md"]:
        p = os.path.join(DOC, f)
        print(f"{f}: {os.path.getsize(p)/1024:.1f} KB")
