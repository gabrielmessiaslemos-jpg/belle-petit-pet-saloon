#!/usr/bin/env python3
"""Gera CasaCeli_Cardapio_Texto.pdf — design premium com logo real."""

import base64, os

# ── Cores da marca ────────────────────────────────────────────────────────────
VERDE    = '#1E4B26'
OLIVA    = '#8F9C68'
TERRA    = '#B05216'
MARROM   = '#4F2915'
DOURADO  = '#B89A4A'
FUNDO    = '#FAF8F3'
FUNDO2   = '#F0E8D5'

# ── Preços por kit com desconto progressivo por gramagem ─────────────────────
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

# ── Logos em base64 ───────────────────────────────────────────────────────────
_base = os.path.dirname(__file__)
_logo_b64       = base64.b64encode(open(f'{_base}/logo_casa_celi_real.png',   'rb').read()).decode()
_logo_transp_b64= base64.b64encode(open(f'{_base}/logo_casa_celi_transp.png', 'rb').read()).decode()
_logo_full  = f'data:image/png;base64,{_logo_b64}'
_logo_transp= f'data:image/png;base64,{_logo_transp_b64}'

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: Georgia,"Times New Roman",serif; background:{FUNDO}; color:{MARROM}; }}

/* ════════════════════ CAPA ════════════════════ */
.cover {{
  width:210mm; height:297mm;
  background: linear-gradient(175deg, {FUNDO} 0%, {FUNDO2} 55%, #D9C89A 100%);
  display:flex; flex-direction:column; align-items:center;
  page-break-after:always; position:relative; overflow:hidden;
}}

/* Borda interna decorativa */
.cover-frame {{
  position:absolute;
  top:14mm; left:14mm; right:14mm; bottom:14mm;
  border:1px solid rgba(180,154,74,.35);
  pointer-events:none;
}}
.cover-frame::before {{
  content:'';
  position:absolute;
  top:5px; left:5px; right:5px; bottom:5px;
  border:1px solid rgba(180,154,74,.18);
}}

/* Faixa superior escura */
.cover-top {{
  width:100%; background:{VERDE};
  padding:18px 0 14px;
  text-align:center;
  flex-shrink:0;
}}
.cover-top-label {{
  font-family:"Courier New",monospace;
  font-size:7.5px; letter-spacing:7px; text-transform:uppercase;
  color:rgba(250,248,243,.55);
}}

/* Logo central */
.cover-body {{
  flex:1; display:flex; flex-direction:column;
  align-items:center; justify-content:center;
  padding:0 30px;
}}
.cover-logo-wrap {{
  width:320px; height:320px;
  display:flex; align-items:center; justify-content:center;
  margin-bottom:22px;
}}
.cover-logo-wrap img {{
  width:100%; height:100%; object-fit:contain;
}}

.cover-brand {{
  font-family:Georgia,serif;
  font-size:36px; font-weight:bold; letter-spacing:3px;
  color:{VERDE}; text-align:center; line-height:1.1;
}}
.cover-tagline {{
  margin-top:10px;
  font-size:11px; font-style:italic; color:{MARROM};
  text-align:center; opacity:.75; letter-spacing:.5px;
}}
.cover-divider {{
  display:flex; align-items:center; gap:10px;
  margin:18px 0;
}}
.cover-divider-line {{
  width:60px; height:1px; background:{DOURADO}; opacity:.6;
}}
.cover-divider-dot {{
  width:5px; height:5px; border-radius:50%; background:{DOURADO};
}}

/* Rodapé da capa */
.cover-foot {{
  width:100%; background:{VERDE};
  padding:12px 0 14px; text-align:center;
  flex-shrink:0;
}}
.cover-foot-line {{
  font-family:"Courier New",monospace;
  font-size:8px; letter-spacing:4px; text-transform:uppercase;
  color:rgba(250,248,243,.6); margin-top:4px;
}}
.cover-foot-wa {{
  font-family:"Courier New",monospace;
  font-size:14px; letter-spacing:3px;
  color:{DOURADO}; margin-top:6px;
}}

/* ════════════════════ PÁGINA CARDÁPIO ════════════════════ */
.page {{
  width:210mm; min-height:297mm;
  padding:0 0 12mm;
  page-break-after:always; background:{FUNDO};
}}

/* Cabeçalho de página */
.ph {{
  background:{VERDE};
  padding:10px 18mm 10px;
  display:flex; align-items:center; gap:18px;
  margin-bottom:22px;
}}
.ph-logo {{
  width:80px; height:80px; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
}}
.ph-logo img {{ width:100%; height:100%; object-fit:contain; }}
.ph-divider {{ width:1px; height:60px; background:rgba(250,248,243,.2); flex-shrink:0; }}
.ph-text {{ flex:1; }}
.ph-eye   {{
  font-family:"Courier New",monospace; font-size:7.5px;
  letter-spacing:5px; text-transform:uppercase; color:{OLIVA};
}}
.ph-brand {{
  font-size:20px; color:{FUNDO}; font-weight:bold;
  margin-top:3px; letter-spacing:1px;
}}

.page-body {{ padding:0 18mm; }}

.sec {{ margin-bottom:20px; }}
.sh  {{ display:flex; align-items:center; gap:12px; margin-bottom:12px; }}
.sl  {{
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:5px;
  color:{TERRA}; white-space:nowrap;
}}
.sr  {{ flex:1; height:1px; background:rgba(143,156,104,.3); }}

.dish {{
  display:flex; justify-content:space-between; align-items:center;
  padding:9px 12px; margin-bottom:2px;
  border-bottom:1px dotted rgba(143,156,104,.22);
}}
.dish:last-child {{ border-bottom:none; }}
.dish:hover {{ background:rgba(44,95,52,.03); }}
.dn {{ font-size:13px; font-weight:bold; color:{VERDE}; }}
.dp {{
  font-family:"Courier New",monospace; font-size:13px;
  color:{DOURADO}; font-weight:bold; white-space:nowrap;
  background:rgba(184,154,74,.08); padding:3px 10px;
  border-radius:2px;
}}

.size-note {{
  margin:20px 18mm 0;
  padding:12px 16px;
  background:rgba(44,95,52,.04);
  border-left:3px solid {DOURADO};
}}
.sn-lbl  {{
  font-family:"Courier New",monospace; font-size:7.5px;
  text-transform:uppercase; letter-spacing:3px;
  color:{OLIVA}; margin-bottom:8px;
}}
.sn-row  {{ display:flex; gap:28px; }}
.sn-item {{ font-size:12px; color:{VERDE}; font-weight:bold; }}
.sn-item span {{ font-weight:normal; color:{MARROM}; font-size:11px; }}
.sn-foot {{
  font-size:8px; color:{MARROM}; font-style:italic;
  margin-top:6px; opacity:.65;
}}

/* Rodapé de página */
.page-footer {{
  margin:22px 18mm 0;
  padding-top:10px;
  border-top:1px solid rgba(143,156,104,.25);
  display:flex; justify-content:space-between; align-items:center;
}}
.pf-brand {{ font-size:9px; color:{OLIVA}; font-style:italic; }}
.pf-wa    {{
  font-family:"Courier New",monospace;
  font-size:9px; color:{VERDE}; letter-spacing:1.5px;
}}

/* ════════════════════ PÁGINA KITS ════════════════════ */
.kits-page {{
  width:210mm; min-height:297mm;
  background:{VERDE};
  padding:0 0 14mm;
}}

/* Cabeçalho kits */
.kh {{
  background:rgba(0,0,0,.18);
  padding:20px 16mm 18px;
  text-align:center; margin-bottom:20px;
  display:flex; flex-direction:column; align-items:center;
}}
.kh-logo {{
  width:140px; height:140px;
  margin-bottom:14px;
  display:flex; align-items:center; justify-content:center;
}}
.kh-logo img {{ width:100%; height:100%; object-fit:contain; }}
.kh-eye   {{
  font-family:"Courier New",monospace; font-size:7.5px;
  text-transform:uppercase; letter-spacing:6px; color:{OLIVA};
}}
.kh-title {{
  font-size:30px; color:{DOURADO}; margin-top:5px; letter-spacing:2px;
}}
.kh-div   {{
  width:50px; height:1px;
  background:rgba(184,154,74,.45); margin:10px auto;
}}
.kh-sub   {{ font-size:10px; color:{OLIVA}; font-style:italic; line-height:1.7; }}

/* Barras de desconto */
.disc-bar {{ display:flex; gap:2px; margin:0 16mm 16px; }}
.ds {{
  flex:1; padding:10px 12px;
  background:rgba(250,248,243,.07);
  border-top:2px solid transparent;
}}
.ds.act {{ background:rgba(184,154,74,.15); border-top-color:{DOURADO}; }}
.ds-n   {{
  font-family:"Courier New",monospace; font-size:22px;
  font-weight:bold; color:{FUNDO};
}}
.ds-un  {{
  font-family:"Courier New",monospace; font-size:7.5px;
  text-transform:uppercase; letter-spacing:1.5px; color:{OLIVA};
  margin-top:2px;
}}
.ds-off {{ font-family:"Courier New",monospace; font-size:10px; font-weight:bold; color:{TERRA}; margin-top:4px; }}
.ds.act .ds-off {{ color:{DOURADO}; }}

/* Cards de tamanho */
.size-cards {{ display:flex; gap:8px; margin:0 16mm 16px; }}
.sc {{ flex:1; background:{FUNDO}; overflow:hidden; border-radius:2px; }}
.sc-hdr {{
  background:{DOURADO}; color:{VERDE};
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:4px;
  padding:8px; text-align:center; font-weight:bold;
}}
.sc-table {{ width:100%; border-collapse:collapse; }}
.sc-table td {{
  padding:9px 8px;
  border-bottom:1px solid rgba(30,75,38,.07);
  vertical-align:middle;
}}
.sc-table tr.best td {{ background:rgba(176,82,22,.05); }}
.sc-table tr:last-child td {{ border-bottom:none; }}
.sc-qty {{ font-family:"Courier New",monospace; font-weight:bold; color:{VERDE}; font-size:14px; }}
.sc-un  {{ color:{OLIVA}; font-size:8px; font-family:"Courier New",monospace; }}
.sc-tot {{ font-family:"Courier New",monospace; font-weight:bold; color:{VERDE}; font-size:16px; text-align:right; }}
.sc-off {{ font-size:8px; font-family:"Courier New",monospace; font-weight:bold; color:{TERRA}; text-align:right; min-width:44px; }}
.sc-table tr.best .sc-off {{ color:{DOURADO}; }}

/* Notas e rodapé */
.kn {{
  text-align:center; font-size:9.5px; color:{OLIVA};
  font-style:italic; line-height:1.9; margin:0 16mm 10px;
}}
.pix {{
  display:inline-block; margin-top:6px;
  font-family:"Courier New",monospace; font-size:8.5px;
  text-transform:uppercase; letter-spacing:2px; font-weight:bold;
  background:{DOURADO}; color:{VERDE}; padding:5px 18px;
}}
.kf {{
  margin:16px 16mm 0;
  text-align:center;
  border-top:1px solid rgba(184,154,74,.2);
  padding-top:16px;
}}
.kf-lbl {{ font-family:"Courier New",monospace; font-size:7.5px; letter-spacing:4px; text-transform:uppercase; color:{OLIVA}; margin-bottom:6px; }}
.kf-wa  {{ font-family:"Courier New",monospace; font-size:22px; color:{FUNDO}; letter-spacing:4px; }}
.kf-tag {{ font-size:9px; font-style:italic; color:{OLIVA}; margin-top:8px; }}
"""

# ── HTML ──────────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>

<!-- ══════════════════════════ CAPA ══════════════════════════ -->
<div class="cover">
  <div class="cover-frame"></div>

  <div class="cover-top">
    <div class="cover-top-label">Marmitas Congeladas Artesanais</div>
  </div>

  <div class="cover-body">
    <div class="cover-logo-wrap">
      <img src="{_logo_full}" alt="Casa Celi"/>
    </div>

    <div class="cover-brand">Casa Celi</div>
    <div class="cover-tagline">Comida feita hoje para facilitar o seu amanhã</div>

    <div class="cover-divider">
      <div class="cover-divider-line"></div>
      <div class="cover-divider-dot"></div>
      <div class="cover-divider-line"></div>
    </div>

    <div style="font-family:'Courier New',monospace;font-size:8px;letter-spacing:5px;text-transform:uppercase;color:{OLIVA};text-align:center;">
      Cardápio &amp; Tabela de Kits · 2025
    </div>
  </div>

  <div class="cover-foot">
    <div class="cover-foot-line">Peça pelo WhatsApp</div>
    <div class="cover-foot-wa">(15) 99677-9560</div>
    <div class="cover-foot-line" style="margin-top:8px;">Sob encomenda · Entrega programada · Freezer por 90 dias</div>
  </div>
</div>


<!-- ══════════════════════════ CARDÁPIO ══════════════════════════ -->
<div class="page">

  <div class="ph">
    <div class="ph-logo"><img src="{_logo_transp}" alt=""/></div>
    <div class="ph-divider"></div>
    <div class="ph-text">
      <div class="ph-eye">Cardápio Completo</div>
      <div class="ph-brand">Casa Celi · Marmitas Congeladas</div>
    </div>
  </div>

  <div class="page-body">

    <div class="sec">
      <div class="sh"><span class="sl">Tradicionais</span><div class="sr"></div></div>
      <div class="dish"><div class="dn">Frango Desfiado ao Creme de Milho</div><div class="dp">R$ 20,00</div></div>
      <div class="dish"><div class="dn">Frango em Cubos Acebolado</div><div class="dp">R$ 20,00</div></div>
      <div class="dish"><div class="dn">Almôndegas ao Molho Pomodoro</div><div class="dp">R$ 20,00</div></div>
      <div class="dish"><div class="dn">Frango Xadrez da Casa</div><div class="dp">R$ 20,00</div></div>
      <div class="dish"><div class="dn">Filé de Frango ao Molho de Mel</div><div class="dp">R$ 20,00</div></div>
      <div class="dish"><div class="dn">Filé de Merluza</div><div class="dp">R$ 20,00</div></div>
    </div>

    <div class="sec">
      <div class="sh"><span class="sl">Premium</span><div class="sr"></div></div>
      <div class="dish"><div class="dn">Parmegiana com Crosta</div><div class="dp">R$ 28,50</div></div>
      <div class="dish"><div class="dn">Nhoque à Bolonhesa</div><div class="dp">R$ 33,50</div></div>
      <div class="dish"><div class="dn">Lasanha Saborosa</div><div class="dp">R$ 26,00</div></div>
      <div class="dish"><div class="dn">Escondidinho Caprichado</div><div class="dp">R$ 24,50</div></div>
      <div class="dish"><div class="dn">Panquecas Caseiras</div><div class="dp">R$ 23,50</div></div>
      <div class="dish"><div class="dn">Macarrões da Casa</div><div class="dp">R$ 24,90</div></div>
    </div>

    <div class="sec">
      <div class="sh"><span class="sl">Caldos Artesanais</span><div class="sr"></div></div>
      <div class="dish"><div class="dn">Caldo Artesanal (500 ml)</div><div class="dp">R$ 21,90</div></div>
    </div>

  </div>

  <div class="size-note">
    <div class="sn-lbl">Gramagem &amp; preços — marmitas avulsas (Tradicionais)</div>
    <div class="sn-row">
      <div class="sn-item">300 g <span>· R$ 18,00</span></div>
      <div class="sn-item">400 g <span>· R$ 20,00</span></div>
      <div class="sn-item">500 g <span>· R$ 22,00</span></div>
    </div>
    <div class="sn-foot">* Pratos Premium têm preço fixo · Consulte disponibilidade semanal</div>
  </div>

  <div class="page-footer">
    <div class="pf-brand">Casa Celi · Congelados Artesanais</div>
    <div class="pf-wa">(15) 99677-9560</div>
  </div>

</div>


<!-- ══════════════════════════ KITS ══════════════════════════ -->
<div class="kits-page">

  <div class="kh">
    <div class="kh-logo"><img src="{_logo_transp}" alt=""/></div>
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

  <div class="size-cards">{size_cards()}</div>

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
