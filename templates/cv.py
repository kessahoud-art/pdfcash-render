"""
Template CV Pro — PDF Cash IA
CORRIGE : zero rect().fill() — compatibilite Android
"""
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from .utils import (
    W, H, ML, MR, TW, BOTTOM, DARK, GRAY, LGRAY, BORDER, GREEN,
    clean, hex_to_color, wrap_text, text_height,
    draw_footer, draw_brand_footer
)

def generate_cv(content, color=None, author="Candidat"):
    ac_hex = (color.ac if color else None) or "#2C3E50"
    AC = hex_to_color(ac_hex)

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setTitle(clean(content.title or "Curriculum Vitae"))
    c.setAuthor(clean(author))
    c.setCreator("PDF Cash IA")

    page_num = 1
    chapters = content.chapters or []

    c.showPage()
    draw_footer(c, page_num, AC)

    # ── EN-TETE CV — zero fill, lignes uniquement ──
    # Ligne epaisse en haut
    c.setStrokeColor(AC)
    c.setLineWidth(6)
    c.line(0, H - 3, W, H - 3)

    # Ligne fine sous le nom
    c.setStrokeColor(AC)
    c.setLineWidth(1.5)
    c.line(ML, H - 110, W - MR, H - 110)

    # Nom
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(DARK)
    c.drawString(ML, H - 38, clean(author))

    # Titre poste
    job_title = clean(content.title or "").replace("CV Pro pour", "").replace("CV pour", "").strip()
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(AC)
    c.drawString(ML, H - 58, job_title[:70])

    # Contact
    c.setFont("Helvetica", 10)
    c.setFillColor(GRAY)
    c.drawString(ML, H - 76, "Afrique francophone  |  WhatsApp disponible  |  pro@email.com")

    # Ligne accent sous contact
    c.setStrokeColor(AC)
    c.setLineWidth(2)
    c.line(ML, H - 95, W - MR, H - 95)

    y = H - 120

    def skill_bar_line(name, level, yy):
        """Barre de competence en lignes — zero fill."""
        # Nom
        c.setFont("Helvetica", 9)
        c.setFillColor(DARK)
        c.drawString(ML, yy, clean(name))

        # Barre fond — stroke uniquement
        bar_w = 100
        c.setStrokeColor(BORDER)
        c.setLineWidth(6)
        c.line(ML + 130, yy + 4, ML + 130 + bar_w, yy + 4)

        # Barre remplie — ligne coloree epaisse
        filled = bar_w * level / 100
        c.setStrokeColor(AC)
        c.setLineWidth(6)
        c.line(ML + 130, yy + 4, ML + 130 + filled, yy + 4)

        return yy - 20

    def sec_title(label, yy):
        yy -= 8
        # Label en gras colore
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(AC)
        c.drawString(ML, yy, label.upper())
        yy -= 14
        # Ligne accent
        c.setStrokeColor(AC)
        c.setLineWidth(1.5)
        c.line(ML, yy, W - MR, yy)
        yy -= 10
        return yy

    def exp_item(poste, entreprise, periode, desc, yy):
        if yy < BOTTOM + 60:
            c.showPage()
            nonlocal page_num
            page_num += 1
            draw_footer(c, page_num, AC)
            yy = H - 40

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK)
        c.drawString(ML, yy, clean(poste))
        c.setFont("Helvetica", 9)
        c.setFillColor(LGRAY)
        c.drawRightString(W - MR, yy, clean(periode))
        yy -= 15

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(AC)
        c.drawString(ML, yy, clean(entreprise))
        yy -= 14

        if desc:
            lines = [l.strip() for l in clean(desc).split('.') if len(l.strip()) > 5][:4]
            for line in lines:
                lh = text_height(c, line, TW - 14, "Helvetica", 9, 1)
                c.setFont("Helvetica-Bold", 9)
                c.setFillColor(AC)
                c.drawString(ML, yy, "-")
                c.setFont("Helvetica", 9)
                c.setFillColor(GRAY)
                wrap_text(c, line, ML + 12, yy, TW - 14, "Helvetica", 9, GRAY, 1)
                yy -= lh + 5
        yy -= 8
        return yy

    # Resume
    y = sec_title("Resume Professionnel", y)
    desc = clean(content.description or (chapters[0].content[:400] if chapters else ""))
    if desc:
        dh = text_height(c, desc, TW, "Helvetica", 10, 2)
        wrap_text(c, desc, ML, y, TW, "Helvetica", 10, DARK, 2)
        y -= dh + 10

    # Experiences
    y = sec_title("Experiences Professionnelles", y)
    for i, ch in enumerate(chapters[:4]):
        parts = clean(ch.title or "").split("-")
        poste = parts[0].strip() if parts else clean(ch.title or "")
        entreprise = parts[1].strip() if len(parts) > 1 else "Entreprise Afrique"
        periode = parts[2].strip() if len(parts) > 2 else f"{2024 - i} - {'Present' if i == 0 else str(2023 - i)}"
        y = exp_item(poste, entreprise, periode, ch.content or "", y)

    # Formation
    y = sec_title("Formation", y)
    toc = content.table_of_contents or []
    diplome = clean(toc[4]) if len(toc) >= 5 else "Licence professionnelle"
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(DARK)
    c.drawString(ML, y, diplome)
    c.setFont("Helvetica", 9)
    c.setFillColor(LGRAY)
    c.drawRightString(W - MR, y, "2018")
    y -= 14
    c.setFont("Helvetica", 9)
    c.setFillColor(AC)
    c.drawString(ML, y, "Universite Afrique francophone")
    y -= 22

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(DARK)
    c.drawString(ML, y, "Baccalaureat")
    c.setFont("Helvetica", 9)
    c.setFillColor(LGRAY)
    c.drawRightString(W - MR, y, "2015")
    y -= 14
    c.setFont("Helvetica", 9)
    c.setFillColor(AC)
    c.drawString(ML, y, "Lycee Excellence")
    y -= 22

    # Competences — barres en lignes
    y = sec_title("Competences", y)
    skills = (content.key_takeaways or [])[:6]
    saved_y = y
    left = skills[:3]
    right = skills[3:]

    for i, sk in enumerate(left):
        y = skill_bar_line(clean(sk)[:28], 95 - i * 10, y)

    ry = saved_y
    for i, sk in enumerate(right):
        rx = W / 2 + 10
        c.setFont("Helvetica", 9)
        c.setFillColor(DARK)
        c.drawString(rx, ry, clean(sk)[:28])
        bar_w = 80
        # Barre fond
        c.setStrokeColor(BORDER)
        c.setLineWidth(6)
        c.line(rx + 130, ry + 4, rx + 130 + bar_w, ry + 4)
        # Barre remplie
        filled = bar_w * (90 - i * 10) / 100
        c.setStrokeColor(AC)
        c.setLineWidth(6)
        c.line(rx + 130, ry + 4, rx + 130 + filled, ry + 4)
        ry -= 20

    y = min(y, ry)

    # Langues
    y = sec_title("Langues", y)
    for lang, lvl in [("Francais", 100), ("Anglais", 65), ("Langue locale", 100)]:
        y = skill_bar_line(lang, lvl, y)

    # Pied de page CV
    if y > BOTTOM + 25:
        y -= 10
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.5)
        c.line(ML, y, W - MR, y)
        y -= 12
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(AC)
        c.drawCentredString(W / 2, y, "Disponible immediatement — References disponibles sur demande")

    c.save()
    buf.seek(0)
    return buf.read()
