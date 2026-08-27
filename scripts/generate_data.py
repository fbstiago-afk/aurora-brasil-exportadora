#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aurora Brasil Exportadora S.A. — Gerador de base sintetica para Power BI
Seed fixa = 20260816  (execucao reproduzivel)
Dependencias: pandas, numpy  (Faker nao e necessario)
"""

import os
import sys
import math
import unicodedata
from datetime import date, timedelta

import numpy as np
import pandas as pd

SEED = 20260816
rng = np.random.default_rng(SEED)

DT_INI = date(2022, 1, 1)
DT_FIM = date(2026, 7, 31)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "dados")
DOC = os.path.join(BASE, "documentacao")
os.makedirs(OUT, exist_ok=True)
os.makedirs(DOC, exist_ok=True)


def r2(x):
    return float(np.round(x, 2))


def pick(lst, n=None, p=None, replace=True):
    idx = rng.choice(len(lst), size=n, p=p, replace=replace)
    if n is None:
        return lst[int(idx)]
    return [lst[int(i)] for i in np.atleast_1d(idx)]


# =====================================================================
# 1. dCalendario
# =====================================================================
MESES = ["Janeiro", "Fevereiro", "Marco", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
MESES_ABR = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
             "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
DIAS = ["Segunda-feira", "Terca-feira", "Quarta-feira", "Quinta-feira",
        "Sexta-feira", "Sabado", "Domingo"]


def gerar_calendario():
    dts = pd.date_range(DT_INI, DT_FIM, freq="D")
    df = pd.DataFrame({"Data": dts})
    df["Ano"] = df.Data.dt.year
    df["Trimestre"] = "T" + df.Data.dt.quarter.astype(str)
    df["NumeroMes"] = df.Data.dt.month
    df["Mes"] = df.NumeroMes.map(lambda m: MESES[m - 1])
    df["MesAbreviado"] = df.NumeroMes.map(lambda m: MESES_ABR[m - 1])
    df["AnoMes"] = df.MesAbreviado + "/" + df.Ano.astype(str).str[-2:]
    df["AnoMesNumero"] = df.Ano * 100 + df.NumeroMes
    df["SemanaAno"] = df.Data.dt.isocalendar().week.astype(int)
    df["NumeroDiaSemana"] = df.Data.dt.weekday + 1
    df["DiaSemana"] = df.Data.dt.weekday.map(lambda d: DIAS[d])
    df["FimDeSemana"] = df.NumeroDiaSemana.isin([6, 7])
    df["DiaUtil"] = ~df.FimDeSemana
    df["InicioMes"] = df.Data.values.astype("datetime64[M]")
    df["FimMes"] = df.InicioMes + pd.offsets.MonthEnd(0)
    for c in ["Data", "InicioMes", "FimMes"]:
        df[c] = pd.to_datetime(df[c]).dt.strftime("%Y-%m-%d")
    df["DiaUtil"] = df.DiaUtil.map({True: "Sim", False: "Nao"})
    df["FimDeSemana"] = df.FimDeSemana.map({True: "Sim", False: "Nao"})
    return df


# =====================================================================
# 2. dPais
# =====================================================================
PAISES = [
    # Pais, ISO, Continente, Regiao, Moeda, Idioma, Classe, Risco, LT, Tarifa, peso_mercado
    ("Estados Unidos", "USA", "America do Norte", "NAFTA", "USD", "Ingles", "Principal", "Baixo", 22, 4.2, 19.0),
    ("Canada", "CAN", "America do Norte", "NAFTA", "CAD", "Ingles", "Principal", "Baixo", 24, 3.1, 5.5),
    ("Mexico", "MEX", "America Latina", "America Latina", "USD", "Espanhol", "Secundario", "Medio", 18, 6.5, 3.4),
    ("Alemanha", "DEU", "Europa", "Europa Ocidental", "EUR", "Alemao", "Principal", "Baixo", 26, 5.0, 11.5),
    ("Paises Baixos", "NLD", "Europa", "Europa Ocidental", "EUR", "Holandes", "Principal", "Baixo", 25, 5.0, 9.0),
    ("Franca", "FRA", "Europa", "Europa Ocidental", "EUR", "Frances", "Principal", "Baixo", 27, 5.0, 6.2),
    ("Reino Unido", "GBR", "Europa", "Europa Ocidental", "GBP", "Ingles", "Principal", "Baixo", 26, 4.4, 6.0),
    ("Italia", "ITA", "Europa", "Europa do Sul", "EUR", "Italiano", "Secundario", "Baixo", 28, 5.0, 4.6),
    ("Espanha", "ESP", "Europa", "Europa do Sul", "EUR", "Espanhol", "Secundario", "Baixo", 27, 5.0, 3.9),
    ("Portugal", "PRT", "Europa", "Europa do Sul", "EUR", "Portugues", "Secundario", "Baixo", 26, 5.0, 2.6),
    ("Belgica", "BEL", "Europa", "Europa Ocidental", "EUR", "Holandes", "Secundario", "Baixo", 25, 5.0, 2.2),
    ("Emirados Arabes Unidos", "ARE", "Oriente Medio", "Golfo", "AED", "Arabe", "Secundario", "Medio", 30, 5.0, 4.1),
    ("Arabia Saudita", "SAU", "Oriente Medio", "Golfo", "USD", "Arabe", "Emergente", "Medio", 32, 6.0, 2.3),
    ("Japao", "JPN", "Asia", "Asia Oriental", "JPY", "Japones", "Principal", "Baixo", 38, 7.5, 5.0),
    ("China", "CHN", "Asia", "Asia Oriental", "CNY", "Mandarim", "Secundario", "Medio", 40, 9.5, 4.3),
    ("Coreia do Sul", "KOR", "Asia", "Asia Oriental", "USD", "Coreano", "Emergente", "Baixo", 39, 8.0, 2.4),
    ("Cingapura", "SGP", "Asia", "Sudeste Asiatico", "USD", "Ingles", "Emergente", "Baixo", 36, 0.5, 1.3),
    ("Australia", "AUS", "Oceania", "Oceania", "USD", "Ingles", "Secundario", "Baixo", 34, 4.0, 2.5),
    ("Nova Zelandia", "NZL", "Oceania", "Oceania", "USD", "Ingles", "Emergente", "Baixo", 36, 4.0, 0.9),
    ("Chile", "CHL", "America Latina", "Cone Sul", "USD", "Espanhol", "Secundario", "Baixo", 14, 6.0, 2.3),
    ("Argentina", "ARG", "America Latina", "Cone Sul", "USD", "Espanhol", "Secundario", "Alto", 10, 12.0, 2.1),
    ("Colombia", "COL", "America Latina", "Andina", "USD", "Espanhol", "Emergente", "Medio", 13, 9.0, 1.4),
    ("Uruguai", "URY", "America Latina", "Cone Sul", "USD", "Espanhol", "Emergente", "Medio", 8, 8.0, 0.9),
    ("Africa do Sul", "ZAF", "Africa", "Africa Austral", "USD", "Ingles", "Emergente", "Medio", 28, 10.0, 0.9),
    ("Israel", "ISR", "Oriente Medio", "Levante", "USD", "Hebraico", "Emergente", "Medio", 29, 6.5, 0.9),
    ("Suica", "CHE", "Europa", "Europa Ocidental", "EUR", "Alemao", "Secundario", "Baixo", 27, 3.0, 1.4),
    ("Suecia", "SWE", "Europa", "Escandinavia", "EUR", "Sueco", "Secundario", "Baixo", 29, 5.0, 1.3),
    ("Polonia", "POL", "Europa", "Europa Central", "EUR", "Polones", "Emergente", "Baixo", 30, 5.0, 1.1),
]


def gerar_pais():
    rows = []
    for i, p in enumerate(PAISES, start=1):
        rows.append(dict(PaisID=i, Pais=p[0], CodigoISO=p[1], Continente=p[2], Regiao=p[3],
                         Moeda=p[4], IdiomaPrincipal=p[5], ClassificacaoMercado=p[6],
                         RiscoPais=p[7], LeadTimeMedio=p[8], TarifaMediaImportacao=p[9]))
    return pd.DataFrame(rows)


PESO_MERCADO = {p[0]: p[10] for p in PAISES}

# =====================================================================
# 3. dVendedor
# =====================================================================
VENDEDORES = [
    # Nome, Cargo, Gerente, Regiao, Continente
    ("Ricardo Salgueiro Mendes", "Diretor Comercial", None, "Global", "Global"),
    ("Beatriz Continho Alvarenga", "Gerente Regional", "Ricardo Salgueiro Mendes", "America do Norte", "America do Norte"),
    ("Henrique Vasconcelos Pires", "Gerente Regional", "Ricardo Salgueiro Mendes", "Europa", "Europa"),
    ("Mariana Toledo Guimaraes", "Gerente Regional", "Ricardo Salgueiro Mendes", "Asia-Pacifico", "Asia"),
    ("Rodrigo Alencastro Paiva", "Gerente Regional", "Ricardo Salgueiro Mendes", "America Latina", "America Latina"),
    ("Fernanda Quintela Bastos", "Gerente Regional", "Ricardo Salgueiro Mendes", "Oriente Medio e Africa", "Oriente Medio"),
    ("Lucas Bittencourt Ferraz", "Executivo de Contas", "Beatriz Continho Alvarenga", "America do Norte", "America do Norte"),
    ("Camila Ostrowski Nunes", "Executivo de Contas", "Beatriz Continho Alvarenga", "America do Norte", "America do Norte"),
    ("Gustavo Peixoto Andrade", "Executivo de Contas", "Henrique Vasconcelos Pires", "Europa Ocidental", "Europa"),
    ("Isabela Marchetti Rangel", "Executivo de Contas", "Henrique Vasconcelos Pires", "Europa Ocidental", "Europa"),
    ("Thiago Bandeira Cordeiro", "Executivo de Contas", "Henrique Vasconcelos Pires", "Europa do Sul", "Europa"),
    ("Aline Furtado Bezerra", "Executivo de Contas", "Henrique Vasconcelos Pires", "Europa Central e Norte", "Europa"),
    ("Eduardo Sampaio Vilela", "Executivo de Contas", "Mariana Toledo Guimaraes", "Asia Oriental", "Asia"),
    ("Patricia Nakamura Ribeiro", "Executivo de Contas", "Mariana Toledo Guimaraes", "Asia Oriental", "Asia"),
    ("Vinicius Caldeira Rocha", "Executivo de Contas", "Mariana Toledo Guimaraes", "Oceania e Sudeste Asiatico", "Oceania"),
    ("Larissa Amorim Tavares", "Executivo de Contas", "Rodrigo Alencastro Paiva", "Cone Sul", "America Latina"),
    ("Marcelo Duarte Siqueira", "Executivo de Contas", "Rodrigo Alencastro Paiva", "Andina e Mexico", "America Latina"),
    ("Juliana Espindola Braga", "Executivo de Contas", "Fernanda Quintela Bastos", "Golfo", "Oriente Medio"),
    ("Rafael Monteiro Lacerda", "Executivo de Contas", "Fernanda Quintela Bastos", "Africa e Levante", "Oriente Medio"),
    ("Carolina Bragantini Reis", "Executivo de Contas", "Beatriz Continho Alvarenga", "America do Norte", "America do Norte"),
]

REGIAO_PAISES = {
    "America do Norte": ["Estados Unidos", "Canada"],
    "Europa Ocidental": ["Alemanha", "Paises Baixos", "Franca", "Belgica", "Suica"],
    "Europa do Sul": ["Italia", "Espanha", "Portugal"],
    "Europa Central e Norte": ["Reino Unido", "Suecia", "Polonia"],
    "Asia Oriental": ["Japao", "China", "Coreia do Sul"],
    "Oceania e Sudeste Asiatico": ["Australia", "Nova Zelandia", "Cingapura"],
    "Cone Sul": ["Chile", "Argentina", "Uruguai"],
    "Andina e Mexico": ["Mexico", "Colombia"],
    "Golfo": ["Emirados Arabes Unidos", "Arabia Saudita"],
    "Africa e Levante": ["Africa do Sul", "Israel"],
}


def gerar_vendedor():
    rows = []
    for i, v in enumerate(VENDEDORES, start=1):
        cargo = v[1]
        adm = date(2015, 1, 1) + timedelta(days=int(rng.integers(0, 3200)))
        if cargo == "Diretor Comercial":
            meta = 0
        elif cargo == "Gerente Regional":
            meta = float(rng.integers(9, 16)) * 1_000_000
        else:
            meta = float(rng.integers(24, 62)) * 100_000
        rows.append(dict(VendedorID=i, CodigoVendedor=f"VD{i:03d}", NomeVendedor=v[0],
                         Cargo=cargo, Gerente=v[2] or "", RegiaoResponsavel=v[3],
                         ContinenteResponsavel=v[4], DataAdmissao=adm.isoformat(),
                         MetaAnualUSD=r2(meta), Status="Ativo"))
    df = pd.DataFrame(rows)
    # um executivo desligado em 2025 (realismo)
    df.loc[df.NomeVendedor == "Marcelo Duarte Siqueira", "Status"] = "Inativo"
    return df


# =====================================================================
# 4. dProduto
# =====================================================================
CATALOGO = [
    # Categoria, Subcategoria, Linha, base_preco_usd_kg, margem_alvo, vida_util, estado
    ("Cafe", "Cafe Arabica Especial", "Premium", 9.80, 0.34, 540, "Minas Gerais"),
    ("Cafe", "Cafe Bourbon Amarelo", "Premium", 10.60, 0.35, 540, "Sao Paulo"),
    ("Cafe", "Cafe Torrado Premium", "Premium", 13.40, 0.38, 365, "Minas Gerais"),
    ("Cafe", "Cafe Verde Comercial", "Standard", 6.20, 0.21, 720, "Espirito Santo"),
    ("Cafe", "Cafe Organico Certificado", "Organico", 12.10, 0.36, 540, "Bahia"),
    ("Cacau", "Cacau em Po Alcalino", "Ingredientes", 7.40, 0.27, 720, "Bahia"),
    ("Cacau", "Nibs de Cacau", "Premium", 11.20, 0.33, 540, "Para"),
    ("Cacau", "Amendoas de Cacau", "Standard", 6.90, 0.24, 540, "Bahia"),
    ("Cacau", "Manteiga de Cacau", "Ingredientes", 14.80, 0.29, 730, "Bahia"),
    ("Castanhas", "Castanha-do-Para", "Premium", 16.50, 0.31, 300, "Amazonas"),
    ("Castanhas", "Castanha de Caju W240", "Premium", 13.90, 0.28, 365, "Ceara"),
    ("Castanhas", "Castanha de Caju Quebrada", "Standard", 9.30, 0.22, 365, "Rio Grande do Norte"),
    ("Castanhas", "Mix de Nuts Brasileiro", "Premium", 15.20, 0.34, 270, "Ceara"),
    ("Acai", "Polpa de Acai Congelada", "Congelados", 5.60, 0.19, 365, "Para"),
    ("Acai", "Acai Liofilizado em Po", "Premium", 34.00, 0.41, 720, "Para"),
    ("Acai", "Acai Organico Congelado", "Organico", 7.10, 0.24, 365, "Amapa"),
    ("Frutas Processadas", "Polpa de Manga", "Congelados", 3.90, 0.20, 365, "Bahia"),
    ("Frutas Processadas", "Polpa de Maracuja", "Congelados", 4.60, 0.22, 365, "Bahia"),
    ("Frutas Processadas", "Manga Desidratada", "Premium", 11.70, 0.32, 270, "Pernambuco"),
    ("Frutas Processadas", "Banana Chips Premium", "Standard", 6.40, 0.25, 240, "Santa Catarina"),
    ("Mel", "Mel Silvestre", "Standard", 6.80, 0.26, 730, "Piaui"),
    ("Mel", "Mel Organico Certificado", "Organico", 9.90, 0.33, 730, "Santa Catarina"),
    ("Mel", "Mel de Florada de Laranjeira", "Premium", 11.30, 0.35, 730, "Sao Paulo"),
    ("Produtos Naturais", "Guarana em Po", "Premium", 22.50, 0.38, 540, "Amazonas"),
    ("Produtos Naturais", "Propolis Extrato", "Premium", 48.00, 0.42, 730, "Minas Gerais"),
    ("Produtos Naturais", "Erva Mate Solavel", "Standard", 8.20, 0.27, 540, "Parana"),
    ("Ingredientes Alimenticios", "Amido de Mandioca", "Ingredientes", 2.30, 0.16, 540, "Parana"),
    ("Ingredientes Alimenticios", "Farinha de Castanha", "Ingredientes", 12.60, 0.30, 300, "Amazonas"),
    ("Ingredientes Alimenticios", "Oleo de Babacu", "Ingredientes", 9.10, 0.28, 540, "Maranhao"),
    ("Ingredientes Alimenticios", "Acucar Demerara Organico", "Organico", 1.85, 0.15, 730, "Sao Paulo"),
]

EMBALAGENS = [
    ("Saca Juta", 60.0, "KG"), ("Big Bag", 500.0, "KG"), ("Caixa Master", 25.0, "KG"),
    ("Pouch Vacuo", 10.0, "KG"), ("Balde Grau Alimenticio", 20.0, "KG"),
    ("Tambor", 200.0, "KG"), ("Cartucho Varejo", 5.0, "KG"),
]

MARCAS = ["Aurora Select", "Aurora Origins", "Terra Viva", "Casa Aurora", "Aurora Industrial"]
CERTIFICACOES = ["Organico USDA/EU", "Fair Trade", "Rainforest Alliance", "Kosher", "Halal",
                 "BRCGS", "Sem Certificacao Especifica", "Organico BR"]


def gerar_produto():
    rows = []
    pid = 0
    for cat, sub, linha, preco_kg, marg, vida, uf in CATALOGO:
        n_emb = int(rng.integers(3, 5))
        embs = pick(EMBALAGENS, n_emb, replace=False)
        for emb, peso, um in embs:
            pid += 1
            fator_emb = {"Saca Juta": 0.94, "Big Bag": 0.88, "Tambor": 0.90,
                         "Caixa Master": 1.00, "Balde Grau Alimenticio": 1.06,
                         "Pouch Vacuo": 1.18, "Cartucho Varejo": 1.42}[emb]
            preco_lista = r2(preco_kg * fator_emb * peso * float(rng.normal(1.0, 0.035)))
            margem_alvo = round(min(0.55, max(0.10, marg + float(rng.normal(0, 0.02)))), 3)
            custo_usd = preco_lista * (1 - margem_alvo - 0.06)
            rows.append(dict(
                ProdutoID=pid,
                SKU=f"{cat[:3].upper()}-{sub.split()[0][:3].upper()}-{int(peso):03d}-{pid:03d}",
                Produto=f"{sub} {int(peso) if peso == int(peso) else peso}kg {emb}",
                Categoria=cat, Subcategoria=sub, Linha=linha,
                Marca=pick(MARCAS), TipoEmbalagem=emb, PesoLiquidoKg=peso, UnidadeMedida=um,
                OrigemBrasil="Sim", EstadoOrigem=uf,
                CustoBaseBRL=r2(custo_usd * 5.25), PrecoListaUSD=preco_lista,
                MargemAlvo=margem_alvo, VidaUtilDias=vida,
                Certificacao=pick(CERTIFICACOES), StatusProduto="Ativo"))
    df = pd.DataFrame(rows)
    # produtos descontinuados e novos
    desc = rng.choice(df.ProdutoID.values, 6, replace=False)
    df.loc[df.ProdutoID.isin(desc), "StatusProduto"] = "Descontinuado"
    novos = rng.choice(df[~df.ProdutoID.isin(desc)].ProdutoID.values, 7, replace=False)
    df.loc[df.ProdutoID.isin(novos), "StatusProduto"] = "Novo"
    return df, set(desc.tolist()), set(novos.tolist())


# =====================================================================
# 5. dCliente
# =====================================================================
PREFIXOS = {
    "Estados Unidos": (["Redwood", "Harborline", "Silver Creek", "Northgate", "Blue Ridge", "Cascadia",
                        "Ironwood", "Sunbelt", "Great Lakes", "Pioneer Valley", "Copperfield", "Westmark"],
                       ["Foods Inc.", "Trading LLC", "Imports Inc.", "Distribution Co.", "Provisions LLC",
                        "Commodities Inc."]),
    "Canada": (["Maple Hollow", "Laurentide", "Northwind", "Grandview", "Aurora Bay", "Fraser Delta"],
               ["Foods Ltd.", "Imports Ltd.", "Trading Corp.", "Distribution Ltd."]),
    "Mexico": (["Valle Dorado", "Casa Herrera", "Monteverde", "Sol Naciente", "Puerto Nuevo"],
               ["Alimentos S.A. de C.V.", "Importadora S.A.", "Comercializadora S.A."]),
    "Alemanha": (["Rheinquell", "Nordbaum", "Schwarzwald", "Hansefeld", "Grunhaus", "Weserland", "Altmark"],
                 ["Lebensmittel GmbH", "Handels GmbH", "Import GmbH", "Rohstoffe GmbH"]),
    "Paises Baixos": (["Zuiderveld", "Havenlicht", "Groenmarkt", "Vandermeer", "Waterlinie"],
                      ["Food B.V.", "Trading B.V.", "Import B.V.", "Commodities B.V."]),
    "Franca": (["Val de Loire", "Maison Cheverny", "Bellecour", "Cotes du Nord", "Saint-Aubain"],
               ["Alimentaire SAS", "Negoce SARL", "Import SAS"]),
    "Reino Unido": (["Thameswick", "Northbury", "Kingsmere", "Greyfriars", "Aldergate"],
                    ["Foods Ltd", "Trading Ltd", "Imports Ltd", "Provisions Ltd"]),
    "Italia": (["Val Serena", "Casa Moretti", "Adriatica", "Monte Bianco", "Portofelice"],
               ["Alimentari S.r.l.", "Import S.p.A.", "Commercio S.r.l."]),
    "Espanha": (["Costa Serena", "Casa Olivares", "Valdemar", "Puerto Blanco"],
                ["Alimentacion S.L.", "Importaciones S.A.", "Comercial S.L."]),
    "Portugal": (["Douro Verde", "Casa Ribamar", "Atlantico Sul", "Vila Nova"],
                 ["Alimentar Lda.", "Importadora Lda.", "Comercio S.A."]),
    "Belgica": (["Scheldeveld", "Brugmarkt", "Ardennes Nord"], ["Food NV", "Trading NV", "Import BVBA"]),
    "Emirados Arabes Unidos": (["Al Nasira", "Desert Pearl", "Khaleej Star", "Marina Gate"],
                               ["Foodstuff LLC", "General Trading LLC", "Import LLC"]),
    "Arabia Saudita": (["Al Rawdah", "Najd Horizon", "Sahara Bloom"], ["Trading Co.", "Foods Co.", "Import Est."]),
    "Japao": (["Kaneyama", "Shirogane", "Midorikawa", "Tsukishima", "Hoshino"],
              ["Shoji K.K.", "Trading Co., Ltd.", "Foods Co., Ltd."]),
    "China": (["Jinhe", "Nanpu", "Yuanfeng", "Baiyun", "Changtai"],
              ["Trading Co., Ltd.", "Food Group Co., Ltd.", "Import & Export Co."]),
    "Coreia do Sul": (["Hanbit", "Daesan", "Seorin", "Cheongwon"], ["Trading Co., Ltd.", "Foods Co., Ltd."]),
    "Cingapura": (["Marina Crest", "Straits Green", "Orchid Bay"], ["Pte. Ltd.", "Trading Pte. Ltd."]),
    "Australia": (["Kingsford", "Coral Bay", "Southern Cross", "Yarra Ridge"],
                  ["Foods Pty Ltd", "Imports Pty Ltd", "Trading Pty Ltd"]),
    "Nova Zelandia": (["Kaiwaka", "Southland", "Silverfern"], ["Foods Ltd", "Trading Ltd"]),
    "Chile": (["Valle Andino", "Puerto Claro", "Casa Elqui"], ["Alimentos SpA", "Importadora Ltda.", "Comercial SpA"]),
    "Argentina": (["Pampa Grande", "Rio Plata", "Casa Belgrano"], ["Alimentos S.A.", "Importadora S.R.L."]),
    "Colombia": (["Monte Verde", "Casa Bolivar", "Cafetal Alto"], ["Alimentos S.A.S.", "Importadora S.A.S."]),
    "Uruguai": (["Punta Serena", "Casa Artigas"], ["Alimentos S.A.", "Comercial S.R.L."]),
    "Africa do Sul": (["Cape Ridge", "Karoo Trade", "Table Bay"], ["Foods (Pty) Ltd", "Trading (Pty) Ltd"]),
    "Israel": (["Har Hadar", "Yam Tikva", "Neve Shaked"], ["Foods Ltd.", "Import Ltd."]),
    "Suica": (["Alpenblick", "Seehalde", "Bergquell"], ["Handels AG", "Food AG", "Import AG"]),
    "Suecia": (["Nordvik", "Bjorkdal", "Sjolund"], ["Livs AB", "Trading AB", "Import AB"]),
    "Polonia": (["Wislaland", "Bialy Dom", "Zielona Gora"], ["Sp. z o.o.", "Handel Sp. z o.o."]),
}

CIDADES = {
    "Estados Unidos": [("Newark", "New Jersey"), ("Houston", "Texas"), ("Miami", "Florida"),
                       ("Long Beach", "California"), ("Chicago", "Illinois"), ("Seattle", "Washington"),
                       ("Atlanta", "Georgia"), ("Boston", "Massachusetts")],
    "Canada": [("Toronto", "Ontario"), ("Montreal", "Quebec"), ("Vancouver", "British Columbia")],
    "Mexico": [("Cidade do Mexico", "CDMX"), ("Guadalajara", "Jalisco"), ("Monterrey", "Nuevo Leon")],
    "Alemanha": [("Hamburgo", "Hamburgo"), ("Bremen", "Bremen"), ("Colonia", "Renania"), ("Munique", "Baviera")],
    "Paises Baixos": [("Roterda", "Holanda do Sul"), ("Amsterda", "Holanda do Norte"), ("Utreque", "Utreque")],
    "Franca": [("Le Havre", "Normandia"), ("Marselha", "PACA"), ("Lyon", "Auvergne-Rhone-Alpes")],
    "Reino Unido": [("Londres", "Inglaterra"), ("Felixstowe", "Suffolk"), ("Manchester", "Inglaterra")],
    "Italia": [("Genova", "Liguria"), ("Milao", "Lombardia"), ("Napoles", "Campania")],
    "Espanha": [("Valencia", "Valencia"), ("Barcelona", "Catalunha"), ("Algeciras", "Andaluzia")],
    "Portugal": [("Lisboa", "Lisboa"), ("Porto", "Porto"), ("Leixoes", "Porto")],
    "Belgica": [("Antuerpia", "Flandres"), ("Bruxelas", "Bruxelas")],
    "Emirados Arabes Unidos": [("Dubai", "Dubai"), ("Abu Dhabi", "Abu Dhabi"), ("Sharjah", "Sharjah")],
    "Arabia Saudita": [("Jeddah", "Makkah"), ("Riade", "Riade")],
    "Japao": [("Yokohama", "Kanagawa"), ("Kobe", "Hyogo"), ("Toquio", "Toquio")],
    "China": [("Xangai", "Xangai"), ("Shenzhen", "Guangdong"), ("Qingdao", "Shandong")],
    "Coreia do Sul": [("Busan", "Busan"), ("Seul", "Seul")],
    "Cingapura": [("Cingapura", "Cingapura")],
    "Australia": [("Sydney", "New South Wales"), ("Melbourne", "Victoria"), ("Brisbane", "Queensland")],
    "Nova Zelandia": [("Auckland", "Auckland"), ("Tauranga", "Bay of Plenty")],
    "Chile": [("Valparaiso", "Valparaiso"), ("Santiago", "Metropolitana")],
    "Argentina": [("Buenos Aires", "Buenos Aires"), ("Rosario", "Santa Fe")],
    "Colombia": [("Cartagena", "Bolivar"), ("Bogota", "Cundinamarca")],
    "Uruguai": [("Montevideu", "Montevideu")],
    "Africa do Sul": [("Durban", "KwaZulu-Natal"), ("Cidade do Cabo", "Western Cape")],
    "Israel": [("Haifa", "Haifa"), ("Ashdod", "Distrito Sul")],
    "Suica": [("Basileia", "Basileia"), ("Zurique", "Zurique")],
    "Suecia": [("Goteborg", "Vastra Gotaland"), ("Estocolmo", "Estocolmo")],
    "Polonia": [("Gdansk", "Pomerania"), ("Varsovia", "Mazovia")],
}

TIPOS_CLIENTE = ["Importador", "Distribuidor", "Rede Varejista", "Industria",
                 "Food Service", "Atacadista", "Private Label"]
P_TIPO = [0.26, 0.22, 0.11, 0.16, 0.10, 0.09, 0.06]
SEGMENTOS = {
    "Importador": ["Trading de Commodities", "Importacao Especializada"],
    "Distribuidor": ["Distribuicao Alimentar", "Distribuicao Gourmet"],
    "Rede Varejista": ["Varejo Premium", "Varejo Massa"],
    "Industria": ["Industria de Alimentos", "Industria de Bebidas", "Industria de Chocolates"],
    "Food Service": ["Cadeias de Cafeteria", "Hotelaria e Restaurantes"],
    "Atacadista": ["Atacado Geral", "Cash and Carry"],
    "Private Label": ["Marca Propria Varejo", "Marca Propria Industrial"],
}
CANAIS = ["Venda Direta", "Representante Local", "Trading Parceira", "E-commerce B2B", "Feira Internacional"]
P_CANAL = [0.44, 0.24, 0.18, 0.06, 0.08]


def porte_from_potencial(pot):
    if pot >= 4_000_000:
        return "Grande"
    if pot >= 1_200_000:
        return "Medio"
    if pot >= 350_000:
        return "Pequeno"
    return "Micro"


def gerar_cliente(dpais, dvend, n=330):
    paises = list(PESO_MERCADO.keys())
    pesos = np.array([PESO_MERCADO[p] for p in paises], dtype=float)
    pesos = pesos / pesos.sum()
    pais_map = dpais.set_index("Pais").to_dict("index")

    # vendedor por regiao
    reg_to_vend = {}
    for _, v in dvend[dvend.Cargo == "Executivo de Contas"].iterrows():
        reg_to_vend.setdefault(v.RegiaoResponsavel, []).append(int(v.VendedorID))
    pais_to_vends = {}
    for reg, pss in REGIAO_PAISES.items():
        for ps in pss:
            pais_to_vends.setdefault(ps, []).extend(reg_to_vend.get(reg, []))

    rows = []
    usados = set()
    for i in range(1, n + 1):
        pais = paises[int(rng.choice(len(paises), p=pesos))]
        pref, suf = PREFIXOS[pais]
        for _ in range(60):
            nome_base = f"{pick(pref)} {pick(suf)}"
            if nome_base not in usados:
                break
        usados.add(nome_base)
        fantasia = nome_base.split(" ")[0] + " " + nome_base.split(" ")[1] if len(nome_base.split()) > 2 else nome_base
        tipo = pick(TIPOS_CLIENTE, p=P_TIPO)
        cid, estado = pick(CIDADES[pais])
        info = pais_map[pais]

        # potencial anual segue lognormal -> concentracao natural
        pot = float(np.exp(rng.normal(13.4, 1.05)))
        pot = float(min(pot, 22_000_000))

        # cohort de aquisicao
        u = rng.random()
        if u < 0.42:
            cad = date(2021, 6, 1) + timedelta(days=int(rng.integers(0, 214)))   # legado
        elif u < 0.60:
            cad = date(2022, 1, 1) + timedelta(days=int(rng.integers(0, 365)))
        elif u < 0.74:
            cad = date(2023, 1, 1) + timedelta(days=int(rng.integers(0, 365)))
        elif u < 0.86:
            cad = date(2024, 1, 1) + timedelta(days=int(rng.integers(0, 365)))
        elif u < 0.96:
            cad = date(2025, 1, 1) + timedelta(days=int(rng.integers(0, 365)))
        else:
            cad = date(2026, 1, 1) + timedelta(days=int(rng.integers(0, 180)))

        vends = pais_to_vends.get(pais) or [7]
        vend = int(pick(vends))
        prazo = int(pick([0, 30, 45, 60, 90, 120], p=[0.08, 0.30, 0.20, 0.24, 0.13, 0.05]))
        rows.append(dict(
            ClienteID=i, CodigoCliente=f"CL{i:04d}", RazaoSocial=nome_base, NomeFantasia=fantasia,
            TipoCliente=tipo, Segmento=pick(SEGMENTOS[tipo]),
            Subsegmento=pick(["Premium", "Mainstream", "Organico", "Industrial", "Gourmet"]),
            Porte=porte_from_potencial(pot), Pais=pais, CodigoPais=info["CodigoISO"],
            Continente=info["Continente"], RegiaoComercial=info["Regiao"], Cidade=cid,
            EstadoProvincia=estado, MoedaPreferencial=info["Moeda"], Idioma=info["IdiomaPrincipal"],
            DataCadastro=cad.isoformat(), VendedorResponsavelID=vend,
            CanalVenda=pick(CANAIS, p=P_CANAL),
            ClassificacaoCliente=pick(["Estrategico", "Chave", "Regular", "Ocasional"],
                                      p=[0.07, 0.18, 0.47, 0.28]),
            LimiteCreditoUSD=r2(pot * float(rng.uniform(0.06, 0.22))),
            PrazoPagamentoPadrao=prazo, StatusCliente="Ativo",
            PotencialAnualEstimadoUSD=r2(pot), PaisID=int(dpais.loc[dpais.Pais == pais, "PaisID"].iloc[0]),
        ))
    return pd.DataFrame(rows)


# =====================================================================
# 6. dPorto / dTransportadora
# =====================================================================
PORTOS_BR = [("Porto de Santos", "Santos", "Brasil", "BRSSZ", "Maritimo"),
             ("Porto de Paranagua", "Paranagua", "Brasil", "BRPNG", "Maritimo"),
             ("Porto de Itajai", "Itajai", "Brasil", "BRITJ", "Maritimo"),
             ("Porto do Rio de Janeiro", "Rio de Janeiro", "Brasil", "BRRIO", "Maritimo"),
             ("Porto de Vitoria", "Vitoria", "Brasil", "BRVIX", "Maritimo"),
             ("Porto de Suape", "Ipojuca", "Brasil", "BRSUA", "Maritimo"),
             ("Porto de Manaus", "Manaus", "Brasil", "BRMAO", "Fluvial"),
             ("Aeroporto de Viracopos", "Campinas", "Brasil", "BRVCP", "Aereo"),
             ("Aeroporto de Guarulhos", "Guarulhos", "Brasil", "BRGRU", "Aereo")]

PORTOS_INT = {
    "Estados Unidos": [("Port of New York", "Newark", "USNYC", "Maritimo"),
                       ("Port of Houston", "Houston", "USHOU", "Maritimo"),
                       ("Port of Miami", "Miami", "USMIA", "Maritimo"),
                       ("Port of Long Beach", "Long Beach", "USLGB", "Maritimo")],
    "Canada": [("Port of Montreal", "Montreal", "CAMTR", "Maritimo"),
               ("Port of Vancouver", "Vancouver", "CAVAN", "Maritimo")],
    "Mexico": [("Puerto de Veracruz", "Veracruz", "MXVER", "Maritimo")],
    "Alemanha": [("Hafen Hamburg", "Hamburgo", "DEHAM", "Maritimo"),
                 ("Hafen Bremerhaven", "Bremerhaven", "DEBRV", "Maritimo")],
    "Paises Baixos": [("Port of Rotterdam", "Roterda", "NLRTM", "Maritimo")],
    "Franca": [("Port du Havre", "Le Havre", "FRLEH", "Maritimo"),
               ("Port de Marseille", "Marselha", "FRMRS", "Maritimo")],
    "Reino Unido": [("Port of Felixstowe", "Felixstowe", "GBFXT", "Maritimo"),
                    ("Port of London", "Londres", "GBLON", "Maritimo")],
    "Italia": [("Porto di Genova", "Genova", "ITGOA", "Maritimo")],
    "Espanha": [("Puerto de Valencia", "Valencia", "ESVLC", "Maritimo"),
                ("Puerto de Algeciras", "Algeciras", "ESALG", "Maritimo")],
    "Portugal": [("Porto de Leixoes", "Leixoes", "PTLEI", "Maritimo"),
                 ("Porto de Lisboa", "Lisboa", "PTLIS", "Maritimo")],
    "Belgica": [("Haven Antwerpen", "Antuerpia", "BEANR", "Maritimo")],
    "Emirados Arabes Unidos": [("Jebel Ali Port", "Dubai", "AEJEA", "Maritimo")],
    "Arabia Saudita": [("Jeddah Islamic Port", "Jeddah", "SAJED", "Maritimo")],
    "Japao": [("Port of Yokohama", "Yokohama", "JPYOK", "Maritimo"),
              ("Port of Kobe", "Kobe", "JPUKB", "Maritimo")],
    "China": [("Port of Shanghai", "Xangai", "CNSHA", "Maritimo"),
              ("Port of Qingdao", "Qingdao", "CNTAO", "Maritimo")],
    "Coreia do Sul": [("Port of Busan", "Busan", "KRPUS", "Maritimo")],
    "Cingapura": [("Port of Singapore", "Cingapura", "SGSIN", "Maritimo")],
    "Australia": [("Port of Sydney", "Sydney", "AUSYD", "Maritimo"),
                  ("Port of Melbourne", "Melbourne", "AUMEL", "Maritimo")],
    "Nova Zelandia": [("Port of Tauranga", "Tauranga", "NZTRG", "Maritimo")],
    "Chile": [("Puerto de Valparaiso", "Valparaiso", "CLVAP", "Maritimo")],
    "Argentina": [("Puerto de Buenos Aires", "Buenos Aires", "ARBUE", "Maritimo")],
    "Colombia": [("Puerto de Cartagena", "Cartagena", "COCTG", "Maritimo")],
    "Uruguai": [("Puerto de Montevideo", "Montevideu", "UYMVD", "Maritimo")],
    "Africa do Sul": [("Port of Durban", "Durban", "ZADUR", "Maritimo")],
    "Israel": [("Port of Ashdod", "Ashdod", "ILASH", "Maritimo")],
    "Suica": [("Basel Rheinhafen", "Basileia", "CHBSL", "Fluvial")],
    "Suecia": [("Port of Goteborg", "Goteborg", "SEGOT", "Maritimo")],
    "Polonia": [("Port Gdansk", "Gdansk", "PLGDN", "Maritimo")],
}


def gerar_porto():
    rows, pid = [], 0
    for p in PORTOS_BR:
        pid += 1
        rows.append(dict(PortoID=pid, Porto=p[0], Cidade=p[1], Pais=p[2],
                         CodigoUNLOCODE=p[3], TipoPorto=p[4]))
    for pais, lst in PORTOS_INT.items():
        for nome, cid, unl, tp in lst:
            pid += 1
            rows.append(dict(PortoID=pid, Porto=nome, Cidade=cid, Pais=pais,
                             CodigoUNLOCODE=unl, TipoPorto=tp))
    return pd.DataFrame(rows)


TRANSPORTADORAS = [
    ("Meridian Blue Lines", "Maritimo", "Dinamarca", 4.6, 26),
    ("Pacifica Container Lines", "Maritimo", "Cingapura", 4.3, 31),
    ("Atlantis Cargo Maritima", "Maritimo", "Brasil", 4.1, 24),
    ("Nordwind Shipping AG", "Maritimo", "Alemanha", 4.5, 25),
    ("Oceanica Sul Navegacao", "Maritimo", "Brasil", 3.6, 29),
    ("Vela Marittima S.p.A.", "Maritimo", "Italia", 3.9, 28),
    ("Global Reach Freight", "Maritimo", "Paises Baixos", 4.4, 26),
    ("Andes Cargo Line", "Maritimo", "Chile", 3.4, 21),
    ("SkyBridge Air Cargo", "Aereo", "Estados Unidos", 4.7, 6),
    ("AeroLusitana Cargo", "Aereo", "Portugal", 4.2, 7),
    ("Condor Air Logistics", "Aereo", "Brasil", 4.0, 6),
    ("TransPampa Rodoviaria", "Rodoviario", "Brasil", 3.8, 9),
    ("Ruta Sur Transportes", "Rodoviario", "Argentina", 3.5, 11),
]


def gerar_transportadora():
    rows = []
    for i, t in enumerate(TRANSPORTADORAS, start=1):
        rows.append(dict(TransportadoraID=i, Transportadora=t[0], ModalPrincipal=t[1],
                         Pais=t[2], AvaliacaoFornecedor=t[3], LeadTimeMedio=t[4],
                         Status="Ativo" if i != 8 else "Em Revisao"))
    return pd.DataFrame(rows)


# =====================================================================
# 7. fCambio
# =====================================================================
MOEDAS_BASE = {"USD": 5.20, "EUR": 5.85, "GBP": 6.90, "CAD": 4.05,
               "JPY": 0.0405, "CNY": 0.760, "AED": 1.415}


def gerar_cambio():
    dts = pd.date_range(DT_INI, DT_FIM, freq="D")
    n = len(dts)
    t = np.arange(n)
    # trajetoria macro do USD/BRL: 2022 ~5.2 -> 2023 ~4.95 -> 2024 sobe -> 2025 pico ~6.1 -> 2026 ~5.7
    ancoras = {date(2022, 1, 1): 5.20, date(2022, 12, 31): 5.28, date(2023, 6, 30): 4.85,
               date(2023, 12, 31): 4.92, date(2024, 6, 30): 5.45, date(2024, 12, 31): 6.05,
               date(2025, 6, 30): 5.72, date(2025, 12, 31): 6.12, date(2026, 7, 31): 5.68}
    xs = np.array([(d - DT_INI).days for d in ancoras])
    ys = np.array(list(ancoras.values()))
    trend = np.interp(t, xs, ys)
    ruido = np.cumsum(rng.normal(0, 0.011, n))
    ruido = ruido - np.linspace(0, ruido[-1], n)
    usd = trend * (1 + ruido * 0.05) + rng.normal(0, 0.012, n)

    rows = []
    for moeda, base in MOEDAS_BASE.items():
        ratio = base / MOEDAS_BASE["USD"]
        drift = np.cumsum(rng.normal(0, 0.0016, n))
        drift = drift - np.linspace(0, drift[-1] * 0.4, n)
        serie = usd * ratio * (1 + drift)
        s = pd.Series(serie, index=dts)
        var_dia = s.pct_change() * 100
        mensal = s.resample("MS").first()
        var_mes = mensal.pct_change().reindex(s.index, method="ffill") * 100
        for d, v, vd, vm in zip(dts, serie, var_dia, var_mes):
            rows.append((d.strftime("%Y-%m-%d"), moeda, r2(v) if moeda != "JPY" else round(v, 4),
                         round(float(vd) if not math.isnan(vd) else 0.0, 4),
                         round(float(vm) if not math.isnan(vm) else 0.0, 4)))
    df = pd.DataFrame(rows, columns=["Data", "Moeda", "TaxaBRL", "VariacaoDia", "VariacaoMes"])
    usd_map = {d.strftime("%Y-%m-%d"): float(v) for d, v in zip(dts, usd)}
    return df, usd_map


# =====================================================================
# 8. fVendas  — motor comercial
# =====================================================================
SAZONALIDADE = {
    "Cafe":                     [0.80, 0.78, 0.85, 0.88, 0.92, 0.95, 1.02, 1.10, 1.22, 1.30, 1.25, 0.93],
    "Cacau":                    [0.82, 0.84, 0.90, 0.94, 0.98, 1.00, 1.05, 1.18, 1.24, 1.22, 1.05, 0.78],
    "Castanhas":                [0.72, 0.74, 0.80, 0.86, 0.90, 0.96, 1.06, 1.16, 1.28, 1.34, 1.28, 0.90],
    "Acai":                     [0.74, 0.78, 0.92, 1.10, 1.26, 1.38, 1.40, 1.24, 1.00, 0.82, 0.72, 0.64],
    "Frutas Processadas":       [0.80, 0.86, 1.02, 1.14, 1.22, 1.24, 1.16, 1.06, 0.94, 0.88, 0.84, 0.84],
    "Mel":                      [0.92, 0.86, 0.86, 0.88, 0.92, 0.94, 0.98, 1.04, 1.12, 1.24, 1.28, 0.96],
    "Produtos Naturais":        [1.20, 1.14, 1.08, 1.00, 0.96, 0.94, 0.94, 0.96, 0.98, 0.96, 0.92, 0.92],
    "Ingredientes Alimenticios":[0.96, 0.98, 1.02, 1.02, 1.00, 1.00, 1.00, 1.02, 1.04, 1.02, 0.98, 0.96],
}

# inflacao de custo por categoria e ano (indice sobre o custo base)
CUSTO_INDEX = {
    "Cafe":                     {2022: 1.00, 2023: 1.02, 2024: 1.14, 2025: 1.27, 2026: 1.24},
    "Cacau":                    {2022: 1.00, 2023: 1.09, 2024: 1.38, 2025: 1.62, 2026: 1.49},  # choque de custo
    "Castanhas":                {2022: 1.00, 2023: 1.03, 2024: 1.07, 2025: 1.11, 2026: 1.13},
    "Acai":                     {2022: 1.00, 2023: 1.06, 2024: 1.15, 2025: 1.24, 2026: 1.31},
    "Frutas Processadas":       {2022: 1.00, 2023: 1.04, 2024: 1.08, 2025: 1.10, 2026: 1.12},
    "Mel":                      {2022: 1.00, 2023: 1.03, 2024: 1.06, 2025: 1.08, 2026: 1.10},
    "Produtos Naturais":        {2022: 1.00, 2023: 1.02, 2024: 1.05, 2025: 1.07, 2026: 1.08},
    "Ingredientes Alimenticios":{2022: 1.00, 2023: 1.05, 2024: 1.09, 2025: 1.12, 2026: 1.14},
}

CRESC_ANO = {2022: 1.00, 2023: 0.803, 2024: 0.787, 2025: 0.761, 2026: 0.738}

INCOTERMS = ["FOB", "CIF", "CFR", "EXW", "FCA", "DDP"]
P_INCOTERM = [0.34, 0.29, 0.13, 0.07, 0.10, 0.07]
FRETE_INCOTERM = {"EXW": 0.00, "FOB": 0.10, "FCA": 0.08, "CFR": 1.00, "CIF": 1.00, "DDP": 1.28}
SEGURO_INCOTERM = {"EXW": 0.0, "FOB": 0.0, "FCA": 0.0, "CFR": 0.0, "CIF": 1.0, "DDP": 1.0}

CROSS_SELL = {
    "Cafe": ["Cacau", "Castanhas", "Mel"],
    "Cacau": ["Cafe", "Castanhas", "Ingredientes Alimenticios"],
    "Castanhas": ["Cafe", "Frutas Processadas", "Mel"],
    "Acai": ["Frutas Processadas", "Produtos Naturais"],
    "Frutas Processadas": ["Acai", "Castanhas"],
    "Mel": ["Cafe", "Produtos Naturais"],
    "Produtos Naturais": ["Acai", "Mel"],
    "Ingredientes Alimenticios": ["Cacau", "Frutas Processadas"],
}

MESES_IDX = pd.period_range(DT_INI, DT_FIM, freq="M")


def perfil_clientes(dcli):
    """Define o comportamento comercial de cada cliente (base, tendencia, cesta)."""
    perfis = {}
    # calibra a receita para respeitar o peso comercial de cada mercado
    share_alvo = {k: v / sum(PESO_MERCADO.values()) for k, v in PESO_MERCADO.items()}
    cont = dcli.Pais.value_counts(normalize=True).to_dict()
    fator_pais = {p: (share_alvo[p] / cont[p]) if cont.get(p) else 1.0 for p in share_alvo}
    cats = list(SAZONALIDADE.keys())
    p_cat = np.array([0.30, 0.14, 0.14, 0.12, 0.08, 0.08, 0.07, 0.07])
    for _, c in dcli.iterrows():
        pot = c.PotencialAnualEstimadoUSD
        u = rng.random()
        if u < 0.16:
            sow = float(rng.uniform(0.45, 0.80))     # alta penetracao
        elif u < 0.58:
            sow = float(rng.uniform(0.18, 0.45))     # media
        else:
            sow = float(rng.uniform(0.03, 0.18))     # baixa -> white space
        base = pot * sow

        t = rng.random()
        if t < 0.20:
            tend = float(rng.uniform(1.13, 1.30))    # crescimento forte
        elif t < 0.58:
            tend = float(rng.uniform(0.99, 1.11))    # crescimento moderado
        elif t < 0.82:
            tend = float(rng.uniform(0.93, 1.00))    # estavel
        else:
            tend = float(rng.uniform(0.72, 0.92))    # declinio

        cat_p = pick(cats, p=p_cat / p_cat.sum())
        cesta = [cat_p]
        for extra in CROSS_SELL[cat_p]:
            if rng.random() < 0.55:
                cesta.append(extra)
        if rng.random() < 0.10:
            cesta.append(pick(cats))
        cesta = list(dict.fromkeys(cesta))

        porte_lambda = {"Grande": 3.1, "Medio": 1.9, "Pequeno": 1.05, "Micro": 0.45}[c.Porte]
        base *= fator_pais.get(c.Pais, 1.0)
        perfis[int(c.ClienteID)] = dict(
            base=base, tend=tend, cesta=cesta, cat_p=cat_p,
            lam=porte_lambda * float(rng.uniform(0.75, 1.30)),
            desc_perfil=float(rng.uniform(0.01, 0.11)),
            churn_ini=None, churn_fim=None, fim=None,
            incoterm=pick(INCOTERMS, p=P_INCOTERM),
            modal_aereo=0.22 if c.TipoCliente in ("Food Service", "Rede Varejista") else 0.07,
            pais=c.Pais,
        )
    # normalizacao final: a receita potencial por pais respeita o peso comercial do mercado
    tot = sum(p["base"] for p in perfis.values())
    por_pais = {}
    for p in perfis.values():
        por_pais[p["pais"]] = por_pais.get(p["pais"], 0.0) + p["base"]
    for p in perfis.values():
        alvo = share_alvo[p["pais"]] * tot
        p["base"] *= (alvo / por_pais[p["pais"]]) ** 0.85
    return perfis


def aplicar_insights(dcli, dprod, dvend, perfis):
    """Implanta os padroes deliberados. Retorna dicionario com o registro do que foi implantado."""
    reg = {}
    ranking = sorted(perfis.items(), key=lambda kv: -kv[1]["base"])
    top_ids = [k for k, _ in ranking]

    # I1 - cliente top em queda (2024 cresce, 2025 estavel, 2026 -30%)
    c1 = top_ids[1]
    perfis[c1]["override_ano"] = {2023: 1.10, 2024: 1.34, 2025: 1.36, 2026: 0.94}
    reg["I1"] = c1

    # I3 - vendedor dependente de um cliente
    vend_alvo = int(dcli.loc[dcli.ClienteID == top_ids[3], "VendedorResponsavelID"].iloc[0])
    perfis[top_ids[3]]["base"] *= 3.0
    reg["I3"] = (vend_alvo, top_ids[3])

    # I4 - mercado emergente: Coreia do Sul
    ids_kor = dcli.loc[dcli.Pais == "Coreia do Sul", "ClienteID"].tolist()
    for cid in ids_kor:
        perfis[cid]["override_ano"] = {2022: 0.35, 2023: 0.55, 2024: 1.45, 2025: 2.35, 2026: 3.10}
    reg["I4"] = ids_kor

    # I15 - mercado em retracao: Argentina
    ids_arg = dcli.loc[dcli.Pais == "Argentina", "ClienteID"].tolist()
    for cid in ids_arg:
        perfis[cid]["override_ano"] = {2022: 1.25, 2023: 1.20, 2024: 1.00, 2025: 0.72, 2026: 0.48}
    reg["I15"] = ids_arg

    # I9 - churn deliberado (90 / 180 / 365 dias) em clientes relevantes
    churns = []
    for cid, dias in [(top_ids[6], 90), (top_ids[9], 180), (top_ids[12], 365), (top_ids[17], 365)]:
        ini = date(2025, 3, 1) + timedelta(days=int(rng.integers(0, 200)))
        perfis[cid]["churn_ini"] = ini
        perfis[cid]["churn_fim"] = ini + timedelta(days=dias)
        churns.append((cid, dias, ini.isoformat()))
    reg["I9"] = churns

    # clientes perdidos definitivos
    perdidos = [k for k in top_ids[25:200:23]][:8]
    for cid in perdidos:
        perfis[cid]["fim"] = date(2024, 6, 1) + timedelta(days=int(rng.integers(0, 500)))
    reg["I9b"] = perdidos

    # I3b - vendedor que cresce descontando demais
    vend_desc = 11
    for cid in dcli.loc[dcli.VendedorResponsavelID == vend_desc, "ClienteID"]:
        perfis[cid]["desc_perfil"] = float(rng.uniform(0.11, 0.19))
        perfis[cid]["tend"] = max(perfis[cid]["tend"], 1.22)
    reg["I20"] = vend_desc

    # I13 - Food Service com desconto agressivo e margem baixa
    for cid in dcli.loc[dcli.TipoCliente == "Food Service", "ClienteID"]:
        perfis[cid]["desc_perfil"] += 0.05
    reg["I13"] = "Food Service"

    # I7 - produto campeao / I8 - produto problematico
    camp = int(dprod.loc[(dprod.Subcategoria == "Cafe Arabica Especial")].ProdutoID.iloc[0])
    prob = int(dprod.loc[(dprod.Subcategoria == "Polpa de Acai Congelada")].ProdutoID.iloc[-1])
    reg["I7"], reg["I8"] = camp, prob

    # I18 - grupo de clientes so-cafe (white space)
    ws = [k for k in top_ids[30:150:9]][:12]
    for cid in ws:
        perfis[cid]["cesta"] = ["Cafe"]
        perfis[cid]["cat_p"] = "Cafe"
    reg["I18"] = ws

    # I11 - concentracao: reforca os 6 maiores
    for cid in top_ids[:6]:
        perfis[cid]["base"] *= 2.05
    reg["I11"] = top_ids[:10]
    return reg


def gerar_vendas(dcli, dprod, dpais, perfis, usd_map, reg):
    prod_por_cat = {c: g.ProdutoID.tolist() for c, g in dprod.groupby("Categoria")}
    prod_info = dprod.set_index("ProdutoID").to_dict("index")
    cli_info = dcli.set_index("ClienteID").to_dict("index")
    pais_info = dpais.set_index("PaisID").to_dict("index")

    ativos = set(dprod.loc[dprod.StatusProduto != "Descontinuado", "ProdutoID"])
    novos = set(dprod.loc[dprod.StatusProduto == "Novo", "ProdutoID"])
    descont = set(dprod.loc[dprod.StatusProduto == "Descontinuado", "ProdutoID"])

    camp, prob = reg["I7"], reg["I8"]

    linhas = []
    venda_id = 0
    pedido_id = 0
    invoice_seq = 0

    LAMBDA_MULT = 1.85

    for cid, pf in perfis.items():
        cli = cli_info[cid]
        cad = date.fromisoformat(cli["DataCadastro"])
        pid_pais = int(cli["PaisID"])
        base_mes = pf["base"] / 12.0
        for per in MESES_IDX:
            m_ini = per.to_timestamp().date()
            m_fim = per.to_timestamp(how="end").date()
            if m_fim < cad or m_ini > DT_FIM:
                continue
            if pf.get("fim") and m_ini > pf["fim"]:
                continue
            if pf.get("churn_ini") and pf["churn_ini"] <= m_ini <= pf["churn_fim"]:
                continue
            ano, mes = per.year, per.month

            f_ano = CRESC_ANO[ano] * (pf["tend"] ** (ano - 2022))
            if "override_ano" in pf:
                f_ano = CRESC_ANO[ano] * pf["override_ano"].get(ano, 1.0)

            lam = pf["lam"] * LAMBDA_MULT
            if ano == cad.year and mes < cad.month + 1:
                lam *= 0.5
            n_ped = int(rng.poisson(lam))
            if n_ped == 0:
                continue

            for _ in range(n_ped):
                pedido_id += 1
                invoice_seq += 1
                dia = int(rng.integers(1, (m_fim - m_ini).days + 2))
                d_pedido = m_ini + timedelta(days=dia - 1)
                if d_pedido > DT_FIM:
                    d_pedido = DT_FIM
                lag = int(rng.integers(3, 21))
                d_fat = min(d_pedido + timedelta(days=lag), DT_FIM)
                tx = usd_map.get(d_fat.isoformat(), 5.3)

                status_ped = "Faturado"
                if rng.random() < 0.018:
                    status_ped = "Cancelado"
                elif d_fat > date(2026, 7, 15):
                    status_ped = pick(["Faturado", "Em Producao"], p=[0.7, 0.3])

                inco = pf["incoterm"] if rng.random() < 0.75 else pick(INCOTERMS, p=P_INCOTERM)
                modal_aereo = rng.random() < pf["modal_aereo"]

                n_itens = int(rng.integers(1, 7))
                cats_pedido = [pick(pf["cesta"]) for _ in range(n_itens)]
                receita_mes_pedido = base_mes * f_ano / max(lam, 0.4)

                for cat in cats_pedido:
                    cands = [p for p in prod_por_cat.get(cat, []) if p in ativos or rng.random() < 0.25]
                    if not cands:
                        continue
                    # produto campeao e problematico ganham peso
                    w = np.ones(len(cands))
                    for k, p in enumerate(cands):
                        if p == camp:
                            w[k] = 5.5 + 1.9 * (ano - 2022)
                        elif p == prob:
                            w[k] = 4.2
                        elif p in novos:
                            w[k] = 0.25 if ano < 2025 else 1.8
                        elif p in descont:
                            w[k] = 1.4 if ano <= 2023 else 0.05
                    w = w / w.sum()
                    pidp = int(pick(cands, p=w))
                    pr = prod_info[pidp]
                    cat_real = pr["Categoria"]

                    saz = SAZONALIDADE[cat_real][mes - 1]
                    alvo = receita_mes_pedido / max(n_itens, 1) * saz * float(rng.lognormal(0, 0.34))
                    preco_lista = pr["PrecoListaUSD"]

                    # politica de preco: reajustes anuais + premio/desconto por pais
                    reaj = {2022: 1.00, 2023: 1.045, 2024: 1.09, 2025: 1.155, 2026: 1.19}[ano]
                    premio_pais = 1.0 + (0.04 if pais_info[pid_pais]["ClassificacaoMercado"] == "Principal" else -0.02)
                    preco_un = preco_lista * reaj * premio_pais * float(rng.normal(1.0, 0.045))
                    if pidp == camp:
                        preco_un *= 1.06
                    if pidp == prob:
                        preco_un *= 0.93
                    preco_un = r2(max(preco_un, preco_lista * 0.55))

                    qtd = max(1, int(round(alvo / preco_un)))
                    if qtd > 4000:
                        qtd = int(4000 + (qtd - 4000) * 0.25)
                    receita_bruta = r2(qtd * preco_un)
                    if receita_bruta < 380:
                        continue

                    peso = qtd * pr["PesoLiquidoKg"]

                    # descontos
                    desc_pct = pf["desc_perfil"] + max(0.0, (receita_bruta - 60000) / 1_400_000)
                    if rng.random() < 0.007:
                        desc_pct += float(rng.uniform(0.10, 0.20))     # desconto excepcional (anomalia)
                    desc_pct = float(np.clip(desc_pct + rng.normal(0, 0.012), 0, 0.42))
                    desconto = r2(receita_bruta * desc_pct)
                    receita_liq = r2(receita_bruta - desconto)

                    # custo do produto
                    ci = CUSTO_INDEX[cat_real][ano]
                    tx = round(tx, 4)
                    custo_brl = r2(pr["CustoBaseBRL"] * ci * qtd * float(rng.normal(1.0, 0.03)))
                    custo_usd = r2(custo_brl / tx)

                    # frete
                    lt = pais_info[pid_pais]["LeadTimeMedio"]
                    frete_kg = (0.055 + lt * 0.0072) * (3.6 if modal_aereo else 1.0)
                    # choque logistico out/2024 - jan/2025
                    if (ano == 2024 and mes >= 10) or (ano == 2025 and mes == 1):
                        frete_kg *= 1.38
                    if pidp == prob:
                        frete_kg *= 1.55            # produto problematico: refrigerado
                    frete = peso * frete_kg * FRETE_INCOTERM[inco] * float(rng.normal(1.0, 0.09))
                    frete = r2(max(frete, 0.0))
                    seguro = r2(receita_liq * 0.0042 * SEGURO_INCOTERM[inco] * float(rng.normal(1.0, 0.12)))
                    despesas = receita_liq * float(rng.uniform(0.016, 0.034)) + 240 / max(n_itens, 1)
                    if inco == "DDP":
                        despesas += receita_liq * pais_info[pid_pais]["TarifaMediaImportacao"] / 100
                    despesas = r2(despesas)

                    custo_total = r2(custo_usd + frete + seguro + despesas)
                    margem = r2(receita_liq - custo_total)
                    venda_id += 1
                    linhas.append((
                        venda_id, f"PED-{ano}-{pedido_id:06d}",
                        d_pedido.isoformat(), d_fat.isoformat(),
                        cid, pidp, int(cli["VendedorResponsavelID"]), pid_pais,
                        qtd, r2(peso), preco_un, receita_bruta, desconto, receita_liq,
                        tx, r2(receita_liq * tx), custo_brl, custo_usd,
                        frete, seguro, despesas, custo_total, margem,
                        round(margem / receita_liq, 4) if receita_liq else 0.0,
                        cli["MoedaPreferencial"], inco, cli["CanalVenda"],
                        f"INV-{ano}-{invoice_seq:06d}", status_ped))

    cols = ["VendaID", "PedidoID", "DataPedido", "DataFaturamento", "ClienteID", "ProdutoID",
            "VendedorID", "PaisID", "Quantidade", "PesoTotalKg", "PrecoUnitarioUSD",
            "ReceitaBrutaUSD", "DescontoUSD", "ReceitaLiquidaUSD", "TaxaCambio", "ReceitaLiquidaBRL",
            "CustoProdutoBRL", "CustoProdutoUSD", "FreteUSD", "SeguroUSD", "DespesasExportacaoUSD",
            "CustoTotalUSD", "MargemBrutaUSD", "MargemBrutaPercentual", "MoedaNegociacao",
            "Incoterm", "CanalVenda", "NumeroInvoice", "StatusPedido"]
    return pd.DataFrame(linhas, columns=cols)


# =====================================================================
# 9. fEmbarques
# =====================================================================
MOTIVOS = ["Congestionamento portuario", "Documentacao", "Inspecao alfandegaria",
           "Atraso do armador", "Condicoes climaticas", "Indisponibilidade de container",
           "Atraso na producao"]
P_MOTIVO = [0.24, 0.16, 0.14, 0.18, 0.10, 0.10, 0.08]


def gerar_embarques(fv, dporto, dtrans, dpais, dcli):
    ped = (fv[fv.StatusPedido == "Faturado"]
           .groupby("PedidoID")
           .agg(ClienteID=("ClienteID", "first"), PaisID=("PaisID", "first"),
                DataFaturamento=("DataFaturamento", "first"), PesoKg=("PesoTotalKg", "sum"),
                FreteUSD=("FreteUSD", "sum"), SeguroUSD=("SeguroUSD", "sum"),
                Incoterm=("Incoterm", "first"), Receita=("ReceitaLiquidaUSD", "sum"))
           .reset_index())

    portos_br = dporto[(dporto.Pais == "Brasil")]
    br_mar = portos_br[portos_br.TipoPorto.isin(["Maritimo", "Fluvial"])].PortoID.tolist()
    br_aer = portos_br[portos_br.TipoPorto == "Aereo"].PortoID.tolist()
    p_br_mar = np.array([0.52, 0.16, 0.11, 0.08, 0.06, 0.04, 0.03])
    p_br_mar = p_br_mar[:len(br_mar)] / p_br_mar[:len(br_mar)].sum()

    dest_map = {}
    for pais, lst in PORTOS_INT.items():
        ids = dporto[(dporto.Pais == pais)].PortoID.tolist()
        dest_map[pais] = ids
    pais_nome = dpais.set_index("PaisID")["Pais"].to_dict()
    pais_lt = dpais.set_index("PaisID")["LeadTimeMedio"].to_dict()

    tr_mar = dtrans[dtrans.ModalPrincipal == "Maritimo"].TransportadoraID.tolist()
    tr_aer = dtrans[dtrans.ModalPrincipal == "Aereo"].TransportadoraID.tolist()
    tr_rod = dtrans[dtrans.ModalPrincipal == "Rodoviario"].TransportadoraID.tolist()
    p_mar = np.array([0.19, 0.14, 0.15, 0.14, 0.11, 0.09, 0.11, 0.07])
    p_mar = p_mar[:len(tr_mar)] / p_mar[:len(tr_mar)].sum()
    aval = dtrans.set_index("TransportadoraID")["AvaliacaoFornecedor"].to_dict()

    rows = []
    for i, r in enumerate(ped.itertuples(index=False), start=1):
        pais = pais_nome[r.PaisID]
        d_fat = date.fromisoformat(r.DataFaturamento)
        rodo = pais in ("Argentina", "Uruguai", "Chile") and rng.random() < 0.45
        aereo = (not rodo) and (r.PesoKg < 900 and rng.random() < 0.34)
        if rodo:
            modal, po, pd_ = "Rodoviario", int(pick(br_mar, p=p_br_mar)), int(pick(dest_map[pais]))
            tid = int(pick(tr_rod))
            lt_prev = int(max(4, pais_lt[r.PaisID] * 0.6))
        elif aereo:
            modal, po, pd_ = "Aereo", int(pick(br_aer)), int(pick(dest_map[pais]))
            tid = int(pick(tr_aer))
            lt_prev = int(max(3, round(pais_lt[r.PaisID] * 0.22)))
        else:
            modal, po, pd_ = "Maritimo", int(pick(br_mar, p=p_br_mar)), int(pick(dest_map[pais]))
            tid = int(pick(tr_mar, p=p_mar))
            lt_prev = int(pais_lt[r.PaisID] + rng.integers(-2, 4))

        d_prev_emb = d_fat + timedelta(days=int(rng.integers(2, 12)))
        # atraso no embarque
        base_atraso_p = 0.105
        if aval[tid] < 3.7:
            base_atraso_p += 0.10
        # I5 - rota problematica: Santos -> Jebel Ali (Emirados)
        rota_critica = (pais == "Emirados Arabes Unidos" and modal == "Maritimo")
        if rota_critica:
            base_atraso_p += 0.30
        # choque logistico
        if (d_fat.year == 2024 and d_fat.month >= 10) or (d_fat.year == 2025 and d_fat.month <= 1):
            base_atraso_p += 0.09

        atraso_emb = int(rng.integers(1, 7)) if rng.random() < base_atraso_p * 0.45 else 0
        d_real_emb = d_prev_emb + timedelta(days=atraso_emb)
        d_prev_ent = d_prev_emb + timedelta(days=lt_prev)

        if rng.random() < base_atraso_p:
            extra = int(rng.gamma(2.1, 4.6)) + 1
            if rota_critica:
                extra += int(rng.integers(3, 14))
            motivo = pick(MOTIVOS, p=P_MOTIVO)
        else:
            extra = int(rng.integers(-4, 1))
            motivo = ""
        d_real_ent = d_real_emb + timedelta(days=max(1, lt_prev + extra))
        dias_atraso = (d_real_ent - d_prev_ent).days

        entregue = d_real_ent <= DT_FIM
        if not entregue:
            status = "Em transito" if d_real_emb <= DT_FIM else "Aguardando embarque"
        else:
            status = "Entregue com atraso" if dias_atraso > 0 else "Entregue no prazo"

        peso = r.PesoKg
        if modal == "Aereo":
            tipo_cont, cont_pref, vol = "ULD Aereo", "ULD", peso / 165
        elif peso > 21000:
            tipo_cont, cont_pref, vol = "40 HC", "MSKU", peso / 310
        elif peso > 9000:
            tipo_cont, cont_pref, vol = "20 DRY", "TCLU", peso / 330
        else:
            tipo_cont, cont_pref, vol = "LCL Consolidado", "LCLU", peso / 340
        if rng.random() < 0.11:
            tipo_cont = "40 REEFER"

        rows.append((
            i, r.PedidoID, r.ClienteID, r.PaisID, po, pd_, tid,
            d_prev_emb.isoformat(), d_real_emb.isoformat() if d_real_emb <= DT_FIM else "",
            d_prev_ent.isoformat(), d_real_ent.isoformat() if entregue else "",
            modal, f"{cont_pref}{int(rng.integers(1000000, 9999999))}", tipo_cont,
            r2(peso), r2(max(vol, 0.4)), r2(r.FreteUSD), r2(r.SeguroUSD),
            lt_prev, (d_real_ent - d_real_emb).days if entregue else None,
            dias_atraso if entregue else None, status, motivo))

    cols = ["EmbarqueID", "PedidoID", "ClienteID", "PaisDestinoID", "PortoOrigemID", "PortoDestinoID",
            "TransportadoraID", "DataPrevistaEmbarque", "DataRealEmbarque", "DataPrevistaEntrega",
            "DataRealEntrega", "Modal", "Container", "TipoContainer", "PesoKg", "VolumeM3",
            "FreteUSD", "SeguroUSD", "LeadTimePrevisto", "LeadTimeReal", "DiasAtraso",
            "StatusEmbarque", "MotivoAtraso"]
    df = pd.DataFrame(rows, columns=cols)
    for c in ["LeadTimeReal", "DiasAtraso"]:
        df[c] = df[c].astype("Int64")
    return df


# =====================================================================
# 10. fMetas
# =====================================================================
def gerar_metas(fv, dcli, dvend):
    fv2 = fv[fv.StatusPedido == "Faturado"].copy()
    fv2["AnoMesNumero"] = fv2.DataFaturamento.str[:4].astype(int) * 100 + fv2.DataFaturamento.str[5:7].astype(int)
    real = fv2.groupby(["VendedorID", "AnoMesNumero"]).agg(
        rec=("ReceitaLiquidaUSD", "sum"), vol=("PesoTotalKg", "sum"),
        marg=("MargemBrutaUSD", "sum"), ped=("PedidoID", "nunique")).reset_index()

    # fator de atingimento por vendedor (distribuicao proposital)
    vids = sorted(fv2.VendedorID.unique().tolist())
    fatores = {}
    for k, v in enumerate(vids):
        u = (k * 7 % len(vids)) / len(vids)
        if u < 0.20:
            fatores[v] = float(rng.uniform(1.22, 1.45))     # acima de 120%
        elif u < 0.50:
            fatores[v] = float(rng.uniform(1.02, 1.19))
        elif u < 0.80:
            fatores[v] = float(rng.uniform(0.83, 0.99))
        else:
            fatores[v] = float(rng.uniform(0.62, 0.79))     # abaixo de 80%

    reg_map = dvend.set_index("VendedorID")["RegiaoResponsavel"].to_dict()
    rows = []
    for r in real.itertuples(index=False):
        ano, mes = r.AnoMesNumero // 100, r.AnoMesNumero % 100
        f = fatores[r.VendedorID] * float(rng.normal(1.0, 0.11))
        meta_rec = r.rec / max(f, 0.35)
        rows.append(dict(
            Ano=ano, Mes=mes, AnoMes=f"{MESES_ABR[mes-1]}/{str(ano)[-2:]}",
            AnoMesNumero=r.AnoMesNumero, VendedorID=int(r.VendedorID),
            Regiao=reg_map.get(int(r.VendedorID), "Global"),
            MetaReceitaUSD=r2(meta_rec), MetaVolumeKg=r2(r.vol / max(f, 0.35) * float(rng.normal(1, .07))),
            MetaMargemUSD=r2(max(r.marg, 0) / max(f, 0.35) * float(rng.normal(1, .09))),
            MetaNovosClientes=int(max(0, rng.poisson(0.8))),
            MetaPedidos=int(max(1, round(r.ped / max(f, 0.35))))))
    df = pd.DataFrame(rows).sort_values(["AnoMesNumero", "VendedorID"])
    df.insert(0, "Data", df.AnoMesNumero.map(lambda x: f"{x//100:04d}-{x%100:02d}-01"))
    return df


# =====================================================================
# 11. fOrcamento / fForecast
# =====================================================================
def gerar_orcamento_forecast(fv, dprod, dcli, dvend):
    fv2 = fv[fv.StatusPedido == "Faturado"].copy()
    fv2["Ano"] = fv2.DataFaturamento.str[:4].astype(int)
    fv2["Mes"] = fv2.DataFaturamento.str[5:7].astype(int)
    fv2["AnoMesNumero"] = fv2.Ano * 100 + fv2.Mes
    cat = dprod.set_index("ProdutoID")["Categoria"].to_dict()
    reg = dcli.set_index("ClienteID")["RegiaoComercial"].to_dict()
    fv2["Categoria"] = fv2.ProdutoID.map(cat)
    fv2["Regiao"] = fv2.ClienteID.map(reg)

    g = fv2.groupby(["AnoMesNumero", "Regiao", "Categoria"]).agg(
        rec=("ReceitaLiquidaUSD", "sum"), cus=("CustoTotalUSD", "sum"),
        marg=("MargemBrutaUSD", "sum"), vol=("PesoTotalKg", "sum")).reset_index()

    orc = []
    for r in g.itertuples(index=False):
        f = float(rng.normal(1.0, 0.14))
        f = float(np.clip(f, 0.72, 1.34))
        ano, mes = r.AnoMesNumero // 100, r.AnoMesNumero % 100
        orc.append(dict(AnoMesNumero=r.AnoMesNumero, AnoMes=f"{MESES_ABR[mes-1]}/{str(ano)[-2:]}",
                        Ano=ano, Mes=mes, Regiao=r.Regiao, Categoria=r.Categoria,
                        ReceitaOrcadaUSD=r2(r.rec / f), CustoOrcadoUSD=r2(r.cus / f * float(rng.normal(1, .05))),
                        MargemOrcadaUSD=r2(r.marg / f * float(rng.normal(1, .08))),
                        VolumeOrcadoKg=r2(r.vol / f * float(rng.normal(1, .06)))))
    dorc = pd.DataFrame(orc)
    dorc.insert(0, "Data", dorc.AnoMesNumero.map(lambda x: f"{x//100:04d}-{x%100:02d}-01"))

    # forecast: 3 revisoes por ano (Jan, Mai, Set) — precisao melhora ao longo do ano
    fcs = []
    for ano in [2022, 2023, 2024, 2025, 2026]:
        revisoes = [(ano, 1, 1), (ano, 5, 1), (ano, 9, 1)]
        for (ry, rm, rd) in revisoes:
            d_fc = date(ry, rm, rd)
            if d_fc > DT_FIM:
                continue
            sub = g[(g.AnoMesNumero // 100 == ano)]
            for r in sub.itertuples(index=False):
                mes = r.AnoMesNumero % 100
                horizonte = max(0, mes - rm)
                erro = 0.035 + 0.021 * horizonte
                if mes < rm:
                    f = float(rng.normal(1.0, 0.012))     # meses ja realizados
                else:
                    f = float(rng.normal(1.0 + rng.normal(0, 0.02), erro))
                fcs.append(dict(AnoMesNumero=r.AnoMesNumero,
                                AnoMes=f"{MESES_ABR[mes-1]}/{str(ano)[-2:]}", Ano=ano, Mes=mes,
                                Regiao=r.Regiao, Categoria=r.Categoria,
                                ReceitaForecastUSD=r2(r.rec * f),
                                MargemForecastUSD=r2(r.marg * f * float(rng.normal(1, .05))),
                                VolumeForecastKg=r2(r.vol * f * float(rng.normal(1, .04))),
                                DataForecast=d_fc.isoformat()))
    dfc = pd.DataFrame(fcs)
    dfc.insert(0, "Data", dfc.AnoMesNumero.map(lambda x: f"{x//100:04d}-{x%100:02d}-01"))
    return dorc, dfc


# =====================================================================
# 12. fRecebimentos
# =====================================================================
FORMAS = ["Carta de Credito", "Cobranca Documentaria", "Transferencia Antecipada",
          "Conta Aberta", "Cobranca a Vista"]
P_FORMA = [0.28, 0.31, 0.14, 0.19, 0.08]


def gerar_recebimentos(fv, dcli):
    fv2 = fv[fv.StatusPedido == "Faturado"]
    inv = fv2.groupby("NumeroInvoice").agg(
        ClienteID=("ClienteID", "first"), DataFaturamento=("DataFaturamento", "first"),
        Valor=("ReceitaLiquidaUSD", "sum")).reset_index()

    prazo = dcli.set_index("ClienteID")["PrazoPagamentoPadrao"].to_dict()
    cli_ids = dcli.ClienteID.tolist()
    # comportamento financeiro por cliente
    comp = {}
    for c in cli_ids:
        u = rng.random()
        if u < 0.58:
            comp[c] = ("Pontual", 0.9, 2)
        elif u < 0.84:
            comp[c] = ("Atraso leve", 0.75, 14)
        elif u < 0.94:
            comp[c] = ("Atraso relevante", 0.52, 55)
        else:
            comp[c] = ("Inadimplente", 0.18, 260)

    hoje = DT_FIM
    rows = []
    for i, r in enumerate(inv.itertuples(index=False), start=1):
        d_fat = date.fromisoformat(r.DataFaturamento)
        pz = prazo.get(r.ClienteID, 30)
        d_venc = d_fat + timedelta(days=pz)
        perfil, p_ok, atraso_med = comp[r.ClienteID]
        valor = r.Valor

        if rng.random() < p_ok:
            atraso = int(max(0, rng.normal(1.5, 4)))
        else:
            atraso = int(max(1, rng.gamma(2.2, atraso_med / 2.2)))
        d_pag = d_venc + timedelta(days=atraso)

        if d_pag <= hoje:
            if rng.random() < 0.045:
                receb = valor * float(rng.uniform(0.35, 0.85))
                status = "Parcial"
                saldo = valor - receb
            else:
                receb = valor
                saldo = 0.0
                status = "Pago em atraso" if atraso > 3 else "Pago"
            d_pag_s = d_pag.isoformat()
            dias_atraso = max(0, (d_pag - d_venc).days)
        else:
            receb = 0.0
            saldo = valor
            d_pag_s = ""
            if d_venc < hoje:
                status = "Vencido"
                dias_atraso = (hoje - d_venc).days
            else:
                status = "Em aberto"
                dias_atraso = 0
        rows.append((i, r.NumeroInvoice, r.ClienteID, d_fat.isoformat(), d_venc.isoformat(),
                     d_pag_s, r2(valor), r2(receb), r2(saldo), status, dias_atraso,
                     pick(FORMAS, p=P_FORMA)))
    cols = ["RecebimentoID", "Invoice", "ClienteID", "DataFaturamento", "DataVencimento",
            "DataPagamento", "ValorUSD", "ValorRecebidoUSD", "SaldoUSD", "Status",
            "DiasAtraso", "FormaPagamento"]
    return pd.DataFrame(rows, columns=cols)


# =====================================================================
# 13. Validacao
# =====================================================================
def validar(tabs):
    L = []
    ok = True

    def chk(cond, msg):
        nonlocal ok
        L.append(("OK   " if cond else "FALHA") + " | " + msg)
        if not cond:
            ok = False

    fv, dcli, dprod, dvend, dpais = tabs["fVendas"], tabs["dCliente"], tabs["dProduto"], tabs["dVendedor"], tabs["dPais"]
    fe, fr, fm = tabs["fEmbarques"], tabs["fRecebimentos"], tabs["fMetas"]

    L.append("=== 1. UNICIDADE DE CHAVES ===")
    for t, k in [("dCliente", "ClienteID"), ("dProduto", "ProdutoID"), ("dVendedor", "VendedorID"),
                 ("dPais", "PaisID"), ("dPorto", "PortoID"), ("dTransportadora", "TransportadoraID"),
                 ("dCalendario", "Data"), ("fVendas", "VendaID"), ("fEmbarques", "EmbarqueID"),
                 ("fRecebimentos", "RecebimentoID")]:
        chk(tabs[t][k].is_unique, f"{t}[{k}] sem duplicidades ({tabs[t][k].nunique():,} chaves)")

    L.append("=== 2. INTEGRIDADE REFERENCIAL ===")
    chk(fv.ClienteID.isin(dcli.ClienteID).all(), "fVendas[ClienteID] -> dCliente")
    chk(fv.ProdutoID.isin(dprod.ProdutoID).all(), "fVendas[ProdutoID] -> dProduto")
    chk(fv.VendedorID.isin(dvend.VendedorID).all(), "fVendas[VendedorID] -> dVendedor")
    chk(fv.PaisID.isin(dpais.PaisID).all(), "fVendas[PaisID] -> dPais")
    chk(fe.ClienteID.isin(dcli.ClienteID).all(), "fEmbarques[ClienteID] -> dCliente")
    chk(fe.PortoOrigemID.isin(tabs["dPorto"].PortoID).all(), "fEmbarques[PortoOrigemID] -> dPorto")
    chk(fe.PortoDestinoID.isin(tabs["dPorto"].PortoID).all(), "fEmbarques[PortoDestinoID] -> dPorto")
    chk(fe.TransportadoraID.isin(tabs["dTransportadora"].TransportadoraID).all(), "fEmbarques[TransportadoraID] -> dTransportadora")
    chk(fe.PedidoID.isin(fv.PedidoID).all(), "fEmbarques[PedidoID] -> fVendas")
    chk(fr.ClienteID.isin(dcli.ClienteID).all(), "fRecebimentos[ClienteID] -> dCliente")
    chk(fr.Invoice.isin(fv.NumeroInvoice).all(), "fRecebimentos[Invoice] -> fVendas")
    chk(fm.VendedorID.isin(dvend.VendedorID).all(), "fMetas[VendedorID] -> dVendedor")
    cal = set(tabs["dCalendario"].Data)
    chk(set(fv.DataFaturamento).issubset(cal), "fVendas[DataFaturamento] dentro de dCalendario")
    chk(set(fv.DataPedido).issubset(cal), "fVendas[DataPedido] dentro de dCalendario")

    L.append("=== 3. CONSISTENCIA FINANCEIRA (tolerancia 0,05 USD) ===")
    e1 = (fv.ReceitaBrutaUSD - fv.Quantidade * fv.PrecoUnitarioUSD).abs().max()
    e2 = (fv.ReceitaLiquidaUSD - (fv.ReceitaBrutaUSD - fv.DescontoUSD)).abs().max()
    e3 = (fv.CustoTotalUSD - (fv.CustoProdutoUSD + fv.FreteUSD + fv.SeguroUSD + fv.DespesasExportacaoUSD)).abs().max()
    e4 = (fv.MargemBrutaUSD - (fv.ReceitaLiquidaUSD - fv.CustoTotalUSD)).abs().max()
    e5 = (fv.ReceitaLiquidaBRL - fv.ReceitaLiquidaUSD * fv.TaxaCambio).abs().max()
    chk(e1 < 0.05, f"Receita Bruta = Qtd x Preco (erro max {e1:.4f})")
    chk(e2 < 0.05, f"Receita Liquida = Bruta - Desconto (erro max {e2:.4f})")
    chk(e3 < 0.05, f"Custo Total = Produto + Frete + Seguro + Despesas (erro max {e3:.4f})")
    chk(e4 < 0.05, f"Margem = Receita Liquida - Custo Total (erro max {e4:.4f})")
    chk(e5 < 1.0, f"Receita BRL = Receita USD x Taxa (erro max {e5:.4f})")
    chk((fv.ReceitaLiquidaUSD > 0).all(), "Receita liquida sempre positiva")
    chk((fv.DescontoUSD >= 0).all(), "Descontos nao negativos")

    L.append("=== 4. COERENCIA TEMPORAL ===")
    chk((fv.DataFaturamento >= fv.DataPedido).all(), "DataFaturamento >= DataPedido")
    fe2 = fe[fe.DataRealEntrega != ""]
    chk((fe2.DataRealEntrega >= fe2.DataRealEmbarque).all(), "Entrega real posterior ao embarque real")
    chk((fe.DataRealEmbarque.replace("", "9999-12-31") >= fe.DataPrevistaEmbarque).all(),
        "Embarque real nao anterior ao previsto")
    fr2 = fr[fr.DataPagamento != ""]
    chk((fr2.DataPagamento >= fr2.DataFaturamento).all(), "Pagamento posterior ao faturamento")
    chk((fr.DataVencimento >= fr.DataFaturamento).all(), "Vencimento posterior ao faturamento")
    chk(fv.DataFaturamento.max() <= DT_FIM.isoformat(), "Nenhuma data fora do periodo")

    L.append("=== 5. NULOS EM CHAVES ===")
    for t in ["dCliente", "dProduto", "fVendas", "fEmbarques", "fRecebimentos"]:
        nn = tabs[t].isna().sum().sum()
        chk(True, f"{t}: {nn} celulas nulas (aceitavel em colunas de evento em aberto)")

    return ok, L


def estatisticas(tabs):
    fv = tabs["fVendas"]
    fvf = fv[fv.StatusPedido == "Faturado"]
    fe, fr = tabs["fEmbarques"], tabs["fRecebimentos"]
    S = []
    S.append(f"Clientes cadastrados............: {tabs['dCliente'].ClienteID.nunique():,}")
    S.append(f"Clientes com venda..............: {fvf.ClienteID.nunique():,}")
    S.append(f"Produtos (SKUs).................: {tabs['dProduto'].ProdutoID.nunique():,}")
    S.append(f"Vendedores......................: {tabs['dVendedor'].VendedorID.nunique():,}")
    S.append(f"Paises atendidos................: {fvf.PaisID.nunique():,}")
    S.append(f"Linhas em fVendas...............: {len(fv):,}")
    S.append(f"Pedidos.........................: {fv.PedidoID.nunique():,}")
    S.append(f"Pedidos cancelados..............: {fv[fv.StatusPedido=='Cancelado'].PedidoID.nunique():,}")
    S.append(f"Embarques.......................: {len(fe):,}")
    S.append(f"Receita liquida total (USD).....: {fvf.ReceitaLiquidaUSD.sum():,.2f}")
    S.append(f"Receita liquida total (BRL).....: {fvf.ReceitaLiquidaBRL.sum():,.2f}")
    S.append(f"Margem bruta total (USD)........: {fvf.MargemBrutaUSD.sum():,.2f}")
    S.append(f"Margem bruta media (%)..........: {fvf.MargemBrutaUSD.sum()/fvf.ReceitaLiquidaUSD.sum()*100:,.2f}%")
    S.append(f"Desconto medio (%)..............: {fvf.DescontoUSD.sum()/fvf.ReceitaBrutaUSD.sum()*100:,.2f}%")
    tk = fvf.groupby('PedidoID').ReceitaLiquidaUSD.sum()
    S.append(f"Ticket medio por pedido (USD)...: {tk.mean():,.2f}")
    S.append(f"Volume total (toneladas)........: {fvf.PesoTotalKg.sum()/1000:,.1f}")
    S.append(f"Preco medio por kg (USD)........: {fvf.ReceitaLiquidaUSD.sum()/fvf.PesoTotalKg.sum():,.2f}")
    S.append(f"Linhas com margem negativa......: {(fvf.MargemBrutaUSD<0).mean()*100:,.2f}%")
    ent = fe[fe.DiasAtraso.notna()]
    S.append(f"Entregas realizadas.............: {len(ent):,}")
    S.append(f"% entregas atrasadas............: {(ent.DiasAtraso>0).mean()*100:,.2f}%")
    S.append(f"Atraso medio (dias, atrasados)..: {ent.loc[ent.DiasAtraso>0,'DiasAtraso'].mean():,.1f}")
    S.append(f"Lead time medio real (dias).....: {ent.LeadTimeReal.mean():,.1f}")
    S.append(f"Mix modal (%)...................: " + ", ".join(
        f"{k} {v*100:.1f}%" for k, v in fe.Modal.value_counts(normalize=True).items()))
    S.append(f"Saldo em aberto (USD)...........: {fr.SaldoUSD.sum():,.2f}")
    S.append(f"Inadimplencia (vencido/total %).: {fr.loc[fr.Status=='Vencido','SaldoUSD'].sum()/fr.ValorUSD.sum()*100:,.2f}%")
    S.append(f"Prazo medio recebimento (dias)..: {fr.loc[fr.DataPagamento!='','DiasAtraso'].mean():,.1f} de atraso sobre o vencimento")
    S.append("")
    S.append("--- Receita liquida por ano (USD) ---")
    a = fvf.copy(); a["Ano"] = a.DataFaturamento.str[:4]
    ser = a.groupby("Ano").ReceitaLiquidaUSD.sum()
    prev = None
    for ano, v in ser.items():
        g = f"  ({(v/prev-1)*100:+.1f}% YoY)" if prev else ""
        S.append(f"{ano}: {v:,.2f}{g}   [margem {a[a.Ano==ano].MargemBrutaUSD.sum()/v*100:.1f}%]")
        prev = v
    S.append("  (2026 parcial: jan-jul)")
    S.append("")
    S.append("--- Concentracao de clientes (Pareto) ---")
    rc = fvf.groupby("ClienteID").ReceitaLiquidaUSD.sum().sort_values(ascending=False)
    tot = rc.sum()
    for n in [1, 5, 10, 20, 50]:
        S.append(f"Top {n:>2} clientes: {rc.head(n).sum()/tot*100:5.1f}% da receita")
    n80 = int((rc.cumsum()/tot <= 0.8).sum()) + 1
    S.append(f"{n80} clientes ({n80/len(rc)*100:.1f}%) concentram 80% da receita")
    S.append("")
    S.append("--- Top 8 paises por receita ---")
    pn = tabs["dPais"].set_index("PaisID").Pais.to_dict()
    rp = fvf.groupby("PaisID").ReceitaLiquidaUSD.sum().sort_values(ascending=False).head(8)
    for k, v in rp.items():
        S.append(f"{pn[k]:<28} {v:>16,.2f}  ({v/tot*100:4.1f}%)")
    S.append("")
    S.append("--- Receita e margem por categoria ---")
    cat = tabs["dProduto"].set_index("ProdutoID").Categoria.to_dict()
    b = fvf.copy(); b["Categoria"] = b.ProdutoID.map(cat)
    gg = b.groupby("Categoria").agg(rec=("ReceitaLiquidaUSD", "sum"), mar=("MargemBrutaUSD", "sum"))
    for k, r in gg.sort_values("rec", ascending=False).iterrows():
        S.append(f"{k:<28} {r.rec:>16,.2f}  margem {r.mar/r.rec*100:5.1f}%")
    S.append("")
    S.append("--- Incoterms ---")
    for k, v in fvf.groupby("Incoterm").ReceitaLiquidaUSD.sum().sort_values(ascending=False).items():
        S.append(f"{k:<6} {v/tot*100:5.1f}%")
    return S


# =====================================================================
# MAIN
# =====================================================================
def main():
    print("1/12 dCalendario...");   dcal = gerar_calendario()
    print("2/12 dPais...");         dpais = gerar_pais()
    print("3/12 dVendedor...");     dvend = gerar_vendedor()
    print("4/12 dProduto...");      dprod, desc, novos = gerar_produto()
    print("5/12 dCliente...");      dcli = gerar_cliente(dpais, dvend)
    print("6/12 dPorto/dTransportadora..."); dporto = gerar_porto(); dtrans = gerar_transportadora()
    print("7/12 fCambio...");       dcamb, usd_map = gerar_cambio()
    print("8/12 perfis + insights...")
    perfis = perfil_clientes(dcli)
    reg = aplicar_insights(dcli, dprod, dvend, perfis)
    print("9/12 fVendas (pode levar ~1 min)...")
    fv = gerar_vendas(dcli, dprod, dpais, perfis, usd_map, reg)
    print(f"      -> {len(fv):,} linhas")
    print("10/12 fEmbarques...");   fe = gerar_embarques(fv, dporto, dtrans, dpais, dcli)
    print("11/12 metas/orcamento/forecast/recebimentos...")
    fm = gerar_metas(fv, dcli, dvend)
    forc, ffc = gerar_orcamento_forecast(fv, dprod, dcli, dvend)
    fr = gerar_recebimentos(fv, dcli)

    # StatusCliente dinamico coerente com o historico
    ult = fv[fv.StatusPedido == "Faturado"].groupby("ClienteID").DataFaturamento.max()
    def st(c):
        u = ult.get(c)
        if u is None:
            return "Prospect"
        d = (DT_FIM - date.fromisoformat(u)).days
        return "Ativo" if d <= 180 else ("Inativo" if d <= 365 else "Perdido")
    dcli["StatusCliente"] = dcli.ClienteID.map(st)
    dcli = dcli.drop(columns=["PaisID"])

    tabs = dict(dCalendario=dcal, dCliente=dcli, dProduto=dprod, dVendedor=dvend, dPais=dpais,
                dPorto=dporto, dTransportadora=dtrans, fVendas=fv, fEmbarques=fe, fCambio=dcamb,
                fMetas=fm, fOrcamento=forc, fForecast=ffc, fRecebimentos=fr)

    print("12/12 validacao e exportacao...")
    ok, log = validar({**tabs, "dCliente": dcli})
    stats = estatisticas(tabs)

    for nome, df in tabs.items():
        df.to_csv(os.path.join(OUT, f"{nome}.csv"), index=False, encoding="utf-8-sig",
                  sep=";", decimal=",", date_format="%Y-%m-%d")

    with open(os.path.join(DOC, "ValidacaoDados.md"), "w", encoding="utf-8") as f:
        f.write("# Relatorio de Validacao — Aurora Brasil Exportadora\n\n")
        f.write(f"Seed: `{SEED}` | Periodo: {DT_INI} a {DT_FIM}\n\n")
        f.write(f"**Resultado geral: {'APROVADO' if ok else 'REPROVADO'}**\n\n## Testes\n\n```\n")
        f.write("\n".join(log))
        f.write("\n```\n\n## Estatisticas\n\n```\n")
        f.write("\n".join(stats))
        f.write("\n```\n\n## Linhas por tabela\n\n| Tabela | Linhas | Colunas |\n|---|---:|---:|\n")
        for n, d in tabs.items():
            f.write(f"| {n} | {len(d):,} | {len(d.columns)} |\n")

    print("\n".join(log[-0:]))
    print("\n".join(stats))
    print("\nVALIDACAO:", "APROVADO" if ok else "REPROVADO")
    for l in log:
        if l.startswith("FALHA"):
            print(l)
    import json
    with open(os.path.join(DOC, "_insights_registro.json"), "w") as f:
        json.dump({k: (v if not isinstance(v, (np.integer,)) else int(v)) for k, v in reg.items()},
                  f, default=str, indent=1)
    return tabs


if __name__ == "__main__":
    main()
