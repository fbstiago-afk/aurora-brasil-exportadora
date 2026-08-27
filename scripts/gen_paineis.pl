#!/usr/bin/perl
# Gera os arquivos .dax dos paineis HTML de KPI (um por pagina) a partir de um
# spec unico, para que os 11 fiquem consistentes.
use strict; use warnings;
use utf8;
binmode(STDOUT, ':encoding(UTF-8)');

my $OUT = shift or die "uso: gen_paineis.pl <pasta scripts/html>\n";

# ---------------------------------------------------------------- spec
# tile: [medida, rotulo, formato, grafico, contexto]
#   formato: usd | brl | pct | int | mil | ton | dec | usdk | dias
#   grafico: spark | bar:<alvo> | -   (alvo em fracao: 1 = 100%)
#   contexto: string DAX (ou "-")
my @PAG = (
 { id=>'p01', arq=>'painel_p01.dax', med=>'HTML Painel Executivo', cols=>4,
   desc=>'Painel de KPIs da pagina 01 Executive Overview.',
   tiles=>[
    ['Receita USD','Receita USD','usd','spark','"<em>vs ano anterior</em>"',      'yoy:Receita YoY %'],
    ['Margem Bruta %','Margem Bruta','pct','spark','"<em>YoY</em>"',              'pp:Margem YoY p.p.'],
    ['Atingimento %','Atingimento da Meta','pct','bar:1.5','"<em>meta " & FMTUSD([Meta Receita USD]) & "</em>"','sem:1:0.9'],
    ['Toneladas','Volume Exportado','ton','spark','"<em>vs ano anterior</em>"',   'yoy:Volume YoY %'],
    ['Receita BRL','Receita em BRL','brl','-','"<em>câmbio médio R$ " & FORMAT([Taxa Media Ponderada],"#,0.00","pt-BR") & "</em>"','-'],
    ['Clientes Ativos','Clientes Ativos','int','-','"<em>" & FORMAT([Novos Clientes],"#,0","pt-BR") & " novos · " & FORMAT([Clientes Perdidos],"#,0","pt-BR") & " perdidos</em>"','-'],
    ['Pedidos','Pedidos Faturados','mil','-','"<em>ticket " & FMTUSDK([Ticket Medio USD]) & "</em>"','-'],
    ['OTIF %','OTIF Logístico','pct','bar:1','"<em>" & FORMAT([% Embarques Atrasados],"0.0%","pt-BR") & " com atraso</em>"','sem:0.9:0.8'],
   ]},
 { id=>'p02', arq=>'painel_p02.dax', med=>'HTML Painel Vendas', cols=>5,
   desc=>'Painel de KPIs da pagina 02 Sales Performance.',
   tiles=>[
    ['Receita USD','Receita','usd','spark','"<em>vs ano anterior</em>"','yoy:Receita YoY %'],
    ['Meta Receita USD','Meta','usd','-','"<em>" & [Status Meta] & "</em>"','-'],
    ['Gap Meta USD','Gap versus Meta','usd','-','"<em>realizado − meta</em>"','sin:Gap Meta USD'],
    ['Ticket Medio USD','Ticket Médio','usdk','spark','"<em>por pedido</em>"','-'],
    ['Pedidos','Pedidos','mil','spark','"<em>no período</em>"','-'],
   ]},
 { id=>'p03', arq=>'painel_p03.dax', med=>'HTML Painel Clientes', cols=>6,
   desc=>'Painel de KPIs da pagina 03 Customers.',
   tiles=>[
    ['Clientes Ativos','Clientes Ativos','int','spark','"<em>com faturamento</em>"','-'],
    ['Novos Clientes','Novos','int','spark','"<em>1ª compra no período</em>"','-'],
    ['Clientes Reativados','Reativados','int','-','"<em>após 180d parados</em>"','-'],
    ['Clientes Perdidos','Perdidos','int','-','"<em>sem compra há 365d</em>"','-'],
    ['Taxa de Churn %','Churn','pct','-','"<em>perdidos / base</em>"','sem:0.05:0.1'],
    ['Receita em Risco','Receita em Risco','usd','-','"<em>clientes 180d+ parados</em>"','-'],
   ]},
 { id=>'p04', arq=>'painel_p04.dax', med=>'HTML Painel Potencial', cols=>4,
   desc=>'Painel de KPIs da pagina 04 Customer Potential.',
   tiles=>[
    ['Receita 12M','Receita 12 Meses','usd','spark','"<em>últimos 12 meses</em>"','-'],
    ['Potencial Anual USD','Potencial Estimado','usd','-','"<em>estimativa da base</em>"','-'],
    ['Share of Wallet','Share of Wallet','pct','bar:1','"<em>receita / potencial</em>"','sem:0.4:0.25'],
    ['Potencial Nao Capturado','Gap Não Capturado','usd','-','"<em>espaço para crescer</em>"','-'],
   ]},
 { id=>'p05', arq=>'painel_p05.dax', med=>'HTML Painel Produtos', cols=>4,
   desc=>'Painel de KPIs da pagina 05 Products.',
   tiles=>[
    ['Receita USD','Receita','usd','spark','"<em>vs ano anterior</em>"','yoy:Receita YoY %'],
    ['Margem Bruta %','Margem','pct','spark','"<em>YoY</em>"','pp:Margem YoY p.p.'],
    ['Toneladas','Volume','ton','spark','"<em>vs ano anterior</em>"','yoy:Volume YoY %'],
    ['Preco Medio por Kg','Preço Médio/kg','usdk2','spark','"<em>receita bruta / kg</em>"','-'],
   ]},
 { id=>'p06', arq=>'painel_p06.dax', med=>'HTML Painel Mercados', cols=>4,
   desc=>'Painel de KPIs da pagina 06 Markets.',
   tiles=>[
    ['Receita USD','Receita Exportada','usd','spark','"<em>vs ano anterior</em>"','yoy:Receita YoY %'],
    ['Toneladas','Volume','ton','spark','"<em>vs ano anterior</em>"','yoy:Volume YoY %'],
    ['Receita YoY %','Crescimento YoY','pct','-','"<em>" & [Maior Crescimento Mercado] & " lidera</em>"','sin:Receita YoY %'],
    ['Margem Bruta %','Margem','pct','spark','"<em>YoY</em>"','pp:Margem YoY p.p.'],
   ]},
 { id=>'p07', arq=>'painel_p07.dax', med=>'HTML Painel Rentabilidade', cols=>5,
   desc=>'Painel de KPIs da pagina 07 Profitability.',
   tiles=>[
    ['Receita Bruta USD','Receita Bruta','usd','spark','"<em>antes de descontos</em>"','-'],
    ['Descontos USD','Descontos','usd','-','"<em>" & FORMAT([Desconto %],"0.0%","pt-BR") & " da bruta</em>"','-'],
    ['Custo Total USD','Custo Total','usd','-','"<em>produto + frete + seguro</em>"','-'],
    ['Margem Bruta USD','Margem Bruta','usd','spark','"<em>vs ano anterior</em>"','yoy:Margem YoY %'],
    ['Margem Bruta %','Margem %','pct','spark','"<em>YoY</em>"','pp:Margem YoY p.p.'],
   ]},
 { id=>'p08', arq=>'painel_p08.dax', med=>'HTML Painel Logistica', cols=>5,
   desc=>'Painel de KPIs da pagina 08 Logistics.',
   tiles=>[
    ['OTIF %','OTIF','pct','bar:1','"<em>on time e in full</em>"','sem:0.9:0.8'],
    ['Lead Time Real','Lead Time Real','dias','spark','"<em>previsto " & FORMAT([Lead Time Previsto],"#,0.0","pt-BR") & "d</em>"','-'],
    ['% Embarques Atrasados','Embarques Atrasados','pct','spark','"<em>sobre entregas realizadas</em>"','sem:0.1:0.2'],
    ['Dias de Atraso Medio','Atraso Médio','dias','-','"<em>só embarques atrasados</em>"','-'],
    ['Frete por Kg','Frete por Kg','usdk2','spark','"<em>frete / peso embarcado</em>"','-'],
   ]},
 { id=>'p09', arq=>'painel_p09.dax', med=>'HTML Painel Equipe', cols=>4,
   desc=>'Painel de KPIs da pagina 09 Sales Team.',
   tiles=>[
    ['Receita USD','Receita da Equipe','usd','spark','"<em>vs ano anterior</em>"','yoy:Receita YoY %'],
    ['Atingimento %','Atingimento Médio','pct','bar:1.5','"<em>" & [Status Meta] & "</em>"','sem:1:0.9'],
    ['Novos Clientes','Novos Clientes','int','spark','"<em>1ª compra no período</em>"','-'],
    ['Margem Bruta %','Margem','pct','spark','"<em>YoY</em>"','pp:Margem YoY p.p.'],
   ]},
 { id=>'p10', arq=>'painel_p10.dax', med=>'HTML Painel Financeiro', cols=>5,
   desc=>'Painel de KPIs da pagina 10 Finance.',
   tiles=>[
    ['Contas a Receber','Contas a Receber','usd','-','"<em>carteira total</em>"','-'],
    ['Recebido USD','Recebido','usd','spark','"<em>já liquidado</em>"','-'],
    ['Saldo em Aberto','Saldo em Aberto','usd','-','"<em>a vencer + vencido</em>"','-'],
    ['Saldo Vencido','Saldo Vencido','usd','-','"<em>vencido + parcial</em>"','-'],
    ['Inadimplencia %','Inadimplência','pct','bar:0.05','"<em>vencido / carteira</em>"','sem:0.02:0.04'],
   ]},
 # --- paginas de drill-through (dossie do item selecionado) ---------------
 { id=>'dtc', arq=>'painel_dt_cliente.dax', med=>'HTML Painel Detalhe Cliente', cols=>4,
   desc=>'Painel de KPIs da pagina de drill-through Detalhe Cliente.',
   tiles=>[
    ['Receita USD','Receita','usd','spark','"<em>vs ano anterior</em>"','yoy:Receita YoY %'],
    ['Margem Bruta %','Margem','pct','spark','"<em>YoY</em>"','pp:Margem YoY p.p.'],
    ['Share of Wallet','Share of Wallet','pct','bar:1','"<em>receita / potencial</em>"','sem:0.4:0.25'],
    ['Segmento RFV','Classificação RFV','txt','-','"<em>classe " & [Classe ABC Cliente] & " · " & FORMAT([Recencia Dias],"#,0","pt-BR") & " d sem comprar</em>"','-'],
   ]},
 { id=>'dtp', arq=>'painel_dt_pais.dax', med=>'HTML Painel Detalhe Mercado', cols=>4,
   desc=>'Painel de KPIs da pagina de drill-through Detalhe Mercado.',
   tiles=>[
    ['Receita USD','Receita','usd','spark','"<em>vs ano anterior</em>"','yoy:Receita YoY %'],
    ['Receita YoY %','Crescimento','pct','-','"<em>" & [Titulo Periodo] & "</em>"','sin:Receita YoY %'],
    ['Margem Bruta %','Margem','pct','spark','"<em>YoY</em>"','pp:Margem YoY p.p.'],
    ['OTIF %','OTIF','pct','bar:1','"<em>" & FORMAT([% Embarques Atrasados],"0.0%","pt-BR") & " com atraso</em>"','sem:0.9:0.8'],
   ]},

 { id=>'p11', arq=>'painel_p11.dax', med=>'HTML Painel Forecast', cols=>5,
   desc=>'Painel de KPIs da pagina 11 Forecast e Budget.',
   tiles=>[
    ['Receita USD','Realizado','usd','spark','"<em>vs ano anterior</em>"','yoy:Receita YoY %'],
    ['Receita Orcada USD','Orçado','usd','-','"<em>" & FORMAT([Actual vs Budget %],"0.0%","pt-BR") & " do orçado</em>"','-'],
    ['Receita Forecast USD','Forecast','usd','-','"<em>última revisão</em>"','-'],
    ['Forecast Gap','Gap Forecast','usd','-','"<em>forecast − realizado</em>"','sin:Forecast Gap'],
    ['Projecao Fechamento Ano','Projeção do Ano','usd','-','"<em>linear sobre o realizado</em>"','-'],
   ]},
);

# ---------------------------------------------------------------- helpers
sub fmt_valor {
    my ($med, $f) = @_;
    my $v = "[$med]";
    return "IF ( ABS ( $v ) >= 1E9, \"US\$ \" & FORMAT ( $v / 1E9, \"#,0.0\", \"pt-BR\" ) & \" Bi\", \"US\$ \" & FORMAT ( $v / 1E6, \"#,0.0\", \"pt-BR\" ) & \" Mi\" )" if $f eq 'usd';
    return "IF ( ABS ( $v ) >= 1E9, \"R\$ \" & FORMAT ( $v / 1E9, \"#,0.0\", \"pt-BR\" ) & \" Bi\", \"R\$ \" & FORMAT ( $v / 1E6, \"#,0.0\", \"pt-BR\" ) & \" Mi\" )" if $f eq 'brl';
    return "FORMAT ( $v, \"0.0%\", \"pt-BR\" )"                                    if $f eq 'pct';
    return "FORMAT ( $v, \"#,0\", \"pt-BR\" )"                                     if $f eq 'int';
    return "FORMAT ( $v / 1000, \"#,0.0\", \"pt-BR\" ) & \" Mil\""                 if $f eq 'mil';
    return "FORMAT ( $v / 1000, \"#,0.0\", \"pt-BR\" ) & \" Mil t\""               if $f eq 'ton';
    return "\"US\$ \" & FORMAT ( $v, \"#,0\", \"pt-BR\" )"                         if $f eq 'usdk';
    return "\"US\$ \" & FORMAT ( $v, \"#,0.00\", \"pt-BR\" )"                      if $f eq 'usdk2';
    return "FORMAT ( $v, \"#,0.0\", \"pt-BR\" ) & \" d\""                          if $f eq 'dias';
    # medida que ja devolve texto (segmento, classe, status)
    return $v                                                                      if $f eq 'txt';
    return "FORMAT ( $v, \"#,0.0\", \"pt-BR\" )";
}

my $CSS = <<'CSS';
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:transparent;overflow:hidden}
.ab{height:100%;display:grid;grid-auto-rows:1fr;gap:clamp(5px,.62vw,11px);font-family:'Segoe UI',system-ui,sans-serif}
.t{background:rgba(255,255,255,.65);border:1px solid rgba(227,224,217,.65);border-radius:clamp(5px,.6vw,9px);padding:clamp(6px,.7vw,11px) clamp(8px,.85vw,14px);display:flex;flex-direction:column;gap:.15em;overflow:hidden;position:relative}
.t:before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:#C8763C;opacity:.9}
.t.b:before{background:#17495A}
.t.g:before{background:#8FA98F}
.lb{font-size:clamp(7.5px,.66vw,10px);letter-spacing:.06em;text-transform:uppercase;color:#5D6E75;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.vl{font-size:clamp(14px,1.6vw,26px);font-weight:700;color:#0E2A33;line-height:1.05;letter-spacing:-.015em;white-space:nowrap}
.dt{font-size:clamp(7.5px,.66vw,10px);font-weight:600;display:flex;align-items:baseline;gap:.3em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#5D6E75}
.dt em{font-style:normal;color:#8C96A5;font-weight:500}
.spk{display:flex;align-items:flex-end;gap:clamp(1px,.12vw,2.5px);flex:1;min-height:clamp(11px,1.3vw,24px);margin-top:.2em}
.spk i{flex:1 1 0;background:currentColor;border-radius:1.5px 1.5px 0 0;opacity:.9;min-width:1px}
.spk i:last-child{opacity:1}
.bar{position:relative;height:clamp(4px,.4vw,7px);background:rgba(233,225,212,.7);border-radius:99px;margin-top:auto;overflow:hidden}
.bar i{position:absolute;left:0;top:0;bottom:0;border-radius:99px}
.bar u{position:absolute;top:0;bottom:0;width:1.5px;background:#0E2A33;opacity:.5}
</style>
CSS
$CSS =~ s/\s+\z//;

# ---------------------------------------------------------------- geracao
for my $pg (@PAG) {
    my @tiles = @{ $pg->{tiles} };
    my @vars;
    push @vars, 'VAR _fim = MAX ( dCalendario[Data] )';

    # serie de 12 meses apenas para os tiles com sparkline
    my @spark = grep { $tiles[$_][3] eq 'spark' } 0 .. $#tiles;
    if (@spark) {
        my @cols = map { "        \"\@s$_\", CALCULATE ( [$tiles[$_][0]] )" } @spark;
        push @vars,
            "VAR _serie =\n" .
            "    ADDCOLUMNS (\n" .
            "        CALCULATETABLE (\n" .
            "            VALUES ( dCalendario[AnoMesNumero] ),\n" .
            "            DATESINPERIOD ( dCalendario[Data], _fim, -12, MONTH )\n" .
            "        ),\n" . join(",\n", @cols) . "\n    )";
        for my $i (@spark) {
            push @vars, "VAR _mn$i = MINX ( _serie, [\@s$i] )";
            push @vars, "VAR _mx$i = MAXX ( _serie, [\@s$i] )";
            # Barras em <div>, nao <svg>: o visual HTML Content nao renderiza SVG
            # (o projeto de FIIs, que funciona, tambem monta tudo com div).
            # Altura de 12% a 100%; DIVIDE com alternativa cobre serie plana.
            push @vars,
                "VAR _pt$i =\n" .
                "    CONCATENATEX (\n" .
                "        _serie,\n" .
                "        \"<i style='height:\"\n" .
                "            & FORMAT ( 12 + DIVIDE ( [\@s$i] - _mn$i, _mx$i - _mn$i, 0.5 ) * 88, \"0\", \"en-US\" )\n" .
                "            & \"%'></i>\",\n" .
                "        \"\",\n" .
                "        dCalendario[AnoMesNumero], ASC\n" .
                "    )";
        }
    }

    my @html;
    my $traco = 0;
    for my $i (0 .. $#tiles) {
        my ($med, $rot, $f, $graf, $ctx, $delta) = @{ $tiles[$i] };
        # limiar "bom" do semaforo: vira a marca de referencia na barra
        my $limiar = ($delta =~ /^sem:([\d.]+):/) ? $1 : undef;
        my $cls = 't' . ($i % 3 == 1 ? ' b' : ($i % 3 == 2 ? ' g' : ''));
        my $valexpr = fmt_valor($med, $f);

        # cor/valor do delta
        my ($corVar, $deltaTxt) = ('', '');
        if ($delta =~ /^yoy:(.+)$/) {
            my $d = $1;
            push @vars, "VAR _d$i = [$d]";
            push @vars, "VAR _c$i = IF ( _d$i >= 0, \"#1F8A70\", \"#C0453B\" )";
            $deltaTxt = "IF ( _d$i >= 0, \"▲ \", \"▼ \" ) & FORMAT ( _d$i, \"0.0%\", \"pt-BR\" ) & \" \" & ";
            $corVar = "\" style='color:\" & _c$i & \"'\"";
        } elsif ($delta =~ /^pp:(.+)$/) {
            my $d = $1;
            # p.p. e diferenca de fracoes: multiplicar por 100 para virar ponto percentual
            push @vars, "VAR _d$i = [$d] * 100";
            push @vars, "VAR _c$i = IF ( _d$i >= 0, \"#1F8A70\", \"#C0453B\" )";
            $deltaTxt = "IF ( _d$i >= 0, \"▲ \", \"▼ \" ) & FORMAT ( _d$i, \"0.0\", \"pt-BR\" ) & \" p.p. \" & ";
            $corVar = "\" style='color:\" & _c$i & \"'\"";
        } elsif ($delta =~ /^sin:(.+)$/) {
            my $d = $1;
            push @vars, "VAR _c$i = IF ( [$d] >= 0, \"#1F8A70\", \"#C0453B\" )";
            $corVar = "\" style='color:\" & _c$i & \"'\"";
        } elsif ($delta =~ /^sem:([\d.]+):([\d.]+)$/) {
            my ($bom, $ok) = ($1, $2);
            my $inv = ($bom < $ok) ? 1 : 0;   # menor e melhor
            push @vars, $inv
                ? "VAR _c$i = IF ( [$med] <= $bom, \"#1F8A70\", IF ( [$med] <= $ok, \"#D9A441\", \"#C0453B\" ) )"
                : "VAR _c$i = IF ( [$med] >= $bom, \"#1F8A70\", IF ( [$med] >= $ok, \"#D9A441\", \"#C0453B\" ) )";
        }

        my $valStyle = ($delta =~ /^sem:/) ? " & \" style='color:\" & _c$i & \"'\"" : '';
        my $h = "\"<div class='$cls'><div class='lb'>$rot</div>\"\n"
              . "            & \"<div class='vl'\"$valStyle & \">\" & " . $valexpr . " & \"</div>\"\n";

        if ($ctx ne '-' || $deltaTxt) {
            $h .= "            & \"<div class='dt'\"" . ($corVar ? " & $corVar" : "") . " & \">\" & "
                . ($deltaTxt ? $deltaTxt : "")
                . ($ctx ne '-' ? $ctx : "\"\"") . " & \"</div>\"\n";
        }

        if ($graf eq 'spark') {
            my $cor = ($i % 3 == 1) ? '#17495A' : (($i % 3 == 2) ? '#8FA98F' : '#C8763C');
            $h .= "            & \"<div class='spk' style='color:$cor'>\" & _pt$i & \"</div>\"\n";
        } elsif ($graf =~ /^bar:([\d.]+)$/) {
            my $alvo = $1;
            my $marca = sprintf("%.1f", (defined $limiar ? $limiar : $alvo) / $alvo * 100);
            $h .= "            & \"<div class='bar'><i style='width:\"\n"
                . "            & FORMAT ( MIN ( MAX ( [$med], 0 ), $alvo ) / $alvo * 100, \"0.0\", \"en-US\" )\n"
                . "            & \"%;background:\" & _c$i & \"'></i><u style='left:$marca%'></u></div>\"\n";
        }
        $h .= "            & \"</div>\"";
        push @html, $h;
    }

    my $dax = join("\n", @vars) . "\n\n"
        . "VAR _css = \"" . $CSS . "\"\n\n"
        . "VAR _html =\n    _css\n        & \"<div class='ab' style=\"\"grid-template-columns:repeat($pg->{cols},1fr)\"\">\"\n        & "
        . join("\n        & ", @html)
        . "\n        & \"</div>\"\nRETURN\n    _html\n";

    # FMTUSD/FMTUSDK sao atalhos do spec - expandir
    $dax =~ s/FMTUSD\(\s*(\[[^\]]+\])\s*\)/IF ( ABS ( $1 ) >= 1E9, "US\$ " & FORMAT ( $1 \/ 1E9, "#,0.0", "pt-BR" ) & " Bi", "US\$ " & FORMAT ( $1 \/ 1E6, "#,0.0", "pt-BR" ) & " Mi" )/g;
    $dax =~ s/FMTUSDK\(\s*(\[[^\]]+\])\s*\)/"US\$ " & FORMAT ( $1, "#,0", "pt-BR" )/g;

    open(my $o, '>:encoding(UTF-8)', "$OUT/$pg->{arq}") or die "$OUT/$pg->{arq}: $!";
    print $o $dax; close $o;
    printf "%-6s %-28s %d tiles, %d sparklines -> %s\n", $pg->{id}, $pg->{med}, scalar(@tiles), scalar(@spark), $pg->{arq};
}
print "\nOK\n";
