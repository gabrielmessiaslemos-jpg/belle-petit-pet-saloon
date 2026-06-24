#!/usr/bin/env python3
"""Gera CasaCeli_Cardapio_Texto.pdf — com logo SVG fiel à marca."""

import math

# ── preços avulsas ───────────────────────────────────────────────────────────
BASE = {'300': 18.00, '400': 20.00, '500': 22.00}

# ── preços por kit (por unidade × qtd) ───────────────────────────────────────
# 10 marmitas = R$19/un · 20 = R$18/un · 30 = R$17/un (qualquer gramagem)
KIT_TIERS = [
    {'qty': 10, 'unit': 19.00, 'label': '10 marmitas', 'off': 'Preço base'},
    {'qty': 20, 'unit': 18.00, 'label': '20 marmitas', 'off': '5% OFF',  'best': True},
    {'qty': 30, 'unit': 17.00, 'label': '30 marmitas', 'off': '10% OFF'},
]

def row_kits():
    rows = ''
    for tier in KIT_TIERS:
        total = tier['qty'] * tier['unit']
        best  = ' best' if tier.get('best') else ''
        rows += (f'<tr>'
                 f'<td class="cg">{tier["label"]}</td>'
                 f'<td class="cv{best}" style="text-align:left;padding-left:20px">'
                 f'R$ {tier["unit"]:.0f},00 / marmita</td>'
                 f'<td class="cv{best}">R$ {total:.0f}<span class="un">economia real</span></td>'
                 f'<td class="cv{best} off-badge">{tier["off"]}</td>'
                 f'</tr>')
    return rows

# ── SVG: badge oval com bordas festonadas ────────────────────────────────────
def scalloped_oval(cx, cy, rx, ry, bumps=26, amp=7):
    steps = bumps * 24
    pts = []
    for i in range(steps + 1):
        t = 2 * math.pi * i / steps
        s = 1 + (amp / ((rx + ry) / 2)) * math.cos(bumps * t)
        pts.append(f"{cx + rx*s*math.cos(t):.2f},{cy + ry*s*math.sin(t):.2f}")
    return "M " + " L ".join(pts) + " Z"

BADGE = scalloped_oval(250, 215, 210, 220)

# ── SVG completo do logo ─────────────────────────────────────────────────────
LOGO_SVG = f"""
<svg viewBox="0 0 500 470" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <defs>
    <filter id="sh" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="5" stdDeviation="10" flood-color="#00000022"/>
    </filter>
  </defs>

  <!-- ── Badge background ── -->
  <path d="{BADGE}" fill="#FEFAF3" filter="url(#sh)" stroke="white" stroke-width="6"/>
  <path d="{BADGE}" fill="none" stroke="#2C5F34" stroke-width="2.5"/>
  <!-- Inner ring -->
  <ellipse cx="250" cy="215" rx="194" ry="203" fill="none" stroke="#C4952A"
           stroke-width="0.8" stroke-dasharray="3 4"/>

  <!-- ── Trigo no topo ── -->
  <g transform="translate(250,58)">
    <!-- haste central -->
    <line x1="0" y1="38" x2="0" y2="-10" stroke="#C4952A" stroke-width="2"/>
    <!-- grãos centrais -->
    <ellipse cx="0"  cy="-10" rx="7"  ry="13" fill="#C4952A" transform="rotate(0)"/>
    <ellipse cx="-9" cy="2"   rx="6"  ry="11" fill="#C4952A" transform="rotate(-20,-9,2)"/>
    <ellipse cx="9"  cy="2"   rx="6"  ry="11" fill="#C4952A" transform="rotate(20,9,2)"/>
    <ellipse cx="-14" cy="14"  rx="5" ry="10" fill="#C4952A" transform="rotate(-30,-14,14)"/>
    <ellipse cx="14"  cy="14"  rx="5" ry="10" fill="#C4952A" transform="rotate(30,14,14)"/>
    <!-- vapor -->
    <path d="M -12 35 Q -18 20 -10 5"  stroke="#C4952A" stroke-width="1.2" fill="none" opacity="0.55" stroke-linecap="round"/>
    <path d="M 0 38 Q 0 18 0 2"        stroke="#C4952A" stroke-width="1.2" fill="none" opacity="0.55" stroke-linecap="round"/>
    <path d="M 12 35 Q 18 20 10 5"     stroke="#C4952A" stroke-width="1.2" fill="none" opacity="0.55" stroke-linecap="round"/>
  </g>

  <!-- ── Ramos de oliveira esquerdo ── -->
  <g transform="translate(75,188)">
    <path d="M 0 20 Q 20 -10 50 -55" stroke="#2C5F34" stroke-width="1.8" fill="none"/>
    <ellipse cx="12"  cy="5"   rx="14" ry="5.5" fill="#2C5F34" transform="rotate(-35,12,5)"/>
    <ellipse cx="24"  cy="-12" rx="14" ry="5.5" fill="#2C5F34" transform="rotate(-42,24,-12)"/>
    <ellipse cx="36"  cy="-29" rx="13" ry="5"   fill="#2C5F34" transform="rotate(-50,36,-29)"/>
    <ellipse cx="46"  cy="-46" rx="12" ry="4.5" fill="#2C5F34" transform="rotate(-55,46,-46)"/>
    <!-- bacas -->
    <circle cx="10"  cy="3"   r="3" fill="#6B8F4A" opacity="0.7"/>
    <circle cx="28"  cy="-16" r="3" fill="#6B8F4A" opacity="0.7"/>
  </g>

  <!-- ── Ramos de oliveira direito (espelhado) ── -->
  <g transform="translate(425,188) scale(-1,1)">
    <path d="M 0 20 Q 20 -10 50 -55" stroke="#2C5F34" stroke-width="1.8" fill="none"/>
    <ellipse cx="12"  cy="5"   rx="14" ry="5.5" fill="#2C5F34" transform="rotate(-35,12,5)"/>
    <ellipse cx="24"  cy="-12" rx="14" ry="5.5" fill="#2C5F34" transform="rotate(-42,24,-12)"/>
    <ellipse cx="36"  cy="-29" rx="13" ry="5"   fill="#2C5F34" transform="rotate(-50,36,-29)"/>
    <ellipse cx="46"  cy="-46" rx="12" ry="4.5" fill="#2C5F34" transform="rotate(-55,46,-46)"/>
    <circle cx="10"  cy="3"   r="3" fill="#6B8F4A" opacity="0.7"/>
    <circle cx="28"  cy="-16" r="3" fill="#6B8F4A" opacity="0.7"/>
  </g>

  <!-- Folhas ornamentais menores flanqueando a panela -->
  <g transform="translate(120,210)">
    <path d="M 0 0 Q 8 -18 0 -32" stroke="#2C5F34" stroke-width="1.2" fill="none"/>
    <ellipse cx="4"  cy="-10" rx="9"  ry="4" fill="#2C5F34" transform="rotate(-40,4,-10)"/>
    <ellipse cx="-2" cy="-22" rx="8"  ry="3.5" fill="#2C5F34" transform="rotate(-55,-2,-22)"/>
  </g>
  <g transform="translate(380,210) scale(-1,1)">
    <path d="M 0 0 Q 8 -18 0 -32" stroke="#2C5F34" stroke-width="1.2" fill="none"/>
    <ellipse cx="4"  cy="-10" rx="9"  ry="4" fill="#2C5F34" transform="rotate(-40,4,-10)"/>
    <ellipse cx="-2" cy="-22" rx="8"  ry="3.5" fill="#2C5F34" transform="rotate(-55,-2,-22)"/>
  </g>

  <!-- Arabescos ornamentais -->
  <path d="M 120 232 Q 140 220 160 228 Q 150 218 170 222" stroke="#C4952A" stroke-width="1"
        fill="none" stroke-linecap="round" opacity="0.8"/>
  <path d="M 380 232 Q 360 220 340 228 Q 350 218 330 222" stroke="#C4952A" stroke-width="1"
        fill="none" stroke-linecap="round" opacity="0.8"/>

  <!-- ── Panela de barro ── -->
  <g transform="translate(250,195)">
    <!-- Sombra da panela -->
    <ellipse cx="0" cy="50" rx="58" ry="10" fill="#00000015"/>
    <!-- Tampa - base -->
    <path d="M -52 -42 Q 0 -28 52 -42 Q 0 -30 -52 -42 Z" fill="#A34820"/>
    <!-- Tampa - domo -->
    <path d="M -52 -42 Q -48 -72 -20 -80 Q 0 -84 20 -80 Q 48 -72 52 -42 Z" fill="#C05A28"/>
    <!-- Tampa - aba -->
    <path d="M -55 -42 Q 0 -36 55 -42 Q 0 -50 -55 -42 Z" fill="#A34820"/>
    <!-- Botão da tampa -->
    <ellipse cx="0" cy="-84" rx="10" ry="7" fill="#8B3A18"/>
    <ellipse cx="0" cy="-87" rx="7" ry="4" fill="#C05A28"/>
    <!-- Corpo da panela -->
    <path d="M -60 -32 Q -72 8 -60 48 Q 0 62 60 48 Q 72 8 60 -32 Q 0 -24 -60 -32 Z" fill="#C05A28"/>
    <!-- Anel superior do corpo -->
    <ellipse cx="0" cy="-32" rx="60" ry="12" fill="#A34820"/>
    <!-- Alça esquerda -->
    <path d="M -60 -15 Q -88 -22 -86 8 Q -84 28 -60 22" fill="none" stroke="#A34820"
          stroke-width="10" stroke-linecap="round"/>
    <!-- Alça direita -->
    <path d="M 60 -15 Q 88 -22 86 8 Q 84 28 60 22" fill="none" stroke="#A34820"
          stroke-width="10" stroke-linecap="round"/>
    <!-- Reflexo / highlight -->
    <path d="M -35 -20 Q -28 5 -30 30" stroke="white" stroke-width="3" fill="none"
          opacity="0.15" stroke-linecap="round"/>
    <!-- Anel inferior do corpo -->
    <path d="M -58 42 Q 0 56 58 42 Q 0 52 -58 42 Z" fill="#A34820" opacity="0.6"/>
  </g>

  <!-- ── Arabescos decorativos abaixo da panela ── -->
  <path d="M 145 282 Q 175 272 200 278" stroke="#C4952A" stroke-width="1.2" fill="none" stroke-linecap="round"/>
  <path d="M 355 282 Q 325 272 300 278" stroke="#C4952A" stroke-width="1.2" fill="none" stroke-linecap="round"/>
  <circle cx="250" cy="279" r="2.5" fill="#C4952A"/>

  <!-- ── Texto: Casa Celi ── -->
  <text x="250" y="324" text-anchor="middle"
        font-family="Georgia,'Times New Roman',serif"
        font-size="58" font-weight="bold" fill="#2C5F34" letter-spacing="1">Casa Celi</text>

  <!-- ── Divisória com ornamento ── -->
  <line x1="118" y1="338" x2="216" y2="338" stroke="#C4952A" stroke-width="1.2"/>
  <path d="M 234 335 Q 250 330 266 335 M 234 341 Q 250 346 266 341" stroke="#C4952A" stroke-width="0.8" fill="none"/>
  <circle cx="250" cy="338" r="2" fill="#C4952A"/>
  <line x1="284" y1="338" x2="382" y2="338" stroke="#C4952A" stroke-width="1.2"/>

  <!-- ── Texto: CONGELADOS ARTESANAIS ── -->
  <text x="250" y="360" text-anchor="middle"
        font-family="Arial,Helvetica,sans-serif"
        font-size="14.5" font-weight="bold" fill="#2C5F34" letter-spacing="3.5">CONGELADOS ARTESANAIS</text>

  <!-- ── Ornamento folha entre texto e fita ── -->
  <g transform="translate(250,374)">
    <path d="M -10 0 Q 0 -14 10 0" fill="#2C5F34"/>
    <path d="M -6 0 Q 0 -8 6 0"    fill="#4A7A50" opacity="0.6"/>
    <line x1="0" y1="-5" x2="0" y2="8" stroke="#2C5F34" stroke-width="1.2"/>
    <circle cx="-14" cy="1" r="2.5" fill="#C4952A"/>
    <circle cx="14"  cy="1" r="2.5" fill="#C4952A"/>
  </g>

  <!-- ── Fita/banner ── -->
  <!-- Sombra da fita -->
  <path d="M 35 402 L 15 420 L 40 432 L 460 432 L 485 420 L 465 402 Z"
        fill="#00000018"/>
  <!-- Cauda esquerda -->
  <path d="M 42 395 L 18 413 L 42 428 L 215 428 L 215 395 Z" fill="#9B3F1A"/>
  <!-- Cauda direita -->
  <path d="M 458 395 L 482 413 L 458 428 L 285 428 L 285 395 Z" fill="#9B3F1A"/>
  <!-- Centro da fita -->
  <rect x="22" y="392" width="456" height="38" rx="2" fill="#B84E22"/>
  <!-- Reflexo superior da fita -->
  <rect x="22" y="392" width="456" height="8" rx="2" fill="white" opacity="0.08"/>
  <!-- Texto da fita -->
  <text x="250" y="417" text-anchor="middle"
        font-family="Georgia,'Times New Roman',serif"
        font-style="italic" font-size="14" fill="#FEFAF3" letter-spacing="0.3">
    Comida feita hoje para facilitar o seu amanhã
  </text>

  <!-- ── Ornamento final ── -->
  <text x="250" y="455" text-anchor="middle" font-size="13" fill="#C4952A"
        font-family="serif">✦</text>
</svg>
"""

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

.kn { text-align:center; font-size:9.5px; color:#8F9C68; font-style:italic; line-height:1.9; }
.pix { display:inline-block; margin-top:10px; font-family:"Courier New",monospace; font-size:8.5px; text-transform:uppercase; letter-spacing:2px; font-weight:bold; background:#B89A4A; color:#1E4B26; padding:5px 16px; }
.kf { margin-top:20px; text-align:center; border-top:1px solid rgba(184,154,74,.25); padding-top:16px; }
.kf-lbl { font-family:"Courier New",monospace; font-size:8px; letter-spacing:4px; text-transform:uppercase; color:#8F9C68; margin-bottom:4px; }
.kf-wa  { font-family:"Courier New",monospace; font-size:20px; color:#FAF8F3; letter-spacing:3px; }
.kf-tag { font-size:9px; font-style:italic; color:#8F9C68; margin-top:7px; }
"""

# Mini logo para cabeçalho das páginas internas (versão simplificada)
MINI_LOGO = f"""
<svg viewBox="0 0 500 470" xmlns="http://www.w3.org/2000/svg">
  <path d="{BADGE}" fill="#FEFAF3" stroke="#2C5F34" stroke-width="2.5"/>
  <ellipse cx="250" cy="215" rx="194" ry="203" fill="none" stroke="#C4952A" stroke-width="0.8" stroke-dasharray="3 4"/>
  <g transform="translate(250,195)">
    <path d="M -52 -42 Q 0 -30 52 -42 Q 48 -68 20 -76 Q 0 -80 -20 -76 Q -48 -68 -52 -42 Z" fill="#C05A28"/>
    <ellipse cx="0" cy="-83" rx="9" ry="6" fill="#8B3A18"/>
    <path d="M -60 -32 Q -70 8 -58 46 Q 0 60 58 46 Q 70 8 60 -32 Q 0 -24 -60 -32 Z" fill="#C05A28"/>
    <ellipse cx="0" cy="-32" rx="60" ry="12" fill="#A34820"/>
    <path d="M -60 -15 Q -86 -20 -84 8 Q -82 26 -60 22" fill="none" stroke="#A34820" stroke-width="9" stroke-linecap="round"/>
    <path d="M 60 -15 Q 86 -20 84 8 Q 82 26 60 22" fill="none" stroke="#A34820" stroke-width="9" stroke-linecap="round"/>
  </g>
  <text x="250" y="324" text-anchor="middle" font-family="Georgia,serif" font-size="56" font-weight="bold" fill="#2C5F34">Casa Celi</text>
  <line x1="120" y1="337" x2="218" y2="337" stroke="#C4952A" stroke-width="1.2"/>
  <circle cx="250" cy="337" r="2" fill="#C4952A"/>
  <line x1="282" y1="337" x2="380" y2="337" stroke="#C4952A" stroke-width="1.2"/>
  <text x="250" y="358" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="bold" fill="#2C5F34" letter-spacing="3.5">CONGELADOS ARTESANAIS</text>
  <path d="M 28 395 L 8 413 L 28 428 L 472 428 L 492 413 L 472 395 Z" fill="#B84E22" opacity="0.9"/>
  <rect x="8" y="392" width="484" height="38" rx="2" fill="#C05A28"/>
  <text x="250" y="417" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="13.5" fill="#FEFAF3">Comida feita hoje para facilitar o seu amanhã</text>
</svg>
"""

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
    <div class="dish"><div class="dl"><div class="dn">Frango Desfiado ao Creme de Milho</div><div class="dd">Frango cozido lentamente e desfiado, envolvido em creme de milho suave com ervas da casa</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Frango em Cubos Acebolado</div><div class="dd">Cubos de peito de frango dourados com cebola caramelizada e temperos especiais</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Almôndegas ao Molho Pomodoro</div><div class="dd">Almôndegas artesanais de carne moída cozidas em molho de tomate fresco com manjericão</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Frango Xadrez da Casa</div><div class="dd">Peito de frango com legumes coloridos no molho agridoce oriental — receita exclusiva</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Filé de Frango ao Molho de Mel</div><div class="dd">Filé grelhado finalizado com molho de mel e mostarda, suculento e aromático</div></div><div class="dp">R$ 20,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Filé de Merluza</div><div class="dd">Filé de merluza temperado com limão, alho e ervas frescas, assado no ponto certo</div></div><div class="dp">R$ 20,00</div></div>
  </div>

  <div class="sec">
    <div class="sh"><span class="sl">Premium</span><div class="sr"></div></div>
    <div class="dish"><div class="dl"><div class="dn">Parmegiana com Crosta</div><div class="dd">Filé empanado com crosta crocante, molho de tomate encorpado e queijo gratinado</div></div><div class="dp">R$ 28,50</div></div>
    <div class="dish"><div class="dl"><div class="dn">Nhoque à Bolonhesa</div><div class="dd">Nhoque artesanal de batata com ragù de carne ao molho bolonhesa — feito na hora</div></div><div class="dp">R$ 33,50</div></div>
    <div class="dish"><div class="dl"><div class="dn">Lasanha Saborosa</div><div class="dd">Montada em camadas com carne moída temperada, molho branco cremoso e queijo</div></div><div class="dp">R$ 26,00</div></div>
    <div class="dish"><div class="dl"><div class="dn">Escondidinho Caprichado</div><div class="dd">Carne desfiada e temperada escondida sob purê cremoso de mandioca gratinado</div></div><div class="dp">R$ 24,50</div></div>
    <div class="dish"><div class="dl"><div class="dn">Panquecas Caseiras</div><div class="dd">Panquecas recheadas com frango desfiado ou carne moída, cobertas com molho de tomate</div></div><div class="dp">R$ 23,50</div></div>
    <div class="dish"><div class="dl"><div class="dn">Macarrões da Casa</div><div class="dd">Massa no ponto certo · molho à escolha: Sugo · Bolonhesa · Alho e Óleo · Bechamel</div></div><div class="dp">R$ 24,90</div></div>
  </div>

  <div class="sec">
    <div class="sh"><span class="sl">Caldos Artesanais</span><div class="sr"></div></div>
    <div class="dish"><div class="dl"><div class="dn">Caldo Artesanal (500 ml)</div><div class="dd">Preparado lentamente com ingredientes frescos · pergunte o sabor disponível</div></div><div class="dp">R$ 21,90</div></div>
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
    <div class="ds"><div class="ds-n">R$ 19</div><div class="ds-un">por marmita · Kit 10</div><div class="ds-off">R$ 190 total</div></div>
    <div class="ds act"><div class="ds-n">R$ 18</div><div class="ds-un">por marmita · Kit 20</div><div class="ds-off">R$ 360 total · 5% OFF</div></div>
    <div class="ds"><div class="ds-n">R$ 17</div><div class="ds-un">por marmita · Kit 30</div><div class="ds-off">R$ 510 total · 10% OFF</div></div>
  </div>

  <table class="kit-table">
    <thead>
      <tr>
        <th style="text-align:left">Qtd</th>
        <th style="text-align:left;padding-left:20px">Preço por marmita</th>
        <th>Total do kit</th>
        <th>Desconto</th>
      </tr>
    </thead>
    <tbody>
      {row_kits()}
    </tbody>
  </table>

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
