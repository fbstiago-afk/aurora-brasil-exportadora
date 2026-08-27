#!/usr/bin/perl
# Gera os .dax dos tooltips HTML (um por entidade). Canvas pequeno (320px),
# entao a densidade e alta: cabecalho com identificacao, faixa de KPIs,
# barras de 12 meses e uma secao de contexto especifica de cada entidade.
use strict; use warnings;
use utf8;
binmode(STDOUT, ':encoding(UTF-8)');

my $OUT = shift or die "uso: gen_tooltips.pl <pasta scripts/html>\n";

# CSS compartilhado. rgba para acompanhar a translucidez do resto do relatorio.
my $CSS = <<'CSS';
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:transparent;overflow:hidden}
.tt{height:100%;display:flex;flex-direction:column;gap:6px;padding:2px;
    font-family:'Segoe UI',system-ui,sans-serif;color:#16262C}
.hd{display:flex;align-items:baseline;justify-content:space-between;gap:6px;
    border-left:3px solid #C8763C;padding-left:7px}
.hd h1{font-size:12.5px;font-weight:700;color:#0E2A33;line-height:1.15;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:200px}
.hd .tag{font-size:8px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;
    padding:2px 6px;border-radius:99px;background:rgba(200,118,60,.16);color:#8A4F26;white-space:nowrap}
.sub{font-size:8.5px;color:#8C96A5;margin:-3px 0 0 10px;
     white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kp{display:grid;grid-template-columns:repeat(4,1fr);gap:4px}
.kp div{background:rgba(255,255,255,.72);border:1px solid rgba(227,224,217,.8);
        border-radius:5px;padding:4px 5px;overflow:hidden}
.kp span{display:block;font-size:7.5px;letter-spacing:.04em;text-transform:uppercase;
         color:#5D6E75;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kp b{display:block;font-size:12.5px;font-weight:700;color:#0E2A33;line-height:1.2;white-space:nowrap}
.sec{font-size:7.5px;letter-spacing:.06em;text-transform:uppercase;color:#8C96A5;font-weight:700;margin-top:1px}
.spk{display:flex;align-items:flex-end;gap:1.5px;height:30px}
.spk i{flex:1 1 0;background:#C8763C;border-radius:1.5px 1.5px 0 0;opacity:.55;min-width:1px}
.spk i:last-child{opacity:1}
.rows{display:flex;flex-direction:column;gap:3px}
.r{display:flex;align-items:center;gap:5px;font-size:9px}
.r em{font-style:normal;color:#5D6E75;flex:0 0 82px;white-space:nowrap;
      overflow:hidden;text-overflow:ellipsis}
.r .tr{flex:1;height:6px;background:rgba(233,225,212,.75);border-radius:99px;position:relative;overflow:hidden}
.r .tr i{position:absolute;left:0;top:0;bottom:0;border-radius:99px}
.r b{flex:0 0 auto;font-weight:700;color:#0E2A33;font-size:9px;min-width:42px;text-align:right}
.ft{margin-top:auto;font-size:7.5px;color:#8C96A5;display:flex;justify-content:space-between;gap:6px;
    border-top:1px solid rgba(227,224,217,.7);padding-top:4px}
.ft b{color:#16262C;font-weight:600}
</style>
CSS
$CSS =~ s/\s+\z//;

# --------------------------------------------------------------- helpers DAX
sub usd {  my $v = shift; "IF ( ABS ( $v ) >= 1E6, \"US\$ \" & FORMAT ( $v / 1E6, \"#,0.0\", \"pt-BR\" ) & \" Mi\", \"US\$ \" & FORMAT ( $v / 1E3, \"#,0\", \"pt-BR\" ) & \" k\" )" }
sub pct {  my $v = shift; "FORMAT ( $v, \"0.0%\", \"pt-BR\" )" }
sub int_ { my $v = shift; "FORMAT ( $v, \"#,0\", \"pt-BR\" )" }

# barra de 12 meses de uma medida
sub spark {
    my ($idx, $medida) = @_;
    return (
        "VAR _serie$idx =\n" .
        "    ADDCOLUMNS (\n" .
        "        CALCULATETABLE (\n" .
        "            VALUES ( dCalendario[AnoMesNumero] ),\n" .
        "            DATESINPERIOD ( dCalendario[Data], _fim, -12, MONTH )\n" .
        "        ),\n" .
        "        \"\@v\", CALCULATE ( [$medida] )\n" .
        "    )\n" .
        "VAR _mn$idx = MINX ( _serie$idx, [\@v] )\n" .
        "VAR _mx$idx = MAXX ( _serie$idx, [\@v] )\n" .
        "VAR _spk$idx =\n" .
        "    CONCATENATEX (\n" .
        "        _serie$idx,\n" .
        "        \"<i style='height:\"\n" .
        "            & FORMAT ( 14 + DIVIDE ( [\@v] - _mn$idx, _mx$idx - _mn$idx, 0.5 ) * 86, \"0\", \"en-US\" )\n" .
        "            & \"%'></i>\",\n" .
        "        \"\",\n" .
        "        dCalendario[AnoMesNumero], ASC\n" .
        "    )"
    );
}

# linha com barra proporcional
sub linha {
    my ($rot, $valExpr, $fracExpr, $corExpr) = @_;
    return "\"<div class='r'><em>$rot</em><div class='tr'><i style='width:\"\n"
         . "            & FORMAT ( MIN ( MAX ( $fracExpr, 0 ), 1 ) * 100, \"0\", \"en-US\" )\n"
         . "            & \"%;background:\" & $corExpr & \"'></i></div><b>\" & $valExpr & \"</b></div>\"";
}

my $VERDE = '"#1F8A70"'; my $COBRE = '"#C8763C"'; my $PETRO = '"#17495A"'; my $OLIVA = '"#8FA98F"';

# --------------------------------------------------------------- definicoes
my @TT = (

 { arq=>'tooltip_cliente.dax', med=>'HTML Tooltip Cliente',
   desc=>'Tooltip HTML de cliente: identificacao, KPIs, tendencia e carteira.',
   dax=>sub {
     my @v;
     push @v, 'VAR _fim = MAX ( dCalendario[Data] )';
     push @v, 'VAR _nome = SELECTEDVALUE ( dCliente[RazaoSocial], "Vários clientes" )';
     push @v, 'VAR _pais = SELECTEDVALUE ( dCliente[Pais], "—" )';
     push @v, 'VAR _seg = SELECTEDVALUE ( dCliente[Segmento], "—" )';
     push @v, 'VAR _porte = SELECTEDVALUE ( dCliente[Porte], "—" )';
     push @v, 'VAR _canal = SELECTEDVALUE ( dCliente[CanalVenda], "—" )';
     push @v, 'VAR _rfv = [Segmento RFV]';
     push @v, 'VAR _abc = [Classe ABC Cliente]';
     push @v, 'VAR _yoy = [Receita YoY %]';
     push @v, 'VAR _sow = [Share of Wallet]';
     push @v, 'VAR _rec = [Recencia Dias]';
     push @v, 'VAR _cor = IF ( _yoy >= 0, "#1F8A70", "#C0453B" )';
     push @v, spark(0, 'Receita USD');
     my $html =
        "\"<div class='tt'>\"\n"
      . "        & \"<div class='hd'><h1>\" & _nome & \"</h1><span class='tag'>\" & _rfv & \"</span></div>\"\n"
      . "        & \"<div class='sub'>\" & _pais & \" · \" & _seg & \" · porte \" & _porte & \" · \" & _canal & \"</div>\"\n"
      . "        & \"<div class='kp'>\"\n"
      . "            & \"<div><span>Receita</span><b>\" & " . usd('[Receita USD]') . " & \"</b></div>\"\n"
      . "            & \"<div><span>Margem</span><b>\" & " . pct('[Margem Bruta %]') . " & \"</b></div>\"\n"
      . "            & \"<div><span>Pedidos</span><b>\" & " . int_('[Pedidos]') . " & \"</b></div>\"\n"
      . "            & \"<div><span>Ticket</span><b>\" & " . usd('[Ticket Medio USD]') . " & \"</b></div>\"\n"
      . "        & \"</div>\"\n"
      . "        & \"<div class='sec'>Receita — últimos 12 meses</div>\"\n"
      . "        & \"<div class='spk'>\" & _spk0 & \"</div>\"\n"
      . "        & \"<div class='rows'>\"\n"
      . "            & " . linha('Share of Wallet', pct('_sow'), '_sow', $COBRE) . "\n"
      . "            & " . linha('Classe ABC', '_abc', 'SWITCH ( _abc, "A", 1, "B", 0.6, 0.3 )', $PETRO) . "\n"
      . "        & \"</div>\"\n"
      . "        & \"<div class='ft'><span>Última compra <b>\" & FORMAT ( [Data Ultima Compra], \"dd/mm/yy\", \"pt-BR\" ) & \"</b> · \" & " . int_('_rec') . " & \" d</span>\"\n"
      . "            & \"<span style='color:\" & _cor & \"'>\" & IF ( _yoy >= 0, \"▲\", \"▼\" ) & \" \" & " . pct('_yoy') . " & \" YoY</span></div>\"\n"
      . "        & \"</div>\"";
     return (\@v, $html);
   } },

 { arq=>'tooltip_produto.dax', med=>'HTML Tooltip Produto',
   desc=>'Tooltip HTML de produto: ficha do SKU, KPIs, tendencia e margem alvo.',
   dax=>sub {
     my @v;
     push @v, 'VAR _fim = MAX ( dCalendario[Data] )';
     push @v, 'VAR _nome = SELECTEDVALUE ( dProduto[Produto], "Vários produtos" )';
     push @v, 'VAR _sku = SELECTEDVALUE ( dProduto[SKU], "—" )';
     push @v, 'VAR _cat = SELECTEDVALUE ( dProduto[Categoria], "—" )';
     push @v, 'VAR _linha = SELECTEDVALUE ( dProduto[Linha], "—" )';
     push @v, 'VAR _emb = SELECTEDVALUE ( dProduto[TipoEmbalagem], "—" )';
     push @v, 'VAR _origem = SELECTEDVALUE ( dProduto[EstadoOrigem], "—" )';
     push @v, 'VAR _alvo = SELECTEDVALUE ( dProduto[MargemAlvo], BLANK () )';
     push @v, 'VAR _abc = [Classe ABC Produto]';
     push @v, 'VAR _mrg = [Margem Bruta %]';
     push @v, 'VAR _yoy = [Receita YoY %]';
     push @v, 'VAR _cor = IF ( _yoy >= 0, "#1F8A70", "#C0453B" )';
     push @v, 'VAR _corMrg = IF ( _mrg >= _alvo, "#1F8A70", "#C0453B" )';
     push @v, spark(0, 'Receita USD');
     my $html =
        "\"<div class='tt'>\"\n"
      . "        & \"<div class='hd'><h1>\" & _nome & \"</h1><span class='tag'>ABC \" & _abc & \"</span></div>\"\n"
      . "        & \"<div class='sub'>\" & _sku & \" · \" & _cat & \" · \" & _linha & \" · \" & _emb & \" · \" & _origem & \"</div>\"\n"
      . "        & \"<div class='kp'>\"\n"
      . "            & \"<div><span>Receita</span><b>\" & " . usd('[Receita USD]') . " & \"</b></div>\"\n"
      . "            & \"<div><span>Margem</span><b>\" & " . pct('_mrg') . " & \"</b></div>\"\n"
      . "            & \"<div><span>Volume</span><b>\" & FORMAT ( [Toneladas], \"#,0.0\", \"pt-BR\" ) & \" t</b></div>\"\n"
      . "            & \"<div><span>US\$/kg</span><b>\" & FORMAT ( [Preco Medio por Kg], \"#,0.00\", \"pt-BR\" ) & \"</b></div>\"\n"
      . "        & \"</div>\"\n"
      . "        & \"<div class='sec'>Receita — últimos 12 meses</div>\"\n"
      . "        & \"<div class='spk'>\" & _spk0 & \"</div>\"\n"
      . "        & \"<div class='rows'>\"\n"
      . "            & " . linha('Margem alvo', pct('_alvo'), '_alvo', $OLIVA) . "\n"
      . "            & " . linha('Margem real', pct('_mrg'), '_mrg', '_corMrg') . "\n"
      . "        & \"</div>\"\n"
      . "        & \"<div class='ft'><span>Margem/kg <b>US\$ \" & FORMAT ( [Margem por Kg], \"#,0.00\", \"pt-BR\" ) & \"</b></span>\"\n"
      . "            & \"<span style='color:\" & _cor & \"'>\" & IF ( _yoy >= 0, \"▲\", \"▼\" ) & \" \" & " . pct('_yoy') . " & \" YoY</span></div>\"\n"
      . "        & \"</div>\"";
     return (\@v, $html);
   } },

 { arq=>'tooltip_pais.dax', med=>'HTML Tooltip Pais',
   desc=>'Tooltip HTML de mercado: perfil do pais, KPIs, tendencia e logistica.',
   dax=>sub {
     my @v;
     push @v, 'VAR _fim = MAX ( dCalendario[Data] )';
     push @v, 'VAR _nome = SELECTEDVALUE ( dPais[Pais], "Vários mercados" )';
     push @v, 'VAR _cont = SELECTEDVALUE ( dPais[Continente], "—" )';
     push @v, 'VAR _reg = SELECTEDVALUE ( dPais[Regiao], "—" )';
     push @v, 'VAR _class = SELECTEDVALUE ( dPais[ClassificacaoMercado], "—" )';
     push @v, 'VAR _risco = SELECTEDVALUE ( dPais[RiscoPais], "—" )';
     push @v, 'VAR _tarifa = SELECTEDVALUE ( dPais[TarifaMediaImportacao], BLANK () )';
     push @v, 'VAR _otif = [OTIF %]';
     push @v, 'VAR _atr = [% Embarques Atrasados]';
     push @v, 'VAR _yoy = [Receita YoY %]';
     push @v, 'VAR _cor = IF ( _yoy >= 0, "#1F8A70", "#C0453B" )';
     push @v, 'VAR _corOtif = IF ( _otif >= 0.9, "#1F8A70", IF ( _otif >= 0.8, "#D9A441", "#C0453B" ) )';
     push @v, spark(0, 'Receita USD');
     my $html =
        "\"<div class='tt'>\"\n"
      . "        & \"<div class='hd'><h1>\" & _nome & \"</h1><span class='tag'>\" & _class & \"</span></div>\"\n"
      . "        & \"<div class='sub'>\" & _cont & \" · \" & _reg & \" · risco \" & _risco & \" · tarifa \" & " . pct('_tarifa') . " & \"</div>\"\n"
      . "        & \"<div class='kp'>\"\n"
      . "            & \"<div><span>Receita</span><b>\" & " . usd('[Receita USD]') . " & \"</b></div>\"\n"
      . "            & \"<div><span>Margem</span><b>\" & " . pct('[Margem Bruta %]') . " & \"</b></div>\"\n"
      . "            & \"<div><span>Volume</span><b>\" & FORMAT ( [Toneladas], \"#,0.0\", \"pt-BR\" ) & \" t</b></div>\"\n"
      . "            & \"<div><span>Clientes</span><b>\" & " . int_('[Clientes Ativos]') . " & \"</b></div>\"\n"
      . "        & \"</div>\"\n"
      . "        & \"<div class='sec'>Receita — últimos 12 meses</div>\"\n"
      . "        & \"<div class='spk'>\" & _spk0 & \"</div>\"\n"
      . "        & \"<div class='rows'>\"\n"
      . "            & " . linha('OTIF', pct('_otif'), '_otif', '_corOtif') . "\n"
      . "            & " . linha('Embarq. atraso', pct('_atr'), '_atr', $COBRE) . "\n"
      . "        & \"</div>\"\n"
      . "        & \"<div class='ft'><span>Lead time <b>\" & FORMAT ( [Lead Time Real], \"#,0.0\", \"pt-BR\" ) & \" d</b> · frete US\$ \" & FORMAT ( [Frete por Kg], \"#,0.00\", \"pt-BR\" ) & \"/kg</span>\"\n"
      . "            & \"<span style='color:\" & _cor & \"'>\" & IF ( _yoy >= 0, \"▲\", \"▼\" ) & \" \" & " . pct('_yoy') . " & \" YoY</span></div>\"\n"
      . "        & \"</div>\"";
     return (\@v, $html);
   } },

 { arq=>'tooltip_vendedor.dax', med=>'HTML Tooltip Vendedor',
   desc=>'Tooltip HTML de vendedor: perfil, KPIs, tendencia, meta e concentracao.',
   dax=>sub {
     my @v;
     push @v, 'VAR _fim = MAX ( dCalendario[Data] )';
     push @v, 'VAR _nome = SELECTEDVALUE ( dVendedor[NomeVendedor], "Vários vendedores" )';
     push @v, 'VAR _cargo = SELECTEDVALUE ( dVendedor[Cargo], "—" )';
     push @v, 'VAR _ger = SELECTEDVALUE ( dVendedor[Gerente], "—" )';
     push @v, 'VAR _reg = SELECTEDVALUE ( dVendedor[RegiaoResponsavel], "—" )';
     push @v, 'VAR _at = [Atingimento %]';
     push @v, 'VAR _conc = [Concentracao Carteira Vendedor]';
     push @v, 'VAR _status = [Status Meta]';
     push @v, 'VAR _yoy = [Receita YoY %]';
     push @v, 'VAR _cor = IF ( _yoy >= 0, "#1F8A70", "#C0453B" )';
     push @v, 'VAR _corAt = IF ( _at >= 1, "#1F8A70", IF ( _at >= 0.9, "#D9A441", "#C0453B" ) )';
     push @v, 'VAR _corConc = IF ( _conc >= 0.4, "#C0453B", IF ( _conc >= 0.25, "#D9A441", "#1F8A70" ) )';
     push @v, spark(0, 'Receita USD');
     my $html =
        "\"<div class='tt'>\"\n"
      . "        & \"<div class='hd'><h1>\" & _nome & \"</h1><span class='tag'>\" & _status & \"</span></div>\"\n"
      . "        & \"<div class='sub'>\" & _cargo & \" · \" & _reg & \" · reporta a \" & _ger & \"</div>\"\n"
      . "        & \"<div class='kp'>\"\n"
      . "            & \"<div><span>Receita</span><b>\" & " . usd('[Receita USD]') . " & \"</b></div>\"\n"
      . "            & \"<div><span>Meta</span><b>\" & " . usd('[Meta Receita USD]') . " & \"</b></div>\"\n"
      . "            & \"<div><span>Clientes</span><b>\" & " . int_('[Clientes Ativos]') . " & \"</b></div>\"\n"
      . "            & \"<div><span>Margem</span><b>\" & " . pct('[Margem Bruta %]') . " & \"</b></div>\"\n"
      . "        & \"</div>\"\n"
      . "        & \"<div class='sec'>Receita — últimos 12 meses</div>\"\n"
      . "        & \"<div class='spk'>\" & _spk0 & \"</div>\"\n"
      . "        & \"<div class='rows'>\"\n"
      . "            & " . linha('Atingimento', pct('_at'), 'DIVIDE ( _at, 1.5 )', '_corAt') . "\n"
      . "            & " . linha('Maior cliente', pct('_conc'), '_conc', '_corConc') . "\n"
      . "        & \"</div>\"\n"
      . "        & \"<div class='ft'><span>Gap <b>\" & " . usd('[Gap Meta USD]') . " & \"</b> · novos \" & " . int_('[Novos Clientes]') . " & \"</span>\"\n"
      . "            & \"<span style='color:\" & _cor & \"'>\" & IF ( _yoy >= 0, \"▲\", \"▼\" ) & \" \" & " . pct('_yoy') . " & \" YoY</span></div>\"\n"
      . "        & \"</div>\"";
     return (\@v, $html);
   } },
);

for my $t (@TT) {
    my ($vars, $html) = $t->{dax}->();
    my $dax = join("\n", @$vars) . "\n\n"
            . "VAR _css = \"" . $CSS . "\"\n\n"
            . "VAR _html =\n    _css\n        & " . $html . "\nRETURN\n    _html\n";
    open(my $o, '>:encoding(UTF-8)', "$OUT/$t->{arq}") or die "$OUT/$t->{arq}: $!";
    print $o $dax; close $o;
    printf "%-24s -> %s\n", $t->{med}, $t->{arq};
}
print "\nOK\n";
