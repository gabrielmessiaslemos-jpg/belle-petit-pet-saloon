#!/usr/bin/env python3
"""Casa Celi – Cardapio Gourmet Premium v4
Real logo from original PDF + improved synthetic food images + premium layout.
"""
import os, io, math, random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFilter
import qrcode
import fitz

W, H = A4
OUT      = "/home/user/belle-petit-pet-saloon/CasaCeli_Cardapio_Premium_v4.pdf"
LOGO_PATH= "/home/user/belle-petit-pet-saloon/fotos_reais/pg1_img1.png"
PHOTOS   = "/home/user/belle-petit-pet-saloon/fotos_cardapio"
QR_PATH  = f"{PHOTOS}/qrcode_wa.png"
WA_URL   = "https://wa.me/5511999999999"

# ── Fonts ─────────────────────────────────────────────────────────────────────
BF = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("R",  BF+"LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("B",  BF+"LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("I",  BF+"LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("BI", BF+"LiberationSans-BoldItalic.ttf"))

# ── Palette (0-1 floats) ──────────────────────────────────────────────────────
VM = (0x1E/255, 0x4B/255, 0x26/255)   # Verde musgo
VO = (0x8F/255, 0x9C/255, 0x68/255)   # Verde oliva
TC = (0xB0/255, 0x52/255, 0x16/255)   # Terracota
MR = (0x4F/255, 0x29/255, 0x15/255)   # Marrom
DO = (0xB8/255, 0x9A/255, 0x4A/255)   # Dourado
BG = (0xFA/255, 0xF8/255, 0xF3/255)   # Pergaminho
WH = (1.0, 1.0, 1.0)

def F(c, col):
    c.setFillColorRGB(*col)
    c.setFillAlpha(1.0)

def S(c, col):
    c.setStrokeColorRGB(*col)
    c.setStrokeAlpha(1.0)

def RA(c):
    c.setFillAlpha(1.0)
    c.setStrokeAlpha(1.0)

def txt(c, text, x, y, font="R", size=10, col=None, align="left"):
    if col:
        F(c, col)
    c.setFont(font, size)
    if align == "center":
        c.drawCentredString(x, y, text)
    elif align == "right":
        c.drawRightString(x, y, text)
    else:
        c.drawString(x, y, text)

# ── Improved synthetic food images ────────────────────────────────────────────
# Each dish gets a distinct color palette to suggest the actual food
DISH_PALETTES = {
    "frango_desfiado":   [(220,160,60),(200,130,40),(240,180,80),(180,110,30)],
    "frango_cubos":      [(210,150,50),(180,100,30),(230,170,70),(150,90,20)],
    "frango_xadrez":     [(200,50,30),(50,150,60),(220,170,30),(180,80,40)],
    "file_mel":          [(220,160,40),(200,140,20),(240,180,60),(170,120,10)],
    "merluza":           [(200,210,220),(160,180,200),(220,230,240),(140,160,190)],
    "almondegas":        [(160,60,30),(140,40,10),(190,90,50),(120,30,10)],
    "parmegiana":        [(210,70,30),(240,160,40),(190,50,10),(230,120,50)],
    "escondidinho":      [(180,120,60),(160,90,40),(200,150,80),(140,70,20)],
    "panquecas":         [(220,180,100),(200,150,70),(240,200,120),(180,130,50)],
    "nhoque":            [(200,160,80),(180,130,50),(220,180,100),(150,100,30)],
    "lasanha":           [(190,80,40),(210,120,60),(170,50,10),(230,150,80)],
    "macarrao":          [(230,190,80),(210,160,50),(240,210,100),(190,140,30)],
}

def make_food_img(key, w=520, h=340):
    """Generate appetizing synthetic food image for a dish."""
    palette = DISH_PALETTES.get(key, [(200,150,80),(180,120,50),(220,170,100),(160,100,30)])
    img = Image.new("RGB", (w, h), (30, 20, 10))
    px  = img.load()

    # Background gradient - dark warm bokeh
    for y in range(h):
        for x in range(w):
            t = y / h
            r = int(20 + 40*t)
            g = int(10 + 20*t)
            b = int(5  + 10*t)
            px[x, y] = (r, g, b)

    # Plate circle - centered slightly up
    cx, cy = w//2, int(h*0.44)
    pr = int(min(w,h)*0.34)

    for y in range(h):
        for x in range(w):
            dx, dy = x-cx, y-cy
            d  = math.sqrt(dx*dx + dy*dy)
            if d < pr:
                # Plate rim: off-white
                rim = pr * 0.88
                if d > rim:
                    t = (d - rim) / (pr - rim)
                    r = int(230*(1-t) + 20*t)
                    g = int(220*(1-t) + 10*t)
                    b = int(200*(1-t) + 5*t)
                    px[x, y] = (r, g, b)
                else:
                    # Food area - blend palette colors
                    ang = math.atan2(dy, dx)
                    idx = int((ang + math.pi) / (2*math.pi) * len(palette)) % len(palette)
                    c1  = palette[idx]
                    c2  = palette[(idx+1) % len(palette)]
                    tf  = ((ang + math.pi) / (2*math.pi) * len(palette)) % 1.0
                    # Radial gradient
                    tr  = (d / rim) ** 0.7
                    base_r = int(c1[0]*(1-tf) + c2[0]*tf)
                    base_g = int(c1[1]*(1-tf) + c2[1]*tf)
                    base_b = int(c1[2]*(1-tf) + c2[2]*tf)
                    # Darken edges, lighten center
                    lf = 1 - 0.45*tr
                    r  = min(255, int(base_r * lf + 60*(1-tr)))
                    g  = min(255, int(base_g * lf + 40*(1-tr)))
                    b  = min(255, int(base_b * lf + 20*(1-tr)))
                    # Noise
                    noise = random.randint(-12, 12)
                    r = max(0, min(255, r + noise))
                    g = max(0, min(255, g + noise))
                    b = max(0, min(255, b + noise))
                    px[x, y] = (r, g, b)

    # Plate shadow below
    draw = ImageDraw.Draw(img)
    shadow_y = cy + pr - 10
    for i in range(18):
        alpha = int(90 * (1 - i/18))
        ew = pr*2 - i*8
        eh = 18 - i
        if ew > 0 and eh > 0:
            draw.ellipse([cx-ew//2, shadow_y+i, cx+ew//2, shadow_y+i+eh],
                        fill=(5, 3, 0))

    # Warm highlight glow on plate
    for y in range(h):
        for x in range(w):
            dx, dy = x-cx, y-cy
            d = math.sqrt(dx*dx + dy*dy)
            if d < pr*0.35:
                t = 1 - d/(pr*0.35)
                r0, g0, b0 = px[x, y]
                r0 = min(255, int(r0 + 50*t))
                g0 = min(255, int(g0 + 35*t))
                b0 = min(255, int(b0 + 15*t))
                px[x, y] = (r0, g0, b0)

    # Blur slightly for photographic feel
    img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
    return img

# Pre-generate and save all dish images
DISH_KEYS_TRAD = ["frango_desfiado","frango_cubos","frango_xadrez","file_mel","merluza","almondegas"]
DISH_KEYS_PREM = ["parmegiana","escondidinho","panquecas","nhoque","lasanha","macarrao"]

def gen_images():
    for key in DISH_KEYS_TRAD + DISH_KEYS_PREM:
        path = f"{PHOTOS}/v4_{key}.jpeg"
        if not os.path.exists(path):
            img = make_food_img(key, 520, 340)
            img.save(path, "JPEG", quality=88)
    # QR code
    if not os.path.exists(QR_PATH):
        qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_M,
                           box_size=10, border=3)
        qr.add_data(WA_URL)
        qr.make(fit=True)
        qrimg = qr.make_image(fill_color=(0x1E, 0x4B, 0x26), back_color=(0xFA, 0xF8, 0xF3))
        qrimg.save(QR_PATH)

# ── Dish data ─────────────────────────────────────────────────────────────────
TRAD = [
    {"nome":"Frango Desfiado",            "desc":"Creme de milho cremoso, arroz branco e brocolis no vapor.",           "preco":"A partir de R$ 18,00","campeo":True, "tag":"ALTA ACEITACAO", "key":"frango_desfiado"},
    {"nome":"Frango em Cubos Acebolado",  "desc":"Frango macio, cebola caramelizada, arroz, feijao e misto de legumes.","preco":"A partir de R$ 18,00","campeo":False,"tag":"EQUILIBRADO",    "key":"frango_cubos"},
    {"nome":"Frango Xadrez",              "desc":"Classico agridoce com pimentoes coloridos, arroz, feijao e vagem.",   "preco":"A partir de R$ 18,00","campeo":True, "tag":"SUCESSO",        "key":"frango_xadrez"},
    {"nome":"File ao Molho de Mel",       "desc":"File suculento ao mel e ervas, arroz, feijao e abobrinha grelhada.",  "preco":"A partir de R$ 18,00","campeo":False,"tag":"TOQUE ESPECIAL","key":"file_mel"},
    {"nome":"File de Merluza",            "desc":"Peixe suculento, arroz branco e couve-flor gratinada. Leve.",         "preco":"A partir de R$ 18,00","campeo":False,"tag":"LEVE & NUTRITIVO","key":"merluza"},
    {"nome":"Almondegas ao Molho",        "desc":"Almondegas artesanais no molho especial, arroz, feijao e legumes.",   "preco":"A partir de R$ 18,00","campeo":True, "tag":"CLASSICO",       "key":"almondegas"},
]

PREM = [
    {"nome":"Parmegiana",         "desc":"Queijo derretido, molho de tomates frescos, arroz e batatinhas douradas.","preco":"R$ 28,50","campeo":True, "tag":"PREMIUM",       "key":"parmegiana"},
    {"nome":"Escondidinho",       "desc":"Carne, frango ou costela desfiada. Cremoso, encorpado e irresistivel.",    "preco":"R$ 24,50","campeo":True, "tag":"FAVORITO",      "key":"escondidinho"},
    {"nome":"Panquecas Caseiras", "desc":"Massa fina artesanal com frango e catupiry ou presunto e queijo.",         "preco":"R$ 23,50","campeo":False,"tag":"ARTESANAL",     "key":"panquecas"},
    {"nome":"Nhoque a Bolonhesa", "desc":"Massa leve, molho ragu encorpado de carne, ervas e parmesao.",             "preco":"R$ 33,50","campeo":True, "tag":"CHEF",          "key":"nhoque"},
    {"nome":"Lasanha Saborosa",   "desc":"Camadas generosas, molho apurado, queijo gratinado, toque artesanal.",     "preco":"R$ 26,00","campeo":False,"tag":"CLASSICO",      "key":"lasanha"},
    {"nome":"Macarroes da Casa",  "desc":"Bolonhesa robusta, quatro queijos ou bechamel cremoso. Sob encomenda.",    "preco":"R$ 24,90","campeo":False,"tag":"SOB ENCOMENDA", "key":"macarrao"},
]

# ── Layout helpers ────────────────────────────────────────────────────────────
MG = 28   # page margin
GAP = 10  # gap between cards

def hdr_bar(c, title, subtitle=None):
    HDR_H = 55
    F(c, VM)
    c.rect(0, H - HDR_H, W, HDR_H, fill=1, stroke=0)
    F(c, DO)
    c.rect(0, H - HDR_H - 3, W, 3, fill=1, stroke=0)
    txt(c, title, W/2, H-32, font="B", size=15, col=WH, align="center")
    if subtitle:
        txt(c, subtitle, W/2, H-47, font="I", size=7.5, col=VO, align="center")
    RA(c)
    return HDR_H

def footer_bar(c, pgnum):
    FTR_H = 28
    F(c, VM)
    c.rect(0, 0, W, FTR_H, fill=1, stroke=0)
    F(c, DO)
    c.rect(0, FTR_H, W, 1.5, fill=1, stroke=0)
    txt(c, "Casa Celi  |  Congelados Artesanais  |  Comida feita hoje para facilitar o seu amanha.",
        W/2, 10, font="I", size=7, col=VO, align="center")
    txt(c, str(pgnum), W-16, 10, font="B", size=9, col=DO, align="right")
    RA(c)
    return FTR_H

def dish_card(c, x, y, cw, ch, dish):
    img_h = int(ch * 0.52)
    txt_h = ch - img_h

    # Drop shadow
    c.saveState()
    c.setFillColorRGB(0.08, 0.04, 0.01)
    c.setFillAlpha(0.22)
    c.rect(x+5, y-5, cw, ch, fill=1, stroke=0)
    c.restoreState()
    RA(c)

    # Card white base
    F(c, WH)
    c.rect(x, y, cw, ch, fill=1, stroke=0)

    # Photo
    img_path = f"{PHOTOS}/v4_{dish['key']}.jpeg"
    if os.path.exists(img_path):
        c.drawImage(img_path, x, y+txt_h, cw, img_h,
                    mask='auto', preserveAspectRatio=False)

    # Dark fade at bottom of photo to blend into text area
    c.saveState()
    c.setFillColorRGB(0.05, 0.02, 0)
    c.setFillAlpha(0.40)
    c.rect(x, y+txt_h, cw, 20, fill=1, stroke=0)
    c.restoreState()
    RA(c)

    # Tag label over photo
    tag = dish.get("tag", "")
    if tag:
        tag_col = DO if dish["campeo"] else TC
        tag_w   = min(len(tag)*5.2 + 14, cw-8)
        F(c, tag_col)
        c.rect(x+5, y+txt_h+5, tag_w, 13, fill=1, stroke=0)
        txt(c, tag, x+9, y+txt_h+9, font="B", size=6, col=WH)

    # Text area - solid VM background
    F(c, VM)
    c.rect(x, y, cw, txt_h, fill=1, stroke=0)

    # CAMPEAO banner at top of text area
    if dish["campeo"]:
        F(c, DO)
        c.rect(x, y+txt_h-15, cw, 15, fill=1, stroke=0)
        txt(c, "* CAMPEO DE VENDAS *", x+cw/2, y+txt_h-11, font="B", size=6.5, col=MR, align="center")

    # Dish name
    banner_off = 18 if dish["campeo"] else 5
    name_y = y + txt_h - banner_off - 13
    name   = dish["nome"]
    if len(name) > 24:
        words = name.split()
        mid   = (len(words)+1)//2
        l1    = " ".join(words[:mid])
        l2    = " ".join(words[mid:])
        txt(c, l1, x+7, name_y,     font="B", size=9,   col=WH)
        txt(c, l2, x+7, name_y-11,  font="B", size=9,   col=WH)
        desc_top = name_y - 24
    else:
        txt(c, name, x+7, name_y, font="B", size=9.5, col=WH)
        desc_top = name_y - 13

    # Description - max 2 lines
    desc    = dish["desc"]
    maxch   = int(cw / 4.3)
    lines   = []
    cur     = ""
    for w in desc.split():
        t = (cur+" "+w).strip()
        if len(t) <= maxch:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)

    for i, line in enumerate(lines[:2]):
        txt(c, line, x+7, desc_top - i*11, font="I", size=7, col=VO)

    # Price - right-aligned in gold
    F(c, DO)
    c.setFont("B", 10)
    c.drawRightString(x+cw-7, y+7, dish["preco"])

    # Thin gold border
    S(c, DO)
    c.setLineWidth(0.7)
    c.rect(x, y, cw, ch, fill=0, stroke=1)
    RA(c)


def pg_dishes(c, dishes, title, subtitle, pgnum, note=None):
    hdr_h = hdr_bar(c, title, subtitle)
    ftr_h = footer_bar(c, pgnum)

    note_h = 26 if note else 0
    if note:
        ny = ftr_h + 2
        F(c, TC)
        c.rect(MG, ny, W-2*MG, note_h-2, fill=1, stroke=0)
        txt(c, note, W/2, ny+8, font="B", size=8, col=WH, align="center")
        RA(c)

    start_y = H - hdr_h - GAP
    end_y   = ftr_h + note_h + GAP
    total_h = start_y - end_y
    card_h  = (total_h - 2*GAP) / 3
    card_w  = (W - 2*MG - GAP) / 2
    col_x   = [MG, MG + card_w + GAP]

    for i, dish in enumerate(dishes):
        row = i // 2
        col = i % 2
        cx  = col_x[col]
        cy  = start_y - (row+1)*card_h - row*GAP
        dish_card(c, cx, cy, card_w, card_h, dish)


# ── Page 1 – Capa ─────────────────────────────────────────────────────────────
def pg_capa(c):
    # Pergaminho background with horizontal texture lines
    F(c, BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.saveState()
    c.setStrokeColorRGB(*VO)
    c.setStrokeAlpha(0.05)
    c.setLineWidth(1)
    for y0 in range(0, int(H)+1, 16):
        c.line(0, y0, W, y0)
    c.restoreState()
    RA(c)

    # ── Bottom strip (build up from y=0) ────────────────────────────────────
    strip_h = 58
    F(c, MR)
    c.rect(0, 0, W, strip_h, fill=1, stroke=0)
    F(c, DO)
    c.rect(0, strip_h, W, 2, fill=1, stroke=0)
    txt(c, "Casa Celi  |  Congelados Artesanais  |  Comida feita hoje para facilitar o seu amanha.",
        W/2, 22, font="I", size=7.5, col=DO, align="center")
    txt(c, "PIX  |  Cartao de Credito  |  Debito  |  Dinheiro",
        W/2, 8,  font="I", size=7,   col=VO, align="center")
    RA(c)

    # ── Feature trio cards (3 colored info cards) ────────────────────────────
    cards_bottom = strip_h + 16
    fc_h = 90
    fcard_data = [
        (VM, "Linha Tradicional", "300g | 400g | 500g", "R$ 18,00 a R$ 22,00"),
        (TC, "Linha Premium",     "400g especial",       "R$ 23,50 a R$ 33,50"),
        (MR, "Kits Casa Celi",    "10 | 20 | 30 unid.",  "3% OFF na soma"),
    ]
    fw = (W - 2*MG - 16) / 3
    for i, (fc_col, ft, fs, fp) in enumerate(fcard_data):
        fx = MG + i*(fw+8)
        fy = cards_bottom
        c.saveState()
        c.setFillColorRGB(0,0,0)
        c.setFillAlpha(0.15)
        c.rect(fx+3, fy-3, fw, fc_h, fill=1, stroke=0)
        c.restoreState()
        RA(c)
        F(c, fc_col)
        c.rect(fx, fy, fw, fc_h, fill=1, stroke=0)
        txt(c, ft, fx+fw/2, fy+fc_h-18, font="B", size=9.5, col=WH, align="center")
        txt(c, fs, fx+fw/2, fy+fc_h-32, font="I", size=8,   col=BG, align="center")
        F(c, DO)
        c.rect(fx+8, fy+8, fw-16, 20, fill=1, stroke=0)
        txt(c, fp, fx+fw/2, fy+14, font="B", size=8, col=MR, align="center")
        S(c, DO)
        c.setLineWidth(0.8)
        c.rect(fx, fy, fw, fc_h, fill=0, stroke=1)
        RA(c)

    # ── Gold separator ────────────────────────────────────────────────────────
    sep1_y = cards_bottom + fc_h + 14
    F(c, DO)
    c.rect(MG+30, sep1_y, W-2*MG-60, 1.5, fill=1, stroke=0)
    RA(c)

    # ── 4 seals row ──────────────────────────────────────────────────────────
    seals = ["Artesanal", "Sem Conservantes", "Gourmet", "Pronto em Min."]
    seal_r = 20
    seal_center_y = sep1_y + 22 + seal_r
    sw0 = W / len(seals)
    for i, seal in enumerate(seals):
        sx = i*sw0 + sw0/2
        F(c, VM)
        c.circle(sx, seal_center_y, seal_r, fill=1, stroke=0)
        S(c, DO)
        c.setLineWidth(1.2)
        c.circle(sx, seal_center_y, seal_r, fill=0, stroke=1)
        RA(c)
        txt(c, seal, sx, seal_center_y + seal_r + 6, font="B", size=6.5, col=MR, align="center")

    # ── Gold separator 2 ─────────────────────────────────────────────────────
    sep2_y = seal_center_y + seal_r + 26
    F(c, DO)
    c.rect(MG+30, sep2_y, W-2*MG-60, 1.5, fill=1, stroke=0)
    RA(c)

    # ── Tagline ───────────────────────────────────────────────────────────────
    tag_y = sep2_y + 22
    txt(c, '"Comida feita hoje para facilitar o seu amanha."',
        W/2, tag_y, font="BI", size=12, col=MR, align="center")

    # ── Logo (fills remaining space up to header) ────────────────────────────
    logo_bottom = tag_y + 22
    header_h = 90
    logo_avail = H - header_h - 8 - logo_bottom
    logo_sz = min(260, logo_avail)
    lx = W/2 - logo_sz/2
    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH, lx, logo_bottom, width=logo_sz, height=logo_sz, mask='auto')
    # Gold ring
    S(c, DO)
    c.setStrokeAlpha(0.30)
    c.setLineWidth(1.5)
    c.circle(W/2, logo_bottom + logo_sz/2, logo_sz/2 + 10, fill=0, stroke=1)
    RA(c)

    # ── Header band ──────────────────────────────────────────────────────────
    F(c, VM)
    c.rect(0, H-header_h, W, header_h, fill=1, stroke=0)
    F(c, DO)
    c.rect(0, H-header_h-3, W, 3, fill=1, stroke=0)
    txt(c, "CATALOGO GOURMET ARTESANAL 2025",              W/2, H-44, font="B", size=16, col=BG, align="center")
    txt(c, "Congelados Artesanais com Sabor de Cozinha Afetiva", W/2, H-63, font="I", size=9, col=VO, align="center")
    txt(c, "Marmitas Congeladas com Sabor de Comida Feita em Casa", W/2, H-78, font="I", size=8, col=VO, align="center")
    RA(c)


# ── Page 2 – Nossa Proposta ───────────────────────────────────────────────────
def pg_proposta(c):
    # Absolute Y positions (A4 = 841.89pt, Y=0 bottom, Y=H top)
    # Content area: y=28 (FTR_H) to y=787 (H-HDR_H=H-55)
    # Budget (759pt): intro=45, gap=10, cards=245, gap=18, seals_header=40,
    #   seals=2*115+10=240, gap=10, cta=151 → total=759 ✓
    HDR_H = 55
    FTR_H = 28
    hdr_bar(c, "Nossa Proposta", "Qualidade artesanal com a praticidade que sua rotina merece")
    footer_bar(c, 2)

    F(c, BG)
    c.rect(0, FTR_H, W, H-HDR_H-FTR_H, fill=1, stroke=0)
    RA(c)

    # Intro texts (top)
    txt(c, "Comida de verdade, feita com ingredientes selecionados e muito carinho.",
        W/2, 776, font="I", size=10, col=MR, align="center")
    txt(c, "Congelada na hora certa para manter sabor, textura e nutricao.",
        W/2, 759, font="I", size=9,  col=MR, align="center")
    F(c, DO)
    c.rect(MG+50, 745, W-2*MG-100, 1.5, fill=1, stroke=0)
    RA(c)

    # Linha cards: bottom=497, top=742 (h=245)
    cw2 = (W - 2*MG - 16) / 3
    ch2 = 245
    cy2 = 497
    linhas = [
        {"t":"Linha Tradicional","d":"Marmitas praticas para o dia a dia, com tempero caseiro equilibrado.","p":"R$ 18,00 a R$ 22,00","col":VM},
        {"t":"Linha Premium",    "d":"Receitas especiais em porcoes de 400g para uma refeicao caprichada.", "p":"R$ 23,50 a R$ 33,50","col":TC},
        {"t":"Kits Casa Celi",   "d":"Combos para organizar a semana ou o mes com 3% OFF na soma.",         "p":"3% OFF em todos",    "col":MR},
    ]
    for i, l in enumerate(linhas):
        cx2 = MG + i*(cw2+8)
        c.saveState()
        c.setFillColorRGB(0,0,0); c.setFillAlpha(0.16)
        c.rect(cx2+4, cy2-4, cw2, ch2, fill=1, stroke=0)
        c.restoreState(); RA(c)
        F(c, l["col"])
        c.rect(cx2, cy2, cw2, ch2, fill=1, stroke=0)
        txt(c, l["t"], cx2+cw2/2, cy2+ch2-24, font="B", size=12, col=WH, align="center")
        words = l["d"].split()
        lines2, cur = [], ""
        for w in words:
            t = (cur+" "+w).strip()
            if len(t) <= 26: cur = t
            else: lines2.append(cur); cur=w
        if cur: lines2.append(cur)
        for j, ln in enumerate(lines2[:4]):
            txt(c, ln, cx2+cw2/2, cy2+ch2-42-j*14, font="I", size=9, col=BG, align="center")
        F(c, DO)
        c.rect(cx2+8, cy2+12, cw2-16, 30, fill=1, stroke=0)
        txt(c, l["p"], cx2+cw2/2, cy2+20, font="B", size=10, col=MR, align="center")
        S(c, DO); c.setLineWidth(1)
        c.rect(cx2, cy2, cw2, ch2, fill=0, stroke=1)
        RA(c)

    # Compromissos section header
    F(c, DO)
    c.rect(MG, 479, W-2*MG, 1.5, fill=1, stroke=0)
    txt(c, "* Nossos Compromissos *", W/2, 458, font="BI", size=13, col=MR, align="center")
    RA(c)

    # Seals grid: 6 seals, 3 cols × 2 rows, each cell h=115
    seals = [
        ("Feito Artesanalmente","Receita caseira"),
        ("Congelamento Seguro","ABNT NBR"),
        ("Ingredientes Selecionados","Frescos & naturais"),
        ("Sem Conservantes","Formula limpa"),
        ("Producao Local","Apoie o local"),
        ("Pronto em Minutos","Ate 5 min micro"),
    ]
    sw3 = (W - 2*MG - 16) / 3
    sh3 = 115
    # row 0 top: 449, row 0 bottom: 334; row 1 top: 324, row 1 bottom: 209
    SEAL_TOPS = [449, 449 - sh3 - 10]  # y of top of each row

    for i, (title, sub) in enumerate(seals):
        row = i // 3; col = i % 3
        sx3   = MG + col*(sw3+8)
        card_t = SEAL_TOPS[row]
        card_b = card_t - sh3
        mid    = (card_t + card_b) / 2

        c.saveState()
        c.setFillColorRGB(*VM); c.setFillAlpha(0.06)
        c.rect(sx3, card_b, sw3, sh3, fill=1, stroke=0)
        c.restoreState(); RA(c)
        S(c, VO); c.setLineWidth(0.5)
        c.rect(sx3, card_b, sw3, sh3, fill=0, stroke=1); RA(c)

        F(c, VM); c.circle(sx3+28, mid+4, 22, fill=1, stroke=0)
        S(c, DO); c.setLineWidth(1.2); c.circle(sx3+28, mid+4, 22, fill=0, stroke=1); RA(c)
        F(c, DO); c.setFont("B", 12); c.drawCentredString(sx3+28, mid, str(i+1))
        txt(c, title, sx3+58, mid+14, font="B",  size=9,   col=VM)
        txt(c, sub,   sx3+58, mid-1,  font="I",  size=8.5, col=TC)
        RA(c)

    # CTA strip: y=28 to y=195 (h=167)
    F(c, VM)
    c.rect(0, FTR_H, W, 167, fill=1, stroke=0)
    F(c, DO); c.rect(0, FTR_H+167, W, 2, fill=1, stroke=0)
    txt(c, "Encomendar pelo WhatsApp  |  Escolha sua linha e peca agora",
        W/2, FTR_H + 83 + 5, font="B", size=11, col=WH, align="center")
    txt(c, "wa.me/5511999999999", W/2, FTR_H + 83 - 16, font="I", size=9, col=VO, align="center")
    RA(c)


# ── Page 5 – Kits + Como Pedir ────────────────────────────────────────────────
def pg_kits(c):
    HDR_H = 55
    FTR_H = 28
    hdr_bar(c, "Kits Casa Celi", "Combos para organizar a rotina com praticidade e economia")
    footer_bar(c, 5)

    F(c, BG)
    c.rect(0, FTR_H, W, H-HDR_H-FTR_H, fill=1, stroke=0)
    RA(c)

    # Layout (build top down, content_top = H-HDR_H-12 = 775):
    # Kit cards: 230pt, then caldos: 52pt, then "Como Pedir": 44pt, then steps: 200pt,
    # then WA banner: remainder

    kw   = (W - 2*MG - 16) / 3
    kh   = 230
    ky   = H - HDR_H - 14 - kh    # top of kit cards

    kits = [
        {"badge":"SEMANAL", "qtd":"10 marmitas",
         "desc":["Para organizar a","rotina semanal","com praticidade.",
                 "Ideal para quem","come em casa."], "col":VM, "extra":"3% OFF no total"},
        {"badge":"FAMILIA",  "qtd":"20 marmitas",
         "desc":["Almoco e jantar","sem preocupacao","para toda a familia.",
                 "Pratos variados","para a semana."], "col":TC, "extra":"3% OFF no total"},
        {"badge":"ECONOMIA", "qtd":"30 marmitas",
         "desc":["Abastece a casa","com o melhor","custo-beneficio.",
                 "Recomendado","para o mes todo."], "col":MR, "extra":"3% OFF + MELHOR OPCAO"},
    ]

    for i, kit in enumerate(kits):
        kx = MG + i*(kw+8)
        c.saveState()
        c.setFillColorRGB(0,0,0)
        c.setFillAlpha(0.20)
        c.rect(kx+5, ky-5, kw, kh, fill=1, stroke=0)
        c.restoreState()
        RA(c)

        F(c, BG)
        c.rect(kx, ky, kw, kh, fill=1, stroke=0)

        bh = 52
        F(c, kit["col"])
        c.rect(kx, ky+kh-bh, kw, bh, fill=1, stroke=0)
        txt(c, kit["badge"],  kx+kw/2, ky+kh-22, font="B", size=15, col=WH, align="center")
        txt(c, kit["qtd"],    kx+kw/2, ky+kh-38, font="I", size=9,  col=BG, align="center")

        for j, line in enumerate(kit["desc"]):
            txt(c, line, kx+kw/2, ky+kh-bh-20-j*14, font="R", size=8.5, col=MR, align="center")

        F(c, DO)
        c.rect(kx+10, ky+10, kw-20, 26, fill=1, stroke=0)
        txt(c, kit["extra"], kx+kw/2, ky+17, font="B", size=8, col=MR, align="center")

        S(c, kit["col"])
        c.setLineWidth(1.5)
        c.rect(kx, ky, kw, kh, fill=0, stroke=1)
        RA(c)

    # Caldos banner
    caldo_top = ky - 14
    caldo_h   = 52
    caldo_y   = caldo_top - caldo_h
    F(c, VO)
    c.rect(MG, caldo_y, W-2*MG, caldo_h, fill=1, stroke=0)
    S(c, VM)
    c.setLineWidth(1)
    c.rect(MG, caldo_y, W-2*MG, caldo_h, fill=0, stroke=1)
    txt(c, "CALDOS ARTESANAIS  |  500ml  |  R$ 21,90",
        W/2, caldo_y+32, font="B", size=13, col=VM, align="center")
    txt(c, "Opcoes quentinhas e confortaveis para completar o pedido.",
        W/2, caldo_y+14, font="I", size=8.5, col=MR, align="center")
    RA(c)

    # Como Pedir section
    section_top = caldo_y - 18
    txt(c, "Como Fazer seu Pedido", W/2, section_top, font="B", size=14, col=VM, align="center")
    F(c, DO)
    c.rect(MG+50, section_top-8, W-2*MG-100, 1.5, fill=1, stroke=0)
    RA(c)

    # Step cards: placed right below section header, fill to CTA
    sw4  = (W - 2*MG - 16) / 3
    cta_h = 72
    sh4  = section_top - 30 - (FTR_H + cta_h + 8)   # dynamic height
    sy4  = FTR_H + cta_h + 8                          # bottom of step cards

    steps = [
        ("1","Escolha", ["Selecione a linha,","os pratos e o tamanho.","Confira disponibilidade.","Escolha 300g, 400g ou 500g."], VM),
        ("2","Envie",   ["Mande a lista pelo","WhatsApp e confirme.","Aguarde confirmacao","de estoque e prazo."],                 TC),
        ("3","Combine", ["Finalize pagamento:","PIX, cartao ou dinheiro.","Combine retirada","ou entrega no endereco."],           MR),
    ]

    for i, (num, title, detail, scol) in enumerate(steps):
        sx4 = MG + i*(sw4+8)
        c.saveState()
        c.setFillColorRGB(0,0,0); c.setFillAlpha(0.14)
        c.rect(sx4+3, sy4-3, sw4, sh4, fill=1, stroke=0)
        c.restoreState(); RA(c)

        F(c, BG)
        c.rect(sx4, sy4, sw4, sh4, fill=1, stroke=0)

        fh = 50
        F(c, scol)
        c.rect(sx4, sy4+sh4-fh, sw4, fh, fill=1, stroke=0)
        txt(c, num, sx4+sw4/2, sy4+sh4-fh/2-11, font="B", size=26, col=WH, align="center")

        txt(c, title, sx4+sw4/2, sy4+sh4-fh-20, font="B", size=12, col=scol, align="center")
        F(c, DO); c.rect(sx4+15, sy4+sh4-fh-30, sw4-30, 1, fill=1, stroke=0); RA(c)
        for j, line in enumerate(detail):
            txt(c, line, sx4+sw4/2, sy4+sh4-fh-44-j*15, font="I", size=8.5, col=MR, align="center")

        S(c, scol); c.setLineWidth(1)
        c.rect(sx4, sy4, sw4, sh4, fill=0, stroke=1); RA(c)

    # Bottom CTA strip (above footer)
    F(c, TC)
    c.rect(0, FTR_H, W, cta_h, fill=1, stroke=0)
    F(c, DO); c.rect(0, FTR_H+cta_h, W, 2, fill=1, stroke=0)
    txt(c, "Peca agora pelo WhatsApp  |  wa.me/5511999999999",
        W/2, FTR_H + cta_h/2 + 6, font="B", size=11, col=WH, align="center")
    txt(c, "PIX  |  Credito  |  Debito  |  Dinheiro",
        W/2, FTR_H + cta_h/2 - 10, font="I", size=9, col=BG, align="center")
    RA(c)


# ── Page 6 – CTA Final ────────────────────────────────────────────────────────
def pg_cta(c):
    # Dark hero bg
    F(c, MR)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Subtle diagonal texture
    c.saveState()
    c.setStrokeColorRGB(*DO)
    c.setStrokeAlpha(0.07)
    c.setLineWidth(1)
    for xi in range(-int(H), int(W)+int(H), 22):
        c.line(xi, 0, xi+int(H), int(H))
    c.restoreState()
    RA(c)

    # Gold top accent
    F(c, DO)
    c.rect(0, H-5, W, 5, fill=1, stroke=0)
    RA(c)

    # Headline
    txt(c, "FINALIZE SEU PEDIDO AGORA", W/2, H-52, font="B", size=20, col=DO,  align="center")
    txt(c, "Seu almoco da semana comeca aqui.", W/2, H-72, font="BI", size=13, col=BG, align="center")
    txt(c, "Escolha seus pratos, envie a quantidade e combine a entrega.", W/2, H-89, font="I", size=9, col=VO, align="center")

    # CTA box
    bx  = 55
    bw  = W - 110
    bh  = 225
    by  = H/2 - bh/2 - 15

    # Shadow
    c.saveState()
    c.setFillColorRGB(0,0,0)
    c.setFillAlpha(0.30)
    c.rect(bx+7, by-7, bw, bh, fill=1, stroke=0)
    c.restoreState()
    RA(c)

    # Box
    F(c, BG)
    c.rect(bx, by, bw, bh, fill=1, stroke=0)
    S(c, DO)
    c.setLineWidth(2.5)
    c.rect(bx, by, bw, bh, fill=0, stroke=1)
    RA(c)

    # Gold top strip on box
    F(c, DO)
    c.rect(bx, by+bh-22, bw, 22, fill=1, stroke=0)
    txt(c, "Chame pelo WhatsApp!", bx+bw/2, by+bh-15, font="B", size=10, col=MR, align="center")
    RA(c)

    # QR code left
    qr_sz = 115
    qr_x  = bx + 22
    qr_y  = by + bh/2 - qr_sz/2 - 10
    if os.path.exists(QR_PATH):
        c.drawImage(QR_PATH, qr_x, qr_y, width=qr_sz, height=qr_sz, mask='auto')

    # QR border
    S(c, VM)
    c.setLineWidth(1.5)
    c.rect(qr_x, qr_y, qr_sz, qr_sz, fill=0, stroke=1)
    RA(c)
    txt(c, "Aponte a camera para pedir", qr_x+qr_sz/2, qr_y-14, font="I", size=7.5, col=MR, align="center")

    # Right section
    rx   = qr_x + qr_sz + 22
    rw   = bx + bw - rx - 16

    # WhatsApp button
    btn_y = by + bh/2 + 10
    btn_h = 42
    F(c, VM)
    c.rect(rx, btn_y, rw, btn_h, fill=1, stroke=0)
    F(c, DO)
    c.rect(rx, btn_y+btn_h-4, rw, 4, fill=1, stroke=0)
    c.rect(rx, btn_y,         rw, 4, fill=1, stroke=0)
    txt(c, "FAZER PEDIDO AGORA", rx+rw/2, btn_y+15, font="B", size=12, col=WH, align="center")
    RA(c)

    txt(c, "Pagamentos aceitos:", rx+rw/2, btn_y-18, font="B",  size=8.5, col=VM, align="center")
    txt(c, "PIX  |  Cartao de Credito  |  Debito  |  Dinheiro",
        rx+rw/2, btn_y-32, font="R", size=8, col=MR, align="center")

    # Value circles row inside box
    vcircles = ["Artesanal","Caseiro","Nutritivo","Pratico","Premium","Local"]
    vc_y  = by + 18
    vc_total_w = bw - 20
    vc_step = vc_total_w / len(vcircles)
    for i, label in enumerate(vcircles):
        vx = bx + 10 + i*vc_step + vc_step/2
        F(c, VM)
        c.setFillAlpha(0.18)
        c.circle(vx, vc_y+14, 16, fill=1, stroke=0)
        c.setFillAlpha(1.0)
        S(c, DO)
        c.setLineWidth(0.8)
        c.circle(vx, vc_y+14, 16, fill=0, stroke=1)
        RA(c)
        txt(c, label, vx, vc_y+4, font="B", size=6, col=VM, align="center")

    RA(c)

    # Brand strip at bottom
    brand_h = 72
    F(c, VM)
    c.rect(0, 0, W, brand_h, fill=1, stroke=0)
    F(c, DO)
    c.rect(0, brand_h, W, 2, fill=1, stroke=0)
    txt(c, "Casa Celi", W/2, brand_h-24, font="B",  size=18, col=DO, align="center")
    txt(c, '"Comida feita hoje para facilitar o seu amanha."', W/2, brand_h-40, font="I", size=9, col=VO, align="center")
    txt(c, "PIX  |  Credito  |  Debito  |  Dinheiro", W/2, 10, font="R", size=8, col=VO, align="center")
    RA(c)


# ── Add interactivity via PyMuPDF ─────────────────────────────────────────────
def add_interactivity(path):
    doc = fitz.open(path)

    # TOC / bookmarks
    toc = [
        [1, "Capa",                1],
        [1, "Nossa Proposta",      2],
        [1, "Linha Tradicional",   3],
        [1, "Linha Premium",       4],
        [1, "Kits & Como Pedir",   5],
        [1, "Finalize seu Pedido", 6],
    ]
    doc.set_toc(toc)

    # WhatsApp link on CTA page (page index 5 = page 6)
    cta_page = doc[5]
    btn_rect = fitz.Rect(120, 320, 475, 365)
    cta_page.insert_link({"kind": fitz.LINK_URI, "from": btn_rect, "uri": WA_URL})

    # Page nav links: footer area on each page except cover
    for i in range(1, len(doc)):
        page   = doc[i]
        pw, ph = page.rect.width, page.rect.height
        if i < len(doc)-1:
            next_r = fitz.Rect(pw-70, ph-28, pw, ph)
            page.insert_link({"kind": fitz.LINK_GOTO, "from": next_r, "page": i+1, "to": fitz.Point(0,0)})
        if i > 0:
            prev_r = fitz.Rect(0, ph-28, 70, ph)
            page.insert_link({"kind": fitz.LINK_GOTO, "from": prev_r, "page": i-1, "to": fitz.Point(0,0)})

    tmp = path + ".tmp"
    doc.save(tmp)
    doc.close()
    import shutil; shutil.move(tmp, path)


# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    print("Generating dish images...")
    gen_images()

    print("Building PDF...")
    c = canvas.Canvas(OUT, pagesize=A4)

    pg_capa(c);    c.showPage()
    pg_proposta(c);c.showPage()

    pg_dishes(c, TRAD, "Linha Tradicional",
              "Tempero caseiro e equilibrio perfeito  |  300g | 400g | 500g", 3,
              note="Todos os pratos disponíveis em 300g, 400g e 500g  |  Peca por WhatsApp")
    c.showPage()

    pg_dishes(c, PREM, "Linha Premium",
              "Receitas especiais em 400g  |  Para uma refeicao verdadeiramente caprichada", 4)
    c.showPage()

    pg_kits(c);    c.showPage()
    pg_cta(c);     c.showPage()

    c.save()
    print(f"PDF saved: {OUT}")

    print("Adding interactivity...")
    add_interactivity(OUT)
    print("Done!")

if __name__ == "__main__":
    build()
