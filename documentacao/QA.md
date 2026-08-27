# QA — Aurora Brasil Exportadora S.A.

> **Atualização 17/08/2026 (sessão Claude Code):** o QA abaixo descreve o estado anterior às
> correções de formato. Seis bloqueadores foram corrigidos desde então — inclusive dois que este
> QA não detectava (indentação mista nas partitions M e descrições `///` fora de lugar no TMDL).
> Ver `CorrecoesPBIP.md` para o registro completo e para as verificações que substituíram
> `validate_pbip.py` nesta máquina (sem Python instalado).

Registro dos testes executados sobre os dados e sobre o projeto PBIP, com o resultado real da
última execução (17/08/2026).

## 1. QA dos dados (`scripts/validate_data.py`)

Executa de forma independente do gerador — lê apenas os CSVs finais.

- **Unicidade de chaves primárias**: OK em todas as 10 tabelas com PK definida.
- **Integridade referencial**: OK nas 11 relações FK→PK verificadas (fVendas, fEmbarques,
  fRecebimentos, fMetas contra suas dimensões).
- **Consistência financeira** (linha a linha, 96.443 registros de fVendas):
  - Receita Bruta = Quantidade × Preço — erro máximo **0,0000 USD**
  - Receita Líquida = Bruta − Desconto — erro máximo **0,0000 USD**
  - Custo Total = Produto + Frete + Seguro + Despesas — erro máximo **0,0000 USD**
  - Margem = Receita Líquida − Custo Total — erro máximo **0,0000 USD**
- **Coerência temporal**: faturamento sempre ≥ pedido; entrega real sempre ≥ embarque real.
- **Resultado: APROVADO.**

## 2. QA do modelo semântico e do relatório (`scripts/validate_pbip.py`)

| Verificação | Resultado |
|---|---|
| Arquivos obrigatórios (.pbip, .pbism, .pbir, TMDL, report.json) | OK |
| Sintaxe de todos os arquivos JSON do projeto | OK — 203 arquivos |
| Referências de coluna usadas no DAX existem no modelo | OK — 0 inválidas |
| Referências de medida usadas no DAX existem na tabela `_Medidas` | OK — 0 inválidas |
| Todas as medidas têm `displayFolder` | OK — 159/159 |
| Relacionamentos referenciam colunas existentes | OK — 21/21 |
| Nenhum relacionamento bidirecional | OK |
| `pages.json` coerente com as pastas de página em disco | OK — 17/17 |
| Visuais sem sobreposição de bounding box | OK — 0 conflitos |
| Visuais dentro dos limites da página (1280×720 ou tooltip) | OK — 180/180 |
| Tema customizado registrado e referenciado em `report.json` | OK |
| `definition.pbir` aponta para o Semantic Model correto | OK |
| Parâmetro `pBasePath` declarado como `IsParameterQuery=true` | OK |
| Queries de dados usando `pBasePath` | OK — 14/14 |

**Avisos (não bloqueantes):** os 4 visuais de tabela dentro das páginas de tooltip (Cliente,
Produto, País, Vendedor) não têm título próprio — decisão intencional, pois cada tooltip já tem
um textbox de cabeçalho cumprindo esse papel visualmente.

**Resultado: 20 verificações OK, 4 avisos intencionais, 0 erros.**

## 3. QA de DAX (amostras manuais)

- `Receita Bruta USD − Descontos USD = Receita USD` — validado contra `SUM` direto da tabela.
- `Receita USD − Custo Total USD = Margem Bruta USD` — validado.
- Medidas de time intelligence (`Receita LY`, `Receita YTD`, `Receita Rolling 12M`) testadas
  contra filtro de Ano/Mês variando o contexto de `dCalendario`.
- `USERELATIONSHIP` verificado nas 4 medidas que usam datas alternativas (`Receita por Data de
  Pedido` e as medidas de aging que dependem de `DataVencimento`/`DataPagamento`).
- RFV, Pareto/ABC, Churn, Cohort (via `Data Primeira Compra`), Share of Wallet e OTIF testados
  contra os valores apurados diretamente em pandas na análise exploratória (ver
  `InsightsEncontrados.md`) — sem divergência.

## 4. QA visual (estrutural, não renderizado)

- Grid 1280×720 respeitado em todas as páginas normais; tooltips em 320×260–300.
- Nenhum visual menor que 60×24px.
- Cabeçalho, navegação lateral e slicers posicionados de forma consistente entre páginas.
- Paleta de cores validada contra os tokens do design system (sem cor fora do tema nos gráficos
  principais).

**Limitação conhecida:** este QA é estrutural — verifica JSON/TMDL válidos, referências
corretas e ausência de sobreposição geométrica. **O Power BI Desktop não pôde ser aberto neste
ambiente de geração**, portanto não houve renderização visual real nem captura de tela para
revisão humana. Recomenda-se, ao abrir o arquivo pela primeira vez, uma passada visual rápida
pelas 11 páginas antes de apresentar à diretoria.

## 5. Checklist final (item 87 da especificação)

| Item | Status |
|---|---|
| PBIP existe | ✅ |
| SemanticModel existe | ✅ |
| Report existe | ✅ |
| TMDL válido | ✅ |
| PBIR válido | ✅ |
| Power Query válido (estrutura M revisada) | ✅ |
| Dados carregam (validado apenas estruturalmente, não em runtime) | ⚠️ ver limitação acima |
| Relacionamentos válidos | ✅ |
| Modelo estrela | ✅ |
| Calendário configurado (dataCategory Time, coluna chave) | ✅ |
| Medidas DAX (sintaxe e referências) | ✅ |
| Time intelligence, Metas, RFV, Pareto, Churn, Potencial, Logística, Financeiro, Forecast | ✅ implementadas em DAX |
| Páginas, tooltips, drill-through, navegação, tema | ✅ |
| Documentação completa | ✅ |
| Caminhos documentados (`pBasePath`) | ✅ |
| Projeto armazenado em `E:\Projetos BI\02 - Aurora Exportação\` | ⚠️ ver pendência abaixo |
| Projeto abre corretamente no Power BI Desktop | ⚠️ não testado neste ambiente |

**Pendência real:** a entrega foi empacotada em ZIP para download, pois este ambiente não tem
acesso ao sistema de arquivos Windows do usuário. A abertura efetiva no Power BI Desktop (leitura
runtime do XMLA local, carregamento de dados, renderização de visuais) precisa ser confirmada
pelo usuário após extrair o pacote no caminho indicado.
