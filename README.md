# Aurora Brasil Exportadora — Dashboard Executivo em Power BI

<!-- portfolio-link:start -->
[![Ver no portfólio](https://img.shields.io/badge/Ver%20o%20painel%20no%20portf%C3%B3lio-Bocardi%20Data-6C3BAA?style=for-the-badge)](https://bocardidata.base44.app/ProjectDetail?id=6a9037768f19cf0df82696d2)

> 🔗 **Quer ver o visual do Power BI?** Acesse a página do projeto no portfólio: **[https://bocardidata.base44.app/ProjectDetail?id=6a9037768f19cf0df82696d2](https://bocardidata.base44.app/ProjectDetail?id=6a9037768f19cf0df82696d2)**
<!-- portfolio-link:end -->


Dashboard executivo completo para uma exportadora brasileira de alimentos premium, construído do
zero: da geração da base sintética ao modelo dimensional, das medidas DAX ao storytelling visual.

**Empresa fictícia, complexidade real.** Todos os dados, clientes, produtos e pessoas são
sintéticos — mas as regras de negócio, a matemática financeira e os padrões analíticos foram
construídos para sustentar decisões reais.

---

## O que o painel responde

Cada página existe para responder a uma pergunta de negócio específica:

| Página | Pergunta |
|---|---|
| **Executive Overview** | Estamos crescendo, atingindo meta e preservando rentabilidade? |
| **Sales Performance** | O ritmo comercial está acima ou abaixo do compromisso assumido? |
| **Customers** | Quem sustenta a receita, quem está escapando e quanto isso custa? |
| **Customer Potential** | Onde existe receita não capturada e qual conta merece prioridade? |
| **Products** | Qual portfólio cresce com rentabilidade e qual cresce destruindo margem? |
| **Markets** | Quais mercados sustentam hoje e quais sustentarão os próximos anos? |
| **Profitability** | Entre a receita bruta e a margem, onde o valor está sendo consumido? |
| **Logistics** | Onde a operação perde prazo e quanto isso custa por quilo? |
| **Sales Team** | Quem entrega, quem depende de um único cliente e quem precisa de apoio? |
| **Finance** | Quanto do faturamento ainda não virou caixa e qual cliente trava o ciclo? |
| **Forecast e Budget** | Se a tendência continuar, fechamos o ano acima ou abaixo do compromisso? |

---

## Números do projeto

| | |
|---|---|
| Transações (fVendas) | 96.443 linhas |
| Período | jan/2022 a jul/2026 |
| Mercados | 28 países |
| Clientes | 330 |
| SKUs | 106 |
| Equipe comercial | 20 vendedores |
| Receita líquida simulada | US$ 447,6 milhões |
| Margem bruta | 25,6% |
| Medidas DAX | 179, em 17 display folders |
| Tabelas | 15 (modelo estrela, 21 relacionamentos, zero bidirecionais) |
| Páginas | 11 analíticas + guia + 4 tooltips + 2 drill-through |

---

## O que tem de diferente aqui

**Painéis de KPI em HTML.** Os cartões nativos deram lugar a painéis renderizados por medida DAX
que devolve HTML — cada KPI traz um mini-gráfico de 12 meses ou uma barra de progresso com marca
na meta, tudo dentro da mesma faixa de 92px que os cartões ocupavam.

**Tooltips contextuais por dimensão.** Quatro fichas em HTML (Cliente, Produto, Mercado,
Vendedor). A do produto compara margem real contra a margem alvo do SKU; a do vendedor mostra
concentração de carteira no maior cliente — números que não aparecem em nenhum gráfico da página.

**Guia de análise embutido.** Uma medida HTML documenta o que cada visual permite analisar, dentro
do próprio relatório. Quem abre o painel sem ter acompanhado a construção não fica perdido.

**Dossiês por drill-through.** Botão direito em qualquer cliente ou país abre uma página inteira
de detalhe, com botão de retorno para a página de origem exata.

---

## Como está construído

```
dados/          14 CSVs sintéticos (sep=";", decimal=",", UTF-8, datas ISO)
PowerBI/        projeto PBIP — TMDL para o modelo, PBIR enhanced para o relatório
scripts/        geradores em Python e Perl (o projeto é reproduzível por código)
documentacao/   13 documentos: dicionário de dados, medidas, regras de negócio, QA
```

Todo o projeto é **gerado por script**, não editado à mão. Alterou uma regra? Edita o gerador e
regera — assim o artefato nunca diverge da fonte.

| Script | O que faz |
|---|---|
| `generate_data.py` | Gera os 14 CSVs com seed fixa (20260816) |
| `build_model.py` | Gera o TMDL: tabelas, 179 medidas, relacionamentos |
| `build_report.py` | Gera o PBIR: páginas, visuais, tema |
| `gen_paineis.pl` | Gera os painéis HTML de KPI a partir de um spec único |
| `gen_tooltips.pl` | Gera as 4 fichas HTML de tooltip |
| `gen_guia.pl` | Gera o guia de análise embutido |
| `validate_pbip.py` | QA estrutural do projeto |
| `validate_data.py` | QA independente dos CSVs |

---

## Como abrir

1. Clone o repositório em um caminho curto (`C:\PBI\`, por exemplo) — projetos PBIR criam
   caminhos profundos e o Windows tem limite de 260 caracteres.
2. Abra `PowerBI/AuroraBrasilExportadora.pbip` no Power BI Desktop.
3. Ajuste o parâmetro **`pBasePath`** no Power Query para a pasta `dados/` do seu clone. É o único
   ponto de configuração — as 14 queries derivam dele.

**Requisitos:** Power BI Desktop com PBIR habilitado. Os visuais de mapa dependem da configuração
de locatário *"Visuais de mapa e mapa preenchido"*. O painel de KPI usa o visual **HTML Content**
(AppSource).

Para regerar do zero: Python 3.11+ com `pandas` e `numpy`, e Perl (já vem no Git for Windows).

---

## Documentação

Em `documentacao/`:

- **`DicionarioDados.md`** — toda coluna documentada
- **`ModeloDados.md`** — relacionamentos e cardinalidades
- **`MedidasDAX.md`** — as 179 medidas com expressão e dependências
- **`RegrasNegocio.md`** — as regras que geraram os dados
- **`InsightsEncontrados.md`** — o que a análise exploratória revelou
- **`CorrecoesPBIP.md`** — registro de causa-raiz dos bloqueios de formato e como foram resolvidos
- **`QA.md`** — validações executadas

> `InsightsOcultos.md` contém as respostas dos padrões implantados na base. Se a intenção for
> treinar análise exploratória, explore o dashboard antes de ler.

---

## Licença

Projeto de portfólio. Dados inteiramente sintéticos — nenhuma informação real de empresa,
cliente ou pessoa.
