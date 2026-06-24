#!/usr/bin/env python3
"""Gera CasaCeli_Cardapio_Texto.pdf — com logo SVG fiel à marca."""

import math, base64, os

# ── preços avulsas ───────────────────────────────────────────────────────────
BASE = {'300': 18.00, '400': 20.00, '500': 22.00}

# ── preços por kit com desconto progressivo por gramagem ─────────────────────
KIT_SIZES = [
    {'label': '300 ml', 'tiers': [
        {'qty': 10, 'unit': 19, 'off': 'Base',    'total': 190},
        {'qty': 20, 'unit': 18, 'off': '5% OFF',  'total': 360, 'best': True},
        {'qty': 30, 'unit': 17, 'off': '10% OFF', 'total': 510},
    ]},
    {'label': '400 ml', 'tiers': [
        {'qty': 10, 'unit': 21, 'off': 'Base',    'total': 210},
        {'qty': 20, 'unit': 20, 'off': '5% OFF',  'total': 400, 'best': True},
        {'qty': 30, 'unit': 19, 'off': '10% OFF', 'total': 570},
    ]},
    {'label': '500 ml', 'tiers': [
        {'qty': 10, 'unit': 23, 'off': 'Base',    'total': 230},
        {'qty': 20, 'unit': 22, 'off': '5% OFF',  'total': 440, 'best': True},
        {'qty': 30, 'unit': 21, 'off': '10% OFF', 'total': 630},
    ]},
]

def size_cards():
    cards = ''
    for sz in KIT_SIZES:
        rows = ''
        for t in sz['tiers']:
            cls = ' class="best"' if t.get('best') else ''
            rows += (f'<tr{cls}>'
                     f'<td><span class="sc-qty">{t["qty"]}×</span>'
                     f'<br><span class="sc-un">R${t["unit"]},00/un</span></td>'
                     f'<td class="sc-tot">R$ {t["total"]}</td>'
                     f'<td class="sc-off">{t["off"]}</td>'
                     f'</tr>')
        cards += (f'<div class="sc">'
                  f'<div class="sc-hdr">{sz["label"]}</div>'
                  f'<table class="sc-table"><tbody>{rows}</tbody></table>'
                  f'</div>')
    return cards

# ── Logo real em base64 ──────────────────────────────────────────────────────
_logo_path = os.path.join(os.path.dirname(__file__), 'logo_casa_celi_real.png')
_logo_b64  = base64.b64encode(open(_logo_path, 'rb').read()).decode()
_logo_src  = f'data:image/png;base64,{_logo_b64}'

LOGO_SVG = f'<img src="{_logo_src}" style="width:100%;height:100%;object-fit:contain"/>'

# ── CSS ──────────────────────────────────────────────────────────────────────
CSS = """
@page { size: A4; margin: 0; }
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: Georgia,"Times New Roman",serif; background:#FAF8F3; color:#4F2915; }

/* ══ CAPA ══ */
.cover {
  width:210mm; height:297mm;
  background: radial-gradient(ellipse at 50% 40%, #F7EDD5 0%, #EBD9B0 100%);
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  page-break-after:always; position:relative; overflow:hidden;
}
/* folhas decorativas de fundo (como no logo original) */
.cover::before {
  content:'';
  position:absolute; inset:0;
  background-image:
    radial-gradient(ellipse 4px 40px at 20px 60px, rgba(100,130,80,.12) 100%, transparent 100%),
    radial-gradient(ellipse 4px 40px at 780px 200px, rgba(100,130,80,.10) 100%, transparent 100%);
  pointer-events:none;
}
.cover-logo { width:82%; max-width:440px; }
.cover-foot {
  position:absolute; bottom:38px; text-align:center; width:100%;
}
.cover-fline {
  font-family:"Courier New",monospace; font-size:9px; letter-spacing:4px;
  text-transform:uppercase; color:#4F2915; opacity:.5; margin-top:5px;
}

/* ══ PÁGINA ══ */
.page {
  width:210mm; min-height:297mm;
  padding:14mm 18mm 12mm;
  page-break-after:always; background:#FAF8F3;
}
/* cabeçalho com mini-logo */
.ph {
  display:flex; align-items:center; gap:14px;
  padding-bottom:12px; margin-bottom:20px;
  border-bottom:2px solid #2C5F34;
}
.ph-logo { width:52px; height:52px; flex-shrink:0; }
.ph-text {}
.ph-eye   { font-family:"Courier New",monospace; font-size:8px; letter-spacing:5px; text-transform:uppercase; color:#8F9C68; }
.ph-brand { font-size:18px; color:#2C5F34; font-weight:bold; margin-top:2px; }

.sec { margin-bottom:22px; }
.sh  { display:flex; align-items:center; gap:10px; margin-bottom:11px; }
.sl  { font-family:"Courier New",monospace; font-size:8.5px; text-transform:uppercase; letter-spacing:5px; color:#B05216; white-space:nowrap; }
.sr  { flex:1; height:1px; background:rgba(143,156,104,.35); }

.dish { display:flex; justify-content:space-between; align-items:baseline; padding:8px 0; border-bottom:1px dotted rgba(143,156,104,.28); }
.dish:last-child { border-bottom:none; }
.dl { flex:1; padding-right:14px; }
.dn { font-size:13px; font-weight:bold; color:#2C5F34; line-height:1.3; }
.dd { font-size:9.5px; color:#4F2915; font-style:italic; margin-top:3px; opacity:.78; line-height:1.4; }
.dp { font-family:"Courier New",monospace; font-size:13px; color:#B89A4A; font-weight:bold; white-space:nowrap; }

.size-note { margin-top:14px; padding:11px 16px; background:rgba(44,95,52,.05); border-left:3px solid #B89A4A; }
.sn-lbl { font-family:"Courier New",monospace; font-size:8px; text-transform:uppercase; letter-spacing:3px; color:#8F9C68; margin-bottom:6px; }
.sn-row { display:flex; gap:26px; }
.sn-item { font-size:11px; color:#2C5F34; }
.sn-foot { font-size:8px; color:#4F2915; font-style:italic; margin-top:5px; opacity:.7; }

/* ══ KITS ══ */
.kits-page {
  width:210mm; min-height:297mm;
  background:#1E4B26;
  padding:14mm 16mm 12mm;
}
.kh { text-align:center; margin-bottom:24px; }
.kh-logo { width:120px; margin:0 auto 14px; display:block; }
.kh-eye   { font-family:"Courier New",monospace; font-size:8px; text-transform:uppercase; letter-spacing:6px; color:#8F9C68; }
.kh-title { font-size:34px; color:#B89A4A; margin-top:5px; letter-spacing:2px; }
.kh-div   { width:70px; height:1px; background:rgba(184,154,74,.5); margin:12px auto; }
.kh-sub   { font-size:10.5px; color:#8F9C68; font-style:italic; line-height:1.7; }

.disc-bar { display:flex; gap:2px; margin-bottom:18px; }
.ds { flex:1; padding:9px 11px; background:#FAF8F3; }
.ds.act { background:#B89A4A; }
.ds-n   { font-family:"Courier New",monospace; font-size:18px; font-weight:bold; color:#2C5F34; }
.ds-un  { font-family:"Courier New",monospace; font-size:8px; text-transform:uppercase; letter-spacing:2px; color:#8F9C68; }
.ds-off { font-family:"Courier New",monospace; font-size:10px; font-weight:bold; color:#B05216; margin-top:3px; }
.ds.act .ds-off { color:#2C5F34; }
.ds.act .ds-un  { color:rgba(30,75,38,.7); }

.kit-table { width:100%; border-collapse:collapse; margin-bottom:16px; }
.kit-table th {
  font-family:"Courier New",monospace; font-size:8px; text-transform:uppercase;
  letter-spacing:3px; color:#8F9C68; padding:9px 12px 7px;
  border-bottom:1px solid rgba(184,154,74,.3);
}
.kit-table th.feat { color:#FAF8F3; }
.feat-badge { display:block; font-size:6.5px; letter-spacing:2px; background:#B89A4A; color:#1E4B26; padding:2px 6px; margin:0 auto 3px; width:fit-content; }
.kit-table td { padding:10px 12px; background:#FAF8F3; border-bottom:2px solid #1E4B26; vertical-align:middle; }
.kit-table tr:last-child td { border-bottom:none; }
.cg { font-size:13px; font-weight:bold; color:#2C5F34; width:55px; font-family:"Courier New",monospace; }
.cv { font-family:"Courier New",monospace; font-size:17px; color:#2C5F34; font-weight:bold; text-align:center; }
.cv.best { color:#B05216; }
.un { display:block; font-size:8px; color:#8F9C68; font-weight:normal; margin-top:2px; }
.off-badge { font-family:"Courier New",monospace; font-size:11px; font-weight:bold; color:#B05216; text-align:center; }
.cv.best.off-badge { color:#B89A4A; }

.size-cards { display:flex; gap:8px; margin-bottom:16px; }
.sc { flex:1; background:#FAF8F3; overflow:hidden; }
.sc-hdr { background:#B89A4A; color:#1E4B26; font-family:"Courier New",monospace; font-size:8px; text-transform:uppercase; letter-spacing:4px; padding:7px; text-align:center; font-weight:bold; }
.sc-table { width:100%; border-collapse:collapse; }
.sc-table td { padding:8px 8px; border-bottom:1px solid rgba(30,75,38,.08); vertical-align:middle; }
.sc-table tr.best td { background:rgba(176,82,22,.06); }
.sc-table tr:last-child td { border-bottom:none; }
.sc-qty { font-family:"Courier New",monospace; font-weight:bold; color:#1E4B26; font-size:13px; }
.sc-un { color:#8F9C68; font-size:8px; font-family:"Courier New",monospace; }
.sc-tot { font-family:"Courier New",monospace; font-weight:bold; color:#2C5F34; font-size:15px; text-align:right; }
.sc-off { font-size:8px; font-family:"Courier New",monospace; font-weight:bold; color:#B05216; text-align:right; min-width:42px; }
.sc-table tr.best .sc-off { color:#B89A4A; }

.kn { text-align:center; font-size:9.5px; color:#8F9C68; font-style:italic; line-height:1.9; }
.pix { display:inline-block; margin-top:10px; font-family:"Courier New",monospace; font-size:8.5px; text-transform:uppercase; letter-spacing:2px; font-weight:bold; background:#B89A4A; color:#1E4B26; padding:5px 16px; }
.kf { margin-top:20px; text-align:center; border-top:1px solid rgba(184,154,74,.25); padding-top:16px; }
.kf-lbl { font-family:"Courier New",monospace; font-size:8px; letter-spacing:4px; text-transform:uppercase; color:#8F9C68; margin-bottom:4px; }
.kf-wa  { font-family:"Courier New",monospace; font-size:20px; color:#FAF8F3; letter-spacing:3px; }
.kf-tag { font-size:9px; font-style:italic; color:#8F9C68; margin-top:7px; }
"""

MINI_LOGO = f'<img src="{_logo_src}" style="width:100%;height:100%;object-fit:contain"/>'


HTML = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>{CSS}</style>
</head>
<body>

<!-- ══════════ CAPA ══════════ -->
<div class="cover">
  <div class="cover-logo">{LOGO_SVG}</div>
  <div class="cover-foot">
    <div class="cover-fline">Cardápio &amp; Kits · 2025</div>
    <div class="cover-fline">WhatsApp (15) 99677-9560</div>
  </div>
</div>


<!-- ══════════ CARDÁPIO ══════════ -->
<div class="page">

  <div class="ph">
    <div class="ph-logo">{MINI_LOGO}</div>
    <div class="ph-text">
      <div class="ph-eye">Cardápio Completo</div>
      <div class="ph-brand">Casa Celi · Marmitas Congeladas</div>
    </div>
  </div>

  <div class="sec">
    <div class="sh"><span class="sl">Tradicionais</span><div class="sr"></div></div>
    <div class="dish"><div class="dl"><div class="dn">Frango Desfiado ao Creme de Milho</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Frango em Cubos Acebolado</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Almôndegas ao Molho Pomodoro</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Frango Xadrez da Casa</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Filé de Frango ao Molho de Mel</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Filé de Merluza</div></div><div class="dp">R$ 20,00</div></div>
  </div>

  <div class="sec">
    <div class="sh"><span class="sl">Premium</span><div class="sr"></div></div>
    <div class="dish"><div class="dl"><div class="dn">Parmegiana com Crosta</div></div><div class="dp">R$ 28,50</div></div>
    <div class="dish"><div class="dl"><div class="dn">Nhoque à Bolonhesa</div></div><div class="dp">R$ 33,50</div></div>
    <div class="dish"><div class="dl"><div class="dn">Lasanha Saborosa</div></div><div class="dp">R$ 26,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Escondidinho Caprichado</div></div><div class="dp">R$ 24,50</div></div>
    <div class="dish"><div class="dl"><div class="dn">Panquecas Caseiras</div></div><div class="dp">R$ 23,50</div></div>
    <div class="dish"><div class="dl"><div class="dn">Macarrões da Casa</div></div><div class="dp">R$ 24,90</div></div>
  </div>

  <div class="sec">
    <div class="sh"><span class="sl">Caldos Artesanais</span><div class="sr"></div></div>
    <div class="dish"><div class="dl"><div class="dn">Caldo Artesanal (500 ml)</div></div><div class="dp">R$ 21,90</div></div>
  </div>

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
    <div class="kh-logo">{MINI_LOGO}</div>
    <div class="kh-eye">Monte seu estoque</div>
    <div class="kh-title">Kits &amp; Descontos</div>
    <div class="kh-div"></div>
    <div class="kh-sub">Quanto mais você pede, mais você economiza<br>Combine qualquer prato no mesmo kit</div>
  </div>

  <div class="disc-bar">
    <div class="ds"><div class="ds-n">10×</div><div class="ds-un">Kit · Preço base</div><div class="ds-off">sem desconto</div></div>
    <div class="ds act"><div class="ds-n">20×</div><div class="ds-un">Kit · Melhor valor</div><div class="ds-off">5% OFF ★</div></div>
    <div class="ds"><div class="ds-n">30×</div><div class="ds-un">Kit · Máx. economia</div><div class="ds-off">10% OFF</div></div>
  </div>

  <div class="size-cards">
    {size_cards()}
  </div>

  <div class="kn">
    Validade de 90 dias no freezer · Conservar congelado<br>
    Aquecer em banho-maria ou micro-ondas · Pedido mínimo: 10 marmitas<br>
    Kits mistos são bem-vindos — escolha diferentes pratos no mesmo kit
  </div>
  <div style="text-align:center"><span class="pix">+ 3% OFF adicional pagando com PIX</span></div>

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
print(f"OK → {output}")
