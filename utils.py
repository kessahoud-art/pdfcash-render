"""
Utilitaires communs — PDF Cash IA
Fonctions réutilisables pour tous les templates ReportLab
"""
import re
import unicodedata
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ── DIMENSIONS A4 ──
W, H = A4
ML = 55   # marge gauche
MR = 55   # marge droite
TW = W - ML - MR  # largeur utile

# ── COULEURS COMMUNES ──
DARK   = colors.HexColor("#1A1A2E")
GRAY   = colors.HexColor("#555577")
LGRAY  = colors.HexColor("#9898B8")
BORDER = colors.HexColor("#D8DCE8")
WHITE  = colors.white
GREEN  = colors.HexColor("#16A34A")
ORANGE = colors.HexColor("#D97706")
RED    = colors.HexColor("#B91C1C")
YELLOW = colors.HexColor("#EAB308")

def clean(text):
    """Nettoie le texte : supprime emojis, normalise les caractères."""
    if not text:
        return ""
    text = str(text)
    # Supprimer emojis
    text = re.sub(r'[\U0001F000-\U0001FFFF]', '', text)
    text = re.sub(r'[\u2600-\u27BF]', '', text)
    # Normaliser accents
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Nettoyer espaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def hex_to_color(hex_str, fallback="#7c3aed"):
    """Convertit un code hex en couleur ReportLab."""
    try:
        return colors.HexColor(hex_str or fallback)
    except Exception:
        return colors.HexColor(fallback)

def wrap_text(c, text, x, y, width, font, size, color, line_gap=2):
    """
    Écrit du texte avec retour à la ligne automatique.
    Retourne le nouveau Y après écriture.
    """
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line = ""
    lines = []
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font, size) <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    for l in lines:
        c.drawString(x, y, l)
        y -= (size + line_gap)
    return y - 4

def text_height(c, text, width, font, size, line_gap=2):
    """Calcule la hauteur qu'occupera un texte."""
    c.setFont(font, size)
    words = text.split()
    line = ""
    lines = []
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font, size) <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return len(lines) * (size + line_gap)

def draw_header(c, title, section, ac_color, page_num=None):
    """Dessine l'en-tête standard sur chaque page intérieure."""
    # Ligne accent en haut
    c.setStrokeColor(ac_color)
    c.setLineWidth(3)
    c.line(0, H, W, H)

    # Titre à gauche
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(GRAY)
    c.drawString(ML, H - 14, clean(title)[:55])

    # Section à droite
    c.setFont("Helvetica", 7)
    c.setFillColor(LGRAY)
    c.drawRightString(W - MR, H - 14, clean(section))

    # Séparateur
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(ML, H - 22, W - MR, H - 22)

    return H - 34  # y de départ après header

def draw_footer(c, page_num, ac_color):
    """Dessine le pied de page standard."""
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(ML, 22, W - MR, 22)

    c.setFont("Helvetica", 7)
    c.setFillColor(LGRAY)
    c.drawCentredString(W / 2, 10, "PDF Cash IA  -  pdfcash-ia.vercel.app")

    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(ac_color)
    c.drawRightString(W - MR, 10, str(page_num))

def section_title(c, text, y, ac_color, num=None):
    """
    Dessine un titre de section avec numéro optionnel et ligne accent.
    Retourne le nouveau Y.
    """
    y -= 6
    if num is not None:
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(LGRAY)
        c.drawString(ML, y, f"PARTIE {str(num).zfill(2)}")
        y -= 14

    label = clean(text).upper()
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(LGRAY)
    c.drawString(ML, y, label)
    y -= 14

    c.setStrokeColor(ac_color)
    c.setLineWidth(2)
    c.line(ML, y, ML + 40, y)
    y -= 12

    return y

def tip_box(c, text, y, ac_color, label="CONSEIL"):
    """Encadré conseil avec bordure colorée à gauche."""
    text = clean(text)
    if not text:
        return y

    # Calculer hauteur
    from reportlab.pdfgen import canvas as cv_module
    import io
    tmp = canvas.Canvas(io.BytesIO(), pagesize=A4)
    h = text_height(tmp, text, TW - 24, "Helvetica", 10) + 28

    # Bordure
    c.setStrokeColor(ac_color)
    c.setLineWidth(1.5)
    c.rect(ML, y - h, TW, h, stroke=1, fill=0)

    # Barre gauche
    c.setLineWidth(4)
    c.line(ML, y - h, ML, y)

    # Label
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(ac_color)
    c.drawString(ML + 8, y - 12, label)

    # Texte
    wrap_text(c, text, ML + 8, y - 24, TW - 24, "Helvetica", 10, DARK)

    return y - h - 10

def warning_box(c, text, y, label="IMPORTANT"):
    """Encadré avertissement en orange."""
    return tip_box(c, text, y, ORANGE, label)

def error_box(c, text, y, label="ERREUR A EVITER"):
    """Encadré erreur en rouge."""
    return tip_box(c, text, y, RED, label)

def action_box(c, text, y, label="ACTION IMMEDIATE"):
    """Encadré action en orange."""
    return tip_box(c, text, y, ORANGE, label)

def bullet_item(c, text, y, ac_color, indent=0):
    """Point de liste avec tiret coloré. Retourne le nouveau Y."""
    text = clean(text)
    if not text:
        return y

    x = ML + indent
    w = TW - indent - 14

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(ac_color)
    c.drawString(x, y, "-")

    h = text_height(c, text, w, "Helvetica", 10)
    wrap_text(c, text, x + 14, y, w, "Helvetica", 10, DARK)

    return y - h - 8

def draw_table(c, headers, rows, y, ac_color, col_widths=None):
    """
    Dessine un tableau avec en-tête coloré.
    Retourne le nouveau Y.
    """
    n_cols = len(headers)
    if col_widths is None:
        col_widths = [TW / n_cols] * n_cols

    row_h = 22

    # En-tête
    c.setFillColor(ac_color)
    c.rect(ML, y - row_h, TW, row_h, stroke=0, fill=1)
    x = ML
    for i, h in enumerate(headers):
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(WHITE)
        c.drawString(x + 4, y - row_h + 8, clean(h))
        x += col_widths[i]
    y -= row_h

    # Lignes de données
    for ri, row in enumerate(rows):
        # Fond alterné
        if ri % 2 == 0:
            c.setFillColor(colors.HexColor("#F0F4FF"))
            c.rect(ML, y - row_h, TW, row_h, stroke=0, fill=1)

        x = ML
        for ci, cell in enumerate(row):
            c.setFont("Helvetica", 9)
            c.setFillColor(DARK)
            c.drawString(x + 4, y - row_h + 8, clean(str(cell)))
            x += col_widths[ci]

        # Bordures colonnes
        x = ML
        for w in col_widths[:-1]:
            x += w
            c.setStrokeColor(BORDER)
            c.setLineWidth(0.3)
            c.line(x, y - row_h, x, y)

        y -= row_h

    # Bordure extérieure
    total_h = (len(rows) + 1) * row_h
    c.setStrokeColor(BORDER)
    c.setLineWidth(1)
    c.rect(ML, y, TW, total_h, stroke=1, fill=0)

    return y - 12

def draw_cta_box(c, text, price, y, ac_color):
    """Dessine le CTA final avec cadre et prix."""
    text = clean(text)
    price = clean(price)

    h_text = text_height(c, text, TW - 30, "Helvetica-Bold", 12) + 50
    box_h = h_text

    c.setStrokeColor(ac_color)
    c.setLineWidth(2)
    c.rect(ML, y - box_h, TW, box_h, stroke=1, fill=0)
    c.setLineWidth(4)
    c.line(ML, y, ML + TW, y)

    wrap_text(c, text, ML + 15, y - 18, TW - 30, "Helvetica-Bold", 12, DARK)

    if price:
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(ac_color)
        c.drawCentredString(W / 2, y - box_h + 12, price)

    return y - box_h - 14

def draw_brand_footer(c, y, ac_color):
    """Ligne de marque finale."""
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(ML, y, W - MR, y)
    y -= 12
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(ac_color)
    c.drawCentredString(W / 2, y, "PDF Cash IA  -  pdfcash-ia.vercel.app")
    return y - 14

def metric_boxes(c, items, y, border=BORDER):
    """
    Dessine des boîtes métriques côte à côte.
    items: list of dict {label, value, color}
    """
    n = len(items)
    bw = (TW - (n - 1) * 8) / n
    bh = 50

    for i, item in enumerate(items):
        bx = ML + i * (bw + 8)
        col = hex_to_color(item.get("color_hex")) if item.get("color_hex") else DARK

        # Bordure
        c.setStrokeColor(border)
        c.setLineWidth(1)
        c.rect(bx, y - bh, bw, bh, stroke=1, fill=0)

        # Ligne accent en haut
        c.setStrokeColor(col)
        c.setLineWidth(3)
        c.line(bx, y, bx + bw, y)

        # Label
        c.setFont("Helvetica", 8)
        c.setFillColor(LGRAY)
        c.drawCentredString(bx + bw / 2, y - 14, clean(item.get("label", "")))

        # Valeur
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(col)
        c.drawCentredString(bx + bw / 2, y - 32, clean(item.get("value", "")))

    return y - bh - 12

def cover_base(c, label, title, subtitle, tagline, price, author, ac_color, infos=""):
    """
    Dessine une couverture minimaliste pro standard.
    Retourne le Y courant après le contenu.
    """
    cx = W / 2

    # Bande fine en haut
    c.setFillColor(ac_color)
    c.rect(0, H - 5, W, 5, stroke=0, fill=1)

    # Label type
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(ac_color)
    c.drawCentredString(cx, H - 28, clean(label).upper())

    # Titre
    title_clean = clean(title)
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(DARK)
    # Calcul hauteur titre
    tmp_h = text_height(c, title_clean, TW, "Helvetica-Bold", 26)
    wrap_text(c, title_clean, ML, H - 65, TW, "Helvetica-Bold", 26, DARK)
    cy = H - 65 - tmp_h - 16

    # Ligne déco
    c.setStrokeColor(ac_color)
    c.setLineWidth(2.5)
    c.line(cx - 50, cy, cx + 50, cy)
    cy -= 18

    # Sous-titre
    if subtitle:
        sub_clean = clean(subtitle)
        sub_h = text_height(c, sub_clean, TW, "Helvetica", 12)
        wrap_text(c, sub_clean, ML, cy, TW, "Helvetica", 12, GRAY)
        cy -= sub_h + 14

    # Tagline
    if tagline:
        tag = '"' + clean(tagline) + '"'
        tag_h = text_height(c, tag, TW, "Helvetica-Oblique", 10)
        wrap_text(c, tag, ML, cy, TW, "Helvetica-Oblique", 10, LGRAY)
        cy -= tag_h + 16

    # Séparateur léger
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.8)
    c.line(cx - 20, cy, cx + 20, cy)
    cy -= 18

    # Infos
    if infos:
        c.setFont("Helvetica", 9)
        c.setFillColor(LGRAY)
        c.drawCentredString(cx, cy, clean(infos))
        cy -= 20

    # Prix
    if price:
        c.setFont("Helvetica", 9)
        c.setFillColor(GRAY)
        c.drawCentredString(cx, cy, "Prix :")
        cy -= 16
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(DARK)
        c.drawCentredString(cx, cy, clean(price))
        cy -= 28

    # Auteur + marque en bas
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(ML, 46, W - MR, 46)

    c.setFont("Helvetica", 8)
    c.setFillColor(LGRAY)
    c.drawString(ML, 32, "Par : " + clean(author))

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(ac_color)
    c.drawRightString(W - MR, 32, "PDF Cash IA")

    c.setFont("Helvetica", 7)
    c.setFillColor(LGRAY)
    c.drawRightString(W - MR, 18, "pdfcash-ia.vercel.app")

    return cy
