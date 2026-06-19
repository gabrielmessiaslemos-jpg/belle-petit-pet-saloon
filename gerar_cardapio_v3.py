#!/usr/bin/env python3
"""
Cardápio Gourmet Premium — Casa Celi Congelados Artesanais
v3 — Reescrita limpa e correta
"""

import os, io, math, qrcode
from io import BytesIO
from PIL import Image, ImageFilter, ImageDraw
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fitz

W, H = A4  # 595.27 x 841.89

# ── FONTES TTF (suporte a caracteres especiais) ──────────────────────────────
FONT_R  = "LiberationSans"
FONT_B  = "LiberationSans-Bold"
FONT_I  = "LiberationSans-Italic"
FONT_BI = "LiberationSans-BoldItalic"
BASE = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont(FONT_R,  BASE + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont(FONT_B,  BASE + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont(FONT_I,  BASE + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont(FONT_BI, BASE + "LiberationSans-BoldItalic.ttf"))

# ── PALETA ───────────────────────────────────────────────────────────────────
VM  = "#1E4B26"   # Verde musgo
VO  = "#8F9C68"   # Verde oliva
TC  = "#B05216"   # Terracota
MA  = "#4F2915"   # Marrom
DQ  = "#B89A4A"   # Dourado envelhecido
PG  = "#FAF8F3"   # Pergaminho
BR  = "#FFFFFF"
PR  = "#1C1C1C"
CS  = "#E0DBD0"   # Cinza suave
CT  = "#3A3228"   # Cinza texto escuro
LG  = "#D4EDDA"   # Verde claro
AM  = "#F5C842"   # Amarelo destaque
OR  = "#D4681E"   # Laranja queimado

def rgb(h):
    h = h.lstrip("#")
    return int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255

def fill(c, h):
    c.setFillColorRGB(*rgb(h))
    c.setFillAlpha(1)

def stroke(c, h):
    c.setStrokeColorRGB(*rgb(h))

def fill_alpha(c, h, a):
    r,g,b = rgb(h)
    c.setFillColorRGB(r, g, b)
    c.setFillAlpha(a)

def reset_alpha(c):
    c.setFillAlpha(1)
    c.setStrokeAlpha(1)


# ── IMAGENS SINTÉTICAS RÁPIDAS ───────────────────────────────────────────────
PALETTES = {
    # key: (bg_hex, glow_hex, plate_hex, food_hex)
    "cover":           ("#0D1A0D", "#1E4B26", "#2D6A2D", "#B89A4A"),
    "frango_desfiado": ("#1A0800", "#8B4513", "#D4A060", "#E8C080"),
    "frango_cubos":    ("#1A0A00", "#7A3010", "#C88050", "#E0A070"),
    "frango_xadrez":   ("#0A1200", "#3A5010", "#C84020", "#FF8040"),
    "frango_mel":      ("#1A0E00", "#8B6000", "#D4A020", "#FFD060"),
    "merluza":         ("#00101A", "#1A4A6A", "#6090B0", "#A0C8D8"),
    "almondegas":      ("#150000", "#5C1A08", "#A04020", "#D08060"),
    "parmegiana":      ("#150000", "#7A2008", "#C03010", "#E87040"),
    "escondidinho":    ("#100800", "#5C3010", "#B08040", "#D4B060"),
    "panquecas":       ("#1A0E00", "#7A4A10", "#D4A060", "#F0C880"),
    "nhoque":          ("#100000", "#5C1A08", "#B03010", "#E06030"),
    "lasanha":         ("#120000", "#6A1808", "#C02808", "#E06040"),
    "macarrao":        ("#150800", "#7A3A08", "#C08020", "#E8C050"),
    "kits_bg":         ("#050F08", "#1E4B26", "#2D6A2D", "#8F9C68"),
    "cta":             ("#050F08", "#1A3A1A", "#2A5A2A", "#B89A4A"),
}

def make_img(key, w, h):
    bg, gl, pl, fd = PALETTES.get(key, ("#1A1A1A","#3A3A3A","#5A5A5A","#7A7A7A"))

    def hc(hx):
        hx = hx.lstrip("#")
        return int(hx[0:2],16), int(hx[2:4],16), int(hx[4:6],16)

    bgR,bgG,bgB = hc(bg)
    glR,glG,glB = hc(gl)
    plR,plG,plB = hc(pl)
    fdR,fdG,fdB = hc(fd)

    img = Image.new("RGB", (w, h))
    pix = img.load()

    cx, cy = w*0.5, h*0.43

    for y in range(h):
        for x in range(w):
            t = y / h
            # Base gradient
            r = int(bgR + t*(bgR//2))
            g = int(bgG + t*(bgG//2))
            b = int(bgB + t*(bgB//2))

            # Distance from center (for plate glow)
            dx = (x - cx) / (w * 0.38)
            dy = (y - cy) / (h * 0.34)
            d = math.sqrt(dx*dx + dy*dy)

            # Plate area
            if d < 1.0:
                plate_t = min(1, d)
                p_blend = max(0, 1 - plate_t)
                # Food (center) vs plate (edge)
                food_blend = max(0, 1 - d/0.55)
                r = int(r*(1-p_blend) + plR*p_blend + (fdR-plR)*food_blend*p_blend)
                g = int(g*(1-p_blend) + plG*p_blend + (fdG-plG)*food_blend*p_blend)
                b = int(b*(1-p_blend) + plB*p_blend + (fdB-plB)*food_blend*p_blend)

                # Warm highlight
                hi = max(0, 1 - d/0.3)
                r = min(255, int(r + hi*60))
                g = min(255, int(g + hi*50))
                b = min(255, int(b + hi*20))

            # Glow around plate
            glow = max(0, 1 - d/1.6) * 0.4
            r = min(255, int(r + glow*(glR-r)))
            g = min(255, int(g + glow*(glG-g)))
            b = min(255, int(b + glow*(glB-b)))

            # Bottom dark gradient (for text legibility)
            dark = max(0, (t - 0.45) / 0.55) * 0.8
            r = int(r * (1-dark))
            g = int(g * (1-dark))
            b = int(b * (1-dark))

            pix[x, y] = (max(0,min(255,r)), max(0,min(255,g)), max(0,min(255,b)))

    img = img.filter(ImageFilter.GaussianBlur(1.0))
    out = BytesIO()
    img.save(out, "JPEG", quality=88)
    out.seek(0)
    return out

def make_qr(url):
    qr = qrcode.QRCode(version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=7, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1E4B26", back_color="#FAF8F3")
    out = BytesIO()
    img.save(out, "PNG")
    out.seek(0)
    return out


# ── HELPERS DE DESENHO ────────────────────────────────────────────────────────
def rect_fill(c, x, y, w, h, col):
    fill(c, col); c.rect(x, y, w, h, fill=1, stroke=0)

def rect_stroke(c, x, y, w, h, col, lw=1):
    stroke(c, col); c.setLineWidth(lw); c.rect(x, y, w, h, fill=0, stroke=1)

def txt_c(c, s, x, y, font, size, col):
    fill(c, col); c.setFont(font, size); c.drawCentredString(x, y, s)

def txt_l(c, s, x, y, font, size, col):
    fill(c, col); c.setFont(font, size); c.drawString(x, y, s)

def txt_r(c, s, x, y, font, size, col):
    fill(c, col); c.setFont(font, size); c.drawRightString(x, y, s)

def draw_img(c, buf, x, y, w, h):
    if buf is None: return
    try:
        buf.seek(0)
        c.drawImage(ImageReader(buf), x, y, w, h, preserveAspectRatio=False)
    except: pass

def overlay_rect(c, x, y, w, h, col, a):
    c.saveState()
    fill_alpha(c, col, a)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.restoreState()
    reset_alpha(c)

def pill(c, x, y, w, h, bg, label, font=None, fsize=7, fcol=BR):
    font = font or FONT_B
    rect_fill(c, x, y, w, h, bg)
    txt_c(c, label, x+w/2, y+h/2-fsize/2+1, font, fsize, fcol)

def hline(c, x1, x2, y, col, lw=0.8):
    stroke(c, col); c.setLineWidth(lw); c.line(x1, y, x2, y)

def footer_bar(c, page_n=None):
    rect_fill(c, 0, 0, W, 26, VM)
    rect_fill(c, 0, 25, W, 2, DQ)
    txt_c(c, "Casa Celi  •  Congelados Artesanais  •  Comida feita hoje para facilitar o seu amanha.",
          W/2, 8, FONT_B, 7, DQ)
    if page_n:
        txt_r(c, str(page_n), W - 1.2*cm, 8, FONT_B, 7, VO)

def section_bar(c, title, sub=""):
    rect_fill(c, 0, H-54, W, 54, VM)
    rect_fill(c, 0, H-55, W, 2, DQ)
    rect_fill(c, 0, H-57, W, 2, TC)
    txt_l(c, title, 2*cm, H-34, FONT_B, 20, DQ)
    if sub:
        txt_l(c, sub, 2*cm, H-50, FONT_R, 8.5, VO)


# ── CARD DE PRATO ─────────────────────────────────────────────────────────────
def card_prato(c, img_buf, x, y, cw, ch, nome, desc, preco,
               badge=None, champion=False, accent=TC):
    """
    Card com imagem na metade superior, info na metade inferior.
    x, y = canto inferior esquerdo.  cw x ch = largura x altura total.
    """
    img_h = round(ch * 0.52)  # imagem ocupa 52% da altura
    txt_h = ch - img_h         # texto ocupa o resto

    # --- Sombra ---
    c.saveState()
    fill_alpha(c, "#000000", 0.15)
    c.rect(x+4, y-4, cw, ch, fill=1, stroke=0)
    c.restoreState()
    reset_alpha(c)

    # --- Imagem de fundo (area superior) ---
    rect_fill(c, x, y+txt_h, cw, img_h, "#2A2A2A")  # fallback
    draw_img(c, img_buf, x, y+txt_h, cw, img_h)

    # Gradiente escuro suave no fundo da imagem (para legibilidade)
    for band in range(6):
        band_h = img_h * 0.18
        band_y = y + txt_h
        a = 0.0 + band * 0.07
        overlay_rect(c, x, band_y + band*(band_h/6), cw, band_h, "#050A05", a)

    # Badge campeao
    if champion:
        bw, bh = 106, 17
        rect_fill(c, x + 6, y + txt_h + img_h - bh - 6, bw, bh, OR)
        txt_l(c, "* CAMPIAO DE VENDAS", x + 14, y + txt_h + img_h - bh - 6 + 5,
              FONT_B, 6.5, BR)

    # Badge de categoria
    if badge:
        bw, bh = 85, 17
        rect_fill(c, x + cw - bw - 5, y + txt_h + img_h - bh - 5, bw, bh, VM)
        rect_stroke(c, x + cw - bw - 5, y + txt_h + img_h - bh - 5, bw, bh, DQ, 0.7)
        txt_c(c, badge, x + cw - bw/2 - 5,
              y + txt_h + img_h - bh - 5 + 5, FONT_B, 6, DQ)

    # Barra de acento na base da imagem
    rect_fill(c, x, y+txt_h, cw, 4, accent)

    # --- Área de texto (inferior) ---
    rect_fill(c, x, y, cw, txt_h, VM)

    # Nome do prato
    txt_l(c, nome if len(nome)<=28 else nome[:26]+"...",
          x+10, y+txt_h-17, FONT_B, 11, BR)

    # Divisor
    hline(c, x+10, x+cw-10, y+txt_h-22, DQ, 0.7)

    # Descrição (max 2 linhas)
    fill(c, LG)
    c.setFont(FONT_R, 8)
    words = desc.split(); line = ""; dy = y+txt_h-34; nlines = 0
    for word in words:
        test = (line+" "+word).strip()
        if c.stringWidth(test, FONT_R, 8) <= cw-22: line = test
        else:
            if line:
                c.drawString(x+10, dy, line); dy -= 11; nlines += 1
                if nlines >= 2: break
            line = word
    if line and nlines < 2:
        c.drawString(x+10, dy, line)

    # Preço
    pw, ph = 108, 22
    px = x + cw - pw - 7
    py = y + 7
    rect_fill(c, px, py, pw, ph, DQ)
    rect_stroke(c, px, py, pw, ph, MA, 0.8)
    txt_c(c, preco, px + pw/2, py + ph/2 - 5, FONT_B, 10, MA)

    # Borda externa dourada
    rect_stroke(c, x, y, cw, ch, DQ, 1.1)


# ── PAGE 1: CAPA ──────────────────────────────────────────────────────────────
def pg_capa(c, imgs):
    print("  -> Capa")

    # Hero bg
    draw_img(c, imgs.get("cover"), 0, 0, W, H)
    # Overlay geral
    overlay_rect(c, 0, 0, W, H, "#030F05", 0.45)

    # Topo: badge dourado
    bw, bh = 240, 26
    rect_fill(c, W/2-bw/2, H-72, bw, bh, DQ)
    rect_fill(c, W/2-bw/2+2, H-70, bw-4, bh-4, MA)
    txt_c(c, "  CATALOGO GOURMET ARTESANAL 2025  ", W/2, H-60, FONT_B, 8, DQ)

    # Titulo principal
    txt_c(c, "MARMITAS CONGELADAS", W/2, H-122, FONT_B, 30, BR)
    txt_c(c, "COM SABOR DE COMIDA FEITA EM CASA", W/2, H-158, FONT_B, 22, BR)

    # Linha dourada
    rect_fill(c, W/2-80, H-170, 160, 2.5, DQ)

    # Subtitulo
    txt_c(c, "Produzidas artesanalmente, congeladas com segurança", W/2, H-188, FONT_R, 10.5, LG)
    txt_c(c, "e prontas para facilitar sua rotina.", W/2, H-202, FONT_R, 10.5, LG)

    # Imagem hero central (o prato sintético como vitrine)
    iw, ih = 320, 220
    draw_img(c, imgs.get("cover"), W/2-iw/2, H/2-ih/2-20, iw, ih)
    overlay_rect(c, W/2-iw/2, H/2-ih/2-20, iw, ih, "#030F05", 0.3)

    # Painel inferior da marca
    ph_panel = 155
    rect_fill(c, 0, 0, W, ph_panel, VM)
    rect_fill(c, 0, ph_panel, W, 3, DQ)
    rect_fill(c, 0, ph_panel+3, W, 2, TC)

    # Nome da marca
    txt_c(c, "Casa Celi", W/2, 112, FONT_B, 46, BR)
    txt_c(c, "C O N G E L A D O S   A R T E S A N A I S", W/2, 88, FONT_R, 10, VO)
    hline(c, W/2-90, W/2+90, 80, DQ, 0.8)
    txt_c(c, '"Comida feita hoje para facilitar o seu amanha."', W/2, 64, FONT_I, 9.5, DQ)

    # Pills
    labels = ["Artesanal", "Sem Conservantes", "Premium", "Pronto em Min."]
    total = len(labels)*115 + (len(labels)-1)*6
    px = (W-total)/2
    for lab in labels:
        pill(c, px, 34, 115, 18, VO, lab, fsize=7.5, fcol=BR)
        px += 121

    footer_bar(c, "1")


# ── PAGE 2: NOSSA PROPOSTA ────────────────────────────────────────────────────
def pg_proposta(c):
    print("  -> Nossa Proposta")
    rect_fill(c, 0, 0, W, H, PG)
    section_bar(c, "Nossa Proposta", "Qualidade artesanal com a praticidade que sua rotina merece")

    # Faixa de frase
    fy = H - 110
    rect_fill(c, 1.5*cm, fy-58, W-3*cm, 52, VM)
    txt_c(c, "Comida de verdade, feita com ingredientes selecionados e muito carinho.",
          W/2, fy-28, FONT_B, 13, BR)
    txt_c(c, "Congelada na hora certa para manter sabor, textura e nutricao.",
          W/2, fy-46, FONT_R, 9.5, LG)
    rect_fill(c, 1.5*cm, fy-60, W-3*cm, 2, DQ)

    # 3 cards de linhas — altura calculada para chegar nos selos
    card_top = fy - 80
    card_h   = 210
    cw3      = (W - 3.2*cm) / 3

    linhas = [
        (VM,  "LINHA TRADICIONAL", "Marmitas praticas para o dia\na dia com tempero caseiro\nequilibrado.",
         "R$ 18 a R$ 22", "[Tradicional]"),
        (TC,  "LINHA PREMIUM",     "Receitas especiais em porcoes\nde 400g para uma refeicao\nverdadeiramente caprichada.",
         "R$ 23,50 a R$ 33,50", "[Premium]"),
        (MA,  "KITS CASA CELI",    "Combos para organizar a\nsemana, o mes ou abastecer\na casa com economia.",
         "3% OFF na soma", "[Kits]"),
    ]
    lx = 1.5*cm
    for col, title, desc, price, icon in linhas:
        # Sombra
        c.saveState(); fill_alpha(c, "#AAAAAA", 0.25)
        c.rect(lx+3, card_top-card_h-3, cw3-8, card_h, fill=1, stroke=0)
        c.restoreState(); reset_alpha(c)

        # Card bg
        rect_fill(c, lx, card_top-card_h, cw3-8, card_h, BR)
        # Topo colorido
        rect_fill(c, lx, card_top-38, cw3-8, 38, col)

        # Badge no topo
        bw2, bh2 = 70, 16
        rect_fill(c, lx+(cw3-8)/2-bw2/2, card_top-bh2-8, bw2, bh2, DQ)
        txt_c(c, title.split()[1], lx+(cw3-8)/2, card_top-bh2-8+5, FONT_B, 5.5, MA)

        # Icone / titulo
        txt_c(c, icon, lx+(cw3-8)/2, card_top-28, FONT_B, 11, BR)

        # Divisor
        hline(c, lx+12, lx+cw3-20, card_top-card_h+65, CS, 0.8)

        # Descricao
        fill(c, CT); c.setFont(FONT_R, 8)
        for i, dl in enumerate(desc.split("\n")):
            c.drawCentredString(lx+(cw3-8)/2, card_top-card_h+60-i*12, dl)

        # Preço
        pw2, ph2 = 110, 22
        rect_fill(c, lx+(cw3-8)/2-pw2/2, card_top-card_h+14, pw2, ph2, DQ)
        txt_c(c, price, lx+(cw3-8)/2, card_top-card_h+14+7, FONT_B, 9, MA)

        # Título inline
        txt_c(c, title, lx+(cw3-8)/2, card_top-card_h+70+20, FONT_B, 9.5, PR)

        # Borda
        rect_stroke(c, lx, card_top-card_h, cw3-8, card_h, CS, 0.8)
        lx += cw3

    # Selos de qualidade
    sy = card_top - card_h - 40
    txt_c(c, "Nossos Compromissos com Voce", W/2, sy, FONT_B, 12, VM)
    hline(c, W/2-120, W/2+120, sy-8, DQ, 1)

    seals = [
        ("Feito", "Artesanalmente"),
        ("Congelamento", "Seguro"),
        ("Ingredientes", "Selecionados"),
        ("Sem Conservantes", "Exagerados"),
        ("Producao", "Local"),
        ("Pronto em", "Minutos"),
    ]
    # Selos dispostos em 2 linhas de 3 para mais impacto visual
    seg_w = (W - 3*cm) / 3
    for i, (l1, l2) in enumerate(seals):
        row = i // 3
        col = i % 3
        cx2 = 1.5*cm + col*seg_w + seg_w/2
        cy2 = sy - 50 - row*68

        c.saveState()
        fill(c, DQ); c.circle(cx2, cy2, 26, fill=1, stroke=0)
        stroke(c, MA); c.setLineWidth(1.2); c.circle(cx2, cy2, 23, fill=0, stroke=1)
        c.restoreState(); reset_alpha(c)

        txt_c(c, l1, cx2, cy2+5, FONT_B, 5.5, MA)
        txt_c(c, l2, cx2, cy2-5, FONT_R, 5, MA)

    # Faixa de fecho da página
    close_y = sy - 50 - 68 - 34
    rect_fill(c, 1.5*cm, close_y - 42, W-3*cm, 38, VM)
    txt_c(c, "Qualidade artesanal desde o preparo ate a sua mesa.",
          W/2, close_y - 22, FONT_B, 11, DQ)
    txt_c(c, "Escolha sua linha, monte seu kit e peca pelo WhatsApp.",
          W/2, close_y - 36, FONT_R, 9, LG)

    footer_bar(c, "2")


# ── PAGE 3: TRADICIONAL 1/2 ──────────────────────────────────────────────────
def pg_trad1(c, imgs):
    print("  -> Tradicional 1/2")
    rect_fill(c, 0, 0, W, H, PG)
    section_bar(c, "Linha Tradicional", "Tempero caseiro e equilibrio perfeito  |  300g / 400g / 500g")

    # Tabela de tamanhos
    tabx = 1.5*cm; taby = H - 82; tabw = (W-3*cm)/3
    for size, price in [("300g","R$ 18,00"),("400g","R$ 20,00"),("500g","R$ 22,00")]:
        rect_fill(c, tabx, taby-36, tabw-8, 34, VM)
        rect_stroke(c, tabx, taby-36, tabw-8, 34, DQ, 0.8)
        txt_c(c, size,  tabx+(tabw-8)/2, taby-17, FONT_B, 14, DQ)
        txt_c(c, price, tabx+(tabw-8)/2, taby-30, FONT_R, 8.5, LG)
        tabx += tabw

    # 4 cards em grid 2×2 — altura calculada para preencher a página
    pratos = [
        ("frango_desfiado", "Frango Desfiado",
         "Creme de milho cremoso, arroz branco soltinho e brocolis no vapor.",
         "A partir de R$ 18,00", "ALTA ACEITACAO", True),
        ("frango_cubos", "Frango em Cubos Acebolado",
         "Frango macio, cebola caramelizada, arroz, feijao e mix de legumes.",
         "A partir de R$ 18,00", "EQUILIBRADO", False),
        ("frango_xadrez", "Frango Xadrez",
         "Classico agridoce com pimentoes coloridos, arroz, feijao e vagem.",
         "A partir de R$ 18,00", "SUCESSO", True),
        ("frango_mel", "File ao Molho de Mel",
         "File suculento ao mel e ervas, arroz, feijao e abobrinha grelhada.",
         "A partir de R$ 18,00", "TOQUE ESPECIAL", False),
    ]

    cw      = (W - 3.2*cm) / 2
    gutter  = 10
    # Preenche do footer até logo abaixo da tabela de tamanhos
    avail   = (taby - 42) - (26 + 6)   # de 32pt acima do footer até abaixo da tabela
    ch      = (avail - gutter) / 2      # 2 linhas
    top_ref = taby - 42                 # y topo do grid

    for i, (key, nome, desc, preco, badge, champ) in enumerate(pratos):
        col = i % 2
        row = i // 2
        cx = 1.5*cm + col*(cw+gutter)
        cy = top_ref - (row+1)*ch - row*gutter
        card_prato(c, imgs.get(key), cx, cy, cw, ch, nome, desc, preco, badge, champ)

    footer_bar(c, "3")


# ── PAGE 4: TRADICIONAL 2/2 ──────────────────────────────────────────────────
def pg_trad2(c, imgs):
    print("  -> Tradicional 2/2")
    rect_fill(c, 0, 0, W, H, PG)
    section_bar(c, "Linha Tradicional", "Mais opcoes — todas feitas com ingredientes selecionados")

    pratos = [
        ("merluza", "File de Merluza",
         "Peixe suculento, arroz branco e couve-flor gratinada dourada. Leve e nutritivo.",
         "A partir de R$ 18,00", "LEVE E NUTRITIVO", False),
        ("almondegas", "Almondegas ao Molho",
         "Almondegas artesanais no molho especial, arroz, feijao e mix de legumes.",
         "A partir de R$ 18,00", "CLASSICO", True),
    ]

    gutter  = 14
    cw_full = W - 3*cm
    nota_h  = 46
    avail   = (H - 72) - (26 + 6 + nota_h + gutter)
    ch      = (avail - gutter) / 2
    top     = H - 72

    for i, (key, nome, desc, preco, badge, champ) in enumerate(pratos):
        cy = top - (i+1)*ch - i*gutter
        card_prato(c, imgs.get(key), 1.5*cm, cy, cw_full, ch, nome, desc, preco, badge, champ)

    ny = top - 2*ch - gutter - gutter
    rect_fill(c, 1.5*cm, ny-nota_h, W-3*cm, nota_h, VM)
    rect_fill(c, 1.5*cm, ny-2, W-3*cm, 2, DQ)
    txt_c(c, "Todos os pratos disponiveis em 300g, 400g e 500g",
          W/2, ny-22, FONT_B, 11, DQ)
    txt_c(c, "Escolha o tamanho ideal  •  Peca pelo WhatsApp",
          W/2, ny-36, FONT_R, 8.5, LG)

    footer_bar(c, "4")


# ── PAGE 5: LINHA PREMIUM ─────────────────────────────────────────────────────
def pg_premium(c, imgs):
    print("  -> Linha Premium")
    rect_fill(c, 0, 0, W, H, PG)

    # Header especial terracota
    rect_fill(c, 0, H-54, W, 54, TC)
    rect_fill(c, 0, H-55, W, 2, DQ)
    rect_fill(c, 0, H-57, W, 2, MA)
    txt_l(c, "Linha Premium", 2*cm, H-34, FONT_B, 22, DQ)
    txt_l(c, "Receitas especiais em 400g  |  Para uma refeicao verdadeiramente caprichada",
          2*cm, H-50, FONT_R, 8.5, "#F5D5B0")

    pratos = [
        ("parmegiana",   "Parmegiana de Frango ou Carne",
         "Queijo derretido puxando, molho de tomates frescos, arroz e batatinhas douradas.",
         "R$ 28,50", "PREMIUM", True),
        ("escondidinho", "Escondidinho Caprichado",
         "Carne, frango ou costela bovina desfiada. Cremoso, encorpado e irresistivel.",
         "R$ 24,50", "FAVORITO", True),
        ("panquecas",    "Panquecas Caseiras",
         "Massa fina artesanal com frango e catupiry ou presunto e queijo.",
         "R$ 23,50", "ARTESANAL", False),
        ("nhoque",       "Nhoque a Bolonhesa",
         "Massa leve e macia, molho ragu encorpado de carne, ervas finas e parmesao.",
         "R$ 33,50", "CHEF ESPECIAL", True),
        ("lasanha",      "Lasanha Saborosa",
         "Camadas generosas, molho apurado, queijo gratinado e toque artesanal da casa.",
         "R$ 26,00", "CLASSICO", False),
        ("macarrao",     "Macarroes da Casa",
         "Bolonhesa robusta, quatro queijos gratinado ou bechamel cremoso. Sob encomenda.",
         "R$ 24,90", "SOB ENCOMENDA", False),
    ]

    cw      = (W - 3.2*cm) / 2
    gutter  = 8
    avail   = (H - 68) - (26 + 6)
    ch      = (avail - 2*gutter) / 3   # 3 linhas
    top     = H - 68

    for i, (key, nome, desc, preco, badge, champ) in enumerate(pratos):
        col = i % 2
        row = i // 2
        cx  = 1.5*cm + col*(cw+gutter)
        cy  = top - (row+1)*ch - row*gutter
        card_prato(c, imgs.get(key), cx, cy, cw, ch, nome, desc, preco, badge, champ, accent=TC)

    footer_bar(c, "5")


# ── PAGE 6: KITS + COMO PEDIR ────────────────────────────────────────────────
def pg_kits(c):
    print("  -> Kits & Como Pedir")
    rect_fill(c, 0, 0, W, H, PG)
    section_bar(c, "Kits Casa Celi", "Combos para organizar a rotina com praticidade e economia  |  3% OFF em todos")

    kh   = 230   # altura dos kit cards
    ca_h = 44
    st_h = 148   # altura dos step cards

    ktop = H - 68    # topo do card de kit (y topo)
    kw   = (W - 3.2*cm) / 3
    kx   = 1.5*cm

    kits = [
        (VM,  "Kit Semana Leve",     "10 marmitas",
         ["Para organizar a rotina", "semanal com praticidade."], "SEMANAL"),
        (TC,  "Kit Familia Pratica", "20 marmitas",
         ["Almoco e jantar sem", "preocupacao para a familia."], "FAMILIA"),
        (MA,  "Kit Mes Organizado",  "30 marmitas",
         ["Abastece a casa com o", "melhor custo-beneficio."], "ECONOMIA"),
    ]

    for col, title, qtd, desc, badge in kits:
        cb = ktop - kh   # bottom do card
        ct = ktop        # top do card
        cw2 = kw - 8

        # Sombra
        c.saveState(); fill_alpha(c, "#AAAAAA", 0.22)
        c.rect(kx+3, cb-3, cw2, kh, fill=1, stroke=0)
        c.restoreState(); reset_alpha(c)

        # Fundo branco
        rect_fill(c, kx, cb, cw2, kh, BR)
        # TOPO colorido (banda superior)
        band_h = int(kh * 0.38)
        rect_fill(c, kx, ct - band_h, cw2, band_h, col)

        # Badge tipo (no topo da faixa colorida)
        bw2, bh2 = 70, 17
        rect_fill(c, kx + cw2/2 - bw2/2, ct - bh2 - 6, bw2, bh2, DQ)
        txt_c(c, badge, kx + cw2/2, ct - bh2 - 6 + 6, FONT_B, 6.5, MA)

        # Quantidade
        txt_c(c, qtd, kx + cw2/2, ct - band_h + 36, FONT_B, 16, DQ)
        # Titulo
        txt_c(c, title, kx + cw2/2, ct - band_h + 18, FONT_B, 11, BR)

        # Divisor
        hline(c, kx+14, kx+cw2-14, ct - band_h - 2, CS, 0.7)

        # Descricao
        for j, dl in enumerate(desc):
            txt_c(c, dl, kx + cw2/2, ct - band_h - 18 - j*13, FONT_R, 8.5, CT)

        # Bullets de benefícios
        bullets = ["Marmitas variadas", "Congele ate 3 meses", "Pede 1x, come varias"]
        for j, b in enumerate(bullets):
            bly = ct - band_h - 50 - j*15
            # bolinha
            fill(c, VO); c.circle(kx + 18, bly + 4, 4, fill=1, stroke=0)
            txt_l(c, b, kx + 28, bly, FONT_R, 8, CT)

        # OFF badge (base do card)
        ow, oh = 100, 28
        rect_fill(c, kx + cw2/2 - ow/2, cb + 10, ow, oh, DQ)
        txt_c(c, "3% OFF no total", kx + cw2/2, cb + 10 + 9, FONT_B, 9, MA)

        # Borda dourada
        rect_stroke(c, kx, cb, cw2, kh, DQ, 1)
        kx += kw

    # Caldos artesanais
    ca_y = ktop - kh - 14   # top do banner caldos
    rect_fill(c, 1.5*cm, ca_y - ca_h, W-3*cm, ca_h, "#D4EDDA")
    rect_stroke(c, 1.5*cm, ca_y - ca_h, W-3*cm, ca_h, VO, 1.5)
    txt_c(c, "CALDOS ARTESANAIS  |  500ml  |  R$ 21,90",
          W/2, ca_y - ca_h + 26, FONT_B, 12, VM)
    txt_c(c, "Opcoes quentinhas e confortaveis para completar o pedido.",
          W/2, ca_y - ca_h + 12, FONT_R, 8.5, CT)

    # Como Pedir — título
    stt_y = ca_y - ca_h - 14   # y do título "Como Fazer seu Pedido"
    txt_c(c, "Como Fazer seu Pedido", W/2, stt_y - 16, FONT_B, 14, VM)
    hline(c, W/2-120, W/2+120, stt_y - 24, DQ, 1)

    # Steps
    steps = [
        (VM, "1", "Escolha",  ["Selecione a linha, os", "pratos e o tamanho."]),
        (TC, "2", "Envie",    ["Mande a lista pelo", "WhatsApp."]),
        (MA, "3", "Combine",  ["Finalize pagamento", "e entrega."]),
    ]
    sw  = (W - 3.2*cm) / 3
    sx  = 1.5*cm
    sbt = stt_y - 32           # top dos steps
    sb  = sbt - st_h           # bottom dos steps

    for scol, num, titulo, desc in steps:
        cw2 = sw - 8
        # Sombra
        c.saveState(); fill_alpha(c, "#AAAAAA", 0.18)
        c.rect(sx+3, sb-3, cw2, st_h, fill=1, stroke=0)
        c.restoreState(); reset_alpha(c)

        # Fundo branco
        rect_fill(c, sx, sb, cw2, st_h, BR)
        # Faixa colorida no TOPO do step card
        faixa_h = int(st_h * 0.32)
        rect_fill(c, sx, sbt - faixa_h, cw2, faixa_h, scol)

        # Número (dentro da faixa colorida, no topo)
        txt_c(c, num, sx + cw2/2, sbt - faixa_h/2 - 10, FONT_B, 22, BR)

        # Título (abaixo da faixa)
        txt_c(c, titulo, sx + cw2/2, sbt - faixa_h - 18, FONT_B, 13, PR)

        # Divisor
        hline(c, sx+14, sx+cw2-14, sbt - faixa_h - 24, CS, 0.7)

        # Descrição
        for j, dl in enumerate(desc):
            txt_c(c, dl, sx + cw2/2, sbt - faixa_h - 36 - j*13, FONT_R, 8.5, CT)

        # Detalhe extra (tempo / ação)
        extras = {
            "Escolha": ["Linha Tradicional ou Premium", "300g, 400g ou 500g"],
            "Envie":   ["Lista de pratos e quantidades", "Confirmamos disponibilidade"],
            "Combine": ["PIX, cartao ou dinheiro", "Retirada ou entrega combinada"],
        }
        det_list = extras.get(titulo, [])
        for j, d in enumerate(det_list):
            fill(c, VO); c.circle(sx + cw2/2 - 55, sbt - faixa_h - 65 - j*14 + 4, 3, fill=1, stroke=0)
            txt_l(c, d, sx + cw2/2 - 48, sbt - faixa_h - 65 - j*14, FONT_R, 7.5, CT)

        rect_stroke(c, sx, sb, cw2, st_h, CS, 0.8)
        sx += sw

    # Faixa de fechamento no rodapé da página
    close_y = sb - 12
    rect_fill(c, 1.5*cm, close_y - 36, W-3*cm, 32, VM)
    txt_c(c, "Qualidade em cada marmita  •  Feito com carinho  •  Pede agora pelo WhatsApp",
          W/2, close_y - 20, FONT_B, 9, DQ)

    footer_bar(c, "6")


# ── PAGE 7: CTA FINAL ────────────────────────────────────────────────────────
def pg_cta(c, imgs, qr_buf):
    print("  -> CTA Final")

    # BG hero
    draw_img(c, imgs.get("cta"), 0, 0, W, H)
    overlay_rect(c, 0, 0, W, H, "#030F05", 0.60)

    # Top badge
    bw, bh = 230, 26
    rect_fill(c, W/2-bw/2, H-72, bw, bh, DQ)
    txt_c(c, "FINALIZE SEU PEDIDO AGORA", W/2, H-61, FONT_B, 9, MA)

    # Headline
    txt_c(c, "Seu almoco da semana", W/2, H-118, FONT_B, 28, BR)
    txt_c(c, "comeca aqui.", W/2, H-150, FONT_B, 28, DQ)
    rect_fill(c, W/2-80, H-160, 160, 2.5, DQ)

    txt_c(c, "Escolha seus pratos, envie a quantidade e combine a entrega.",
          W/2, H-178, FONT_R, 10, LG)

    # --- BOX CENTRAL --- posicionado para cobrir a página com conteúdo
    box_w = W - 3*cm
    box_h = 240
    box_x = 1.5*cm
    box_y = H - 450

    rect_fill(c, box_x, box_y, box_w, box_h, VM)
    rect_stroke(c, box_x, box_y, box_w, box_h, DQ, 2)
    rect_fill(c, box_x, box_y+box_h-3, box_w, 3, TC)
    rect_fill(c, box_x, box_y, box_w, 3, TC)

    # QR Code
    qr_s = 128
    qr_x = box_x + 20
    qr_y = box_y + (box_h-qr_s)/2
    rect_fill(c, qr_x-4, qr_y-4, qr_s+8, qr_s+8, PG)
    draw_img(c, qr_buf, qr_x, qr_y, qr_s, qr_s)
    rect_stroke(c, qr_x-4, qr_y-4, qr_s+8, qr_s+8, DQ, 1.5)
    txt_c(c, "Aponte a camera para pedir", qr_x+qr_s/2, qr_y-14, FONT_R, 7, LG)

    # Texto CTA
    tx  = box_x + qr_s + 44
    tw  = box_w - qr_s - 66
    ty2 = box_y + box_h - 26

    txt_l(c, "Chame pelo WhatsApp!", tx, ty2, FONT_B, 16, DQ)
    ty2 -= 28

    rect_fill(c, tx, ty2-20, tw, 22, TC)
    txt_c(c, "FAZER PEDIDO AGORA", tx+tw/2, ty2-13, FONT_B, 11, BR)
    ty2 -= 36

    txt_l(c, "Formas de pagamento:", tx, ty2, FONT_B, 9, LG)
    ty2 -= 14

    for pay in ["PIX", "Cartao de Credito", "Cartao de Debito", "Dinheiro"]:
        rect_fill(c, tx, ty2-16, tw, 16, "#2A5E32")
        txt_l(c, "  " + pay, tx+6, ty2-11, FONT_B, 8.5, LG)
        ty2 -= 22

    # Tagline final
    final_y = box_y - 48
    # Linha decorativa
    rect_fill(c, W/2-100, final_y+4, 200, 2, DQ)
    txt_c(c, "Casa Celi", W/2, final_y - 14, FONT_B, 22, DQ)
    txt_c(c, '"Comida feita hoje para facilitar o seu amanha."',
          W/2, final_y - 30, FONT_I, 10, LG)
    rect_fill(c, W/2-100, final_y - 38, 200, 2, DQ)

    # Selos de pagamento
    pays = ["PIX", "Cartao Credito", "Cartao Debito", "Dinheiro"]
    pw_each = 108
    total_w = len(pays)*pw_each + (len(pays)-1)*8
    px = (W-total_w)/2
    py = final_y - 72
    for p in pays:
        rect_fill(c, px, py, pw_each, 28, VM)
        rect_stroke(c, px, py, pw_each, 28, DQ, 0.9)
        txt_c(c, p, px+pw_each/2, py+10, FONT_B, 8, DQ)
        px += pw_each + 8

    # Frase de urgência
    txt_c(c, "Peca agora e receba sua semana organizada!",
          W/2, py - 22, FONT_B, 10, LG)

    # Seção decorativa de fecho (fundo escuro é intencional — preenchemos com branding)
    bottom_y = py - 52
    # Linha ornamental
    hline(c, 1.5*cm, W-1.5*cm, bottom_y, DQ, 0.6)
    txt_c(c, "C A S A   C E L I",
          W/2, bottom_y - 18, FONT_B, 10, VO)
    txt_c(c, "Congelados Artesanais  •  Producao Local  •  Sem Conservantes Exagerados",
          W/2, bottom_y - 34, FONT_R, 8, "#6A8F70")
    hline(c, 1.5*cm, W-1.5*cm, bottom_y - 44, DQ, 0.6)

    # Proposta de valores no rodapé escuro
    valores = ["Artesanal", "Caseiro", "Nutritivo", "Pratico", "Premium", "Local"]
    seg = (W - 3*cm) / len(valores)
    for i, v in enumerate(valores):
        vx = 1.5*cm + i*seg + seg/2
        fill(c, "#2A5E32"); c.circle(vx, bottom_y - 68, 18, fill=1, stroke=0)
        txt_c(c, v, vx, bottom_y - 73, FONT_B, 6, DQ)

    footer_bar(c, "7")


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    out_raw   = "/tmp/casaceli_v3_raw.pdf"
    out_final = "/home/user/belle-petit-pet-saloon/CasaCeli_Cardapio_GourmetPremium.pdf"
    wa_url    = "https://wa.me/5511999999999?text=Ola%2C+quero+fazer+um+pedido+Casa+Celi%21"

    print("Gerando imagens sinteticas...")
    imgs = {}
    for key in PALETTES:
        imgs[key] = make_img(key, 900, 600)

    print("Gerando QR Code...")
    qr = make_qr(wa_url)

    print("Montando PDF...")
    c = pdfcanvas.Canvas(out_raw, pagesize=A4)
    c.setTitle("Cardapio Gourmet Premium — Casa Celi Congelados Artesanais")
    c.setAuthor("Casa Celi")
    c.setSubject("Catalogo de Marmitas Artesanais Premium")

    pg_capa(c, imgs);      c.showPage()
    pg_proposta(c);        c.showPage()
    pg_trad1(c, imgs);     c.showPage()
    pg_trad2(c, imgs);     c.showPage()
    pg_premium(c, imgs);   c.showPage()
    pg_kits(c);            c.showPage()
    pg_cta(c, imgs, qr)
    c.save()
    print(f"  PDF base: {out_raw}")

    print("Adicionando interatividade...")
    doc = fitz.open(out_raw)
    doc.set_toc([
        [1, "Inicio — Capa",                1],
        [1, "Nossa Proposta & Selos",        2],
        [1, "Linha Tradicional — Parte 1",  3],
        [1, "Linha Tradicional — Parte 2",  4],
        [1, "Linha Premium",                5],
        [1, "Kits & Como Pedir",            6],
        [1, "Fazer Pedido — WhatsApp",      7],
    ])

    # Link WhatsApp no botao CTA (pagina 7)
    pg7 = doc[6]
    btn_x0 = 1.5*cm + 128 + 44
    btn_w  = (W - 3*cm) - 128 - 66
    btn_y0 = H - 430 + (220-128)/2 + 128/2 - 50  # aprox
    btn_rect = fitz.Rect(btn_x0, btn_y0, btn_x0+btn_w, btn_y0+22)
    pg7.insert_link({"kind": fitz.LINK_URI, "from": btn_rect, "uri": wa_url})

    # Link no QR Code
    qr_rect = fitz.Rect(1.5*cm+16, H-430+(220-128)/2-4, 1.5*cm+16+136, H-430+(220-128)/2+136)
    pg7.insert_link({"kind": fitz.LINK_URI, "from": qr_rect, "uri": wa_url})

    # Footer clicavel = volta para capa
    for i in range(1, 7):
        pg = doc[i]
        pg.insert_link({"kind": fitz.LINK_GOTO, "from": fitz.Rect(0, 0, W, 26),
                         "page": 0, "to": fitz.Point(0, H)})

    doc.save(out_final, garbage=4, deflate=True)
    kb = os.path.getsize(out_final) // 1024
    print(f"\nPDF FINAL: {out_final}")
    print(f"  {doc.page_count} paginas  |  {kb} KB")
    doc.close()

if __name__ == "__main__":
    main()
