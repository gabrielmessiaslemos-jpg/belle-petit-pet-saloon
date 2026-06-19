#!/usr/bin/env python3
"""
Gerador do Cardápio Profissional — Casa Celi Congelados Artesanais
Design: tipografia rica, paleta quente, ícones visuais, layout editorial
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String, Polygon
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.platypus import Flowable
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.graphics import renderPDF
import math

# ─── PALETA ──────────────────────────────────────────────────────────────────
VERDE_ESCURO   = colors.HexColor("#1A3A2A")   # fundo header / destaques
VERDE_MEDIO    = colors.HexColor("#2D6A4F")   # subtítulos
VERDE_CLARO    = colors.HexColor("#52B788")   # badges / bordas
VERDE_MENTA    = colors.HexColor("#D8F3DC")   # backgrounds suaves
AMARELO_OURO   = colors.HexColor("#F5A623")   # preços / ícones de estrela
LARANJA_QUENTE = colors.HexColor("#E76F51")   # tags premium / CTA
CREME          = colors.HexColor("#FEFAE0")   # fundo de página
BRANCO         = colors.white
CINZA_SUAVE    = colors.HexColor("#F0EDE5")   # separadores leves
CINZA_TEXTO    = colors.HexColor("#4A4A4A")   # corpo de texto
PRETO_RICO     = colors.HexColor("#1C1C1C")   # títulos fortes

W, H = A4  # 595.27 x 841.89 pts


# ─── FORMAS DECORATIVAS ──────────────────────────────────────────────────────
class CircleDecor(Flowable):
    """Círculo decorativo colorido."""
    def __init__(self, size=20, color=VERDE_CLARO, fill=True):
        self.size = size
        self.color = color
        self.fill = fill

    def wrap(self, *args):
        return self.size, self.size

    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.setStrokeColor(self.color)
        if self.fill:
            c.circle(self.size / 2, self.size / 2, self.size / 2, fill=1, stroke=0)
        else:
            c.setLineWidth(2)
            c.circle(self.size / 2, self.size / 2, self.size / 2 - 1, fill=0, stroke=1)


class DividerLine(Flowable):
    """Linha decorativa com círculos nas pontas."""
    def __init__(self, width=None, color=VERDE_CLARO, thickness=1.5):
        self._width = width
        self.color = color
        self.thickness = thickness

    def wrap(self, avail_w, avail_h):
        self._avail = avail_w
        return avail_w, 12

    def draw(self):
        w = self._avail
        c = self.canv
        c.setStrokeColor(self.color)
        c.setFillColor(self.color)
        c.setLineWidth(self.thickness)
        c.line(0, 6, w, 6)
        c.circle(0, 6, 3, fill=1, stroke=0)
        c.circle(w, 6, 3, fill=1, stroke=0)


class BadgeTag(Flowable):
    """Tag colorida (badge) para categorias."""
    def __init__(self, text, bg=LARANJA_QUENTE, fg=BRANCO, w=90, h=20):
        self.text = text
        self.bg = bg
        self.fg = fg
        self._w = w
        self._h = h

    def wrap(self, *args):
        return self._w, self._h

    def draw(self):
        c = self.canv
        r = self._h / 2
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self._w, self._h, r, fill=1, stroke=0)
        c.setFillColor(self.fg)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(self._w / 2, (self._h - 8) / 2 + 1, self.text)


class PriceBox(Flowable):
    """Box destacado para preço."""
    def __init__(self, price_text, w=120, h=32):
        self.price = price_text
        self._w = w
        self._h = h

    def wrap(self, *args):
        return self._w, self._h

    def draw(self):
        c = self.canv
        c.setFillColor(AMARELO_OURO)
        c.roundRect(0, 0, self._w, self._h, 6, fill=1, stroke=0)
        c.setFillColor(PRETO_RICO)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(self._w / 2, (self._h - 13) / 2 + 2, self.price)


class DishCard(Flowable):
    """Card visual de prato — retângulo com emoji, nome, descrição e preço."""
    def __init__(self, emoji, nome, descricao, preco, badge=None,
                 card_w=None, card_h=130, accent=VERDE_MEDIO):
        self.emoji = emoji
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.badge = badge
        self._card_w = card_w  # resolved in wrap
        self._card_h = card_h
        self.accent = accent

    def wrap(self, avail_w, avail_h):
        self._card_w = avail_w
        return avail_w, self._card_h

    def draw(self):
        c = self.canv
        w, h = self._card_w, self._card_h

        # Sombra
        c.setFillColor(colors.HexColor("#CCCCCC"))
        c.roundRect(3, -3, w, h, 10, fill=1, stroke=0)

        # Fundo branco do card
        c.setFillColor(BRANCO)
        c.setStrokeColor(CINZA_SUAVE)
        c.setLineWidth(1)
        c.roundRect(0, 0, w, h, 10, fill=1, stroke=1)

        # Barra lateral colorida
        c.setFillColor(self.accent)
        c.roundRect(0, 0, 8, h, 5, fill=1, stroke=0)
        c.rect(4, 0, 4, h, fill=1, stroke=0)  # fechar lado direito da borda

        # Emoji grande
        c.setFont("Helvetica-Bold", 38)
        c.setFillColor(PRETO_RICO)
        c.drawString(20, h - 55, self.emoji)

        # Badge de categoria
        if self.badge:
            bw = 85
            bh = 18
            c.setFillColor(LARANJA_QUENTE)
            c.roundRect(w - bw - 10, h - bh - 8, bw, bh, 5, fill=1, stroke=0)
            c.setFillColor(BRANCO)
            c.setFont("Helvetica-Bold", 7)
            c.drawCentredString(w - bw / 2 - 10, h - bh - 8 + 5, self.badge)

        # Nome do prato
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(PRETO_RICO)
        nome_y = h - 68
        # Truncar nome longo
        nome = self.nome if len(self.nome) <= 38 else self.nome[:35] + "..."
        c.drawString(20, nome_y, nome)

        # Linha separadora
        c.setStrokeColor(CINZA_SUAVE)
        c.setLineWidth(0.8)
        c.line(20, nome_y - 6, w - 15, nome_y - 6)

        # Descrição (multi-linha simples)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(CINZA_TEXTO)
        desc_lines = self._wrap_text(self.descricao, w - 35, "Helvetica", 8.5, c)
        y = nome_y - 20
        for line in desc_lines[:3]:
            c.drawString(20, y, line)
            y -= 12

        # Box de preço
        pw = 115
        ph = 26
        c.setFillColor(AMARELO_OURO)
        c.roundRect(w - pw - 12, 10, pw, ph, 6, fill=1, stroke=0)
        c.setFillColor(PRETO_RICO)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(w - pw / 2 - 12, 10 + (ph - 11) / 2 + 1, self.preco)

    def _wrap_text(self, text, max_w, font, size, c):
        words = text.split()
        lines = []
        cur = ""
        for word in words:
            test = (cur + " " + word).strip()
            if c.stringWidth(test, font, size) <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


# ─── CANVAS CALLBACKS (fundo / cabeçalho de página) ────────────────────────
def page_background(canvas, doc):
    """Desenha fundo creme e footer em todas as páginas."""
    canvas.saveState()
    canvas.setFillColor(CREME)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Footer
    canvas.setFillColor(VERDE_ESCURO)
    canvas.rect(0, 0, W, 28, fill=1, stroke=0)
    canvas.setFillColor(AMARELO_OURO)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawCentredString(W / 2, 10, "Casa Celi • Congelados Artesanais • Comida feita hoje para facilitar o seu amanhã")
    canvas.restoreState()


def cover_background(canvas, doc):
    """Fundo especial para capa."""
    canvas.saveState()
    # Fundo verde escuro
    canvas.setFillColor(VERDE_ESCURO)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Faixa dourada decorativa inferior
    canvas.setFillColor(AMARELO_OURO)
    canvas.rect(0, 0, W, 8, fill=1, stroke=0)
    # Círculos decorativos (background art)
    canvas.setFillColor(colors.HexColor("#2D6A4F"))
    canvas.circle(W * 0.85, H * 0.75, 120, fill=1, stroke=0)
    canvas.circle(W * 0.1, H * 0.2, 80, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#1A4535"))
    canvas.circle(W * 0.7, H * 0.15, 60, fill=1, stroke=0)
    canvas.circle(W * 0.15, H * 0.85, 90, fill=1, stroke=0)
    canvas.restoreState()


# ─── ESTILOS ─────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def make_styles():
    return {
        "cover_brand": ParagraphStyle("cover_brand",
            fontName="Helvetica", fontSize=11, textColor=VERDE_CLARO,
            alignment=TA_CENTER, spaceAfter=4, letterSpacing=4),

        "cover_title": ParagraphStyle("cover_title",
            fontName="Helvetica-Bold", fontSize=46, textColor=BRANCO,
            alignment=TA_CENTER, leading=52, spaceAfter=10),

        "cover_sub": ParagraphStyle("cover_sub",
            fontName="Helvetica", fontSize=14, textColor=VERDE_MENTA,
            alignment=TA_CENTER, spaceAfter=6, leading=20),

        "cover_tagline": ParagraphStyle("cover_tagline",
            fontName="Helvetica-Oblique", fontSize=12, textColor=AMARELO_OURO,
            alignment=TA_CENTER, spaceAfter=8),

        "cover_pill": ParagraphStyle("cover_pill",
            fontName="Helvetica-Bold", fontSize=9, textColor=BRANCO,
            alignment=TA_CENTER),

        "section_title": ParagraphStyle("section_title",
            fontName="Helvetica-Bold", fontSize=26, textColor=VERDE_ESCURO,
            spaceBefore=8, spaceAfter=4, leading=30),

        "section_sub": ParagraphStyle("section_sub",
            fontName="Helvetica", fontSize=12, textColor=VERDE_MEDIO,
            spaceAfter=10, leading=16),

        "dish_name": ParagraphStyle("dish_name",
            fontName="Helvetica-Bold", fontSize=13, textColor=PRETO_RICO,
            spaceAfter=2),

        "dish_desc": ParagraphStyle("dish_desc",
            fontName="Helvetica", fontSize=9.5, textColor=CINZA_TEXTO,
            spaceAfter=4, leading=14),

        "price": ParagraphStyle("price",
            fontName="Helvetica-Bold", fontSize=14, textColor=AMARELO_OURO,
            spaceAfter=6),

        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=10, textColor=CINZA_TEXTO,
            spaceAfter=6, leading=15, alignment=TA_JUSTIFY),

        "step_num": ParagraphStyle("step_num",
            fontName="Helvetica-Bold", fontSize=28, textColor=VERDE_CLARO,
            alignment=TA_CENTER),

        "step_title": ParagraphStyle("step_title",
            fontName="Helvetica-Bold", fontSize=12, textColor=VERDE_ESCURO,
            spaceAfter=2),

        "step_body": ParagraphStyle("step_body",
            fontName="Helvetica", fontSize=9.5, textColor=CINZA_TEXTO,
            leading=14),

        "cta_title": ParagraphStyle("cta_title",
            fontName="Helvetica-Bold", fontSize=22, textColor=BRANCO,
            alignment=TA_CENTER, spaceAfter=8),

        "cta_body": ParagraphStyle("cta_body",
            fontName="Helvetica", fontSize=11, textColor=VERDE_MENTA,
            alignment=TA_CENTER, leading=16),

        "kit_title": ParagraphStyle("kit_title",
            fontName="Helvetica-Bold", fontSize=13, textColor=PRETO_RICO,
            spaceAfter=3),

        "kit_desc": ParagraphStyle("kit_desc",
            fontName="Helvetica", fontSize=9, textColor=CINZA_TEXTO,
            leading=13),

        "kit_badge": ParagraphStyle("kit_badge",
            fontName="Helvetica-Bold", fontSize=8, textColor=VERDE_ESCURO,
            alignment=TA_CENTER),
    }


# ─── BUILDER ─────────────────────────────────────────────────────────────────
def build_cover(S):
    items = []
    items.append(Spacer(1, 2.5 * cm))
    items.append(Paragraph("✦  CASA CELI  ✦", S["cover_brand"]))
    items.append(Spacer(1, 0.6 * cm))

    # Linha decorativa dourada
    items.append(DividerLine(color=AMARELO_OURO, thickness=2.5))
    items.append(Spacer(1, 0.5 * cm))

    items.append(Paragraph("CATÁLOGO\nARTESANAL\nPREMIUM", S["cover_title"]))
    items.append(Spacer(1, 0.5 * cm))
    items.append(DividerLine(color=AMARELO_OURO, thickness=2.5))
    items.append(Spacer(1, 1 * cm))

    items.append(Paragraph(
        "Congelados artesanais com sabor de cozinha afetiva",
        S["cover_sub"]))
    items.append(Spacer(1, 0.4 * cm))
    items.append(Paragraph(
        '"Comida feita hoje para facilitar o seu amanhã."',
        S["cover_tagline"]))

    items.append(Spacer(1, 1.8 * cm))

    # 3 Pills de proposta de valor
    pills_data = [
        ["🫕 Artesanal", "🕐 Prático", "🏆 Qualidade"],
        [
            "Receitas com carinho\ne cuidado",
            "Organize sua rotina\nda semana",
            "Congelado com segurança\ne embalagem própria"
        ]
    ]
    pill_table = Table(pills_data, colWidths=[145, 145, 145])
    pill_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), VERDE_MEDIO),
        ("BACKGROUND",  (0, 1), (-1, 1), colors.HexColor("#2D6A4F")),
        ("TEXTCOLOR",   (0, 0), (-1, -1), BRANCO),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME",    (0, 1), (-1, 1), "Helvetica"),
        ("FONTSIZE",    (0, 0), (-1, 0), 11),
        ("FONTSIZE",    (0, 1), (-1, 1), 8.5),
        ("ALIGN",       (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 0), (-1, 0), [VERDE_MEDIO]),
        ("TOPPADDING",  (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("ROUNDEDCORNERS", [8]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#1A4535")),
        ("LEADING",     (0, 1), (-1, 1), 13),
    ]))
    items.append(pill_table)

    items.append(Spacer(1, 2.5 * cm))

    # Linha de anos e emojis
    items.append(Paragraph("🥘  🍱  🥗  🫙  🍝  🫕", ParagraphStyle("emojis",
        fontName="Helvetica", fontSize=18, textColor=VERDE_CLARO,
        alignment=TA_CENTER, spaceAfter=8)))

    items.append(Spacer(1, 0.8 * cm))
    items.append(DividerLine(color=colors.HexColor("#2D6A4F"), thickness=1))

    return items


def build_tradicional(S):
    items = []

    # Header da seção
    items.append(Spacer(1, 0.5 * cm))
    items.append(Paragraph("Linha Tradicional", S["section_title"]))
    items.append(Paragraph(
        "Marmitas práticas para o dia a dia, com combinações equilibradas e tempero caseiro.",
        S["section_sub"]))
    items.append(DividerLine(color=VERDE_CLARO))
    items.append(Spacer(1, 0.4 * cm))

    # Tabela de tamanhos e preços
    size_data = [
        ["TAMANHO", "PREÇO"],
        ["300g", "R$ 18,00"],
        ["400g", "R$ 20,00"],
        ["500g", "R$ 22,00"],
    ]
    size_table = Table(size_data, colWidths=[200, 200])
    size_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), VERDE_ESCURO),
        ("TEXTCOLOR",     (0, 0), (-1, 0), AMARELO_OURO),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0), 10),
        ("BACKGROUND",    (0, 1), (-1, -1), VERDE_MENTA),
        ("TEXTCOLOR",     (0, 1), (-1, -1), VERDE_ESCURO),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 1), (-1, -1), 11),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [VERDE_MENTA, BRANCO]),
        ("GRID",          (0, 0), (-1, -1), 0.5, VERDE_CLARO),
        ("ROUNDEDCORNERS", [6]),
    ]))
    items.append(size_table)
    items.append(Spacer(1, 0.5 * cm))

    pratos = [
        ("🍗", "Frango Desfiado",
         "Creme de milho cremoso, arroz branco soltinho e brócolis no vapor.",
         "A partir de R$ 18,00", "ALTA ACEITAÇÃO"),
        ("🍛", "Frango em Cubos Acebolado",
         "Frango macio com cebolas caramelizadas, arroz, feijão e misto de legumes.",
         "A partir de R$ 18,00", "EQUILIBRADO"),
        ("🍱", "Frango Xadrez",
         "Clássico agridoce com arroz, feijão e mix de cenoura e vagem crocante.",
         "A partir de R$ 18,00", "SUCESSO"),
        ("🍯", "Filé de Frango ao Molho de Mel",
         "Filé suculento ao mel, arroz, feijão e abobrinha grelhada.",
         "A partir de R$ 18,00", "TOQUE ESPECIAL"),
        ("🐟", "Filé de Merluza",
         "Filé delicado de merluza, arroz branco e couve-flor gratinada.",
         "A partir de R$ 18,00", "LEVE"),
        ("🍝", "Almôndegas ao Molho",
         "Almôndegas artesanais ao molho especial, arroz, feijão e mix de legumes.",
         "A partir de R$ 18,00", "CLÁSSICO"),
    ]

    # Cards em grid 2 colunas
    cards_row = []
    for i, (emoji, nome, desc, preco, badge) in enumerate(pratos):
        card = DishCard(emoji, nome, desc, preco, badge, card_h=138, accent=VERDE_MEDIO)
        cards_row.append(card)
        if len(cards_row) == 2:
            row_table = Table([[cards_row[0], cards_row[1]]], colWidths=[238, 238])
            row_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]))
            items.append(row_table)
            cards_row = []

    if cards_row:  # ímpares
        pad = Spacer(238, 1)
        row_table = Table([[cards_row[0], pad]], colWidths=[238, 238])
        row_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        items.append(row_table)

    return items


def build_premium(S):
    items = []
    items.append(Spacer(1, 0.4 * cm))

    # Banner Premium
    banner_data = [["✦  LINHA PREMIUM  ✦\nReceitas especiais caprichadas · 400g"]]
    banner = Table(banner_data, colWidths=[W - 4 * cm])
    banner.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), LARANJA_QUENTE),
        ("TEXTCOLOR",     (0, 0), (-1, -1), BRANCO),
        ("FONTNAME",      (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 14),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("ROUNDEDCORNERS", [10]),
        ("LEADING",       (0, 0), (-1, -1), 20),
    ]))
    items.append(banner)
    items.append(Spacer(1, 0.5 * cm))

    pratos_premium = [
        ("🍖", "Parmegiana de Frango ou Carne",
         "Molho de tomates frescos, queijo derretido generoso, arroz e batatinhas douradas.",
         "R$ 28,50", "PREMIUM ⭐"),
        ("🥘", "Escondidinho Caprichado",
         "Carne, frango ou costela bovina desfiada — cremoso e irresistível.",
         "R$ 24,50", "FAVORITO"),
        ("🫕", "Panquecas Caseiras",
         "Frango com catupiry cremoso ou presunto e queijo — massa fina e artesanal.",
         "R$ 23,50", "ARTESANAL"),
        ("🍝", "Nhoque Tradicional à Bolonhesa",
         "Massa leve e macia com molho ragu de carne e ervas finas selecionadas.",
         "R$ 33,50", "CHEF ⭐"),
        ("🍕", "Lasanha Saborosa",
         "Camadas generosas com molho apurado, recheio especial e toque artesanal.",
         "R$ 26,00", "CLÁSSICO"),
        ("🍜", "Macarrões da Casa",
         "Bolonhesa robusta, quatro queijos gratinado ou bechamel cremoso — sob encomenda.",
         "R$ 24,90", "SOB ENCOMENDA"),
    ]

    cards_row = []
    for emoji, nome, desc, preco, badge in pratos_premium:
        card = DishCard(emoji, nome, desc, preco, badge, card_h=140, accent=LARANJA_QUENTE)
        cards_row.append(card)
        if len(cards_row) == 2:
            row_table = Table([[cards_row[0], cards_row[1]]], colWidths=[238, 238])
            row_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]))
            items.append(row_table)
            cards_row = []

    if cards_row:
        pad = Spacer(238, 1)
        row_table = Table([[cards_row[0], pad]], colWidths=[238, 238])
        row_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        items.append(row_table)

    return items


def build_kits(S):
    items = []
    items.append(Spacer(1, 0.5 * cm))
    items.append(Paragraph("Kits Casa Celi", S["section_title"]))
    items.append(Paragraph(
        "Combos pensados para organizar sua rotina com praticidade e economia.",
        S["section_sub"]))
    items.append(DividerLine(color=VERDE_CLARO))
    items.append(Spacer(1, 0.4 * cm))

    # 3 kits em cards coloridos
    kits = [
        ("🥗", "Kit Semana Leve",
         "10 marmitas para organizar a rotina com praticidade.",
         "SEMANAL", VERDE_MEDIO),
        ("👨‍👩‍👧‍👦", "Kit Família Prática",
         "20 marmitas para almoço e jantar sem preocupação.",
         "FAMÍLIA", LARANJA_QUENTE),
        ("📦", "Kit Mês Organizado",
         "30 marmitas para abastecer a casa com custo-benefício.",
         "ECONOMIA", VERDE_ESCURO),
    ]

    kit_cells = []
    for emoji, nome, desc, badge, cor in kits:
        cell_data = [
            [Paragraph(emoji, ParagraphStyle("e", fontName="Helvetica", fontSize=28,
                        alignment=TA_CENTER))],
            [Paragraph(badge, ParagraphStyle("b", fontName="Helvetica-Bold", fontSize=7,
                        textColor=BRANCO, alignment=TA_CENTER))],
            [Paragraph(nome, ParagraphStyle("n", fontName="Helvetica-Bold", fontSize=11,
                        textColor=PRETO_RICO, alignment=TA_CENTER, spaceAfter=4))],
            [Paragraph(desc, ParagraphStyle("d", fontName="Helvetica", fontSize=8.5,
                        textColor=CINZA_TEXTO, alignment=TA_CENTER, leading=13))],
            [Paragraph("3% OFF no total", ParagraphStyle("off", fontName="Helvetica-Bold",
                        fontSize=10, textColor=cor, alignment=TA_CENTER))],
        ]
        kit_t = Table(cell_data, colWidths=[140])
        kit_t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), CINZA_SUAVE),
            ("BACKGROUND", (0, 1), (0, 1), cor),
            ("BACKGROUND", (0, 2), (0, -1), BRANCO),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("ROUNDEDCORNERS", [8]),
            ("BOX", (0, 0), (-1, -1), 1, CINZA_SUAVE),
        ]))
        kit_cells.append(kit_t)

    kits_row = Table([kit_cells], colWidths=[156, 156, 156])
    kits_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    items.append(kits_row)

    items.append(Spacer(1, 0.6 * cm))

    # Caldo artesanal destaque
    caldo_data = [["🍲  CALDOS ARTESANAIS  —  500ml  —  R$ 21,90\nOpções quentinhas e confortáveis para completar o pedido."]]
    caldo_t = Table(caldo_data, colWidths=[W - 4 * cm])
    caldo_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE_MENTA),
        ("TEXTCOLOR", (0, 0), (-1, -1), VERDE_ESCURO),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("ROUNDEDCORNERS", [8]),
        ("BOX", (0, 0), (-1, -1), 1.5, VERDE_CLARO),
        ("LEADING", (0, 0), (-1, -1), 18),
    ]))
    items.append(caldo_t)
    items.append(Spacer(1, 0.7 * cm))

    # Como pedir — 3 passos
    items.append(Paragraph("Como Pedir", S["section_title"]))
    items.append(DividerLine(color=VERDE_CLARO))
    items.append(Spacer(1, 0.4 * cm))

    steps = [
        ("1", "Escolha", "Selecione a linha, os pratos e o tamanho desejado."),
        ("2", "Envie", "Mande a lista pelo WhatsApp e confirme disponibilidade."),
        ("3", "Combine", "Finalize pagamento, retirada ou entrega combinada."),
    ]

    step_cells = []
    for num, titulo, desc in steps:
        cell = Table([
            [Paragraph(num, S["step_num"])],
            [Paragraph(titulo, S["step_title"])],
            [Paragraph(desc, S["step_body"])],
        ], colWidths=[140])
        cell.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), VERDE_ESCURO),
            ("BACKGROUND", (0, 1), (-1, -1), BRANCO),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("ROUNDEDCORNERS", [8]),
            ("BOX", (0, 0), (-1, -1), 1, VERDE_CLARO),
            ("LINEBELOW", (0, 0), (-1, 0), 1, VERDE_CLARO),
        ]))
        step_cells.append(cell)

    steps_row = Table([step_cells], colWidths=[156, 156, 156])
    steps_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    items.append(steps_row)

    return items


def build_cta(S):
    items = []
    items.append(Spacer(1, 0.6 * cm))

    cta_data = [[
        Paragraph("📲  Finalize seu Pedido pelo WhatsApp", S["cta_title"]),
    ], [
        Paragraph(
            "Escolha seus pratos, envie a quantidade e combine a entrega.\n"
            "Pagamentos aceitos: Pix · Cartão de Crédito · Débito · Dinheiro",
            S["cta_body"]),
    ], [
        Paragraph("💬  Chame agora e garanta suas marmitas!", ParagraphStyle(
            "cta_call", fontName="Helvetica-Bold", fontSize=13,
            textColor=AMARELO_OURO, alignment=TA_CENTER, spaceBefore=8)),
    ]]

    cta_t = Table(cta_data, colWidths=[W - 4 * cm])
    cta_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE_ESCURO),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("ROUNDEDCORNERS", [12]),
        ("BOX", (0, 0), (-1, -1), 2, AMARELO_OURO),
    ]))
    items.append(cta_t)
    items.append(Spacer(1, 0.6 * cm))

    # Linha final com proposta de valor
    items.append(DividerLine(color=AMARELO_OURO, thickness=2))
    items.append(Spacer(1, 0.4 * cm))
    items.append(Paragraph(
        "Casa Celi • Comida feita hoje para facilitar o seu amanhã.",
        ParagraphStyle("final", fontName="Helvetica-BoldOblique", fontSize=12,
            textColor=VERDE_ESCURO, alignment=TA_CENTER)))

    return items


# ─── MAIN ────────────────────────────────────────────────────────────────────
def generate_pdf(output_path):
    S = make_styles()

    # Capa com fundo especial
    doc_cover = SimpleDocTemplate(
        "/tmp/cover_tmp.pdf",
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=1 * cm, bottomMargin=1 * cm,
    )
    doc_cover.build(build_cover(S), onFirstPage=cover_background, onLaterPages=cover_background)

    # Páginas internas
    doc_main = SimpleDocTemplate(
        "/tmp/main_tmp.pdf",
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
    )

    content = []
    content += build_tradicional(S)
    content += [PageBreak()]
    content += build_premium(S)
    content += [PageBreak()]
    content += build_kits(S)
    content += [PageBreak()]
    content += build_cta(S)

    doc_main.build(content, onFirstPage=page_background, onLaterPages=page_background)

    # Merge cover + main
    import fitz
    doc1 = fitz.open("/tmp/cover_tmp.pdf")
    doc2 = fitz.open("/tmp/main_tmp.pdf")
    doc1.insert_pdf(doc2)
    doc1.set_metadata({
        "title": "Cardápio Casa Celi — Congelados Artesanais",
        "author": "Casa Celi",
        "subject": "Catálogo de Marmitas Artesanais Premium",
        "keywords": "marmitas, congelados, artesanal, casa celi",
        "creator": "Casa Celi Design Studio",
    })
    doc1.save(output_path)
    print(f"✅ PDF gerado: {output_path} ({doc1.page_count} páginas)")


if __name__ == "__main__":
    out = "/home/user/belle-petit-pet-saloon/CasaCeli_Cardapio_Premium.pdf"
    generate_pdf(out)
