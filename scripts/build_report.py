#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o Report (PBIR enhanced) do projeto AuroraBrasilExportadora.pbip."""
import os, json, shutil, hashlib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PBI = os.path.join(BASE, "PowerBI")
RPT = os.path.join(PBI, "AuroraBrasilExportadora.Report")
DEF = os.path.join(RPT, "definition")
PAGES = os.path.join(DEF, "pages")
STATIC = os.path.join(RPT, "StaticResources", "RegisteredResources")
if os.path.exists(RPT):
    shutil.rmtree(RPT)
for p in [RPT, DEF, PAGES, STATIC]:
    os.makedirs(p, exist_ok=True)

S_REPORT = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.3.0/schema.json"
S_PAGES = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json"
S_PAGE = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
S_VIS = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.11.0/schema.json"
S_VERSION = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json"

# ====================================================================
# DESIGN SYSTEM — tokens
# ====================================================================
C = dict(
    base="#0E2A33",        # petroleo profundo (barra lateral / titulos)
    base2="#17495A",       # petroleo medio
    accent="#C8763C",      # cobre — destaque principal
    accent2="#8FA98F",     # verde oliva dessaturado
    sand="#E9E1D4",        # areia
    bg="#F5F3EF",          # fundo da pagina
    card="#FFFFFF",
    ink="#16262C",         # texto principal
    ink2="#5D6E75",        # texto secundario
    grid="#E3E0D9",
    pos="#1F8A70", neg="#C0453B", alert="#D9A441", info="#2F6F9F", neutro="#8C96A5",
    meta="#6B7C93", forecast="#A98BC0", ly="#B9B2A5",
)
FONT = "Segoe UI"
FONT_B = "Segoe UI Semibold"
PAL = [C["base2"], C["accent"], C["accent2"], C["info"], C["alert"], C["sand"],
       C["pos"], C["neg"], C["meta"], C["forecast"]]

# Transparencia padrao do fundo dos visuais (%). Os decorativos (shape, textbox,
# image) e o pageNavigator ficam de fora - o menu tem texto claro sobre a barra
# escura e perde contraste se ela ficar translucida.
BG_TRANSP = 35

# grid 1280x720
NAV_W, MG, GAP = 176, 20, 14
X0 = NAV_W + MG          # 196
CW = 1280 - X0 - MG      # 1064


def uid(seed):
    return hashlib.md5(seed.encode()).hexdigest()[:20]


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def sstr(v):
    return lit(f"'{v}'")


def snum(v):
    return lit(f"{v}D")


def sbool(v):
    return lit("true" if v else "false")


def color(hexv):
    return {"solid": {"color": lit(f"'{hexv}'")}}


def fld(entity, prop, measure=True, alias=None):
    key = "Measure" if measure else "Column"
    return {"field": {key: {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
            "queryRef": f"{entity}.{prop}", "nativeQueryRef": alias or prop}


def m(prop, alias=None):
    return fld("_Medidas", prop, True, alias)


def c(entity, prop, alias=None):
    return fld(entity, prop, False, alias)


# ====================================================================
# Fabrica de visuais
# ====================================================================
def txt_run(t, size=11, bold=False, col=None, italic=False):
    r = {"value": t, "textStyle": {"fontSize": f"{size}pt", "fontFamily": FONT}}
    if bold:
        r["textStyle"]["fontWeight"] = "bold"
    if italic:
        r["textStyle"]["fontStyle"] = "italic"
    if col:
        r["textStyle"]["color"] = col
    return r


def visual(page_dir, vid, vtype, x, y, w, h, roles=None, title=None, subtitle=None,
           objects=None, vco=None, z=1, sort=None, tab_order=None, alt=None,
           tooltip_page=None, drill_page=None):
    o = {"$schema": S_VIS, "name": vid,
         "position": {"x": x, "y": y, "z": z, "width": w, "height": h},
         "visual": {"visualType": vtype}}
    if roles:
        qs = {}
        for role, projs in roles.items():
            qs[role] = {"projections": projs}
        o["visual"]["query"] = {"queryState": qs}
        if sort:
            o["visual"]["query"]["sortDefinition"] = sort
    objects = dict(objects or {})
    o["visual"]["objects"] = objects

    v = dict(vco or {})
    if title is not None:
        # Sem background proprio: o titulo herda a translucidez do container,
        # senao a faixa do titulo fica opaca sobre a imagem de fundo.
        tp = {"show": sbool(True), "fontFamily": sstr(FONT_B), "fontSize": snum(12),
              "fontColor": color(C["ink"]), "alignment": sstr("left")}
        tp["text"] = title if isinstance(title, dict) else sstr(title)
        v.setdefault("title", [{"properties": tp}])
    if subtitle is not None:
        sp = {"show": sbool(True), "fontFamily": sstr(FONT), "fontSize": snum(9),
              "fontColor": color(C["ink2"]), "alignment": sstr("left")}
        sp["text"] = subtitle if isinstance(subtitle, dict) else sstr(subtitle)
        v.setdefault("subTitle", [{"properties": sp}])
    else:
        # SWD: subtitulo sempre desligado de forma explicita quando nao ha texto.
        v.setdefault("subTitle", [{"properties": {"show": sbool(False)}}])
    # 35% de transparencia deixa a imagem de fundo da pagina aparecer atras
    # dos visuais sem comprometer a leitura do conteudo.
    v.setdefault("background", [{"properties": {"show": sbool(True), "color": color(C["card"]),
                                                "transparency": snum(BG_TRANSP)}}])
    v.setdefault("border", [{"properties": {"show": sbool(True), "color": color(C["grid"]),
                                            "radius": snum(6)}}])
    if alt:
        v.setdefault("general", [{"properties": {"altText": sstr(alt)}}])
    if tab_order is not None:
        v.setdefault("visualHeader", [{"properties": {"show": sbool(False)}}])
    o["visual"]["visualContainerObjects"] = v
    # O Desktop grava drillFilterOtherVisuals em todo visual; sem a chave o
    # comportamento de cross-filter fica indefinido no carregamento.
    o["visual"]["drillFilterOtherVisuals"] = True
    if tab_order is not None:
        o["position"]["tabOrder"] = tab_order
    if tooltip_page:
        o["visual"].setdefault("objects", {})["tooltip"] = [{"properties": {
            "type": sstr("ReportPage"), "section": sstr(tooltip_page)}}]
    d = os.path.join(page_dir, "visuals", vid)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "visual.json"), "w", encoding="utf-8") as f:
        json.dump(o, f, indent=2, ensure_ascii=False)
    return vid


# --------- atalhos de visuais tipados -------------------------------
def card(pd_, seed, x, y, w, h, medida, rotulo, sub=None, cor=None, tab=None):
    return visual(pd_, uid(seed), "card", x, y, w, h,
                  roles={"Values": [m(medida)]},
                  title=rotulo.upper(),
                  subtitle=({"expr": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Medidas"}},
                                                  "Property": sub}}} if sub else None),
                  objects={"labels": [{"properties": {
                      "fontSize": snum(26), "fontFamily": sstr(FONT_B),
                      "color": color(cor or C["base"]), "labelPrecision": snum(1),
                      "labelDisplayUnits": snum(0)}}],
                      "categoryLabels": [{"properties": {"show": sbool(False)}}]},
                  tab_order=tab, alt=f"Cartao de KPI: {rotulo}")


def _axis(titulo=None, show_labels=True, size=9):
    p = {"show": sbool(True), "fontSize": snum(size), "fontFamily": sstr(FONT),
         "labelColor": color(C["ink2"]), "showAxisTitle": sbool(bool(titulo))}
    if titulo:
        p["titleText"] = sstr(titulo)
    if not show_labels:
        p["show"] = sbool(False)
    return [{"properties": p}]


def _data_colors(cores):
    return [{"properties": {"fillRule": {}, "solidColor": color(cores[0])}}]


def grafico(pd_, seed, vtype, x, y, w, h, roles, titulo, sub=None, cores=None,
            labels=False, legend=False, sort=None, tab=None, alt=None, tooltip_page=None):
    cores = cores or PAL
    objs = {
        "categoryAxis": _axis(),
        # SWD: o titulo do visual ja da o contexto - eixo nunca leva titulo.
        "valueAxis": [{"properties": {"show": sbool(not labels), "fontSize": snum(9),
                                      "labelColor": color(C["ink2"]),
                                      "showAxisTitle": sbool(False),
                                      "gridlineShow": sbool(not labels),
                                      "gridlineColor": color(C["grid"])}}],
        "legend": [{"properties": {"show": sbool(legend), "position": sstr("Top"),
                                   "fontSize": snum(9), "labelColor": color(C["ink2"])}}],
        "dataPoint": [{"properties": {"defaultColor": color(cores[0])}}],
        "labels": [{"properties": {"show": sbool(labels), "fontSize": snum(9),
                                   "fontFamily": sstr(FONT), "color": color(C["ink"]),
                                   "labelDisplayUnits": snum(0)}}],
    }
    if vtype in ("lineChart", "lineClusteredColumnComboChart", "areaChart"):
        objs["lineStyles"] = [{"properties": {"strokeWidth": snum(2.5),
                                              "showMarker": sbool(False)}}]
    return visual(pd_, uid(seed), vtype, x, y, w, h, roles=roles, title=titulo, subtitle=sub,
                  objects=objs, sort=sort, tab_order=tab,
                  alt=alt or f"Grafico {vtype}: {titulo}", tooltip_page=tooltip_page)


def tabela(pd_, seed, x, y, w, h, valores, titulo, linhas=None, sub=None, tab=None,
           tooltip_page=None):
    vtype = "pivotTable" if linhas else "tableEx"
    roles = {"Values": valores}
    if linhas:
        roles = {"Rows": linhas, "Values": valores}
    # Sem backColor nas celulas nem no cabecalho: com fundo translucido no
    # container, qualquer cor solida aqui taparia a imagem de fundo da pagina.
    objs = {"grid": [{"properties": {"gridVertical": sbool(False),
                                     "gridHorizontalColor": color(C["grid"]),
                                     "rowPadding": snum(3), "outlineColor": color(C["grid"])}}],
            "columnHeaders": [{"properties": {"fontFamily": sstr(FONT_B), "fontSize": snum(9),
                                              "fontColor": color(C["ink"]),
                                              "alignment": sstr("Center"),
                                              "autoSizeColumnWidth": sbool(True)}}],
            "values": [{"properties": {"fontSize": snum(9), "fontFamily": sstr(FONT),
                                       "fontColor": color(C["ink"])}}],
            # Alinhamento e por coluna: uma entrada por medida do well Values.
            "columnFormatting": [{"properties": {"alignment": sstr("Center")},
                                  "selector": {"metadata": v["queryRef"]}}
                                 for v in valores]}
    return visual(pd_, uid(seed), vtype, x, y, w, h, roles=roles, title=titulo, subtitle=sub,
                  objects=objs, tab_order=tab, alt=f"Tabela: {titulo}", tooltip_page=tooltip_page)


def slicer(pd_, seed, x, y, w, h, campo, titulo, modo="Dropdown", tab=None):
    objs = {"general": [{"properties": {"orientation": snum(1) if modo == "Dropdown" else snum(2)}}],
            # O nome do campo ja aparece no titulo do container; manter tambem o
            # header interno duplicaria o rotulo e nao cabe nos 42px do cabecalho.
            "header": [{"properties": {"show": sbool(False), "fontSize": snum(9),
                                       "fontColor": color(C["ink2"]), "fontFamily": sstr(FONT)}}],
            "items": [{"properties": {"fontSize": snum(9), "fontColor": color(C["ink"]),
                                      "fontFamily": sstr(FONT)}}]}
    return visual(pd_, uid(seed), "slicer", x, y, w, h, roles={"Values": [campo]},
                  title=titulo, objects=objs, tab_order=tab, alt=f"Filtro: {titulo}")


# Visual custom "HTML Content" (AppSource). Precisa constar em
# report.json > publicCustomVisuals para o Desktop carregar.
HTML_VISUAL = "htmlContent443BE3AD55E043BF878BED274D3A6855"


def painel_html(pd_, seed, x, y, w, h, medida, alt, tab=None):
    """Painel de KPIs renderizado por uma medida DAX que devolve HTML.

    Os wells do HTML Content sao "content" (a medida) e "sampling" (vazio).
    Container sem fundo/borda/titulo: o visual ja desenha os proprios cards.
    """
    vco = {"background": [{"properties": {"show": sbool(False)}}],
           "border": [{"properties": {"show": sbool(False)}}],
           "title": [{"properties": {"show": sbool(False)}}]}
    o = visual(pd_, uid(seed), HTML_VISUAL, x, y, w, h,
               roles={"sampling": [], "content": [m(medida)]},
               objects={}, vco=vco, tab_order=tab, alt=alt)
    return o


def botao_voltar(pd_, seed, x=1176, y=14, w=84, h=36):
    """Botao Voltar das paginas de drill-through.

    O tipo "Back" devolve o usuario a pagina de ORIGEM do drill, nao a uma
    pagina fixa. Sem ele o dossie vira um beco sem saida: o usuario entra e so
    sai pelo menu lateral, perdendo o contexto de onde veio.

    fill e text sao propriedades POR ESTADO (default/hover) - sem o selector
    elas nao se aplicam, o mesmo detalhe que deixava o pageNavigator invisivel.
    """
    objs = {
        "shape": [{"properties": {"tileShape": sstr("rectangle"), "roundEdge": snum(6)}}],
        "outline": [{"properties": {"show": sbool(False)}}],
        "icon": [{"properties": {"shapeType": sstr("back"), "placement": sstr("left"),
                                 "shapeStroke": snum(1.5)},
                  "selector": {"id": "default"}}],
        "text": [{"properties": {"show": sbool(True), "text": sstr("Voltar"),
                                 "fontColor": color(C["card"]), "fontSize": snum(10),
                                 "fontFamily": sstr(FONT_B),
                                 "horizontalAlignment": sstr("center")},
                  "selector": {"id": "default"}},
                 {"properties": {"fontColor": color(C["card"])},
                  "selector": {"id": "hover"}}],
        "fill": [{"properties": {"show": sbool(True), "fillColor": color(C["base"]),
                                 "transparency": snum(0)},
                  "selector": {"id": "default"}},
                 {"properties": {"show": sbool(True), "fillColor": color(C["accent"]),
                                 "transparency": snum(0)},
                  "selector": {"id": "hover"}}],
    }
    vco = {"visualLink": [{"properties": {"show": sbool(True), "type": sstr("Back")}}],
           "background": [{"properties": {"show": sbool(False)}}],
           "border": [{"properties": {"show": sbool(False)}}],
           "title": [{"properties": {"show": sbool(False)}}]}
    return visual(pd_, uid(seed), "actionButton", x, y, w, h, z=20,
                  objects=objs, vco=vco, tab_order=0,
                  alt="Voltar para a pagina de origem")


def texto(pd_, seed, x, y, w, h, runs, fundo=None, tab=None):
    vco = {"background": [{"properties": {"show": sbool(bool(fundo)),
                                          "color": color(fundo or C["bg"]),
                                          "transparency": snum(0 if fundo else 100)}}],
           "border": [{"properties": {"show": sbool(False)}}]}
    return visual(pd_, uid(seed), "textbox", x, y, w, h,
                  objects={"general": [{"properties": {
                      "paragraphs": [{"textRuns": runs}]}}]},
                  vco=vco, tab_order=tab, alt="Bloco de texto")


def forma(pd_, seed, x, y, w, h, cor, z=0):
    vco = {"background": [{"properties": {"show": sbool(True), "color": color(cor),
                                          "transparency": snum(0)}}],
           "border": [{"properties": {"show": sbool(False)}}]}
    return visual(pd_, uid(seed), "shape", x, y, w, h, z=z,
                  objects={"shape": [{"properties": {"tileShape": sstr("rectangle"),
                                                     "roundEdge": snum(0)}}],
                           "fill": [{"properties": {"show": sbool(False)}}],
                           "outline": [{"properties": {"show": sbool(False)}}]},
                  vco=vco, alt="Elemento decorativo")


# Paginas que NAO devem aparecer no menu lateral: tooltips e drill-throughs.
NAV_OCULTAR = ["tt_cliente", "tt_produto", "tt_pais", "tt_vendedor",
               "dt_cliente", "dt_pais"]


def navegador(pd_, seed):
    # O pageNavigator e da familia dos botoes: "text" e "fill" sao propriedades
    # POR ESTADO (default/hover/selected). Sem o selector a propriedade nao se
    # aplica - era por isso que o menu ficava invisivel (o texto caia na cor do
    # tema, #17495A sobre a barra #0E2A33, contraste 1,5:1).
    def _estado(sel, fundo, texto):
        return ({"properties": {"fillColor": color(fundo), "show": sbool(True),
                                "transparency": snum(0)},
                 "selector": {"id": sel}},
                {"properties": {"fontColor": color(texto), "fontSize": snum(9.5),
                                "fontFamily": sstr(FONT)},
                 "selector": {"id": sel}})

    estados = [_estado("default",  C["base"],   "#D8E2E6"),
               _estado("hover",    C["base2"],  "#FFFFFF"),
               _estado("selected", C["accent"], "#FFFFFF")]

    objs = {"pageNavigatorSettings": [{"properties": {"showTooltip": sbool(False)}}],
            "shape": [{"properties": {"tileShape": sstr("rectangle"), "roundEdge": snum(4)}}],
            "text": [{"properties": {"fontSize": snum(9.5), "fontFamily": sstr(FONT),
                                     "fontColor": color("#D8E2E6")}}] + [t for _, t in estados],
            "fill": [{"properties": {"show": sbool(True),
                                     "fillColor": color(C["base"]),
                                     "transparency": snum(0)}}] + [f for f, _ in estados],
            "outline": [{"properties": {"show": sbool(False)}}],
            "padding": [{"properties": {"top": snum(4), "bottom": snum(4)}}],
            "grid": [{"properties": {"columnCount": snum(1), "rowPadding": snum(2)}}],
            # Tooltips e drill-throughs nao sao destinos de navegacao.
            "pages": [{"properties": {"showPage": sbool(False)},
                       "selector": {"id": p}} for p in NAV_OCULTAR]}
    vco = {"background": [{"properties": {"show": sbool(False)}}],
           "border": [{"properties": {"show": sbool(False)}}]}
    return visual(pd_, uid(seed), "pageNavigator", 8, 96, NAV_W - 16, 600,
                  objects=objs, vco=vco, alt="Menu de navegacao entre paginas")


# ====================================================================
# Estrutura de paginas
# ====================================================================
PAGINAS = []       # (id, nome, tipo, largura, altura)


def nova_pagina(pid, nome, w=1280, h=720, tipo="normal"):
    d = os.path.join(PAGES, pid)
    os.makedirs(os.path.join(d, "visuals"), exist_ok=True)
    page = {"$schema": S_PAGE, "name": pid, "displayName": nome,
            "displayOption": "FitToPage", "width": w, "height": h,
            "objects": {"background": [{"properties": {"color": color(C["bg"]),
                                                       "transparency": snum(0)}}],
                        "displayArea": [{"properties": {"verticalAlignment": sstr("Top")}}]}}
    # Sao DUAS propriedades distintas, e as duas sao necessarias:
    #   pageBinding.type -> o vinculo da pagina
    #   type             -> a designacao de uso; sem ela o Desktop nao registra
    #                       a pagina e o visual so oferece "Automatico" no
    #                       dropdown de dicas de ferramenta.
    if tipo == "tooltip":
        page["type"] = "Tooltip"
        page["pageBinding"] = {"name": pid + "_b", "type": "Tooltip"}
        # Sem isto a pagina de tooltip aparece como aba normal no modo leitura.
        page["visibility"] = "HiddenInViewMode"
    elif tipo == "drill":
        page["type"] = "Drillthrough"
        page["pageBinding"] = {"name": pid + "_b", "type": "Drillthrough"}
        page["visibility"] = "HiddenInViewMode"
    PAGINAS.append((pid, nome, tipo))
    return d, page


def salvar_pagina(d, page):
    with open(os.path.join(d, "page.json"), "w", encoding="utf-8") as f:
        json.dump(page, f, indent=2, ensure_ascii=False)


def cabecalho(d, pid, titulo, pergunta):
    forma(d, pid + "navbg", 0, 0, NAV_W, 720, C["base"], z=0)
    texto(d, pid + "logo", 14, 20, NAV_W - 24, 62,
          [txt_run("AURORA BRASIL", 12, True, "#FFFFFF"),
           txt_run("\nExportadora S.A.", 8.5, False, "#9FBCC4")])
    navegador(d, pid + "nav")
    texto(d, pid + "titulo", X0, 16, CW - 300, 50,
          [txt_run(titulo, 17, True, C["base"]),
           txt_run("\n" + pergunta, 9.5, False, C["ink2"])])


# ====================================================================
# PAGINAS DE TOOLTIP  (criadas antes para referencia)
# ====================================================================
def tooltip_cliente():
    d, p = nova_pagina("tt_cliente", "Tooltip Cliente", 320, 300, "tooltip")
    texto(d, "ttc_t", 8, 6, 304, 26, [txt_run("Perfil do cliente", 10, True, C["base"])])
    tabela(d, "ttc_tb", 8, 34, 304, 254,
           [m("Receita USD"), m("Margem Bruta %"), m("Receita YoY %"), m("Data Ultima Compra"),
            m("Pedidos"), m("Segmento RFV"), m("Share of Wallet")],
           None)
    salvar_pagina(d, p)


def tooltip_produto():
    d, p = nova_pagina("tt_produto", "Tooltip Produto", 320, 260, "tooltip")
    texto(d, "ttp_t", 8, 6, 304, 26, [txt_run("Perfil do SKU", 10, True, C["base"])])
    tabela(d, "ttp_tb", 8, 34, 304, 214,
           [m("Receita USD"), m("Margem Bruta %"), m("Toneladas"),
            m("Clientes Ativos"), m("Receita YoY %")], None)
    salvar_pagina(d, p)


def tooltip_pais():
    d, p = nova_pagina("tt_pais", "Tooltip Pais", 320, 280, "tooltip")
    texto(d, "ttk_t", 8, 6, 304, 26, [txt_run("Perfil do mercado", 10, True, C["base"])])
    tabela(d, "ttk_tb", 8, 34, 304, 234,
           [m("Receita USD"), m("Margem Bruta %"), m("Toneladas"), m("Receita YoY %"),
            m("Clientes Ativos"), m("Lead Time Real"), m("% Embarques Atrasados")], None)
    salvar_pagina(d, p)


def tooltip_vendedor():
    d, p = nova_pagina("tt_vendedor", "Tooltip Vendedor", 320, 260, "tooltip")
    texto(d, "ttv_t", 8, 6, 304, 26, [txt_run("Perfil do vendedor", 10, True, C["base"])])
    tabela(d, "ttv_tb", 8, 34, 304, 214,
           [m("Receita USD"), m("Atingimento %"), m("Clientes Ativos"),
            m("Receita YoY %"), m("Margem Bruta %"), m("Concentracao Carteira Vendedor")], None)
    salvar_pagina(d, p)


# ====================================================================
# 01 — EXECUTIVE OVERVIEW
# ====================================================================
def p01():
    d, p = nova_pagina("p01_executive", "01 Executive Overview")
    cabecalho(d, "p01", "Executive Overview",
              "Estamos crescendo, atingindo meta e preservando rentabilidade?")
    slicer(d, "p01_sl_ano", X0 + CW - 280, 20, 130, 42, c("dCalendario", "Ano"), "Ano", tab=1)
    slicer(d, "p01_sl_cont", X0 + CW - 140, 20, 140, 42, c("dPais", "Continente"), "Continente", tab=2)

    # Os 8 cards nativos deram lugar a um unico painel HTML (4x2), que traz
    # sparkline de 12 meses e barra de progresso dentro de cada KPI.
    painel_html(d, "p01_kpis", X0, 76, CW, 192,
                "HTML Painel Executivo",
                "Painel de KPIs executivos em HTML", tab=10)

    grafico(d, "p01_tend", "lineClusteredColumnComboChart", X0, 280, 640, 210,
            {"Category": [c("dCalendario", "AnoMes")],
             "Y": [m("Receita USD")],
             "Y2": [m("Receita LY"), m("Meta Receita USD")]},
            "Receita mensal: realizado x ano anterior x meta", legend=True, tab=30,
            cores=[C["base2"], C["ly"], C["meta"]])

    # filledMap: a saturacao de cor e o well "Gradient". "Y" e a role Latitude -
    # a medida caia no campo de latitude e o mapa nao pintava nada.
    grafico(d, "p01_mapa", "filledMap", X0 + 654, 280, CW - 654, 210,
            {"Category": [c("dPais", "Pais")], "Gradient": [m("Receita USD")]},
            "Receita por mercado", tab=31, tooltip_page="tt_pais")

    grafico(d, "p01_wf", "waterfallChart", X0, 502, 520, 198,
            {"Category": [c("dPais", "Continente")], "Y": [m("Receita YoY")]},
            "De onde veio a variacao de receita YoY", labels=True, tab=32,
            cores=[C["pos"]])

    tabela(d, "p01_mat", X0 + 534, 502, CW - 534 - 250, 198,
           [m("Receita USD"), m("Receita YoY %"), m("Margem Bruta %"),
            m("Atingimento %"), m("Status Meta")],
           "Destaques por mercado", linhas=[c("dPais", "Pais")], tab=33,
           tooltip_page="tt_pais")

    texto(d, "p01_ins", X0 + CW - 244, 502, 244, 198,
          [txt_run("LEITURA DO PERIODO\n", 9, True, C["accent"]),
           txt_run("Use a area ao lado para diagnosticar. Os textos abaixo sao calculados "
                   "em DAX e refletem os filtros ativos.\n\n", 8.5, False, C["ink2"]),
           txt_run("Consulte as medidas: Texto Insight Crescimento, Texto Insight Margem "
                   "e Alerta Rota Critica na pasta 14 Inteligencia Comercial.", 8.5, False, C["ink2"])],
          fundo=C["sand"], tab=34)
    salvar_pagina(d, p)


# ====================================================================
# 02 — SALES PERFORMANCE
# ====================================================================
def p02():
    d, p = nova_pagina("p02_sales", "02 Sales Performance")
    cabecalho(d, "p02", "Sales Performance",
              "O ritmo comercial esta acima ou abaixo do compromisso assumido?")
    slicer(d, "p02_sl", X0 + CW - 280, 20, 280, 42, c("dCalendario", "Ano"), "Ano", tab=1)
    # Os cards nativos deram lugar a um painel HTML unico na mesma faixa.
    painel_html(d, "p02_kpis", X0, 76, CW, 92,
                "HTML Painel Vendas",
                "Painel de KPIs em HTML", tab=10)

    grafico(d, "p02_tend", "lineClusteredColumnComboChart", X0, 184, 660, 200,
            {"Category": [c("dCalendario", "AnoMes")],
             "Y": [m("Receita USD")], "Y2": [m("Atingimento %")]},
            "Realizado mensal e atingimento acumulado", legend=True, tab=20,
            cores=[C["base2"], C["accent"]])
    grafico(d, "p02_reg", "clusteredBarChart", X0 + 674, 184, CW - 674, 200,
            {"Category": [c("dCliente", "RegiaoComercial")],
             "Y": [m("Receita USD"), m("Meta Receita USD")]},
            "Regiao comercial: realizado x meta", legend=True, tab=21,
            cores=[C["base2"], C["meta"]],
            sort={"sort": [{"field": m("Receita USD")["field"], "direction": "Descending"}],
                  "isDefaultSort": True})
    grafico(d, "p02_vend", "clusteredBarChart", X0, 396, 520, 304,
            {"Category": [c("dVendedor", "NomeVendedor")], "Y": [m("Receita USD")]},
            "Receita por executivo comercial", labels=True, tab=22,
            tooltip_page="tt_vendedor",
            sort={"sort": [{"field": m("Receita USD")["field"], "direction": "Descending"}],
                  "isDefaultSort": True})
    tabela(d, "p02_dec", X0 + 534, 396, CW - 534, 304,
           [m("Receita USD"), m("Receita YoY %"), m("Contribuicao para Crescimento"),
            m("Margem Bruta %"), m("Atingimento %")],
           "Decomposicao por canal e categoria",
           linhas=[c("fVendas", "CanalVenda"), c("dProduto", "Categoria")], tab=23)
    salvar_pagina(d, p)


# ====================================================================
# 03 — CUSTOMERS
# ====================================================================
def p03():
    d, p = nova_pagina("p03_customers", "03 Customers")
    cabecalho(d, "p03", "Customers",
              "Quem sustenta a receita, quem esta escapando e o quanto isso custa?")
    slicer(d, "p03_sl", X0 + CW - 280, 20, 280, 42, c("dCliente", "Continente"), "Continente", tab=1)
    # Os cards nativos deram lugar a um painel HTML unico na mesma faixa.
    painel_html(d, "p03_kpis", X0, 76, CW, 92,
                "HTML Painel Clientes",
                "Painel de KPIs em HTML", tab=10)

    grafico(d, "p03_rfv", "clusteredBarChart", X0, 184, 340, 250,
            {"Category": [m("Segmento RFV")], "Y": [m("Clientes Ativos")]},
            "Distribuicao RFV da carteira", labels=True, tab=20, cores=[C["accent"]])
    grafico(d, "p03_par", "lineClusteredColumnComboChart", X0 + 354, 184, 400, 250,
            {"Category": [c("dCliente", "RazaoSocial")],
             "Y": [m("Receita USD")], "Y2": [m("Receita Acumulada Cliente %")]},
            "Pareto de clientes", tab=21, legend=True, cores=[C["base2"], C["accent"]],
            tooltip_page="tt_cliente",
            sort={"sort": [{"field": m("Receita USD")["field"], "direction": "Descending"}],
                  "isDefaultSort": True})
    grafico(d, "p03_conc", "clusteredBarChart", X0 + 768, 184, CW - 768, 250,
            {"Category": [m("Classe ABC Cliente")], "Y": [m("Receita USD")]},
            "Receita por classe ABC", labels=True, tab=22, cores=[C["base2"]])

    tabela(d, "p03_tab", X0, 446, 660, 254,
           [m("Receita USD"), m("Receita YoY %"), m("Margem Bruta %"), m("Recencia Dias"),
            m("Pedidos"), m("Segmento RFV"), m("Classe ABC Cliente")],
           "Carteira detalhada — ordenar por recencia para achar risco",
           linhas=[c("dCliente", "RazaoSocial")], tab=23, tooltip_page="tt_cliente")
    grafico(d, "p03_coh", "lineChart", X0 + 674, 446, CW - 674, 254,
            {"Category": [c("dCalendario", "AnoMes")],
             "Y": [m("Clientes Ativos")], "Series": [c("dCliente", "Porte")]},
            "Clientes ativos por porte (base de cohort)", legend=True, tab=24)
    salvar_pagina(d, p)


# ====================================================================
# 04 — CUSTOMER POTENTIAL
# ====================================================================
def p04():
    d, p = nova_pagina("p04_potential", "04 Customer Potential")
    cabecalho(d, "p04", "Customer Potential",
              "Onde existe receita nao capturada e qual conta merece prioridade?")
    # Os cards nativos deram lugar a um painel HTML unico na mesma faixa.
    painel_html(d, "p04_kpis", X0, 76, CW, 92,
                "HTML Painel Potencial",
                "Painel de KPIs em HTML", tab=10)

    grafico(d, "p04_sc", "scatterChart", X0, 184, 640, 300,
            {"Category": [c("dCliente", "RazaoSocial")],
             "X": [m("Receita 12M")], "Y": [m("Share of Wallet")],
             "Size": [m("Potencial Anual USD")],
             "Series": [c("dCliente", "TipoCliente")]},
            "Receita x Share of Wallet — bolha = potencial",
            sub="Quadrante inferior direito: contas grandes com baixa penetracao",
            legend=True, tab=20, tooltip_page="tt_cliente")
    tabela(d, "p04_tab", X0 + 654, 184, CW - 654, 300,
           [m("Receita 12M"), m("Potencial Anual USD"), m("Share of Wallet"),
            m("Score de Oportunidade"), m("White Space Categorias")],
           "Ranking de oportunidade", linhas=[c("dCliente", "RazaoSocial")], tab=21,
           tooltip_page="tt_cliente")
    grafico(d, "p04_cross", "clusteredBarChart", X0, 496, 520, 204,
            {"Category": [c("dProduto", "Categoria")], "Y": [m("Clientes Ativos")]},
            "Penetracao por categoria (clientes compradores)", labels=True, tab=22,
            cores=[C["accent2"]])
    tabela(d, "p04_ws", X0 + 534, 496, CW - 534, 204,
           [m("Categorias Compradas"), m("White Space Categorias"),
            m("Penetracao Categorias %"), m("Score de Oportunidade")],
           "White space por segmento", linhas=[c("dCliente", "Segmento")], tab=23)
    salvar_pagina(d, p)


# ====================================================================
# 05 — PRODUCTS
# ====================================================================
def p05():
    d, p = nova_pagina("p05_products", "05 Products")
    cabecalho(d, "p05", "Products",
              "Qual portfolio cresce com rentabilidade e qual cresce destruindo margem?")
    slicer(d, "p05_sl", X0 + CW - 280, 20, 280, 42, c("dProduto", "Categoria"), "Categoria", tab=1)
    # Os cards nativos deram lugar a um painel HTML unico na mesma faixa.
    painel_html(d, "p05_kpis", X0, 76, CW, 92,
                "HTML Painel Produtos",
                "Painel de KPIs em HTML", tab=10)

    grafico(d, "p05_bcg", "scatterChart", X0, 184, 640, 300,
            {"Category": [c("dProduto", "Subcategoria")],
             "X": [m("Receita YoY %")], "Y": [m("Margem Bruta %")],
             "Size": [m("Receita USD")], "Series": [c("dProduto", "Categoria")]},
            "Matriz BCG adaptada: crescimento x margem",
            sub="Bolha = receita. Alto crescimento com margem baixa merece revisao de preco",
            legend=True, tab=20, tooltip_page="tt_produto")
    tabela(d, "p05_tab", X0 + 654, 184, CW - 654, 300,
           [m("Receita USD"), m("Receita YoY %"), m("Margem Bruta %"),
            m("Margem por Kg"), m("Classe ABC Produto")],
           "Portfolio por SKU", linhas=[c("dProduto", "Produto")], tab=21,
           tooltip_page="tt_produto")
    grafico(d, "p05_cat", "clusteredBarChart", X0, 496, 520, 204,
            {"Category": [c("dProduto", "Categoria")],
             "Y": [m("Receita USD"), m("Margem Bruta USD")]},
            "Receita e margem por categoria", legend=True, tab=22,
            cores=[C["base2"], C["accent"]])
    grafico(d, "p05_evo", "lineChart", X0 + 534, 496, CW - 534, 204,
            {"Category": [c("dCalendario", "AnoMes")],
             "Y": [m("Margem Bruta %")], "Series": [c("dProduto", "Categoria")]},
            "Evolucao da margem por categoria", legend=True, tab=23)
    salvar_pagina(d, p)


# ====================================================================
# 06 — MARKETS
# ====================================================================
def p06():
    d, p = nova_pagina("p06_markets", "06 Markets")
    cabecalho(d, "p06", "Markets",
              "Quais mercados sustentam hoje e quais sustentarao os proximos tres anos?")
    # Os cards nativos deram lugar a um painel HTML unico na mesma faixa.
    painel_html(d, "p06_kpis", X0, 76, CW, 92,
                "HTML Painel Mercados",
                "Painel de KPIs em HTML", tab=10)

    grafico(d, "p06_map", "map", X0, 184, 620, 300,
            {"Category": [c("dPais", "Pais")], "Size": [m("Receita USD")]},
            "Distribuicao global da receita", tab=20, tooltip_page="tt_pais")
    grafico(d, "p06_opp", "scatterChart", X0 + 634, 184, CW - 634, 300,
            {"Category": [c("dPais", "Pais")],
             "X": [m("Receita YoY %")], "Y": [m("Margem Bruta %")],
             "Size": [m("Receita USD")], "Series": [c("dPais", "Continente")]},
            "Market Opportunity Matrix", sub="Crescimento x margem, bolha = receita",
            legend=True, tab=21, tooltip_page="tt_pais")
    grafico(d, "p06_rank", "clusteredBarChart", X0, 496, 480, 204,
            {"Category": [c("dPais", "Pais")], "Y": [m("Receita USD")]},
            "Ranking de mercados", labels=True, tab=22, tooltip_page="tt_pais",
            sort={"sort": [{"field": m("Receita USD")["field"], "direction": "Descending"}],
                  "isDefaultSort": True})
    tabela(d, "p06_mat", X0 + 494, 496, CW - 494, 204,
           [m("Receita USD"), m("Receita YoY %"), m("Margem Bruta %"), m("Lead Time Real")],
           "Mercado x categoria", linhas=[c("dPais", "Continente"), c("dProduto", "Categoria")],
           tab=23)
    salvar_pagina(d, p)


# ====================================================================
# 07 — PROFITABILITY
# ====================================================================
def p07():
    d, p = nova_pagina("p07_profit", "07 Profitability")
    cabecalho(d, "p07", "Profitability",
              "Entre a receita bruta e a margem, onde o valor esta sendo consumido?")
    # Os cards nativos deram lugar a um painel HTML unico na mesma faixa.
    painel_html(d, "p07_kpis", X0, 76, CW, 92,
                "HTML Painel Rentabilidade",
                "Painel de KPIs em HTML", tab=10)

    grafico(d, "p07_wf", "waterfallChart", X0, 184, 640, 280,
            {"Category": [c("dProduto", "Categoria")], "Y": [m("Margem Bruta USD")]},
            "Formacao da margem por categoria", labels=True, tab=20, cores=[C["base2"]])
    tabela(d, "p07_ponte", X0 + 654, 184, CW - 654, 280,
           [m("Receita Bruta USD"), m("Descontos USD"), m("Receita USD"),
            m("Custo Produto USD"), m("Frete USD"), m("Seguro USD"),
            m("Despesas Exportacao USD"), m("Margem Bruta USD"), m("Margem Bruta %")],
           "Ponte economica detalhada", linhas=[c("fVendas", "Incoterm")], tab=21)
    grafico(d, "p07_cli", "scatterChart", X0, 476, 520, 224,
            {"Category": [c("dCliente", "RazaoSocial")],
             "X": [m("Receita USD")], "Y": [m("Margem Bruta %")],
             "Size": [m("Toneladas")], "Series": [c("dCliente", "Segmento")]},
            "Cliente: receita x margem", legend=False, tab=22, tooltip_page="tt_cliente")
    tabela(d, "p07_tab", X0 + 534, 476, CW - 534, 224,
           [m("Receita USD"), m("Margem Bruta %"), m("Frete % Receita"), m("Desconto %")],
           "Rentabilidade por vendedor e Incoterm",
           linhas=[c("dVendedor", "NomeVendedor")], tab=23, tooltip_page="tt_vendedor")
    salvar_pagina(d, p)


# ====================================================================
# 08 — LOGISTICS
# ====================================================================
def p08():
    d, p = nova_pagina("p08_logistics", "08 Logistics")
    cabecalho(d, "p08", "Logistics",
              "Onde a operacao perde prazo e quanto isso custa por quilo?")
    # Os cards nativos deram lugar a um painel HTML unico na mesma faixa.
    painel_html(d, "p08_kpis", X0, 76, CW, 92,
                "HTML Painel Logistica",
                "Painel de KPIs em HTML", tab=10)

    grafico(d, "p08_rota", "clusteredBarChart", X0, 184, 520, 250,
            {"Category": [c("dPais", "Pais")], "Y": [m("% Embarques Atrasados")]},
            "Rotas com maior incidencia de atraso", labels=True, tab=20, cores=[C["neg"]],
            sort={"sort": [{"field": m("% Embarques Atrasados")["field"], "direction": "Descending"}],
                  "isDefaultSort": True})
    grafico(d, "p08_transp", "clusteredBarChart", X0 + 534, 184, CW - 534, 250,
            {"Category": [c("dTransportadora", "Transportadora")],
             "Y": [m("OTIF %")]},
            "Performance por transportadora", labels=True, tab=21, cores=[C["base2"]],
            sort={"sort": [{"field": m("OTIF %")["field"], "direction": "Ascending"}],
                  "isDefaultSort": True})
    grafico(d, "p08_motivo", "clusteredBarChart", X0, 446, 380, 254,
            {"Category": [c("fEmbarques", "MotivoAtraso")], "Y": [m("Embarques Atrasados")]},
            "Motivos de atraso", labels=True, tab=22, cores=[C["alert"]],
            sort={"sort": [{"field": m("Embarques Atrasados")["field"], "direction": "Descending"}],
                  "isDefaultSort": True})
    grafico(d, "p08_lt", "lineChart", X0 + 394, 446, 380, 254,
            {"Category": [c("dCalendario", "AnoMes")],
             "Y": [m("Lead Time Real"), m("Lead Time Previsto")]},
            "Lead time real x previsto", legend=True, tab=23, cores=[C["accent"], C["meta"]])
    tabela(d, "p08_tab", X0 + 788, 446, CW - 788, 254,
           [m("Embarques"), m("OTIF %"), m("Frete por Kg")],
           "Modal e porto de origem",
           linhas=[c("fEmbarques", "Modal"), c("dPorto", "Porto")], tab=24)
    salvar_pagina(d, p)


# ====================================================================
# 09 — SALES TEAM
# ====================================================================
def p09():
    d, p = nova_pagina("p09_team", "09 Sales Team")
    cabecalho(d, "p09", "Sales Team",
              "Quem entrega, quem depende de um unico cliente e quem precisa de apoio?")
    # Os cards nativos deram lugar a um painel HTML unico na mesma faixa.
    painel_html(d, "p09_kpis", X0, 76, CW, 92,
                "HTML Painel Equipe",
                "Painel de KPIs em HTML", tab=10)

    grafico(d, "p09_quad", "scatterChart", X0, 184, 620, 290,
            {"Category": [c("dVendedor", "NomeVendedor")],
             "X": [m("Receita YoY %")], "Y": [m("Atingimento %")],
             "Size": [m("Receita USD")], "Series": [c("dVendedor", "ContinenteResponsavel")]},
            "Quadrante: crescimento x atingimento",
            sub="Bolha = receita. Canto inferior esquerdo exige plano de acao",
            legend=True, tab=20, tooltip_page="tt_vendedor")
    tabela(d, "p09_tab", X0 + 634, 184, CW - 634, 290,
           [m("Receita USD"), m("Meta Receita USD"), m("Atingimento %"), m("Gap Meta USD"),
            m("Clientes Ativos"), m("Concentracao Carteira Vendedor")],
           "Ranking comercial", linhas=[c("dVendedor", "NomeVendedor")], tab=21,
           tooltip_page="tt_vendedor")
    grafico(d, "p09_meta", "clusteredBarChart", X0, 486, 520, 214,
            {"Category": [c("dVendedor", "NomeVendedor")],
             "Y": [m("Receita USD"), m("Meta Receita USD")]},
            "Realizado x meta por vendedor", legend=True, tab=22,
            cores=[C["base2"], C["meta"]])
    grafico(d, "p09_conc", "clusteredBarChart", X0 + 534, 486, CW - 534, 214,
            {"Category": [c("dVendedor", "NomeVendedor")],
             "Y": [m("Concentracao Carteira Vendedor")]},
            "Dependencia do maior cliente da carteira", labels=True, tab=23, cores=[C["alert"]],
            sort={"sort": [{"field": m("Concentracao Carteira Vendedor")["field"],
                            "direction": "Descending"}], "isDefaultSort": True})
    salvar_pagina(d, p)


# ====================================================================
# 10 — FINANCE
# ====================================================================
def p10():
    d, p = nova_pagina("p10_finance", "10 Finance")
    cabecalho(d, "p10", "Finance",
              "Quanto do faturamento ainda nao virou caixa e qual cliente trava o ciclo?")
    # Os cards nativos deram lugar a um painel HTML unico na mesma faixa.
    painel_html(d, "p10_kpis", X0, 76, CW, 92,
                "HTML Painel Financeiro",
                "Painel de KPIs em HTML", tab=10)

    grafico(d, "p10_aging", "clusteredBarChart", X0, 184, 520, 250,
            {"Category": [m("Faixa Aging")], "Y": [m("Saldo em Aberto")]},
            "Aging da carteira", labels=True, tab=20, cores=[C["base2"]])
    grafico(d, "p10_status", "clusteredBarChart", X0 + 534, 184, CW - 534, 250,
            {"Category": [c("fRecebimentos", "Status")], "Y": [m("Contas a Receber")]},
            "Situacao dos titulos", labels=True, tab=21, cores=[C["accent"]])
    tabela(d, "p10_dev", X0, 446, 660, 254,
           [m("Contas a Receber"), m("Saldo Vencido"), m("Dias Medios de Atraso"),
            m("Prazo Medio Recebimento"), m("Inadimplencia %")],
           "Principais devedores", linhas=[c("dCliente", "RazaoSocial")], tab=22,
           tooltip_page="tt_cliente")
    grafico(d, "p10_forma", "clusteredBarChart", X0 + 674, 446, CW - 674, 254,
            {"Category": [c("fRecebimentos", "FormaPagamento")],
             "Y": [m("Saldo Vencido")]},
            "Saldo vencido por forma de pagamento", labels=True, tab=23, cores=[C["neg"]])
    salvar_pagina(d, p)


# ====================================================================
# 11 — FORECAST & BUDGET
# ====================================================================
def p11():
    d, p = nova_pagina("p11_forecast", "11 Forecast e Budget")
    cabecalho(d, "p11", "Forecast & Budget",
              "Se a tendencia continuar, fechamos o ano acima ou abaixo do compromisso?")
    # Os cards nativos deram lugar a um painel HTML unico na mesma faixa.
    painel_html(d, "p11_kpis", X0, 76, CW, 92,
                "HTML Painel Forecast",
                "Painel de KPIs em HTML", tab=10)

    grafico(d, "p11_linha", "lineChart", X0, 184, CW, 260,
            {"Category": [c("dCalendario", "AnoMes")],
             "Y": [m("Receita USD"), m("Receita Orcada USD"),
                   m("Receita Forecast USD"), m("Meta Receita USD")]},
            "Linha temporal: realizado, orcado, forecast e meta", legend=True, tab=20,
            cores=[C["base2"], C["meta"], C["forecast"], C["accent"]])
    grafico(d, "p11_saz", "columnChart", X0, 456, 520, 244,
            {"Category": [c("dCalendario", "MesAbreviado")],
             "Y": [m("Sazonalidade Historica %")]},
            "Peso historico de cada mes (base do orcamento adaptativo)", labels=True,
            tab=21, cores=[C["accent2"]])
    tabela(d, "p11_tab", X0 + 534, 456, CW - 534, 244,
           [m("Receita USD"), m("Receita Orcada USD"), m("Actual vs Budget %"),
            m("Receita Forecast USD"), m("Forecast x Orcado")],
           "Realizado x orcado x forecast por regiao",
           linhas=[c("fOrcamento", "Regiao"), c("fOrcamento", "Categoria")], tab=22)
    salvar_pagina(d, p)


def p12():
    """Guia de analise: documentacao navegavel dentro do proprio relatorio.

    O conteudo e um <details> por pagina - o cabecalho e o botao, o corpo
    expande. Como e HTML nativo, nao depende de indicador nem de bookmark.
    """
    d, p = nova_pagina("p12_guia", "12 Guia de Análise")
    cabecalho(d, "p12", "Guia de Análise",
              "O que cada pagina responde e o que cada visual permite analisar")
    painel_html(d, "p12_guia_html", X0, 76, CW, 624,
                "HTML Guia de Analise",
                "Guia de analise do relatorio", tab=2)
    salvar_pagina(d, p)


# ====================================================================
# DRILL-THROUGH
# ====================================================================
def drill_cliente():
    d, p = nova_pagina("dt_cliente", "Detalhe Cliente", tipo="drill")
    p["filterConfig"] = {"filters": [{
        "name": "dtCliente",
        "field": {"Column": {"Expression": {"SourceRef": {"Entity": "dCliente"}},
                             "Property": "RazaoSocial"}},
        "type": "Categorical",
        "howCreated": "Drillthrough"}]}
    cabecalho(d, "dtc", "Detalhe do Cliente",
              "Historico completo da conta selecionada")
    painel_html(d, "dtc_kpis", X0, 76, CW, 92,
                "HTML Painel Detalhe Cliente",
                "Painel de KPIs do cliente selecionado", tab=10)
    botao_voltar(d, "dtc_back")
    grafico(d, "dtc_ln", "lineChart", X0, 184, 640, 250,
            {"Category": [c("dCalendario", "AnoMes")],
             "Y": [m("Receita USD"), m("Receita LY")]},
            "Historico mensal da conta", legend=True, tab=20, cores=[C["base2"], C["ly"]])
    grafico(d, "dtc_cat", "clusteredBarChart", X0 + 654, 184, CW - 654, 250,
            {"Category": [c("dProduto", "Categoria")], "Y": [m("Receita USD")]},
            "Mix de categorias compradas", labels=True, tab=21, cores=[C["accent"]])
    tabela(d, "dtc_tb", X0, 446, CW, 254,
           [m("Receita USD"), m("Margem Bruta USD"), m("Margem Bruta %"),
            m("Toneladas"), m("Pedidos"), m("Frete % Receita")],
           "Detalhe por produto", linhas=[c("dProduto", "Produto")], tab=22)
    salvar_pagina(d, p)


def drill_pais():
    d, p = nova_pagina("dt_pais", "Detalhe Mercado", tipo="drill")
    p["filterConfig"] = {"filters": [{
        "name": "dtPais",
        "field": {"Column": {"Expression": {"SourceRef": {"Entity": "dPais"}}, "Property": "Pais"}},
        "type": "Categorical", "howCreated": "Drillthrough"}]}
    cabecalho(d, "dtp", "Detalhe do Mercado", "Diagnostico completo do pais selecionado")
    painel_html(d, "dtp_kpis", X0, 76, CW, 92,
                "HTML Painel Detalhe Mercado",
                "Painel de KPIs do mercado selecionado", tab=10)
    botao_voltar(d, "dtp_back")
    grafico(d, "dtp_ln", "lineChart", X0, 184, 640, 250,
            {"Category": [c("dCalendario", "AnoMes")], "Y": [m("Receita USD")]},
            "Evolucao do mercado", tab=20, cores=[C["base2"]])
    grafico(d, "dtp_cli", "clusteredBarChart", X0 + 654, 184, CW - 654, 250,
            {"Category": [c("dCliente", "RazaoSocial")], "Y": [m("Receita USD")]},
            "Clientes do mercado", labels=True, tab=21, cores=[C["accent"]],
            sort={"sort": [{"field": m("Receita USD")["field"], "direction": "Descending"}],
                  "isDefaultSort": True})
    tabela(d, "dtp_tb", X0, 446, CW, 254,
           [m("Receita USD"), m("Margem Bruta %"), m("Toneladas"),
            m("Lead Time Real"), m("% Embarques Atrasados"), m("Frete por Kg")],
           "Categorias e desempenho logistico",
           linhas=[c("dProduto", "Categoria"), c("fVendas", "Incoterm")], tab=22)
    salvar_pagina(d, p)


# ====================================================================
# TEMA
# ====================================================================
def tema():
    t = {
        "name": "AuroraBrasilTheme",
        "dataColors": PAL,
        "background": C["bg"], "foreground": C["ink"], "tableAccent": C["accent"],
        "good": C["pos"], "bad": C["neg"], "neutral": C["alert"],
        "maximum": C["base"], "minimum": C["sand"],
        "textClasses": {
            "callout": {"fontSize": 26, "fontFace": FONT_B, "color": C["base"]},
            "title": {"fontSize": 12, "fontFace": FONT_B, "color": C["ink"]},
            "header": {"fontSize": 11, "fontFace": FONT_B, "color": C["ink"]},
            "label": {"fontSize": 9, "fontFace": FONT, "color": C["ink2"]},
        },
        "visualStyles": {
            "*": {"*": {
                "background": [{"show": True, "color": {"solid": {"color": C["card"]}},
                               "transparency": 0}],
                "border": [{"show": True, "color": {"solid": {"color": C["grid"]}}, "radius": 6}],
                "visualHeader": [{"show": False}],
                "title": [{"show": True, "fontColor": {"solid": {"color": C["ink"]}},
                           "background": {"solid": {"color": C["card"]}},
                           "alignment": "left", "fontSize": 12, "fontFamily": FONT_B}],
                "outspacePane": [{"backgroundColor": {"solid": {"color": C["card"]}},
                                  "foregroundColor": {"solid": {"color": C["ink"]}},
                                  "titleSize": 12, "searchTextSize": 10}],
            }},
            "page": {"*": {"background": [{"color": {"solid": {"color": C["bg"]}},
                                           "transparency": 0}]}},
        },
    }
    with open(os.path.join(STATIC, "AuroraBrasilTheme.json"), "w", encoding="utf-8") as f:
        json.dump(t, f, indent=2, ensure_ascii=False)


# ====================================================================
def main():
    tema()
    tooltip_cliente(); tooltip_produto(); tooltip_pais(); tooltip_vendedor()
    p01(); p02(); p03(); p04(); p05(); p06(); p07(); p08(); p09(); p10(); p11(); p12()
    drill_cliente(); drill_pais()

    ordem = [x[0] for x in PAGINAS if x[2] == "normal"] + \
            [x[0] for x in PAGINAS if x[2] != "normal"]
    with open(os.path.join(PAGES, "pages.json"), "w", encoding="utf-8") as f:
        json.dump({"$schema": S_PAGES, "pageOrder": ordem,
                   "activePageName": "p01_executive",
                   "landingPageName": "p01_executive"}, f, indent=2)

    report = {
        "$schema": S_REPORT,
        # O name do customTheme precisa ser identico ao name do item em
        # resourcePackages - e o Desktop grava ambos com a extensao .json.
        "themeCollection": {"customTheme": {"name": "AuroraBrasilTheme.json",
                                            "type": "RegisteredResources"}},
        "publicCustomVisuals": [HTML_VISUAL],
        "resourcePackages": [{
            "name": "RegisteredResources", "type": "RegisteredResources",
            "items": [{"name": "AuroraBrasilTheme.json", "path": "AuroraBrasilTheme.json",
                       "type": "CustomTheme"}]}],
        # Somente chaves confirmadas em report.json gerado pelo proprio Desktop.
        "settings": {
            "useStylableVisualContainerHeader": True,
            "exportDataMode": "AllowSummarized",
            "defaultFilterActionIsDataFilter": True,
            "defaultDrillFilterOtherVisuals": True,
            "allowChangeFilterTypes": True,
            "useEnhancedTooltips": True,
        },
        "objects": {
            "section": [{"properties": {
                "verticalAlignment": {"expr": {"Literal": {"Value": "'Top'"}}}}}]
        },
    }
    with open(os.path.join(DEF, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Artefato obrigatorio do PBIR enhanced: sem ele o ExplorationSerializer
    # aborta com "Cannot find file 'version.json'" ao ler o ReportDocument.
    with open(os.path.join(DEF, "version.json"), "w", encoding="utf-8") as f:
        json.dump({"$schema": S_VERSION, "version": "2.0.0"}, f, indent=2)

    with open(os.path.join(RPT, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump({"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
                   "version": "4.0",
                   "datasetReference": {"byPath": {"path": "../AuroraBrasilExportadora.SemanticModel"}}},
                  f, indent=2)

    with open(os.path.join(RPT, ".platform"), "w", encoding="utf-8") as f:
        json.dump({"$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
                   "metadata": {"type": "Report", "displayName": "AuroraBrasilExportadora"},
                   "config": {"version": "2.0", "logicalId": "7b3e9c14-58a2-4d61-9f0e-2c86d1b47a35"}}, f, indent=2)

    # arquivo .pbip
    with open(os.path.join(PBI, "AuroraBrasilExportadora.pbip"), "w", encoding="utf-8") as f:
        json.dump({"$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
                   "version": "1.0",
                   "artifacts": [{"report": {"path": "AuroraBrasilExportadora.Report"}}],
                   "settings": {"enableAutoRecovery": True}}, f, indent=2)

    nvis = sum(len(os.listdir(os.path.join(PAGES, pid, "visuals"))) for pid, _, _ in PAGINAS)
    print(f"Paginas: {len(PAGINAS)} "
          f"(normais {sum(1 for x in PAGINAS if x[2]=='normal')}, "
          f"tooltips {sum(1 for x in PAGINAS if x[2]=='tooltip')}, "
          f"drill-through {sum(1 for x in PAGINAS if x[2]=='drill')}) | Visuais: {nvis}")


if __name__ == "__main__":
    main()
