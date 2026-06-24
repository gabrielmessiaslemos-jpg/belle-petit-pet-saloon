#!/usr/bin/env python3
"""Casa Celi — PDF comercial completo 5 páginas."""

import base64, os

# ── Identidade ────────────────────────────────────────────────────────────────
NOME      = "Casa Celi"
CIDADE    = "Sorocaba · SP"
WA        = "(15) 99677-9560"
TAGLINE   = "Comida feita hoje para facilitar o seu amanhã"
ESTILO    = "Caseiro / Afetivo"

# ── Cores ─────────────────────────────────────────────────────────────────────
VERDE   = '#1E4B26'
VERDE2  = '#2C5F34'
OLIVA   = '#8F9C68'
TERRA   = '#B05216'
MARROM  = '#4F2915'
DOURADO = '#B89A4A'
FUNDO   = '#FAF8F3'
FUNDO2  = '#F0E8D5'
CREME   = '#EBD9B0'

# ── Cardápio ──────────────────────────────────────────────────────────────────
TRADICIONAIS = [
    ("Frango Desfiado ao Creme de Milho",   "R$ 20,00"),
    ("Frango em Cubos Acebolado",           "R$ 20,00"),
    ("Almôndegas ao Molho Pomodoro",        "R$ 20,00"),
    ("Frango Xadrez da Casa",               "R$ 20,00"),
    ("Filé de Frango ao Molho de Mel",      "R$ 20,00"),
    ("Filé de Merluza",                     "R$ 20,00"),
]
PREMIUM = [
    ("Parmegiana com Crosta",     "R$ 28,50"),
    ("Nhoque à Bolonhesa",        "R$ 33,50"),
    ("Lasanha Saborosa",          "R$ 26,00"),
    ("Escondidinho Caprichado",   "R$ 24,50"),
    ("Panquecas Caseiras",        "R$ 23,50"),
    ("Macarrões da Casa",         "R$ 24,90"),
]
CALDOS = [
    ("Caldo Artesanal (500 ml)",  "R$ 21,90"),
]

# ── Kits ──────────────────────────────────────────────────────────────────────
KIT_TIERS = [
    {
        'name': 'Kit 10', 'qty': 10, 'badge': None, 'featured': False,
        'sizes': [
            {'label': '300 ml', 'unit': 19, 'total': 190},
            {'label': '400 ml', 'unit': 21, 'total': 210},
            {'label': '500 ml', 'unit': 23, 'total': 230},
        ]
    },
    {
        'name': 'Kit 20', 'qty': 20, 'badge': 'MAIS POPULAR', 'featured': True,
        'sizes': [
            {'label': '300 ml', 'unit': 18, 'total': 360},
            {'label': '400 ml', 'unit': 20, 'total': 400},
            {'label': '500 ml', 'unit': 22, 'total': 440},
        ]
    },
    {
        'name': 'Kit 30', 'qty': 30, 'badge': '10% OFF', 'featured': False,
        'sizes': [
            {'label': '300 ml', 'unit': 17, 'total': 510},
            {'label': '400 ml', 'unit': 19, 'total': 570},
            {'label': '500 ml', 'unit': 21, 'total': 630},
        ]
    },
]

# ── Helpers HTML ──────────────────────────────────────────────────────────────
def dish_rows(lista):
    return ''.join(
        f'<div class="dish"><div class="dn">{n}</div><div class="dp">{p}</div></div>'
        for n, p in lista
    )

def tier_cards():
    cards = ''
    for t in KIT_TIERS:
        feat  = ' featured' if t['featured'] else ''
        badge = f'<div class="tc-badge">{t["badge"]}</div>' if t['badge'] else '<div class="tc-badge-placeholder"></div>'
        u_min = min(s['unit'] for s in t['sizes'])
        u_max = max(s['unit'] for s in t['sizes'])
        rows  = ''.join(
            f'<div class="tc-row">'
            f'<span class="tc-size">{s["label"]}</span>'
            f'<span class="tc-total">R$ {s["total"]}</span>'
            f'</div>'
            for s in t['sizes']
        )
        cards += (
            f'<div class="tc{feat}">'
            f'<div class="tc-head">'
            f'{badge}'
            f'<div class="tc-name">{t["name"]}</div>'
            f'<div class="tc-qty">{t["qty"]}</div>'
            f'<div class="tc-per">marmitas</div>'
            f'<div class="tc-price">R$ {u_min}–{u_max}<span class="tc-un">/un</span></div>'
            f'</div>'
            f'<div class="tc-body">{rows}</div>'
            f'</div>'
        )
    return cards

# ── Logo ──────────────────────────────────────────────────────────────────────
_base = os.path.dirname(os.path.abspath(__file__))
_logo_b64  = base64.b64encode(open(f'{_base}/logo_casa_celi_real.png', 'rb').read()).decode()
LOGO = f'data:image/png;base64,{_logo_b64}'

def logo_seal(size=130, padding=10, border_w=2):
    return (f'<div style="width:{size}px;height:{size}px;background:{FUNDO};'
            f'border-radius:50%;border:{border_w}px solid {DOURADO};'
            f'display:flex;align-items:center;justify-content:center;padding:{padding}px;">'
            f'<img src="{LOGO}" style="width:100%;height:100%;object-fit:contain;"/>'
            f'</div>')

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: Georgia,"Times New Roman",serif; color:{MARROM}; }}

/* ═══════════ UTILITÁRIOS ═══════════ */
.page-break {{ page-break-after:always; }}
.mono {{ font-family:"Courier New",monospace; }}
.upper {{ text-transform:uppercase; letter-spacing:4px; }}
.center {{ text-align:center; }}

/* ═══════════ CABEÇALHO PADRÃO ═══════════ */
.ph {{
  background:{VERDE};
  padding:12px 18mm;
  display:flex; align-items:center; gap:16px;
  margin-bottom:0;
}}
.ph-seal {{
  flex-shrink:0;
}}
.ph-div {{ width:1px; height:52px; background:rgba(250,248,243,.18); flex-shrink:0; }}
.ph-text {{ flex:1; }}
.ph-eye {{
  font-family:"Courier New",monospace; font-size:7.5px;
  letter-spacing:5px; text-transform:uppercase; color:{OLIVA};
}}
.ph-title {{ font-size:19px; color:{FUNDO}; font-weight:bold; margin-top:3px; }}

/* ═══════════ PÁGINA GENÉRICA ═══════════ */
.page {{
  width:210mm; min-height:297mm;
  background:{FUNDO};
  display:flex; flex-direction:column;
}}
.page-body {{ flex:1; padding:18px 18mm 14px; }}

/* Rodapé de página */
.page-foot {{
  padding:10px 18mm;
  border-top:1px solid rgba(143,156,104,.22);
  display:flex; justify-content:space-between; align-items:center;
  flex-shrink:0;
}}
.pf-brand {{ font-size:8.5px; color:{OLIVA}; font-style:italic; }}
.pf-wa    {{ font-family:"Courier New",monospace; font-size:9px; color:{VERDE}; letter-spacing:1.5px; }}

/* ═══════════ CAPA (P1) ═══════════ */
.cover {{
  width:210mm; height:297mm;
  background: linear-gradient(170deg, {FUNDO} 0%, {FUNDO2} 60%, {CREME} 100%);
  display:flex; flex-direction:column;
  position:relative; overflow:hidden;
}}
.cover-stripe {{
  background:{VERDE}; padding:14px 0; text-align:center; flex-shrink:0;
}}
.cover-stripe-label {{
  font-family:"Courier New",monospace; font-size:7px;
  letter-spacing:8px; text-transform:uppercase; color:rgba(250,248,243,.55);
}}
.cover-center {{
  flex:1; display:flex; flex-direction:column;
  align-items:center; justify-content:center; padding:30px;
}}
.cover-brand {{
  font-size:48px; font-weight:bold; color:{VERDE};
  letter-spacing:4px; margin-top:20px; text-align:center;
}}
.cover-sub {{
  font-family:"Courier New",monospace; font-size:9px;
  text-transform:uppercase; letter-spacing:6px;
  color:{OLIVA}; margin-top:6px; text-align:center;
}}
.cover-tagline {{
  font-size:13px; font-style:italic; color:{MARROM};
  text-align:center; margin-top:14px; line-height:1.6;
  opacity:.8; max-width:320px;
}}
.cover-ornament {{
  display:flex; align-items:center; gap:12px; margin:20px 0;
}}
.cover-orn-line {{
  width:55px; height:1px; background:{DOURADO}; opacity:.5;
}}
.cover-orn-dot {{
  font-family:"Courier New",monospace; font-size:10px; color:{DOURADO};
}}
.cover-city {{
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:5px;
  color:{OLIVA}; text-align:center; margin-top:8px;
}}
.cover-foot {{
  background:{VERDE}; padding:16px 0 18px; text-align:center; flex-shrink:0;
}}
.cover-foot-label {{
  font-family:"Courier New",monospace; font-size:7.5px;
  letter-spacing:5px; text-transform:uppercase; color:rgba(250,248,243,.5);
}}
.cover-foot-wa {{
  font-family:"Courier New",monospace; font-size:22px;
  color:{DOURADO}; letter-spacing:4px; margin:6px 0;
}}
.cover-foot-sub {{
  font-family:"Courier New",monospace; font-size:7px;
  text-transform:uppercase; letter-spacing:4px; color:rgba(250,248,243,.35);
}}

/* ═══════════ APRESENTAÇÃO (P2) ═══════════ */
.intro-text {{
  background:rgba(44,95,52,.04);
  border-left:3px solid {DOURADO};
  padding:14px 18px; margin-bottom:22px;
  font-size:12px; line-height:1.8; color:{MARROM};
}}
.intro-text p + p {{ margin-top:10px; }}

.benefits {{ display:flex; gap:10px; margin-bottom:24px; }}
.benefit {{
  flex:1; text-align:center;
  background:white; border:1px solid rgba(143,156,104,.25);
  padding:16px 10px;
}}
.benefit-icon {{
  font-size:22px; color:{VERDE}; margin-bottom:8px;
  font-family:"Courier New",monospace; font-weight:bold;
}}
.benefit-title {{
  font-size:11px; font-weight:bold; color:{VERDE};
  text-transform:uppercase; letter-spacing:1.5px;
  margin-bottom:6px;
}}
.benefit-text {{ font-size:9.5px; color:{MARROM}; line-height:1.6; opacity:.8; }}

.sec-title {{
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:6px;
  color:{TERRA}; text-align:center; margin-bottom:16px;
}}
.sec-divider {{
  display:flex; align-items:center; gap:10px; margin-bottom:16px;
}}
.sec-divider-line {{ flex:1; height:1px; background:rgba(143,156,104,.28); }}
.sec-divider-dot  {{ width:4px; height:4px; border-radius:50%; background:{DOURADO}; flex-shrink:0; }}

.steps {{ display:flex; gap:8px; margin-bottom:20px; }}
.step {{
  flex:1; text-align:center;
  padding:14px 8px;
}}
.step-n {{
  width:32px; height:32px; border-radius:50%;
  background:{VERDE}; color:{FUNDO};
  font-family:"Courier New",monospace; font-size:14px; font-weight:bold;
  display:flex; align-items:center; justify-content:center;
  margin:0 auto 8px;
}}
.step-t {{ font-size:11px; font-weight:bold; color:{VERDE}; margin-bottom:4px; }}
.step-d {{ font-size:9px; color:{MARROM}; line-height:1.5; opacity:.75; }}

.step-connector {{
  display:flex; align-items:center; padding-top:16px;
}}
.step-arrow {{
  font-family:"Courier New",monospace; color:{DOURADO};
  font-size:16px; margin:0 2px;
}}

/* ═══════════ CARDÁPIO (P3) ═══════════ */
.sec {{ margin-bottom:18px; }}
.sh  {{ display:flex; align-items:center; gap:10px; margin-bottom:10px; }}
.sl  {{
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:5px;
  color:{TERRA}; white-space:nowrap;
}}
.sr  {{ flex:1; height:1px; background:rgba(143,156,104,.3); }}

.dish {{
  display:flex; justify-content:space-between; align-items:center;
  padding:8px 12px; margin-bottom:2px;
  border-bottom:1px dotted rgba(143,156,104,.2);
}}
.dish:last-child {{ border-bottom:none; }}
.dn {{ font-size:12.5px; font-weight:bold; color:{VERDE}; }}
.dp {{
  font-family:"Courier New",monospace; font-size:12px;
  color:{DOURADO}; font-weight:bold; white-space:nowrap;
  background:rgba(184,154,74,.08); padding:3px 9px;
}}

.size-note {{
  padding:12px 16px; margin-top:10px;
  background:rgba(44,95,52,.04); border-left:3px solid {DOURADO};
}}
.sn-lbl  {{
  font-family:"Courier New",monospace; font-size:7.5px;
  text-transform:uppercase; letter-spacing:3px; color:{OLIVA}; margin-bottom:7px;
}}
.sn-row  {{ display:flex; gap:28px; }}
.sn-item {{ font-size:12px; color:{VERDE}; font-weight:bold; }}
.sn-item span {{ font-weight:normal; color:{MARROM}; font-size:11px; }}
.sn-foot {{ font-size:8px; color:{MARROM}; font-style:italic; margin-top:5px; opacity:.65; }}

/* ═══════════ KITS (P4) ═══════════ */
.kits-page {{
  width:210mm; min-height:297mm;
  background:{VERDE};
  display:flex; flex-direction:column;
}}
.kh {{
  background:rgba(0,0,0,.18);
  padding:20px 16mm 16px;
  text-align:center;
  display:flex; flex-direction:column; align-items:center;
  flex-shrink:0;
}}
.kh-eye   {{
  font-family:"Courier New",monospace; font-size:7.5px;
  text-transform:uppercase; letter-spacing:6px; color:{OLIVA}; margin-bottom:4px;
}}
.kh-title {{ font-size:28px; color:{DOURADO}; letter-spacing:2px; }}
.kh-div   {{ width:50px; height:1px; background:rgba(184,154,74,.4); margin:10px auto 8px; }}
.kh-sub   {{ font-size:10px; color:{OLIVA}; font-style:italic; line-height:1.7; }}

.tier-cards {{ display:flex; gap:10px; margin:16px 14mm; flex:1; }}
.tc {{
  flex:1; border:1px solid rgba(184,154,74,.2); overflow:hidden;
  display:flex; flex-direction:column;
}}
.tc.featured {{ border-color:{DOURADO}; }}

.tc-head {{
  padding:16px 12px 14px; text-align:center;
  background:rgba(250,248,243,.05);
  border-bottom:1px solid rgba(184,154,74,.12);
  flex-shrink:0;
}}
.tc.featured .tc-head {{
  background:rgba(184,154,74,.12);
  border-bottom-color:rgba(184,154,74,.28);
}}

.tc-badge {{
  display:inline-block;
  font-family:"Courier New",monospace; font-size:7px;
  text-transform:uppercase; letter-spacing:3px;
  padding:3px 9px; margin-bottom:10px;
  background:{DOURADO}; color:{VERDE}; font-weight:bold;
}}
.tc:not(.featured) .tc-badge {{
  background:rgba(176,82,22,.25); color:{TERRA};
}}
.tc-badge-placeholder {{ height:21px; margin-bottom:10px; }}

.tc-name {{
  font-family:"Courier New",monospace; font-size:7.5px;
  text-transform:uppercase; letter-spacing:5px;
  color:rgba(250,248,243,.4); margin-bottom:5px;
}}
.tc-qty {{
  font-size:50px; font-weight:bold; color:{FUNDO};
  line-height:1; letter-spacing:-2px;
}}
.tc.featured .tc-qty {{ color:{DOURADO}; }}
.tc-per {{
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:3px; color:{OLIVA}; margin-top:2px;
}}
.tc-price {{
  margin-top:12px; font-family:"Courier New",monospace;
  font-size:17px; font-weight:bold; color:{FUNDO};
}}
.tc.featured .tc-price {{ color:{DOURADO}; }}
.tc-un {{ font-size:9px; font-weight:normal; color:{OLIVA}; }}

.tc-body {{ padding:4px 0; flex:1; }}
.tc-row {{
  display:flex; justify-content:space-between; align-items:center;
  padding:9px 12px; border-bottom:1px solid rgba(250,248,243,.05);
}}
.tc-row:last-child {{ border-bottom:none; }}
.tc-size  {{ font-size:10px; color:rgba(250,248,243,.5); font-family:"Courier New",monospace; }}
.tc-total {{ font-family:"Courier New",monospace; font-size:14px; font-weight:bold; color:{FUNDO}; }}
.tc.featured .tc-total {{ color:{DOURADO}; }}

.kits-note {{
  text-align:center; font-size:9px; color:{OLIVA};
  font-style:italic; margin:0 14mm 8px;
}}
.pix-badge {{
  text-align:center; margin:0 0 12px;
}}
.pix {{
  display:inline-block;
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:2px; font-weight:bold;
  background:{DOURADO}; color:{VERDE}; padding:5px 18px;
}}
.kits-foot {{
  margin:10px 14mm 0;
  border-top:1px solid rgba(184,154,74,.18);
  padding-top:14px; text-align:center; flex-shrink:0;
}}
.kf-label {{ font-family:"Courier New",monospace; font-size:7.5px; letter-spacing:4px; text-transform:uppercase; color:{OLIVA}; }}
.kf-wa    {{ font-family:"Courier New",monospace; font-size:22px; color:{FUNDO}; letter-spacing:4px; margin:5px 0; }}
.kf-tag   {{ font-size:9px; font-style:italic; color:{OLIVA}; margin-bottom:14px; }}

/* ═══════════ COMO PEDIR (P5) ═══════════ */
.order-steps {{ margin-bottom:22px; }}
.os {{
  display:flex; align-items:flex-start; gap:16px;
  padding:14px 0; border-bottom:1px solid rgba(143,156,104,.18);
}}
.os:last-child {{ border-bottom:none; }}
.os-n {{
  width:38px; height:38px; border-radius:50%;
  background:{VERDE}; color:{FUNDO};
  font-family:"Courier New",monospace; font-size:16px; font-weight:bold;
  display:flex; align-items:center; justify-content:center;
  flex-shrink:0;
}}
.os-title {{ font-size:13px; font-weight:bold; color:{VERDE}; margin-bottom:4px; }}
.os-desc  {{ font-size:10.5px; color:{MARROM}; line-height:1.6; opacity:.8; }}

.payment-box {{
  background:rgba(44,95,52,.04); border:1px solid rgba(143,156,104,.25);
  padding:14px 18px; margin-bottom:22px;
}}
.payment-title {{
  font-family:"Courier New",monospace; font-size:7.5px;
  text-transform:uppercase; letter-spacing:4px; color:{OLIVA}; margin-bottom:10px;
}}
.payment-methods {{ display:flex; gap:12px; }}
.pay-m {{
  flex:1; text-align:center; padding:10px 8px;
  background:white; border:1px solid rgba(143,156,104,.2);
  font-size:11px; color:{VERDE}; font-weight:bold;
}}

.cta-box {{
  background:{VERDE}; padding:24px; text-align:center;
}}
.cta-label {{
  font-family:"Courier New",monospace; font-size:8px;
  text-transform:uppercase; letter-spacing:5px; color:{OLIVA}; margin-bottom:10px;
}}
.cta-wa {{
  font-family:"Courier New",monospace; font-size:28px;
  font-weight:bold; color:{DOURADO}; letter-spacing:3px; margin:4px 0 10px;
}}
.cta-sub {{
  font-size:10px; font-style:italic; color:rgba(250,248,243,.55);
}}
"""

# ── HTML ──────────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>


<!-- ══════════════════════ P1 · CAPA ══════════════════════ -->
<div class="cover page-break">
  <div class="cover-stripe">
    <div class="cover-stripe-label">Marmitas Congeladas Artesanais</div>
  </div>

  <div class="cover-center">
    {logo_seal(size=280, padding=20, border_w=2)}

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


<!-- ══════════════════════ P2 · APRESENTAÇÃO ══════════════════════ -->
<div class="page page-break">

  <div class="ph">
    <div class="ph-seal">{logo_seal(size=60, padding=5, border_w=1)}</div>
    <div class="ph-div"></div>
    <div class="ph-text">
      <div class="ph-eye">Sobre nós</div>
      <div class="ph-title">{NOME} · Nossa História</div>
    </div>
  </div>

  <div class="page-body">

    <div class="intro-text">
      <p>A <strong>Casa Celi</strong> nasceu do desejo de levar para a sua mesa a autenticidade
      de uma cozinha feita com carinho — sem abrir mão da praticidade do dia a dia.</p>
      <p>Cada marmita é preparada com ingredientes frescos, temperada com amor e congelada
      no ponto certo para preservar o sabor, a nutrição e a textura de sempre.</p>
      <p>Aqui não tem industrializado escondido, nem atalho: é comida de verdade,
      feita como a sua mãe faria — só que pronta para quando você precisar.</p>
    </div>

    <div class="sec-title">Por que escolher a Casa Celi?</div>

    <div class="benefits">
      <div class="benefit">
        <div class="benefit-icon">C</div>
        <div class="benefit-title">Sabor Caseiro</div>
        <div class="benefit-text">Receitas tradicionais com ingredientes frescos e tempero da casa</div>
      </div>
      <div class="benefit">
        <div class="benefit-icon">*</div>
        <div class="benefit-title">90 Dias no Freezer</div>
        <div class="benefit-text">Congelamento seguro que preserva sabor e nutrição completa</div>
      </div>
      <div class="benefit">
        <div class="benefit-icon">+</div>
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
        <div class="step-d">Guarde no freezer por até 90 dias sem perder o sabor</div>
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


<!-- ══════════════════════ P3 · CARDÁPIO ══════════════════════ -->
<div class="page page-break">

  <div class="ph">
    <div class="ph-seal">{logo_seal(size=60, padding=5, border_w=1)}</div>
    <div class="ph-div"></div>
    <div class="ph-text">
      <div class="ph-eye">Cardápio Completo</div>
      <div class="ph-title">{NOME} · Marmitas Congeladas</div>
    </div>
  </div>

  <div class="page-body">

    <div class="sec">
      <div class="sh"><span class="sl">Tradicionais</span><div class="sr"></div></div>
      {dish_rows(TRADICIONAIS)}
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


<!-- ══════════════════════ P4 · KITS ══════════════════════ -->
<div class="kits-page page-break">

  <div class="kh">
    {logo_seal(size=120, padding=10, border_w=2)}
    <div class="kh-eye" style="margin-top:14px;">Monte seu estoque</div>
    <div class="kh-title">Kits &amp; Descontos</div>
    <div class="kh-div"></div>
    <div class="kh-sub">Quanto mais você pede, mais você economiza<br>Combine qualquer prato no mesmo kit</div>
  </div>

  <div class="tier-cards">{tier_cards()}</div>

  <div class="kits-note">Pedido mínimo: 10 marmitas · Kits mistos permitidos · Validade: 90 dias no freezer</div>
  <div class="pix-badge"><span class="pix">+ 3% OFF pagando com PIX</span></div>

  <div class="kits-foot">
    <div class="kf-label">Faça seu pedido · WhatsApp</div>
    <div class="kf-wa">{WA}</div>
    <div class="kf-tag">Casa Celi · Congelados com sabor de cozinha afetiva</div>
  </div>

</div>


<!-- ══════════════════════ P5 · COMO PEDIR ══════════════════════ -->
<div class="page">

  <div class="ph">
    <div class="ph-seal">{logo_seal(size=60, padding=5, border_w=1)}</div>
    <div class="ph-div"></div>
    <div class="ph-text">
      <div class="ph-eye">Pedido simples e rápido</div>
      <div class="ph-title">{NOME} · Como Pedir</div>
    </div>
  </div>

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
          <div class="os-desc">Receba suas marmitas, guarde no freezer e tenha refeições prontas por até 90 dias. Aqueça em banho-maria ou micro-ondas e sirva.</div>
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
print(f"OK → {output}")
