#!/usr/bin/perl
# Gera o .dax do guia de analise: uma medida que devolve o HTML inteiro.
#
# Conteudo: lista em <details>/<summary> (HTML nativo, sem JS) - um item por
# pagina, clique expande so aquele item.
#
# Capa: botao fixo no canto do visual. O painel com a lista completa aparece
# por HOVER (":hover .panel"), abrindo para a DIREITA do botao - nao precisa
# de checkbox, e puro CSS :hover, no mesmo padrao do "Card Fluxo HTML" do
# usuario. O container do painel fica SEM fundo proprio; so os <details>
# internos tem fundo (transparencia so no container, cor so nos itens).
use strict; use warnings;
use utf8;
binmode(STDOUT, ':encoding(UTF-8)');

my $OUT = shift or die "uso: gen_guia.pl <pasta scripts/html>\n";

# --------------------------------------------------------------- conteudo
# [id, titulo, pergunta-guia, [ [visual, o-que-analisar], ... ] ]
my @PAG = (
 ['01','Executive Overview','Estamos crescendo, atingindo meta e preservando rentabilidade?', [
   ['Painel de 8 KPIs','Leitura de 3 segundos. As barras de 12 meses mostram se o número atual é ponto fora da curva ou tendência. A barra de Atingimento tem marca nos 100%: à esquerda dela, o ano está em risco.'],
   ['Receita mensal: realizado x ano anterior x meta','Compare as três linhas. Realizado acima do ano anterior mas abaixo da meta significa que a meta subiu mais rápido que a operação.'],
   ['Receita por mercado (mapa)','Concentração geográfica. Poucos países escuros = risco de dependência.'],
   ['De onde veio a variação YoY (cascata)','Atribui o crescimento por continente. Serve para responder "crescemos por quê" — não é o mesmo que "onde vendemos mais".'],
   ['Destaques por mercado','Cruza crescimento, margem e atingimento. Procure linhas com receita alta e margem baixa.'],
 ]],
 ['02','Sales Performance','O ritmo comercial está acima ou abaixo do compromisso assumido?', [
   ['Realizado mensal e atingimento acumulado','A coluna é o mês, a linha é o acumulado. A linha cruzando 100% no meio do ano indica meta subdimensionada.'],
   ['Região comercial: realizado x meta','Barras pareadas. Região que bate meta com receita pequena pode ter meta frouxa.'],
   ['Receita por executivo comercial','Ranking. Passe o mouse para ver a ficha do vendedor.'],
   ['Decomposição por canal e categoria','A coluna Contribuição para Crescimento mostra quanto cada combinação puxou o total — não confunda com crescimento próprio.'],
 ]],
 ['03','Customers','Quem sustenta a receita, quem está escapando e quanto isso custa?', [
   ['Pareto de clientes','Barras por cliente e linha do acumulado. Onde a linha cruza 80% está sua dependência real.'],
   ['Distribuição RFV da carteira','Campeões, Leais, Em Risco, Hibernando, Perdidos. Blocos grandes em Em Risco e Hibernando são receita ainda recuperável.'],
   ['Receita por classe ABC','Concentração por valor. Compare com o RFV: classe A em situação Em Risco é a combinação mais cara.'],
   ['Clientes ativos por porte','Série temporal por porte. Queda em um porte específico aponta problema de proposta, não de mercado.'],
   ['Carteira detalhada','Ordene por Recência para achar risco: recência alta com receita alta é conta escapando.'],
 ]],
 ['04','Customer Potential','Onde existe receita não capturada e qual conta merece prioridade?', [
   ['Receita x Share of Wallet (dispersão)','O tamanho da bolha é o potencial. Bolha grande à esquerda = muito potencial, pouca penetração. É a região de maior retorno.'],
   ['Ranking de oportunidade','O Score de Oportunidade pondera gap absoluto contra baixa penetração — prioriza quem tem espaço e ainda não foi trabalhado.'],
   ['White space por segmento','Categorias que o segmento poderia comprar e não compra. Cruze com Penetração de Categorias.'],
   ['Penetração por categoria','Quantos clientes compram cada categoria. Categoria com poucos compradores e margem boa é candidata a cross-sell.'],
 ]],
 ['05','Products','Qual portfólio cresce com rentabilidade e qual cresce destruindo margem?', [
   ['Matriz BCG adaptada','Crescimento no eixo x, margem no y, tamanho = receita. O quadrante inferior direito — cresce muito, margem baixa — é o que merece revisão de preço.'],
   ['Receita e margem por categoria','Barras pareadas. Categoria com receita alta e margem em valor baixa está sendo vendida barato demais.'],
   ['Evolução da margem por categoria','Tendência. Margem caindo de forma consistente indica erosão de preço, não sazonalidade.'],
   ['Portfólio por SKU','Classe ABC e margem por quilo. Margem/kg é o indicador mais honesto num negócio de exportação por peso.'],
 ]],
 ['06','Markets','Quais mercados sustentam hoje e quais sustentarão os próximos anos?', [
   ['Market Opportunity Matrix','Crescimento x margem por país. O canto superior direito é onde investir; o inferior esquerdo, onde revisar a operação.'],
   ['Distribuição global (mapa)','Leitura geográfica da concentração.'],
   ['Ranking de mercados','Ordem por receita. Passe o mouse para OTIF, lead time e frete do país.'],
   ['Mercado x categoria','Cruza continente e categoria com lead time. Combinação de margem boa e lead time alto é candidata a revisar logística, não preço.'],
 ]],
 ['07','Profitability','Entre a receita bruta e a margem, onde o valor está sendo consumido?', [
   ['Ponte econômica detalhada','Da receita bruta à margem, coluna a coluna: descontos, custo de produto, frete, seguro, despesas. É o mapa completo do consumo de valor.'],
   ['Formação da margem por categoria (cascata)','Quanto cada categoria adiciona ou subtrai da margem total.'],
   ['Cliente: receita x margem','Dispersão. Clientes grandes e de margem baixa aparecem à direita e embaixo — são os que mais pesam na média.'],
   ['Rentabilidade por vendedor e Incoterm','Frete % Receita e Desconto % lado a lado revelam se a margem cai por concessão comercial ou por estrutura logística.'],
 ]],
 ['08','Logistics','Onde a operação perde prazo e quanto isso custa por quilo?', [
   ['Painel com OTIF','A barra de OTIF tem marca nos 90%. Abaixo disso, o problema é sistêmico, não pontual.'],
   ['Lead time real x previsto','Duas linhas. Gap constante significa previsão mal calibrada; gap crescente significa degradação real.'],
   ['Motivos de atraso','Pareto dos motivos. Concentre esforço nos dois primeiros.'],
   ['Rotas com maior incidência','Percentual de atraso por país de destino. Cruze com o volume: 40% de atraso numa rota pequena importa menos.'],
   ['Performance por transportadora','OTIF por operador. Base de renegociação contratual.'],
   ['Modal e porto de origem','Frete por quilo por combinação. Modal aéreo com frete/kg fora da curva pode indicar uso emergencial.'],
 ]],
 ['09','Sales Team','Quem entrega, quem depende de um único cliente e quem precisa de apoio?', [
   ['Quadrante: crescimento x atingimento','Cresce e bate meta (manter), cresce e não bate (meta agressiva), não cresce e bate (meta frouxa), nenhum dos dois (agir).'],
   ['Realizado x meta por vendedor','Barras pareadas para a leitura direta do gap.'],
   ['Dependência do maior cliente','Risco de carteira. Acima de 40% num único cliente, a saída dele derruba o vendedor — e o número não aparece em nenhum outro visual.'],
   ['Ranking comercial','Consolidado com gap e clientes ativos.'],
 ]],
 ['10','Finance','Quanto do faturamento ainda não virou caixa e qual cliente trava o ciclo?', [
   ['Aging da carteira','Faixas de vencimento. O peso nas faixas acima de 90 dias é o que dificilmente se recupera.'],
   ['Situação dos títulos','Pago, Pago em atraso, Parcial, Vencido, Em aberto. "Pago em atraso" não é inadimplência, mas é custo de capital de giro.'],
   ['Saldo vencido por forma de pagamento','Identifica se a inadimplência está concentrada num instrumento — o que é problema de política, não de cliente.'],
   ['Principais devedores','Dias médios de atraso e prazo médio por conta. Cruze com a página Customers: devedor que também é Campeão RFV pede negociação, não cobrança.'],
 ]],
 ['11','Forecast e Budget','Se a tendência continuar, fechamos o ano acima ou abaixo do compromisso?', [
   ['Linha temporal: realizado, orçado, forecast e meta','Quatro séries. O ponto onde forecast e meta divergem é a data em que a decisão precisa ser tomada.'],
   ['Peso histórico de cada mês','Sazonalidade. Base para julgar se um mês fraco é problema ou calendário.'],
   ['Realizado x orçado x forecast por região','Actual vs Budget por região e categoria, para saber onde o desvio se origina.'],
 ]],
);

my @EXTRA = (
 ['Dicas de ferramenta','4 páginas de tooltip em HTML, acionadas ao passar o mouse',
  'Cliente, Produto, Mercado e Vendedor. Cada uma traz identificação, 4 KPIs, barras de 12 meses e duas comparações específicas — margem alvo no produto, concentração de carteira no vendedor, OTIF no mercado. Escolha ditada pela dimensão que o visual agrupa, não pela página.'],
 ['Detalhe Cliente e Detalhe Mercado','Páginas de drill-through, botão direito sobre o item',
  'Dossiê de página inteira do item selecionado: KPIs, histórico mensal, mix e detalhe tabular. O botão Voltar retorna à página de origem exata. Use quando a pergunta deixa de ser "como isso se compara" e vira "o que está acontecendo aqui".'],
);

# ====================================================================
# Duas variantes, mesmo conteudo:
#   guia_analise.dax         -> CAPA: botao no canto, painel por hover para a
#                               direita, paleta clara p/ fundo escuro.
#   guia_analise_pagina.dax  -> ABA:  ocupa a pagina inteira, sem botao,
#                               paleta escura sobre fundo claro (1a versao).
# ====================================================================

# --- CSS comum a lista em accordion, parametrizado por paleta -----------
sub css_lista {
    my (%c) = @_;
    return <<"CSS";
.gh{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;
    border-left:4px solid #C8763C;padding:2px 0 2px 11px;margin-bottom:6px}
.gh h1{font-size:$c{h1};font-weight:700;color:$c{titulo};letter-spacing:-.01em$c{sombraH1}}
.gh span{font-size:$c{peq};color:$c{fraco}}
.hint{font-size:$c{med};color:$c{corpo};margin:0 0 13px 15px}
.hint b{color:$c{titulo}}
details{background:$c{cardBg};border:1px solid $c{cardBorda};
        border-radius:9px;margin-bottom:8px;overflow:hidden$c{cardSombra}}
details[open]{background:$c{cardBgOpen};border-color:$c{cardBordaOpen}}
summary{cursor:pointer;list-style:none;padding:$c{padSum};
        display:flex;align-items:baseline;gap:11px;user-select:none}
summary::-webkit-details-marker{display:none}
summary::after{content:'+';margin-left:auto;font-size:$c{sinal};color:$c{acento};
               font-weight:700;line-height:1}
details[open] summary::after{content:'–'}
summary:hover{background:$c{hover}}
.num{font-size:$c{peq};font-weight:700;letter-spacing:.05em;color:#FFF;
     background:$c{numBg};border-radius:4px;padding:2px 7px;flex:none}
details[open] .num{background:$c{acento}}
.tit{font-size:$c{tit};font-weight:700;color:$c{titulo};flex:none}
.q{font-size:$c{med};color:$c{fraco};font-style:italic;
   overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.body{padding:2px $c{padBody};display:flex;flex-direction:column;gap:$c{gapBody}}
.v{display:grid;grid-template-columns:$c{colV} 1fr;gap:$c{gapV};align-items:baseline}
.v em{font-style:normal;font-size:$c{txt};font-weight:600;color:$c{rotulo}}
.v p{font-size:$c{txt};color:$c{corpo};line-height:1.55}
.sep{font-size:$c{peq};letter-spacing:.08em;text-transform:uppercase;
     color:$c{fraco};font-weight:700;margin:15px 0 7px 2px}
.x{background:$c{xBg};border:1px solid $c{cardBorda};
   border-left:4px solid #C8763C;border-radius:8px;
   padding:$c{padX};margin-bottom:8px$c{cardSombra}}
.x .tit{display:block;margin-bottom:3px}
.x .how{font-size:$c{peq};color:$c{fraco};margin-bottom:6px}
.x p{font-size:$c{txt};color:$c{corpo};line-height:1.55}
CSS
}

# --- paleta CLARA (para fundo escuro) — usada na capa -------------------
my %CLARA = (
    h1=>'clamp(20px,1.5vw,30px)', tit=>'clamp(14px,1.05vw,19px)',
    med=>'clamp(12px,.9vw,16px)', peq=>'clamp(11px,.85vw,15px)',
    txt=>'clamp(12.5px,.95vw,17px)', sinal=>'clamp(16px,1.2vw,23px)',
    padSum=>'clamp(10px,.75vw,15px) clamp(13px,1vw,18px)',
    padBody=>'clamp(14px,1.05vw,19px) clamp(13px,1vw,18px)',
    padX=>'clamp(11px,.85vw,16px) clamp(13px,1vw,18px)',
    gapBody=>'clamp(9px,.7vw,14px)', gapV=>'clamp(13px,1vw,20px)',
    colV=>'clamp(180px,17vw,260px)',
    titulo=>'#F2F7F8', corpo=>'#C7D5DA', fraco=>'#9FBCC4',
    rotulo=>'#E8A877', acento=>'#E08D4F', numBg=>'#C8763C',
    cardBg=>'rgba(14,42,51,.88)', cardBgOpen=>'rgba(14,42,51,.96)',
    cardBorda=>'rgba(159,188,196,.3)', cardBordaOpen=>'rgba(200,118,60,.62)',
    hover=>'rgba(200,118,60,.16)', xBg=>'rgba(23,73,90,.72)',
    cardSombra=>';box-shadow:0 3px 12px rgba(0,0,0,.3)',
    sombraH1=>';text-shadow:0 1px 4px rgba(0,0,0,.5)',
);

# --- paleta ESCURA (para fundo claro) — a 1a versao, usada na aba -------
my %ESCURA = (
    h1=>'19px', tit=>'13px', med=>'11.5px', peq=>'10px', txt=>'11.5px', sinal=>'15px',
    padSum=>'9px 13px', padBody=>'13px 12px', padX=>'10px 13px',
    gapBody=>'8px', gapV=>'12px', colV=>'200px',
    titulo=>'#0E2A33', corpo=>'#5D6E75', fraco=>'#8C96A5',
    rotulo=>'#17495A', acento=>'#C8763C', numBg=>'#0E2A33',
    cardBg=>'rgba(255,255,255,.66)', cardBgOpen=>'rgba(255,255,255,.82)',
    cardBorda=>'rgba(227,224,217,.85)', cardBordaOpen=>'rgba(200,118,60,.45)',
    hover=>'rgba(200,118,60,.07)', xBg=>'rgba(23,73,90,.06)',
    cardSombra=>'', sombraH1=>'',
);

# --- o conteudo (identico nas duas) -------------------------------------
sub esc { my $s = shift; $s =~ s/"/""/g; return $s }

sub blocos_conteudo {
    my @b;
    push @b, "<div class='gh'><h1>Guia de análise</h1><span>"
           . esc('11 páginas · 4 dicas de ferramenta · 2 dossiês') . "</span></div>";
    push @b, "<div class='hint'>Clique em qualquer página para <b>expandir</b> o detalhe dos visuais e o que cada um permite analisar.</div>";
    for my $p (@PAG) {
        my ($id, $tit, $q, $vis) = @$p;
        my $h = "<details><summary><span class='num'>$id</span><span class='tit'>"
              . esc($tit) . "</span><span class='q'>" . esc($q) . "</span></summary><div class='body'>";
        $h .= "<div class='v'><em>" . esc($_->[0]) . "</em><p>" . esc($_->[1]) . "</p></div>" for @$vis;
        push @b, $h . "</div></details>";
    }
    push @b, "<div class='sep'>Além das páginas</div>";
    for my $e (@EXTRA) {
        push @b, "<div class='x'><span class='tit'>" . esc($e->[0])
               . "</span><div class='how'>" . esc($e->[1]) . "</div><p>" . esc($e->[2]) . "</p></div>";
    }
    return @b;
}

sub monta_dax {
    my ($css, $abre, $fecha) = @_;
    my @out = ("\"$abre\"");
    push @out, "        & \"$_\"" for blocos_conteudo();
    push @out, "        & \"$fecha\"";
    return "VAR _css = \"<style>\n" . $css . "</style>\"\n\nVAR _html =\n    _css\n        & "
         . substr($out[0], 0) . "\n" . join("\n", @out[1..$#out])
         . "\nRETURN\n    _html\n";
}

# ---------------------------------------------------------------- capa
my $css_capa = <<'CSS' . css_lista(%CLARA);
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:transparent}
.g{position:relative;height:100%;font-family:'Segoe UI',system-ui,sans-serif}
.hoverArea{position:absolute;top:6px;left:6px;z-index:20}
.trigger{display:inline-flex;align-items:center;gap:7px;
  padding:clamp(8px,.62vw,12px) clamp(15px,1.15vw,22px);border-radius:99px;
  background:#C8763C;color:#FFF;font-size:clamp(12.5px,.95vw,17px);font-weight:700;
  letter-spacing:.02em;cursor:pointer;user-select:none;
  box-shadow:0 3px 12px rgba(0,0,0,.45);
  transition:background .2s ease,transform .2s ease;white-space:nowrap}
.hoverArea:hover .trigger{background:#E08D4F;transform:scale(1.04)}
.panel{position:absolute;top:0;left:calc(100% + 12px);
  width:clamp(560px,62vw,900px);max-height:min(640px,calc(100vh - 24px));
  background:transparent;overflow-y:auto;padding-right:4px;
  opacity:0;transform:translateX(-14px);pointer-events:none;
  transition:opacity .18s ease,transform .18s ease}
.hoverArea:hover .panel{opacity:1;transform:translateX(0);pointer-events:auto}
.panel::-webkit-scrollbar{width:8px}
.panel::-webkit-scrollbar-thumb{background:rgba(200,118,60,.5);border-radius:99px}
CSS

open(my $o1, '>:encoding(UTF-8)', "$OUT/guia_analise.dax") or die $!;
print $o1 monta_dax($css_capa,
    "<div class='g'><div class='hoverArea'><div class='trigger'>&#128214; Guia de Análise</div><div class='panel'>",
    "</div></div></div>");
close $o1;

# ---------------------------------------------------------------- aba
my $css_pagina = <<'CSS' . css_lista(%ESCURA);
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:transparent}
.g{height:100%;overflow-y:auto;font-family:'Segoe UI',system-ui,sans-serif;
   color:#16262C;padding:2px 6px 10px 2px}
.g::-webkit-scrollbar{width:7px}
.g::-webkit-scrollbar-thumb{background:rgba(14,42,51,.22);border-radius:99px}
CSS

open(my $o2, '>:encoding(UTF-8)', "$OUT/guia_analise_pagina.dax") or die $!;
print $o2 monta_dax($css_pagina, "<div class='g'>", "</div>");
close $o2;

printf "guia_analise.dax         capa  (botao + hover p/ direita, fonte clara)\n";
printf "guia_analise_pagina.dax  aba   (pagina inteira, 1a versao)\n";
printf "%d paginas, %d visuais documentados\n",
    scalar(@PAG), scalar(map { @{$_->[3]} } @PAG);
