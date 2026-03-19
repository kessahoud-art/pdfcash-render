"""
Template Mini-Formation — PDF Cash IA
"""
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from .utils import (
    W, H, ML, MR, TW, DARK, GRAY, LGRAY, BORDER, GREEN, ORANGE, YELLOW,
    clean, hex_to_color, wrap_text, text_height,
    draw_header, draw_footer, tip_box, bullet_item,
    draw_cta_box, draw_brand_footer, cover_base
)

BOTTOM = 50


def generate_formation(content, color=None, author="Formateur Expert"):
    ac_hex = (color.ac if color else None) or "#7c3aed"
    AC = hex_to_color(ac_hex)

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setTitle(clean(content.title or "Mini-Formation"))
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

    def exercise_box(text, num, y):
        text = clean(text)
        if not text:
            return y
        th = text_height(c, text, TW - 28, "Helvetica", 10) + 44
        c.setStrokeColor(GREEN)
        c.setLineWidth(1.5)
        c.rect(ML, y - th, TW, th, stroke=1, fill=0)
        c.setLineWidth(3)
        c.line(ML, y - th, ML, y)
        c.setFillColor(GREEN)
        c.rect(ML, y - 20, 100, 20, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.white)
        c.drawString(ML + 4, y - 13, f"EXERCICE {str(num).zfill(2)}")
        wrap_text(c, text, ML + 14, y - 28, TW - 28, "Helvetica", 10, DARK)
        return y - th - 12

    def retain_box(text, y):
        text = clean(text)
        if not text:
            return y
        th = text_height(c, text, TW - 28, "Helvetica-Bold", 10) + 44
        c.setStrokeColor(YELLOW)
        c.setLineWidth(1.5)
        c.rect(ML, y - th, TW, th, stroke=1, fill=0)
        c.setLineWidth(3)
        c.line(ML, y - th, ML, y)
        c.setFillColor(YELLOW)
        c.rect(ML, y - 20, 80, 20, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(DARK)
        c.drawString(ML + 4, y - 13, "A RETENIR")
        wrap_text(c, text, ML + 14, y - 28, TW - 28, "Helvetica-Bold", 10, DARK)
        return y - th - 12

    # PAGE 1 — COUVERTURE
    c.showPage()
    page_num += 1
    cover_base(c, "MINI-FORMATION", content.title or "", content.subtitle or "",
               content.tagline or "", price, author, AC,
               f"{nb} lecons  |  Exercices pratiques  |  Plan d'action inclus")

    # PAGE 2 — PROGRAMME
    y = new_page("PROGRAMME DE FORMATION")
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(DARK)
    c.drawString(ML, y, "Programme de Formation")
    y -= 26
    c.setStrokeColor(AC)
    c.setLineWidth(3)
    c.line(ML, y, ML + 30, y)
    y -= 16

    for i, ch in enumerate(chapters[:6]):
        c.setFillColor(AC)
        c.rect(ML, y - 26, 26, 26, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.white)
        c.drawCentredString(ML + 13, y - 15, str(i+1).zfill(2))
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(ML + 34, y - 10, clean(ch.title or f"Lecon {i+1}"))
        c.setFont("Helvetica", 9)
        c.setFillColor(LGRAY)
        c.drawRightString(W - MR, y - 10, "~12 min")
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.4)
        c.line(ML + 34, y - 26, W - MR, y - 26)
        y -= 32

    # Objectifs
    y -= 14
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(ML, y, W - MR, y)
    y -= 16
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(DARK)
    c.drawString(ML, y, "Objectifs de la Formation")
    y -= 20
    c.setStrokeColor(AC)
    c.setLineWidth(2)
    c.line(ML, y, ML + 25, y)
    y -= 12

    for k in (content.key_takeaways or [])[:5]:
        y = bullet_item(c, k, y, GREEN)

    # LEÇONS
    for i, ch in enumerate(chapters[:6]):
        y = new_page(f"LECON {str(i+1).zfill(2)}")
        lecon_title = clean(ch.title or f"Lecon {i+1}")

        # Badge
        c.setFillColor(AC)
        c.rect(ML, y - 54, 54, 54, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.white)
        c.drawCentredString(ML + 27, y - 14, "LECON")
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(ML + 27, y - 36, str(i+1).zfill(2))

        # Titre
        c.setFont("Helvetica-Bold", 15)
        c.setFillColor(DARK)
        wrap_text(c, lecon_title, ML + 64, y - 12, TW - 64, "Helvetica-Bold", 15, DARK)
        y -= 62

        # Ligne accent
        c.setStrokeColor(AC)
        c.setLineWidth(2)
        c.line(ML, y, W - MR, y)
        y -= 14

        # Durée
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(LGRAY)
        c.drawString(ML, y, "Duree estimee : 10 - 15 minutes  |  Difficulte : Accessible")
        y -= 18

        # Contenu
        content_text = clean(ch.content or "")
        paras = [p.strip() for p in content_text.split('\n') if p.strip() and len(p.strip()) > 5]

        for para in paras:
            is_heading = (para.endswith(':') and len(para) < 80) or para.startswith('**')
            if is_heading:
                head = para.replace('**', '').rstrip(':')
                if not head:
                    continue
                if y < BOTTOM + 40:
                    y = new_page(f"LECON {str(i+1).zfill(2)}")
                y -= 6
                c.setFont("Helvetica-Bold", 11)
                c.setFillColor(AC)
                hh = text_height(c, head, TW, "Helvetica-Bold", 11)
                wrap_text(c, head, ML, y, TW, "Helvetica-Bold", 11, AC)
                y -= hh + 6
            else:
                ph = text_height(c, para, TW, "Helvetica", 10, 3)
                if y - ph < BOTTOM + 8:
                    y = new_page(f"LECON {str(i+1).zfill(2)}")
                wrap_text(c, para, ML, y, TW, "Helvetica", 10, DARK, 3)
                y -= ph + 10

        # Exercice
        exercise_text = paras[-1] if paras else "Applique ce que tu viens d'apprendre et note tes resultats."
        if y < BOTTOM + 80:
            y = new_page(f"LECON {str(i+1).zfill(2)}")
        y -= 6
        y = exercise_box(exercise_text[:300], i+1, y)

        # À retenir
        retain_text = (content.key_takeaways or [])[i] if i < len(content.key_takeaways or []) else \
            "Cette lecon est une etape cle. Reviens la relire si necessaire."
        if y < BOTTOM + 60:
            y = new_page(f"LECON {str(i+1).zfill(2)}")
        y = retain_box(retain_text, y)

    # PAGE FINALE — PLAN D'ACTION
    y = new_page("PLAN D'ACTION")
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(DARK)
    c.drawString(ML, y, "Ton Plan d'Action")
    y -= 26
    c.setStrokeColor(AC)
    c.setLineWidth(3)
    c.line(ML, y, ML + 30, y)
    y -= 16

    for i, action in enumerate((content.key_takeaways or [])[:5]):
        at = clean(action)
        ah = text_height(c, at, TW - 44, "Helvetica", 10)
        if y - max(36, ah + 20) < BOTTOM:
            y = new_page("PLAN D'ACTION")
        c.setFillColor(AC if i < 3 else GREEN)
        c.rect(ML, y - 30, 30, 30, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(colors.white)
        c.drawCentredString(ML + 15, y - 20, str(i+1))
        wrap_text(c, at, ML + 40, y - 8, TW - 44, "Helvetica", 10, DARK)
        y -= max(36, ah + 22)

    y -= 10
    y = draw_cta_box(c, content.call_to_action or "Applique et transforme ta vie !", price, y, AC)
    draw_brand_footer(c, y - 10, AC)

    c.save()
    buf.seek(0)
    return buf.read()
