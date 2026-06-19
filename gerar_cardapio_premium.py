#!/usr/bin/env python3
"""
Cardápio Gourmet Premium — Casa Celi Congelados Artesanais
Nível: Agência de Branding Gastronômico
"""

import os, sys, io, math, requests
from io import BytesIO
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.utils import ImageReader
import fitz

W, H = A4  # 595.27 x 841.89 pts

# ── PALETA OBRIGATÓRIA ───────────────────────────────────────────────────────
VM = "#1E4B26"   # Verde musgo
VO = "#8F9C68"   # Verde oliva
TC = "#B05216"   # Terracota
MA = "#4F2915"   # Marrom
DQ = "#B89A4A"   # Dourado envelhecido
PG = "#FAF8F3"   # Fundo pergaminho
BR = "#FFFFFF"
PR = "#1C1C1C"
CS = "#E8E4DC"   # Cinza suave
CT = "#4A4240"   # Cinza texto
DK = "#8B6914"   # Dourado escuro
LG = "#D4EDDA"   # Verde claro texto

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def sf(c, h):   c.setFillColorRGB(*hex2rgb(h))
def ss(c, h):   c.setStrokeColorRGB(*hex2rgb(h))
def sfa(c, h, a): r,g,b = hex2rgb(h); c.setFillColorRGB(r,g,b,a)


# ── FOTOS UNSPLASH ───────────────────────────────────────────────────────────
PHOTOS = {
    "cover":           "1565299624946-b28f40a0ae38",
    "frango_desfiado": "1568901346375-23c9450c58cd",
    "frango_cubos":    "1598515214211-89d3c73ae83b",
    "frango_xadrez":   "1603133872878-684f208fb84b",
    "frango_mel":      "1559847814-e7c79c9b01af",
    "merluza":         "1519708227418-c8fd9a32b7a2",
    "almondegas":      "1529042410759-befb1204b468",
    "parmegiana":      "1565299507177-b0ac66763828",
    "escondidinho":    "1586190848861-99aa4a171e90",
    "panquecas":       "1519984388953-d2406bc725e1",
    "nhoque":          "1579631542720-3a87824fff86",
    "lasanha":         "1574071318508-1cdbab80d002",
    "macarrao":        "1555949258-eb67b1ef0ceb",
    "kits_bg":         "1543352633-16e549d6-d596",
    "cta":             "1414235077428-338989a2e8c0",
}

FALLBACK = {
    "cover": "#1A2E1A", "frango_desfiado": "#5C3D1A", "frango_cubos": "#6B3A20",
    "frango_xadrez": "#4A3A10", "frango_mel": "#7A5000", "merluza": "#1A3A4A",
    "almondegas": "#5C2A10", "parmegiana": "#6A2A08", "escondidinho": "#4F2915",
    "panquecas": "#7A5010", "nhoque": "#5C3A10", "lasanha": "#6B2010",
    "macarrao": "#7A4010", "kits_bg": "#1E3A20", "cta": "#1A2818",
}

import random
import struct

def noise_field(w, h, scale=40, seed=0):
    """Simple value-noise approximation for texture."""
    import hashlib
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            gx, gy = x // scale, y // scale
            fx, fy = (x % scale) / scale, (y % scale) / scale
            def corner(cx, cy):
                h_val = int(hashlib.md5(f"{seed}{cx}{cy}".encode()).hexdigest(), 16) % 256
                return h_val / 255.0
            c00 = corner(gx, gy); c10 = corner(gx+1, gy)
            c01 = corner(gx, gy+1); c11 = corner(gx+1, gy+1)
            top = c00 + fx*(c10-c00); bot = c01 + fx*(c11-c01)
            row.append(top + fy*(bot-top))
        out.append(row)
    return out

def make_food_image(key, w, h):
    """Gera imagem gastronômica artística via Pillow com gradientes quentes."""
    CONFIGS = {
        # (bg_top, bg_bottom, plate_color, food1, food2, food3, accent_spots, label_hint)
        "cover":           ("#1A2E1A","#0D1A0D","#2C1810","#5C3A1A","#8B5E1A","#B8860B","#D4A017","Capa"),
        "frango_desfiado": ("#3D2009","#1E0D04","#C8A97A","#E8C888","#D4A850","#B88030","#F5D090","Frango"),
        "frango_cubos":    ("#3A1C06","#1E0D03","#C89060","#D4A870","#E0C090","#B87040","#F0D0A0","Cubos"),
        "frango_xadrez":   ("#1C3A10","#0D1E08","#C84020","#E06030","#A83010","#F0804020","#FFB040","Xadrez"),
        "frango_mel":      ("#4A2A00","#1E1000","#D4880020","#E8A000","#C87800","#F5C040","#FFD080","Mel"),
        "merluza":         ("#0D2A3A","#061520","#8BADB5","#B0C8CC","#6090A0","#D0E8F0","#A0C8D8","Merluza"),
        "almondegas":      ("#3A0D0D","#1E0606","#8B3010","#B05020","#C87850","#D4A080","#7A2008","Almônd."),
        "parmegiana":      ("#3A0A00","#1E0500","#C83010","#D45020","#E87840","#F0A080","#B02808","Parme."),
        "escondidinho":    ("#2A1A08","#150D04","#C8A060","#D4B870","#E0D090","#A88040","#F0C890","Escondi."),
        "panquecas":       ("#3A2010","#1E1008","#D4A870","#E8C890","#C89060","#F0D8A0","#B87840","Panquecas"),
        "nhoque":          ("#3A0808","#1E0404","#C04020","#D06030","#E08050","#B03018","#F0A070","Nhoque"),
        "lasanha":         ("#3A0A0A","#1E0505","#C03015","#D05025","#E07040","#B02810","#F5906050","Lasanha"),
        "macarrao":        ("#3A2508","#1E1204","#D4A040","#E8C060","#C88020","#F0D070","#B87010","Macarrão"),
        "kits_bg":         ("#0D2010","#060E08","#1E4B26","#2D6A30","#3A8040","#509050","#8FC068","Kits"),
        "cta":             ("#1A2E1A","#0D170D","#2A4020","#3A5030","#4A6040","#5A7050","#B89A4A","CTA"),
    }
    cfg = CONFIGS.get(key, ("#1A1A1A","#0D0D0D","#4A4A4A","#606060","#707070","#808080","#909090","?"))
    c0, c1, p0, p1, p2, p3, acc, lbl = cfg

    def parse_hex(hx):
        hx = hx.lstrip("#")[:6]
        if len(hx) < 6: hx = hx + "0"*(6-len(hx))
        return int(hx[0:2],16), int(hx[2:4],16), int(hx[4:6],16)

    img = Image.new("RGB", (w, h))
    pixels = img.load()

    r0,g0,b0 = parse_hex(c0)
    r1,g1,b1 = parse_hex(c1)
    rp0,gp0,bp0 = parse_hex(p0)
    rp1,gp1,bp1 = parse_hex(p1)
    rp2,gp2,bp2 = parse_hex(p2)
    racc,gacc,bacc = parse_hex(acc)

    seed_v = abs(hash(key)) % 9999
    noise = noise_field(w, h, scale=max(30, w//10), seed=seed_v)

    for y in range(h):
        for x in range(w):
            t = y / h
            # Base gradient
            r = int(r0 + t*(r1-r0))
            g = int(g0 + t*(g1-g0))
            b = int(b0 + t*(b1-b0))

            # Center warm glow (simula iluminação sobre o prato)
            cx, cy = w*0.5, h*0.42
            dist = math.sqrt((x-cx)**2 + (y-cy)**2) / (min(w,h)*0.55)
            glow = max(0, 1 - dist*dist)

            # Plate circle
            in_plate = dist < 0.45
            if in_plate:
                plate_t = dist / 0.45
                pr = int(rp0 + plate_t*(rp1-rp0))
                pg_ = int(gp0 + plate_t*(gp1-gp0))
                pb = int(bp0 + plate_t*(bp1-bp0))
                n = noise[y][x]
                # Food texture in center
                food_t = max(0, 1 - dist/0.32)
                r = int(pr + food_t*(rp2-pr) + n*30*food_t)
                g = int(pg_ + food_t*(gp2-pg_) + n*25*food_t)
                b = int(pb + food_t*(bp2-pb) + n*20*food_t)
            else:
                # Background texture
                n = noise[y][x]
                r = max(0, min(255, int(r + n*18 + glow*30)))
                g = max(0, min(255, int(g + n*15 + glow*25)))
                b = max(0, min(255, int(b + n*12 + glow*20)))

            # Accent sparkles
            n2 = noise[(y+37)%h][(x+41)%w]
            if n2 > 0.88 and in_plate:
                blend = (n2-0.88)/0.12
                r = int(r + blend*(racc-r)*0.7)
                g = int(g + blend*(gacc-g)*0.7)
                b = int(b + blend*(bacc-b)*0.7)

            # Vignette
            vig = max(0, 0.6 - dist*0.4) if dist > 0.5 else 0
            r = max(0, min(255, int(r*(1-vig*0.5))))
            g = max(0, min(255, int(g*(1-vig*0.5))))
            b = max(0, min(255, int(b*(1-vig*0.5))))

            pixels[x, y] = (r, g, b)

    # Subtle blur for realism
    img = img.filter(ImageFilter.GaussianBlur(radius=1.2))

    buf = BytesIO()
    img.save(buf, "JPEG", quality=88)
    buf.seek(0)
    print(f"  ✓ {key} (gerado)")
    return buf

def download_img(key, w=900, h=600):
    return make_food_image(key, w, h)

def make_qr(url):
    qr = qrcode.QRCode(version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1E4B26", back_color="#FAF8F3")
    buf = BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)
    return buf

def darken_image_bottom(img_buf, darkness=0.65):
    """Add dark gradient to bottom of image for text legibility."""
    img_buf.seek(0)
    img = Image.open(img_buf).convert("RGBA")
    w, h = img.size
    grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(grad)
    for i in range(h):
        progress = max(0, (i - h * 0.35) / (h * 0.65))
        alpha = int(255 * darkness * min(1, progress * 1.5))
        draw.line([(0, i), (w, i)], fill=(10, 25, 15, alpha))
    result = Image.alpha_composite(img, grad).convert("RGB")
    out = BytesIO()
    result.save(out, "JPEG", quality=92)
    out.seek(0)
    return out


# ── DRAWING HELPERS ──────────────────────────────────────────────────────────
def rrect(c, x, y, w, h, r=8, fill=None, stroke=None, lw=1):
    p = c.beginPath()
    p.moveTo(x+r, y); p.lineTo(x+w-r, y)
    p.arcTo(x+w-r, y, x+w, y+r, 0, 90)
    p.lineTo(x+w, y+h-r)
    p.arcTo(x+w-r, y+h-r, x+w, y+h, 0, 90)
    p.lineTo(x+r, y+h)
    p.arcTo(x, y+h-r, x+r, y+h, 0, 90)
    p.lineTo(x, y+r)
    p.arcTo(x, y, x+r, y+r, 0, 90)
    p.close()
    if fill: sf(c, fill)
    else: c.setFillAlpha(0)
    if stroke: ss(c, stroke); c.setLineWidth(lw)
    c.drawPath(p, fill=1 if fill else 0, stroke=1 if stroke else 0)

def img_rect(c, buf, x, y, w, h):
    if buf is None: return
    try:
        buf.seek(0)
        c.drawImage(ImageReader(buf), x, y, w, h,
                    preserveAspectRatio=False, mask="auto")
    except Exception as e:
        print(f"    img_rect error: {e}")

def overlay(c, x, y, w, h, hex_c, alpha=0.6):
    c.saveState()
    sfa(c, hex_c, alpha)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.restoreState()

def txt(c, s, x, y, font="Helvetica", size=10, color=BR, align="left"):
    sf(c, color)
    c.setFont(font, size)
    if align == "center": c.drawCentredString(x, y, s)
    elif align == "right": c.drawRightString(x, y, s)
    else: c.drawString(x, y, s)

def wrap_txt(c, s, x, y, mw, font="Helvetica", size=10, color=CT, lh=14, max_lines=3):
    sf(c, color); c.setFont(font, size)
    words = s.split(); line = ""; count = 0
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font, size) <= mw: line = test
        else:
            if line:
                c.drawString(x, y, line); y -= lh; count += 1
                if count >= max_lines: return y
            line = word
    if line: c.drawString(x, y, line); y -= lh
    return y

def footer(c, page_n=None):
    sf(c, VM); c.rect(0, 0, W, 26, fill=1, stroke=0)
    sf(c, DQ); c.rect(0, 25, W, 2, fill=1, stroke=0)
    sf(c, DQ); c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(W/2, 9, "Casa Celi  •  Congelados Artesanais  •  Comida feita hoje para facilitar o seu amanhã.")
    if page_n:
        c.drawRightString(W - 1.5*cm, 9, str(page_n))

def section_header(c, title, subtitle="", icon=""):
    sf(c, VM); c.rect(0, H-56, W, 56, fill=1, stroke=0)
    sf(c, DQ); c.rect(0, H-58, W, 3, fill=1, stroke=0)
    sf(c, TC); c.rect(0, H-60, W, 2, fill=1, stroke=0)
    sf(c, DQ); c.setFont("Helvetica-Bold", 22)
    label = f"{icon}  {title}" if icon else title
    c.drawString(2.2*cm, H-38, label)
    if subtitle:
        sf(c, VO); c.setFont("Helvetica", 9)
        c.drawString(2.2*cm, H-52, subtitle)

def price_badge(c, price, x, y, w=110, h=26):
    rrect(c, x, y, w, h, r=7, fill=DQ)
    rrect(c, x+2, y+2, w-4, h-4, r=5, stroke=MA, lw=0.7)
    sf(c, MA); c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(x+w/2, y+8, price)

def bestseller_badge(c, x, y, label="CAMPEÃO DE VENDAS"):
    w, h = 118, 18
    rrect(c, x, y, w, h, r=5, fill=TC)
    sf(c, BR); c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(x+w/2, y+5, f"🏆  {label}")

def seal_circle(c, cx, cy, line1, line2, r=24):
    sf(c, DQ); c.circle(cx, cy, r, fill=1, stroke=0)
    ss(c, MA); c.setLineWidth(1.2); c.circle(cx, cy, r-3, fill=0, stroke=1)
    sf(c, MA); c.setFont("Helvetica-Bold", 6); c.drawCentredString(cx, cy+4, line1)
    c.setFont("Helvetica", 5); c.drawCentredString(cx, cy-4, line2)


# ── DISH CARD (foto de fundo + gradiente + texto) ────────────────────────────
def dish_card(c, img_buf, x, y, w, h, nome, desc, preco,
              badge=None, is_champion=False, accent=TC):
    c.saveState()
    # Clip para o card
    p = c.beginPath()
    r = 10
    p.moveTo(x+r, y); p.lineTo(x+w-r, y)
    p.arcTo(x+w-r, y, x+w, y+r, 0, 90)
    p.lineTo(x+w, y+h-r)
    p.arcTo(x+w-r, y+h-r, x+w, y+h, 0, 90)
    p.lineTo(x+r, y+h)
    p.arcTo(x, y+h-r, x+r, y+h, 0, 90)
    p.lineTo(x, y+r)
    p.arcTo(x, y, x+r, y+r, 0, 90)
    p.close()
    c.clipPath(p, stroke=0)

    # Imagem de fundo
    if img_buf:
        dark_buf = darken_image_bottom(img_buf, 0.72)
        img_rect(c, dark_buf, x, y, w, h)
    else:
        sf(c, "#2A2A2A"); c.rect(x, y, w, h, fill=1, stroke=0)

    # Gradiente escuro na parte inferior
    overlay(c, x, y, w, h*0.55, "#0A1508", alpha=0.75)

    c.restoreState()

    # Borda dourada
    ss(c, DQ); c.setLineWidth(1.2)
    rrect(c, x, y, w, h, r=10, stroke=DQ)

    # Barra de acento lateral esquerda
    rrect(c, x, y, 5, h, r=3, fill=accent)
    c.rect(x+2, y, 3, h, fill=1, stroke=0)

    # Champion ribbon
    if is_champion:
        bestseller_badge(c, x+8, y+h-22)

    # Badge de categoria
    if badge:
        bw, bh = 88, 17
        rrect(c, x+w-bw-8, y+h-bh-7, bw, bh, r=5, fill=VM)
        ss(c, DQ); c.setLineWidth(0.7)
        rrect(c, x+w-bw-8, y+h-bh-7, bw, bh, r=5, stroke=DQ)
        sf(c, DQ); c.setFont("Helvetica-Bold", 6.5)
        c.drawCentredString(x+w-bw/2-8, y+h-bh-7+5, badge)

    # Nome do prato
    sf(c, BR); c.setFont("Helvetica-Bold", 11.5)
    nome_y = y + 54
    nome_short = nome if len(nome) <= 30 else nome[:28]+"…"
    c.drawString(x+12, nome_y, nome_short)

    # Linha separadora
    ss(c, DQ); c.setLineWidth(0.8)
    c.line(x+12, nome_y-6, x+w-15, nome_y-6)

    # Descrição
    sf(c, "#C8DFCA"); c.setFont("Helvetica", 8)
    words = desc.split(); line = ""; dy = nome_y-20; count = 0
    mw = w - 28
    for word in words:
        test = (line+" "+word).strip()
        if c.stringWidth(test, "Helvetica", 8) <= mw: line = test
        else:
            if line:
                c.drawString(x+12, dy, line); dy -= 11; count+=1
                if count >= 3: break
            line = word
    if line and count < 3:
        c.drawString(x+12, dy, line)

    # Preço
    price_badge(c, preco, x+w-118, y+6)


# ── PAGE 1: CAPA ─────────────────────────────────────────────────────────────
def page_cover(c, imgs):
    print("  → Capa...")
    # Hero image full bleed
    if "cover" in imgs:
        buf = imgs["cover"]
        buf.seek(0)
        dark = darken_image_bottom(buf, 0.8)
        img_rect(c, dark, 0, 0, W, H)

    # Top-left dark vignette
    overlay(c, 0, H*0.55, W, H*0.45, "#000D05", alpha=0.45)

    # ── TOP AREA ──
    # Gold badge
    bw, bh = 230, 26
    rrect(c, W/2-bw/2, H-70, bw, bh, r=13, fill=DQ)
    sf(c, MA); c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(W/2, H-70+9, "✦   CATÁLOGO GOURMET ARTESANAL 2025   ✦")

    # ── MIDDLE TITLE ──
    title_y = H - 125
    sf(c, BR); c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(W/2, title_y, "MARMITAS CONGELADAS")
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(W/2, title_y-37, "COM SABOR DE COMIDA")
    c.drawCentredString(W/2, title_y-67, "FEITA EM CASA")

    # Gold separator
    sf(c, DQ); c.rect(W/2-70, title_y-84, 140, 2.5, fill=1, stroke=0)

    # Subtitle
    sf(c, LG); c.setFont("Helvetica", 10.5)
    c.drawCentredString(W/2, title_y-100, "Produzidas artesanalmente, congeladas com")
    c.drawCentredString(W/2, title_y-115, "segurança e prontas para facilitar sua rotina.")

    # ── BOTTOM BRAND PANEL ──
    panel_h = 150
    overlay(c, 0, 0, W, panel_h, VM, alpha=0.96)
    sf(c, DQ); c.rect(0, panel_h, W, 3, fill=1, stroke=0)
    sf(c, TC); c.rect(0, panel_h+2, W, 2, fill=1, stroke=0)

    # Brand name
    sf(c, BR); c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(W/2, 105, "Casa Celi")

    sf(c, VO); c.setFont("Helvetica", 10)
    c.drawCentredString(W/2, 83, "C  O  N  G  E  L  A  D  O  S    A  R  T  E  S  A  N  A  I  S")

    # Divider
    ss(c, DQ); c.setLineWidth(0.8); c.line(W/2-80, 76, W/2+80, 76)

    sf(c, DQ); c.setFont("Helvetica-Oblique", 9.5)
    c.drawCentredString(W/2, 62, '"Comida feita hoje para facilitar o seu amanhã."')

    # Pills
    pills = ["🫕  Artesanal", "✓  Sem Conservantes", "🏆  Gourmet", "🕐  Pronto em Min."]
    total_w = len(pills)*116 + (len(pills)-1)*6
    px = (W - total_w) / 2
    py = 30
    for pill in pills:
        rrect(c, px, py, 116, 20, r=10, fill=VO)
        sf(c, BR); c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(px+58, py+7, pill)
        px += 122

    footer(c, "1")


# ── PAGE 2: SELOS + INTRO LINHAS ─────────────────────────────────────────────
def page_intro(c):
    print("  → Intro & Selos...")
    sf(c, PG); c.rect(0, 0, W, H, fill=1, stroke=0)

    section_header(c, "Nossa Proposta", "Qualidade artesanal com a praticidade que sua rotina merece", "🍃")

    # Faixa central decorativa
    oy = H - 80
    rrect(c, 1.5*cm, oy-80, W-3*cm, 70, r=12, fill=VM)
    sf(c, DQ); c.rect(1.5*cm, oy-12, W-3*cm, 3, fill=1, stroke=0)
    sf(c, BR); c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(W/2, oy-40, "Comida de verdade, feita com ingredientes")
    c.drawCentredString(W/2, oy-57, "selecionados e muito carinho.")
    sf(c, LG); c.setFont("Helvetica", 9)
    c.drawCentredString(W/2, oy-72, "Congelada na hora certa para manter sabor, textura e nutrição.")

    # ── 3 LINHAS ──
    lines_y = H - 210
    lines = [
        ("🍲", "Linha Tradicional", "Marmitas práticas para o\ndia a dia, com tempero\ncaseiro equilibrado.", "R$ 18,00 a R$ 22,00", VM),
        ("⭐", "Linha Premium", "Receitas especiais em\nporções de 400g para\numa refeição caprichada.", "R$ 23,50 a R$ 33,50", TC),
        ("📦", "Kits Casa Celi", "Combos para organizar a\nsemana, o mês ou abastecer\na casa com economia.", "3% OFF na soma", MA),
    ]
    cw = (W - 3*cm) / 3
    lx = 1.5*cm
    for icon, name, desc, price, color in lines:
        lh = 230
        # Shadow
        sfa(c, "#888888", 0.2); c.rect(lx+3, lines_y-lh-3, cw-10, lh, fill=1, stroke=0)
        # Card
        rrect(c, lx, lines_y-lh, cw-10, lh, r=10, fill=BR)
        # Top colored band
        rrect(c, lx, lines_y-lh, cw-10, 8, r=5, fill=color)
        c.rect(lx, lines_y-lh+4, cw-10, 4, fill=1, stroke=0)
        # Icon
        sf(c, color); c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(lx+(cw-10)/2, lines_y-50, icon)
        # Name
        sf(c, PR); c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(lx+(cw-10)/2, lines_y-72, name)
        # Divider
        ss(c, CS); c.setLineWidth(0.8)
        c.line(lx+15, lines_y-80, lx+cw-25, lines_y-80)
        # Desc
        sf(c, CT); c.setFont("Helvetica", 8.5)
        for i, dl in enumerate(desc.split("\n")):
            c.drawCentredString(lx+(cw-10)/2, lines_y-96-i*13, dl)
        # Price
        price_badge(c, price, lx+(cw-10)/2-55, lines_y-lh+18, w=110, h=24)
        # Border
        ss(c, CS); c.setLineWidth(0.8); rrect(c, lx, lines_y-lh, cw-10, lh, r=10, stroke=CS)

        lx += cw

    # ── SELOS ──
    seals_y = lines_y - 270
    sf(c, VM); c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W/2, seals_y+30, "✦  Nossos Compromissos  ✦")
    ss(c, DQ); c.setLineWidth(1)
    c.line(W/2-90, seals_y+22, W/2+90, seals_y+22)

    seals = [
        ("Feito\nArtesanalmente", "Receita caseira"),
        ("Congelamento\nSeguro", "ABNT NBR"),
        ("Ingredientes\nSelecionados", "Frescos & naturais"),
        ("Sem Conservantes\nExagerados", "Fórmula limpa"),
        ("Produção\nLocal", "Apoie o local"),
        ("Pronto em\nMinutos", "Até 5 min micro"),
    ]
    sx = 1.5*cm + 30; sy = seals_y - 10
    for i, (l1, l2) in enumerate(seals):
        cx = sx + i * (W-3*cm)/6 + (W-3*cm)/12
        seal_circle(c, cx, sy, l1.replace("\n", " "), l2, r=28)

    footer(c, "2")


# ── PAGE 3: PRATOS TRADICIONAIS (1/2) ────────────────────────────────────────
def page_trad1(c, imgs):
    print("  → Linha Tradicional 1/2...")
    sf(c, PG); c.rect(0, 0, W, H, fill=1, stroke=0)
    section_header(c, "Linha Tradicional", "Tempero caseiro e equilíbrio perfeito • 300g | 400g | 500g", "🍲")

    # Tabela de tamanhos
    ty = H - 90
    sizes = [("300g", "R$ 18,00"), ("400g", "R$ 20,00"), ("500g", "R$ 22,00")]
    sw = (W - 3*cm) / 3
    sx2 = 1.5*cm
    for size, price in sizes:
        rrect(c, sx2, ty-40, sw-8, 38, r=8, fill=VM)
        sf(c, DQ); c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(sx2+(sw-8)/2, ty-15, size)
        sf(c, LG); c.setFont("Helvetica", 9)
        c.drawCentredString(sx2+(sw-8)/2, ty-30, price)
        sx2 += sw

    # Grid 2×2 de pratos (primeiros 4)
    pratos = [
        ("frango_desfiado", "Frango Desfiado",
         "Creme de milho cremoso, arroz branco soltinho e brócolis no vapor.",
         "A partir de R$ 18,00", "ALTA ACEITAÇÃO", True),
        ("frango_cubos", "Frango em Cubos Acebolado",
         "Frango macio, cebola caramelizada, arroz, feijão e misto de legumes.",
         "A partir de R$ 18,00", "EQUILIBRADO", False),
        ("frango_xadrez", "Frango Xadrez",
         "Clássico agridoce com pimentões coloridos, arroz, feijão e vagem.",
         "A partir de R$ 18,00", "SUCESSO", True),
        ("frango_mel", "Filé ao Molho de Mel",
         "Filé suculento ao mel e ervas, arroz, feijão e abobrinha grelhada.",
         "A partir de R$ 18,00", "TOQUE ESPECIAL", False),
    ]
    cw, ch = (W - 3.2*cm) / 2, 178
    gy = ty - 60
    for i, (key, nome, desc, preco, badge, champ) in enumerate(pratos):
        col, row = i % 2, i // 2
        cx = 1.5*cm + col*(cw+8)
        cy = gy - row*(ch+10) - ch
        dish_card(c, imgs.get(key), cx, cy, cw, ch, nome, desc, preco, badge, champ, TC)

    footer(c, "3")


# ── PAGE 4: PRATOS TRADICIONAIS (2/2) ────────────────────────────────────────
def page_trad2(c, imgs):
    print("  → Linha Tradicional 2/2...")
    sf(c, PG); c.rect(0, 0, W, H, fill=1, stroke=0)
    section_header(c, "Linha Tradicional", "Continue escolhendo — mais 2 opções irresistíveis", "🍲")

    # 2 cards grandes
    pratos = [
        ("merluza", "Filé de Merluza",
         "Peixe suculento, arroz branco e couve-flor gratinada dourada. Leve e nutritivo.",
         "A partir de R$ 18,00", "LEVE & NUTRITIVO", False),
        ("almondegas", "Almôndegas ao Molho",
         "Almôndegas artesanais no molho especial, arroz, feijão e mix de legumes.",
         "A partir de R$ 18,00", "CLÁSSICO", True),
    ]
    cw = W - 3*cm
    ch = 220
    cy = H - 100
    for key, nome, desc, preco, badge, champ in pratos:
        cy -= ch + 14
        dish_card(c, imgs.get(key), 1.5*cm, cy, cw, ch, nome, desc, preco, badge, champ, TC)

    # Nota de rodapé section
    ny = cy - 40
    rrect(c, 1.5*cm, ny-55, W-3*cm, 50, r=10, fill=VM)
    sf(c, DQ); c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W/2, ny-20, "✦  Todos os pratos disponíveis em 300g, 400g e 500g  ✦")
    sf(c, LG); c.setFont("Helvetica", 8.5)
    c.drawCentredString(W/2, ny-35, "Escolha o tamanho ideal para sua fome do dia  •  Peça por WhatsApp")

    footer(c, "4")


# ── PAGE 5: LINHA PREMIUM ─────────────────────────────────────────────────────
def page_premium(c, imgs):
    print("  → Linha Premium...")
    sf(c, PG); c.rect(0, 0, W, H, fill=1, stroke=0)

    # Header especial Terracota
    sf(c, TC); c.rect(0, H-56, W, 56, fill=1, stroke=0)
    sf(c, DQ); c.rect(0, H-58, W, 3, fill=1, stroke=0)
    sf(c, MA); c.rect(0, H-60, W, 2, fill=1, stroke=0)
    sf(c, BR); c.setFont("Helvetica-Bold", 22)
    c.drawString(2.2*cm, H-38, "⭐  Linha Premium")
    sf(c, "#F5D5B0"); c.setFont("Helvetica", 9)
    c.drawString(2.2*cm, H-52, "Receitas especiais em 400g  •  Para uma refeição verdadeiramente caprichada")

    pratos = [
        ("parmegiana", "Parmegiana de Frango ou Carne",
         "Queijo derretido puxando, molho de tomates frescos, arroz e batatinhas douradas.",
         "R$ 28,50", "PREMIUM ⭐", True),
        ("escondidinho", "Escondidinho Caprichado",
         "Carne, frango ou costela bovina desfiada. Cremoso, encorpado e irresistível.",
         "R$ 24,50", "FAVORITO", True),
        ("panquecas", "Panquecas Caseiras",
         "Massa fina artesanal com frango e catupiry ou presunto e queijo. Corte que revela o recheio.",
         "R$ 23,50", "ARTESANAL", False),
        ("nhoque", "Nhoque Tradicional à Bolonhesa",
         "Massa leve e macia, molho ragu encorpado de carne, ervas finas e parmesão.",
         "R$ 33,50", "CHEF ⭐", True),
        ("lasanha", "Lasanha Saborosa",
         "Camadas visíveis e generosas, molho apurado, queijo gratinado e toque artesanal.",
         "R$ 26,00", "CLÁSSICO", False),
        ("macarrao", "Macarrões da Casa",
         "Bolonhesa robusta, quatro queijos gratinado ou bechamel cremoso. Sob encomenda.",
         "R$ 24,90", "SOB ENCOMENDA", False),
    ]
    cw, ch = (W - 3.2*cm) / 2, 170
    gy = H - 82
    for i, (key, nome, desc, preco, badge, champ) in enumerate(pratos):
        col, row = i % 2, i // 2
        cx = 1.5*cm + col*(cw+8)
        cy = gy - row*(ch+10) - ch
        dish_card(c, imgs.get(key), cx, cy, cw, ch, nome, desc, preco, badge, champ, TC)

    footer(c, "5")


# ── PAGE 6: KITS ──────────────────────────────────────────────────────────────
def page_kits(c):
    print("  → Kits & Como Pedir...")
    sf(c, PG); c.rect(0, 0, W, H, fill=1, stroke=0)
    section_header(c, "Kits Casa Celi", "Combos para organizar a rotina com praticidade e economia  •  3% OFF em todos", "📦")

    kits = [
        ("🥗", "Kit Semana\nLeve", "10 marmitas", "Para organizar a\nrotina semanal\ncom praticidade.",
         "3% OFF no\ntotal", VM, "SEMANAL"),
        ("👨‍👩‍👧‍👦", "Kit Família\nPrática", "20 marmitas",
         "Almoço e jantar\nsem preocupação\npara a família.",
         "3% OFF no\ntotal", TC, "FAMÍLIA"),
        ("📦", "Kit Mês\nOrganizado", "30 marmitas",
         "Abastece a casa\ncom o melhor\ncusto-benefício.",
         "3% OFF no\ntotal + MELHOR\nOPÇÃO", MA, "ECONOMIA"),
    ]
    cw = (W - 3.2*cm) / 3 + 2
    kx = 1.5*cm
    ky = H - 100
    kh = 230
    for icon, name, qtd, desc, off, color, badge in kits:
        # Shadow
        sfa(c, "#AAAAAA", 0.25); c.rect(kx+3, ky-kh-3, cw-8, kh, fill=1, stroke=0)
        # Card bg
        rrect(c, kx, ky-kh, cw-8, kh, r=12, fill=BR)
        # Top colored band
        rrect(c, kx, ky-kh, cw-8, kh//3, r=10, fill=color)
        c.rect(kx, ky-kh+10, cw-8, kh//3-10, fill=1, stroke=0)
        # Badge no topo
        bw, bh = 68, 16
        rrect(c, kx+(cw-8)/2-bw/2, ky-18, bw, bh, r=6, fill=DQ)
        sf(c, MA); c.setFont("Helvetica-Bold", 6)
        c.drawCentredString(kx+(cw-8)/2, ky-18+5, badge)
        # Icon
        sf(c, BR); c.setFont("Helvetica-Bold", 34)
        c.drawCentredString(kx+(cw-8)/2, ky-kh+kh//3-22, icon)
        # Name
        sf(c, BR); c.setFont("Helvetica-Bold", 12)
        for j, nl in enumerate(name.split("\n")):
            c.drawCentredString(kx+(cw-8)/2, ky-kh+kh//3-42-j*14, nl)
        # Qtd
        sf(c, DQ); c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(kx+(cw-8)/2, ky-kh+kh//3+8, qtd)
        # Desc
        sf(c, CT); c.setFont("Helvetica", 8)
        desc_y = ky-kh+kh//3-62
        for j, dl in enumerate(desc.split("\n")):
            c.drawCentredString(kx+(cw-8)/2, desc_y-j*12, dl)
        # OFF badge
        rrect(c, kx+(cw-8)/2-50, ky-kh+18, 100, 36, r=8, fill=DQ)
        sf(c, MA); c.setFont("Helvetica-Bold", 8)
        off_lines = off.split("\n")
        for j, ol in enumerate(off_lines):
            c.drawCentredString(kx+(cw-8)/2, ky-kh+38-j*12, ol)
        # Border
        ss(c, DQ); c.setLineWidth(1)
        rrect(c, kx, ky-kh, cw-8, kh, r=12, stroke=DQ)
        kx += cw + 2

    # Caldo artesanal
    ca_y = ky - kh - 25
    rrect(c, 1.5*cm, ca_y-50, W-3*cm, 46, r=10, fill=VO)
    ss(c, DQ); c.setLineWidth(1.5); rrect(c, 1.5*cm, ca_y-50, W-3*cm, 46, r=10, stroke=DQ)
    sf(c, MA); c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W/2, ca_y-18, "🍲  CALDOS ARTESANAIS  •  500ml  •  R$ 21,90")
    sf(c, PR); c.setFont("Helvetica", 9)
    c.drawCentredString(W/2, ca_y-33, "Opções quentinhas e confortáveis para completar o pedido.")

    # ── COMO PEDIR ──
    steps_title_y = ca_y - 72
    sf(c, VM); c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(W/2, steps_title_y, "Como Fazer seu Pedido")
    ss(c, DQ); c.setLineWidth(1)
    c.line(W/2-100, steps_title_y-8, W/2+100, steps_title_y-8)

    steps = [
        ("1", "Escolha", "Selecione a linha,\nos pratos e tamanho.", VM),
        ("2", "Envie", "Mande lista pelo\nWhatsApp.", TC),
        ("3", "Combine", "Finalize pagamento\ne entrega.", MA),
    ]
    sw = (W-3.2*cm)/3 + 2
    sx = 1.5*cm
    sy = steps_title_y - 25
    sh = 100
    for num, titulo, desc, color in steps:
        rrect(c, sx, sy-sh, sw-8, sh, r=10, fill=BR)
        rrect(c, sx, sy-sh, sw-8, sh, r=10, stroke=CS, lw=0.8)
        # Number circle
        sf(c, color); c.circle(sx+(sw-8)/2, sy-22, 18, fill=1, stroke=0)
        sf(c, BR); c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(sx+(sw-8)/2, sy-27, num)
        # Title
        sf(c, PR); c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(sx+(sw-8)/2, sy-50, titulo)
        # Desc
        sf(c, CT); c.setFont("Helvetica", 8)
        for j, dl in enumerate(desc.split("\n")):
            c.drawCentredString(sx+(sw-8)/2, sy-64-j*11, dl)
        sx += sw + 2

    # Linha connect steps
    ss(c, CS); c.setLineWidth(1.5)
    step1_cx = 1.5*cm + (W-3.2*cm)/3/2 + 18
    step3_cx = W - 1.5*cm - 4 - (W-3.2*cm)/3/2
    c.line(step1_cx, sy-22, step3_cx, sy-22)

    footer(c, "6")


# ── PAGE 7: CTA FINAL ────────────────────────────────────────────────────────
def page_cta(c, imgs, qr_buf):
    print("  → CTA Final...")
    # Hero BG
    if "cta" in imgs:
        buf = imgs["cta"]; buf.seek(0)
        dark = darken_image_bottom(buf, 0.85)
        img_rect(c, dark, 0, 0, W, H)
    overlay(c, 0, 0, W, H, "#050F06", alpha=0.5)

    # Top badge
    rrect(c, W/2-110, H-70, 220, 26, r=13, fill=DQ)
    sf(c, MA); c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(W/2, H-70+9, "✦  FINALIZE SEU PEDIDO AGORA  ✦")

    # Main headline
    sf(c, BR); c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(W/2, H-130, "Seu almoço da semana")
    sf(c, DQ); c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(W/2, H-164, "começa aqui.")
    sf(c, BR); c.rect(W/2-80, H-175, 160, 2, fill=1, stroke=0)

    sf(c, LG); c.setFont("Helvetica", 10.5)
    c.drawCentredString(W/2, H-195, "Escolha seus pratos, envie a quantidade e combine a entrega.")
    c.drawCentredString(W/2, H-210, "Rápido, simples e sem complicação.")

    # ── QR CODE + CTA BOX ──
    mid_y = H/2 - 20
    qr_size = 140
    box_w = W - 3*cm
    box_h = 230
    box_x = 1.5*cm
    box_y = mid_y - box_h/2 - 20
    rrect(c, box_x, box_y, box_w, box_h, r=16, fill=VM)
    ss(c, DQ); c.setLineWidth(2)
    rrect(c, box_x, box_y, box_w, box_h, r=16, stroke=DQ)
    sf(c, TC); c.rect(box_x, box_y+box_h-3, box_w, 3, fill=1, stroke=0)
    c.rect(box_x, box_y, box_w, 3, fill=1, stroke=0)

    # QR Code
    if qr_buf:
        qr_buf.seek(0)
        qr_x = box_x + 22
        qr_y = box_y + (box_h-qr_size)/2
        img_rect(c, qr_buf, qr_x, qr_y, qr_size, qr_size)
        # Frame QR
        ss(c, DQ); c.setLineWidth(2)
        c.rect(qr_x-3, qr_y-3, qr_size+6, qr_size+6, fill=0, stroke=1)
        sf(c, LG); c.setFont("Helvetica", 7)
        c.drawCentredString(qr_x+qr_size/2, qr_y-13, "Aponte a câmera para pedir")

    # Text do CTA
    tx = box_x + qr_size + 48
    tw = box_w - qr_size - 72
    ty2 = box_y + box_h - 32

    sf(c, DQ); c.setFont("Helvetica-Bold", 16)
    c.drawString(tx, ty2, "Chame pelo WhatsApp!")
    ty2 -= 24

    rrect(c, tx, ty2-20, tw, 22, r=8, fill=TC)
    sf(c, BR); c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(tx+tw/2, ty2-13, "📲  FAZER PEDIDO AGORA")
    ty2 -= 38

    sf(c, LG); c.setFont("Helvetica", 9)
    c.drawString(tx, ty2, "Pagamentos aceitos:")
    ty2 -= 16

    payments = ["⚡ PIX", "💳 Cartão de Crédito", "💳 Débito", "💵 Dinheiro"]
    for pay in payments:
        rrect(c, tx, ty2-16, tw, 16, r=5, fill="#2A5E32")
        sf(c, LG); c.setFont("Helvetica-Bold", 8)
        c.drawString(tx+8, ty2-10, pay)
        ty2 -= 22

    # ── TAGLINE FINAL ──
    final_y = box_y - 40
    sf(c, DQ); c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W/2, final_y, "Casa Celi")
    sf(c, LG); c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(W/2, final_y-16, '"Comida feita hoje para facilitar o seu amanhã."')

    # Payment icons row
    icons = ["⚡PIX", "💳 Crédito", "💳 Débito", "💵 Dinheiro"]
    ix = (W - len(icons)*82) / 2
    iy = final_y - 50
    for icon in icons:
        rrect(c, ix, iy-18, 76, 18, r=7, fill=VM)
        sf(c, DQ); c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(ix+38, iy-11, icon)
        ix += 82

    footer(c, "7")


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    out_tmp = "/tmp/casaceli_premium_raw.pdf"
    out_final = "/home/user/belle-petit-pet-saloon/CasaCeli_Cardapio_GourmetPremium.pdf"
    whatsapp_url = "https://wa.me/5511999999999?text=Ol%C3%A1%2C+quero+fazer+um+pedido+Casa+Celi!"

    print("📥 Baixando imagens...")
    imgs = {}
    for key in PHOTOS:
        imgs[key] = download_img(key, 900, 600)

    print("📱 Gerando QR Code...")
    qr_buf = make_qr(whatsapp_url)

    print("🎨 Montando PDF...")
    c = pdfcanvas.Canvas(out_tmp, pagesize=A4)
    c.setTitle("Cardápio Gourmet Premium — Casa Celi Congelados Artesanais")
    c.setAuthor("Casa Celi")
    c.setSubject("Catálogo de Marmitas Artesanais Premium")
    c.setCreator("Casa Celi Design Studio")

    page_cover(c, imgs);    c.showPage()
    page_intro(c);          c.showPage()
    page_trad1(c, imgs);    c.showPage()
    page_trad2(c, imgs);    c.showPage()
    page_premium(c, imgs);  c.showPage()
    page_kits(c);           c.showPage()
    page_cta(c, imgs, qr_buf)
    c.save()
    print(f"  ✓ PDF base salvo: {out_tmp}")

    print("🔗 Adicionando interatividade (links, bookmarks)...")
    doc = fitz.open(out_tmp)

    # ── BOOKMARKS (outline) ──
    toc = [
        [1, "🏠 Início", 1],
        [1, "🍃 Nossa Proposta & Selos", 2],
        [1, "🍲 Linha Tradicional — Parte 1", 3],
        [1, "🍲 Linha Tradicional — Parte 2", 4],
        [1, "⭐ Linha Premium", 5],
        [1, "📦 Kits & Como Pedir", 6],
        [1, "📲 Fazer Pedido — WhatsApp", 7],
    ]
    doc.set_toc(toc)

    # ── LINKS WhatsApp ──
    # Página CTA (índice 6): botão "FAZER PEDIDO AGORA"
    page6 = doc[6]
    # Posição aproximada do botão CTA (em pontos PDF: y invertido)
    # Botão está em torno de H/2, largura ~200pt
    btn_rect = fitz.Rect(
        1.5*cm + 140 + 48,           # tx
        H - (H/2 + 115 + 22),        # y invertido
        1.5*cm + 140 + 48 + (W-3*cm-140-72),  # tx+tw
        H - (H/2 + 115),             # y + h
    )
    page6.insert_link({"kind": fitz.LINK_URI, "from": btn_rect, "uri": whatsapp_url})

    # ── LINKS QR AREA ──
    qr_area = fitz.Rect(1.5*cm+22, H-(H/2-20+230/2)-(140), 1.5*cm+22+140, H-(H/2-20-230/2+20))
    page6.insert_link({"kind": fitz.LINK_URI, "from": qr_area, "uri": whatsapp_url})

    # ── LINKS INTERNOS: nav entre seções ──
    # Adicionar link "Voltar ao início" no rodapé de cada página interna
    for i in range(1, 7):
        pg = doc[i]
        footer_link = fitz.Rect(0, 0, W, 26)
        pg.insert_link({"kind": fitz.LINK_GOTO, "from": footer_link, "page": 0,
                         "to": fitz.Point(0, H)})

    # ── LINK: Linha Premium na página 2 ──
    intro_pg = doc[1]
    # Area aproximada do card Premium (segundo card)
    prem_area = fitz.Rect(1.5*cm + (W-3.2*cm)/3, H-350, 1.5*cm + 2*(W-3.2*cm)/3, H-130)
    intro_pg.insert_link({"kind": fitz.LINK_GOTO, "from": prem_area, "page": 4,
                            "to": fitz.Point(0, H)})

    # ── LINK: Kits na página 2 ──
    kits_area = fitz.Rect(1.5*cm + 2*(W-3.2*cm)/3, H-350, W-1.5*cm, H-130)
    intro_pg.insert_link({"kind": fitz.LINK_GOTO, "from": kits_area, "page": 5,
                            "to": fitz.Point(0, H)})

    doc.save(out_final, garbage=4, deflate=True)
    size_kb = os.path.getsize(out_final) // 1024
    print(f"\n✅ PDF FINAL: {out_final}")
    print(f"   {doc.page_count} páginas  •  {size_kb} KB")
    doc.close()


if __name__ == "__main__":
    main()
