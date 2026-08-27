#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Revalida os CSVs entregues, de forma independente do gerador.
Uso:  python3 validate_data.py [caminho_da_pasta_dados]"""
import os, sys
import pandas as pd

DADOS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados")

TAB = ["dCalendario", "dCliente", "dProduto", "dVendedor", "dPais", "dPorto", "dTransportadora",
       "fVendas", "fEmbarques", "fCambio", "fMetas", "fOrcamento", "fForecast", "fRecebimentos"]
PK = {"dCliente": "ClienteID", "dProduto": "ProdutoID", "dVendedor": "VendedorID",
      "dPais": "PaisID", "dPorto": "PortoID", "dTransportadora": "TransportadoraID",
      "dCalendario": "Data", "fVendas": "VendaID", "fEmbarques": "EmbarqueID",
      "fRecebimentos": "RecebimentoID"}
FK = [("fVendas", "ClienteID", "dCliente", "ClienteID"),
      ("fVendas", "ProdutoID", "dProduto", "ProdutoID"),
      ("fVendas", "VendedorID", "dVendedor", "VendedorID"),
      ("fVendas", "PaisID", "dPais", "PaisID"),
      ("fEmbarques", "ClienteID", "dCliente", "ClienteID"),
      ("fEmbarques", "PaisDestinoID", "dPais", "PaisID"),
      ("fEmbarques", "PortoOrigemID", "dPorto", "PortoID"),
      ("fEmbarques", "PortoDestinoID", "dPorto", "PortoID"),
      ("fEmbarques", "TransportadoraID", "dTransportadora", "TransportadoraID"),
      ("fRecebimentos", "ClienteID", "dCliente", "ClienteID"),
      ("fMetas", "VendedorID", "dVendedor", "VendedorID")]

erros = []
d = {}
for t in TAB:
    p = os.path.join(DADOS, f"{t}.csv")
    if not os.path.exists(p):
        erros.append(f"Arquivo ausente: {t}.csv"); continue
    d[t] = pd.read_csv(p, sep=";", decimal=",", encoding="utf-8-sig")
    print(f"{t:<18} {len(d[t]):>8,} linhas x {len(d[t].columns):>2} colunas")

for t, k in PK.items():
    if t in d and not d[t][k].is_unique:
        erros.append(f"Chave duplicada em {t}[{k}]")
for ft, fc, dt, dc in FK:
    if ft in d and dt in d and not d[ft][fc].isin(d[dt][dc]).all():
        erros.append(f"Chave orfa: {ft}[{fc}] -> {dt}[{dc}]")

if "fVendas" in d:
    f = d["fVendas"]
    checks = [("Receita Bruta = Qtd x Preco", (f.ReceitaBrutaUSD - f.Quantidade * f.PrecoUnitarioUSD).abs().max()),
              ("Receita Liquida = Bruta - Desconto", (f.ReceitaLiquidaUSD - (f.ReceitaBrutaUSD - f.DescontoUSD)).abs().max()),
              ("Custo Total = soma dos custos", (f.CustoTotalUSD - (f.CustoProdutoUSD + f.FreteUSD + f.SeguroUSD + f.DespesasExportacaoUSD)).abs().max()),
              ("Margem = Liquida - Custo Total", (f.MargemBrutaUSD - (f.ReceitaLiquidaUSD - f.CustoTotalUSD)).abs().max())]
    for nome, err in checks:
        print(f"{nome:<38} erro maximo {err:.4f}")
        if err > 0.05:
            erros.append(f"Inconsistencia financeira: {nome} (erro {err:.4f})")
    if (f.DataFaturamento < f.DataPedido).any():
        erros.append("Faturamento anterior ao pedido")

if "fEmbarques" in d:
    e = d["fEmbarques"].dropna(subset=["DataRealEntrega"])
    if (e.DataRealEntrega < e.DataRealEmbarque).any():
        erros.append("Entrega anterior ao embarque")

print()
if erros:
    print("REPROVADO")
    for x in erros:
        print(" -", x)
    sys.exit(1)
print("APROVADO — integridade referencial e consistencia financeira verificadas")
