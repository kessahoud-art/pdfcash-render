"""
Template Guide Pratique — PDF Cash IA
CORRIGE : zero rect/circle fill — compatibilite Android
"""
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from .utils import (
    W, H, ML, MR, TW, BOTTOM, DARK, GRAY, LGRAY, BORDER, GREEN, ORANGE, RED,
    clean, hex_to_color, wrap_text, text_height,
    draw_header, draw_footer, tip_box, error_box, action_box, bullet_item,
    draw_cta_box, draw_brand_footer, cover_base
)

def generate_guide(content, color=None, author="Coach Business Afrique"):
    ac_hex = (color.ac if color else None) or "#059669"
    AC = hex_to_color(ac_hex)

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setTitle(clean(content.title or "Guide Pratique"))
    c.setAuthor(clean(author))
    c.setCreator("PDF Cash IA")

    page_num = 0
    chapters = content.chapters or []
    price = clean(content.price_suggested or "")
    nb = min(len(chapters), 6)

    def new_page(section):
        nonlocal page_num
        c.showPage()
        page_num += 1
        draw_footer(c, page_num, AC)
        return draw_header(c, content.title or "", section, AC)

    # PAGE 1 — COUVERTURE
    c.showPage()
    page_num += 1
    cover_base(c, "GUIDE PRATIQUE", content.title or "", content.subtitle or "",
               content.tagline or "", price, author, AC,
               f"{nb} etapes  |  Actions immediates  |  Resultats mesurables")

    # PAGE 2 — VUE D'ENSEMBLE
    y = new_page("VUE D'ENSEMBLE")
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(DARK)
    c.drawString(ML, y, "Vue d'ensemble du Guide")
    y -= 26
    c.setStrokeColor(AC)
    c.setLineWidth(3)
    c.line(ML, y, ML + 30, y)
    y -= 16

    # Etapes avec numeros colores — ZERO circle fill
    for i, ch in enumerate(chapters[:6]):
        is_last = i == min(len(chapters), 6) - 1

        # Cercle stroke uniquement
        c.setStrokeColor(AC)
        c.setLineWidth(2)
        c.circle(ML + 13, y - 13, 13, stroke=1, fill=0)

        # Numero colore a l'interieur
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(AC)
        c.drawCentredString(ML + 13, y - 17, str(i + 1))

        # Titre etape
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(ML + 34, y - 10, clean(ch.title or f"Etape {i+1}"))

        # Tiret pointille vers suivant
        if not is_last:
            c.setStrokeColor(AC)
            c.setLineWidth(1)
            c.setDash(3, 2)
            c.line(ML + 13, y - 26, ML + 13, y - 36)
            c.setDash()
        y -= (is_last and 30 or 40)

    # Promesse
    y -= 14
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(ML, y, W - MR, y)
    y -= 14

    promesse = clean(content.tagline or content.subtitle or
                     "Applique ce guide et obtiens des resultats en moins de 7 jours.")
    tmp = canvas.Canvas(io.BytesIO(), pagesize=A4)
    ph = text_height(tmp, promesse, TW - 28, "Helvetica-Bold", 11) + 44

    # Encadre promesse stroke uniquement
    c.setStrokeColor(AC)
    c.setLineWidth(1.5)
    c.rect(ML, y - ph, TW, ph, stroke=1, fill=0)
    c.setLineWidth(3)
    c.line(ML, y - ph, ML, y)
    c.setLineWidth(4)
    c.line(ML, y, ML + TW, y)

    # Label PROMESSE texte colore
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(AC)
    c.drawString(ML + 8, y - 13, "PROMESSE")

    wrap_text(c, promesse, ML + 10, y - 28, TW - 20, "Helvetica-Bold", 11, DARK)
    y -= ph + 14

    # ETAPES — 1 par page
    for i, ch in enumerate(chapters[:6]):
        etape_title = clean(ch.title or f"Etape {i+1}")
        y = new_page(f"ETAPE {str(i+1).zfill(2)}")

        # Badge etape — ZERO rect fill
        # Numero en gras colore avec lignes decoratives
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(LGRAY)
        c.drawString(ML, y, "ETAPE")
        y -= 12

        # Grand numero colore
        c.setFont("Helvetica-Bold", 32)
        c.setFillColor(AC)
        c.drawString(ML, y - 26, str(i + 1).zfill(2))

        # Ligne verticale accent a gauche
        c.setStrokeColor(AC)
        c.setLineWidth(3)
        c.line(ML + 46, y + 2, ML + 46, y - 36)

        # Titre a droite du numero
        c.setFont("Helvetica-Bold", 15)
        c.setFillColor(DARK)
        wrap_text(c, etape_title, ML + 56, y - 6, TW - 56, "Helvetica-Bold", 15, DARK)
        y -= 50

        # Ligne accent
        c.setStrokeColor(AC)
        c.setLineWidth(2)
        c.line(ML, y, W - MR, y)
        y -= 14

        # Resultat attendu
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(LGRAY)
        c.drawString(ML, y, "Resultat attendu : appliquer en moins de 24 heures")
        y -= 18

        # Contenu
        content_text = clean(ch.content or "")
        paras = [p.strip() for p in content_text.split('\n') if p.strip() and len(p.strip()) > 5]
        total = len(paras)

        intro = paras[:max(1, total // 4)]
        corps = paras[max(1, total // 4):max(2, total * 3 // 4)]
        fin   = paras[max(2, total * 3 // 4):]

        for para in intro:
            ph = text_height(c, para, TW, "Helvetica", 10, 3)
            if y - ph < BOTTOM + 8:
                y = new_page(f"ETAPE {str(i+1).zfill(2)}")
            wrap_text(c, para, ML, y, TW, "Helvetica", 10, DARK, 3)
            y -= ph + 10

        for para in corps:
            bh = text_height(c, para, TW - 16, "Helvetica", 10)
            if y - bh - 8 < BOTTOM + 8:
                y = new_page(f"ETAPE {str(i+1).zfill(2)}")
            y = bullet_item(c, para, y, AC)

        erreur  = fin[0] if fin else ""
        conseil = fin[1] if len(fin) > 1 else ""
        action  = fin[2] if len(fin) > 2 else "Applique cette etape maintenant et passe a la suivante."

        if erreur:
            if y < BOTTOM + 80:
                y = new_page(f"ETAPE {str(i+1).zfill(2)}")
            y = error_box(c, erreur, y)

        if conseil:
            if y < BOTTOM + 60:
                y = new_page(f"ETAPE {str(i+1).zfill(2)}")
            y = tip_box(c, conseil, y, AC, "CONSEIL PRO")

        if y < BOTTOM + 60:
            y = new_page(f"ETAPE {str(i+1).zfill(2)}")
        y = action_box(c, action, y)

    # PAGE FINALE — CHECKLIST
    y = new_page("CHECKLIST FINALE")
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(DARK)
    c.drawString(ML, y, "Checklist de Completion")
    y -= 26
    c.setStrokeColor(AC)
    c.setLineWidth(3)
    c.line(ML, y, ML + 30, y)
    y -= 16

    c.setFont("Helvetica", 10)
    c.setFillColor(GRAY)
    c.drawString(ML, y, "Coche chaque etape une fois completee :")
    y -= 18

    for i, ch in enumerate(chapters[:6]):
        # Checkbox stroke uniquement
        c.setStrokeColor(AC)
        c.setLineWidth(1.5)
        c.rect(ML, y - 16, 16, 16, stroke=1, fill=0)
        c.setFont("Helvetica", 10)
        c.setFillColor(DARK)
        c.drawString(ML + 24, y - 12, f"Etape {i+1} : {clean(ch.title or '')}")
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.3)
        c.line(ML + 24, y - 18, W - MR, y - 18)
        y -= 26

    # Points cles
    y -= 14
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(ML, y, W - MR, y)
    y -= 14
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(DARK)
    c.drawString(ML, y, "Points Cles a Retenir")
    y -= 20
    c.setStrokeColor(AC)
    c.setLineWidth(2)
    c.line(ML, y, ML + 25, y)
    y -= 12

    for k in (content.key_takeaways or []):
        kt = clean(k)
        if not kt:
            continue
        kh = text_height(c, kt, TW - 16, "Helvetica", 10)
        if y - kh < BOTTOM + 14:
            y = new_page("CHECKLIST FINALE")
        c.setStrokeColor(AC)
        c.setLineWidth(3)
        c.line(ML, y, ML, y - kh - 4)
        wrap_text(c, kt, ML + 12, y, TW - 16, "Helvetica", 10, DARK)
        y -= kh + 14

    y -= 10
    y = draw_cta_box(c, content.call_to_action or "Commence l'etape 1 maintenant !", price, y, AC)
    draw_brand_footer(c, y - 10, AC)

    c.save()
    buf.seek(0)
    return buf.read()
