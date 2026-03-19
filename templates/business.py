"""
Template Business Plan — PDF Cash IA
"""
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from .utils import (
    W, H, ML, MR, TW, DARK, GRAY, LGRAY, BORDER, GREEN, ORANGE, RED,
    clean, hex_to_color, wrap_text, text_height,
    draw_header, draw_footer, section_title,
    tip_box, bullet_item, draw_table,
    draw_cta_box, draw_brand_footer, metric_boxes, cover_base
)

BOTTOM = 50

def generate_business(content, color=None, author="Consultant Business"):
    ac_hex = (color.ac if color else None) or "#1a5276"
    AC = hex_to_color(ac_hex)

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setTitle(clean(content.title or "Business Plan"))
    c.setAuthor(clean(author))
    c.setCreator("PDF Cash IA")

    page_num = 0
    chapters = content.chapters or []
    price = clean(content.price_suggested or "50 000 FCFA")
    pn = int(''.join(filter(str.isdigit, price)) or '50000')

    def new_page(section):
        nonlocal page_num
        c.showPage()
        page_num += 1
        draw_footer(c, page_num, AC)
        return draw_header(c, content.title or "", section, AC)

    def para(text, y, section):
        t = clean(text)
        if not t or len(t) < 5:
            return y
        ph = text_height(c, t, TW, "Helvetica", 10, 3)
        if y - ph < BOTTOM + 8:
            nonlocal_y = new_page(section)
            y = nonlocal_y
        wrap_text(c, t, ML, y, TW, "Helvetica", 10, DARK, 3)
        return y - ph - 10

    # PAGE 1 — COUVERTURE
    c.showPage()
    page_num += 1
    cover_base(c, "BUSINESS PLAN", content.title or "", content.subtitle or "",
               content.tagline or "", price, author, AC,
               f"Projection 12 mois  |  Plan financier  |  Marche africain")

    # PAGE 2 — TABLE DES MATIÈRES
    y = new_page("TABLE DES MATIERES")
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(DARK)
    c.drawString(ML, y, "Table des Matieres")
    y -= 26
    c.setStrokeColor(AC)
    c.setLineWidth(3)
    c.line(ML, y, ML + 30, y)
    y -= 16

    sections_bp = ["Resume Executif", "Presentation du Projet", "Etude de Marche",
                   "Plan Financier", "Strategie Marketing", "Projections et Objectifs"]
    for i, s in enumerate(sections_bp):
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(AC)
        c.drawString(ML, y, str(i+1).zfill(2))
        c.setFont("Helvetica", 11)
        c.setFillColor(DARK)
        c.drawString(ML + 36, y, s)
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.4)
        c.line(ML + 36, y - 4, W - MR, y - 4)
        y -= 20

    if content.description:
        y -= 14
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(GRAY)
        dh = text_height(c, clean(content.description), TW, "Helvetica-Oblique", 10)
        wrap_text(c, clean(content.description), ML, y, TW, "Helvetica-Oblique", 10, GRAY)
        y -= dh + 10

    # SECTIONS
    section_names = ["RESUME EXECUTIF", "PRESENTATION DU PROJET", "ETUDE DE MARCHE",
                     "PLAN FINANCIER", "STRATEGIE MARKETING", "PROJECTIONS"]

    for i, ch in enumerate(chapters[:6]):
        y = new_page(section_names[i] if i < len(section_names) else f"SECTION {i+1}")
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(LGRAY)
        c.drawString(ML, y, f"{i+1}. {sections_bp[i] if i < len(sections_bp) else ''}")
        y -= 14
        c.setStrokeColor(AC)
        c.setLineWidth(2)
        c.line(ML, y, W - MR, y)
        y -= 12

        paras = [p.strip() for p in clean(ch.content or "").split('\n') if p.strip() and len(p.strip()) > 5]
        for p_text in paras[:8]:
            ph = text_height(c, p_text, TW, "Helvetica", 10, 3)
            if y - ph < BOTTOM + 8:
                y = new_page(section_names[i] if i < len(section_names) else f"SECTION {i+1}")
            wrap_text(c, p_text, ML, y, TW, "Helvetica", 10, DARK, 3)
            y -= ph + 10

        # Section plan financier — ajouter tableau
        if i == 3 and y > BOTTOM + 80:
            y -= 10
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(DARK)
            c.drawString(ML, y, "Projections de Revenus (12 mois)")
            y -= 18
            rows = []
            for m in range(1, 7):
                ventes = 5 + m * 3
                ca = ventes * (pn // 10)
                rows.append([f"Mois {m}", f"{ventes} ventes", f"{ca:,} FCFA".replace(",", " "),
                              "Beneficiaire" if m >= 4 else "Investissement"])
            y = draw_table(c, ["Periode", "Ventes", "CA Previsionnel", "Statut"],
                           rows, y, AC, [70, 80, 130, 205])

    # PAGE FINALE — CTA
    y = new_page("CONCLUSION")
    for k in (content.key_takeaways or [])[:5]:
        y = bullet_item(c, k, y, AC)

    y -= 10
    y = draw_cta_box(c, content.call_to_action or "Passez a l'action maintenant !", price, y, AC)
    draw_brand_footer(c, y - 10, AC)

    c.save()
    buf.seek(0)
    return buf.read()
