#!/usr/bin/env python3
"""Casa Celi — PDF comercial completo 5 páginas (v2 corrigido)."""

import base64, os

# ── Identidade ────────────────────────────────────────────────────────────────
NOME    = "Casa Celi"
CIDADE  = "Sorocaba · SP"
WA      = "(15) 99677-9560"
TAGLINE = "Comida feita hoje para facilitar o seu amanhã"

# ── Cores ─────────────────────────────────────────────────────────────────────
VERDE   = '#1E4B26'
OLIVA   = '#8F9C68'
TERRA   = '#B05216'
MARROM  = '#4F2915'
DOURADO = '#B89A4A'
FUNDO   = '#FAF8F3'
FUNDO2  = '#F0E8D5'
CREME   = '#EBD9B0'

# ── Cardápio ──────────────────────────────────────────────────────────────────
TRADICIONAIS = [
    ("Frango Desfiado ao Creme de Milho", "R$ 20,00"),
    ("Frango em Cubos Acebolado",         "R$ 20,00"),
    ("Almôndegas ao Molho Pomodoro",      "R$ 20,00"),
    ("Frango Xadrez da Casa",             "R$ 20,00"),
    ("Filé de Frango ao Molho de Mel",    "R$ 20,00"),
    ("Filé de Merluza",                   "R$ 20,00"),
    ("Frango Desfiado com Cenoura", "R$ 20,00", "Arroz, feijão e misto de brócolis com couve-flor"),
    ("Carne Moída Refogada",        "R$ 20,00", "Purê de mandioquinha e misto de cenoura com vagem"),
    ("Estrogonofe de Frango",       "R$ 20,00", "Acompanha arroz branco"),
    ("Almôndegas ao Molho",         "R$ 20,00", "Arroz, feijão e misto de vagem com cenoura"),
    ("Macarrão à Bolonhesa",        "R$ 20,00", "Ao molho bolonhesa"),
]
PREMIUM = [
    ("Frango à Parmegiana da Casa",          "R$ 28,50"),
    ("Nhoque Artesanal à Bolonhesa",         "R$ 33,50"),
    ("Lasanha Caseira à Bolonhesa",          "R$ 26,00"),
    ("Escondidinho Cremoso Gratinado",       "R$ 24,50"),
    ("Panquecas Artesanais ao Molho da Casa","R$ 23,50"),
    ("Massas Especiais Casa Celi",           "R$ 24,90"),
]
CALDOS = [
    ("Caldo Artesanal (500 ml)", "R$ 21,90"),
]

# ── Kits (gramas, não ml) ──────────────────────────────────────────────────────
KIT_TIERS = [
    {
        'name': 'Kit 10', 'qty': 10, 'badge': None, 'featured': False,
        'sizes': [
            {'label': '300 g', 'unit': 19, 'total': 190},
            {'label': '400 g', 'unit': 21, 'total': 210},
            {'label': '500 g', 'unit': 23, 'total': 230},
        ]
    },
    {
        'name': 'Kit 20', 'qty': 20, 'badge': 'MAIS POPULAR', 'featured': True,
        'sizes': [
            {'label': '300 g', 'unit': 18, 'total': 360},
            {'label': '400 g', 'unit': 20, 'total': 400},
            {'label': '500 g', 'unit': 22, 'total': 440},
        ]
    },
    {
        'name': 'Kit 30', 'qty': 30, 'badge': '10% OFF', 'featured': False,
        'sizes': [
            {'label': '300 g', 'unit': 17, 'total': 510},
            {'label': '400 g', 'unit': 19, 'total': 570},
            {'label': '500 g', 'unit': 21, 'total': 630},
        ]
    },
]

# ── Logo ──────────────────────────────────────────────────────────────────────
_base     = os.path.dirname(os.path.abspath(__file__))
_logo_b64 = base64.b64encode(open(f'{_base}/logo_casa_celi_real.png', 'rb').read()).decode()
LOGO      = f'data:image/png;base64,{_logo_b64}'

# Selo circular (capa e kits)
# Dois divs: externo = borda dourada visível; interno = clip circular da imagem
def logo_seal(size=130, padding=8, border_w=2):
    clip = size - border_w * 2 - padding * 2
    return (
        f'<div style="width:{size}px;height:{size}px;'
        f'border-radius:50%;border:{border_w}px solid {DOURADO};'
        f'background:{FUNDO};'
        f'display:flex;align-items:center;justify-content:center;'
        f'flex-shrink:0;">'
        f'<div style="width:{clip}px;height:{clip}px;'
        f'border-radius:50%;overflow:hidden;">'
        f'<img src="{LOGO}" style="width:100%;height:100%;object-fit:cover;display:block;"/>'
        f'</div>'
        f'</div>'
    )

# Logo quadrado para cabeçalhos (evita sobreposição)
def logo_header(size=56):
    inner = size - 8
    return (
        f'<div style="width:{size}px;height:{size}px;flex-shrink:0;'
        f'background:{FUNDO};border:1px solid {DOURADO};'
        f'display:flex;align-items:center;justify-content:center;padding:4px;">'
        f'<img src="{LOGO}" style="width:{inner}px;height:{inner}px;'
        f'object-fit:contain;display:block;"/>'
        f'</div>'
    )

# ── Ícones SVG embutidos ───────────────────────────────────────────────────────
ICO_HEART = (
    '<svg width="28" height="28" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3'
    'c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5'
    'c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="#1E4B26"/>'
    '</svg>'
)
ICO_SNOW = (
    '<svg width="28" height="28" viewBox="0 0 26 26" xmlns="http://www.w3.org/2000/svg">'
    '<g stroke="#1E4B26" stroke-width="2" stroke-linecap="round" fill="none">'
    '<line x1="13" y1="2" x2="13" y2="24"/>'
    '<line x1="2" y1="13" x2="24" y2="13"/>'
    '<line x1="5" y1="5" x2="21" y2="21"/>'
    '<line x1="21" y1="5" x2="5" y2="21"/>'
    '<line x1="13" y1="2" x2="10" y2="5"/><line x1="13" y1="2" x2="16" y2="5"/>'
    '<line x1="13" y1="24" x2="10" y2="21"/><line x1="13" y1="24" x2="16" y2="21"/>'
    '<line x1="2" y1="13" x2="5" y2="10"/><line x1="2" y1="13" x2="5" y2="16"/>'
    '<line x1="24" y1="13" x2="21" y2="10"/><line x1="24" y1="13" x2="21" y2="16"/>'
    '</g>'
    '</svg>'
)
ICO_BOLT = (
    '<svg width="28" height="28" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M7 2v11h3v9l7-12h-4l4-8z" fill="#1E4B26"/>'
    '</svg>'
)

# ── Helpers ───────────────────────────────────────────────────────────────────
def dish_rows(lista, preco=True):
    rows = []
    for item in lista:
        n, p = item[0], item[1]
        desc       = f'<div class="dd">{item[2]}</div>' if len(item) > 2 else ''
        price_html = f'<div class="dp">{p}</div>' if preco else ''
        rows.append(
            f'<div class="dish">'
            f'<div class="dn-wrap"><div class="dn">{n}</div>{desc}</div>'
            f'{price_html}'
            f'</div>'
        )
    return ''.join(rows)

def tier_cards():
    cards = ''
    for t in KIT_TIERS:
        feat  = ' featured' if t['featured'] else ''
        u_min = min(s['unit'] for s in t['sizes'])
        u_max = max(s['unit'] for s in t['sizes'])
        # Badge: espaço reservado mesmo quando vazio para alinhar os três cards
        if t['badge']:
            badge_html = (f'<div class="tc-badge-area">'
                          f'<span class="tc-badge">{t["badge"]}</span>'
                          f'</div>')
        else:
            badge_html = '<div class="tc-badge-area"></div>'
        rows = ''.join(
            f'<div class="tc-row">'
            f'<span class="tc-size">{s["label"]}</span>'
            f'<span class="tc-total">R$ {s["total"]}</span>'
            f'</div>'
            for s in t['sizes']
        )
        cards += (
            f'<div class="tc{feat}">'
            f'{badge_html}'
            f'<div class="tc-head">'
            f'<div class="tc-kit-name">{t["name"]}</div>'
            f'<div class="tc-marmitas">{t["qty"]} marmitas</div>'
            f'<div class="tc-price">R$ {u_min}–{u_max}<span class="tc-un"> /un</span></div>'
            f'</div>'
            f'<div class="tc-body">{rows}</div>'
            f'</div>'
        )
    return cards

def page_header(eye, title):
    """Cabeçalho de página com logo de dimensões fixas — sem sobreposição."""
    return (
        f'<div style="background:{VERDE};padding:11px 18mm;display:flex;'
        f'align-items:center;gap:14px;min-height:80px;">'
        f'{logo_header(56)}'
        f'<div style="width:1px;height:48px;background:rgba(250,248,243,.18);flex-shrink:0;"></div>'
        f'<div style="flex:1;min-width:0;">'
        f'<div class="ph-eye">{eye}</div>'
        f'<div class="ph-title">{title}</div>'
        f'</div>'
        f'</div>'
    )

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: Georgia,"Times New Roman",serif; color:{MARROM}; }}

/* ═══════ UTILITÁRIOS ═══════ */
.page-break {{ page-break-after:always; }}

/* ═══════ CABEÇALHO ═══════ */
.ph-eye {{
  font-family:"Courier New",monospace; font-size:7.5px;
  letter-spacing:3px; text-transform:uppercase; color:{OLIVA};
  margin-bottom:3px;
}}
.ph-title {{
  font-size:18px; color:{FUNDO}; font-weight:bold; line-height:1.2;
}}

/* ═══════ PÁGINA GENÉRICA ═══════ */
.page {{
  width:210mm; min-height:297mm;
  background:{FUNDO};
  display:flex; flex-direction:column;
}}
.page-body {{ flex:1; padding:18px 18mm 14px; }}

.page-foot {{
  padding:9px 18mm;
  border-top:1px solid rgba(143,156,104,.22);
  display:flex; justify-content:space-between; align-items:center;
  flex-shrink:0;
}}
.pf-brand {{ font-size:8px; color:{OLIVA}; font-style:italic; }}
.pf-wa    {{ font-family:"Courier New",monospace; font-size:9px; color:{VERDE}; letter-spacing:1px; }}

/* ═══════ CAPA (P1) ═══════ */
.cover {{
  width:210mm; height:297mm;
  background: linear-gradient(170deg, {FUNDO} 0%, {FUNDO2} 60%, {CREME} 100%);
  display:flex; flex-direction:column;
  overflow:hidden;
}}
.cover-stripe {{
  background:{VERDE}; padding:12px 0; text-align:center; flex-shrink:0;
}}
.cover-stripe-label {{
  font-family:"Courier New",monospace; font-size:7px;
  letter-spacing:4px; text-transform:uppercase; color:rgba(250,248,243,.55);
}}
.cover-center {{
  flex:1; display:flex; flex-direction:column;
  align-items:center; justify-content:center; padding:30px;
}}
.cover-brand {{
  font-size:46px; font-weight:bold; color:{VERDE};
  letter-spacing:3px; margin-top:18px; text-align:center;
}}
.cover-sub {{
  font-family:"Courier New",monospace; font-size:8.5px;
  text-transform:uppercase; letter-spacing:4px;
  color:{OLIVA}; margin-top:5px; text-align:center;
}}
.cover-tagline {{
  font-size:13px; font-style:italic; color:{MARROM};
  text-align:center; margin-top:14px; line-height:1.7;
  opacity:.8; max-width:320px;
}}
.cover-ornament {{
  display:flex; align-items:center; gap:12px; margin:18px 0;
}}
.cover-orn-line {{ width:55px; height:1px; background:{DOURADO}; opacity:.5; }}
.cover-orn-dot  {{ font-family:"Courier New",monospace; font-size:10px; color:{DOURADO}; }}
.cover-city {{
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:3px;
  color:{OLIVA}; text-align:center; margin-top:6px;
}}
.cover-foot {{
  background:{VERDE}; padding:14px 0 16px; text-align:center; flex-shrink:0;
}}
.cover-foot-label {{
  font-family:"Courier New",monospace; font-size:7.5px;
  letter-spacing:3px; text-transform:uppercase; color:rgba(250,248,243,.5);
}}
.cover-foot-wa {{
  font-family:"Courier New",monospace; font-size:22px;
  color:{DOURADO}; letter-spacing:3px; margin:5px 0;
}}
.cover-foot-sub {{
  font-family:"Courier New",monospace; font-size:7px;
  text-transform:uppercase; letter-spacing:3px; color:rgba(250,248,243,.35);
}}

/* ═══════ APRESENTAÇÃO (P2) ═══════ */
.intro-text {{
  background:rgba(44,95,52,.04);
  border-left:3px solid {DOURADO};
  padding:13px 17px; margin-bottom:20px;
  font-size:12px; line-height:1.8; color:{MARROM};
}}
.intro-text p + p {{ margin-top:9px; }}

.sec-title {{
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:3px;
  color:{TERRA}; text-align:center; margin-bottom:14px;
}}
.sec-divider {{
  display:flex; align-items:center; gap:10px; margin-bottom:14px;
}}
.sec-divider-line {{ flex:1; height:1px; background:rgba(143,156,104,.28); }}
.sec-divider-dot  {{ width:4px; height:4px; border-radius:50%; background:{DOURADO}; flex-shrink:0; }}

.benefits {{ display:flex; gap:10px; margin-bottom:22px; }}
.benefit {{
  flex:1; text-align:center;
  background:white; border:1px solid rgba(143,156,104,.25);
  padding:14px 10px;
}}
.benefit-icon {{ margin-bottom:8px; }}
.benefit-title {{
  font-size:10.5px; font-weight:bold; color:{VERDE};
  text-transform:uppercase; letter-spacing:1px;
  margin-bottom:5px;
}}
.benefit-text {{ font-size:9px; color:{MARROM}; line-height:1.6; opacity:.8; }}

.steps {{ display:flex; gap:8px; margin-bottom:20px; }}
.step  {{ flex:1; text-align:center; padding:12px 8px; }}
.step-n {{
  width:30px; height:30px; border-radius:50%;
  background:{VERDE}; color:{FUNDO};
  font-family:"Courier New",monospace; font-size:13px; font-weight:bold;
  display:flex; align-items:center; justify-content:center;
  margin:0 auto 7px;
}}
.step-t {{ font-size:10.5px; font-weight:bold; color:{VERDE}; margin-bottom:3px; }}
.step-d {{ font-size:8.5px; color:{MARROM}; line-height:1.5; opacity:.75; }}

/* ═══════ CARDÁPIO (P3) ═══════ */
.sec {{ margin-bottom:16px; }}
.sh  {{ display:flex; align-items:center; gap:10px; margin-bottom:8px; }}
.sl  {{
  font-family:"Courier New",monospace; font-size:7.5px;
  text-transform:uppercase; letter-spacing:3px;
  color:{TERRA}; white-space:nowrap;
}}
.sr  {{ flex:1; height:1px; background:rgba(143,156,104,.3); }}

.dish {{
  display:flex; justify-content:space-between; align-items:center;
  padding:7px 12px; margin-bottom:2px;
  border-bottom:1px dotted rgba(143,156,104,.2);
}}
.dish:last-child {{ border-bottom:none; }}
.dn-wrap {{ flex:1; min-width:0; }}
.dn {{ font-size:12px; font-weight:bold; color:{VERDE}; }}
.dd {{ font-size:8.5px; color:{MARROM}; opacity:.6; font-style:italic; margin-top:2px; }}
.dp {{
  font-family:"Courier New",monospace; font-size:11.5px;
  color:{DOURADO}; font-weight:bold; white-space:nowrap;
  background:rgba(184,154,74,.08); padding:3px 8px;
}}

.size-note {{
  padding:11px 15px; margin-top:10px;
  background:rgba(44,95,52,.04); border-left:3px solid {DOURADO};
}}
.sn-lbl  {{
  font-family:"Courier New",monospace; font-size:7px;
  text-transform:uppercase; letter-spacing:2px; color:{OLIVA}; margin-bottom:6px;
}}
.sn-row  {{ display:flex; gap:24px; }}
.sn-item {{ font-size:12px; color:{VERDE}; font-weight:bold; }}
.sn-item span {{ font-weight:normal; color:{MARROM}; font-size:11px; }}
.sn-foot {{ font-size:7.5px; color:{MARROM}; font-style:italic; margin-top:5px; opacity:.65; }}

/* ═══════ KITS (P4) ═══════ */
.kits-page {{
  width:210mm; height:297mm;
  background:{VERDE};
  display:flex; flex-direction:column;
  overflow:hidden;
}}
.kh {{
  background:rgba(0,0,0,.18);
  padding:16px 16mm 14px;
  text-align:center;
  display:flex; flex-direction:column; align-items:center;
  flex-shrink:0;
}}
.kh-eye   {{
  font-family:"Courier New",monospace; font-size:7px;
  text-transform:uppercase; letter-spacing:3px; color:{OLIVA}; margin-bottom:4px;
}}
.kh-title {{ font-size:24px; color:{DOURADO}; letter-spacing:2px; }}
.kh-div   {{ width:44px; height:1px; background:rgba(184,154,74,.4); margin:8px auto 6px; }}
.kh-sub   {{ font-size:10px; color:{OLIVA}; font-style:italic; line-height:1.6; }}
.kh-obs   {{
  font-family:"Courier New",monospace; font-size:7.5px;
  color:rgba(143,156,104,.6); line-height:1.8; margin-top:6px;
  letter-spacing:0.5px;
}}

/* Kit cards */
.tier-cards {{ display:flex; gap:8px; margin:12px 14mm; }}
.tc {{
  flex:1; border:1px solid rgba(184,154,74,.2);
  display:flex; flex-direction:column;
}}
.tc.featured {{ border:2px solid {DOURADO}; }}

/* Área do badge — altura fixa para alinhar os três cards */
.tc-badge-area {{
  min-height:26px; display:flex; align-items:center;
  justify-content:center; padding-top:10px;
}}
.tc-badge {{
  display:inline-block;
  font-family:"Courier New",monospace; font-size:6.5px;
  text-transform:uppercase; letter-spacing:2px;
  padding:3px 10px; font-weight:bold;
  background:{DOURADO}; color:{VERDE};
}}
.tc:not(.featured) .tc-badge {{
  background:rgba(176,82,22,.3); color:{TERRA};
}}

/* Cabeçalho do card */
.tc-head {{
  padding:10px 12px 13px; text-align:center;
  background:rgba(250,248,243,.05);
  border-bottom:1px solid rgba(184,154,74,.12);
  flex-shrink:0;
}}
.tc.featured .tc-head {{
  background:rgba(184,154,74,.10);
  border-bottom-color:rgba(184,154,74,.3);
}}

/* Título principal do card */
.tc-kit-name {{
  font-size:22px; font-weight:bold; color:{FUNDO};
  letter-spacing:1px; margin-bottom:3px;
}}
.tc.featured .tc-kit-name {{ color:{DOURADO}; }}

/* Subtítulo: "20 marmitas" */
.tc-marmitas {{
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:2px;
  color:rgba(250,248,243,.38); margin-bottom:10px;
}}

/* Faixa de preço */
.tc-price {{
  font-family:"Courier New",monospace;
  font-size:14px; font-weight:bold; color:{FUNDO};
}}
.tc.featured .tc-price {{ color:{DOURADO}; }}
.tc-un {{ font-size:8.5px; font-weight:normal; color:{OLIVA}; }}

/* Linhas de gramagem */
.tc-body {{ padding:4px 0; }}
.tc-row {{
  display:flex; justify-content:space-between; align-items:center;
  padding:8px 12px; border-bottom:1px solid rgba(250,248,243,.05);
}}
.tc-row:last-child {{ border-bottom:none; }}
.tc-size  {{ font-size:10px; color:rgba(250,248,243,.5); font-family:"Courier New",monospace; }}
.tc-total {{ font-family:"Courier New",monospace; font-size:13px; font-weight:bold; color:{FUNDO}; }}
.tc.featured .tc-total {{ color:{DOURADO}; }}

.kits-note {{
  text-align:center; font-size:9px; color:{OLIVA};
  font-style:italic; margin:6px 14mm 6px;
}}
.pix-badge {{ text-align:center; margin:0 0 10px; }}
.pix {{
  display:inline-block;
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:2px; font-weight:bold;
  background:{DOURADO}; color:{VERDE}; padding:5px 18px;
}}
.kits-foot {{
  margin:8px 14mm 0;
  border-top:1px solid rgba(184,154,74,.18);
  padding-top:12px; text-align:center; flex-shrink:0;
  margin-bottom:14px;
}}
.kf-label {{ font-family:"Courier New",monospace; font-size:7.5px; letter-spacing:2px; text-transform:uppercase; color:{OLIVA}; }}
.kf-wa    {{ font-family:"Courier New",monospace; font-size:20px; color:{FUNDO}; letter-spacing:2px; margin:4px 0; }}
.kf-tag   {{ font-size:9px; font-style:italic; color:{OLIVA}; }}

/* ═══════ COMO PEDIR (P5) ═══════ */
.order-steps {{ margin-bottom:20px; }}
.os {{
  display:flex; align-items:flex-start; gap:15px;
  padding:12px 0; border-bottom:1px solid rgba(143,156,104,.18);
}}
.os:last-child {{ border-bottom:none; }}
.os-n {{
  width:36px; height:36px; border-radius:50%;
  background:{VERDE}; color:{FUNDO};
  font-family:"Courier New",monospace; font-size:15px; font-weight:bold;
  display:flex; align-items:center; justify-content:center;
  flex-shrink:0;
}}
.os-title {{ font-size:13px; font-weight:bold; color:{VERDE}; margin-bottom:3px; }}
.os-desc  {{ font-size:10px; color:{MARROM}; line-height:1.6; opacity:.8; }}

.payment-box {{
  background:rgba(44,95,52,.04); border:1px solid rgba(143,156,104,.25);
  padding:13px 17px; margin-bottom:20px;
}}
.payment-title {{
  font-family:"Courier New",monospace; font-size:7.5px;
  text-transform:uppercase; letter-spacing:2px; color:{OLIVA}; margin-bottom:9px;
}}
.payment-methods {{ display:flex; gap:10px; }}
.pay-m {{
  flex:1; text-align:center; padding:9px 8px;
  background:white; border:1px solid rgba(143,156,104,.2);
  font-size:11px; color:{VERDE}; font-weight:bold;
}}

.cta-box {{
  background:{VERDE}; padding:22px; text-align:center;
}}
.cta-label {{
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:3px; color:{OLIVA}; margin-bottom:9px;
}}
.cta-wa {{
  font-family:"Courier New",monospace; font-size:26px;
  font-weight:bold; color:{DOURADO}; letter-spacing:2px; margin:4px 0 8px;
}}
.cta-sub {{
  font-size:9.5px; font-style:italic; color:rgba(250,248,243,.55);
}}
"""

# ── HTML ──────────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>


<!-- ══════════════ P1 · CAPA ══════════════ -->
<div class="cover page-break">
  <div class="cover-stripe">
    <div class="cover-stripe-label">Marmitas Congeladas Artesanais</div>
  </div>

  <div class="cover-center">
    {logo_seal(size=270, padding=18, border_w=2)}

    <div class="cover-brand">{NOME}</div>
    <div class="cover-sub">{CIDADE}</div>

    <div class="cover-ornament">
      <div class="cover-orn-line"></div>
      <div class="cover-orn-dot">✦</div>
      <div class="cover-orn-line"></div>
    </div>

    <div class="cover-tagline">{TAGLINE}</div>
  </div>

  <div class="cover-foot">
    <div class="cover-foot-label">Peça pelo WhatsApp</div>
    <div class="cover-foot-wa">{WA}</div>
    <div class="cover-foot-sub">Cardápio · Kits · Encomendas</div>
  </div>
</div>


<!-- ══════════════ P2 · APRESENTAÇÃO ══════════════ -->
<div class="page page-break">

  {page_header("Sobre nós", f"{NOME} · Nossa História")}

  <div class="page-body">

    <div class="intro-text">
      <p>A <strong>Casa Celi</strong> nasceu do desejo de levar para a sua mesa a autenticidade
      de uma cozinha feita com carinho — sem abrir mão da praticidade do dia a dia.</p>
      <p>Cada marmita é preparada com ingredientes frescos, temperada com amor e congelada
      no ponto certo para preservar o sabor, a nutrição e a textura de sempre.</p>
      <p>Aqui não tem industrializado escondido, nem atalho: é comida de verdade,
      feita como a sua mãe faria — pronta quando precisa.</p>
    </div>

    <div class="sec-title">Por que escolher a Casa Celi?</div>

    <div class="benefits">
      <div class="benefit">
        <div class="benefit-icon">{ICO_HEART}</div>
        <div class="benefit-title">Sabor Caseiro</div>
        <div class="benefit-text">Receitas tradicionais com ingredientes frescos e tempero da casa</div>
      </div>
      <div class="benefit">
        <div class="benefit-icon">{ICO_SNOW}</div>
        <div class="benefit-title">30 Dias no Freezer</div>
        <div class="benefit-text">Congelamento seguro que preserva sabor e nutrição completa</div>
      </div>
      <div class="benefit">
        <div class="benefit-icon">{ICO_BOLT}</div>
        <div class="benefit-title">Praticidade Total</div>
        <div class="benefit-text">Do freezer ao prato em minutos. Sem cozinhar, sem louça extra</div>
      </div>
    </div>

    <div class="sec-divider">
      <div class="sec-divider-line"></div>
      <div class="sec-divider-dot"></div>
      <div class="sec-divider-line"></div>
    </div>

    <div class="sec-title">Como funciona</div>

    <div class="steps">
      <div class="step">
        <div class="step-n">1</div>
        <div class="step-t">Escolha</div>
        <div class="step-d">Selecione os pratos e a gramagem desejada</div>
      </div>
      <div class="step">
        <div class="step-n">2</div>
        <div class="step-t">Peça</div>
        <div class="step-d">Envie a lista pelo WhatsApp com seu nome</div>
      </div>
      <div class="step">
        <div class="step-n">3</div>
        <div class="step-t">Armazene</div>
        <div class="step-d">Guarde no freezer por até 30 dias sem perder o sabor</div>
      </div>
      <div class="step">
        <div class="step-n">4</div>
        <div class="step-t">Aqueça</div>
        <div class="step-d">Banho-maria ou micro-ondas. Pronto em minutos!</div>
      </div>
    </div>

  </div>

  <div class="page-foot">
    <div class="pf-brand">Casa Celi · Congelados Artesanais · {CIDADE}</div>
    <div class="pf-wa">{WA}</div>
  </div>
</div>


<!-- ══════════════ P3 · CARDÁPIO ══════════════ -->
<div class="page page-break">

  {page_header("Cardápio Completo", f"{NOME} · Marmitas Congeladas")}

  <div class="page-body">

    <div class="sec">
      <div class="sh"><span class="sl">Tradicionais</span><div class="sr"></div></div>
      {dish_rows(TRADICIONAIS, preco=False)}
    </div>

    <div class="sec">
      <div class="sh"><span class="sl">Premium</span><div class="sr"></div></div>
      {dish_rows(PREMIUM)}
    </div>

    <div class="sec">
      <div class="sh"><span class="sl">Caldos Artesanais</span><div class="sr"></div></div>
      {dish_rows(CALDOS)}
    </div>

    <div class="size-note">
      <div class="sn-lbl">Gramagem · marmitas avulsas (Tradicionais)</div>
      <div class="sn-row">
        <div class="sn-item">300 g <span>· R$ 18,00</span></div>
        <div class="sn-item">400 g <span>· R$ 20,00</span></div>
        <div class="sn-item">500 g <span>· R$ 22,00</span></div>
      </div>
      <div class="sn-foot">* Pratos Premium têm preço fixo · Consulte disponibilidade semanal</div>
    </div>

  </div>

  <div class="page-foot">
    <div class="pf-brand">Consulte pratos disponíveis na semana pelo WhatsApp</div>
    <div class="pf-wa">{WA}</div>
  </div>
</div>


<!-- ══════════════ P4 · KITS ══════════════ -->
<div class="kits-page page-break">

  <div class="kh">
    {logo_seal(size=110, padding=9, border_w=2)}
    <div class="kh-eye" style="margin-top:12px;">Monte seu estoque</div>
    <div class="kh-title">Kits &amp; Descontos</div>
    <div class="kh-div"></div>
    <div class="kh-sub">Quanto mais você pede, mais você economiza</div>
    <div class="kh-obs">Kits válidos para pratos tradicionais<br>Pratos premium seguem valores individuais</div>
  </div>

  <div class="tier-cards">{tier_cards()}</div>

  <div class="kits-note">Pedido mínimo: 10 marmitas · Kits mistos permitidos · Validade: 30 dias no freezer</div>
  <div class="pix-badge"><span class="pix">+ 3% OFF pagando com PIX</span></div>

  <div class="kits-foot">
    <div class="kf-label">Faça seu pedido · WhatsApp</div>
    <div class="kf-wa">{WA}</div>
    <div class="kf-tag">Casa Celi · Congelados com sabor de cozinha afetiva</div>
  </div>

</div>


<!-- ══════════════ P5 · COMO PEDIR ══════════════ -->
<div class="page">

  {page_header("Pedido simples e rápido", f"{NOME} · Como Pedir")}

  <div class="page-body">

    <div class="order-steps">
      <div class="os">
        <div class="os-n">1</div>
        <div>
          <div class="os-title">Escolha seus pratos</div>
          <div class="os-desc">Veja o cardápio e selecione as marmitas que quiser. Informe a gramagem: 300 g, 400 g ou 500 g. Você pode misturar pratos diferentes no mesmo kit.</div>
        </div>
      </div>
      <div class="os">
        <div class="os-n">2</div>
        <div>
          <div class="os-title">Envie pelo WhatsApp</div>
          <div class="os-desc">Mande a lista com pratos, quantidade, gramagem e seu nome para {WA}. Respondemos rápido com a confirmação e o prazo de entrega.</div>
        </div>
      </div>
      <div class="os">
        <div class="os-n">3</div>
        <div>
          <div class="os-title">Combine a entrega</div>
          <div class="os-desc">Entrega em Sorocaba ou retirada no local. Confirmamos o endereço, data e horário pelo WhatsApp.</div>
        </div>
      </div>
      <div class="os">
        <div class="os-n">4</div>
        <div>
          <div class="os-title">Pague e aproveite</div>
          <div class="os-desc">Receba suas marmitas, guarde no freezer e tenha refeições prontas por até 30 dias. Aqueça em banho-maria ou micro-ondas e sirva.</div>
        </div>
      </div>
    </div>

    <div class="payment-box">
      <div class="payment-title">Formas de pagamento</div>
      <div class="payment-methods">
        <div class="pay-m">PIX<br><span style="font-size:8.5px;font-weight:normal;color:#4F2915;opacity:.7;">3% de desconto</span></div>
        <div class="pay-m">Dinheiro</div>
        <div class="pay-m">Transferência<br><span style="font-size:8.5px;font-weight:normal;color:#4F2915;opacity:.7;">na entrega</span></div>
      </div>
    </div>

    <div class="cta-box">
      <div class="cta-label">Peça agora mesmo</div>
      <div class="cta-wa">{WA}</div>
      <div class="cta-sub">WhatsApp · Atendimento de segunda a sábado</div>
    </div>

  </div>

  <div class="page-foot">
    <div class="pf-brand">Casa Celi · {CIDADE} · Congelados Artesanais</div>
    <div class="pf-wa">{WA}</div>
  </div>
</div>


</body>
</html>"""

output = "/home/user/belle-petit-pet-saloon/CasaCeli_Cardapio_Texto.pdf"
from weasyprint import HTML as WP
WP(string=HTML, base_url=".").write_pdf(output)
print(f"PDF → {output}")

# ── HTML Mobile ───────────────────────────────────────────────────────────────
def _kit_cards_mobile():
    out = ''
    for t in KIT_TIERS:
        feat  = ' featured' if t['featured'] else ''
        u_min = min(s['unit'] for s in t['sizes'])
        u_max = max(s['unit'] for s in t['sizes'])
        badge = (f'<div class="kc-badge-area"><span class="kc-badge">{t["badge"]}</span></div>'
                 if t['badge'] else '<div class="kc-badge-area"></div>')
        rows  = ''.join(
            f'<div class="kc-row">'
            f'<span class="kc-g">{s["label"]}</span>'
            f'<span class="kc-total">R$ {s["total"]}</span>'
            f'</div>'
            for s in t['sizes']
        )
        out += (
            f'<div class="kit-card{feat}">'
            f'{badge}'
            f'<div class="kc-head">'
            f'<div class="kc-name">{t["name"]}</div>'
            f'<div class="kc-marmitas">{t["qty"]} marmitas</div>'
            f'<div class="kc-price">R$ {u_min}–{u_max}<span class="kc-un"> /un</span></div>'
            f'</div>'
            f'<div class="kc-body">{rows}</div>'
            f'</div>'
        )
    return out

def _dish_mobile(lista, show_price=True):
    rows = []
    for item in lista:
        n, p = item[0], item[1]
        desc  = f'<div class="dish-desc">{item[2]}</div>' if len(item) > 2 else ''
        price = f'<span class="dish-price">{p}</span>' if show_price else ''
        rows.append(
            f'<div class="dish">'
            f'<div class="dish-wrap"><div class="dish-name">{n}</div>{desc}</div>'
            f'{price}'
            f'</div>'
        )
    return ''.join(rows)

def _seal_mobile(size=180, pad=10):
    clip = size - pad * 2
    return (
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;'
        f'border:2px solid {DOURADO};background:{FUNDO};'
        f'display:flex;align-items:center;justify-content:center;margin:0 auto;">'
        f'<div style="width:{clip}px;height:{clip}px;border-radius:50%;overflow:hidden;">'
        f'<img src="{LOGO}" style="width:100%;height:100%;object-fit:cover;display:block;"/>'
        f'</div></div>'
    )

def _mini_seal_mobile(size=44):
    clip = size - 8
    return (
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;'
        f'border:1px solid {DOURADO};background:{FUNDO};flex-shrink:0;'
        f'display:flex;align-items:center;justify-content:center;">'
        f'<div style="width:{clip}px;height:{clip}px;border-radius:50%;overflow:hidden;">'
        f'<img src="{LOGO}" style="width:100%;height:100%;object-fit:cover;display:block;"/>'
        f'</div></div>'
    )

def _sec_header_mobile(eye, title):
    return (
        f'<div class="sec-header">'
        f'{_mini_seal_mobile()}'
        f'<div style="flex:1;min-width:0;">'
        f'<div class="sec-eye">{eye}</div>'
        f'<div class="sec-title">{title}</div>'
        f'</div></div>'
    )

HTML_MOBILE = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Casa Celi — Cardápio</title>
<style>
:root{{
  --v:{VERDE};--o:{OLIVA};--t:{TERRA};--m:{MARROM};
  --d:{DOURADO};--f:{FUNDO};--f2:{FUNDO2};--c:{CREME};
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:Georgia,"Times New Roman",serif;background:var(--f);color:var(--m);max-width:480px;margin:0 auto;}}

/* CAPA */
.cover{{background:linear-gradient(170deg,var(--f) 0%,var(--f2) 60%,var(--c) 100%);}}
.stripe{{background:var(--v);padding:10px;text-align:center;font-family:monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:rgba(250,248,243,.55);}}
.cover-center{{padding:30px 24px;display:flex;flex-direction:column;align-items:center;}}
.brand{{font-size:34px;font-weight:bold;color:var(--v);letter-spacing:3px;margin-top:16px;text-align:center;}}
.brand-city{{font-family:monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--o);margin-top:4px;text-align:center;}}
.orn{{display:flex;align-items:center;gap:10px;margin:16px 0;}}
.orn-line{{width:40px;height:1px;background:var(--d);opacity:.5;}}
.orn-dot{{color:var(--d);font-size:12px;}}
.tagline{{font-size:14px;font-style:italic;color:var(--m);text-align:center;line-height:1.7;opacity:.8;max-width:280px;}}
.cover-foot{{background:var(--v);padding:20px;text-align:center;}}
.wa-label{{font-family:monospace;font-size:8px;letter-spacing:3px;text-transform:uppercase;color:rgba(250,248,243,.5);}}
.wa{{font-family:monospace;font-size:24px;color:var(--d);letter-spacing:2px;margin:6px 0;}}
.wa-sub{{font-family:monospace;font-size:8px;text-transform:uppercase;letter-spacing:3px;color:rgba(250,248,243,.35);}}

/* SEÇÃO GENÉRICA */
.sec-header{{background:var(--v);padding:13px 18px;display:flex;align-items:center;gap:12px;}}
.sec-eye{{font-family:monospace;font-size:7px;letter-spacing:3px;text-transform:uppercase;color:var(--o);}}
.sec-title{{font-size:16px;font-weight:bold;color:var(--f);margin-top:2px;}}
.sec-body{{padding:18px 18px 14px;background:var(--f);}}
.sec-foot{{padding:9px 18px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(143,156,104,.22);background:var(--f);}}
.sf-brand{{font-size:8px;color:var(--o);font-style:italic;}}
.sf-wa{{font-family:monospace;font-size:9px;color:var(--v);}}

/* APRESENTAÇÃO */
.intro-box{{background:rgba(44,95,52,.04);border-left:3px solid var(--d);padding:14px 15px;margin-bottom:18px;font-size:13px;line-height:1.8;}}
.intro-box p+p{{margin-top:9px;}}
.blk-title{{font-family:monospace;font-size:8px;letter-spacing:3px;text-transform:uppercase;color:var(--t);text-align:center;margin-bottom:12px;}}
.benefit{{background:white;border:1px solid rgba(143,156,104,.25);padding:13px 15px;display:flex;align-items:center;gap:13px;margin-bottom:8px;}}
.benefit-info{{flex:1;}}
.benefit-title{{font-size:12px;font-weight:bold;color:var(--v);text-transform:uppercase;letter-spacing:1px;margin-bottom:3px;}}
.benefit-text{{font-size:11px;color:var(--m);line-height:1.5;opacity:.8;}}
.divider{{height:1px;background:rgba(143,156,104,.25);margin:16px 0;}}
.steps{{display:grid;grid-template-columns:1fr 1fr;gap:8px;}}
.step{{text-align:center;padding:12px 8px;}}
.step-n{{width:30px;height:30px;border-radius:50%;background:var(--v);color:var(--f);font-family:monospace;font-size:13px;font-weight:bold;display:flex;align-items:center;justify-content:center;margin:0 auto 7px;}}
.step-t{{font-size:12px;font-weight:bold;color:var(--v);margin-bottom:3px;}}
.step-d{{font-size:10px;color:var(--m);line-height:1.5;opacity:.75;}}

/* CARDÁPIO */
.cat-sec{{margin-bottom:14px;}}
.cat-header{{display:flex;align-items:center;gap:10px;margin-bottom:8px;}}
.cat-label{{font-family:monospace;font-size:8px;letter-spacing:3px;text-transform:uppercase;color:var(--t);white-space:nowrap;}}
.cat-line{{flex:1;height:1px;background:rgba(143,156,104,.3);}}
.dish{{display:flex;justify-content:space-between;align-items:flex-start;padding:9px 0;border-bottom:1px dotted rgba(143,156,104,.2);gap:8px;}}
.dish:last-child{{border-bottom:none;}}
.dish-wrap{{flex:1;min-width:0;}}
.dish-name{{font-size:13px;font-weight:bold;color:var(--v);line-height:1.3;}}
.dish-desc{{font-size:10px;color:var(--m);font-style:italic;opacity:.6;margin-top:2px;}}
.dish-price{{font-family:monospace;font-size:12px;color:var(--d);font-weight:bold;background:rgba(184,154,74,.1);padding:3px 8px;white-space:nowrap;flex-shrink:0;}}
.size-note{{background:rgba(44,95,52,.04);border-left:3px solid var(--d);padding:12px 14px;margin-top:10px;}}
.sn-label{{font-family:monospace;font-size:7px;letter-spacing:2px;text-transform:uppercase;color:var(--o);margin-bottom:7px;}}
.sn-grid{{display:flex;gap:10px;flex-wrap:wrap;}}
.sn-item{{font-size:13px;font-weight:bold;color:var(--v);}}
.sn-item span{{font-weight:normal;color:var(--m);font-size:12px;}}
.sn-foot{{font-size:9px;font-style:italic;color:var(--m);margin-top:5px;opacity:.65;}}

/* KITS */
.kits-page{{background:var(--v);}}
.kits-hdr{{padding:18px 20px 14px;text-align:center;display:flex;flex-direction:column;align-items:center;background:rgba(0,0,0,.18);}}
.kh-eye{{font-family:monospace;font-size:7px;letter-spacing:3px;text-transform:uppercase;color:var(--o);margin-top:12px;margin-bottom:4px;}}
.kh-title{{font-size:24px;color:var(--d);letter-spacing:2px;font-weight:bold;}}
.kh-div{{width:40px;height:1px;background:rgba(184,154,74,.4);margin:8px auto;}}
.kh-sub{{font-size:11px;color:var(--o);font-style:italic;line-height:1.6;text-align:center;}}
.kh-obs{{font-family:monospace;font-size:8px;color:rgba(143,156,104,.65);line-height:1.9;text-align:center;margin-top:5px;}}
.kit-cards{{padding:12px 16px;display:flex;flex-direction:column;gap:10px;}}
.kit-card{{border:1px solid rgba(184,154,74,.22);display:flex;flex-direction:column;}}
.kit-card.featured{{border:2px solid var(--d);}}
.kc-badge-area{{min-height:0;display:flex;align-items:center;justify-content:center;padding-top:10px;}}
.kc-badge{{display:inline-block;font-family:monospace;font-size:7px;letter-spacing:2px;text-transform:uppercase;padding:3px 12px;font-weight:bold;background:var(--d);color:var(--v);}}
.kit-card:not(.featured) .kc-badge{{background:rgba(176,82,22,.3);color:var(--t);}}
.kc-head{{padding:10px 16px 12px;text-align:center;background:rgba(250,248,243,.05);border-bottom:1px solid rgba(184,154,74,.12);}}
.kit-card.featured .kc-head{{background:rgba(184,154,74,.10);border-bottom-color:rgba(184,154,74,.3);}}
.kc-name{{font-size:22px;font-weight:bold;color:var(--f);letter-spacing:1px;}}
.kit-card.featured .kc-name{{color:var(--d);}}
.kc-marmitas{{font-family:monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:rgba(250,248,243,.38);margin:3px 0 9px;}}
.kc-price{{font-family:monospace;font-size:15px;font-weight:bold;color:var(--f);}}
.kit-card.featured .kc-price{{color:var(--d);}}
.kc-un{{font-size:9px;font-weight:normal;color:var(--o);}}
.kc-body{{padding:4px 0;}}
.kc-row{{display:flex;justify-content:space-between;padding:9px 16px;border-bottom:1px solid rgba(250,248,243,.05);}}
.kc-row:last-child{{border-bottom:none;}}
.kc-g{{font-family:monospace;font-size:10px;color:rgba(250,248,243,.5);}}
.kc-total{{font-family:monospace;font-size:14px;font-weight:bold;color:var(--f);}}
.kit-card.featured .kc-total{{color:var(--d);}}
.kits-note{{text-align:center;font-size:9px;color:var(--o);font-style:italic;padding:5px 16px;}}
.pix-area{{text-align:center;padding:6px 0 10px;}}
.pix-tag{{display:inline-block;font-family:monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;font-weight:bold;background:var(--d);color:var(--v);padding:5px 20px;}}
.kits-foot{{border-top:1px solid rgba(184,154,74,.18);margin:0 16px;padding:14px 0;text-align:center;}}
.kf-label{{font-family:monospace;font-size:7.5px;letter-spacing:2px;text-transform:uppercase;color:var(--o);}}
.kf-wa{{font-family:monospace;font-size:20px;color:var(--f);letter-spacing:2px;margin:5px 0;}}
.kf-tag{{font-size:9px;font-style:italic;color:var(--o);padding-bottom:14px;}}

/* COMO PEDIR */
.os{{display:flex;align-items:flex-start;gap:14px;padding:12px 0;border-bottom:1px solid rgba(143,156,104,.18);}}
.os:last-child{{border-bottom:none;}}
.os-n{{width:36px;height:36px;border-radius:50%;background:var(--v);color:var(--f);font-family:monospace;font-size:15px;font-weight:bold;display:flex;align-items:center;justify-content:center;flex-shrink:0;}}
.os-title{{font-size:14px;font-weight:bold;color:var(--v);margin-bottom:3px;}}
.os-desc{{font-size:11px;color:var(--m);line-height:1.6;opacity:.8;}}
.pay-box{{background:rgba(44,95,52,.04);border:1px solid rgba(143,156,104,.25);padding:14px 15px;margin:18px 0;}}
.pay-title{{font-family:monospace;font-size:7.5px;letter-spacing:2px;text-transform:uppercase;color:var(--o);margin-bottom:9px;}}
.pay-methods{{display:flex;gap:8px;}}
.pay-m{{flex:1;text-align:center;padding:10px 6px;background:white;border:1px solid rgba(143,156,104,.2);font-size:11px;color:var(--v);font-weight:bold;}}
.cta{{background:var(--v);padding:24px 20px;text-align:center;}}
.cta-label{{font-family:monospace;font-size:8px;letter-spacing:3px;text-transform:uppercase;color:var(--o);margin-bottom:10px;}}
.cta-wa{{font-family:monospace;font-size:26px;font-weight:bold;color:var(--d);letter-spacing:2px;margin:4px 0 8px;}}
.cta-sub{{font-size:11px;font-style:italic;color:rgba(250,248,243,.55);}}
</style>
</head>
<body>

<!-- CAPA -->
<section class="cover">
  <div class="stripe">Marmitas Congeladas Artesanais</div>
  <div class="cover-center">
    {_seal_mobile(180, 10)}
    <div class="brand">{NOME}</div>
    <div class="brand-city">{CIDADE}</div>
    <div class="orn"><div class="orn-line"></div><div class="orn-dot">✦</div><div class="orn-line"></div></div>
    <div class="tagline">{TAGLINE}</div>
  </div>
  <div class="cover-foot">
    <div class="wa-label">Peça pelo WhatsApp</div>
    <div class="wa">{WA}</div>
    <div class="wa-sub">Cardápio · Kits · Encomendas</div>
  </div>
</section>

<!-- APRESENTAÇÃO -->
<section>
  {_sec_header_mobile("Sobre nós", f"{NOME} · Nossa História")}
  <div class="sec-body">
    <div class="intro-box">
      <p>A <strong>Casa Celi</strong> nasceu do desejo de levar para a sua mesa a autenticidade
      de uma cozinha feita com carinho — sem abrir mão da praticidade do dia a dia.</p>
      <p>Cada marmita é preparada com ingredientes frescos, temperada com amor e congelada
      no ponto certo para preservar o sabor, a nutrição e a textura de sempre.</p>
      <p>Aqui não tem industrializado escondido, nem atalho: é comida de verdade,
      feita como a sua mãe faria — pronta quando precisa.</p>
    </div>
    <div class="blk-title">Por que escolher a Casa Celi?</div>
    <div class="benefit"><div>{ICO_HEART}</div><div class="benefit-info"><div class="benefit-title">Sabor Caseiro</div><div class="benefit-text">Receitas tradicionais com ingredientes frescos e tempero da casa</div></div></div>
    <div class="benefit"><div>{ICO_SNOW}</div><div class="benefit-info"><div class="benefit-title">30 Dias no Freezer</div><div class="benefit-text">Congelamento seguro que preserva sabor e nutrição completa</div></div></div>
    <div class="benefit"><div>{ICO_BOLT}</div><div class="benefit-info"><div class="benefit-title">Praticidade Total</div><div class="benefit-text">Do freezer ao prato em minutos. Sem cozinhar, sem louça extra</div></div></div>
    <div class="divider"></div>
    <div class="blk-title">Como funciona</div>
    <div class="steps">
      <div class="step"><div class="step-n">1</div><div class="step-t">Escolha</div><div class="step-d">Selecione os pratos e a gramagem</div></div>
      <div class="step"><div class="step-n">2</div><div class="step-t">Peça</div><div class="step-d">Envie a lista pelo WhatsApp</div></div>
      <div class="step"><div class="step-n">3</div><div class="step-t">Armazene</div><div class="step-d">Freezer por até 30 dias</div></div>
      <div class="step"><div class="step-n">4</div><div class="step-t">Aqueça</div><div class="step-d">Banho-maria ou micro-ondas</div></div>
    </div>
  </div>
  <div class="sec-foot"><div class="sf-brand">Casa Celi · Congelados Artesanais · {CIDADE}</div><div class="sf-wa">{WA}</div></div>
</section>

<!-- CARDÁPIO -->
<section>
  {_sec_header_mobile("Cardápio Completo", f"{NOME} · Marmitas Congeladas")}
  <div class="sec-body">
    <div class="cat-sec">
      <div class="cat-header"><span class="cat-label">Tradicionais</span><div class="cat-line"></div></div>
      {_dish_mobile(TRADICIONAIS, show_price=False)}
    </div>
    <div class="cat-sec">
      <div class="cat-header"><span class="cat-label">Premium</span><div class="cat-line"></div></div>
      {_dish_mobile(PREMIUM)}
    </div>
    <div class="cat-sec">
      <div class="cat-header"><span class="cat-label">Caldos Artesanais</span><div class="cat-line"></div></div>
      {_dish_mobile(CALDOS)}
    </div>
    <div class="size-note">
      <div class="sn-label">Gramagem · marmitas avulsas (Tradicionais)</div>
      <div class="sn-grid">
        <div class="sn-item">300 g <span>· R$ 18,00</span></div>
        <div class="sn-item">400 g <span>· R$ 20,00</span></div>
        <div class="sn-item">500 g <span>· R$ 22,00</span></div>
      </div>
      <div class="sn-foot">* Pratos Premium têm preço fixo · Consulte disponibilidade semanal</div>
    </div>
  </div>
  <div class="sec-foot"><div class="sf-brand">Consulte pratos disponíveis na semana pelo WhatsApp</div><div class="sf-wa">{WA}</div></div>
</section>

<!-- KITS -->
<section class="kits-page">
  <div class="kits-hdr">
    {_seal_mobile(110, 8)}
    <div class="kh-eye">Monte seu estoque</div>
    <div class="kh-title">Kits &amp; Descontos</div>
    <div class="kh-div"></div>
    <div class="kh-sub">Quanto mais você pede, mais você economiza</div>
    <div class="kh-obs">Kits válidos para pratos tradicionais<br>Pratos premium seguem valores individuais</div>
  </div>
  <div class="kit-cards">{_kit_cards_mobile()}</div>
  <div class="kits-note">Pedido mínimo: 10 marmitas · Kits mistos permitidos · Validade: 30 dias no freezer</div>
  <div class="pix-area"><span class="pix-tag">+ 3% OFF pagando com PIX</span></div>
  <div class="kits-foot">
    <div class="kf-label">Faça seu pedido · WhatsApp</div>
    <div class="kf-wa">{WA}</div>
    <div class="kf-tag">Casa Celi · Congelados com sabor de cozinha afetiva</div>
  </div>
</section>

<!-- COMO PEDIR -->
<section>
  {_sec_header_mobile("Pedido simples e rápido", f"{NOME} · Como Pedir")}
  <div class="sec-body">
    <div class="os"><div class="os-n">1</div><div><div class="os-title">Escolha seus pratos</div><div class="os-desc">Veja o cardápio e selecione as marmitas. Informe a gramagem: 300 g, 400 g ou 500 g. Pode misturar pratos no mesmo kit.</div></div></div>
    <div class="os"><div class="os-n">2</div><div><div class="os-title">Envie pelo WhatsApp</div><div class="os-desc">Mande a lista com pratos, quantidade, gramagem e seu nome para {WA}.</div></div></div>
    <div class="os"><div class="os-n">3</div><div><div class="os-title">Combine a entrega</div><div class="os-desc">Entrega em Sorocaba ou retirada no local. Confirmamos tudo pelo WhatsApp.</div></div></div>
    <div class="os"><div class="os-n">4</div><div><div class="os-title">Pague e aproveite</div><div class="os-desc">Guarde no freezer por até 30 dias. Aqueça em banho-maria ou micro-ondas e sirva.</div></div></div>
    <div class="pay-box">
      <div class="pay-title">Formas de pagamento</div>
      <div class="pay-methods">
        <div class="pay-m">PIX<br><span style="font-size:9px;font-weight:normal;opacity:.7;">3% OFF</span></div>
        <div class="pay-m">Dinheiro</div>
        <div class="pay-m">Transferência<br><span style="font-size:9px;font-weight:normal;opacity:.7;">na entrega</span></div>
      </div>
    </div>
    <div class="cta">
      <div class="cta-label">Peça agora mesmo</div>
      <div class="cta-wa">{WA}</div>
      <div class="cta-sub">WhatsApp · Atendimento de segunda a sábado</div>
    </div>
  </div>
  <div class="sec-foot"><div class="sf-brand">Casa Celi · {CIDADE} · Congelados Artesanais</div><div class="sf-wa">{WA}</div></div>
</section>

</body>
</html>"""

mobile_output = "/home/user/belle-petit-pet-saloon/cardapio_mobile.html"
with open(mobile_output, 'w', encoding='utf-8') as f:
    f.write(HTML_MOBILE)
print(f"HTML  → {mobile_output}")
