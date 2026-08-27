# Aurora Brasil Exportadora S.A. — Projeto Power BI

## A empresa (fictícia)

**Aurora Brasil Exportadora S.A.** é uma exportadora brasileira B2B de alimentos e produtos
naturais premium, fundada em 2011 em Campinas/SP, com centro logístico em Santos/SP. Atua nas
categorias Café, Cacau, Castanhas, Açaí, Frutas Processadas, Mel, Produtos Naturais e
Ingredientes Alimentícios, atendendo cerca de 330 clientes ativos e potenciais em 28 países,
distribuídos entre América do Norte, América Latina, Europa, Oriente Médio, Ásia e Oceania.

A empresa emprega cerca de 140 colaboradores, dos quais 20 na área comercial internacional
(estrutura Diretor Comercial → Gerentes Regionais → Executivos de Contas). Seu posicionamento é
de fornecedor premium com rastreabilidade de origem e certificações (Orgânico, Fair Trade,
Rainforest Alliance, Kosher, Halal, BRCGS), competindo por qualidade e relacionamento de longo
prazo, não por preço. A estratégia comercial combina carteira direta em mercados maduros
(Alemanha, Estados Unidos, Reino Unido) com tradings parceiras em mercados emergentes (Coreia do
Sul, Oriente Médio), e os canais de venda incluem venda direta, representantes locais, tradings
parceiras, e-commerce B2B e feiras internacionais. Essa narrativa é uma construção sintética para
fins de demonstração analítica — todos os dados, clientes, produtos e pessoas são fictícios.

## Objetivo do projeto

Simular uma operação de exportação real o suficiente para sustentar um dashboard executivo
completo, com histórico coerente (matemática financeira exata, sazonalidade, tendências, ruído e
padrões deliberadamente implantados) e um produto Power BI funcional construído sobre essa base:
Power Query → Modelo Dimensional → DAX → Storytelling visual.

## Arquitetura da entrega

```
02 - Aurora Exportação\
├── dados\                          14 arquivos CSV (fonte do modelo)
├── PowerBI\
│   ├── AuroraBrasilExportadora.pbip
│   ├── AuroraBrasilExportadora.SemanticModel\   (TMDL)
│   └── AuroraBrasilExportadora.Report\          (PBIR)
├── documentacao\                   Este README e os demais .md
├── scripts\                        Geradores Python (reprodutíveis)
└── backups\
```

## Como abrir

1. Extraia o ZIP entregue de forma que a pasta final seja exatamente
   `E:\Projetos BI\02 - Aurora Exportação\` (com as subpastas `dados`, `PowerBI`,
   `documentacao`, `scripts`, `backups` dentro dela).
2. Abra `PowerBI\AuroraBrasilExportadora.pbip` no Power BI Desktop (versão de 2024 em diante, com
   suporte a PBIP/PBIR habilitado em Opções > Funcionalidades em versão prévia).
3. Na primeira abertura, o Power BI vai pedir para confirmar o parâmetro `pBasePath`. Ele já vem
   configurado como `E:\Projetos BI\02 - Aurora Exportação\dados\`. Se você extraiu em outro
   caminho, veja "Como alterar o caminho" abaixo.
4. Atualize os dados (Página Inicial > Atualizar).

## Como alterar o caminho dos dados

Todas as 14 consultas usam um único parâmetro. Para apontar o projeto para outra pasta:

1. Página Inicial > Transformar Dados > Editor poder query > Gerenciar Parâmetros.
2. Selecione `pBasePath` e informe o novo caminho, **terminando com barra invertida**, por
   exemplo `E:\Projetos BI\02 - Aurora Exportação\dados\`.
3. Feche e aplique, depois atualize.

Nenhuma query individual precisa ser editada — este é o propósito do parâmetro.

## Como atualizar os dados

Os CSVs são estáticos (gerados uma vez com seed fixa). Para gerar uma nova versão da base,
execute `scripts\generate_data.py` com Python 3.11+ e as bibliotecas `pandas` e `numpy`
instaladas. A seed `20260816` garante que o resultado é sempre idêntico ao entregue; para gerar
uma base diferente, altere a constante `SEED` no topo do script.

## Dependências

- Power BI Desktop com suporte a PBIP/PBIR (dezembro de 2023 ou mais recente; recomendado a
  versão mais atual disponível em 2026).
- Para regenerar dados ou reconstruir o TMDL/PBIR: Python 3.11+, `pandas`, `numpy` (o `Faker`
  não é necessário — os nomes fictícios são gerados por combinatória própria).

## Versão do projeto

Versão 1.0 — gerado em 17/08/2026, seed `20260816`. Ver `ValidacaoDados.md` para o relatório
completo de integridade e `QA.md` para o resultado da auditoria estrutural do PBIP.

## Mapa da documentação

| Arquivo | Conteúdo |
|---|---|
| `DicionarioDados.md` | Toda coluna de toda tabela, com tipo, descrição, exemplo e regra |
| `ModeloDados.md` | Tabelas, granularidade, relacionamentos, chaves ocultas |
| `RegrasNegocio.md` | Regras comerciais, financeiras e logísticas por trás dos números |
| `InsightsOcultos.md` | Os ≥20 padrões implantados deliberadamente na geração da base |
| `InsightsEncontrados.md` | Os mesmos padrões, descobertos analiticamente a partir do modelo pronto |
| `ValidacaoDados.md` | Relatório de integridade referencial e consistência financeira |
| `MedidasDAX.md` | As 159 medidas, fórmula completa, formato e dependências |
| `PowerQuery.md` | Parâmetro, grupos de consulta, padrão de transformação |
| `DashboardPages.md` | As 17 páginas do relatório, com os visuais de cada uma |
| `QA.md` | Auditoria estrutural do PBIP (modelo, DAX, layout) |
| `MedidasPowerBI.md` | Sugestões de medidas por área (documento de especificação original) |
| `DashboardBlueprint.md` | Proposta de páginas por área (documento de especificação original) |
