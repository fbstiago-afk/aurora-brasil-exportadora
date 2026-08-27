# Power Query — Aurora Brasil Exportadora S.A.

## Parametro

```m
pBasePath  //  Texto, obrigatorio
Exemplo: "G:\Meu Drive\Aurora Brasil Exportadora\dados\"
```

Todas as 14 queries de dados derivam o caminho desse unico parametro. Para mover o projeto basta alterar `pBasePath` em *Transformar dados > Gerenciar parametros* — nenhuma query precisa ser editada.

## Grupos de query

| Grupo | Queries |
|---|---|
| 00 Parametros | pBasePath |
| 01 Dimensoes | dCalendario, dCliente, dProduto, dVendedor, dPais, dPorto, dTransportadora |
| 02 Fatos | fVendas, fEmbarques, fCambio, fMetas, fOrcamento, fForecast, fRecebimentos |
| 90 Auxiliares | _Medidas (tabela tecnica gerada em memoria) |

## Padrao de transformacao

Cada query segue exatamente quatro etapas nomeadas, sem passos redundantes:

```m
let
    Origem = Csv.Document(File.Contents(pBasePath & "fVendas.csv"),
        [Delimiter = ";", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    CabecalhoPromovido = Table.PromoteHeaders(Origem, [PromoteAllScalars = true]),
    TiposAplicados = Table.TransformColumnTypes(CabecalhoPromovido, {...}, "pt-BR"),
    ErrosRemovidos = Table.RemoveRowsWithErrors(TiposAplicados)
in
    ErrosRemovidos
```

**Decisoes tecnicas**

- `Encoding = 65001` (UTF-8) porque os CSVs contem acentos e nomes internacionais.
- Cultura `pt-BR` no `TransformColumnTypes` porque os arquivos usam `;` como separador e `,` como decimal — padrao que abre corretamente no Excel brasileiro.
- `Table.RemoveRowsWithErrors` como rede de seguranca; na base validada nenhuma linha e descartada.
- Nenhum calculo financeiro e feito em Power Query: tudo o que depende de contexto de filtro vive em DAX. As colunas calculadas foram deliberadamente evitadas.
- Nenhum merge: as chaves ja vem resolvidas do gerador, o que preserva a compressao do VertiPaq e evita expandir a fato.

## Alternativa de fonte

Se no futuro os arquivos forem para o Google Sheets, o conector `Web.Contents` com a URL de exportacao CSV da planilha substitui apenas a etapa `Origem`; o restante das queries permanece identico. A pasta local sincronizada foi escolhida por permitir refresh no Power BI Desktop sem autenticacao OAuth e por manter o gateway simples em publicacoes futuras.
