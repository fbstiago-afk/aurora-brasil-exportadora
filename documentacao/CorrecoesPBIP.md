# Correções aplicadas ao PBIP — 17/08/2026

Sessão de retomada no Claude Code, seguindo o `HANDOFF` (seção 4: "o projeto ainda não abriu no
Power BI Desktop"). Todas as correções foram feitas **no script gerador e no artefato gerado**,
para que os dois fiquem coerentes.

## Como os erros foram identificados

Este ambiente **não tem Python instalado**, então `validate_pbip.py` não pôde ser executado.
Em vez de validar contra o conhecimento prévio (que foi justamente a origem dos três erros
anteriores), usei como **verdade de campo** um projeto PBIP real gerado pelo próprio Power BI
Desktop desta máquina:

```
E:\Projetos BI\Analise de Fundos\Analise de Fundos novo.pbip
```

Todo `$schema`, versão e convenção de indentação abaixo foi conferido byte a byte contra esse
projeto — que comprovadamente abre nesta versão do Desktop.

---

## 1. Bloqueadores de carregamento (corrigidos)

### 1.1 `$schema` do `.pbip` — o erro nº 3 do handoff nunca chegou ao arquivo

O handoff registra que o `$schema` do `.pbip` havia sido corrigido, mas **nem o arquivo nem o
`build_report.py` tinham a correção**. Estava apontando para o caminho errado.

| | Antes | Depois |
|---|---|---|
| `.pbip` | `fabric/item/pbip/definitionProperties/1.0.0` | `fabric/pbip/pbipProperties/1.0.0` |

### 1.2 `definition.pbir` estava declarando PBIR-legacy

O relatório usa a estrutura PBIR *enhanced* (pasta `definition/` com um JSON por visual), mas o
`definition.pbir` declarava `definitionProperties/1.0.0` + `version 1.0`, que é o contrato do
formato **antigo**. O Desktop procuraria um `report.json` monolítico na raiz.

| | Antes | Depois |
|---|---|---|
| `$schema` | `item/report/definitionProperties/1.0.0` | `item/report/definitionProperties/2.0.0` |
| `version` | `1.0` | `4.0` |

### 1.3 Versões de schema inexistentes em todo o relatório

Todos os arquivos do relatório usavam `1.0.0`, que não é uma versão publicada.

| Arquivo | Antes | Depois | Qtd. |
|---|---|---|---|
| `report.json` | `report/1.0.0` | `report/3.3.0` | 1 |
| `pages/pages.json` | `pagesMetadata/1.0.0` | `pagesMetadata/1.1.0` | 1 |
| `pages/*/page.json` | `page/1.0.0` | `page/2.1.0` | 17 |
| `pages/*/visuals/*/visual.json` | `visualContainer/1.0.0` | `visualContainer/2.11.0` | 180 |

### 1.4 `definition.pbism` sem `$schema`

Adicionado `fabric/item/semanticModel/definitionProperties/1.0.0/schema.json`.

### 1.5 Indentação mista nas partitions M — quebrava o TMDL

**Este era um bloqueador do modelo, não do carregador de projeto.** Em `build_model.py`, a
função `m_query()` devolvia um bloco cuja primeira linha era indentada com **4 tabs** e as
demais com **20 espaços**:

```
\t\t\t\tlet
                    Origem = Csv.Document(
```

O parser TMDL toma a indentação da primeira linha do bloco como prefixo e a remove das demais.
Com tabs na primeira linha e espaços nas seguintes, o bloco não fecha. Afetava **as 14 tabelas**.

Corrigido para o mesmo padrão do projeto de referência: prefixo de 4 tabs em **toda** linha, com
a indentação relativa do M em espaços.

### 1.6 Descrições `///` fora de lugar no TMDL

Em TMDL a descrição precede a declaração do objeto, na mesma indentação. Dois bugs no gerador:

- **Medidas** — `L.insert(len(L) - len(dax.split('\n')), ...)` calculava o deslocamento como se
  o corpo DAX multilinha tivesse sido inserido linha a linha, mas ele entra como **um único
  elemento** da lista. Resultado: 7 descrições caíram no meio do bloco de propriedades da medida
  *anterior* (entre `formatString` e `displayFolder`, ou logo após a expressão).
- **Tabelas** — `linhas.insert(1, ...)` colocava o `///` **depois** de `table X`, e com um tab de
  indentação. Afetava as 15 tabelas.

Ambos corrigidos no gerador e nos 15 `.tmdl`.

---

## 2. Risco de dados apontado no handoff (resolvido)

O handoff alertava que `Table.RemoveRowsWithErrors` **descarta a linha inteira em silêncio**
quando um único valor não converte — o caso citado era `LeadTimeReal`/`DiasAtraso` vazios em
`fEmbarques` (embarque ainda não entregue).

Substituído por `Table.ReplaceErrorValues`, que transforma o erro em `null` e **preserva a
linha**:

```m
ErrosTratados = Table.ReplaceErrorValues(
    TiposAplicados,
    List.Transform(Table.ColumnNames(TiposAplicados), each {_, null})
)
```

Continuam sendo 4 etapas nomeadas por query, conforme a decisão de arquitetura da seção 5 do
handoff. Isso deve fazer a contagem de `fEmbarques` bater com `ValidacaoDados.md` (~24k) em vez
de vir silenciosamente menor.

---

## 3. Ajustes de conformidade com as skills

### 3.1 `pbir-expert` — chaves não confirmadas removidas de `report.json`

`layoutOptimization`, `useNewFilterPaneExperience` e `disableFilterPaneSearch` não aparecem em
nenhum `report.json` gerado pelo Desktop. Como os schemas PBIR rejeitam propriedades
desconhecidas, foram trocadas pelo conjunto confirmado:

```json
"settings": {
  "useStylableVisualContainerHeader": true,
  "exportDataMode": "AllowSummarized",
  "defaultFilterActionIsDataFilter": true,
  "defaultDrillFilterOtherVisuals": true,
  "allowChangeFilterTypes": true,
  "useEnhancedTooltips": true
}
```

Também alinhado o nome do tema: `themeCollection.customTheme.name` agora é idêntico ao `name` do
item em `resourcePackages` (`AuroraBrasilTheme.json`), como o Desktop grava.

### 3.2 Páginas de tooltip apareciam como abas normais

As 4 páginas `tt_*` tinham `pageBinding.type: "Tooltip"` mas **não** tinham
`visibility: "HiddenInViewMode"` — apareceriam como abas comuns no modo leitura. As 2 páginas de
drill-through já estavam corretas. Corrigido.

### 3.3 `dataviz-powerbi` — desvios estruturais/SWD

Auditoria dos 180 visuais contra as regras da skill que independem de paleta:

| Regra | Desvios | Ação |
|---|---|---|
| `drillFilterOtherVisuals` presente | 180 | adicionado (`true`) |
| `subTitle show:false` explícito | 167 | adicionado onde não há subtítulo com texto |
| `showAxisTitle:false` no `valueAxis` | 34 | adicionado |
| Slicer com header e altura < 55px | 5 | header interno desligado — o rótulo já vem do título do container, e a faixa do cabeçalho tem 42px |
| dataLabels ON + valueAxis ON | 0 | já estava correto |
| Query wells (`Y` / `Values` / `Data`) | 0 | já estava correto |
| `lineChart` com marcadores | 0 | já estava correto |

Reauditoria após as correções: **nenhum desvio**.

**A paleta da skill (verde) não foi aplicada** — a identidade petróleo `#0E2A33` + cobre
`#C8763C` é decisão de arquitetura do projeto (seção 5 do handoff). Só as regras estruturais e
de storytelling, que são independentes de paleta, foram aplicadas.

### 3.4 `pages.json`

Adicionado `landingPageName: "p01_executive"`, como o Desktop grava junto de `activePageName`.

---

## 4. Verificações executadas nesta sessão

Substitutos de `validate_pbip.py` escritos em Perl/PowerShell (Python indisponível):

| Verificação | Resultado |
|---|---|
| JSON válido em todo o projeto (200 arquivos) | OK — 0 inválidos |
| Referências campo→modelo nos 180 `visual.json` | OK — 311 referências, 0 quebradas |
| Inventário do modelo | 15 tabelas, 210 colunas, 159 medidas |
| Descrições `///` precedendo a declaração | OK — 0 fora de lugar |
| Indentação dos blocos TMDL (nenhuma linha iniciando com espaço) | OK |
| Parênteses/aspas balanceados nas 159 medidas | OK |
| Encoding: UTF-8 sem BOM, LF, sem escapes `\uXXXX` | OK |
| Auditoria dataviz dos 180 visuais | OK — 0 desvios |

---

## 4b. Segunda rodada — erros reais do Desktop (17/08, tarde)

### `RequiredArtifactMissing: definition.pbir`

A primeira tentativa foi feita sobre o ZIP antigo (`D:\0 - Downloads\Aurora_PowerBI_corrigido.zip`),
que ainda tinha `definitionProperties/1.0.0` + `version 1.0`. O erro confirmou o diagnóstico do
item 1.2: o Desktop não conseguiu casar o `.pbir` com nenhuma variante conhecida
(`PBIProjectSchemaValidator.GetValidVariant`). Aquele ZIP também não contém a pasta `dados\`,
então nunca funcionaria. **Usar sempre a pasta do projeto em `E:\`.**

### `Cannot find file 'version.json'`

Com o `.pbir` correto, o carregador de projeto passou e o erro migrou para o desserializador do
relatório (`ExplorationSerializer.DeserializeRootExplorationArtifactAsync` →
`Error Reading StorageSection: ReportDocument`).

Faltava **`definition/version.json`**, artefato obrigatório do PBIR enhanced que o
`build_report.py` nunca gerou:

```json
{
  "$schema": ".../report/definition/versionMetadata/1.0.0/schema.json",
  "version": "2.0.0"
}
```

Criado no projeto e adicionado ao gerador. O inventário de arquivos do `.Report` agora é idêntico
ao do projeto de referência — fora `bookmarks/`, que o Aurora não usa, e `.pbi/localSettings.json`,
que o próprio Desktop cria.

### Conferência contra os schemas públicos

| Arquivo | Obrigatórios pelo schema | Aurora |
|---|---|---|
| `report.json` (3.3.0) | `$schema`, `themeCollection` | OK — `baseTheme` é opcional |
| `pages.json` (1.1.0) | `$schema`; `additionalProperties: false` | OK, sem chaves extras |
| `page.json` (2.1.0) | `$schema`, `name`, `displayName`, `displayOption` | OK nos 17; enums de `displayOption`/`visibility`/`pageBinding.type` válidos |

O schema de `visualContainer/2.11.0` retorna 404 no site da Microsoft, mas é a versão que o
projeto de referência gerado por este mesmo Desktop usa — é lacuna de publicação, não versão
inválida.

---

## 4c. O projeto ABRIU — validação em runtime (17/08, 13:48)

Terceira tentativa: o `.pbip` abriu, o modelo carregou (`\.pbi\cache.abf` de 17 MB) e o Desktop
re-serializou todo o projeto. **Ele manteve todas as correções**: os schemas (`2.11.0`, `2.1.0`,
`1.1.0`, `3.3.0`), o `version.json`, as 6 páginas ocultas, a indentação das partitions M e os
ajustes de `subTitle`/`showAxisTitle`/`drillFilterOtherVisuals`. Melhor validação possível — o
próprio Desktop concordou com cada escolha ao regravar.

### Contagem de linhas — nenhuma linha descartada

Consulta DAX no modelo vivo contra a contagem dos CSVs:

| Tabela | CSV | Modelo | |
|---|---|---|---|
| fVendas | 96.443 | 96.443 | OK |
| fEmbarques | 28.465 | 28.465 | OK |
| fRecebimentos | 28.465 | 28.465 | OK |
| fCambio | 11.711 | 11.711 | OK |
| fForecast | 11.514 | 11.514 | OK |
| fOrcamento | 4.014 | 4.014 | OK |
| fMetas | 768 | 768 | OK |
| dCalendario | 1.673 | 1.673 | OK |
| dCliente / dProduto / dPais / dVendedor / dPorto / dTransportadora | 330 / 106 / 28 / 20 / 49 / 13 | idem | OK |

As 14 tabelas batem exatamente com a origem — confirma que a troca de
`Table.RemoveRowsWithErrors` por `Table.ReplaceErrorValues` resolveu o risco apontado no handoff.

> Observação: o handoff fala em "~24k embarques" e "24,6k pedidos". Os dois números estão
> **errados**. O `ValidacaoDados.md`, gerado a partir dos CSVs, registra 29.210 pedidos, e o
> arquivo `fEmbarques.csv` tem 28.465 linhas. O modelo bate com os dois.

### Medidas conferidas contra `ValidacaoDados.md`

| Indicador | Documentação | Modelo | |
|---|---|---|---|
| Receita líquida | ~US$ 448M | US$ 447.580.156,66 | OK |
| Margem bruta | 25,6% | 25,605% | OK |
| Top 10 clientes | 32,3% | 32,305% | OK |
| % embarques atrasados | 16,57% | 16,572% | OK |
| Entregas realizadas | 27.697 | 27.697 | OK |
| Pedidos | 29.210 | 29.210 | OK |
| Saldo em aberto | US$ 28.314.979,06 | US$ 28.314.979,06 | OK |
| Inadimplência | 0,82% | 2,50% | **divergente — ver abaixo** |

16 medidas complexas (CAGR, Pareto Top 1/20, Novos/Perdidos/Em Risco, Receita em Risco, Share of
Wallet, Projeção, Forecast, Prazo Médio, os `TOPN`+`CONCATENATEX` e os textos dinâmicos) foram
avaliadas e retornam valores plausíveis, sem erro de compilação.

### Inadimplência: a medida está certa, a documentação é que subestima

`Saldo Vencido` inclui `Status IN {"Vencido", "Parcial"}`, enquanto o `ValidacaoDados.md` contou
apenas `Vencido`. Testei se a inclusão do "Parcial" se justifica:

| | Saldo |
|---|---|
| Parcial **já vencido** | US$ 7.305.264,53 |
| Parcial **a vencer** | US$ 0,00 |
| "Em aberto" já vencido | US$ 0,00 |

Todo o saldo "Parcial" está vencido, e nenhum "Em aberto" venceu. Logo **2,50% é o número
correto** e os 0,82% da documentação ignoram o saldo vencido de títulos parcialmente pagos.
Nenhuma alteração feita na medida; corrigir é caso de atualizar o texto do `ValidacaoDados.md`.
(O 1,56% citado no handoff não corresponde a nenhuma das duas definições — provavelmente é
resíduo de uma geração de dados anterior.)

### Bug encontrado pela renderização: `filledMap` com a medida em Latitude

O mapa preenchido da p01 tinha `Receita USD` no well **`Y`**, que em `filledMap` é a role
**Latitude** — por isso o painel de campos mostrava "Latitude: Receita USD" e o mapa não pintava
nada. O well correto para saturação de cor é **`Gradient`**. Corrigido em `build_report.py`.
O `map` da p06 já estava certo (`Size`).

O auditor de visuais não pegou isso porque a tabela de wells esperados não cobria `map`,
`filledMap`, `treemap` e `pivotTable`. Tabela ampliada.

### `MapVisualNotEnabled` — não é problema do arquivo

Os 2 visuais de mapa dependem da configuração de locatário "Visuais de mapa e mapa preenchido"
(Portal de administração → Configurações do locatário). Nada no PBIP resolve isso.

---

## 5. O que continua em aberto

1. **Abrir no Power BI Desktop.** Nada aqui substitui isso — segue sendo o passo bloqueante.
2. **Python não está instalado** nesta máquina (a pasta `Python311` só tem restos de um `Lib`).
   Consequências: `validate_pbip.py`, `validate_data.py` e `gen_docs.py` não rodaram, e os edits
   feitos em `build_model.py`/`build_report.py` **não passaram por verificação de sintaxe**.
   Os dois scripts foram editados de forma coerente com os artefatos, mas quem regerar deve
   primeiro instalar Python 3.12 + pandas/numpy e rodar `validate_pbip.py`.
3. **Contagem de linhas por tabela após o refresh** — comparar com `ValidacaoDados.md`,
   especialmente `fEmbarques` (~24k), agora que os erros viram `null` em vez de descartar linha.
4. **Revisão visual das 11 páginas** — nunca foram renderizadas.
5. **`pageNavigator`** — mantido. Se o Desktop recusar, cair para `actionButton` com
   `visualLink`, como previsto no handoff.
6. **Query groups** — `01 Dimensoes`, `02 Fatos` e `90 Auxiliares` estão declarados em
   `model.tmdl` mas nenhuma tabela os referencia (só `pBasePath` usa `00 Parametros`). Ligar as
   partitions aos grupos é melhoria pós-abertura; não mexi para não introduzir propriedade não
   verificada antes do primeiro carregamento bem-sucedido.
7. **Backup pré-correção** em `backups\PowerBI_pre-ajuste_20260817\`, com cópia dos dois scripts
   como estavam antes.
