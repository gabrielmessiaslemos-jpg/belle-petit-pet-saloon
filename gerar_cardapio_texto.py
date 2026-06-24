#!/usr/bin/env python3
"""Gera CasaCeli_Cardapio_Texto.pdf — layout sem fotos, apenas descrições e preços."""

import subprocess, sys

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@page { size: A4; margin: 0; }
* { margin:0; padding:0; box-sizing:border-box; }

/* ── tipografia ── */
body       { font-family: Georgia,"Times New Roman",serif; background:#FAF8F3; color:#4F2915; }
.mono      { font-family:"Courier New",Courier,monospace; }

/* ══════════ CAPA ══════════ */
.cover {
  width:210mm; height:297mm;
  background:#1E4B26;
  display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  page-break-after:always;
  position:relative;
}
.cover-border {
  position:absolute; inset:18px;
  border:1px solid rgba(184,154,74,0.35);
  pointer-events:none;
}
.cover-corner {
  position:absolute; width:28px; height:28px;
  border-color:#B89A4A; border-style:solid;
}
.tl { top:14px;  left:14px;  border-width:2px 0 0 2px; }
.tr { top:14px;  right:14px; border-width:2px 2px 0 0; }
.bl { bottom:14px; left:14px;  border-width:0 0 2px 2px; }
.br { bottom:14px; right:14px; border-width:0 2px 2px 0; }

.cover-inner   { text-align:center; padding:0 60px; }
.cover-ornament{ color:#B89A4A; font-size:20px; margin:18px 0; letter-spacing:6px; }
.cover-eyebrow {
  font-family:"Courier New",monospace;
  font-size:9px; letter-spacing:6px;
  text-transform:uppercase; color:#8F9C68;
  margin-bottom:14px;
}
.cover-casa    { font-size:80px; color:#B89A4A; letter-spacing:6px; line-height:1; text-transform:uppercase; }
.cover-celi    { font-size:54px; color:#FAF8F3; letter-spacing:8px; text-transform:uppercase; margin-top:4px; }
.cover-divider { width:100px; height:1px; background:#B89A4A; margin:28px auto; }
.cover-tagline { font-style:italic; font-size:15px; color:#8F9C68; letter-spacing:.5px; line-height:1.7; }

.cover-footer {
  position:absolute; bottom:44px;
  text-align:center; width:100%;
}
.cover-footer-line {
  font-family:"Courier New",monospace;
  font-size:9px; letter-spacing:4px;
  text-transform:uppercase; color:#FAF8F3; opacity:.6;
  margin-top:5px;
}

/* ══════════ PÁGINA INTERNA ══════════ */
.page {
  width:210mm; min-height:297mm;
  padding:18mm 18mm 14mm;
  page-break-after:always;
  background:#FAF8F3;
}
.page:last-child { page-break-after:auto; }

.page-header {
  text-align:center;
  padding-bottom:16px;
  margin-bottom:24px;
  border-bottom:2px solid #1E4B26;
}
.page-header-eye {
  font-family:"Courier New",monospace;
  font-size:8px; letter-spacing:5px;
  text-transform:uppercase; color:#8F9C68;
}
.page-header-brand { font-size:20px; color:#1E4B26; margin-top:4px; }

/* ── seção ── */
.section     { margin-bottom:26px; }
.section-head {
  display:flex; align-items:center; gap:10px;
  margin-bottom:14px;
}
.section-label {
  font-family:"Courier New",monospace;
  font-size:8.5px; text-transform:uppercase; letter-spacing:5px;
  color:#B05216; white-space:nowrap;
}
.section-rule { flex:1; height:1px; background:rgba(143,156,104,.35); }

/* ── prato ── */
.dish {
  display:flex; justify-content:space-between; align-items:baseline;
  padding:9px 0;
  border-bottom:1px dotted rgba(143,156,104,.30);
}
.dish:last-child { border-bottom:none; }
.dish-left  { flex:1; padding-right:16px; }
.dish-name  { font-size:13.5px; font-weight:bold; color:#1E4B26; line-height:1.3; }
.dish-desc  { font-size:9.5px; color:#4F2915; font-style:italic; margin-top:3px; opacity:.8; line-height:1.5; }
.dish-price {
  font-family:"Courier New",monospace;
  font-size:13.5px; color:#B89A4A; font-weight:bold; white-space:nowrap;
}

/* ── nota de gramagem ── */
.size-note {
  margin-top:18px;
  padding:12px 18px;
  background:rgba(30,75,38,.05);
  border-left:3px solid #B89A4A;
}
.size-note-label {
  font-family:"Courier New",monospace;
  font-size:8px; text-transform:uppercase; letter-spacing:3px;
  color:#8F9C68; margin-bottom:7px;
}
.size-row  { display:flex; gap:28px; }
.size-item { font-size:11.5px; color:#1E4B26; }
.size-foot { font-size:8px; color:#4F2915; font-style:italic; margin-top:6px; opacity:.75; }

/* ══════════ PÁGINA DE KITS ══════════ */
.kits-page {
  width:210mm; min-height:297mm;
  background:#1E4B26;
  padding:18mm 18mm 14mm;
  page-break-after:always;
}
.kits-page:last-child { page-break-after:auto; }

.kits-header { text-align:center; margin-bottom:36px; }
.kits-eye {
  font-family:"Courier New",monospace;
  font-size:8px; text-transform:uppercase; letter-spacing:6px; color:#8F9C68;
}
.kits-title  { font-size:42px; color:#B89A4A; margin-top:6px; letter-spacing:2px; }
.kits-div    { width:70px; height:1px; background:rgba(184,154,74,.5); margin:16px auto; }
.kits-sub    { font-size:11px; color:#8F9C68; font-style:italic; line-height:1.7; }

/* ── card de kit ── */
.kit-card {
  background:#FAF8F3;
  padding:20px 24px;
  margin-bottom:14px;
  display:flex; justify-content:space-between; align-items:center;
  position:relative;
}
.kit-card.featured { border-left:4px solid #B89A4A; }

.kit-badge {
  position:absolute; top:12px; right:100px;
  font-family:"Courier New",monospace;
  font-size:7px; text-transform:uppercase; letter-spacing:2px;
  background:#B89A4A; color:#1E4B26; padding:3px 9px;
  font-weight:bold;
}

.kit-label {
  font-family:"Courier New",monospace;
  font-size:8px; text-transform:uppercase; letter-spacing:4px; color:#8F9C68;
}
.kit-name  { font-size:18px; font-weight:bold; color:#1E4B26; margin-top:5px; }
.kit-desc  { font-size:9.5px; color:#4F2915; font-style:italic; margin-top:4px; line-height:1.5; }
.kit-unit  {
  display:inline-block; margin-top:8px;
  font-family:"Courier New",monospace; font-size:8.5px;
  color:#1E4B26; background:rgba(143,156,104,.18);
  padding:3px 10px;
}

.kit-price-box { text-align:right; flex-shrink:0; }
.kit-price-lbl {
  font-family:"Courier New",monospace;
  font-size:8px; text-transform:uppercase; letter-spacing:3px; color:#8F9C68;
}
.kit-price-val {
  font-family:"Courier New",monospace;
  font-size:34px; color:#B89A4A; font-weight:bold; line-height:1.1;
}

/* ── rodapé da página de kits ── */
.kits-footer { margin-top:28px; text-align:center; border-top:1px solid rgba(184,154,74,.25); padding-top:22px; }
.kits-footer-notes {
  font-size:10px; color:#8F9C68; font-style:italic; line-height:1.9;
}
.pix-pill {
  display:inline-block; margin-top:14px;
  font-family:"Courier New",monospace; font-size:8.5px;
  text-transform:uppercase; letter-spacing:2px; font-weight:bold;
  background:#B89A4A; color:#1E4B26; padding:5px 18px;
}
.kits-wa-label {
  font-family:"Courier New",monospace;
  font-size:8px; letter-spacing:4px; text-transform:uppercase; color:#8F9C68;
  margin-top:22px; margin-bottom:5px;
}
.kits-wa {
  font-family:"Courier New",monospace;
  font-size:20px; color:#FAF8F3; letter-spacing:3px;
}
.kits-tagline {
  font-size:9px; font-style:italic; color:#8F9C68; margin-top:10px;
}
</style>
</head>
<body>

<!-- ══════════════ CAPA ══════════════ -->
<div class="cover">
  <div class="cover-border"></div>
  <div class="cover-corner tl"></div>
  <div class="cover-corner tr"></div>
  <div class="cover-corner bl"></div>
  <div class="cover-corner br"></div>

  <div class="cover-inner">
    <div class="cover-eyebrow">Marmitas Congeladas Artesanais</div>
    <div class="cover-ornament">✦</div>
    <div class="cover-casa">Casa</div>
    <div class="cover-celi">Celi</div>
    <div class="cover-divider"></div>
    <div class="cover-tagline">
      Congelados com sabor<br>de cozinha afetiva
    </div>
    <div class="cover-ornament" style="margin-top:32px; letter-spacing:10px;">✦ ✦ ✦</div>
  </div>

  <div class="cover-footer">
    <div class="cover-footer-line">Cardápio &amp; Kits · 2025</div>
    <div class="cover-footer-line">WhatsApp (15) 99677-9560</div>
  </div>
</div>


<!-- ══════════════ CARDÁPIO ══════════════ -->
<div class="page">

  <div class="page-header">
    <div class="page-header-eye">Cardápio Completo</div>
    <div class="page-header-brand">Casa Celi · Marmitas Congeladas</div>
  </div>

  <!-- Tradicionais -->
  <div class="section">
    <div class="section-head">
      <span class="section-label">Tradicionais</span>
      <div class="section-rule"></div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Frango Desfiado ao Creme de Milho</div>
        <div class="dish-desc">Frango cozido lentamente e desfiado, envolvido em creme de milho suave com ervas da casa</div>
      </div>
      <div class="dish-price">R$ 20,00</div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Frango em Cubos Acebolado</div>
        <div class="dish-desc">Cubos de peito de frango dourados com cebola caramelizada e temperos especiais</div>
      </div>
      <div class="dish-price">R$ 20,00</div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Almôndegas ao Molho Pomodoro</div>
        <div class="dish-desc">Almôndegas artesanais de carne moída cozidas em molho de tomate fresco com manjericão</div>
      </div>
      <div class="dish-price">R$ 20,00</div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Frango Xadrez da Casa</div>
        <div class="dish-desc">Peito de frango com legumes coloridos no molho agridoce oriental — receita exclusiva</div>
      </div>
      <div class="dish-price">R$ 20,00</div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Filé de Frango ao Molho de Mel</div>
        <div class="dish-desc">Filé grelhado finalizado com molho de mel e mostarda, suculento e aromático</div>
      </div>
      <div class="dish-price">R$ 20,00</div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Filé de Merluza</div>
        <div class="dish-desc">Filé de merluza temperado com limão, alho e ervas frescas, assado no ponto certo</div>
      </div>
      <div class="dish-price">R$ 20,00</div>
    </div>
  </div>

  <!-- Premium -->
  <div class="section">
    <div class="section-head">
      <span class="section-label">Premium</span>
      <div class="section-rule"></div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Parmegiana com Crosta</div>
        <div class="dish-desc">Filé empanado com crosta crocante, molho de tomate encorpado e queijo gratinado</div>
      </div>
      <div class="dish-price">R$ 28,50</div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Nhoque à Bolonhesa</div>
        <div class="dish-desc">Nhoque artesanal de batata com ragù de carne ao molho bolonhesa — feito na hora</div>
      </div>
      <div class="dish-price">R$ 33,50</div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Lasanha Saborosa</div>
        <div class="dish-desc">Montada em camadas com carne moída temperada, molho branco cremoso e queijo</div>
      </div>
      <div class="dish-price">R$ 26,00</div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Escondidinho Caprichado</div>
        <div class="dish-desc">Carne desfiada e temperada escondida sob purê cremoso de mandioca gratinado</div>
      </div>
      <div class="dish-price">R$ 24,50</div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Panquecas Caseiras</div>
        <div class="dish-desc">Panquecas recheadas com frango desfiado ou carne moída, cobertas com molho de tomate</div>
      </div>
      <div class="dish-price">R$ 23,50</div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Macarrões da Casa</div>
        <div class="dish-desc">Massa no ponto certo · molho à escolha: Sugo · Bolonhesa · Alho e Óleo · Bechamel</div>
      </div>
      <div class="dish-price">R$ 24,90</div>
    </div>
  </div>

  <!-- Caldos -->
  <div class="section">
    <div class="section-head">
      <span class="section-label">Caldos Artesanais</span>
      <div class="section-rule"></div>
    </div>

    <div class="dish">
      <div class="dish-left">
        <div class="dish-name">Caldo Artesanal (500 ml)</div>
        <div class="dish-desc">Preparado lentamente com ingredientes frescos · pergunte o sabor disponível</div>
      </div>
      <div class="dish-price">R$ 21,90</div>
    </div>
  </div>

  <!-- Nota gramagem -->
  <div class="size-note">
    <div class="size-note-label">Gramagem &amp; preços — marmitas avulsas (Tradicionais)</div>
    <div class="size-row">
      <div class="size-item"><strong>300 g</strong> · R$ 18,00</div>
      <div class="size-item"><strong>400 g</strong> · R$ 20,00</div>
      <div class="size-item"><strong>500 g</strong> · R$ 22,00</div>
    </div>
    <div class="size-foot">* Pratos Premium têm preço fixo independente da gramagem · Consulte disponibilidade semanal</div>
  </div>

</div>


<!-- ══════════════ KITS ══════════════ -->
<div class="kits-page">

  <div class="kits-header">
    <div class="kits-eye">Monte seu estoque</div>
    <div class="kits-title">Kits Semana</div>
    <div class="kits-div"></div>
    <div class="kits-sub">
      10 marmitas à sua escolha · Praticidade para a semana toda<br>
      Combine diferentes pratos no mesmo kit
    </div>
  </div>

  <!-- Kit 300g -->
  <div class="kit-card">
    <div>
      <div class="kit-label">Kit Semana</div>
      <div class="kit-name">10 Marmitas · 300 g</div>
      <div class="kit-desc">Porção individual · ideal para lanches e refeições leves</div>
      <div class="kit-unit">R$ 18,00 por marmita</div>
    </div>
    <div class="kit-price-box">
      <div class="kit-price-lbl">Total do kit</div>
      <div class="kit-price-val">R$ 180</div>
    </div>
  </div>

  <!-- Kit 400g — destaque -->
  <div class="kit-card featured">
    <div class="kit-badge">Mais Pedido</div>
    <div>
      <div class="kit-label">Kit Semana · ★ Destaque</div>
      <div class="kit-name">10 Marmitas · 400 g</div>
      <div class="kit-desc">Porção completa para adultos · o preferido da Casa Celi</div>
      <div class="kit-unit">R$ 20,00 por marmita</div>
    </div>
    <div class="kit-price-box">
      <div class="kit-price-lbl">Total do kit</div>
      <div class="kit-price-val">R$ 200</div>
    </div>
  </div>

  <!-- Kit 500g -->
  <div class="kit-card">
    <div>
      <div class="kit-label">Kit Família</div>
      <div class="kit-name">10 Marmitas · 500 g</div>
      <div class="kit-desc">Porção generosa · para quem tem mais fome ou divide a refeição</div>
      <div class="kit-unit">R$ 22,00 por marmita</div>
    </div>
    <div class="kit-price-box">
      <div class="kit-price-lbl">Total do kit</div>
      <div class="kit-price-val">R$ 220</div>
    </div>
  </div>

  <div class="kits-footer">
    <div class="kits-footer-notes">
      Validade de 90 dias no freezer · Conservar congelado · Aquecer em banho-maria ou micro-ondas<br>
      Pedido mínimo: 1 kit (10 marmitas) · Kits mistos são bem-vindos
    </div>
    <div><span class="pix-pill">3% OFF pagando com PIX</span></div>

    <div class="kits-wa-label" style="margin-top:28px;">Faça seu pedido pelo WhatsApp</div>
    <div class="kits-wa">(15) 99677-9560</div>
    <div class="kits-tagline">Casa Celi · Congelados com sabor de cozinha afetiva</div>
  </div>

</div>

</body>
</html>"""

output = "/home/user/belle-petit-pet-saloon/CasaCeli_Cardapio_Texto.pdf"

from weasyprint import HTML as WP
WP(string=HTML, base_url=".").write_pdf(output)
print(f"PDF gerado: {output}")
