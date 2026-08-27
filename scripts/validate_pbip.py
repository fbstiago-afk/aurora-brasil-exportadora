#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QA automatizado do projeto PBIP: TMDL, PBIR, referencias e layout."""
import os, re, json, glob, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PBI = os.path.join(BASE, "PowerBI")
SM = os.path.join(PBI, "AuroraBrasilExportadora.SemanticModel", "definition")
RPT = os.path.join(PBI, "AuroraBrasilExportadora.Report", "definition")
PAGES = os.path.join(RPT, "pages")

erros, avisos, ok = [], [], []


def E(m): erros.append(m)
def A(m): avisos.append(m)
def O(m): ok.append(m)


# ---------------------------------------------------------- 1. arquivos
for f in [os.path.join(PBI, "AuroraBrasilExportadora.pbip"),
          os.path.join(SM, "model.tmdl"), os.path.join(SM, "database.tmdl"),
          os.path.join(SM, "relationships.tmdl"), os.path.join(SM, "expressions.tmdl"),
          os.path.join(RPT, "report.json"), os.path.join(PAGES, "pages.json"),
          os.path.join(PBI, "AuroraBrasilExportadora.Report", "definition.pbir"),
          os.path.join(PBI, "AuroraBrasilExportadora.SemanticModel", "definition.pbism")]:
    (O if os.path.exists(f) else E)(f"Arquivo obrigatorio: {os.path.relpath(f, BASE)}")

# ---------------------------------------------------------- 2. JSON valido
n_json = 0
for f in glob.glob(os.path.join(PBI, "**", "*.json"), recursive=True) + \
         glob.glob(os.path.join(PBI, "**", "*.pbip"), recursive=True) + \
         glob.glob(os.path.join(PBI, "**", "*.pbir"), recursive=True) + \
         glob.glob(os.path.join(PBI, "**", "*.pbism"), recursive=True):
    try:
        json.load(open(f, encoding="utf-8"))
        n_json += 1
    except Exception as ex:
        E(f"JSON invalido em {os.path.relpath(f, BASE)}: {ex}")
O(f"{n_json} arquivos JSON com sintaxe valida")

# ---------------------------------------------------------- 3. modelo
colunas, tabelas = set(), set()
for f in glob.glob(os.path.join(SM, "tables", "*.tmdl")):
    txt = open(f, encoding="utf-8").read()
    t = re.match(r"table (\S+)", txt).group(1)
    tabelas.add(t)
    for mt in re.finditer(r"^\tcolumn (\S+)", txt, re.M):
        colunas.add((t, mt.group(1)))
med_txt = open(os.path.join(SM, "tables", "_Medidas.tmdl"), encoding="utf-8").read()
medidas = set(re.findall(r"^\tmeasure '([^']+)'", med_txt, re.M))
O(f"Modelo: {len(tabelas)} tabelas, {len(colunas)} colunas, {len(medidas)} medidas")

# refs de coluna dentro do DAX
for tb, cl in set(re.findall(r"(\w+)\[(\w+)\]", med_txt)):
    if tb in tabelas and (tb, cl) not in colunas:
        E(f"DAX referencia coluna inexistente: {tb}[{cl}]")

# refs de medida dentro do DAX
for ref in set(re.findall(r"(?<![\w'])\[([A-Z][^\]\n]{2,60})\]", med_txt)):
    if ref not in medidas and not re.match(r"^[a-z]", ref):
        if ref not in {"Coluna = Int64.Type"}:
            E(f"DAX referencia medida inexistente: [{ref}]")

# display folders e formatos
sem_pasta = len(re.findall(r"^\tmeasure ", med_txt, re.M)) - med_txt.count("displayFolder:")
if sem_pasta > 0:
    A(f"{sem_pasta} medidas sem displayFolder")
else:
    O("Todas as medidas possuem displayFolder")

# ---------------------------------------------------------- 4. relacionamentos
rel = open(os.path.join(SM, "relationships.tmdl"), encoding="utf-8").read()
pares = re.findall(r"fromColumn: (\S+)\.(\S+)\n\ttoColumn: (\S+)\.(\S+)", rel)
n_inativos = rel.count("isActive: false")
for ft, fc, tt, tc in pares:
    if (ft, fc) not in colunas:
        E(f"Relacionamento com coluna inexistente: {ft}[{fc}]")
    if (tt, tc) not in colunas:
        E(f"Relacionamento com coluna inexistente: {tt}[{tc}]")
    if not ft.startswith("f") and not tt.startswith("d"):
        A(f"Relacionamento fora do padrao estrela: {ft} -> {tt}")
O(f"Relacionamentos: {len(pares)} ({n_inativos} inativos para USERELATIONSHIP)")
if rel.count("crossFilteringBehavior: bothDirections"):
    E("Existe relacionamento bidirecional")
else:
    O("Nenhum relacionamento bidirecional")

# lado 1 precisa ser unico -> verificado na geracao dos dados; aqui checamos duplicidade de par
if len(pares) != len(set(pares)):
    E("Relacionamentos duplicados")

# ---------------------------------------------------------- 5. relatorio
pages_meta = json.load(open(os.path.join(PAGES, "pages.json"), encoding="utf-8"))
ordem = pages_meta["pageOrder"]
pastas = sorted(os.listdir(PAGES))
pastas = [p for p in pastas if os.path.isdir(os.path.join(PAGES, p))]
if set(ordem) != set(pastas):
    E(f"pages.json divergente das pastas: {set(ordem) ^ set(pastas)}")
else:
    O(f"pages.json coerente com {len(pastas)} paginas")
if pages_meta.get("activePageName") not in ordem:
    E("activePageName invalido")

total_vis, tooltips, drills = 0, 0, 0
for pid in pastas:
    pg = json.load(open(os.path.join(PAGES, pid, "page.json"), encoding="utf-8"))
    W, H = pg.get("width", 1280), pg.get("height", 720)
    if pg.get("name") != pid:
        E(f"{pid}: campo name divergente da pasta")
    if pg.get("pageBinding", {}).get("type") == "Tooltip":
        tooltips += 1
    if pg.get("pageBinding", {}).get("type") == "Drillthrough":
        drills += 1
    caixas = []
    vdir = os.path.join(PAGES, pid, "visuals")
    for vid in os.listdir(vdir):
        vj = json.load(open(os.path.join(vdir, vid, "visual.json"), encoding="utf-8"))
        total_vis += 1
        pos = vj["position"]
        if pos["x"] < 0 or pos["y"] < 0 or pos["x"] + pos["width"] > W + 0.5 \
           or pos["y"] + pos["height"] > H + 0.5:
            E(f"{pid}/{vid}: visual fora dos limites da pagina "
              f"({pos['x']},{pos['y']},{pos['width']}x{pos['height']}) em {W}x{H}")
        if pos["width"] < 60 or pos["height"] < 24:
            A(f"{pid}/{vid}: visual muito pequeno")
        if vj["visual"].get("visualType") not in ("shape", "textbox"):
            caixas.append((pos, vid))
        # referencias de campo
        qs = vj["visual"].get("query", {}).get("queryState", {})
        for role, blk in qs.items():
            for proj in blk["projections"]:
                fdef = proj["field"]
                if "Measure" in fdef:
                    ent = fdef["Measure"]["Expression"]["SourceRef"]["Entity"]
                    prop = fdef["Measure"]["Property"]
                    if prop not in medidas:
                        E(f"{pid}/{vid}: medida inexistente '{prop}'")
                    if ent != "_Medidas":
                        A(f"{pid}/{vid}: medida fora de _Medidas ({ent})")
                else:
                    ent = fdef["Column"]["Expression"]["SourceRef"]["Entity"]
                    prop = fdef["Column"]["Property"]
                    if (ent, prop) not in colunas:
                        E(f"{pid}/{vid}: coluna inexistente {ent}[{prop}]")
        # titulo obrigatorio para visuais de dados
        vco = vj["visual"].get("visualContainerObjects", {})
        if qs and "title" not in vco:
            A(f"{pid}/{vid}: visual de dados sem titulo")
        if "general" not in vco and qs:
            A(f"{pid}/{vid}: sem alt text")
    # sobreposicao
    for i in range(len(caixas)):
        for j in range(i + 1, len(caixas)):
            a, b = caixas[i][0], caixas[j][0]
            ox = min(a["x"] + a["width"], b["x"] + b["width"]) - max(a["x"], b["x"])
            oy = min(a["y"] + a["height"], b["y"] + b["height"]) - max(a["y"], b["y"])
            if ox > 2 and oy > 2:
                E(f"{pid}: sobreposicao entre {caixas[i][1]} e {caixas[j][1]} "
                  f"({ox:.0f}x{oy:.0f}px)")
O(f"Relatorio: {total_vis} visuais, {tooltips} tooltips, {drills} drill-through")

# tema
tema_p = os.path.join(PBI, "AuroraBrasilExportadora.Report", "StaticResources",
                      "RegisteredResources", "AuroraBrasilTheme.json")
(O if os.path.exists(tema_p) else E)("Tema customizado registrado")
rep = json.load(open(os.path.join(RPT, "report.json"), encoding="utf-8"))
if rep.get("themeCollection", {}).get("customTheme", {}).get("name") != "AuroraBrasilTheme":
    E("report.json nao referencia o tema customizado")

# pbir -> semantic model
pbir = json.load(open(os.path.join(PBI, "AuroraBrasilExportadora.Report", "definition.pbir"),
                      encoding="utf-8"))
alvo = os.path.normpath(os.path.join(PBI, "AuroraBrasilExportadora.Report",
                                     pbir["datasetReference"]["byPath"]["path"]))
(O if os.path.isdir(alvo) else E)("definition.pbir aponta para o Semantic Model existente")

# .platform: logicalId precisa ser GUID valido
import uuid as _uuid
for plat in glob.glob(os.path.join(PBI, "**", ".platform"), recursive=True):
    try:
        cfg = json.load(open(plat, encoding="utf-8"))["config"]["logicalId"]
        _uuid.UUID(cfg)
        O(f"logicalId GUID valido em {os.path.basename(os.path.dirname(plat))}/.platform")
    except Exception as ex:
        E(f"logicalId invalido em {os.path.relpath(plat, BASE)}: {ex}")

# parametro Power Query
expr = open(os.path.join(SM, "expressions.tmdl"), encoding="utf-8").read()
(O if "pBasePath" in expr and "IsParameterQuery=true" in expr else E)(
    "Parametro Power Query pBasePath declarado")
n_param = sum(1 for f in glob.glob(os.path.join(SM, "tables", "*.tmdl"))
              if "pBasePath" in open(f, encoding="utf-8").read())
O(f"{n_param} queries usam o parametro pBasePath")

# ---------------------------------------------------------- saida
print("\n".join("OK    | " + x for x in ok))
print("\n".join("AVISO | " + x for x in avisos))
print("\n".join("ERRO  | " + x for x in erros))
print(f"\nRESULTADO: {len(ok)} verificacoes OK | {len(avisos)} avisos | {len(erros)} erros")
sys.exit(1 if erros else 0)
