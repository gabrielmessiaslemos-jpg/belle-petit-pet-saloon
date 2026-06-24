#!/usr/bin/env python3
"""Gera CasaCeli_Cardapio_Texto.pdf — layout sem fotos, descrições e preços."""

# ── preços base ──────────────────────────────────────────────────────────────
BASE = {'300': 18.00, '400': 20.00, '500': 22.00}

def kit_price(g, qty, pct_off):
    return BASE[g] * qty * (1 - pct_off / 100)

def brl(v):
    return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Kits fornecidos pelo cliente (preços fixos)
KIT10 = {'300': 180, '400': 200, '500': 220}
KIT20 = {'300': 340, '400': 400, '500': 440}          # 2% off embutido
KIT30 = {g: round(kit_price(g, 30, 3), 2) for g in BASE}  # 3% off calculado

def row_kit(g):
    u10 = KIT10[g] / 10
    u20 = KIT20[g] / 20
    u30 = KIT30[g] / 30
    return f"""
      <tr>
        <td class="col-g">{g} g</td>
        <td class="col-v">R$ {KIT10[g]}<span class="unit">R$ {u10:.2f}/un</span></td>
        <td class="col-v best">R$ {KIT20[g]}<span class="unit">R$ {u20:.2f}/un</span></td>
        <td class="col-v">R$ {KIT30[g]:.0f}<span class="unit">R$ {u30:.2f}/un</span></td>
      </tr>"""

HTML = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@page {{ size: A4; margin: 0; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body       {{ font-family: Georgia,"Times New Roman",serif; background:#FAF8F3; color:#4F2915; }}

/* ══ CAPA ══ */
.cover {{
  width:210mm; height:297mm; background:#1E4B26;
  display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  page-break-after:always; position:relative;
}}
.cover-border {{ position:absolute; inset:18px; border:1px solid rgba(184,154,74,.35); }}
.cc {{ position:absolute; width:28px; height:28px; border-color:#B89A4A; border-style:solid; }}
.tl {{ top:14px;  left:14px;  border-width:2px 0 0 2px; }}
.tr {{ top:14px;  right:14px; border-width:2px 2px 0 0; }}
.bl {{ bottom:14px; left:14px;  border-width:0 0 2px 2px; }}
.br {{ bottom:14px; right:14px; border-width:0 2px 2px 0; }}
.cover-inner {{ text-align:center; padding:0 60px; }}
.cover-eye   {{ font-family:"Courier New",monospace; font-size:9px; letter-spacing:6px; text-transform:uppercase; color:#8F9C68; margin-bottom:14px; }}
.cover-orn   {{ color:#B89A4A; font-size:18px; margin:18px 0; letter-spacing:6px; }}
.cover-casa  {{ font-size:80px; color:#B89A4A; letter-spacing:6px; line-height:1; text-transform:uppercase; }}
.cover-celi  {{ font-size:54px; color:#FAF8F3; letter-spacing:8px; text-transform:uppercase; margin-top:4px; }}
.cover-div   {{ width:100px; height:1px; background:#B89A4A; margin:28px auto; }}
.cover-tag   {{ font-style:italic; font-size:15px; color:#8F9C68; letter-spacing:.5px; line-height:1.8; }}
.cover-foot  {{ position:absolute; bottom:44px; text-align:center; width:100%; }}
.cover-fline {{ font-family:"Courier New",monospace; font-size:9px; letter-spacing:4px; text-transform:uppercase; color:#FAF8F3; opacity:.6; margin-top:5px; }}

/* ══ PÁGINA CARDÁPIO ══ */
.page {{
  width:210mm; min-height:297mm;
  padding:18mm 18mm 14mm;
  page-break-after:always; background:#FAF8F3;
}}
.ph {{ text-align:center; padding-bottom:16px; margin-bottom:24px; border-bottom:2px solid #1E4B26; }}
.ph-eye   {{ font-family:"Courier New",monospace; font-size:8px; letter-spacing:5px; text-transform:uppercase; color:#8F9C68; }}
.ph-brand {{ font-size:20px; color:#1E4B26; margin-top:4px; }}

.sec {{ margin-bottom:24px; }}
.sh  {{ display:flex; align-items:center; gap:10px; margin-bottom:12px; }}
.sl  {{ font-family:"Courier New",monospace; font-size:8.5px; text-transform:uppercase; letter-spacing:5px; color:#B05216; white-space:nowrap; }}
.sr  {{ flex:1; height:1px; background:rgba(143,156,104,.35); }}

.dish {{ display:flex; justify-content:space-between; align-items:baseline; padding:9px 0; border-bottom:1px dotted rgba(143,156,104,.30); }}
.dish:last-child {{ border-bottom:none; }}
.dl  {{ flex:1; padding-right:16px; }}
.dn  {{ font-size:13.5px; font-weight:bold; color:#1E4B26; line-height:1.3; }}
.dd  {{ font-size:9.5px; color:#4F2915; font-style:italic; margin-top:3px; opacity:.8; line-height:1.5; }}
.dp  {{ font-family:"Courier New",monospace; font-size:13.5px; color:#B89A4A; font-weight:bold; white-space:nowrap; }}

.size-note {{ margin-top:18px; padding:12px 18px; background:rgba(30,75,38,.05); border-left:3px solid #B89A4A; }}
.sn-lbl {{ font-family:"Courier New",monospace; font-size:8px; text-transform:uppercase; letter-spacing:3px; color:#8F9C68; margin-bottom:7px; }}
.sn-row {{ display:flex; gap:28px; }}
.sn-item {{ font-size:11.5px; color:#1E4B26; }}
.sn-foot {{ font-size:8px; color:#4F2915; font-style:italic; margin-top:6px; opacity:.75; }}

/* ══ PÁGINA KITS ══ */
.kits-page {{
  width:210mm; min-height:297mm;
  background:#1E4B26;
  padding:16mm 16mm 12mm;
  page-break-after:always;
}}
.kh {{ text-align:center; margin-bottom:28px; }}
.kh-eye   {{ font-family:"Courier New",monospace; font-size:8px; text-transform:uppercase; letter-spacing:6px; color:#8F9C68; }}
.kh-title {{ font-size:38px; color:#B89A4A; margin-top:6px; letter-spacing:2px; }}
.kh-div   {{ width:70px; height:1px; background:rgba(184,154,74,.5); margin:14px auto; }}
.kh-sub   {{ font-size:11px; color:#8F9C68; font-style:italic; line-height:1.7; }}

/* ── tabela de kits ── */
.kit-table {{ width:100%; border-collapse:collapse; margin-bottom:20px; }}
.kit-table th {{
  font-family:"Courier New",monospace; font-size:8px; text-transform:uppercase;
  letter-spacing:3px; color:#8F9C68; padding:10px 14px 8px;
  border-bottom:1px solid rgba(184,154,74,.3);
}}
.kit-table th.col-qty {{ font-size:11px; color:#B89A4A; letter-spacing:1px; }}
.kit-table th.featured {{ color:#FAF8F3; position:relative; }}
.featured-badge {{
  display:block; font-size:7px; letter-spacing:2px;
  background:#B89A4A; color:#1E4B26; padding:2px 8px;
  margin:0 auto 4px; width:fit-content;
}}
.kit-table td {{ padding:12px 14px; background:#FAF8F3; border-bottom:2px solid #1E4B26; vertical-align:middle; }}
.kit-table tr:last-child td {{ border-bottom:none; }}

.col-g   {{ font-size:13px; font-weight:bold; color:#1E4B26; width:60px; font-family:"Courier New",monospace; }}
.col-v   {{ font-family:"Courier New",monospace; font-size:18px; color:#1E4B26; font-weight:bold; text-align:center; }}
.col-v.best {{ color:#B05216; }}
.unit    {{ display:block; font-size:8.5px; color:#8F9C68; font-weight:normal; margin-top:3px; }}

/* ── desconto progressivo ── */
.disc-bar {{
  display:flex; gap:2px; margin-bottom:22px;
}}
.disc-step {{
  flex:1; padding:10px 12px; background:#FAF8F3; position:relative;
}}
.disc-step.active {{ background:#B89A4A; }}
.disc-n   {{ font-family:"Courier New",monospace; font-size:20px; font-weight:bold; color:#1E4B26; }}
.disc-un  {{ font-family:"Courier New",monospace; font-size:8px; text-transform:uppercase; letter-spacing:2px; color:#8F9C68; }}
.disc-off {{ font-family:"Courier New",monospace; font-size:11px; font-weight:bold; color:#B05216; margin-top:4px; }}
.disc-step.active .disc-off {{ color:#1E4B26; }}
.disc-step.active .disc-un  {{ color:rgba(30,75,38,.7); }}

/* ── notas e footer ── */
.kits-notes {{
  text-align:center; font-size:9.5px; color:#8F9C68;
  font-style:italic; line-height:1.9;
}}
.pix-pill {{
  display:inline-block; margin-top:12px;
  font-family:"Courier New",monospace; font-size:8.5px;
  text-transform:uppercase; letter-spacing:2px; font-weight:bold;
  background:#B89A4A; color:#1E4B26; padding:5px 18px;
}}
.kf {{ margin-top:22px; text-align:center; border-top:1px solid rgba(184,154,74,.25); padding-top:18px; }}
.kf-lbl {{ font-family:"Courier New",monospace; font-size:8px; letter-spacing:4px; text-transform:uppercase; color:#8F9C68; margin-bottom:4px; }}
.kf-wa  {{ font-family:"Courier New",monospace; font-size:20px; color:#FAF8F3; letter-spacing:3px; }}
.kf-tag {{ font-size:9px; font-style:italic; color:#8F9C68; margin-top:8px; }}
</style>
</head>
<body>

<!-- ══════════ CAPA ══════════ -->
<div class="cover">
  <div class="cover-border"></div>
  <div class="cc tl"></div><div class="cc tr"></div>
  <div class="cc bl"></div><div class="cc br"></div>
  <div class="cover-inner">
    <div class="cover-eye">Marmitas Congeladas Artesanais</div>
    <div class="cover-orn">✦</div>
    <div class="cover-casa">Casa</div>
    <div class="cover-celi">Celi</div>
    <div class="cover-div"></div>
    <div class="cover-tag">Congelados com sabor<br>de cozinha afetiva</div>
    <div class="cover-orn" style="margin-top:32px;letter-spacing:10px;">✦ ✦ ✦</div>
  </div>
  <div class="cover-foot">
    <div class="cover-fline">Cardápio &amp; Kits · 2025</div>
    <div class="cover-fline">WhatsApp (15) 99677-9560</div>
  </div>
</div>


<!-- ══════════ CARDÁPIO ══════════ -->
<div class="page">
  <div class="ph">
    <div class="ph-eye">Cardápio Completo</div>
    <div class="ph-brand">Casa Celi · Marmitas Congeladas</div>
  </div>

  <!-- Tradicionais -->
  <div class="sec">
    <div class="sh"><span class="sl">Tradicionais</span><div class="sr"></div></div>
    <div class="dish"><div class="dl"><div class="dn">Frango Desfiado ao Creme de Milho</div><div class="dd">Frango cozido lentamente e desfiado, envolvido em creme de milho suave com ervas da casa</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Frango em Cubos Acebolado</div><div class="dd">Cubos de peito de frango dourados com cebola caramelizada e temperos especiais</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Almôndegas ao Molho Pomodoro</div><div class="dd">Almôndegas artesanais de carne moída cozidas em molho de tomate fresco com manjericão</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Frango Xadrez da Casa</div><div class="dd">Peito de frango com legumes coloridos no molho agridoce oriental — receita exclusiva</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Filé de Frango ao Molho de Mel</div><div class="dd">Filé grelhado finalizado com molho de mel e mostarda, suculento e aromático</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Filé de Merluza</div><div class="dd">Filé de merluza temperado com limão, alho e ervas frescas, assado no ponto certo</div></div><div class="dp">R$ 20,00</div></div>
  </div>

  <!-- Premium -->
  <div class="sec">
    <div class="sh"><span class="sl">Premium</span><div class="sr"></div></div>
    <div class="dish"><div class="dl"><div class="dn">Parmegiana com Crosta</div><div class="dd">Filé empanado com crosta crocante, molho de tomate encorpado e queijo gratinado</div></div><div class="dp">R$ 28,50</div></div>
    <div class="dish"><div class="dl"><div class="dn">Nhoque à Bolonhesa</div><div class="dd">Nhoque artesanal de batata com ragù de carne ao molho bolonhesa — feito na hora</div></div><div class="dp">R$ 33,50</div></div>
    <div class="dish"><div class="dl"><div class="dn">Lasanha Saborosa</div><div class="dd">Montada em camadas com carne moída temperada, molho branco cremoso e queijo</div></div><div class="dp">R$ 26,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Escondidinho Caprichado</div><div class="dd">Carne desfiada e temperada escondida sob purê cremoso de mandioca gratinado</div></div><div class="dp">R$ 24,50</div></div>
    <div class="dish"><div class="dl"><div class="dn">Panquecas Caseiras</div><div class="dd">Panquecas recheadas com frango desfiado ou carne moída, cobertas com molho de tomate</div></div><div class="dp">R$ 23,50</div></div>
    <div class="dish"><div class="dl"><div class="dn">Macarrões da Casa</div><div class="dd">Massa no ponto certo · molho à escolha: Sugo · Bolonhesa · Alho e Óleo · Bechamel</div></div><div class="dp">R$ 24,90</div></div>
  </div>

  <!-- Caldos -->
  <div class="sec">
    <div class="sh"><span class="sl">Caldos Artesanais</span><div class="sr"></div></div>
    <div class="dish"><div class="dl"><div class="dn">Caldo Artesanal (500 ml)</div><div class="dd">Preparado lentamente com ingredientes frescos · pergunte o sabor disponível</div></div><div class="dp">R$ 21,90</div></div>
  </div>

  <!-- Gramagem -->
  <div class="size-note">
    <div class="sn-lbl">Gramagem &amp; preços — marmitas avulsas (Tradicionais)</div>
    <div class="sn-row">
      <div class="sn-item"><strong>300 g</strong> · R$ 18,00</div>
      <div class="sn-item"><strong>400 g</strong> · R$ 20,00</div>
      <div class="sn-item"><strong>500 g</strong> · R$ 22,00</div>
    </div>
    <div class="sn-foot">* Pratos Premium têm preço fixo · Consulte disponibilidade semanal</div>
  </div>
</div>


<!-- ══════════ KITS ══════════ -->
<div class="kits-page">
  <div class="kh">
    <div class="kh-eye">Monte seu estoque</div>
    <div class="kh-title">Kits &amp; Descontos</div>
    <div class="kh-div"></div>
    <div class="kh-sub">Quanto mais você pede, mais você economiza<br>Combine qualquer prato no mesmo kit</div>
  </div>

  <!-- Barra de desconto progressivo -->
  <div class="disc-bar">
    <div class="disc-step">
      <div class="disc-n">10</div>
      <div class="disc-un">marmitas</div>
      <div class="disc-off">Preço base</div>
    </div>
    <div class="disc-step active">
      <div class="disc-n">20</div>
      <div class="disc-un">marmitas</div>
      <div class="disc-off">2% OFF</div>
    </div>
    <div class="disc-step">
      <div class="disc-n">30</div>
      <div class="disc-un">marmitas</div>
      <div class="disc-off">3% OFF</div>
    </div>
  </div>

  <!-- Tabela de preços -->
  <table class="kit-table">
    <thead>
      <tr>
        <th style="text-align:left">Tamanho</th>
        <th class="col-qty">10 marmitas</th>
        <th class="col-qty featured"><span class="featured-badge">⭐ Mais pedido</span>20 marmitas</th>
        <th class="col-qty">30 marmitas</th>
      </tr>
    </thead>
    <tbody>
      {row_kit('300')}
      {row_kit('400')}
      {row_kit('500')}
    </tbody>
  </table>

  <div class="kits-notes">
    Validade de 90 dias no freezer · Conservar congelado<br>
    Aquecer em banho-maria ou micro-ondas · Pedido mínimo: 10 marmitas<br>
    Kits mistos são bem-vindos — escolha diferentes pratos no mesmo kit
  </div>
  <div style="text-align:center"><span class="pix-pill">+ 3% OFF adicional pagando com PIX</span></div>

  <div class="kf">
    <div class="kf-lbl">Faça seu pedido · WhatsApp</div>
    <div class="kf-wa">(15) 99677-9560</div>
    <div class="kf-tag">Casa Celi · Congelados com sabor de cozinha afetiva</div>
  </div>
</div>

</body>
</html>"""

output = "/home/user/belle-petit-pet-saloon/CasaCeli_Cardapio_Texto.pdf"

from weasyprint import HTML as WP
WP(string=HTML, base_url=".").write_pdf(output)
print(f"PDF gerado: {output}")
print(f"Kit 30 marmitas → 300g: R$ {KIT30['300']:.0f} | 400g: R$ {KIT30['400']:.0f} | 500g: R$ {KIT30['500']:.0f}")
